"""Fresh-path transaction evidence packages and deterministic ZIP exports."""

from __future__ import annotations

import csv
import io
import os
import secrets
import stat
import unicodedata
import zipfile
from pathlib import Path
from typing import Any

from . import AUTHORITY_EFFECT, NONASSURANCE_NOTICE, REPORT_NOTICE
from .canonical import (
    canonical_bytes,
    is_link_like,
    read_ordinary_bytes,
    read_canonical_file,
    require_existing_root,
    require_new_root,
    require_safe_ancestors,
    require_single_link_file,
    sha256_bytes,
    strict_load_object,
    write_exclusive_bytes,
    write_exclusive_object,
)


CORE_CONTENT_MEMBERS = (
    "00_STATUS_AND_NONASSURANCE.json",
    "01_AI_SYSTEM_IDENTITY.json",
    "02_REQUEST_AUTHORITY_AND_CONSENT.json",
    "03_SOURCE_AND_RETRIEVAL_MANIFEST.json",
    "04_PROMPT_AND_CONFIGURATION_MANIFEST.json",
    "05_MODEL_INVOCATION_RECORD.json",
    "06_RAW_CANDIDATE_CAPTURE.bin",
    "07_CANDIDATE_AND_CLAIM_MAP.json",
    "08_CONTROL_EXECUTION_RESULTS.jsonl",
    "09_FINDINGS_AND_EXCEPTIONS.jsonl",
    "10_SOPHIA_AUDIT_PACKET.json",
    "11_ATLAS_POSTURE_PACKET.json",
    "12_HUMAN_DECISION.json",
    "14_CUSTODY_EVENTS.jsonl",
    "18_HUMAN_READABLE_REVIEW.html",
    "19_FRAMEWORK_CROSSWALK_SNAPSHOT.csv",
    "20_CONTROL_CATALOG_SNAPSHOT.csv",
    "source/original.bin",
    "source/normalized.txt",
)

CONTROL_MEMBERS = (
    "15_EVIDENCE_PACKAGE_MANIFEST.json",
    "16_SHA256SUMS.txt",
    "17_VERIFICATION_RECEIPT.json",
)

FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
MAX_PACKAGE_FILES = 128
MAX_PACKAGE_BYTES = 64 * 1024 * 1024
MAX_PACKAGE_DIRECTORIES = 32


class PackageError(ValueError):
    """The evidence package failed a closed integrity or topology check."""


def _safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise PackageError("PACKAGE_MEMBER_PATH_INVALID")
    pure = Path(value)
    if pure.is_absolute() or value.startswith("/") or any(part in {"", ".", ".."} for part in value.split("/")):
        raise PackageError("PACKAGE_MEMBER_PATH_INVALID")
    if ":" in value or value != value.strip():
        raise PackageError("PACKAGE_MEMBER_PATH_INVALID")
    return value


