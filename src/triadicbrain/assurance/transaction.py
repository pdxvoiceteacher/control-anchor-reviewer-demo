"""Local transaction registry, state machine, recovery, and human decisions.

Candidate bytes are treated as opaque quarantine input.  They are never parsed
as control results, custody events, findings, human decisions, or practitioner
annotations.  Those evidence classes are written only by their authorized
platform planes.
"""

from __future__ import annotations

import base64
import contextlib
import os
import re
import secrets
import time
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import AUTHORITY_EFFECT, NONASSURANCE_NOTICE, PRODUCT_NAME, REPORT_NOTICE, VERSION
from .authorization import Action, AuthorizationError, permission_matrix, require_authorized
from .canonical import (
    CanonicalError,
    canonical_bytes,
    read_ordinary_bytes,
    read_canonical_file,
    replace_bytes_atomic,
    require_existing_root,
    require_new_root,
    require_safe_ancestors,
    require_single_link_file,
    sha256_bytes,
    strict_load_object,
    write_exclusive_bytes,
    write_exclusive_object,
)
from .claims import claim_control_observations, derive_candidate_claim_map
from .controls import (
    CONTROL_IDS,
    P0_CORE,
    P0_WHEN_APPLICABLE,
    P1,
    execute_controls,
    preliminary_platform_observations,
    render_control_catalog_csv,
    render_framework_crosswalk_csv,
)
from .custody import append_event, build_event, ledger_bytes, read_event_ledger, verify_events
from .models import ActorClass, Decision, Plane, TransactionIdentity, TransactionState, require_identifier, validate_transition
from .review_policy import (
    ApprovalEffect,
    ReviewPolicyEvaluationRequest,
    ReviewPolicyProfile,
    ReviewPolicyRegistry,
    discover_review_policy_registry,
    load_review_policy,
)
from .reporting import render_transaction_review_html
from .transition_policy import (
    TransitionPolicyError,
    validate_recovery_event_semantics,
    validate_transition_event_semantics,
)


STORE_SCHEMA_ID = "uvlm.triadicbrain.aep01.evidence_store.v1"
STATE_SCHEMA_ID = "uvlm.triadicbrain.aep01.transaction_state.v1"
JOURNAL_SCHEMA_ID = "uvlm.triadicbrain.aep01.transition_journal.v1"
RECOVERY_SCHEMA_ID = "uvlm.triadicbrain.aep01.transition_recovery_receipt.v1"
CREATION_SCHEMA_ID = "uvlm.triadicbrain.aep01.creation_ledger_event.v1"
CREATION_LOCK_SCHEMA_ID = "uvlm.triadicbrain.aep01.creation_ledger_lock.v1"
SEGREGATION_POSTURE = "LOGICAL_ROLE_SEPARATION"
SIGNING_POSTURE = "HASH_CHAIN_ONLY"
MAX_RAW_BYTES = 32 * 1024 * 1024
_HEX32 = re.compile(r"^[0-9a-f]{32}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_CREATION_LEDGER_LOCK_TIMEOUT_SECONDS = 30.0
_CREATION_LEDGER_LOCK_RETRY_SECONDS = 0.01
_STATE_FIELDS = frozenset(
    {
        "authority_effect",
        "current_state",
        "last_transition_id",
        "logical_time_utc",
        "parent_transaction_id",
        "root_transaction_id",
        "schema_id",
        "sequence",
        "transaction_id",
    }
)


class TransactionError(ValueError):
    """A transaction request failed its bounded local contract."""


class TransitionInterrupted(RuntimeError):
    """A test-controlled transition stopped after a declared target."""


def _utc(value: Any, label: str) -> str:
    if type(value) is not str or not value.endswith("Z") or len(value) > 64:
        raise TransactionError(f"UTC_TIME_INVALID:{label}")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise TransactionError(f"UTC_TIME_INVALID:{label}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise TransactionError(f"UTC_TIME_INVALID:{label}")
    return value


def _text(value: Any, label: str, *, maximum: int = 4096, empty: bool = False) -> str:
    if type(value) is not str or (not empty and not value) or len(value) > maximum:
        raise TransactionError(f"TEXT_INVALID:{label}")
    if unicodedata.normalize("NFC", value) != value:
        raise TransactionError(f"TEXT_NOT_NFC:{label}")
    try:
        value.encode("utf-8", "strict")
    except UnicodeError as exc:
        raise TransactionError(f"TEXT_INVALID:{label}") from exc
    return value


def _bytes(value: Any, label: str) -> bytes:
    if type(value) is not bytes or len(value) > MAX_RAW_BYTES:
        raise TransactionError(f"RAW_BYTES_INVALID:{label}")
    return value


def _read_authoritative_file(
    path: Path,
    label: str,
    *,
    maximum_bytes: int = 64 * 1024 * 1024,
) -> bytes:
    """Read live authoritative bytes only through the stable file primitive."""

    try:
        return read_ordinary_bytes(path, maximum_bytes=maximum_bytes)
    except (OSError, ValueError) as exc:
        raise TransactionError(f"AUTHORITATIVE_FILE_INVALID:{label}") from exc


def _store_root(path: Path) -> Path:
    root = require_existing_root(Path(path))
    manifest = read_canonical_file(root / "store_manifest.json")
    if manifest.get("schema_id") != STORE_SCHEMA_ID:
        raise TransactionError("EVIDENCE_STORE_MANIFEST_INVALID")
    return root


def _transaction_root(store: Path, transaction_id: str) -> Path:
    identifier = require_identifier(transaction_id, "transaction_id")
    candidate = store / "transactions" / identifier
    if not candidate.is_dir() or candidate.is_symlink():
        raise TransactionError("TRANSACTION_NOT_FOUND")
    return require_existing_root(candidate)


def _jsonl(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical_bytes(dict(row)) for row in rows)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    payload = _read_authoritative_file(path, "JSONL")
    if not payload:
        return []
    if not payload.endswith(b"\n"):
        raise TransactionError("JSONL_INVALID")
    rows: list[dict[str, Any]] = []
    for line in payload.splitlines(keepends=True):
        try:
            rows.append(strict_load_object(line))
        except Exception as exc:
            raise TransactionError("JSONL_INVALID") from exc
    if _jsonl(rows) != payload:
        raise TransactionError("JSONL_NOT_CANONICAL")
    return rows


def _normalize_source(payload: bytes) -> tuple[bytes, str]:
    try:
        text = payload.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return b"", "BINARY_SOURCE_NO_TEXT_PROJECTION"
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    if not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8"), "UTF8_NFC_LF_V1"


def _write_or_match(path: Path, payload: bytes) -> None:
    if os.path.lexists(path):
        if _read_authoritative_file(path, path.name) != payload:
            raise TransactionError(f"IMMUTABLE_RECORD_CONFLICT:{path.name}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    write_exclusive_bytes(path, payload)


def create_evidence_store(
    output_root: Path,
    *,
    predecessor_commit: str,
    predecessor_receipt_sha256: str,
    created_at_utc: str,
) -> dict[str, Any]:
    """Create a fresh local evidence store with no model/provider side effect."""

    if not _HEX40.fullmatch(predecessor_commit) or not _HEX64.fullmatch(
        predecessor_receipt_sha256
    ):
        raise TransactionError("PREDECESSOR_IDENTITY_INVALID")
    created = _utc(created_at_utc, "created_at_utc")
    root = require_new_root(Path(output_root))
    root.mkdir()
    for name in (
        "annotations",
        "failure_receipts",
        "packages",
        "periods",
        "repair_intents",
        "transactions",
    ):
        (root / name).mkdir()
    manifest = {
        "authority_effect": AUTHORITY_EFFECT,
        "created_at_utc": created,
        "effects": {
            "deployment_performed": False,
            "memory_written": False,
            "merge_performed": False,
            "network_used": False,
            "provider_invoked": False,
            "publication_performed": False,
            "release_performed": False,
        },
        "nonauthority": NONASSURANCE_NOTICE,
        "predecessor_commit": predecessor_commit,
        "predecessor_receipt_sha256": predecessor_receipt_sha256,
        "product_name": PRODUCT_NAME,
        "product_version": VERSION,
        "schema_id": STORE_SCHEMA_ID,
        "segregation_posture": SEGREGATION_POSTURE,
        "signing_posture": SIGNING_POSTURE,
    }
    write_exclusive_object(root / "store_manifest.json", manifest)
    write_exclusive_object(root / "role_permission_matrix.json", {
        "authority_effect": AUTHORITY_EFFECT,
        "matrix": permission_matrix(),
        "nonauthority": NONASSURANCE_NOTICE,
        "schema_id": "uvlm.triadicbrain.aep01.role_permission_matrix.v1",
    })
    write_exclusive_bytes(root / "creation_ledger.jsonl", b"")
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "creation_ledger_sha256": sha256_bytes(b""),
        "effects": manifest["effects"],
        "result": "PASS",
        "root": str(root),
        "schema_id": "uvlm.triadicbrain.aep01.store_creation_receipt.v1",
        "store_manifest_sha256": sha256_bytes(canonical_bytes(manifest)),
    }


def _creation_event_hash(row: Mapping[str, Any]) -> str:
    return sha256_bytes(canonical_bytes({k: v for k, v in row.items() if k != "event_sha256"}))


@contextlib.contextmanager
def _creation_ledger_lock(store: Path):
    """Serialize creation-ledger writers with a bounded ordinary-file lock.

    The lock is deliberately local and fail-closed: it is never stolen based on
    wall-clock age, and a process that cannot acquire it within the bounded
    interval records no transaction start.  The random owner nonce prevents one
    writer from releasing a substituted lock owned by another writer.
    """

    path = store / ".creation-ledger.lock"
    owner = {
        "authority_effect": AUTHORITY_EFFECT,
        "owner_nonce": secrets.token_hex(32),
        "owner_pid": os.getpid(),
        "schema_id": CREATION_LOCK_SCHEMA_ID,
    }
    payload = canonical_bytes(owner)
    deadline = time.monotonic() + _CREATION_LEDGER_LOCK_TIMEOUT_SECONDS
    while True:
        try:
            write_exclusive_bytes(path, payload)
            break
        except CanonicalError as exc:
            if str(exc) not in {
                "EXCLUSIVE_OUTPUT_EXISTS",
                "FRESH_PATH_ALREADY_EXISTS",
            }:
                raise TransactionError("CREATION_LEDGER_LOCK_INVALID") from exc
            if time.monotonic() >= deadline:
                raise TransactionError("CREATION_LEDGER_LOCK_TIMEOUT") from exc
            time.sleep(_CREATION_LEDGER_LOCK_RETRY_SECONDS)
    try:
        if _read_authoritative_file(
            path, "CREATION_LEDGER_LOCK", maximum_bytes=4096
        ) != payload:
            raise TransactionError("CREATION_LEDGER_LOCK_OWNERSHIP_LOST")
        yield
    finally:
        try:
            if _read_authoritative_file(
                path, "CREATION_LEDGER_LOCK", maximum_bytes=4096
            ) != payload:
                raise TransactionError("CREATION_LEDGER_LOCK_OWNERSHIP_LOST")
            require_single_link_file(path)
            path.unlink()
        except TransactionError:
            raise
        except (CanonicalError, OSError) as exc:
            raise TransactionError("CREATION_LEDGER_LOCK_RELEASE_FAILED") from exc


def _append_creation_event(
    store: Path,
    *,
    transaction_id: str,
    period_id: str,
    parent_transaction_id: str | None,
    logical_time_utc: str,
) -> dict[str, Any]:
    path = store / "creation_ledger.jsonl"
    with _creation_ledger_lock(store):
        before = _read_authoritative_file(path, "CREATION_LEDGER")
        rows: list[dict[str, Any]] = []
        if before:
            for line in before.splitlines(keepends=True):
                rows.append(strict_load_object(line))
            if _jsonl(rows) != before:
                raise TransactionError("CREATION_LEDGER_INVALID")
        if any(row.get("transaction_id") == transaction_id for row in rows):
            raise TransactionError("TRANSACTION_ID_ALREADY_REGISTERED")
        previous = rows[-1]["event_sha256"] if rows else None
        row: dict[str, Any] = {
            "authority_effect": AUTHORITY_EFFECT,
            "event_sha256": "",
            "event_type": "TRANSACTION_REGISTERED",
            "logical_time_utc": logical_time_utc,
            "parent_transaction_id": parent_transaction_id,
            "period_id": period_id,
            "previous_event_sha256": previous,
            "schema_id": CREATION_SCHEMA_ID,
            "sequence": len(rows) + 1,
            "transaction_id": transaction_id,
        }
        row["event_sha256"] = _creation_event_hash(row)
        rows.append(row)
        replace_bytes_atomic(
            path, _jsonl(rows), expected_sha256=sha256_bytes(before)
        )
        # Authenticate the exact post-image before allowing transaction
        # materialization to proceed outside the serialized section.
        if _read_authoritative_file(path, "CREATION_LEDGER") != _jsonl(rows):
            raise TransactionError("CREATION_LEDGER_POSTCONDITION_FAILED")
        return row


def read_creation_ledger(store_root: Path) -> list[dict[str, Any]]:
    store = _store_root(Path(store_root))
    payload = _read_authoritative_file(
        store / "creation_ledger.jsonl", "CREATION_LEDGER"
    )
    if not payload:
        return []
    rows = [strict_load_object(line) for line in payload.splitlines(keepends=True)]
    if _jsonl(rows) != payload:
        raise TransactionError("CREATION_LEDGER_INVALID")
    previous = None
    for sequence, row in enumerate(rows, 1):
        if (
            row.get("schema_id") != CREATION_SCHEMA_ID
            or row.get("sequence") != sequence
            or row.get("previous_event_sha256") != previous
            or row.get("authority_effect") != AUTHORITY_EFFECT
            or not isinstance(row.get("period_id"), str)
            or row.get("event_sha256") != _creation_event_hash(row)
        ):
            raise TransactionError("CREATION_LEDGER_INVALID")
        previous = row["event_sha256"]
    return rows


def _initial_state(identity: TransactionIdentity, logical_time: str) -> dict[str, Any]:
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "current_state": TransactionState.CREATED.value,
        "last_transition_id": None,
        "logical_time_utc": logical_time,
        "parent_transaction_id": identity.parent_transaction_id,
        "root_transaction_id": identity.root_transaction_id,
        "schema_id": STATE_SCHEMA_ID,
        "sequence": 0,
        "transaction_id": identity.transaction_id,
    }


def _validate_state_record(tx: Path, value: Any) -> dict[str, Any]:
    """Validate the complete live state shape and its path-bound identity."""

    if not isinstance(value, Mapping) or set(value) != _STATE_FIELDS:
        raise TransactionError("TRANSACTION_STATE_FIELDS_INVALID")
    row = dict(value)
    try:
        current = TransactionState(row["current_state"])
        identity = TransactionIdentity(
            row["transaction_id"],
            parent_transaction_id=row["parent_transaction_id"],
            root_transaction_id=row["root_transaction_id"],
        )
        logical_time = _utc(row["logical_time_utc"], "state_logical_time")
    except (KeyError, TypeError, ValueError) as exc:
        raise TransactionError("TRANSACTION_STATE_SEMANTICS_INVALID") from exc
    sequence = row["sequence"]
    if type(sequence) is not int or sequence < 0:
        raise TransactionError("TRANSACTION_STATE_SEQUENCE_INVALID")
    transition_id = row["last_transition_id"]
    if sequence == 0:
        if current is not TransactionState.CREATED or transition_id is not None:
            raise TransactionError("TRANSACTION_INITIAL_STATE_INVALID")
    elif (
        type(transition_id) is not str
        or not transition_id.startswith("tr_")
        or not _HEX32.fullmatch(transition_id[3:])
    ):
        raise TransactionError("TRANSACTION_LAST_TRANSITION_ID_INVALID")
    if (
        row["schema_id"] != STATE_SCHEMA_ID
        or row["authority_effect"] != AUTHORITY_EFFECT
        or identity.transaction_id != tx.name
        or logical_time != row["logical_time_utc"]
    ):
        raise TransactionError("TRANSACTION_STATE_IDENTITY_INVALID")
    return row


def _state(tx: Path) -> dict[str, Any]:
    return _validate_state_record(tx, read_canonical_file(tx / "state.json"))


def _make_transition(
    tx: Path,
    requested_state: TransactionState,
    *,
    logical_time_utc: str,
    actor_id: str,
    actor_class: ActorClass,
    plane: Plane,
    reason_codes: Sequence[str],
    extra_targets: Mapping[str, bytes] | None = None,
    event_output_digests: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    state = _state(tx)
    source = TransactionState(state["current_state"])
    target = validate_transition(source, requested_state)
    state_before = _read_authoritative_file(tx / "state.json", "STATE")
    ledger_before = _read_authoritative_file(
        tx / "custody_events.jsonl", "CUSTODY_LEDGER"
    )
    events = read_event_ledger(tx / "custody_events.jsonl")
    transition_id = f"tr_{sha256_bytes(canonical_bytes({
        'from': source.value,
        'sequence': len(events) + 1,
        'to': target.value,
        'transaction_id': state['transaction_id'],
    }))[:32]}"
    new_state = {
        **state,
        "current_state": target.value,
        "last_transition_id": transition_id,
        "logical_time_utc": logical_time_utc,
        "sequence": state["sequence"] + 1,
    }
    new_state_bytes = canonical_bytes(new_state)
    extra_payloads = dict(extra_targets or {})
    for name, payload in extra_payloads.items():
        if (
            type(name) is not str
            or name.startswith("/")
            or "\\" in name
            or ".." in name.split("/")
            or type(payload) is not bytes
        ):
            raise TransactionError("TRANSITION_EXTRA_TARGET_INVALID")
    output_digests = {
        "state.json": sha256_bytes(new_state_bytes),
        **{name: sha256_bytes(payload) for name, payload in extra_payloads.items()},
    }
    for name, digest in dict(event_output_digests or {}).items():
        if (
            type(name) is not str
            or not name
            or name in output_digests
            or type(digest) is not str
            or not _HEX64.fullmatch(digest)
        ):
            raise TransactionError("TRANSITION_EVENT_OUTPUT_DIGEST_INVALID")
        output_digests[name] = digest
    event = append_event(
        events,
        ledger_id=f"ledger_{state['transaction_id']}",
        transaction_id=state["transaction_id"],
        logical_time=logical_time_utc,
        observed_time_utc=None,
        actor_id=actor_id,
        actor_class=actor_class,
        plane=plane,
        operation=f"STATE_TRANSITION:{source.value}->{target.value}",
        subject_type="TRANSACTION",
        subject_id=state["transaction_id"],
        input_digests={"state.json": sha256_bytes(state_before)},
        output_digests=output_digests,
        result="PASS",
        reason_codes=tuple(reason_codes),
    )
    new_events = [*events, event]
    targets: list[dict[str, Any]] = []
    for name, payload in sorted(extra_payloads.items()):
        targets.append({
            "before_sha256": None,
            "bytes_base64": base64.b64encode(payload).decode("ascii"),
            "path": name,
            "sha256": sha256_bytes(payload),
        })
    state_target = {
        "before_sha256": sha256_bytes(state_before),
        "bytes_base64": base64.b64encode(new_state_bytes).decode("ascii"),
        "path": "state.json",
        "sha256": sha256_bytes(new_state_bytes),
    }
    ledger_target = {
        "before_sha256": sha256_bytes(ledger_before),
        "bytes_base64": base64.b64encode(ledger_bytes(new_events)).decode("ascii"),
        "path": "custody_events.jsonl",
        "sha256": sha256_bytes(ledger_bytes(new_events)),
    }
    # A terminal seal must become visible only after its exact custody ledger
    # is live and the package/live binding has been authenticated.  Other
    # transitions retain their established target order for compatibility.
    targets.extend(
        [ledger_target, state_target]
        if target is TransactionState.SEALED
        else [state_target, ledger_target]
    )
    journal = {
        "authority_effect": AUTHORITY_EFFECT,
        "from_state": source.value,
        "logical_time_utc": logical_time_utc,
        "phase": "APPLY_TARGETS",
        "recovery_observation": None,
        "schema_id": JOURNAL_SCHEMA_ID,
        "targets": targets,
        "to_state": target.value,
        "transaction_id": state["transaction_id"],
        "transition_id": transition_id,
    }
    return journal, new_events, targets


