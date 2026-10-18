"""Hash-linked, independently reproducible AEP01 custody events."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import AUTHORITY_EFFECT, NONASSURANCE_NOTICE
from .canonical import (
    CanonicalError,
    MAX_CANONICAL_BYTES,
    canonical_bytes,
    read_ordinary_bytes,
    require_integer,
    require_single_link_file,
    sha256_bytes,
    strict_load_object,
    write_exclusive_bytes,
)
from .models import ActorClass, CONTROL_OUTCOMES, Plane, require_identifier


CUSTODY_SCHEMA_ID = "uvlm.triadicbrain.aep01.custody_event.v1"
CUSTODY_VERIFICATION_SCHEMA_ID = (
    "uvlm.triadicbrain.aep01.custody_verification_receipt.v1"
)
MAX_LEDGER_BYTES = 64 * 1024 * 1024
ZERO_SIDE_EFFECTS = {
    "deployment_performed": False,
    "memory_written": False,
    "merge_performed": False,
    "network_used": False,
    "provider_invoked": False,
    "publication_performed": False,
    "release_performed": False,
    "training_used": False,
}

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CUSTODY_RESULTS = frozenset((*CONTROL_OUTCOMES, "REFUSED"))
_EVENT_FIELDS = frozenset(
    {
        "actor_class",
        "actor_id",
        "authority_effect",
        "event_sha256",
        "input_digests",
        "ledger_id",
        "logical_time",
        "observed_time_utc",
        "operation",
        "output_digests",
        "plane",
        "previous_event_sha256",
        "reason_codes",
        "result",
        "schema_id",
        "sequence",
        "side_effects",
        "subject_id",
        "subject_type",
        "transaction_id",
    }
)


class CustodyError(ValueError):
    """A custody operation or ledger failed closed."""


def _required_text(value: Any, code: str, *, maximum: int = 512) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise CustodyError(code)
    if unicodedata.normalize("NFC", value) != value:
        raise CustodyError(code)
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise CustodyError(code) from exc
    return value


def _digest(value: Any, code: str) -> str:
    if type(value) is not str or not _HEX64.fullmatch(value):
        raise CustodyError(code)
    return value


def _digest_map(value: Any, code: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise CustodyError(code)
    result: dict[str, str] = {}
    for key, digest in value.items():
        normalized = _required_text(key, code, maximum=256)
        if normalized in result:
            raise CustodyError(code)
        result[normalized] = _digest(digest, code)
    return result


def _reason_codes(value: Any) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise CustodyError("CUSTODY_REASON_CODES_INVALID")
    rows = [
        _required_text(item, "CUSTODY_REASON_CODES_INVALID", maximum=128)
        for item in value
    ]
    if len(rows) != len(set(rows)):
        raise CustodyError("CUSTODY_REASON_CODES_DUPLICATE")
    return rows


def _observed_time(value: Any) -> str | None:
    if value is None:
        return None
    text = _required_text(value, "CUSTODY_OBSERVED_TIME_INVALID", maximum=64)
    try:
        parsed = datetime.fromisoformat(
            text[:-1] + "+00:00" if text.endswith("Z") else text
        )
    except ValueError as exc:
        raise CustodyError("CUSTODY_OBSERVED_TIME_INVALID") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise CustodyError("CUSTODY_OBSERVED_TIME_NOT_UTC")
    return text


def _side_effects(value: Any) -> dict[str, Any]:
    if value is None:
        return dict(ZERO_SIDE_EFFECTS)
    if not isinstance(value, Mapping):
        raise CustodyError("CUSTODY_SIDE_EFFECTS_INVALID")
    result = dict(ZERO_SIDE_EFFECTS)
    for key, observed in value.items():
        name = _required_text(key, "CUSTODY_SIDE_EFFECTS_INVALID", maximum=128)
        if name in ZERO_SIDE_EFFECTS and observed is not False:
            raise CustodyError("CUSTODY_PROHIBITED_SIDE_EFFECT")
        result[name] = observed
    try:
        canonical_bytes(result)
    except CanonicalError as exc:
        raise CustodyError("CUSTODY_SIDE_EFFECTS_INVALID") from exc
    return result


def _unsigned_event(event: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in event.items() if key != "event_sha256"}


def event_sha256(event: Mapping[str, Any]) -> str:
    """Reproduce an event digest over canonical bytes excluding its digest field."""

    if not isinstance(event, Mapping):
        raise CustodyError("CUSTODY_EVENT_OBJECT_REQUIRED")
    try:
        return sha256_bytes(canonical_bytes(_unsigned_event(event)))
    except CanonicalError as exc:
        raise CustodyError("CUSTODY_EVENT_NOT_CANONICAL") from exc


def build_event(
    *,
    ledger_id: str,
    transaction_id: str,
    sequence: int,
    logical_time: str,
    observed_time_utc: str | None,
    actor_id: str,
    actor_class: ActorClass | str,
    plane: Plane | str,
    operation: str,
    subject_type: str,
    subject_id: str,
    input_digests: Mapping[str, str] | None = None,
    output_digests: Mapping[str, str] | None = None,
    previous_event_sha256: str | None = None,
    result: str = "PASS",
    reason_codes: Sequence[str] = (),
    side_effects: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one exact event whose digest is independently reproducible."""

    try:
        ledger = require_identifier(ledger_id, "ledger_id")
        transaction = require_identifier(transaction_id, "transaction_id")
        actor = require_identifier(actor_id, "actor_id")
        subject = require_identifier(subject_id, "subject_id")
    except ValueError as exc:
        raise CustodyError("CUSTODY_IDENTIFIER_INVALID") from exc
    try:
        actor_kind = ActorClass(actor_class)
    except (TypeError, ValueError) as exc:
        raise CustodyError("CUSTODY_ACTOR_CLASS_INVALID") from exc
    try:
        event_plane = Plane(plane)
    except (TypeError, ValueError) as exc:
        raise CustodyError("CUSTODY_PLANE_INVALID") from exc
    try:
        event_sequence = require_integer(sequence, "sequence", minimum=1)
    except CanonicalError as exc:
        raise CustodyError("CUSTODY_SEQUENCE_INVALID") from exc
    previous = None
    if previous_event_sha256 is not None:
        previous = _digest(
            previous_event_sha256, "CUSTODY_PREVIOUS_EVENT_DIGEST_INVALID"
        )
    if event_sequence == 1 and previous is not None:
        raise CustodyError("CUSTODY_FIRST_EVENT_PREVIOUS_DIGEST_NOT_NULL")
    if event_sequence > 1 and previous is None:
        raise CustodyError("CUSTODY_PREVIOUS_EVENT_DIGEST_REQUIRED")
    if result not in _CUSTODY_RESULTS:
        raise CustodyError("CUSTODY_RESULT_INVALID")

    event: dict[str, Any] = {
        "actor_class": actor_kind.value,
        "actor_id": actor,
        "authority_effect": AUTHORITY_EFFECT,
        "input_digests": _digest_map(
            input_digests or {}, "CUSTODY_INPUT_DIGESTS_INVALID"
        ),
        "ledger_id": ledger,
        "logical_time": _required_text(
            logical_time, "CUSTODY_LOGICAL_TIME_INVALID", maximum=128
        ),
        "observed_time_utc": _observed_time(observed_time_utc),
        "operation": _required_text(
            operation, "CUSTODY_OPERATION_INVALID", maximum=128
        ),
        "output_digests": _digest_map(
            output_digests or {}, "CUSTODY_OUTPUT_DIGESTS_INVALID"
        ),
        "plane": event_plane.value,
        "previous_event_sha256": previous,
        "reason_codes": _reason_codes(reason_codes),
        "result": result,
        "schema_id": CUSTODY_SCHEMA_ID,
        "sequence": event_sequence,
        "side_effects": _side_effects(side_effects),
        "subject_id": subject,
        "subject_type": _required_text(
            subject_type, "CUSTODY_SUBJECT_TYPE_INVALID", maximum=128
        ),
        "transaction_id": transaction,
    }
    event["event_sha256"] = event_sha256(event)
    return event