def _walk_files(root: Path) -> dict[str, bytes]:
    root = require_existing_root(root)
    result: dict[str, bytes] = {}
    names_seen: set[str] = set()
    directories: set[str] = set()
    total = 0
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise PackageError("PACKAGE_DIRECTORY_ENUMERATION_FAILED") from exc
        if len(entries) > MAX_PACKAGE_FILES + MAX_PACKAGE_DIRECTORIES:
            raise PackageError("PACKAGE_TOPOLOGY_BOUNDS_EXCEEDED")
        child_directories: list[Path] = []
        for entry in entries:
            path = Path(entry.path)
            require_safe_ancestors(path)
            try:
                before = path.lstat()
            except OSError as exc:
                raise PackageError("PACKAGE_MEMBER_LSTAT_FAILED") from exc
            relative = _safe_relative(path.relative_to(root).as_posix())
            folded = unicodedata.normalize("NFC", relative).casefold()
            if folded in names_seen:
                raise PackageError("PACKAGE_MEMBER_CASE_COLLISION")
            names_seen.add(folded)
            if stat.S_ISDIR(before.st_mode):
                if is_link_like(path):
                    raise PackageError("PACKAGE_DIRECTORY_LINK_PROHIBITED")
                directories.add(relative)
                if len(directories) > MAX_PACKAGE_DIRECTORIES:
                    raise PackageError("PACKAGE_DIRECTORY_BOUNDS_EXCEEDED")
                child_directories.append(path)
                continue
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_nlink != 1
                or is_link_like(path)
            ):
                raise PackageError("PACKAGE_MEMBER_IRREGULAR")
            size = before.st_size
            if size < 0 or size > MAX_PACKAGE_BYTES:
                raise PackageError("PACKAGE_BOUNDS_EXCEEDED")
            total += size
            if len(result) >= MAX_PACKAGE_FILES or total > MAX_PACKAGE_BYTES:
                raise PackageError("PACKAGE_BOUNDS_EXCEEDED")
            try:
                payload = read_ordinary_bytes(path, maximum_bytes=size)
            except (OSError, ValueError) as exc:
                raise PackageError("PACKAGE_MEMBER_CHANGED_DURING_READ") from exc
            after = path.lstat()
            if (
                len(payload) != size
                or (
                    before.st_dev,
                    before.st_ino,
                    before.st_mode,
                    before.st_size,
                    before.st_mtime_ns,
                    before.st_nlink,
                )
                != (
                    after.st_dev,
                    after.st_ino,
                    after.st_mode,
                    after.st_size,
                    after.st_mtime_ns,
                    after.st_nlink,
                )
                or is_link_like(path)
            ):
                raise PackageError("PACKAGE_MEMBER_CHANGED_DURING_READ")
            result[relative] = payload
        pending.extend(reversed(child_directories))
    expected_directories: set[str] = set()
    for name in result:
        parts = name.split("/")[:-1]
        for index in range(1, len(parts) + 1):
            expected_directories.add("/".join(parts[:index]))
    if directories != expected_directories:
        raise PackageError("PACKAGE_DIRECTORY_TOPOLOGY_INVALID")
    return result


def _media_type(name: str) -> str:
    if name.endswith(".json"):
        return "application/json"
    if name.endswith(".jsonl"):
        return "application/x-ndjson"
    if name.endswith(".csv"):
        return "text/csv; charset=utf-8"
    if name.endswith(".html"):
        return "text/html; charset=utf-8"
    if name.endswith(".txt"):
        return "text/plain; charset=utf-8"
    return "application/octet-stream"


def _object_type(name: str) -> str:
    stem = Path(name).name.rsplit(".", 1)[0]
    if len(stem) > 3 and stem[:2].isdigit() and stem[2] == "_":
        stem = stem[3:]
    return stem.upper()


def _member_rows(content: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {
            "bytes": len(content[name]),
            "confidentiality": "PUBLIC_SYNTHETIC",
            "media_type": _media_type(name),
            "object_type": _object_type(name),
            "path": name,
            "required": True,
            "sha256": sha256_bytes(content[name]),
        }
        for name in sorted(content)
    ]


def _checksum_bytes(rows: dict[str, bytes]) -> bytes:
    return "".join(
        f"{sha256_bytes(payload)}  {name}\n" for name, payload in sorted(rows.items())
    ).encode("utf-8")


def _create_stage(target: Path) -> Path:
    target = require_new_root(target)
    stage = target.parent / f".{target.name}.stage-{secrets.token_hex(12)}"
    require_new_root(stage)
    stage.mkdir()
    return stage