def _target_payload(target: Mapping[str, Any]) -> bytes:
    try:
        payload = base64.b64decode(target["bytes_base64"], validate=True)
    except (KeyError, TypeError, ValueError) as exc:
        raise TransactionError("TRANSITION_JOURNAL_PAYLOAD_INVALID") from exc
    if sha256_bytes(payload) != target.get("sha256"):
        raise TransactionError("TRANSITION_JOURNAL_TARGET_DIGEST_INVALID")
    return payload


def _journal_target_path(tx: Path, value: Any) -> Path:
    if (
        type(value) is not str
        or not value
        or len(value) > 240
        or value != unicodedata.normalize("NFC", value)
        or value.startswith("/")
        or "\\" in value
        or ":" in value
        or "\x00" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise TransactionError("TRANSITION_JOURNAL_TARGET_PATH_INVALID")
    candidate = tx.joinpath(*value.split("/"))
    require_safe_ancestors(candidate, include_leaf=False)
    try:
        resolved_root = tx.resolve(strict=True)
        # A recovery receipt is the sole transition target whose bounded
        # parent may not exist until publication. Existing ancestors were
        # already checked for link-like objects above; strict=False lets us
        # validate this prospective parent without weakening containment.
        resolved_parent = candidate.parent.resolve(strict=False)
    except OSError as exc:
        raise TransactionError("TRANSITION_JOURNAL_TARGET_PARENT_INVALID") from exc
    if os.path.commonpath((str(resolved_root), str(resolved_parent))) != str(resolved_root):
        raise TransactionError("TRANSITION_JOURNAL_TARGET_ESCAPES_TRANSACTION")
    return candidate


def _validate_transition_journal(tx: Path, journal: Any) -> dict[str, Any]:
    fields = {
        "authority_effect",
        "from_state",
        "logical_time_utc",
        "phase",
        "recovery_observation",
        "schema_id",
        "targets",
        "to_state",
        "transaction_id",
        "transition_id",
    }
    if not isinstance(journal, Mapping) or set(journal) != fields:
        raise TransactionError("TRANSITION_JOURNAL_FIELDS_INVALID")
    row = dict(journal)
    if (
        row["schema_id"] != JOURNAL_SCHEMA_ID
        or row["authority_effect"] != AUTHORITY_EFFECT
        or row["transaction_id"] != tx.name
        or not isinstance(row["transition_id"], str)
        or not row["transition_id"].startswith("tr_")
        or not _HEX32.fullmatch(row["transition_id"][3:])
    ):
        raise TransactionError("TRANSITION_JOURNAL_IDENTITY_INVALID")
    _utc(row["logical_time_utc"], "journal_logical_time")
    source = TransactionState(row["from_state"])
    target_state = validate_transition(source, row["to_state"])
    if row["phase"] not in {"APPLY_TARGETS", "PUBLISH_RECOVERY_EVIDENCE"}:
        raise TransactionError("TRANSITION_JOURNAL_PHASE_INVALID")
    targets = row["targets"]
    if not isinstance(targets, list) or not 2 <= len(targets) <= 5:
        raise TransactionError("TRANSITION_JOURNAL_TARGETS_INVALID")
    names: list[str] = []
    total = 0
    for value in targets:
        if not isinstance(value, Mapping) or set(value) != {
            "before_sha256",
            "bytes_base64",
            "path",
            "sha256",
        }:
            raise TransactionError("TRANSITION_JOURNAL_TARGET_FIELDS_INVALID")
        name = value["path"]
        _journal_target_path(tx, name)
        if name in names:
            raise TransactionError("TRANSITION_JOURNAL_TARGET_DUPLICATE")
        names.append(name)
        if type(value["sha256"]) is not str or not _HEX64.fullmatch(value["sha256"]):
            raise TransactionError("TRANSITION_JOURNAL_TARGET_DIGEST_INVALID")
        before = value["before_sha256"]
        if before is not None and (type(before) is not str or not _HEX64.fullmatch(before)):
            raise TransactionError("TRANSITION_JOURNAL_TARGET_BASE_INVALID")
        payload = _target_payload(value)
        total += len(payload)
        if total > 64 * 1024 * 1024:
            raise TransactionError("TRANSITION_JOURNAL_TARGETS_OVERSIZE")
    is_seal_route = (
        source is TransactionState.FINALIZATION_PENDING
        and target_state is TransactionState.SEALED
    )
    names_without_recovery = [
        name for name in names if not name.startswith("recovery/")
    ]
    expected_core_tail = (
        ["custody_events.jsonl", "state.json"]
        if is_seal_route
        else ["state.json", "custody_events.jsonl"]
    )
    if (
        names_without_recovery[-2:] != expected_core_tail
        or names.count("state.json") != 1
    ):
        raise TransactionError("TRANSITION_JOURNAL_CORE_TARGETS_INVALID")
    extras = set(names) - {"state.json", "custody_events.jsonl"}
    expected_extras: set[str] = set()
    if source is TransactionState.HUMAN_DECISION_PENDING:
        expected_extras.add("review/human_decision.json")
        if "review/review_policy_repair_authorization.json" in extras:
            if target_state is not TransactionState.REPAIR_REQUESTED:
                raise TransactionError("TRANSITION_JOURNAL_TARGET_SCOPE_INVALID")
            expected_extras.add("review/review_policy_repair_authorization.json")
    if source is TransactionState.REPAIR_REQUESTED:
        expected_extras.add("review/repair_lineage.json")
    recovery_names = {name for name in extras if name.startswith("recovery/")}
    expected_recovery = {f"recovery/{row['transition_id']}.json"} if row["phase"] == "PUBLISH_RECOVERY_EVIDENCE" else set()
    if recovery_names != expected_recovery or extras - recovery_names != expected_extras:
        raise TransactionError("TRANSITION_JOURNAL_TARGET_SCOPE_INVALID")
    observation = row["recovery_observation"]
    if row["phase"] == "APPLY_TARGETS":
        if observation is not None:
            raise TransactionError("TRANSITION_JOURNAL_RECOVERY_OBSERVATION_INVALID")
    else:
        required_observation = {
            "applied_target_prefix_count",
            "cause_posture",
            "next_pending_target_path",
            "pending_journal_sha256",
            "pending_transition_id",
            "target_count",
        }
        if (
            not isinstance(observation, Mapping)
            or set(observation) != required_observation
            or observation.get("pending_transition_id") != row["transition_id"]
            or observation.get("cause_posture") != "UNOBSERVED_PROCESS_INTERRUPTION"
            or type(observation.get("pending_journal_sha256")) is not str
            or not _HEX64.fullmatch(observation["pending_journal_sha256"])
            or type(observation.get("applied_target_prefix_count")) is not int
            or type(observation.get("target_count")) is not int
            or not 0 <= observation["applied_target_prefix_count"] <= observation["target_count"]
            or observation["target_count"] != len(targets) - 1
        ):
            raise TransactionError("TRANSITION_JOURNAL_RECOVERY_OBSERVATION_INVALID")
    state_target = next(value for value in targets if value["path"] == "state.json")
    embedded_state = strict_load_object(_target_payload(state_target))
    actual_state = _state(tx)
    expected_embedded_state = (
        {
            **actual_state,
            "current_state": target_state.value,
            "last_transition_id": row["transition_id"],
            "logical_time_utc": row["logical_time_utc"],
            "sequence": actual_state["sequence"] + 1,
        }
        if actual_state.get("current_state") == source.value
        else actual_state
    )
    if (
        actual_state.get("current_state") not in {source.value, target_state.value}
        or embedded_state != expected_embedded_state
    ):
        raise TransactionError("TRANSITION_JOURNAL_STATE_SEMANTICS_INVALID")
    ledger_target = next(value for value in targets if value["path"] == "custody_events.jsonl")
    embedded_events = [
        strict_load_object(line)
        for line in _target_payload(ledger_target).splitlines(keepends=True)
    ]
    ledger_receipt = verify_events(embedded_events)
    transition_events = [
        event
        for event in embedded_events
        if event.get("operation") == f"STATE_TRANSITION:{source.value}->{target_state.value}"
    ]
    all_recovery_events = [
        event
        for event in embedded_events
        if event.get("operation") == "RECOVER_INTERRUPTED_TRANSITION"
    ]
    recovery_events = [
        event
        for event in all_recovery_events
        if event.get("subject_id") == row["transition_id"]
    ]
    try:
        for recovery_event in all_recovery_events:
            validate_recovery_event_semantics(recovery_event)
    except TransitionPolicyError as exc:
        raise TransactionError("TRANSITION_JOURNAL_RECOVERY_ACTOR_POLICY_INVALID") from exc
    expected_transition_outputs = {"state.json": state_target["sha256"]}
    for name in expected_extras:
        expected_transition_outputs[name] = next(
            value["sha256"] for value in targets if value["path"] == name
        )
    route_evidence: dict[
        tuple[TransactionState, TransactionState], tuple[str, ...]
    ] = {
        (
            TransactionState.CONTROLS_PENDING,
            TransactionState.CONTROLS_COMPLETE,
        ): ("review/control_results.jsonl",),
        (
            TransactionState.CONTROLS_COMPLETE,
            TransactionState.SOPHIA_COMPLETE,
        ): ("review/findings.jsonl", "review/independent_review.json"),
        (
            TransactionState.SOPHIA_COMPLETE,
            TransactionState.ATLAS_COMPLETE,
        ): ("review/orientation.json",),
    }
    for name in route_evidence.get((source, target_state), ()):
        evidence_path = _journal_target_path(tx, name)
        expected_transition_outputs[name] = sha256_bytes(
            _read_transition_target(evidence_path)
        )
    if (
        source is TransactionState.FINALIZATION_PENDING
        and target_state is TransactionState.SEALED
    ):
        transition_output_digests = (
            transition_events[0].get("output_digests", {})
            if len(transition_events) == 1
            else {}
        )
        content_root = transition_output_digests.get("evidence_content_root")
        if type(content_root) is not str or not _HEX64.fullmatch(content_root):
            raise TransactionError("TRANSITION_JOURNAL_CONTENT_ROOT_INVALID")
        expected_transition_outputs["evidence_content_root"] = content_root
    if (
        ledger_receipt.get("transaction_id") != tx.name
        or len(transition_events) != 1
        or transition_events[0].get("logical_time") != row["logical_time_utc"]
        or transition_events[0].get("subject_type") != "TRANSACTION"
        or transition_events[0].get("subject_id") != tx.name
        or transition_events[0].get("input_digests")
        != {"state.json": state_target["before_sha256"]}
        or transition_events[0].get("output_digests") != expected_transition_outputs
    ):
        raise TransactionError("TRANSITION_JOURNAL_CUSTODY_SEMANTICS_INVALID")
    decision_actor_id: str | None = None
    if source is TransactionState.HUMAN_DECISION_PENDING:
        decision_target = next(
            value
            for value in targets
            if value["path"] == "review/human_decision.json"
        )
        decision_record = strict_load_object(_target_payload(decision_target))
        decision_actor_id = decision_record.get("actor_id")
        decision_targets = {
            "APPROVE": TransactionState.APPROVED,
            "HOLD": TransactionState.HELD,
            "REJECT": TransactionState.REJECTED,
            "REQUEST_REPAIR": TransactionState.REPAIR_REQUESTED,
        }
        if (
            decision_record.get("transaction_id") != tx.name
            or decision_record.get("decision_time_utc") != row["logical_time_utc"]
            or decision_targets.get(decision_record.get("decision")) is not target_state
        ):
            raise TransactionError("TRANSITION_JOURNAL_DECISION_SEMANTICS_INVALID")
    try:
        validate_transition_event_semantics(
            transition_events[0],
            source,
            target_state,
            decision_actor_id=decision_actor_id,
        )
    except TransitionPolicyError as exc:
        raise TransactionError("TRANSITION_JOURNAL_ACTOR_POLICY_INVALID") from exc
    expected_recovery_count = 1 if row["phase"] == "PUBLISH_RECOVERY_EVIDENCE" else 0
    if len(recovery_events) != expected_recovery_count:
        raise TransactionError("TRANSITION_JOURNAL_RECOVERY_EVENT_COUNT_INVALID")
    if recovery_events:
        recovery_target = next(
            value for value in targets if value["path"] in recovery_names
        )
        recovery_event = recovery_events[0]
        recovery_receipt = strict_load_object(_target_payload(recovery_target))
        recovery_receipt_fields = {
            "authority_effect",
            "journal_observation",
            "nonauthority",
            "result",
            "schema_id",
            "transaction_id",
            "transition_id",
        }
        original_target_names = [
            value["path"] for value in targets if value["path"] not in recovery_names
        ]
        prefix = observation["applied_target_prefix_count"]
        expected_next = (
            original_target_names[prefix]
            if prefix < len(original_target_names)
            else None
        )
        if (
            set(recovery_receipt) != recovery_receipt_fields
            or recovery_receipt.get("schema_id") != RECOVERY_SCHEMA_ID
            or recovery_receipt.get("transaction_id") != tx.name
            or recovery_receipt.get("transition_id") != row["transition_id"]
            or recovery_receipt.get("authority_effect") != AUTHORITY_EFFECT
            or recovery_receipt.get("result") != "RECOVERED"
            or recovery_receipt.get("journal_observation") != observation
            or observation.get("next_pending_target_path") != expected_next
            or recovery_event.get("subject_id") != row["transition_id"]
            or recovery_event.get("logical_time") != row["logical_time_utc"]
            or recovery_event.get("input_digests")
            != {"pending_journal": row["recovery_observation"]["pending_journal_sha256"]}
            or recovery_event.get("output_digests")
            != {
                "recovery_receipt": recovery_target["sha256"],
                "state.json": state_target["sha256"],
            }
        ):
            raise TransactionError("TRANSITION_JOURNAL_RECOVERY_EVENT_INVALID")
    expected_transition_id = f"tr_{sha256_bytes(canonical_bytes({
        'from': source.value,
        'sequence': transition_events[0]['sequence'],
        'to': target_state.value,
        'transaction_id': tx.name,
    }))[:32]}"
    if expected_transition_id != row["transition_id"]:
        raise TransactionError("TRANSITION_JOURNAL_TRANSITION_ID_INVALID")
    return row