def _validate_event_shape(event: Any) -> dict[str, Any]:
    if not isinstance(event, Mapping) or set(event) != _EVENT_FIELDS:
        raise CustodyError("CUSTODY_EVENT_FIELDS_INVALID")
    # Rebuild from semantic fields so type and enum checks do not trust input.
    rebuilt = build_event(
        ledger_id=event["ledger_id"],
        transaction_id=event["transaction_id"],
        sequence=event["sequence"],
        logical_time=event["logical_time"],
        observed_time_utc=event["observed_time_utc"],
        actor_id=event["actor_id"],
        actor_class=event["actor_class"],
        plane=event["plane"],
        operation=event["operation"],
        subject_type=event["subject_type"],
        subject_id=event["subject_id"],
        input_digests=event["input_digests"],
        output_digests=event["output_digests"],
        previous_event_sha256=event["previous_event_sha256"],
        result=event["result"],
        reason_codes=event["reason_codes"],
        side_effects=event["side_effects"],
    )
    if event.get("authority_effect") != AUTHORITY_EFFECT:
        raise CustodyError("CUSTODY_AUTHORITY_EFFECT_PROHIBITED")
    if event.get("schema_id") != CUSTODY_SCHEMA_ID:
        raise CustodyError("CUSTODY_SCHEMA_INVALID")
    supplied_hash = _digest(event.get("event_sha256"), "CUSTODY_EVENT_DIGEST_INVALID")
    if supplied_hash != rebuilt["event_sha256"]:
        raise CustodyError("CUSTODY_EVENT_DIGEST_MISMATCH")
    if dict(event) != rebuilt:
        raise CustodyError("CUSTODY_EVENT_SEMANTIC_MISMATCH")
    return rebuilt