def build_transaction_package(
    transaction_root: Path,
    output_directory: Path,
    *,
    predecessor_commit: str,
    predecessor_review_status: str = "PENDING",
) -> dict[str, Any]:
    """Build, verify, and atomically publish one closed evidence directory."""

    transaction_root = require_existing_root(Path(transaction_root))
    records = require_existing_root(transaction_root / "records")
    target = require_new_root(Path(output_directory))
    content = _walk_files(records)
    required = set(CORE_CONTENT_MEMBERS)
    if "13_REPAIR_LINEAGE.json" in content:
        required.add("13_REPAIR_LINEAGE.json")
    missing = sorted(required - set(content))
    if missing:
        raise PackageError(f"PACKAGE_REQUIRED_MEMBER_MISSING:{missing[0]}")
    if set(content) & set(CONTROL_MEMBERS):
        raise PackageError("PACKAGE_CONTROL_MEMBER_PREEXISTS")
    status = read_canonical_file(records / "00_STATUS_AND_NONASSURANCE.json")
    transaction_id = status.get("transaction_id")
    if not isinstance(transaction_id, str) or not transaction_id:
        raise PackageError("PACKAGE_TRANSACTION_ID_INVALID")
    stage = _create_stage(target)
    try:
        for name, payload in sorted(content.items()):
            destination = stage.joinpath(*name.split("/"))
            destination.parent.mkdir(parents=True, exist_ok=True)
            write_exclusive_bytes(destination, payload)
        member_rows = _member_rows(content)
        package_root = sha256_bytes(canonical_bytes(member_rows))
        manifest = {
            "authority_effect": AUTHORITY_EFFECT,
            "created_at_utc": status.get("created_at_utc"),
            "effects": {
                "memory_written": False,
                "network_used": False,
                "provider_invoked": False,
                "publication_performed": False,
            },
            "excluded_sensitive_members": [],
            "finalized": True,
            "finalized_at_utc": status.get("finalized_at_utc"),
            "members": member_rows,
            "nonauthority": (
                f"{NONASSURANCE_NOTICE} {REPORT_NOTICE} "
                "Hashes prove only bounded identity and closure, "
                "not truth, legal compliance, or control effectiveness."
            ),
            "package_id": f"PKG-{transaction_id}",
            "package_root_sha256": package_root,
            "parent_transaction_id": status.get("parent_transaction_id"),
            "predecessor_review_dependency": {
                "candidate_commit": predecessor_commit,
                "status": predecessor_review_status,
            },
            "schema_id": "uvlm.triadicbrain.aep01.evidence_package_manifest.v1",
            "segregation_posture": status.get("segregation_posture"),
            "signing_posture": "HASH_CHAIN_ONLY",
            "state": status.get("business_state"),
            "transaction_id": transaction_id,
        }
        manifest_bytes = canonical_bytes(manifest)
        write_exclusive_bytes(stage / "15_EVIDENCE_PACKAGE_MANIFEST.json", manifest_bytes)
        checksummed = {**content, "15_EVIDENCE_PACKAGE_MANIFEST.json": manifest_bytes}
        checksum_bytes = _checksum_bytes(checksummed)
        write_exclusive_bytes(stage / "16_SHA256SUMS.txt", checksum_bytes)
        verification = {
            "authority_effect": AUTHORITY_EFFECT,
            "checksums_sha256": sha256_bytes(checksum_bytes),
            "manifest_sha256": sha256_bytes(manifest_bytes),
            "model_or_provider_required": False,
            "nonauthority": NONASSURANCE_NOTICE,
            "package_root_sha256": package_root,
            "report_notice": REPORT_NOTICE,
            "result": "PASS",
            "schema_id": "uvlm.triadicbrain.aep01.verification_receipt.v1",
            "transaction_id": transaction_id,
            "verification_scope": "DECLARED_MEMBERS_CHECKSUMS_AND_CUSTODY_IDENTITY_ONLY",
        }
        write_exclusive_object(stage / "17_VERIFICATION_RECEIPT.json", verification)
        from .verification import verify_transaction_directory

        observed = verify_transaction_directory(stage)
        if observed.get("result") != "PASS":
            raise PackageError("PACKAGE_STAGE_VERIFICATION_FAILED")
        os.rename(stage, target)
    except BaseException:
        # Evidence remains at the unique stage for diagnosis.  Never recursively
        # delete a path after a failed or interrupted finalization.
        raise
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "directory": str(target),
        "manifest_sha256": sha256_bytes(
            read_ordinary_bytes(
                target / "15_EVIDENCE_PACKAGE_MANIFEST.json",
                maximum_bytes=MAX_PACKAGE_BYTES,
            )
        ),
        "member_count": len(content) + len(CONTROL_MEMBERS),
        "package_root_sha256": package_root,
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.package_build_receipt.v1",
        "transaction_id": transaction_id,
    }


