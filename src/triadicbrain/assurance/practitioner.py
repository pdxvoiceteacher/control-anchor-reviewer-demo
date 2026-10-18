"""Read-only practitioner evidence indexing and separate work products."""

from __future__ import annotations

import copy
import csv
import io
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from .canonical import canonical_bytes, sha256_bytes


NONASSURANCE_NOTICE = "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED."
AUTHORITY_EFFECT = "NONE"
ANNOTATION_TYPES = {
    "NOTE",
    "MAPPING_CHALLENGE",
    "EVIDENCE_REQUEST",
    "PROCEDURE_RECORD",
    "FINDING_DRAFT",
    "EXTERNAL_CONCLUSION_REFERENCE",
}
CHALLENGE_TYPES = {
    "CONTROL_FRAMEWORK_MAPPING",
    "FINDING_CLASSIFICATION",
    "SEVERITY_RISK_POSTURE",
    "POPULATION_INCLUSION_EXCLUSION",
    "MANAGEMENT_DESCRIPTION",
    "EVIDENCE_REFERENCE",
    "SYSTEM_GENERATED_METRIC",
}
CHALLENGE_STATES = {
    "OPEN",
    "MANAGEMENT_RESPONSE_PROVIDED",
    "ACCEPTED",
    "REJECTED",
    "PARTIALLY_ACCEPTED",
    "SUPERSEDED",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ANNOTATION_V1_FIELDS = {
    "schema_id",
    "annotation_id",
    "practitioner_actor_id",
    "engagement_id",
    "annotation_type",
    "evidence_refs",
    "content",
    "created_at_utc",
    "supersedes_annotation_id",
    "source_evidence_mutated",
    "signature_posture",
    "nonauthority",
}


class PractitionerContractError(ValueError):
    """A practitioner operation crossed the source or opinion boundary."""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        result = to_dict()
        if isinstance(result, Mapping):
            return result
    raise PractitionerContractError(f"{label}_MUST_BE_OBJECT")


def _text(value: Any, label: str, *, max_length: int = 20_000) -> str:
    if not isinstance(value, str) or not value:
        raise PractitionerContractError(f"{label}_MUST_BE_NONEMPTY_TEXT")
    value = unicodedata.normalize("NFC", value)
    if len(value) > max_length:
        raise PractitionerContractError(f"{label}_TOO_LONG")
    return value


def _utc(value: Any, label: str) -> str:
    text = _text(value, label)
    if not text.endswith("Z"):
        raise PractitionerContractError(f"{label}_MUST_BE_UTC_Z")
    try:
        datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError as exc:
        raise PractitionerContractError(f"{label}_INVALID") from exc
    return text


def _no_opinion_fields() -> dict[str, Any]:
    return {
        "contains_assurance_conclusion": False,
        "opinion_generated_or_prefilled": False,
        "suitable_criteria_determined": False,
        "materiality_determined": False,
        "sample_sufficiency_determined": False,
        "evidence_sufficiency_determined": False,
        "control_effectiveness_determined": False,
        "practitioner_signature_generated": False,
        "nonassurance": NONASSURANCE_NOTICE,
        "authority_effect": AUTHORITY_EFFECT,
    }


def _object_id(row: Mapping[str, Any], kind: str) -> str:
    candidates = {
        "TRANSACTION": ("transaction_id", "population_row_id"),
        "CONTROL_EXECUTION": ("execution_id", "control_id"),
        "FINDING_EXCEPTION": ("finding_id", "exception_id", "row_id"),
        "EVIDENCE_PACKAGE": ("package_id", "transaction_id"),
        "VERIFICATION": ("verification_id", "receipt_id", "transaction_id"),
        "PERIOD_REVISION": ("revision_id",),
        "OTHER_EVIDENCE": (
            "evidence_id",
            "event_sha256",
            "event_id",
            "change_id",
            "row_id",
        ),
    }
    for key in candidates[kind]:
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    raise PractitionerContractError(f"{kind}_OBJECT_ID_MISSING")


def _evidence_items(kind: str, values: Sequence[Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for value in values:
        source = copy.deepcopy(dict(_mapping(value, kind)))
        object_id = _object_id(source, kind)
        if object_id in seen:
            raise PractitionerContractError(f"DUPLICATE_{kind}_OBJECT_ID")
        seen.add(object_id)
        digest = sha256_bytes(canonical_bytes(source))
        result.append(
            {
                "object_type": kind,
                "object_id": object_id,
                "sha256": digest,
                "read_only": True,
                "drill_through": {
                    "transaction_id": source.get("transaction_id"),
                    "source_row_ids": source.get("source_row_ids", []),
                },
                "adverse": bool(
                    source.get("adverse") is True
                    or source.get("result") in {"FAIL", "HOLD", "NOT_EXECUTED", "ERROR"}
                    or source.get("status") in {"OPEN", "FAIL", "HOLD", "ERROR"}
                ),
                "source_snapshot": source,
            }
        )
    return sorted(result, key=lambda row: (row["object_type"], row["object_id"]))


def build_practitioner_index(
    *,
    period_revision: Mapping[str, Any],
    population_rows: Sequence[Any],
    control_rows: Sequence[Any] = (),
    finding_rows: Sequence[Any] = (),
    package_rows: Sequence[Any] = (),
    verification_rows: Sequence[Any] = (),
    other_evidence_rows: Sequence[Any] = (),
    retained_period_revisions: Sequence[Any] = (),
) -> dict[str, Any]:
    """Create a neutral evidence index from defensive copies of source rows."""

    period = copy.deepcopy(dict(_mapping(period_revision, "PERIOD_REVISION")))
    population = _evidence_items("TRANSACTION", population_rows)
    controls = _evidence_items("CONTROL_EXECUTION", control_rows)
    findings = _evidence_items("FINDING_EXCEPTION", finding_rows)
    packages = _evidence_items("EVIDENCE_PACKAGE", package_rows)
    verifications = _evidence_items("VERIFICATION", verification_rows)
    other_evidence = _evidence_items("OTHER_EVIDENCE", other_evidence_rows)
    revisions = _evidence_items("PERIOD_REVISION", [*retained_period_revisions, period])
    evidence_items = sorted(
        [
            *population,
            *controls,
            *findings,
            *packages,
            *verifications,
            *other_evidence,
            *revisions,
        ],
        key=lambda row: (row["object_type"], row["object_id"]),
    )
    type_counts = Counter(row["object_type"] for row in evidence_items)
    transaction_ids = {row["object_id"] for row in population}
    declared_created = period.get("population_counts", {}).get("created")
    if declared_created is not None and declared_created != len(transaction_ids):
        raise PractitionerContractError("PRACTITIONER_INDEX_POPULATION_COUNT_MISMATCH")
    from .period import population_document

    observed_population_identity = population_document(
        [item["source_snapshot"] for item in population]
    )["population_identity"]
    if period.get("population_identity") != observed_population_identity:
        raise PractitionerContractError("PRACTITIONER_INDEX_POPULATION_IDENTITY_MISMATCH")
    declared_population_digests = period.get("population_row_digests")
    if not isinstance(declared_population_digests, list):
        raise PractitionerContractError("PRACTITIONER_INDEX_POPULATION_MANIFEST_MISSING")
    expected_population_manifest = {
        str(item["source_snapshot"].get("population_row_id")): item["sha256"]
        for item in population
    }
    observed_population_manifest = {
        str(entry.get("row_id")): entry.get("sha256")
        for entry in declared_population_digests
        if isinstance(entry, Mapping)
    }
    if observed_population_manifest != expected_population_manifest:
        raise PractitionerContractError("PRACTITIONER_INDEX_POPULATION_ITEM_SET_MISMATCH")
    declared_evidence_digests = period.get("evidence_row_digests")
    if not isinstance(declared_evidence_digests, list):
        raise PractitionerContractError("PRACTITIONER_INDEX_EVIDENCE_MANIFEST_MISSING")
    expected_evidence_manifest = {
        item["object_id"]: item["sha256"]
        for item in [*controls, *findings, *packages, *verifications, *other_evidence]
    }
    observed_evidence_manifest = {
        str(entry.get("row_id")): entry.get("sha256")
        for entry in declared_evidence_digests
        if isinstance(entry, Mapping)
    }
    if observed_evidence_manifest != expected_evidence_manifest:
        raise PractitionerContractError("PRACTITIONER_INDEX_EVIDENCE_ITEM_SET_MISMATCH")
    period_without_identity = copy.deepcopy(period)
    observed_revision_identity = period_without_identity.pop("revision_identity", None)
    if observed_revision_identity != sha256_bytes(canonical_bytes(period_without_identity)):
        raise PractitionerContractError("PRACTITIONER_INDEX_PERIOD_REVISION_IDENTITY_INVALID")
    current_revision_number = period.get("revision_number")
    if type(current_revision_number) is not int or current_revision_number < 1:
        raise PractitionerContractError("PRACTITIONER_INDEX_REVISION_NUMBER_INVALID")
    revisions_by_number: dict[int, Mapping[str, Any]] = {}
    for item in revisions:
        snapshot = item["source_snapshot"]
        number = snapshot.get("revision_number")
        if (
            type(number) is not int
            or number < 1
            or number in revisions_by_number
            or snapshot.get("period_id") != period.get("period_id")
            or snapshot.get("revision_id") != f"{period.get('period_id')}-R{number:04d}"
        ):
            raise PractitionerContractError("PRACTITIONER_INDEX_REVISION_SET_INVALID")
        revision_without_identity = copy.deepcopy(snapshot)
        identity = revision_without_identity.pop("revision_identity", None)
        if identity != sha256_bytes(canonical_bytes(revision_without_identity)):
            raise PractitionerContractError("PRACTITIONER_INDEX_RETAINED_REVISION_IDENTITY_INVALID")
        revisions_by_number[number] = item
    if set(revisions_by_number) != set(range(1, current_revision_number + 1)):
        raise PractitionerContractError("PRACTITIONER_INDEX_REVISION_SET_INCOMPLETE")
    for number in range(2, current_revision_number + 1):
        retention = revisions_by_number[number]["source_snapshot"].get("predecessor_retention")
        predecessor = revisions_by_number[number - 1]
        if (
            not isinstance(retention, Mapping)
            or retention.get("retained") is not True
            or retention.get("superseded_but_retained") is not True
            or retention.get("revision_id") != predecessor["object_id"]
            or retention.get("revision_sha256") != predecessor["sha256"]
        ):
            raise PractitionerContractError("PRACTITIONER_INDEX_REVISION_CHAIN_INVALID")

    core = {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_evidence_index.v1",
        "period_id": period.get("period_id"),
        "period_revision_id": period.get("revision_id"),
        "period_revision_sha256": sha256_bytes(canonical_bytes(period)),
        "population_identity": period.get("population_identity"),
        "access_posture": "READ_ONLY_CANONICAL_EVIDENCE",
        "canonical_evidence_write_permitted": False,
        "annotation_output_domain": "SEPARATE_PRACTITIONER_OUTPUT",
        "neutral_default_filter": {},
        "favorable_only_default": False,
        "filters_visible_and_resettable": True,
        "complete_population_access": True,
        "sampling_controlled_by_practitioner": True,
        "evidence_item_count": len(evidence_items),
        "evidence_type_counts": dict(sorted(type_counts.items())),
        "transaction_count": len(transaction_ids),
        "adverse_item_count": sum(row["adverse"] for row in evidence_items),
        "evidence_items": evidence_items,
        "evidence_item_set_identity": sha256_bytes(
            canonical_bytes(
                [
                    {
                        "object_id": row["object_id"],
                        "object_type": row["object_type"],
                        "sha256": row["sha256"],
                    }
                    for row in evidence_items
                ]
            )
        ),
        "raw_export_formats": ["CSV", "JSON", "JSONL"],
        "permitted_generated_outputs": [
            "EVIDENCE_INDEX",
            "SELECTED_ITEM_LIST",
            "PROCEDURE_WORKSHEET",
            "ANNOTATION_SUMMARY",
            "EXCEPTION_LISTING",
            "VERIFICATION_REPORT",
        ],
        "prohibited_generated_outputs": [
            "ASSURANCE_OPINION",
            "SOC_REPORT_CONCLUSION",
            "CERTIFICATION_DECISION",
            "REASONABLE_OR_LIMITED_ASSURANCE_STATEMENT",
            "EVIDENCE_SUFFICIENCY_CONCLUSION",
            "CONTROL_EFFECTIVENESS_CONCLUSION",
        ],
        **_no_opinion_fields(),
    }
    core["index_identity"] = sha256_bytes(canonical_bytes(core))
    return core


def export_practitioner_index(index: Mapping[str, Any], format_name: str) -> dict[str, Any]:
    """Export index rows with the nonassurance notice in every format."""

    source = copy.deepcopy(dict(_mapping(index, "PRACTITIONER_INDEX")))
    format_name = _text(format_name, "FORMAT").upper()
    if format_name == "JSON":
        payload = canonical_bytes(source)
        media_type = "application/json"
    elif format_name == "JSONL":
        records = []
        for item in source.get("evidence_items", []):
            row = dict(_mapping(item, "EVIDENCE_ITEM"))
            row["nonassurance"] = NONASSURANCE_NOTICE
            row["authority_effect"] = AUTHORITY_EFFECT
            records.append(canonical_bytes(row))
        payload = b"".join(records)
        media_type = "application/x-ndjson"
    elif format_name == "CSV":
        stream = io.StringIO(newline="")
        fields = (
            "object_type",
            "object_id",
            "sha256",
            "adverse",
            "read_only",
            "drill_through_json",
            "source_snapshot_json",
            "nonassurance",
        )
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for item in source.get("evidence_items", []):
            row = _mapping(item, "EVIDENCE_ITEM")
            writer.writerow(
                {
                    "object_type": row.get("object_type"),
                    "object_id": row.get("object_id"),
                    "sha256": row.get("sha256"),
                    "adverse": str(bool(row.get("adverse"))).lower(),
                    "read_only": "true",
                    "drill_through_json": canonical_bytes(
                        dict(_mapping(row.get("drill_through", {}), "DRILL_THROUGH"))
                    ).decode("utf-8").rstrip("\n"),
                    "source_snapshot_json": canonical_bytes(
                        dict(_mapping(row.get("source_snapshot", {}), "SOURCE_SNAPSHOT"))
                    ).decode("utf-8").rstrip("\n"),
                    "nonassurance": NONASSURANCE_NOTICE,
                }
            )
        payload = unicodedata.normalize("NFC", stream.getvalue()).encode("utf-8")
        media_type = "text/csv; charset=utf-8"
    else:
        raise PractitionerContractError("UNSUPPORTED_RAW_EXPORT_FORMAT")
    return {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_raw_export.v1",
        "index_identity": source.get("index_identity"),
        "format": format_name,
        "media_type": media_type,
        "payload": payload,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        **_no_opinion_fields(),
    }


def _evidence_refs(values: Sequence[Any]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for value in values:
        row = _mapping(value, "EVIDENCE_REFERENCE")
        object_id = _text(row.get("object_id"), "EVIDENCE_OBJECT_ID")
        digest = _text(row.get("sha256"), "EVIDENCE_SHA256")
        if not SHA256_RE.fullmatch(digest):
            raise PractitionerContractError("EVIDENCE_SHA256_INVALID")
        pair = (object_id, digest)
        if pair in seen:
            raise PractitionerContractError("DUPLICATE_EVIDENCE_REFERENCE")
        seen.add(pair)
        result.append({"object_id": object_id, "sha256": digest})
    if not result:
        raise PractitionerContractError("EVIDENCE_REFERENCE_REQUIRED")
    return sorted(result, key=lambda row: (row["object_id"], row["sha256"]))


def create_annotation(
    *,
    annotation_id: str,
    practitioner_actor_id: str,
    evidence_refs: Sequence[Any],
    content: str,
    created_at_utc: str,
    annotation_type: str = "NOTE",
    engagement_id: str | None = None,
    supersedes_annotation_id: str | None = None,
    signature_posture: str = "UNSIGNED",
) -> dict[str, Any]:
    """Create an exact supplied-v1 annotation; no source mutation API exists.

    The commission-supplied v1 schema is closed with
    ``additionalProperties: false``.  Consequently storage enforcement and the
    annotation digest remain outside this object rather than masquerading as
    schema-validated v1 fields.
    """

    annotation_type = _text(annotation_type, "ANNOTATION_TYPE").upper()
    if annotation_type not in ANNOTATION_TYPES:
        raise PractitionerContractError("ANNOTATION_TYPE_INVALID")
    if signature_posture not in {"UNSIGNED", "EXTERNAL_SIGNATURE"}:
        raise PractitionerContractError("SIGNATURE_POSTURE_INVALID")
    return {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_annotation.v1",
        "annotation_id": _text(annotation_id, "ANNOTATION_ID"),
        "practitioner_actor_id": _text(practitioner_actor_id, "PRACTITIONER_ACTOR_ID"),
        "engagement_id": _text(engagement_id, "ENGAGEMENT_ID") if engagement_id else None,
        "annotation_type": annotation_type,
        "evidence_refs": _evidence_refs(evidence_refs),
        "content": _text(content, "ANNOTATION_CONTENT"),
        "created_at_utc": _utc(created_at_utc, "CREATED_AT_UTC"),
        "supersedes_annotation_id": (
            _text(supersedes_annotation_id, "SUPERSEDES_ANNOTATION_ID")
            if supersedes_annotation_id
            else None
        ),
        "source_evidence_mutated": False,
        "signature_posture": signature_posture,
        "nonauthority": NONASSURANCE_NOTICE,
    }


def create_annotation_envelope(
    annotation: Mapping[str, Any],
    *,
    authentication_posture: str,
    time_posture: str,
) -> dict[str, Any]:
    """Bind v1 to platform-only custody fields under a distinct v2 schema.

    This wrapper resolves the supplied v1 schema's intentionally narrow shape:
    the v1 record remains byte-valid, while authentication, time, storage, and
    identity metadata live in an explicitly different object.
    """

    record = copy.deepcopy(dict(_mapping(annotation, "PRACTITIONER_ANNOTATION")))
    if (
        set(record) != ANNOTATION_V1_FIELDS
        or record.get("schema_id") != "uvlm.triadicbrain.aep01.practitioner_annotation.v1"
        or record.get("source_evidence_mutated") is not False
        or record.get("nonauthority") != NONASSURANCE_NOTICE
    ):
        raise PractitionerContractError("PRACTITIONER_ANNOTATION_V1_INVALID")
    core = {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_annotation_envelope.v2",
        "annotation": record,
        "annotation_sha256": sha256_bytes(canonical_bytes(record)),
        "authentication_posture": _text(authentication_posture, "AUTHENTICATION_POSTURE"),
        "time_posture": _text(time_posture, "TIME_POSTURE"),
        "storage_domain": "SEPARATE_PRACTITIONER_OUTPUT",
        "canonical_evidence_write_permitted": False,
        "source_evidence_mutated": False,
        **_no_opinion_fields(),
    }
    core["envelope_sha256"] = sha256_bytes(canonical_bytes(core))
    return core


def create_challenge(
    *,
    challenge_id: str,
    challenge_type: str,
    practitioner_actor_id: str,
    evidence_refs: Sequence[Any],
    rationale: str,
    created_at_utc: str,
    engagement_id: str | None = None,
    status: str = "OPEN",
    supersedes_challenge_id: str | None = None,
) -> dict[str, Any]:
    """Create a challenge linked to, but never written into, canonical evidence."""

    challenge_type = _text(challenge_type, "CHALLENGE_TYPE").upper()
    status = _text(status, "CHALLENGE_STATUS").upper()
    if challenge_type not in CHALLENGE_TYPES:
        raise PractitionerContractError("CHALLENGE_TYPE_INVALID")
    if status not in CHALLENGE_STATES:
        raise PractitionerContractError("CHALLENGE_STATUS_INVALID")
    if supersedes_challenge_id is None and status != "OPEN":
        raise PractitionerContractError("NEW_CHALLENGE_MUST_START_OPEN")
    core = {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_challenge.v1",
        "challenge_id": _text(challenge_id, "CHALLENGE_ID"),
        "challenge_type": challenge_type,
        "status": status,
        "practitioner_actor_id": _text(practitioner_actor_id, "PRACTITIONER_ACTOR_ID"),
        "engagement_id": _text(engagement_id, "ENGAGEMENT_ID") if engagement_id else None,
        "evidence_refs": _evidence_refs(evidence_refs),
        "rationale": _text(rationale, "CHALLENGE_RATIONALE"),
        "created_at_utc": _utc(created_at_utc, "CREATED_AT_UTC"),
        "supersedes_challenge_id": (
            _text(supersedes_challenge_id, "SUPERSEDES_CHALLENGE_ID")
            if supersedes_challenge_id
            else None
        ),
        "source_evidence_mutated": False,
        "storage_domain": "SEPARATE_PRACTITIONER_OUTPUT",
        **_no_opinion_fields(),
    }
    core["challenge_sha256"] = sha256_bytes(canonical_bytes(core))
    return core


def supersede_challenge(
    previous: Mapping[str, Any],
    *,
    challenge_id: str,
    status: str,
    practitioner_actor_id: str,
    rationale: str,
    created_at_utc: str,
) -> dict[str, Any]:
    """Return a new challenge state record while preserving predecessor identity."""

    predecessor = copy.deepcopy(dict(_mapping(previous, "PREVIOUS_CHALLENGE")))
    if predecessor.get("schema_id") != "uvlm.triadicbrain.aep01.practitioner_challenge.v1":
        raise PractitionerContractError("PREVIOUS_CHALLENGE_SCHEMA_INVALID")
    previous_id = _text(predecessor.get("challenge_id"), "PREVIOUS_CHALLENGE_ID")
    new_record = create_challenge(
        challenge_id=challenge_id,
        challenge_type=str(predecessor.get("challenge_type")),
        practitioner_actor_id=practitioner_actor_id,
        evidence_refs=predecessor.get("evidence_refs", []),
        rationale=rationale,
        created_at_utc=created_at_utc,
        engagement_id=predecessor.get("engagement_id"),
        status=status,
        supersedes_challenge_id=previous_id,
    )
    new_record["predecessor_challenge_sha256"] = sha256_bytes(canonical_bytes(predecessor))
    # Rebind after adding the retained predecessor identity.
    new_record.pop("challenge_sha256", None)
    new_record["challenge_sha256"] = sha256_bytes(canonical_bytes(new_record))
    return new_record


def verify_practitioner_index(index: Mapping[str, Any]) -> dict[str, Any]:
    """Authenticate index identity, counts, population, and exact item set."""

    source = copy.deepcopy(dict(_mapping(index, "PRACTITIONER_INDEX")))
    mismatches: list[str] = []
    seen: set[tuple[str, str]] = set()
    items_value = source.get("evidence_items")
    if not isinstance(items_value, list):
        items_value = []
        mismatches.append("EVIDENCE_ITEMS_NOT_ARRAY")
    items: list[Mapping[str, Any]] = []
    allowed_types = {
        "TRANSACTION",
        "CONTROL_EXECUTION",
        "FINDING_EXCEPTION",
        "EVIDENCE_PACKAGE",
        "VERIFICATION",
        "PERIOD_REVISION",
        "OTHER_EVIDENCE",
    }
    expected_item_fields = {
        "object_type",
        "object_id",
        "sha256",
        "read_only",
        "drill_through",
        "adverse",
        "source_snapshot",
    }
    for value in items_value:
        if not isinstance(value, Mapping):
            mismatches.append("EVIDENCE_ITEM_NOT_OBJECT")
            continue
        item = value
        items.append(item)
        if set(item) != expected_item_fields:
            mismatches.append("EVIDENCE_ITEM_FIELDS")
        key = (str(item.get("object_type")), str(item.get("object_id")))
        if key in seen:
            mismatches.append(f"DUPLICATE:{key[0]}:{key[1]}")
        seen.add(key)
        snapshot = item.get("source_snapshot")
        if key[0] not in allowed_types:
            mismatches.append(f"OBJECT_TYPE:{key[0]}:{key[1]}")
        if not isinstance(snapshot, Mapping) or item.get("sha256") != sha256_bytes(canonical_bytes(dict(snapshot))):
            mismatches.append(f"DIGEST:{key[0]}:{key[1]}")
        elif key[0] in allowed_types:
            try:
                if item.get("object_id") != _object_id(snapshot, key[0]):
                    mismatches.append(f"OBJECT_ID:{key[0]}:{key[1]}")
            except PractitionerContractError:
                mismatches.append(f"OBJECT_ID:{key[0]}:{key[1]}")
            expected_drill_through = {
                "transaction_id": snapshot.get("transaction_id"),
                "source_row_ids": snapshot.get("source_row_ids", []),
            }
            if item.get("drill_through") != expected_drill_through:
                mismatches.append(f"DRILL_THROUGH:{key[0]}:{key[1]}")
            expected_adverse = bool(
                snapshot.get("adverse") is True
                or snapshot.get("result") in {"FAIL", "HOLD", "NOT_EXECUTED", "ERROR"}
                or snapshot.get("status") in {"OPEN", "FAIL", "HOLD", "ERROR"}
            )
            if item.get("adverse") is not expected_adverse:
                mismatches.append(f"ADVERSE:{key[0]}:{key[1]}")
        if item.get("read_only") is not True:
            mismatches.append(f"WRITE_POSTURE:{key[0]}:{key[1]}")

    item_keys = [(str(item.get("object_type")), str(item.get("object_id"))) for item in items]
    if item_keys != sorted(item_keys):
        mismatches.append("EVIDENCE_ITEMS_NOT_CANONICALLY_SORTED")
    type_counts = Counter(str(item.get("object_type")) for item in items)
    expected_manifest = [
        {
            "object_id": item.get("object_id"),
            "object_type": item.get("object_type"),
            "sha256": item.get("sha256"),
        }
        for item in items
    ]
    if source.get("evidence_item_set_identity") != sha256_bytes(
        canonical_bytes(expected_manifest)
    ):
        mismatches.append("EVIDENCE_ITEM_SET_IDENTITY")
    if source.get("evidence_item_count") != len(items):
        mismatches.append("EVIDENCE_ITEM_COUNT")
    if source.get("evidence_type_counts") != dict(sorted(type_counts.items())):
        mismatches.append("EVIDENCE_TYPE_COUNTS")
    if source.get("adverse_item_count") != sum(item.get("adverse") is True for item in items):
        mismatches.append("ADVERSE_ITEM_COUNT")

    transaction_items = [item for item in items if item.get("object_type") == "TRANSACTION"]
    transaction_ids = {str(item.get("object_id")) for item in transaction_items}
    if source.get("transaction_count") != len(transaction_ids):
        mismatches.append("TRANSACTION_COUNT")
    try:
        from .period import population_document

        population = population_document(
            [dict(item["source_snapshot"]) for item in transaction_items]
        )
        if source.get("population_identity") != population.get("population_identity"):
            mismatches.append("POPULATION_IDENTITY")
        if source.get("period_id") != population.get("period_id"):
            mismatches.append("POPULATION_PERIOD_ID")
    except (KeyError, PractitionerContractError, ValueError, TypeError):
        mismatches.append("POPULATION_RECONSTRUCTION")

    revision_items = [item for item in items if item.get("object_type") == "PERIOD_REVISION"]
    current_revision_items = [
        item for item in revision_items if item.get("object_id") == source.get("period_revision_id")
    ]
    if len(current_revision_items) != 1:
        mismatches.append("CURRENT_PERIOD_REVISION_ITEM")
    else:
        revision = current_revision_items[0]
        if source.get("period_revision_sha256") != revision.get("sha256"):
            mismatches.append("PERIOD_REVISION_SHA256")
        snapshot = revision.get("source_snapshot")
        if isinstance(snapshot, Mapping):
            if snapshot.get("period_id") != source.get("period_id"):
                mismatches.append("PERIOD_REVISION_PERIOD_ID")
            if snapshot.get("population_identity") != source.get("population_identity"):
                mismatches.append("PERIOD_REVISION_POPULATION_IDENTITY")
            counts = snapshot.get("population_counts")
            if not isinstance(counts, Mapping) or counts.get("created") != len(transaction_items):
                mismatches.append("PERIOD_REVISION_POPULATION_COUNT")
            declared_population = snapshot.get("population_row_digests")
            observed_population = {
                str(entry.get("row_id")): entry.get("sha256")
                for entry in declared_population
                if isinstance(entry, Mapping)
            } if isinstance(declared_population, list) else {}
            actual_population = {
                str(item.get("source_snapshot", {}).get("population_row_id")): item.get("sha256")
                for item in transaction_items
            }
            if observed_population != actual_population:
                mismatches.append("POPULATION_ITEM_SET")
            declared_evidence = snapshot.get("evidence_row_digests")
            observed_evidence = {
                str(entry.get("row_id")): entry.get("sha256")
                for entry in declared_evidence
                if isinstance(entry, Mapping)
            } if isinstance(declared_evidence, list) else {}
            actual_evidence = {
                str(item.get("object_id")): item.get("sha256")
                for item in items
                if item.get("object_type")
                in {
                    "CONTROL_EXECUTION",
                    "FINDING_EXCEPTION",
                    "EVIDENCE_PACKAGE",
                    "VERIFICATION",
                    "OTHER_EVIDENCE",
                }
            }
            if observed_evidence != actual_evidence:
                mismatches.append("EVIDENCE_ITEM_SET")
    revision_by_number: dict[int, Mapping[str, Any]] = {}
    current_revision_number: int | None = None
    if len(current_revision_items) == 1 and isinstance(
        current_revision_items[0].get("source_snapshot"), Mapping
    ):
        number = current_revision_items[0]["source_snapshot"].get("revision_number")
        if type(number) is int and number >= 1:
            current_revision_number = number
    for item in revision_items:
        snapshot = item.get("source_snapshot")
        if not isinstance(snapshot, Mapping):
            mismatches.append("PERIOD_REVISION_SNAPSHOT")
            continue
        number = snapshot.get("revision_number")
        without_identity = copy.deepcopy(dict(snapshot))
        identity = without_identity.pop("revision_identity", None)
        if identity != sha256_bytes(canonical_bytes(without_identity)):
            mismatches.append("PERIOD_REVISION_IDENTITY")
        if (
            type(number) is not int
            or number < 1
            or number in revision_by_number
            or snapshot.get("period_id") != source.get("period_id")
            or snapshot.get("revision_id") != f"{source.get('period_id')}-R{number:04d}"
        ):
            mismatches.append("PERIOD_REVISION_SET")
            continue
        revision_by_number[number] = item
    if current_revision_number is None or set(revision_by_number) != set(
        range(1, current_revision_number + 1)
    ):
        mismatches.append("PERIOD_REVISION_SET_INCOMPLETE")
    elif current_revision_number > 1:
        for number in range(2, current_revision_number + 1):
            retention = revision_by_number[number]["source_snapshot"].get(
                "predecessor_retention"
            )
            predecessor = revision_by_number[number - 1]
            if (
                not isinstance(retention, Mapping)
                or retention.get("retained") is not True
                or retention.get("superseded_but_retained") is not True
                or retention.get("revision_id") != predecessor.get("object_id")
                or retention.get("revision_sha256") != predecessor.get("sha256")
            ):
                mismatches.append("PERIOD_REVISION_CHAIN")

    without_identity = copy.deepcopy(source)
    observed_index_identity = without_identity.pop("index_identity", None)
    if observed_index_identity != sha256_bytes(canonical_bytes(without_identity)):
        mismatches.append("INDEX_IDENTITY")
    if source.get("schema_id") != "uvlm.triadicbrain.aep01.practitioner_evidence_index.v1":
        mismatches.append("INDEX_SCHEMA")
    if source.get("canonical_evidence_write_permitted") is not False:
        mismatches.append("CANONICAL_WRITE_PERMITTED")
    if source.get("opinion_generated_or_prefilled") is not False:
        mismatches.append("OPINION_GENERATED_OR_PREFILLED")
    if source.get("complete_population_access") is not True:
        mismatches.append("COMPLETE_POPULATION_ACCESS")
    if source.get("favorable_only_default") is not False or source.get("neutral_default_filter") != {}:
        mismatches.append("FILTER_POSTURE")
    if source.get("access_posture") != "READ_ONLY_CANONICAL_EVIDENCE":
        mismatches.append("ACCESS_POSTURE")
    if source.get("contains_assurance_conclusion") is not False:
        mismatches.append("ASSURANCE_CONCLUSION")
    if source.get("authority_effect") != AUTHORITY_EFFECT:
        mismatches.append("AUTHORITY_EFFECT")
    return {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_index_verification.v1",
        "status": "PASS" if not mismatches else "HOLD",
        "index_identity": source.get("index_identity"),
        "verified_item_count": len(seen),
        "mismatches": sorted(set(mismatches)),
        "source_evidence_mutated": False,
        **_no_opinion_fields(),
    }