def _applied_prefix(tx: Path, targets: Sequence[Mapping[str, Any]]) -> int:
    count = 0
    for target in targets:
        path = _journal_target_path(tx, target["path"])
        if os.path.lexists(path):
            if sha256_bytes(_read_transition_target(path)) == target.get("sha256"):
                count += 1
                continue
        break
    return count


def _read_transition_target(path: Path) -> bytes:
    """Read one existing target only while it remains ordinary and single-link."""

    try:
        return read_ordinary_bytes(path, maximum_bytes=64 * 1024 * 1024)
    except (OSError, ValueError) as exc:
        if isinstance(exc, TransactionError):
            raise
        raise TransactionError("TRANSITION_TARGET_IRREGULAR") from exc


def _publish_target(tx: Path, target: Mapping[str, Any]) -> None:
    name = str(target.get("path"))
    path = _journal_target_path(tx, name)
    payload = _target_payload(target)
    if os.path.lexists(path):
        current = _read_transition_target(path)
        current_sha = sha256_bytes(current)
        if current_sha == target["sha256"]:
            return
        if current_sha != target.get("before_sha256"):
            raise TransactionError("TRANSITION_TARGET_CONFLICT")
        replace_bytes_atomic(path, payload, expected_sha256=current_sha)
    else:
        if target.get("before_sha256") is not None:
            raise TransactionError("TRANSITION_TARGET_MISSING")
        path.parent.mkdir(parents=True, exist_ok=True)
        write_exclusive_bytes(path, payload)


def _recovery_journal(tx: Path, journal: dict[str, Any], journal_sha: str) -> dict[str, Any]:
    if journal.get("recovery_observation") is not None:
        return journal
    targets = list(journal["targets"])
    prefix = _applied_prefix(tx, targets)
    transaction_id = str(journal["transaction_id"])
    transition_id = str(journal["transition_id"])
    state_target = next(target for target in targets if target["path"] == "state.json")
    ledger_target = next(target for target in targets if target["path"] == "custody_events.jsonl")
    original_events: list[dict[str, Any]] = []
    for line in _target_payload(ledger_target).splitlines(keepends=True):
        original_events.append(strict_load_object(line))
    verify_events(original_events)
    observation = {
        "applied_target_prefix_count": prefix,
        "cause_posture": "UNOBSERVED_PROCESS_INTERRUPTION",
        "next_pending_target_path": targets[prefix]["path"] if prefix < len(targets) else None,
        "pending_journal_sha256": journal_sha,
        "pending_transition_id": transition_id,
        "target_count": len(targets),
    }
    receipt = {
        "authority_effect": AUTHORITY_EFFECT,
        "journal_observation": observation,
        "nonauthority": "Recovery evidence records deterministic re-entry; it does not establish root cause.",
        "result": "RECOVERED",
        "schema_id": RECOVERY_SCHEMA_ID,
        "transaction_id": transaction_id,
        "transition_id": transition_id,
    }
    receipt_bytes = canonical_bytes(receipt)
    recovery_event = append_event(
        original_events,
        ledger_id=f"ledger_{transaction_id}",
        transaction_id=transaction_id,
        logical_time=str(journal["logical_time_utc"]),
        observed_time_utc=None,
        actor_id="SYSTEM-RECOVERY",
        actor_class=ActorClass.SYSTEM_RECOVERY_ACTOR,
        plane=Plane.CONTROL_EVIDENCE,
        operation="RECOVER_INTERRUPTED_TRANSITION",
        subject_type="TRANSITION",
        subject_id=transition_id,
        input_digests={"pending_journal": journal_sha},
        output_digests={
            "recovery_receipt": sha256_bytes(receipt_bytes),
            "state.json": state_target["sha256"],
        },
        result="PASS",
        reason_codes=("DETERMINISTIC_PENDING_TRANSITION_REENTRY",),
    )
    recovered_ledger = ledger_bytes([*original_events, recovery_event])
    new_targets: list[dict[str, Any]] = []
    for target in targets:
        if target["path"] == "custody_events.jsonl":
            ledger_path = tx / "custody_events.jsonl"
            current_ledger_sha = sha256_bytes(
                _read_authoritative_file(ledger_path, "CUSTODY_LEDGER")
            )
            allowed_ledger_bases = {target.get("before_sha256"), target.get("sha256")}
            if current_ledger_sha not in allowed_ledger_bases:
                raise TransactionError("TRANSITION_RECOVERY_LEDGER_CONFLICT")
            target = {
                **target,
                "before_sha256": current_ledger_sha,
                "bytes_base64": base64.b64encode(recovered_ledger).decode("ascii"),
                "sha256": sha256_bytes(recovered_ledger),
            }
        new_targets.append(dict(target))
    recovery_path = f"recovery/{transition_id}.json"
    new_targets.insert(-1, {
        "before_sha256": None,
        "bytes_base64": base64.b64encode(receipt_bytes).decode("ascii"),
        "path": recovery_path,
        "sha256": sha256_bytes(receipt_bytes),
    })
    return {
        **journal,
        "phase": "PUBLISH_RECOVERY_EVIDENCE",
        "recovery_observation": observation,
        "targets": new_targets,
    }


def _finish_transition(
    tx: Path,
    *,
    recovering: bool,
    fault_after_target: int | None = None,
    release_pending: bool = True,
    before_state_publish: Callable[[], None] | None = None,
) -> dict[str, Any]:
    pending = tx / ".transition-pending.json"
    require_single_link_file(pending)
    journal_bytes = _read_transition_target(pending)
    journal = strict_load_object(journal_bytes)
    journal = _validate_transition_journal(tx, journal)
    if recovering and journal.get("phase") == "APPLY_TARGETS":
        # A seal journal is built only after the immutable package directory and
        # ZIP already bind the predicted seal ledger.  Rewriting that ledger to
        # add a recovery event would make the live transaction diverge from the
        # already-published package.  The separately retained finalization-
        # failure receipt is the evidence of this interrupted attempt; recovery
        # therefore finishes the exact authenticated seal journal without
        # changing its predicted bytes.  All pre-seal transitions retain the
        # append-only recovery receipt/event path below.
        is_seal = (
            journal.get("from_state") == TransactionState.FINALIZATION_PENDING.value
            and journal.get("to_state") == TransactionState.SEALED.value
        )
        if not is_seal:
            updated = _recovery_journal(tx, journal, sha256_bytes(journal_bytes))
            updated_bytes = canonical_bytes(updated)
            replace_bytes_atomic(
                pending,
                updated_bytes,
                expected_sha256=sha256_bytes(journal_bytes),
            )
            journal = updated
            journal_bytes = updated_bytes
            journal = _validate_transition_journal(tx, journal)
    targets = journal.get("targets")
    if not isinstance(targets, list) or not targets:
        raise TransactionError("TRANSITION_JOURNAL_TARGETS_INVALID")
    writes = 0
    for target in targets:
        path = _journal_target_path(tx, target["path"])
        already = (
            os.path.lexists(path)
            and sha256_bytes(_read_transition_target(path)) == target.get("sha256")
        )
        if target["path"] == "state.json" and before_state_publish is not None:
            before_state_publish()
        _publish_target(tx, target)
        if not already:
            writes += 1
            if fault_after_target is not None and writes == fault_after_target:
                raise TransitionInterrupted(f"TRANSITION_INTERRUPTED_AFTER_TARGET:{target['path']}")
    if sha256_bytes(_read_transition_target(pending)) != sha256_bytes(journal_bytes):
        raise TransactionError("TRANSITION_JOURNAL_CHANGED")
    require_single_link_file(pending)
    if release_pending:
        pending.unlink()
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "pending_journal_released": release_pending,
        "recovered": recovering,
        "result": "PASS",
        "target_count": len(targets),
        "transaction_id": journal["transaction_id"],
        "transition_id": journal["transition_id"],
    }


def _transition(
    tx: Path,
    state: TransactionState,
    *,
    logical_time_utc: str,
    actor_id: str,
    actor_class: ActorClass,
    plane: Plane,
    reason_codes: Sequence[str],
    extra_targets: Mapping[str, bytes] | None = None,
    event_output_digests: Mapping[str, str] | None = None,
    fault_after_target: int | None = None,
) -> dict[str, Any]:
    if os.path.lexists(tx / ".transition-pending.json"):
        raise TransactionError("PENDING_TRANSITION_REQUIRES_RECOVERY")
    journal, _, _ = _make_transition(
        tx,
        state,
        logical_time_utc=logical_time_utc,
        actor_id=actor_id,
        actor_class=actor_class,
        plane=plane,
        reason_codes=reason_codes,
        extra_targets=extra_targets,
        event_output_digests=event_output_digests,
    )
    write_exclusive_object(tx / ".transition-pending.json", journal)
    return _finish_transition(tx, recovering=False, fault_after_target=fault_after_target)