def verify_package_source_binding(
    transaction_root: Path,
    package_directory: Path,
    *,
    predecessor_commit: str,
    predecessor_review_status: str,
    require_live: bool = True,
) -> dict[str, Any]:
    """Bind an existing verified package to this transaction's exact records."""

    transaction = require_existing_root(Path(transaction_root))
    records = _walk_files(require_existing_root(transaction / "records"))
    package = _walk_files(require_existing_root(Path(package_directory)))
    packaged_records = {
        name: payload for name, payload in package.items() if name not in CONTROL_MEMBERS
    }
    if packaged_records != records:
        raise PackageError("PACKAGE_TRANSACTION_RECORD_BINDING_INVALID")
    try:
        status = strict_load_object(records["00_STATUS_AND_NONASSURANCE.json"])
        packaged_decision = strict_load_object(records["12_HUMAN_DECISION.json"])
    except (KeyError, ValueError) as exc:
        raise PackageError("PACKAGE_DECISION_STATUS_BINDING_INVALID") from exc
    refused = status.get("business_state") == "REFUSED"
    decision = transaction / "review" / "human_decision.json"
    if refused:
        if packaged_decision.get("decision") != "PENDING":
            raise PackageError("PACKAGE_REFUSAL_DECISION_BINDING_INVALID")
        if require_live and os.path.lexists(decision):
            raise PackageError("PACKAGE_REFUSAL_LIVE_DECISION_INVALID")
    elif packaged_decision.get("decision") == "PENDING":
        raise PackageError("PACKAGE_LIVE_HUMAN_DECISION_REQUIRED")
    live_bindings = {
        "06_RAW_CANDIDATE_CAPTURE.bin": transaction / "quarantine" / "candidate.bin",
        "08_CONTROL_EXECUTION_RESULTS.jsonl": transaction / "review" / "control_results.jsonl",
        "09_FINDINGS_AND_EXCEPTIONS.jsonl": transaction / "review" / "findings.jsonl",
        "10_SOPHIA_AUDIT_PACKET.json": transaction / "review" / "independent_review.json",
        "11_ATLAS_POSTURE_PACKET.json": transaction / "review" / "orientation.json",
        "14_CUSTODY_EVENTS.jsonl": transaction / "custody_events.jsonl",
        "source/original.bin": transaction / "quarantine" / "source.bin",
        "source/normalized.txt": transaction / "quarantine" / "source.normalized",
    }
    if not refused:
        live_bindings["12_HUMAN_DECISION.json"] = decision
    lineage = transaction / "review" / "repair_lineage.json"
    if lineage.exists():
        live_bindings["13_REPAIR_LINEAGE.json"] = lineage
    policy_evaluation = transaction / "review" / "review_policy_evaluation.json"
    if policy_evaluation.exists():
        live_bindings["21_REVIEW_POLICY_EVALUATION.json"] = policy_evaluation
    policy_repair = (
        transaction / "review" / "review_policy_repair_authorization.json"
    )
    if policy_repair.exists():
        live_bindings["22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json"] = policy_repair
    recovery_root = transaction / "recovery"
    if recovery_root.exists():
        for recovery in sorted(recovery_root.glob("*.json"), key=lambda item: item.name):
            live_bindings[f"recovery/{recovery.name}"] = recovery
    if require_live:
        optional_live_members = {
            "13_REPAIR_LINEAGE.json": lineage,
            "21_REVIEW_POLICY_EVALUATION.json": policy_evaluation,
            "22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json": policy_repair,
        }
        for name, live_path in optional_live_members.items():
            if (name in records) != os.path.lexists(live_path):
                raise PackageError(
                    f"PACKAGE_LIVE_OPTIONAL_TOPOLOGY_INVALID:{name}"
                )
        for name, live_path in live_bindings.items():
            try:
                live_payload = read_ordinary_bytes(
                    live_path, maximum_bytes=MAX_PACKAGE_BYTES
                )
            except (OSError, ValueError) as exc:
                raise PackageError("PACKAGE_LIVE_EVIDENCE_BINDING_UNAVAILABLE") from exc
            if records.get(name) != live_payload:
                raise PackageError(f"PACKAGE_LIVE_EVIDENCE_BINDING_INVALID:{name}")
        packaged_recovery = {name for name in records if name.startswith("recovery/")}
        expected_recovery = {
            name for name in live_bindings if name.startswith("recovery/")
        }
        if packaged_recovery != expected_recovery:
            raise PackageError("PACKAGE_LIVE_RECOVERY_TOPOLOGY_INVALID")
        custody_lines = records["14_CUSTODY_EVENTS.jsonl"].splitlines(
            keepends=True
        )
        if not custody_lines:
            raise PackageError("PACKAGE_LIVE_TRANSACTION_BINDING_INVALID")
        try:
            first_event = strict_load_object(custody_lines[0])
            transaction_payload = read_ordinary_bytes(
                transaction / "transaction.json", maximum_bytes=MAX_PACKAGE_BYTES
            )
        except (OSError, ValueError) as exc:
            raise PackageError(
                "PACKAGE_LIVE_TRANSACTION_BINDING_UNAVAILABLE"
            ) from exc
        if (
            first_event.get("output_digests", {}).get("transaction.json")
            != sha256_bytes(transaction_payload)
        ):
            raise PackageError("PACKAGE_LIVE_TRANSACTION_BINDING_INVALID")
    manifest = read_canonical_file(
        Path(package_directory) / "15_EVIDENCE_PACKAGE_MANIFEST.json"
    )
    if (
        status.get("transaction_id") != transaction.name
        or manifest.get("transaction_id") != transaction.name
        or manifest.get("predecessor_review_dependency")
        != {
            "candidate_commit": predecessor_commit,
            "status": predecessor_review_status,
        }
    ):
        raise PackageError("PACKAGE_TRANSACTION_IDENTITY_BINDING_INVALID")
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "record_count": len(records),
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.package_source_binding.v1",
        "transaction_id": transaction.name,
    }


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_STORED
    info.create_system = 3
    info.external_attr = 0o100444 << 16
    info.flag_bits = 0
    return info