def verify_events(events: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Independently verify sequence, identities, links, and every event digest."""

    if isinstance(events, (str, bytes)) or not isinstance(events, Sequence) or not events:
        raise CustodyError("CUSTODY_LEDGER_EMPTY_OR_INVALID")
    sequences: list[int] = []
    for event in events:
        if not isinstance(event, Mapping):
            raise CustodyError("CUSTODY_EVENT_OBJECT_REQUIRED")
        try:
            sequences.append(require_integer(event.get("sequence"), "sequence", minimum=1))
        except CanonicalError as exc:
            raise CustodyError("CUSTODY_SEQUENCE_INVALID") from exc
    if len(sequences) != len(set(sequences)):
        raise CustodyError("CUSTODY_SEQUENCE_DUPLICATE")
    expected = list(range(1, len(events) + 1))
    if sorted(sequences) != expected:
        raise CustodyError("CUSTODY_SEQUENCE_GAP")
    if sequences != expected:
        raise CustodyError("CUSTODY_ORDER_INVALID")

    verified: list[dict[str, Any]] = []
    ledger_id: str | None = None
    transaction_id: str | None = None
    prior_digest: str | None = None
    observed_hashes: set[str] = set()
    for event in events:
        row = _validate_event_shape(event)
        if ledger_id is None:
            ledger_id = row["ledger_id"]
            transaction_id = row["transaction_id"]
        elif row["ledger_id"] != ledger_id:
            raise CustodyError("CUSTODY_LEDGER_IDENTITY_MISMATCH")
        elif row["transaction_id"] != transaction_id:
            raise CustodyError("CUSTODY_TRANSACTION_IDENTITY_MISMATCH")
        if row["previous_event_sha256"] != prior_digest:
            raise CustodyError("CUSTODY_PREVIOUS_EVENT_DIGEST_MISMATCH")
        digest = row["event_sha256"]
        if digest in observed_hashes:
            raise CustodyError("CUSTODY_EVENT_DUPLICATE")
        observed_hashes.add(digest)
        prior_digest = digest
        verified.append(row)

    payload = b"".join(canonical_bytes(row) for row in verified)
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "event_count": len(verified),
        "first_event_sha256": verified[0]["event_sha256"],
        "last_event_sha256": verified[-1]["event_sha256"],
        "ledger_id": ledger_id,
        "ledger_sha256": sha256_bytes(payload),
        "nonassurance_notice": NONASSURANCE_NOTICE,
        "result": "PASS",
        "schema_id": CUSTODY_VERIFICATION_SCHEMA_ID,
        "transaction_id": transaction_id,
        "valid": True,
    }


def append_event(
    events: Sequence[Mapping[str, Any]],
    **fields: Any,
) -> dict[str, Any]:
    """Build the next event without mutating the caller's ledger sequence."""

    if events:
        receipt = verify_events(events)
        fields.setdefault("ledger_id", receipt["ledger_id"])
        fields.setdefault("transaction_id", receipt["transaction_id"])
        fields["sequence"] = len(events) + 1
        fields["previous_event_sha256"] = receipt["last_event_sha256"]
    else:
        fields["sequence"] = 1
        fields["previous_event_sha256"] = None
    return build_event(**fields)


def ledger_bytes(events: Sequence[Mapping[str, Any]]) -> bytes:
    verify_events(events)
    return b"".join(canonical_bytes(dict(event)) for event in events)


def read_event_ledger(
    path: str | Path,
    *,
    maximum_bytes: int = MAX_LEDGER_BYTES,
) -> list[dict[str, Any]]:
    if type(maximum_bytes) is not int or maximum_bytes < 1:
        raise CustodyError("CUSTODY_LEDGER_SIZE_LIMIT_INVALID")
    try:
        payload = read_ordinary_bytes(path, maximum_bytes=maximum_bytes)
        if not payload:
            raise CustodyError("CUSTODY_LEDGER_EMPTY_OR_OVERSIZE")
    except CustodyError:
        raise
    except (CanonicalError, OSError) as exc:
        raise CustodyError("CUSTODY_LEDGER_FILE_UNSAFE") from exc
    rows: list[dict[str, Any]] = []
    for line in payload.splitlines(keepends=True):
        try:
            rows.append(strict_load_object(line, maximum_bytes=MAX_CANONICAL_BYTES))
        except CanonicalError as exc:
            raise CustodyError("CUSTODY_LEDGER_LINE_NOT_CANONICAL") from exc
    if b"".join(canonical_bytes(row) for row in rows) != payload:
        raise CustodyError("CUSTODY_LEDGER_NOT_CANONICAL_JSONL")
    verify_events(rows)
    return rows


def write_event_ledger(
    path: str | Path,
    events: Sequence[Mapping[str, Any]],
) -> Path:
    try:
        return write_exclusive_bytes(path, ledger_bytes(events))
    except CanonicalError as exc:
        raise CustodyError("CUSTODY_LEDGER_WRITE_FAILED") from exc


__all__ = [
    "CUSTODY_SCHEMA_ID",
    "CUSTODY_VERIFICATION_SCHEMA_ID",
    "CustodyError",
    "MAX_LEDGER_BYTES",
    "ZERO_SIDE_EFFECTS",
    "append_event",
    "build_event",
    "event_sha256",
    "ledger_bytes",
    "read_event_ledger",
    "verify_events",
    "write_event_ledger",
]