def _verify_seal_outputs(
    store: Path,
    tx: Path,
    transaction_id: str,
    *,
    require_live: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Verify immutable package outputs and, when requested, exact live bytes."""

    from .transaction_package import (
        verify_package_source_binding,
        verify_zip_directory_binding,
    )
    from .verification import verify_transaction_directory, verify_transaction_zip

    manifest = read_canonical_file(store / "store_manifest.json")
    package_dir = store / "packages" / transaction_id
    package_zip = store / "packages" / f"{transaction_id}.zip"
    directory_receipt = verify_transaction_directory(package_dir)
    zip_receipt = verify_transaction_zip(package_zip)
    verify_package_source_binding(
        tx,
        package_dir,
        predecessor_commit=manifest["predecessor_commit"],
        predecessor_review_status="HOLD",
        require_live=require_live,
    )
    verify_zip_directory_binding(package_dir, package_zip)
    return directory_receipt, zip_receipt


def recover_pending_transition(store_root: Path, transaction_id: str) -> dict[str, Any]:
    store = _store_root(Path(store_root))
    tx = _transaction_root(store, transaction_id)
    require_authorized(
        ActorClass.SYSTEM_RECOVERY_ACTOR,
        Action.RECOVER_INTERRUPTED_TRANSITION,
        target_plane=Plane.CONTROL_EVIDENCE,
    )
    pending = tx / ".transition-pending.json"
    if not os.path.lexists(pending):
        return {
            "authority_effect": AUTHORITY_EFFECT,
            "recovered": False,
            "result": "NO_PENDING_TRANSITION",
            "transaction_id": transaction_id,
        }
    pending_row = _validate_transition_journal(
        tx, strict_load_object(_read_transition_target(pending))
    )
    is_seal = (
        pending_row["from_state"] == TransactionState.FINALIZATION_PENDING.value
        and pending_row["to_state"] == TransactionState.SEALED.value
    )
    if is_seal:
        # Authenticate the already-published immutable package before making
        # the terminal state visible. Live custody is intentionally still the
        # journal's before-image at this point.
        _verify_seal_outputs(store, tx, transaction_id, require_live=False)
        result = _finish_transition(
            tx,
            recovering=True,
            release_pending=False,
            before_state_publish=lambda: _verify_seal_outputs(
                store, tx, transaction_id, require_live=True
            ),
        )
        _verify_seal_outputs(store, tx, transaction_id, require_live=True)
        pending_after = require_single_link_file(pending)
        _validate_transition_journal(
            tx, strict_load_object(_read_transition_target(pending_after))
        )
        pending_after.unlink()
        result["pending_journal_released"] = True
        result["finalized_package_rebound"] = True
        return result
    return _finish_transition(tx, recovering=True)


def _metadata(tx: Path) -> dict[str, Any]:
    return read_canonical_file(tx / "transaction.json")


def _review_policy_requires_evaluation(profile: Mapping[str, Any]) -> bool:
    return (
        profile.get("profile_id") != "STANDARD"
        and type(profile.get("policy_source")) is str
        and profile["policy_source"].startswith("OPTIONAL_")
    )


def _selected_review_registry(
    profile_id: str,
    *,
    enabled: bool,
    supplied: ReviewPolicyRegistry | None,
) -> ReviewPolicyRegistry | None:
    """Discover optional policy code only after explicit nonstandard selection."""

    if not enabled or profile_id == "STANDARD" or supplied is not None:
        return supplied
    return discover_review_policy_registry(profile_id)


def _read_review_policy_evaluation(
    tx: Path,
    *,
    required: bool,
) -> dict[str, Any] | None:
    path = tx / "review" / "review_policy_evaluation.json"
    if not path.exists():
        if required:
            raise TransactionError("REVIEW_POLICY_EVALUATION_MISSING")
        return None
    evaluation = read_canonical_file(path)
    metadata = _metadata(tx)
    profile_value = metadata.get("review_policy", {})
    try:
        profile = ReviewPolicyProfile.from_mapping(profile_value)
    except Exception as exc:
        raise TransactionError("REVIEW_POLICY_PROFILE_INVALID") from exc
    if _review_policy_requires_evaluation(profile_value):
        try:
            expected_profile = discover_review_policy_registry(
                profile.profile_id
            ).resolve(profile.profile_id)
        except Exception as exc:
            raise TransactionError("REVIEW_POLICY_PROFILE_UNAVAILABLE") from exc
        if expected_profile.as_dict() != profile.as_dict():
            raise TransactionError("REVIEW_POLICY_EVALUATION_BINDING_INVALID")
    bindings = evaluation.get("input_bindings")
    effects = evaluation.get("effects")
    if (
        evaluation.get("schema_id")
        != "uvlm.triadicbrain.aep01.review_policy_evaluation.v1"
        or evaluation.get("transaction_id") != metadata.get("transaction_id")
        or evaluation.get("profile_id") != profile.profile_id
        or profile.authority_effect != AUTHORITY_EFFECT
        or evaluation.get("external_compliance_criteria") is not False
        or evaluation.get("authority_effect") != AUTHORITY_EFFECT
        or not isinstance(effects, Mapping)
        or set(effects)
        != {"memory_written", "network_used", "provider_invoked", "publication_performed"}
        or any(value is not False for value in effects.values())
        or not isinstance(bindings, Mapping)
        or bindings.get("candidate_sha256") != metadata.get("candidate_sha256")
        or bindings.get("source_sha256") != metadata.get("source_sha256")
        or evaluation.get("status") not in {"INVOKED", "ERROR", "NOT_EXECUTED"}
        or not isinstance(evaluation.get("artifacts"), Mapping)
        or not isinstance(evaluation.get("receipts"), list)
        or not isinstance(evaluation.get("projection"), Mapping)
        or not isinstance(evaluation.get("findings"), list)
    ):
        raise TransactionError("REVIEW_POLICY_EVALUATION_BINDING_INVALID")
    return evaluation


def _review_policy_request(
    tx: Path,
    *,
    parent_evaluation: Mapping[str, Any] | None = None,
    repair_authorization: Mapping[str, Any] | None = None,
    parent_candidate_bytes: bytes | None = None,
) -> ReviewPolicyEvaluationRequest:
    """Reconstruct the captured request used to produce an optional policy."""

    metadata = _metadata(tx)
    return ReviewPolicyEvaluationRequest(
        profile_id=str(metadata["review_policy"]["profile_id"]),
        transaction_id=str(metadata["transaction_id"]),
        source_bytes=_read_authoritative_file(
            tx / "quarantine" / "source.bin", "SOURCE"
        ),
        source_media_type=str(metadata["source_media_type"]),
        task=str(metadata["prompt"]),
        model_identity=str(metadata["model_identity"]),
        candidate_bytes=_read_authoritative_file(
            tx / "quarantine" / "candidate.bin", "CANDIDATE"
        ),
        logical_time_utc=str(metadata["created_at_utc"]),
        parent_evaluation=parent_evaluation,
        repair_authorization=repair_authorization,
        parent_candidate_bytes=parent_candidate_bytes,
    )


def _replay_review_policy_lifecycle(
    store: Path,
    tx: Path,
) -> tuple[dict[str, Any], dict[str, Any] | None, ReviewPolicyEvaluationRequest] | None:
    """Delegate replay to the selected plug-in and fail closed if unavailable."""

    metadata = _metadata(tx)
    profile_id = metadata.get("review_policy", {}).get("profile_id")
    if profile_id == "STANDARD":
        return None
    try:
        registry = discover_review_policy_registry(str(profile_id))
        if registry.resolve(str(profile_id)).as_dict() != metadata["review_policy"]:
            raise ValueError("profile binding mismatch")
        replayed = registry.runtime(str(profile_id)).replay_lifecycle(store, tx)
    except Exception as exc:
        raise TransactionError("REVIEW_POLICY_LIFECYCLE_REPLAY_INVALID") from exc
    if (
        not isinstance(replayed, tuple)
        or len(replayed) != 3
        or not isinstance(replayed[0], dict)
        or (replayed[1] is not None and not isinstance(replayed[1], dict))
        or not isinstance(replayed[2], ReviewPolicyEvaluationRequest)
    ):
        raise TransactionError("REVIEW_POLICY_LIFECYCLE_REPLAY_INVALID")
    return replayed


def _policy_finding_inputs(evaluation: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = evaluation.get("findings")
    if not isinstance(rows, list):
        raise TransactionError("REVIEW_POLICY_FINDINGS_INVALID")
    result: list[dict[str, Any]] = []
    failure = evaluation.get("status") != "INVOKED"
    for row in rows:
        if (
            not isinstance(row, Mapping)
            or type(row.get("namespace")) is not str
            or not row.get("namespace")
            or row.get("external_compliance_criteria") is not False
            or row.get("status") != "OPEN_UNRESOLVED"
        ):
            raise TransactionError("REVIEW_POLICY_FINDING_INVALID")
        result.append(
            {
                "finding_class": (
                    "SYSTEM_ERROR"
                    if failure
                    else (
                        "BINDING_FINDING"
                        if row.get("approval_effect") == "BINDING"
                        else "ADVISORY_FINDING"
                    )
                ),
                "finding_id": row.get("finding_id"),
                "risk_posture": (
                    "POLICY_EXECUTION_ERROR" if failure else "HUMAN_ATTENTION"
                ),
                "summary": row.get("summary"),
            }
        )
    if failure and not result:
        raise TransactionError("REVIEW_POLICY_FAILURE_FINDING_MISSING")
    return result


def _finding_rows(
    transaction_id: str,
    control_rows: Sequence[Mapping[str, Any]],
    supplied: Sequence[Mapping[str, Any]],
    *,
    approval_effect: ApprovalEffect,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for control in control_rows:
        result = control["result"]
        if result not in {"FAIL", "HOLD", "ERROR"}:
            continue
        control_id = str(control["control_id"])
        rows.append({
            "affected_controls": [control_id],
            "authority_effect": AUTHORITY_EFFECT,
            "due_date": None,
            "evidence_refs": list(control["evidence_refs"]),
            "finding_class": "CONTROL_EXCEPTION" if result != "ERROR" else "SYSTEM_ERROR",
            "finding_id": f"finding_{sha256_bytes(canonical_bytes([transaction_id, control_id]))[:24]}",
            "origin": "VERSIONED_CONTROL_EXECUTION",
            "owner": "UNASSIGNED",
            "resolution": None,
            "risk_posture": "REVIEW_REQUIRED",
            "status": "OPEN",
            "summary": f"Control {control_id} recorded {result}; human attention is required.",
            "supersedes": None,
            "transaction_id": transaction_id,
        })
    for index, source in enumerate(supplied, 1):
        if not isinstance(source, Mapping):
            raise TransactionError("REVIEW_FINDING_INVALID")
        allowed = {"affected_controls", "finding_class", "finding_id", "risk_posture", "summary"}
        if set(source) - allowed:
            raise TransactionError("REVIEW_FINDING_FIELDS_INVALID")
        finding_id = require_identifier(source.get("finding_id") or f"finding_supplied_{index}", "finding_id")
        affected = list(source.get("affected_controls", ()))
        if any(control_id not in CONTROL_IDS for control_id in affected):
            raise TransactionError("REVIEW_FINDING_CONTROL_INVALID")
        finding_class = source.get("finding_class", "ADVISORY_FINDING")
        if finding_class not in {"ADVISORY_FINDING", "BINDING_FINDING", "CONTROL_EXCEPTION", "SYSTEM_ERROR", "POLICY_REFUSAL", "HUMAN_OVERRIDE", "INCIDENT", "REMEDIATION_ITEM", "MAPPING_CHALLENGE"}:
            raise TransactionError("REVIEW_FINDING_CLASS_INVALID")
        if approval_effect is ApprovalEffect.BINDING and finding_class == "ADVISORY_FINDING":
            finding_class = "BINDING_FINDING"
        rows.append({
            "affected_controls": affected,
            "authority_effect": AUTHORITY_EFFECT,
            "due_date": None,
            "evidence_refs": [],
            "finding_class": finding_class,
            "finding_id": finding_id,
            "origin": "INDEPENDENT_REVIEW_POLICY",
            "owner": "UNASSIGNED",
            "resolution": None,
            "risk_posture": _text(source.get("risk_posture", "REVIEW_REQUIRED"), "risk_posture", maximum=128),
            "status": "OPEN",
            "summary": _text(source.get("summary", "Review finding requires human attention."), "finding_summary", maximum=2048),
            "supersedes": None,
            "transaction_id": transaction_id,
        })
    if len({row["finding_id"] for row in rows}) != len(rows):
        raise TransactionError("REVIEW_FINDING_ID_DUPLICATE")
    return sorted(rows, key=lambda row: row["finding_id"])


def _preliminary_platform_overrides(candidate_captured: bool) -> dict[str, dict[str, Any]]:
    """Project only facts already present before the human decision."""

    return preliminary_platform_observations(
        candidate_captured=candidate_captured
    )


def _register_captured_transaction(
    store_root: Path,
    *,
    transaction_id: str,
    period_id: str,
    use_case_id: str,
    system_id: str,
    source_bytes: bytes,
    source_media_type: str,
    prompt: str,
    model_identity: str,
    settings: Mapping[str, Any],
    raw_candidate_bytes: bytes,
    logical_time_utc: str,
    admitted: bool = True,
    candidate_captured: bool = True,
    actor_class: ActorClass | str = ActorClass.HUMAN_TASK_REQUESTER,
    review_profile_id: str = "STANDARD",
    review_policy_enabled: bool = True,
    review_registry: ReviewPolicyRegistry | None = None,
    applicable_controls: Sequence[str] = (),
    control_overrides: Mapping[str, Mapping[str, Any]] | None = None,
    review_findings: Sequence[Mapping[str, Any]] = (),
    parent_identity: TransactionIdentity | None = None,
    repair_lineage: Mapping[str, Any] | None = None,
    parent_review_evaluation: Mapping[str, Any] | None = None,
    review_policy_repair_authorization: Mapping[str, Any] | None = None,
    parent_candidate_bytes: bytes | None = None,
    non_model_event: bool = False,
) -> dict[str, Any]:
    """Internal service orchestration for the captured-output route."""

    store = _store_root(Path(store_root))
    transaction_id = require_identifier(transaction_id, "transaction_id")
    period_id = require_identifier(period_id, "period_id")
    use_case_id = require_identifier(use_case_id, "use_case_id")
    system_id = require_identifier(system_id, "system_id")
    timestamp = _utc(logical_time_utc, "logical_time_utc")
    source = _bytes(source_bytes, "source")
    candidate = _bytes(raw_candidate_bytes, "candidate")
    if type(admitted) is not bool or type(candidate_captured) is not bool:
        raise TransactionError("ADMISSION_OR_CAPTURE_FLAG_INVALID")
    if not admitted and candidate_captured:
        raise TransactionError("REFUSED_TRANSACTION_CANNOT_CAPTURE_CANDIDATE")
    if not isinstance(settings, Mapping):
        raise TransactionError("SETTINGS_OBJECT_REQUIRED")
    if type(non_model_event) is not bool:
        raise TransactionError("PROCESSING_KIND_INVALID")
    if non_model_event:
        if not admitted or candidate_captured or candidate or model_identity != 'NOT_APPLICABLE_NON_MODEL_EVENT':
            raise TransactionError("NON_MODEL_EVENT_CANNOT_DECLARE_CANDIDATE")
        if settings.get('processing_kind') != 'NON_MODEL_EVENT':
            raise TransactionError("NON_MODEL_EVENT_CONTEXT_REQUIRED")
        if control_overrides or applicable_controls:
            raise TransactionError('NON_MODEL_LEGACY_MODEL_CONTROL_OVERRIDE_PROHIBITED')
    elif settings.get('processing_kind') == 'NON_MODEL_EVENT':
        raise TransactionError("NON_MODEL_EVENT_REQUIRES_OBSERVED_EVENT_INTERFACE")
    canonical_bytes(dict(settings))
    requester = ActorClass(actor_class)
    require_authorized(requester, Action.REGISTER_TRANSACTION)
    require_authorized(
        ActorClass.SERVICE_INGRESS,
        Action.ADMIT_OR_REFUSE,
        target_plane=Plane.INGRESS_QUARANTINE,
    )
    if not non_model_event:
        require_authorized(
            ActorClass.SERVICE_MODEL_ADAPTER,
            Action.WRITE_RAW_CANDIDATE,
            target_plane=Plane.INGRESS_QUARANTINE,
        )
    effective_registry = _selected_review_registry(
        review_profile_id,
        enabled=review_policy_enabled,
        supplied=review_registry,
    )
    profile = load_review_policy(
        review_profile_id,
        enabled=review_policy_enabled,
        registry=effective_registry,
    )
    if _review_policy_requires_evaluation(profile.as_dict()) and (
        effective_registry is None or not effective_registry.has_evaluator(profile.profile_id)
    ):
        raise TransactionError("REVIEW_POLICY_EVALUATOR_UNAVAILABLE")
    derived_claim_map = derive_candidate_claim_map(
        transaction_id=transaction_id,
        candidate_bytes=candidate,
        source_bytes=source,
    )
    derived_claim_observations = {} if non_model_event else claim_control_observations(derived_claim_map)
    if set(control_overrides or {}) & set(derived_claim_observations):
        raise TransactionError("DERIVED_CLAIM_CONTROL_OVERRIDE_PROHIBITED")
    if parent_identity is None:
        identity = TransactionIdentity(transaction_id)
    else:
        identity = TransactionIdentity(
            transaction_id,
            parent_transaction_id=parent_identity.transaction_id,
            root_transaction_id=parent_identity.root_transaction_id,
        )
    _append_creation_event(
        store,
        transaction_id=transaction_id,
        period_id=period_id,
        parent_transaction_id=identity.parent_transaction_id,
        logical_time_utc=timestamp,
    )
    tx = store / "transactions" / transaction_id
    require_new_root(tx)
    tx.mkdir()
    for directory in ("quarantine", "records", "review"):
        (tx / directory).mkdir()
    normalized, normalization = _normalize_source(source)
    metadata = {
        "applicable_controls": sorted(
            set(applicable_controls) | set(derived_claim_observations)
        ),
        "authority_effect": AUTHORITY_EFFECT,
        "candidate_captured": candidate_captured,
        "candidate_sha256": sha256_bytes(candidate),
        "created_at_utc": timestamp,
        "identity": identity.as_dict(),
        "model_identity": _text(model_identity, "model_identity", maximum=512),
        "normalization_profile": normalization,
        "normalized_source_sha256": sha256_bytes(normalized),
        "period_id": period_id,
        "prompt": _text(prompt, "prompt", maximum=65536),
        "review_policy": profile.as_dict(),
        "schema_id": "uvlm.triadicbrain.aep01.transaction_registration.v1",
        "settings": dict(settings),
        "source_media_type": _text(source_media_type, "source_media_type", maximum=256),
        "source_sha256": sha256_bytes(source),
        "system_id": system_id,
        "transaction_id": transaction_id,
        "use_case_id": use_case_id,
    }
    write_exclusive_object(tx / "transaction.json", metadata)
    write_exclusive_bytes(tx / "quarantine" / "source.bin", source)
    write_exclusive_bytes(tx / "quarantine" / "source.normalized", normalized)
    write_exclusive_bytes(tx / "quarantine" / "candidate.bin", candidate)
    effective_review_findings = list(review_findings)
    if effective_registry is not None and effective_registry.has_evaluator(profile.profile_id):
        assert effective_registry is not None
        evaluation = effective_registry.evaluate(
            profile.profile_id,
            ReviewPolicyEvaluationRequest(
                profile_id=profile.profile_id,
                transaction_id=transaction_id,
                source_bytes=source,
                source_media_type=metadata["source_media_type"],
                task=metadata["prompt"],
                model_identity=metadata["model_identity"],
                candidate_bytes=candidate,
                logical_time_utc=timestamp,
                parent_evaluation=parent_review_evaluation,
                repair_authorization=review_policy_repair_authorization,
                parent_candidate_bytes=parent_candidate_bytes,
            ),
        ).as_dict()
        write_exclusive_object(
            tx / "review" / "review_policy_evaluation.json", evaluation
        )
        effective_review_findings.extend(_policy_finding_inputs(evaluation))
        if evaluation["status"] != "INVOKED":
            failure_digest = sha256_bytes(canonical_bytes(evaluation))
            _write_or_match(
                store
                / "failure_receipts"
                / f"review-policy-{transaction_id}-{failure_digest}.json",
                canonical_bytes(evaluation),
            )
    state = _initial_state(identity, timestamp)
    write_exclusive_object(tx / "state.json", state)
    first_event = build_event(
        ledger_id=f"ledger_{transaction_id}",
        transaction_id=transaction_id,
        sequence=1,
        logical_time=timestamp,
        observed_time_utc=None,
        actor_id="SERVICE-INGRESS",
        actor_class=ActorClass.SERVICE_INGRESS,
        plane=Plane.INGRESS_QUARANTINE,
        operation="TRANSACTION_CREATED",
        subject_type="TRANSACTION",
        subject_id=transaction_id,
        output_digests={
            "quarantine/candidate.bin": sha256_bytes(candidate),
            "quarantine/source.bin": sha256_bytes(source),
            "quarantine/source.normalized": sha256_bytes(normalized),
            "transaction.json": sha256_bytes(canonical_bytes(metadata)),
        },
        reason_codes=(("NON_MODEL_EVENT_ROUTE",) if non_model_event else ("CAPTURED_OUTPUT_ROUTE",)),
    )
    write_exclusive_bytes(tx / "custody_events.jsonl", ledger_bytes([first_event]))
    _transition(tx, TransactionState.ADMISSION_PENDING, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=("ADMISSION_EVALUATION_STARTED",))
    if not admitted:
        _transition(tx, TransactionState.REFUSED, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=("TASK_REFUSED_AND_RETAINED_IN_POPULATION",))
        _prepare_review_evidence(
            tx,
            applicable_controls=(),
            control_overrides={control_id: {"result": "NOT_EXECUTED", "observed_condition": "Task was refused before control execution.", "reason_codes": ["ADMISSION_REFUSED"]} for control_id in (*P0_CORE, *P0_WHEN_APPLICABLE)},
            supplied_findings=(
                {
                    "finding_id": f"finding_refusal_{transaction_id}",
                    "finding_class": "POLICY_REFUSAL",
                    "summary": "The task was refused before candidate processing.",
                },
                *effective_review_findings,
            ),
            approval_effect=profile.approval_effect,
            logical_time_utc=timestamp,
        )
        return transaction_snapshot(store, transaction_id)
    _transition(tx, TransactionState.ADMITTED, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=("TASK_ADMITTED",))
    _transition(tx, TransactionState.INPUTS_BOUND, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=("SOURCE_PROMPT_MODEL_SETTINGS_BOUND",))
    if non_model_event:
        _transition(tx, TransactionState.OBSERVED_EVENT_BOUND, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=("NON_MODEL_EVENT_BOUND_NO_PROVIDER",))
    else:
        _transition(tx, TransactionState.CANDIDATE_PENDING, logical_time_utc=timestamp, actor_id="SERVICE-MODEL-ADAPTER", actor_class=ActorClass.SERVICE_MODEL_ADAPTER, plane=Plane.AI_EXECUTION, reason_codes=("CAPTURED_CANDIDATE_IMPORT_PENDING",))
        _transition(tx, TransactionState.CANDIDATE_CAPTURED if candidate_captured else TransactionState.CANDIDATE_FAILED, logical_time_utc=timestamp, actor_id="SERVICE-INGRESS", actor_class=ActorClass.SERVICE_INGRESS, plane=Plane.INGRESS_QUARANTINE, reason_codes=(("RAW_CANDIDATE_CAPTURED",) if candidate_captured else ("RAW_CANDIDATE_FAILURE_RETAINED",)))
    _transition(tx, TransactionState.CONTROLS_PENDING, logical_time_utc=timestamp, actor_id="SERVICE-CONTROL-EXECUTOR", actor_class=ActorClass.SERVICE_CONTROL_EXECUTOR, plane=Plane.CONTROL_EVIDENCE, reason_codes=("VERSIONED_CONTROL_EXECUTION_STARTED",))
    effective_overrides = _preliminary_platform_overrides(candidate_captured)
    effective_overrides.update(dict(control_overrides or {}))
    effective_overrides.update(derived_claim_observations)
    if non_model_event:
        effective_overrides = {control_id: {
            'result':'NOT_EXECUTED',
            'observed_condition':'Non-model event: this model/candidate procedure is not applicable. Executed event-policy results are separately bound.',
            'reason_codes':['NON_MODEL_EVENT_NO_CANDIDATE_PROCEDURE'],
        } for control_id in (*P0_CORE,*P0_WHEN_APPLICABLE)}
    if not candidate_captured:
        for control_id in (*P0_CORE, *P0_WHEN_APPLICABLE):
            effective_overrides.setdefault(control_id, {
                "result": "NOT_EXECUTED",
                "observed_condition": "Candidate capture failed; the procedure did not execute.",
                "reason_codes": ["CANDIDATE_CAPTURE_FAILED"],
            })
    _prepare_review_evidence(
        tx,
        applicable_controls=sorted(
            set(applicable_controls) | set(derived_claim_observations)
        ),
        control_overrides=effective_overrides,
        supplied_findings=effective_review_findings,
        approval_effect=profile.approval_effect,
        logical_time_utc=timestamp,
    )
    _transition(
        tx,
        TransactionState.CONTROLS_COMPLETE,
        logical_time_utc=timestamp,
        actor_id="SERVICE-CONTROL-EXECUTOR",
        actor_class=ActorClass.SERVICE_CONTROL_EXECUTOR,
        plane=Plane.CONTROL_EVIDENCE,
        reason_codes=("ALL_42_CONTROL_RESULTS_RECORDED",),
        event_output_digests={
            "review/control_results.jsonl": sha256_bytes(
                _read_authoritative_file(
                    tx / "review" / "control_results.jsonl", "CONTROL_RESULTS"
                )
            )
        },
    )
    _transition(
        tx,
        TransactionState.SOPHIA_COMPLETE,
        logical_time_utc=timestamp,
        actor_id="SERVICE-SOPHIA-AUDITOR",
        actor_class=ActorClass.SERVICE_SOPHIA_AUDITOR,
        plane=Plane.AUDIT_ORIENTATION,
        reason_codes=("INDEPENDENT_REVIEW_FINDINGS_RECORDED",),
        event_output_digests={
            "review/findings.jsonl": sha256_bytes(
                _read_authoritative_file(
                    tx / "review" / "findings.jsonl", "FINDINGS"
                )
            ),
            "review/independent_review.json": sha256_bytes(
                _read_authoritative_file(
                    tx / "review" / "independent_review.json", "INDEPENDENT_REVIEW"
                )
            ),
        },
    )
    _transition(
        tx,
        TransactionState.ATLAS_COMPLETE,
        logical_time_utc=timestamp,
        actor_id="SERVICE-ATLAS-ORIENTER",
        actor_class=ActorClass.SERVICE_ATLAS_ORIENTER,
        plane=Plane.AUDIT_ORIENTATION,
        reason_codes=("MANAGEMENT_ORIENTATION_RECORDED_WITH_NO_AUTHORITY",),
        event_output_digests={
            "review/orientation.json": sha256_bytes(
                _read_authoritative_file(
                    tx / "review" / "orientation.json", "ORIENTATION"
                )
            )
        },
    )
    _transition(tx, TransactionState.HUMAN_DECISION_PENDING, logical_time_utc=timestamp, actor_id="SERVICE-EVIDENCE-CUSTODIAN", actor_class=ActorClass.SERVICE_EVIDENCE_CUSTODIAN, plane=Plane.CONTROL_EVIDENCE, reason_codes=("HUMAN_DECISION_REQUIRED",))
    if repair_lineage is not None:
        write_exclusive_object(tx / "review" / "repair_lineage.json", dict(repair_lineage))
    return transaction_snapshot(store, transaction_id)


def register_captured_transaction(
    store_root: Path,
    *,
    transaction_id: str,
    period_id: str,
    use_case_id: str,
    system_id: str,
    source_bytes: bytes,
    source_media_type: str,
    prompt: str,
    model_identity: str,
    settings: Mapping[str, Any],
    raw_candidate_bytes: bytes,
    logical_time_utc: str,
    actor_class: ActorClass | str = ActorClass.HUMAN_TASK_REQUESTER,
    review_profile_id: str = "STANDARD",
    review_policy_enabled: bool = True,
    review_registry: ReviewPolicyRegistry | None = None,
) -> dict[str, Any]:
    """Register a normal admitted captured-output transaction.

    Authoritative admission exceptions, control observations, review findings,
    and repair-parent metadata are deliberately absent from this requester
    interface.  They are accepted only by the role-checked platform endpoint
    below or by the bounded repair-child orchestrator.
    """

    return _register_captured_transaction(
        store_root,
        transaction_id=transaction_id,
        period_id=period_id,
        use_case_id=use_case_id,
        system_id=system_id,
        source_bytes=source_bytes,
        source_media_type=source_media_type,
        prompt=prompt,
        model_identity=model_identity,
        settings=settings,
        raw_candidate_bytes=raw_candidate_bytes,
        logical_time_utc=logical_time_utc,
        actor_class=actor_class,
        review_profile_id=review_profile_id,
        review_policy_enabled=review_policy_enabled,
        review_registry=review_registry,
    )


def register_platform_observed_transaction(
    store_root: Path,
    *,
    transaction_id: str,
    period_id: str,
    use_case_id: str,
    system_id: str,
    source_bytes: bytes,
    source_media_type: str,
    prompt: str,
    model_identity: str,
    settings: Mapping[str, Any],
    raw_candidate_bytes: bytes,
    logical_time_utc: str,
    admitted: bool,
    candidate_captured: bool,
    applicable_controls: Sequence[str] = (),
    control_observations: Mapping[str, Mapping[str, Any]] | None = None,
    review_findings: Sequence[Mapping[str, Any]] = (),
    requester_actor_class: ActorClass | str = ActorClass.HUMAN_TASK_REQUESTER,
    ingress_actor_class: ActorClass | str = ActorClass.SERVICE_INGRESS,
    candidate_actor_class: ActorClass | str = ActorClass.SERVICE_MODEL_ADAPTER,
    control_actor_class: ActorClass | str = ActorClass.SERVICE_CONTROL_EXECUTOR,
    review_actor_class: ActorClass | str = ActorClass.SERVICE_SOPHIA_AUDITOR,
    review_profile_id: str = "STANDARD",
    review_policy_enabled: bool = True,
    review_registry: ReviewPolicyRegistry | None = None,
) -> dict[str, Any]:
    """Role-check platform observations before writing authoritative evidence."""

    require_authorized(
        ActorClass(ingress_actor_class),
        Action.ADMIT_OR_REFUSE,
        target_plane=Plane.INGRESS_QUARANTINE,
    )
    require_authorized(
        ActorClass(candidate_actor_class),
        Action.WRITE_RAW_CANDIDATE,
        target_plane=Plane.INGRESS_QUARANTINE,
    )
    require_authorized(
        ActorClass(control_actor_class),
        Action.WRITE_CONTROL_RESULT,
        target_plane=Plane.CONTROL_EVIDENCE,
    )
    require_authorized(
        ActorClass(review_actor_class),
        Action.WRITE_SOPHIA_FINDING,
        target_plane=Plane.AUDIT_ORIENTATION,
    )
    return _register_captured_transaction(
        store_root,
        transaction_id=transaction_id,
        period_id=period_id,
        use_case_id=use_case_id,
        system_id=system_id,
        source_bytes=source_bytes,
        source_media_type=source_media_type,
        prompt=prompt,
        model_identity=model_identity,
        settings=settings,
        raw_candidate_bytes=raw_candidate_bytes,
        logical_time_utc=logical_time_utc,
        admitted=admitted,
        candidate_captured=candidate_captured,
        actor_class=requester_actor_class,
        review_profile_id=review_profile_id,
        review_policy_enabled=review_policy_enabled,
        review_registry=review_registry,
        applicable_controls=applicable_controls,
        control_overrides=control_observations,
        review_findings=review_findings,
    )


def register_platform_observed_event(store_root: Path, *, transaction_id: str,
        period_id: str, use_case_id: str, system_id: str, source_bytes: bytes,
        source_media_type: str, prompt: str, settings: Mapping[str, Any],
        logical_time_utc: str, review_findings=(),
        ingress_actor_class=ActorClass.SERVICE_INGRESS,
        control_actor_class=ActorClass.SERVICE_CONTROL_EXECUTOR,
        review_actor_class=ActorClass.SERVICE_SOPHIA_AUDITOR) -> dict[str, Any]:
    """Record an observed event through the same custody/review/sealing engine.

    No candidate, model-adapter operation or failed model invocation is created.
    The empty legacy candidate member is explicitly not applicable in the export.
    """
    require_authorized(ActorClass(ingress_actor_class),Action.ADMIT_OR_REFUSE,target_plane=Plane.INGRESS_QUARANTINE)
    require_authorized(ActorClass(control_actor_class),Action.WRITE_CONTROL_RESULT,target_plane=Plane.CONTROL_EVIDENCE)
    require_authorized(ActorClass(review_actor_class),Action.WRITE_SOPHIA_FINDING,target_plane=Plane.AUDIT_ORIENTATION)
    return _register_captured_transaction(store_root,transaction_id=transaction_id,
        period_id=period_id,use_case_id=use_case_id,system_id=system_id,
        source_bytes=source_bytes,source_media_type=source_media_type,prompt=prompt,
        model_identity='NOT_APPLICABLE_NON_MODEL_EVENT',
        settings={**dict(settings),'processing_kind':'NON_MODEL_EVENT'},
        raw_candidate_bytes=b'',logical_time_utc=logical_time_utc,
        admitted=True,candidate_captured=False,non_model_event=True,review_findings=review_findings)


def _prepare_review_evidence(
    tx: Path,
    *,
    applicable_controls: Sequence[str],
    control_overrides: Mapping[str, Mapping[str, Any]],
    supplied_findings: Sequence[Mapping[str, Any]],
    approval_effect: ApprovalEffect,
    logical_time_utc: str,
) -> None:
    require_authorized(
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Action.WRITE_CONTROL_RESULT,
        target_plane=Plane.CONTROL_EVIDENCE,
    )
    require_authorized(
        ActorClass.SERVICE_SOPHIA_AUDITOR,
        Action.WRITE_SOPHIA_FINDING,
        target_plane=Plane.AUDIT_ORIENTATION,
    )
    require_authorized(
        ActorClass.SERVICE_ATLAS_ORIENTER,
        Action.WRITE_ATLAS_POSTURE,
        target_plane=Plane.AUDIT_ORIENTATION,
    )
    metadata = _metadata(tx)
    refs = [
        {"object_id": "SOURCE-ORIGINAL", "path": "source/original.bin", "sha256": metadata["source_sha256"]},
        {"object_id": "RAW-CANDIDATE", "path": "06_RAW_CANDIDATE_CAPTURE.bin", "sha256": metadata["candidate_sha256"]},
    ]
    rows = execute_controls(
        transaction_id=metadata["transaction_id"],
        period_id=metadata["period_id"],
        evidence_refs=refs,
        applicable_controls=applicable_controls,
        overrides=control_overrides,
        observed_time_utc=logical_time_utc,
    )
    write_exclusive_bytes(tx / "review" / "control_results.jsonl", _jsonl(rows))
    findings = _finding_rows(metadata["transaction_id"], rows, supplied_findings, approval_effect=approval_effect)
    write_exclusive_bytes(tx / "review" / "findings.jsonl", _jsonl(findings))
    review_packet = {
        "authority_effect": AUTHORITY_EFFECT,
        "finding_count": len(findings),
        "finding_ids": [row["finding_id"] for row in findings],
        "limitations": ["INDEPENDENT_REVIEW_PACKET_IS_NOT_AN_AUDIT_OPINION"],
        "nonauthority": NONASSURANCE_NOTICE,
        "result": "REVIEW_RECORDED",
        "schema_id": "uvlm.triadicbrain.aep01.independent_review_packet.v1",
        "transaction_id": metadata["transaction_id"],
    }
    orientation = {
        "authority_effect": AUTHORITY_EFFECT,
        "finding_count": len(findings),
        "management_attention": bool(findings),
        "nonauthority": "This orientation does not decide risk, materiality, scope, sufficiency, compliance, or an assurance opinion.",
        "schema_id": "uvlm.triadicbrain.aep01.management_orientation_packet.v1",
        "transaction_id": metadata["transaction_id"],
    }
    write_exclusive_object(tx / "review" / "independent_review.json", review_packet)
    write_exclusive_object(tx / "review" / "orientation.json", orientation)


def _record_denial(store: Path, transaction_id: str, actor: str, action: str, reason: str) -> dict[str, Any]:
    receipt = {
        "action": action,
        "actor_class": actor,
        "authority_effect": AUTHORITY_EFFECT,
        "reason_code": reason,
        "result": "DENIED",
        "schema_id": "uvlm.triadicbrain.aep01.denial_receipt.v1",
        "transaction_id": transaction_id,
    }
    digest = sha256_bytes(canonical_bytes(receipt))
    _write_or_match(store / "failure_receipts" / f"denial-{digest}.json", canonical_bytes(receipt))
    return receipt


def submit_human_decision(
    store_root: Path,
    transaction_id: str,
    *,
    decision: Decision | str,
    selected_finding_ids: Sequence[str],
    rationale: str,
    actor_id: str,
    actor_class: ActorClass | str = ActorClass.HUMAN_REVIEWER,
    logical_time_utc: str,
    fault_after_target: int | None = None,
) -> dict[str, Any]:
    store = _store_root(Path(store_root))
    tx = _transaction_root(store, transaction_id)
    actor = ActorClass(actor_class)
    try:
        require_authorized(actor, Action.SUBMIT_HUMAN_DECISION, target_plane=Plane.HUMAN_DECISION)
    except AuthorizationError as exc:
        _record_denial(store, transaction_id, actor.value, Action.SUBMIT_HUMAN_DECISION.value, str(exc))
        raise
    if _state(tx)["current_state"] != TransactionState.HUMAN_DECISION_PENDING.value:
        raise TransactionError("HUMAN_DECISION_NOT_AVAILABLE")
    selected = Decision(decision)
    ids = [require_identifier(item, "selected_finding_id") for item in selected_finding_ids]
    if len(ids) != len(set(ids)) or ids != sorted(ids):
        raise TransactionError("SELECTED_FINDING_IDS_INVALID")
    findings = _load_jsonl(tx / "review" / "findings.jsonl")
    open_ids = {row["finding_id"] for row in findings if row.get("status") == "OPEN"}
    if not set(ids).issubset(open_ids):
        raise TransactionError("SELECTED_FINDING_ID_NOT_OPEN")
    metadata = _metadata(tx)
    profile = metadata["review_policy"]
    policy_evaluation = _read_review_policy_evaluation(
        tx, required=_review_policy_requires_evaluation(profile)
    )
    if _review_policy_requires_evaluation(profile):
        # An optional-policy artifact is input to a human decision, never an
        # authority grant.  Replay it (and, for a child, its parent) before a
        # decision can advance the immutable lifecycle.
        _replay_review_policy_lifecycle(store, tx)
    control_rows = _load_jsonl(tx / "review" / "control_results.jsonl")
    binding_open = [row for row in findings if row.get("status") == "OPEN" and row.get("finding_class") in {"BINDING_FINDING", "CONTROL_EXCEPTION", "SYSTEM_ERROR", "POLICY_REFUSAL"}]
    p0_blocking = [
        row
        for row in control_rows
        if row["control_id"] not in P1
        and row["expected_condition"].get("applicability") == "APPLICABLE"
        and row["result"] in {"FAIL", "HOLD", "ERROR"}
    ]
    if selected is Decision.APPROVE and (binding_open or p0_blocking or profile.get("approval_effect") == "BINDING" and findings):
        denial = _record_denial(store, transaction_id, actor.value, "APPROVE", "APPROVAL_POLICY_NOT_MET")
        raise TransactionError(denial["reason_code"])
    if selected is Decision.REQUEST_REPAIR:
        if profile.get("repair_selection_supported") is not True:
            denial = _record_denial(
                store,
                transaction_id,
                actor.value,
                "REQUEST_REPAIR",
                "REPAIR_SELECTION_NOT_SUPPORTED",
            )
            raise TransactionError(denial["reason_code"])
        if not ids:
            raise TransactionError("REPAIR_FINDING_SELECTION_REQUIRED")
    elif ids:
        raise TransactionError("SELECTED_FINDING_IDS_INVALID")
    decision_id = f"decision_{sha256_bytes(canonical_bytes([transaction_id, selected.value, actor_id]))[:24]}"
    parent_evidence = {
        "control_results_sha256": sha256_bytes(
            _read_authoritative_file(
                tx / "review" / "control_results.jsonl", "CONTROL_RESULTS"
            )
        ),
        "findings_sha256": sha256_bytes(
            _read_authoritative_file(tx / "review" / "findings.jsonl", "FINDINGS")
        ),
    }
    record = {
        "actor_authentication_posture": "LOCAL_DECLARED_ACTOR_NO_EXTERNAL_IDP",
        "actor_id": require_identifier(actor_id, "actor_id"),
        "authority_effect": AUTHORITY_EFFECT,
        "conditions": [],
        "csrf_replay_protection": "LOCAL_ONE_TIME_STATE_AND_EXCLUSIVE_RECORD",
        "decision": selected.value,
        "decision_id": decision_id,
        "decision_time_utc": _utc(logical_time_utc, "logical_time_utc"),
        "nonauthority": NONASSURANCE_NOTICE,
        "override_records": [],
        "parent_evidence_digests": parent_evidence,
        "rationale": _text(rationale, "decision_rationale", maximum=4096),
        "selected_finding_ids": ids,
        "side_effects": {"network_used": False, "provider_invoked": False},
        "signature_posture": SIGNING_POSTURE,
        "time_posture": "CALLER_SUPPLIED_DETERMINISTIC_UTC",
        "transaction_id": transaction_id,
        "ui_session_version": VERSION,
        "unresolved_findings_acknowledged": sorted(open_ids),
    }
    target = {
        Decision.APPROVE: TransactionState.APPROVED,
        Decision.HOLD: TransactionState.HELD,
        Decision.REJECT: TransactionState.REJECTED,
        Decision.REQUEST_REPAIR: TransactionState.REPAIR_REQUESTED,
    }[selected]
    extra_targets = {"review/human_decision.json": canonical_bytes(record)}
    if (
        selected is Decision.REQUEST_REPAIR
        and policy_evaluation is not None
    ):
        projected_ids = set(policy_evaluation.get("projection", {}))
        if set(ids) & projected_ids:
            if not set(ids).issubset(projected_ids):
                raise TransactionError("REVIEW_POLICY_REPAIR_SELECTION_MIXED_NAMESPACE")
            try:
                registry = discover_review_policy_registry(str(profile["profile_id"]))
                policy_repair = registry.runtime(
                    str(profile["profile_id"])
                ).authorize_repair(
                    policy_evaluation,
                    selected_finding_ids=tuple(ids),
                    decision_id=decision_id,
                    repair_instruction=record["rationale"],
                    task_text=metadata["prompt"],
                    parent_candidate_bytes=_read_authoritative_file(
                        tx / "quarantine" / "candidate.bin", "PARENT_CANDIDATE"
                    ),
                )
            except Exception as exc:
                failure = {
                    "authority_effect": AUTHORITY_EFFECT,
                    "error_class": type(exc).__name__,
                    "failure_evidence_preserved": True,
                    "nonauthority": NONASSURANCE_NOTICE,
                    "profile_id": profile["profile_id"],
                    "reason_code": str(exc) or "REVIEW_POLICY_REPAIR_AUTHORIZATION_FAILED",
                    "result": "ERROR",
                    "schema_id": "uvlm.triadicbrain.aep01.review_policy_repair_failure.v1",
                    "transaction_id": transaction_id,
                }
                digest = sha256_bytes(canonical_bytes(failure))
                _write_or_match(
                    store
                    / "failure_receipts"
                    / f"review-policy-repair-{transaction_id}-{digest}.json",
                    canonical_bytes(failure),
                )
                _record_denial(
                    store,
                    transaction_id,
                    actor.value,
                    "REQUEST_REPAIR",
                    "REVIEW_POLICY_REPAIR_AUTHORIZATION_FAILED",
                )
                raise TransactionError(
                    "REVIEW_POLICY_REPAIR_AUTHORIZATION_FAILED"
                ) from exc
            extra_targets["review/review_policy_repair_authorization.json"] = (
                canonical_bytes(policy_repair)
            )
    _transition(
        tx,
        target,
        logical_time_utc=logical_time_utc,
        actor_id=actor_id,
        actor_class=actor,
        plane=Plane.HUMAN_DECISION,
        reason_codes=(f"HUMAN_DECISION_{selected.value}",),
        extra_targets=extra_targets,
        fault_after_target=fault_after_target,
    )
    return record


def create_repair_child(
    store_root: Path,
    parent_transaction_id: str,
    *,
    child_transaction_id: str,
    changed_inputs: Sequence[str],
    source_bytes: bytes,
    prompt: str,
    settings: Mapping[str, Any],
    raw_candidate_bytes: bytes,
    logical_time_utc: str,
    control_observations: Mapping[str, Mapping[str, Any]] | None = None,
    review_findings: Sequence[Mapping[str, Any]] = (),
    control_actor_class: ActorClass | str | None = None,
    review_actor_class: ActorClass | str | None = None,
) -> dict[str, Any]:
    store = _store_root(Path(store_root))
    parent = _transaction_root(store, parent_transaction_id)
    if os.path.lexists(parent / "review" / "repair_lineage.json"):
        raise TransactionError("REPAIR_CHILD_ALREADY_EXISTS")
    if _state(parent)["current_state"] != TransactionState.REPAIR_REQUESTED.value:
        raise TransactionError("PARENT_NOT_REPAIR_REQUESTED")
    decision = read_canonical_file(parent / "review" / "human_decision.json")
    selected = decision.get("selected_finding_ids")
    if not isinstance(selected, list) or not selected:
        raise TransactionError("PARENT_REPAIR_SELECTION_INVALID")
    parent_findings = _load_jsonl(parent / "review" / "findings.jsonl")
    open_ids = {
        row.get("finding_id") for row in parent_findings if row.get("status") == "OPEN"
    }
    if not set(selected).issubset(open_ids):
        raise TransactionError("PARENT_REPAIR_SELECTION_NOT_OPEN")
    parent_meta = _metadata(parent)
    if parent_meta["review_policy"].get("repair_selection_supported") is not True:
        raise TransactionError("REPAIR_SELECTION_NOT_SUPPORTED")
    inherited_profile_id = parent_meta["review_policy"]["profile_id"]
    replayed_parent: tuple[
        dict[str, Any], dict[str, Any] | None, ReviewPolicyEvaluationRequest
    ] | None = None
    if _review_policy_requires_evaluation(parent_meta["review_policy"]):
        # Authenticate the exact parent evaluation and repair authorization
        # before allocating an immutable child identity or writing its intent.
        replayed_parent = _replay_review_policy_lifecycle(store, parent)
        if replayed_parent is None or replayed_parent[1] is None:
            raise TransactionError("REVIEW_POLICY_PARENT_REPAIR_AUTHORIZATION_MISSING")
    changed = [_text(item, "changed_input", maximum=256) for item in changed_inputs]
    allowed_changed = {"candidate", "prompt", "settings", "source"}
    if (
        not changed
        or len(changed) != len(set(changed))
        or changed != sorted(changed)
        or not set(changed).issubset(allowed_changed)
    ):
        raise TransactionError("CHANGED_INPUTS_INVALID")
    child_source = _bytes(source_bytes, "source")
    child_candidate = _bytes(raw_candidate_bytes, "candidate")
    child_prompt = _text(prompt, "prompt", maximum=65536)
    if not isinstance(settings, Mapping):
        raise TransactionError("SETTINGS_OBJECT_REQUIRED")
    child_settings = dict(settings)
    canonical_bytes(child_settings)
    parent_source = _read_authoritative_file(
        parent / "quarantine" / "source.bin", "PARENT_SOURCE"
    )
    parent_candidate = _read_authoritative_file(
        parent / "quarantine" / "candidate.bin", "PARENT_CANDIDATE"
    )

    def value_digest(value: Any) -> str:
        return sha256_bytes(canonical_bytes({"value": value}))

    comparison = {
        "candidate": {
            "changed": child_candidate != parent_candidate,
            "child_sha256": sha256_bytes(child_candidate),
            "parent_sha256": sha256_bytes(parent_candidate),
        },
        "prompt": {
            "changed": child_prompt != parent_meta["prompt"],
            "child_sha256": value_digest(child_prompt),
            "parent_sha256": value_digest(parent_meta["prompt"]),
        },
        "settings": {
            "changed": child_settings != parent_meta["settings"],
            "child_sha256": value_digest(child_settings),
            "parent_sha256": value_digest(parent_meta["settings"]),
        },
        "source": {
            "changed": child_source != parent_source,
            "child_sha256": sha256_bytes(child_source),
            "parent_sha256": sha256_bytes(parent_source),
        },
    }
    observed_changed = sorted(
        name for name, row in comparison.items() if row["changed"] is True
    )
    if changed != observed_changed:
        raise TransactionError("DECLARED_CHANGED_INPUTS_MISMATCH")
    if control_observations:
        if control_actor_class is None:
            raise TransactionError("CONTROL_OBSERVATION_ACTOR_REQUIRED")
        require_authorized(
            ActorClass(control_actor_class),
            Action.WRITE_CONTROL_RESULT,
            target_plane=Plane.CONTROL_EVIDENCE,
        )
    if review_findings:
        if review_actor_class is None:
            raise TransactionError("REVIEW_FINDING_ACTOR_REQUIRED")
        require_authorized(
            ActorClass(review_actor_class),
            Action.WRITE_SOPHIA_FINDING,
            target_plane=Plane.AUDIT_ORIENTATION,
        )
    parent_identity = TransactionIdentity(**parent_meta["identity"])
    child_id = require_identifier(child_transaction_id, "child_transaction_id")
    intent = {
        "authority_effect": AUTHORITY_EFFECT,
        "changed_inputs": changed,
        "child_transaction_id": child_id,
        "input_comparison": comparison,
        "parent_decision_id": decision["decision_id"],
        "parent_evidence": {
            "candidate_sha256": parent_meta["candidate_sha256"],
            "control_results_sha256": sha256_bytes(
                _read_authoritative_file(
                    parent / "review" / "control_results.jsonl",
                    "PARENT_CONTROL_RESULTS",
                )
            ),
            "decision_sha256": sha256_bytes(canonical_bytes(decision)),
            "findings_sha256": sha256_bytes(
                _read_authoritative_file(
                    parent / "review" / "findings.jsonl", "PARENT_FINDINGS"
                )
            ),
        },
        "parent_transaction_id": parent_transaction_id,
        "root_transaction_id": parent_identity.root_transaction_id,
        "schema_id": "uvlm.triadicbrain.aep01.repair_intent.v1",
        "selected_finding_ids": selected,
    }
    intent_path = store / "repair_intents" / f"{parent_transaction_id}.json"
    _write_or_match(intent_path, canonical_bytes(intent))
    existing_children = [
        row
        for row in read_creation_ledger(store)
        if row.get("parent_transaction_id") == parent_transaction_id
    ]
    if len(existing_children) > 1 or (
        existing_children
        and existing_children[0].get("transaction_id") != child_id
    ):
        raise TransactionError("REPAIR_CHILD_ALREADY_EXISTS")
    inherited_registry: ReviewPolicyRegistry | None = None
    if _review_policy_requires_evaluation(parent_meta["review_policy"]):
        inherited_registry = discover_review_policy_registry(inherited_profile_id)
        if (
            inherited_registry.resolve(inherited_profile_id).as_dict()
            != parent_meta["review_policy"]
        ):
            raise TransactionError("INHERITED_REVIEW_POLICY_PROFILE_MISMATCH")
    elif inherited_profile_id != "STANDARD":
        from .review_policy import ReviewPolicyProfile

        inherited_registry = ReviewPolicyRegistry()
        inherited_registry.register_profile(
            ReviewPolicyProfile.from_mapping(parent_meta["review_policy"])
        )
    if existing_children:
        child_root = _transaction_root(store, child_id)
        child_meta = _metadata(child_root)
        if (
            child_meta.get("identity", {}).get("parent_transaction_id")
            != parent_transaction_id
            or child_meta.get("period_id") != parent_meta["period_id"]
            or _read_authoritative_file(
                child_root / "quarantine" / "source.bin", "CHILD_SOURCE"
            )
            != child_source
            or _read_authoritative_file(
                child_root / "quarantine" / "candidate.bin", "CHILD_CANDIDATE"
            )
            != child_candidate
            or child_meta.get("prompt") != child_prompt
            or child_meta.get("settings") != child_settings
        ):
            raise TransactionError("EXISTING_REPAIR_CHILD_INTENT_MISMATCH")
        child = transaction_snapshot(store, child_id)
    else:
        parent_policy_evaluation = (
            replayed_parent[0]
            if replayed_parent is not None
            else _read_review_policy_evaluation(
                parent,
                required=_review_policy_requires_evaluation(parent_meta["review_policy"]),
            )
        )
        parent_policy_repair_path = (
            parent / "review" / "review_policy_repair_authorization.json"
        )
        parent_policy_repair = (
            replayed_parent[1]
            if replayed_parent is not None
            else read_canonical_file(parent_policy_repair_path)
            if parent_policy_repair_path.exists()
            else None
        )
        child = _register_captured_transaction(
            store,
            transaction_id=child_id,
            period_id=parent_meta["period_id"],
            use_case_id=parent_meta["use_case_id"],
            system_id=parent_meta["system_id"],
            source_bytes=child_source,
            source_media_type=parent_meta["source_media_type"],
            prompt=child_prompt,
            model_identity=parent_meta["model_identity"],
            settings=child_settings,
            raw_candidate_bytes=child_candidate,
            logical_time_utc=logical_time_utc,
            applicable_controls=parent_meta["applicable_controls"],
            control_overrides=control_observations,
            review_findings=review_findings,
            parent_identity=parent_identity,
            review_profile_id=inherited_profile_id,
            review_policy_enabled=True,
            review_registry=inherited_registry,
            parent_review_evaluation=parent_policy_evaluation,
            review_policy_repair_authorization=parent_policy_repair,
            parent_candidate_bytes=parent_candidate,
        )
        child_root = _transaction_root(store, child_id)
    if _state(child_root)["current_state"] != TransactionState.HUMAN_DECISION_PENDING.value:
        raise TransactionError("REPAIR_CHILD_STATE_INVALID")
    child_meta = _metadata(child_root)
    lineage = {
        **intent,
        "execution_posture": "REAL_CAPTURED_OUTPUT_CHILD_ROUTE",
        "inherited_inputs": [
            "model_identity",
            "period_id",
            "review_policy",
            "system_id",
            "use_case_id",
        ],
        "nonauthority": "Creating a repair child does not establish that a selected finding was resolved.",
        "repair_intent_sha256": sha256_bytes(canonical_bytes(intent)),
        "resolved_finding_ids": [],
        "resulting_evidence": {
            "candidate_sha256": child_meta["candidate_sha256"],
            "control_results_sha256": sha256_bytes(
                _read_authoritative_file(
                    child_root / "review" / "control_results.jsonl",
                    "CHILD_CONTROL_RESULTS",
                )
            ),
            "findings_sha256": sha256_bytes(
                _read_authoritative_file(
                    child_root / "review" / "findings.jsonl", "CHILD_FINDINGS"
                )
            ),
            "transaction_record_sha256": sha256_bytes(
                _read_authoritative_file(
                    child_root / "transaction.json", "CHILD_TRANSACTION_RECORD"
                )
            ),
        },
        "schema_id": "uvlm.triadicbrain.aep01.repair_lineage.v1",
    }
    _write_or_match(
        child_root / "review" / "repair_lineage.json", canonical_bytes(lineage)
    )
    _transition(
        parent,
        TransactionState.REPAIR_CHILD_CREATED,
        logical_time_utc=logical_time_utc,
        actor_id="SERVICE-EVIDENCE-CUSTODIAN",
        actor_class=ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        plane=Plane.CONTROL_EVIDENCE,
        reason_codes=("IMMUTABLE_REPAIR_CHILD_CREATED",),
        extra_targets={"review/repair_lineage.json": canonical_bytes(lineage)},
    )
    return {"child": child, "lineage": lineage, "parent": transaction_snapshot(store, parent_transaction_id)}


_FINALIZATION_DECISIONS: dict[TransactionState, tuple[str, TransactionState | None]] = {
    TransactionState.APPROVED: (Decision.APPROVE.value, TransactionState.APPROVED),
    TransactionState.HELD: (Decision.HOLD.value, TransactionState.HELD),
    TransactionState.REJECTED: (Decision.REJECT.value, TransactionState.REJECTED),
    TransactionState.REPAIR_CHILD_CREATED: (
        Decision.REQUEST_REPAIR.value,
        TransactionState.REPAIR_REQUESTED,
    ),
    TransactionState.REFUSED: ("REFUSED", None),
}


def _finalization_source_state(
    transaction_id: str,
    events: Sequence[Mapping[str, Any]],
) -> TransactionState:
    suffix = f"->{TransactionState.FINALIZATION_PENDING.value}"
    matches = [
        event
        for event in events
        if isinstance(event.get("operation"), str)
        and event["operation"].startswith("STATE_TRANSITION:")
        and event["operation"].endswith(suffix)
    ]
    if len(matches) != 1:
        raise TransactionError("FINALIZATION_SOURCE_TRANSITION_INVALID")
    event = matches[0]
    try:
        route = str(event["operation"]).removeprefix("STATE_TRANSITION:")
        source_value, target_value = route.split("->", 1)
        source = TransactionState(source_value)
        target = validate_transition(source, target_value)
    except (TypeError, ValueError) as exc:
        raise TransactionError("FINALIZATION_SOURCE_TRANSITION_INVALID") from exc
    if (
        target is not TransactionState.FINALIZATION_PENDING
        or source not in _FINALIZATION_DECISIONS
        or event.get("transaction_id") != transaction_id
        or event.get("subject_id") != transaction_id
    ):
        raise TransactionError("FINALIZATION_SOURCE_TRANSITION_INVALID")
    return source


def _require_live_human_decision(
    tx: Path,
    source: TransactionState,
    events: Sequence[Mapping[str, Any]],
) -> tuple[str, dict[str, Any]]:
    """Return the business state only after exact decision/custody binding."""

    expected = _FINALIZATION_DECISIONS.get(source)
    if expected is None:
        raise TransactionError("FINALIZATION_SOURCE_STATE_INVALID")
    expected_decision, decision_target = expected
    path = tx / "review" / "human_decision.json"
    if decision_target is None:
        if os.path.lexists(path):
            raise TransactionError("REFUSED_TRANSACTION_HUMAN_DECISION_PROHIBITED")
        return expected_decision, {
            "authority_effect": AUTHORITY_EFFECT,
            "decision": "PENDING",
            "nonauthority": NONASSURANCE_NOTICE,
            "reason": "No human decision was recorded before refusal or incomplete finalization.",
            "transaction_id": tx.name,
        }
    if not os.path.lexists(path):
        raise TransactionError("HUMAN_DECISION_EVIDENCE_MISSING")
    decision_bytes = _read_authoritative_file(
        path, "HUMAN_DECISION", maximum_bytes=1024 * 1024
    )
    try:
        decision = strict_load_object(decision_bytes)
    except CanonicalError as exc:
        raise TransactionError("HUMAN_DECISION_EVIDENCE_INVALID") from exc
    decision_events = [
        event
        for event in events
        if event.get("operation")
        == (
            "STATE_TRANSITION:"
            f"{TransactionState.HUMAN_DECISION_PENDING.value}->"
            f"{decision_target.value}"
        )
    ]
    if (
        len(decision_events) != 1
        or decision.get("transaction_id") != tx.name
        or decision.get("decision") != expected_decision
        or decision.get("decision_time_utc") != decision_events[0].get("logical_time")
        or decision_events[0].get("transaction_id") != tx.name
        or decision_events[0].get("subject_id") != tx.name
        or decision_events[0].get("output_digests", {}).get(
            "review/human_decision.json"
        )
        != sha256_bytes(decision_bytes)
    ):
        raise TransactionError("HUMAN_DECISION_CUSTODY_BINDING_INVALID")
    return expected_decision, decision


def _record_payloads(tx: Path, *, predicted_events: Sequence[Mapping[str, Any]], finalized_at_utc: str) -> dict[str, bytes]:
    meta = _metadata(tx)
    transaction_id = meta["transaction_id"]
    finalization_source = _finalization_source_state(transaction_id, predicted_events)
    business_state, decision = _require_live_human_decision(
        tx, finalization_source, predicted_events
    )
    source = _read_authoritative_file(tx / "quarantine" / "source.bin", "SOURCE")
    normalized = _read_authoritative_file(
        tx / "quarantine" / "source.normalized", "NORMALIZED_SOURCE"
    )
    candidate = _read_authoritative_file(
        tx / "quarantine" / "candidate.bin", "CANDIDATE"
    )
    controls = _read_authoritative_file(
        tx / "review" / "control_results.jsonl", "CONTROL_RESULTS"
    )
    findings = _read_authoritative_file(
        tx / "review" / "findings.jsonl", "FINDINGS"
    )
    finding_rows = _load_jsonl(tx / "review" / "findings.jsonl")
    open_findings = [row for row in finding_rows if row.get("status") == "OPEN"]
    status = {
        "authority_effect": AUTHORITY_EFFECT,
        "business_state": business_state,
        "created_at_utc": meta["created_at_utc"],
        "finalized_at_utc": finalized_at_utc,
        "nonauthority": "This package records system-generated control evidence. It is not an assurance opinion or compliance certification.",
        "notice": NONASSURANCE_NOTICE,
        "report_notice": REPORT_NOTICE,
        "parent_transaction_id": meta["identity"]["parent_transaction_id"],
        "period_id": meta["period_id"],
        "schema_id": "uvlm.triadicbrain.aep01.status_and_nonassurance.v1",
        "segregation_posture": SEGREGATION_POSTURE,
        "signing_posture": SIGNING_POSTURE,
        "state": TransactionState.SEALED.value,
        "transaction_id": transaction_id,
    }
    system_identity = {
        "authority_effect": AUTHORITY_EFFECT,
        "model_identity": meta["model_identity"],
        "model_identity_posture": "NOT_APPLICABLE_NON_MODEL_EVENT" if meta['settings'].get('processing_kind')=='NON_MODEL_EVENT' else "USER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
        "product_name": PRODUCT_NAME,
        "product_version": VERSION,
        "system_id": meta["system_id"],
        "transaction_id": transaction_id,
        "use_case_id": meta["use_case_id"],
    }
    request = {
        "admission_status": "ADMITTED" if business_state != "REFUSED" else "REFUSED",
        "authority_effect": AUTHORITY_EFFECT,
        "consent_posture": "SYNTHETIC_DEMONSTRATION_INPUT",
        "requester_authority_posture": "LOCAL_DECLARED_NOT_EXTERNAL_AUTHORITY",
        "transaction_id": transaction_id,
    }
    source_manifest = {
        "authority_effect": AUTHORITY_EFFECT,
        "availability_limitation": "LOCAL_CAPTURED_BYTES_ONLY",
        "ingestion_method": "CAPTURED_BYTES",
        "normalization_profile": meta["normalization_profile"],
        "normalized_bytes": len(normalized),
        "normalized_sha256": sha256_bytes(normalized),
        "original_bytes": len(source),
        "original_sha256": sha256_bytes(source),
        "privacy_classification": "SYNTHETIC_PUBLIC_DEMONSTRATION",
        "source_media_type": meta["source_media_type"],
        "transaction_id": transaction_id,
        "user_declaration": True,
    }
    configuration = {
        "authority_effect": AUTHORITY_EFFECT,
        "control_catalog_version": "1.0.0",
        "effective_configuration_sha256": sha256_bytes(canonical_bytes({"prompt": meta["prompt"], "settings": meta["settings"]})),
        "feature_flags": {
            "optional_review_policy_selected": meta["review_policy"]["profile_id"] != "STANDARD",
            "remote_provider": False,
        },
        "prompt_components": [{"kind": "USER", "text": meta["prompt"]}],
        "review_policy": meta["review_policy"],
        "secret_references": [],
        "settings": meta["settings"],
        "transaction_id": transaction_id,
    }
    invocation = {
        "authority_effect": AUTHORITY_EFFECT,
        "candidate_bytes": len(candidate),
        "candidate_sha256": sha256_bytes(candidate),
        "capture_time_posture": "CALLER_SUPPLIED_DETERMINISTIC_UTC",
        "invocation_mode": "NON_MODEL_EVENT_NO_INVOCATION" if meta['settings'].get('processing_kind')=='NON_MODEL_EVENT' else "CAPTURED_CANDIDATE",
        "limitations": ["PROVIDER_AND_MODEL_IDENTITY_USER_DECLARED", "NO_PROVIDER_INVOCATION_PERFORMED"],
        "model_identity": meta["model_identity"],
        "provider_identity": "USER_DECLARED_OR_UNKNOWN",
        "provider_invoked": False,
        "raw_capture_method": "OPAQUE_LOCAL_BYTES",
        "transaction_id": transaction_id,
    }
    claim_map = derive_candidate_claim_map(
        transaction_id=transaction_id,
        candidate_bytes=candidate,
        source_bytes=source,
    )
    review = read_canonical_file(tx / "review" / "independent_review.json")
    orientation = read_canonical_file(tx / "review" / "orientation.json")
    rendered = render_transaction_review_html(
        transaction_id=transaction_id,
        business_state=str(business_state),
        open_findings=open_findings,
        product_name=PRODUCT_NAME,
    )
    result = {
        "00_STATUS_AND_NONASSURANCE.json": canonical_bytes(status),
        "01_AI_SYSTEM_IDENTITY.json": canonical_bytes(system_identity),
        "02_REQUEST_AUTHORITY_AND_CONSENT.json": canonical_bytes(request),
        "03_SOURCE_AND_RETRIEVAL_MANIFEST.json": canonical_bytes(source_manifest),
        "04_PROMPT_AND_CONFIGURATION_MANIFEST.json": canonical_bytes(configuration),
        "05_MODEL_INVOCATION_RECORD.json": canonical_bytes(invocation),
        "06_RAW_CANDIDATE_CAPTURE.bin": candidate,
        "07_CANDIDATE_AND_CLAIM_MAP.json": canonical_bytes(claim_map),
        "08_CONTROL_EXECUTION_RESULTS.jsonl": controls,
        "09_FINDINGS_AND_EXCEPTIONS.jsonl": findings,
        "10_SOPHIA_AUDIT_PACKET.json": canonical_bytes(review),
        "11_ATLAS_POSTURE_PACKET.json": canonical_bytes(orientation),
        "12_HUMAN_DECISION.json": canonical_bytes(decision),
        "14_CUSTODY_EVENTS.jsonl": ledger_bytes(predicted_events),
        "18_HUMAN_READABLE_REVIEW.html": rendered,
        "19_FRAMEWORK_CROSSWALK_SNAPSHOT.csv": render_framework_crosswalk_csv(),
        "20_CONTROL_CATALOG_SNAPSHOT.csv": render_control_catalog_csv(),
        "source/original.bin": source,
        "source/normalized.txt": normalized,
    }
    lineage_path = tx / "review" / "repair_lineage.json"
    if lineage_path.exists():
        result["13_REPAIR_LINEAGE.json"] = _read_authoritative_file(
            lineage_path, "REPAIR_LINEAGE"
        )
    policy_evaluation_path = tx / "review" / "review_policy_evaluation.json"
    if policy_evaluation_path.exists():
        result["21_REVIEW_POLICY_EVALUATION.json"] = (
            _read_authoritative_file(
                policy_evaluation_path, "REVIEW_POLICY_EVALUATION"
            )
        )
    policy_repair_path = tx / "review" / "review_policy_repair_authorization.json"
    if policy_repair_path.exists():
        result["22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json"] = (
            _read_authoritative_file(
                policy_repair_path, "REVIEW_POLICY_REPAIR_AUTHORIZATION"
            )
        )
    recovery_root = tx / "recovery"
    if recovery_root.exists():
        for path in sorted(recovery_root.glob("*.json"), key=lambda item: item.name):
            result[f"recovery/{path.name}"] = _read_authoritative_file(
                path, "RECOVERY_RECEIPT"
            )
    return result


def _evidence_content_root(records: Mapping[str, bytes]) -> str:
    """Hash exact pre-manifest evidence bytes without the circular custody ledger."""

    rows = [
        {
            "bytes": len(payload),
            "path": name,
            "sha256": sha256_bytes(payload),
        }
        for name, payload in sorted(records.items())
        if name != "14_CUSTODY_EVENTS.jsonl"
    ]
    return sha256_bytes(canonical_bytes(rows))


def finalize_transaction(
    store_root: Path,
    transaction_id: str,
    *,
    logical_time_utc: str,
) -> dict[str, Any]:
    store = _store_root(Path(store_root))
    tx = _transaction_root(store, transaction_id)
    requested_timestamp = _utc(logical_time_utc, "logical_time_utc")
    current = TransactionState(_state(tx)["current_state"])
    if _review_policy_requires_evaluation(
        _metadata(tx).get("review_policy", {})
    ):
        # Seal only after replaying the child and every bound parent policy
        # object.  This catches any post-decision mutation before a package is
        # materialized or a custody seal transition is attempted.
        _replay_review_policy_lifecycle(store, tx)
    startable = {
        TransactionState.APPROVED,
        TransactionState.HELD,
        TransactionState.REJECTED,
        TransactionState.REPAIR_CHILD_CREATED,
        TransactionState.REFUSED,
    }
    if current not in startable | {TransactionState.FINALIZATION_PENDING}:
        raise TransactionError("TRANSACTION_NOT_FINALIZABLE")
    # A retry reuses the first committed FINALIZATION_PENDING logical time so
    # already materialized record bytes remain deterministic and immutable.
    timestamp = (
        _utc(_state(tx)["logical_time_utc"], "stored_finalization_time")
        if current is TransactionState.FINALIZATION_PENDING
        else requested_timestamp
    )
    require_authorized(ActorClass.SERVICE_EVIDENCE_CUSTODIAN, Action.SEAL_TRANSACTION_PACKAGE, target_plane=Plane.CONTROL_EVIDENCE)
    if current in startable:
        _require_live_human_decision(
            tx,
            current,
            read_event_ledger(tx / "custody_events.jsonl"),
        )
        _transition(tx, TransactionState.FINALIZATION_PENDING, logical_time_utc=timestamp, actor_id="SERVICE-EVIDENCE-CUSTODIAN", actor_class=ActorClass.SERVICE_EVIDENCE_CUSTODIAN, plane=Plane.CONTROL_EVIDENCE, reason_codes=("FINALIZATION_STARTED",))
    try:
        preseal_records = _record_payloads(
            tx,
            predicted_events=read_event_ledger(tx / "custody_events.jsonl"),
            finalized_at_utc=timestamp,
        )
        evidence_content_root = _evidence_content_root(preseal_records)
        journal, predicted_events, _ = _make_transition(
            tx,
            TransactionState.SEALED,
            logical_time_utc=timestamp,
            actor_id="SERVICE-EVIDENCE-CUSTODIAN",
            actor_class=ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
            plane=Plane.CONTROL_EVIDENCE,
            reason_codes=("PACKAGE_SEALED_HASH_CHAIN_ONLY",),
            event_output_digests={
                "evidence_content_root": evidence_content_root,
            },
        )
        records = _record_payloads(tx, predicted_events=predicted_events, finalized_at_utc=timestamp)
        if _evidence_content_root(records) != evidence_content_root:
            raise TransactionError("PRESEAL_EVIDENCE_CONTENT_CHANGED")
        for name, payload in sorted(records.items()):
            _write_or_match(tx / "records" / Path(name), payload)
        manifest = read_canonical_file(store / "store_manifest.json")
        package_dir = store / "packages" / transaction_id
        from .transaction_package import (
            build_transaction_package,
            build_transaction_zip,
            verify_package_source_binding,
        )
        from .verification import verify_transaction_directory

        if package_dir.exists():
            package_receipt = verify_transaction_directory(package_dir)
        else:
            package_receipt = build_transaction_package(
                tx,
                package_dir,
                predecessor_commit=manifest["predecessor_commit"],
                predecessor_review_status="HOLD",
            )
        # Reject a stale or substituted existing package before publishing any
        # dependent ZIP bytes. Live custody is still the pre-seal image here.
        verify_package_source_binding(
            tx,
            package_dir,
            predecessor_commit=manifest["predecessor_commit"],
            predecessor_review_status="HOLD",
            require_live=False,
        )
        zip_path = store / "packages" / f"{transaction_id}.zip"
        if zip_path.exists():
            from .verification import verify_transaction_zip

            zip_receipt = verify_transaction_zip(zip_path)
        else:
            zip_receipt = build_transaction_zip(package_dir, zip_path)
        _verify_seal_outputs(store, tx, transaction_id, require_live=False)
        if os.path.lexists(tx / ".transition-pending.json"):
            raise TransactionError("UNEXPECTED_PENDING_TRANSITION_BEFORE_SEAL")
        write_exclusive_object(tx / ".transition-pending.json", journal)
        _finish_transition(
            tx,
            recovering=False,
            release_pending=False,
            before_state_publish=lambda: _verify_seal_outputs(
                store, tx, transaction_id, require_live=True
            ),
        )
        if _read_authoritative_file(
            tx / "custody_events.jsonl", "CUSTODY_LEDGER"
        ) != records["14_CUSTODY_EVENTS.jsonl"]:
            raise TransactionError("SEALED_CUSTODY_PREDICTION_MISMATCH")
        _verify_seal_outputs(store, tx, transaction_id, require_live=True)
        pending_after = require_single_link_file(tx / ".transition-pending.json")
        _validate_transition_journal(
            tx, strict_load_object(_read_transition_target(pending_after))
        )
        pending_after.unlink()
        return {
            "authority_effect": AUTHORITY_EFFECT,
            "directory_verification": package_receipt,
            "effects": {"network_used": False, "provider_invoked": False, "publication_performed": False},
            "result": "PASS",
            "state": TransactionState.SEALED.value,
            "transaction_id": transaction_id,
            "zip_verification": zip_receipt,
        }
    except BaseException as exc:
        pending_path = tx / ".transition-pending.json"
        pending_transition_id: str | None = None
        pending_journal_sha256: str | None = None
        if os.path.lexists(pending_path):
            try:
                pending_bytes = _read_transition_target(pending_path)
                pending_row = strict_load_object(pending_bytes)
                pending_transition_id = pending_row.get("transition_id")
                pending_journal_sha256 = sha256_bytes(pending_bytes)
            except (OSError, ValueError):
                # Never fabricate a binding if the pending evidence cannot be
                # safely authenticated. The retained error class and state
                # remain truthful, and recovery will fail closed separately.
                pending_transition_id = None
                pending_journal_sha256 = None
        failure = {
            "authority_effect": AUTHORITY_EFFECT,
            "error_class": type(exc).__name__,
            "finalization_time_utc": timestamp,
            "nonauthority": "This retained attempt record does not establish root cause or an assurance conclusion.",
            "pending_journal_sha256": pending_journal_sha256,
            "pending_transition_id": pending_transition_id,
            "result": "FINALIZATION_ATTEMPT_FAILED",
            "retry_permitted_from_state": TransactionState.FINALIZATION_PENDING.value,
            "schema_id": "uvlm.triadicbrain.aep01.finalization_failure_receipt.v1",
            "state_at_failure": _state(tx)["current_state"],
            "transaction_id": transaction_id,
        }
        digest = sha256_bytes(canonical_bytes(failure))
        _write_or_match(
            store / "failure_receipts" / f"finalization-{transaction_id}-{digest}.json",
            canonical_bytes(failure),
        )
        raise


def _state_identity_matches_metadata(
    tx: Path,
    state: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> None:
    identity_value = metadata.get("identity")
    if not isinstance(identity_value, Mapping) or set(identity_value) != {
        "parent_transaction_id",
        "root_transaction_id",
        "transaction_id",
    }:
        raise TransactionError("TRANSACTION_METADATA_IDENTITY_INVALID")
    try:
        identity = TransactionIdentity(
            identity_value["transaction_id"],
            parent_transaction_id=identity_value["parent_transaction_id"],
            root_transaction_id=identity_value["root_transaction_id"],
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise TransactionError("TRANSACTION_METADATA_IDENTITY_INVALID") from exc
    if (
        metadata.get("schema_id")
        != "uvlm.triadicbrain.aep01.transaction_registration.v1"
        or metadata.get("authority_effect") != AUTHORITY_EFFECT
        or metadata.get("transaction_id") != tx.name
        or identity.transaction_id != tx.name
        or state.get("transaction_id") != identity.transaction_id
        or state.get("parent_transaction_id") != identity.parent_transaction_id
        or state.get("root_transaction_id") != identity.root_transaction_id
    ):
        raise TransactionError("TRANSACTION_STATE_METADATA_IDENTITY_MISMATCH")


def _terminal_snapshot_is_complete(
    store: Path,
    tx: Path,
    state_value: Mapping[str, Any],
    metadata: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
) -> bool:
    """Authenticate a terminal snapshot without writing or repairing anything."""

    state = _validate_state_record(tx, state_value)
    _state_identity_matches_metadata(tx, state, metadata)
    if state["current_state"] != TransactionState.SEALED.value:
        return False
    receipt = verify_events(events)
    transition_events = [
        event
        for event in events
        if isinstance(event.get("operation"), str)
        and event["operation"].startswith("STATE_TRANSITION:")
    ]
    if len(transition_events) != state["sequence"] or not transition_events:
        raise TransactionError("TERMINAL_STATE_CUSTODY_SEQUENCE_INVALID")
    seal = transition_events[-1]
    expected_transition_id = f"tr_{sha256_bytes(canonical_bytes({
        'from': TransactionState.FINALIZATION_PENDING.value,
        'sequence': seal.get('sequence'),
        'to': TransactionState.SEALED.value,
        'transaction_id': tx.name,
    }))[:32]}"
    if (
        receipt.get("result") != "PASS"
        or receipt.get("transaction_id") != tx.name
        or seal.get("operation")
        != "STATE_TRANSITION:FINALIZATION_PENDING->SEALED"
        or seal.get("transaction_id") != tx.name
        or seal.get("subject_id") != tx.name
        or seal.get("output_digests", {}).get("state.json")
        != sha256_bytes(canonical_bytes(dict(state)))
        or state["last_transition_id"] != expected_transition_id
        or state["logical_time_utc"] != seal.get("logical_time")
    ):
        raise TransactionError("TERMINAL_STATE_CUSTODY_BINDING_INVALID")
    directory_receipt, zip_receipt = _verify_seal_outputs(
        store, tx, tx.name, require_live=True
    )
    if (
        directory_receipt.get("result") != "PASS"
        or directory_receipt.get("transaction_id") != tx.name
        or zip_receipt.get("result") != "PASS"
        or zip_receipt.get("transaction_id") != tx.name
    ):
        raise TransactionError("TERMINAL_PACKAGE_COHERENCE_INVALID")
    return True


def transaction_snapshot(store_root: Path, transaction_id: str) -> dict[str, Any]:
    store = _store_root(Path(store_root))
    tx = _transaction_root(store, transaction_id)
    state = read_canonical_file(tx / "state.json")
    metadata = _metadata(tx)
    custody_valid = True
    try:
        events = read_event_ledger(tx / "custody_events.jsonl")
        custody = verify_events(events)
    except Exception:
        events = []
        custody_valid = False
        custody = {
            "authority_effect": AUTHORITY_EFFECT,
            "reason_code": "CUSTODY_REPLAY_INVALID",
            "result": "FAIL",
            "transaction_id": transaction_id,
            "valid": False,
        }
    # Preserve the public contract that a selected optional review policy is
    # authenticated on every snapshot.  This is distinct from terminal package
    # coherence: a mutated policy declaration is an explicit caller-visible
    # error, never a condition silently projected as ordinary incompleteness.
    _read_review_policy_evaluation(
        tx,
        required=_review_policy_requires_evaluation(
            metadata.get("review_policy", {})
        ),
    )
    pending_path = tx / ".transition-pending.json"
    pending_transition_id: str | None = None
    pending_transition_phase: str | None = None
    if os.path.lexists(pending_path):
        try:
            pending = _validate_transition_journal(
                tx, strict_load_object(_read_transition_target(pending_path))
            )
            pending_transition_id = pending["transition_id"]
            pending_transition_phase = pending["phase"]
        except Exception:
            pending_transition_id = "INVALID"
            pending_transition_phase = "INVALID"
    terminal_state_complete = False
    if (
        not os.path.lexists(pending_path)
        and custody_valid
        and state.get("current_state") == TransactionState.SEALED.value
    ):
        try:
            terminal_state_complete = _terminal_snapshot_is_complete(
                store, tx, state, metadata, events
            )
        except Exception:
            terminal_state_complete = False
    state_name = state.get("current_state")
    if type(state_name) is not str:
        state_name = "INVALID"
    identity = metadata.get("identity")
    if not isinstance(identity, Mapping):
        identity = {}
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "candidate_sha256": metadata.get("candidate_sha256"),
        "custody": custody,
        "identity": dict(identity),
        "parent_transaction_id": identity.get("parent_transaction_id"),
        "period_id": metadata.get("period_id"),
        "pending_transition": pending_transition_id is not None,
        "pending_transition_id": pending_transition_id,
        "pending_transition_phase": pending_transition_phase,
        "provider_invoked": False,
        "review_policy": metadata.get("review_policy"),
        "state": state_name,
        "terminal_state_complete": terminal_state_complete,
        "transaction_id": transaction_id,
    }


def list_transaction_snapshots(store_root: Path) -> list[dict[str, Any]]:
    store = _store_root(Path(store_root))
    rows = read_creation_ledger(store)
    result: list[dict[str, Any]] = []
    for row in rows:
        try:
            result.append(transaction_snapshot(store, row["transaction_id"]))
        except TransactionError:
            result.append({
                "authority_effect": AUTHORITY_EFFECT,
                "parent_transaction_id": row.get("parent_transaction_id"),
                "state": "INCOMPLETE_REGISTRATION",
                "transaction_id": row["transaction_id"],
            })
    return result


__all__ = [
    "CREATION_SCHEMA_ID",
    "JOURNAL_SCHEMA_ID",
    "RECOVERY_SCHEMA_ID",
    "SEGREGATION_POSTURE",
    "SIGNING_POSTURE",
    "STATE_SCHEMA_ID",
    "STORE_SCHEMA_ID",
    "TransactionError",
    "TransitionInterrupted",
    "create_evidence_store",
    "create_repair_child",
    "finalize_transaction",
    "list_transaction_snapshots",
    "read_creation_ledger",
    "recover_pending_transition",
    "register_captured_transaction",
    "register_platform_observed_transaction",
    "submit_human_decision",
    "transaction_snapshot",
]