def _deterministic_zip_bytes(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", allowZip64=False) as archive:
        archive.comment = b""
        for name, payload in sorted(files.items()):
            archive.writestr(_zip_info(name), payload)
    return buffer.getvalue()


def build_transaction_zip(package_directory: Path, output_zip: Path) -> dict[str, Any]:
    """Create a deterministic, stored ZIP from a verified package directory."""

    from .verification import verify_transaction_directory, verify_transaction_zip

    package_directory = require_existing_root(Path(package_directory))
    if verify_transaction_directory(package_directory).get("result") != "PASS":
        raise PackageError("PACKAGE_DIRECTORY_NOT_VERIFIED")
    target = Path(output_zip)
    if not target.is_absolute() or target == Path(target.anchor) or os.path.lexists(target):
        raise PackageError("PACKAGE_ZIP_OUTPUT_UNSAFE_OR_EXISTS")
    require_safe_ancestors(target, include_leaf=False)
    if not target.parent.is_dir():
        raise PackageError("PACKAGE_ZIP_PARENT_UNAVAILABLE")
    files = _walk_files(package_directory)
    payload = _deterministic_zip_bytes(files)
    write_exclusive_bytes(target, payload)
    receipt = verify_transaction_zip(target)
    if receipt.get("result") != "PASS":
        raise PackageError("PACKAGE_ZIP_VERIFICATION_FAILED")
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "bytes": len(payload),
        "member_count": len(files),
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.package_zip_receipt.v1",
        "sha256": sha256_bytes(payload),
        "zip": str(target),
    }


def verify_zip_directory_binding(
    package_directory: Path,
    package_zip: Path,
) -> dict[str, Any]:
    """Require an existing ZIP to be the exact deterministic encoding of a directory."""

    directory = require_existing_root(Path(package_directory))
    files = _walk_files(directory)
    expected = _deterministic_zip_bytes(files)
    path = require_single_link_file(Path(package_zip))
    before = path.lstat()
    if before.st_size != len(expected):
        raise PackageError("PACKAGE_ZIP_DIRECTORY_BINDING_INVALID")
    actual = read_ordinary_bytes(path, maximum_bytes=MAX_PACKAGE_BYTES)
    require_single_link_file(path)
    after = path.lstat()
    if (
        actual != expected
        or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_nlink)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_nlink)
    ):
        raise PackageError("PACKAGE_ZIP_DIRECTORY_BINDING_INVALID")
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.zip_directory_binding.v1",
        "sha256": sha256_bytes(actual),
    }


__all__ = [
    "CONTROL_MEMBERS",
    "CORE_CONTENT_MEMBERS",
    "FIXED_ZIP_TIME",
    "MAX_PACKAGE_BYTES",
    "MAX_PACKAGE_FILES",
    "PackageError",
    "build_transaction_package",
    "build_transaction_zip",
    "verify_package_source_binding",
    "verify_zip_directory_binding",
]
