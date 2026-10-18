"""Complete-population reporting and immutable period revision primitives.

Population authority comes from transaction creation custody events.  Sealed
packages are evidence about a transaction, never the population source.  This
module deliberately keeps failed, refused, interrupted, and incomplete rows in
the same export as successful rows.
"""

from __future__ import annotations

import copy
import csv
import io
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from typing import Any

from .canonical import canonical_bytes, sha256_bytes


NONASSURANCE_NOTICE = "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED."
AUTHORITY_EFFECT = "NONE"
INCLUSION_POLICY_VERSION = "1.0.0"
PERIOD_CONTROL_SUMMARY_V1_SCHEMA_ID = (
    "uvlm.triadicbrain.aep01.period_control_summary.v1"
)
PERIOD_REVISION_ENVELOPE_SCHEMA_ID = (
    "uvlm.triadicbrain.aep01.period_revision_envelope.v2"
)
PERIOD_REVISION_ENVELOPE_FIELDS = {
    "schema_id",
    "period_id",
    "revision_id",
    "revision_number",
    "parent_revision_id",
    "created_at_utc",
    "start_utc",
    "end_utc",
    "inclusion_policy_version",
    "creation_reason",
    "changed_population_ids",
    "changed_evidence_ids",
    "changed_metric_ids",
    "population_identity",
    "metric_population_sha256",
    "population_row_digests",
    "evidence_row_digests",
    "metric_row_digests",
    "metric_change_digests",
    "population_counts",
    "control_results",
    "open_exception_count",
    "metrics",
    "before_metric_digest",
    "after_metric_digest",
    "reconciliation",
    "preparer_posture",
    "management_representation_status",
    "predecessor_retention",
    "assurance_status",
    "nonassurance",
    "contains_assurance_conclusion",
    "opinion_generated_or_prefilled",
    "authority_effect",
    "period_control_summary_v1",
    "revision_identity",
}

CREATION_OPERATIONS = {
    "CREATE_TRANSACTION",
    "TRANSACTION_CREATED",
    "TRANSACTION_REGISTERED",
    "CREATE_REPAIR_CHILD",
    "REPAIR_CHILD_CREATED",
    "CREATED",
}
DECISIONS = {"APPROVE", "HOLD", "REJECT", "REQUEST_REPAIR", "PENDING"}
CONTROL_RESULTS = ("PASS", "FAIL", "HOLD", "NOT_EXECUTED", "ERROR")
FINDING_OPEN_STATES = {"OPEN", "UNRESOLVED", "PENDING", "MANAGEMENT_RESPONSE_PROVIDED"}
ADVERSE_STATES = {
    "ABORTED",
    "ERROR",
    "FAILED",
    "FINALIZATION_FAILED",
    "HELD",
    "HOLD",
    "INTERRUPTED",
    "INCOMPLETE_REGISTRATION",
    "CANDIDATE_FAILED",
    "CONTROLS_INCOMPLETE",
    "SOPHIA_FAILED",
    "ATLAS_FAILED",
    "PROVIDER_UNAVAILABLE",
    "REFUSED",
    "REJECT",
    "REJECTED",
}
TERMINAL_STATES = {
    "ABORTED",
    "FAILED",
    "FINALIZATION_FAILED",
    "SEALED",
}

POPULATION_COLUMNS = (
    "population_row_id",
    "period_id",
    "transaction_id",
    "creation_ledger_event_id",
    "created_at_utc",
    "lineage_role",
    "parent_transaction_id",
    "admission_status",
    "transaction_state",
    "business_state",
    "human_decision",
    "decision_recorded",
    "terminal",
    "nonterminal",
    "finalization_complete",
    "incomplete",
    "adverse",
    "sealed",
    "package_finalized",
    "package_id",
    "package_sha256",
    "open_advisory_finding_ids",
    "binding_finding_ids",
    "selected_repair_finding_ids",
    "exclusion_status",
    "exclusion_reason",
    "source_row_ids",
    "contains_assurance_conclusion",
    "nonassurance",
    "authority_effect",
)


class PeriodContractError(ValueError):
    """A period object could not be produced without weakening its contract."""


def _as_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        result = to_dict()
        if isinstance(result, Mapping):
            return result
    raise PeriodContractError(f"{label}_MUST_BE_OBJECT")


def _text(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise PeriodContractError(f"{label}_MUST_BE_TEXT")
    normalized = unicodedata.normalize("NFC", value)
    if not allow_empty and not normalized:
        raise PeriodContractError(f"{label}_MUST_NOT_BE_EMPTY")
    return normalized


def _utc(value: Any, label: str) -> str:
    text = _text(value, label)
    if not text.endswith("Z"):
        raise PeriodContractError(f"{label}_MUST_BE_UTC_Z")
    try:
        datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError as exc:
        raise PeriodContractError(f"{label}_INVALID") from exc
    return text


def _first(row: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


def _nested_first(row: Mapping[str, Any], container: str, *names: str) -> Any:
    nested = row.get(container)
    if isinstance(nested, Mapping):
        return _first(nested, *names)
    return None


def _string_list(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, Sequence):
        raise PeriodContractError(f"{label}_MUST_BE_ARRAY")
    result = [_text(item, label) for item in value]
    if len(result) != len(set(result)):
        raise PeriodContractError(f"{label}_HAS_DUPLICATES")
    return sorted(result)


def _index_records(records: Mapping[str, Any] | Sequence[Any]) -> dict[str, Mapping[str, Any]]:
    if isinstance(records, Mapping):
        indexed: dict[str, Mapping[str, Any]] = {}
        for key, value in records.items():
            row = _as_mapping(value, "TRANSACTION_RECORD")
            transaction_id = _text(_first(row, "transaction_id", default=key), "TRANSACTION_ID")
            if transaction_id in indexed:
                raise PeriodContractError("DUPLICATE_TRANSACTION_RECORD")
            indexed[transaction_id] = row
        return indexed
    indexed = {}
    for value in records:
        row = _as_mapping(value, "TRANSACTION_RECORD")
        transaction_id = _text(row.get("transaction_id"), "TRANSACTION_ID")
        if transaction_id in indexed:
            raise PeriodContractError("DUPLICATE_TRANSACTION_RECORD")
        indexed[transaction_id] = row
    return indexed


def _index_transaction_rows(
    values: Mapping[str, Any] | Sequence[Any], label: str
) -> dict[str, Mapping[str, Any]]:
    if isinstance(values, Mapping):
        items = values.items()
    else:
        items = ((None, value) for value in values)
    result: dict[str, Mapping[str, Any]] = {}
    for key, value in items:
        row = _as_mapping(value, label)
        transaction_id = _text(
            _first(row, "transaction_id", default=key), f"{label}_TRANSACTION_ID"
        )
        if transaction_id in result:
            raise PeriodContractError(f"DUPLICATE_{label}")
        result[transaction_id] = row
    return result


def _finding_index(findings: Sequence[Any]) -> dict[str, dict[str, list[str]]]:
    indexed: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"advisory": [], "binding": [], "open": []}
    )
    seen: set[str] = set()
    for value in findings:
        row = _as_mapping(value, "FINDING")
        finding_id = _text(_first(row, "finding_id", "row_id"), "FINDING_ID")
        if finding_id in seen:
            raise PeriodContractError("DUPLICATE_FINDING_ID")
        seen.add(finding_id)
        transaction_id = _text(row.get("transaction_id"), "FINDING_TRANSACTION_ID")
        kind = str(_first(row, "finding_type", "finding_class", "type", default="")).upper()
        status = str(_first(row, "status", default="OPEN")).upper()
        if kind == "ADVISORY_FINDING" and status in FINDING_OPEN_STATES:
            indexed[transaction_id]["advisory"].append(finding_id)
        if kind == "BINDING_FINDING" and status in FINDING_OPEN_STATES:
            indexed[transaction_id]["binding"].append(finding_id)
        if status in FINDING_OPEN_STATES:
            indexed[transaction_id]["open"].append(finding_id)
    for groups in indexed.values():
        for values in groups.values():
            values.sort()
    return dict(indexed)


def _exclusion_index(exclusions: Sequence[Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for value in exclusions:
        row = _as_mapping(value, "EXCLUSION")
        transaction_id = _text(row.get("transaction_id"), "EXCLUSION_TRANSACTION_ID")
        if transaction_id in result:
            raise PeriodContractError("DUPLICATE_EXCLUSION")
        if row.get("authorized") is not True or not isinstance(row.get("reason"), str) or not row["reason"]:
            raise PeriodContractError("EXCLUSION_REQUIRES_REASON_AND_AUTHORIZATION")
        result[transaction_id] = row
    return result


def build_population_rows(
    creation_ledger_rows: Sequence[Any],
    *,
    transaction_records: Mapping[str, Any] | Sequence[Any] = (),
    decision_rows: Mapping[str, Any] | Sequence[Any] = (),
    package_manifests: Mapping[str, Any] | Sequence[Any] = (),
    finding_rows: Sequence[Any] = (),
    exclusion_rows: Sequence[Any] = (),
) -> list[dict[str, Any]]:
    """Build exactly one complete-population row per creation-ledger event.

    Transaction records, findings, packages, and decisions only enrich the
    creation population.  None of those downstream sources can create or erase
    a population member.
    """

    records = _index_records(transaction_records)
    decisions = _index_transaction_rows(decision_rows, "DECISION_ROW")
    packages = _index_transaction_rows(package_manifests, "PACKAGE_MANIFEST")
    findings = _finding_index(finding_rows)
    exclusions = _exclusion_index(exclusion_rows)
    rows: list[dict[str, Any]] = []
    seen_transactions: set[str] = set()
    seen_events: set[str] = set()

    for ordinal, value in enumerate(creation_ledger_rows, 1):
        event = _as_mapping(value, "CREATION_LEDGER_ROW")
        operation = str(_first(event, "operation", "event_type", default="TRANSACTION_CREATED")).upper()
        if operation not in CREATION_OPERATIONS:
            raise PeriodContractError("NON_CREATION_EVENT_IN_CREATION_LEDGER_ROWS")
        transaction_id = _text(event.get("transaction_id"), "TRANSACTION_ID")
        event_id = _text(
            _first(event, "event_sha256", "creation_event_id", "ledger_event_id", "event_id"),
            "CREATION_LEDGER_EVENT_ID",
        )
        if transaction_id in seen_transactions:
            raise PeriodContractError("DUPLICATE_TRANSACTION_CREATION")
        if event_id in seen_events:
            raise PeriodContractError("DUPLICATE_CREATION_EVENT")
        seen_transactions.add(transaction_id)
        seen_events.add(event_id)

        record = records.get(transaction_id, {})
        lineage = record.get("lineage") if isinstance(record.get("lineage"), Mapping) else {}
        parent_id = _first(record, "parent_transaction_id") or _first(lineage, "parent_transaction_id")
        if parent_id is None:
            parent_id = _first(event, "parent_transaction_id") or _nested_first(
                event, "lineage", "parent_transaction_id"
            )
        if parent_id is not None:
            parent_id = _text(parent_id, "PARENT_TRANSACTION_ID")

        supplied_decision = decisions.get(transaction_id, {})
        supplied_package = packages.get(transaction_id, {})
        decision_value = _first(
            supplied_decision,
            "decision",
            default=_first(record, "human_decision", "decision", default="PENDING"),
        )
        decision_record: Mapping[str, Any] = supplied_decision
        if isinstance(decision_value, Mapping):
            decision_record = decision_value
            decision_value = _first(decision_value, "decision", "value", default="PENDING")
        decision = str(decision_value).upper()
        if decision not in DECISIONS:
            decision = "PENDING"

        state = str(
            _first(record, "transaction_state", "final_state", "state", "status", default="CREATED_ONLY")
        ).upper()
        business_state = str(
            _first(record, "business_state", default=_first(supplied_package, "state", default=decision))
        ).upper()
        if decision == "PENDING" and business_state in DECISIONS - {"PENDING"}:
            decision = business_state
        if decision == "PENDING":
            decision = {
                "APPROVED": "APPROVE",
                "APPROVED_WITHIN_DECLARED_SCOPE": "APPROVE",
                "HELD": "HOLD",
                "HOLD": "HOLD",
                "REJECTED": "REJECT",
                "REJECT": "REJECT",
                "REPAIR_REQUESTED": "REQUEST_REPAIR",
                "REPAIR_CHILD_CREATED": "REQUEST_REPAIR",
            }.get(state, "PENDING")
        if business_state == "PENDING" and decision != "PENDING":
            business_state = decision
        if business_state == "PENDING" and state == "REFUSED":
            business_state = "REFUSED"
        admission = str(_first(record, "admission_status", default="PENDING")).upper()
        if state == "REFUSED" or business_state == "REFUSED":
            admission = "REFUSED"
        elif admission == "PENDING" and record and state not in {"CREATED_ONLY", "INCOMPLETE_REGISTRATION", "ADMISSION_PENDING"}:
            admission = "ADMITTED"

        embedded_package = record.get("package") if isinstance(record.get("package"), Mapping) else {}
        package = supplied_package or embedded_package
        package_id = _first(record, "package_id") or _first(package, "package_id")
        package_sha256 = _first(record, "package_sha256") or _first(
            package, "package_sha256", "package_root_sha256", "package_root_digest"
        )
        package_finalized = bool(
            package_id is not None and _first(package, "finalized", default=False)
        )
        sealed = bool(
            _first(record, "sealed", "package_sealed", default=False)
            or state == "SEALED"
        )
        terminal_value = _first(record, "terminal")
        terminal = (
            bool(terminal_value)
            if isinstance(terminal_value, bool)
            else state in TERMINAL_STATES
        )
        finalization_complete = sealed
        incomplete = not finalization_complete

        indexed_findings = findings.get(transaction_id, {"advisory": [], "binding": [], "open": []})
        advisory_ids = _string_list(
            _first(record, "open_advisory_finding_ids", default=indexed_findings["advisory"]),
            "OPEN_ADVISORY_FINDING_IDS",
        )
        binding_ids = _string_list(
            _first(record, "binding_finding_ids", default=indexed_findings["binding"]),
            "BINDING_FINDING_IDS",
        )
        selected_ids = _string_list(
            _first(
                record,
                "selected_repair_finding_ids",
                "selected_finding_ids",
                default=_first(decision_record, "selected_finding_ids", default=[]),
            ),
            "SELECTED_REPAIR_FINDING_IDS",
        )
        adverse = bool(
            _first(record, "adverse", default=False)
            or state in ADVERSE_STATES
            or business_state in {"HOLD", "REJECT", "REFUSED"}
            or admission == "REFUSED"
            or binding_ids
            or advisory_ids
        )
        exclusion = exclusions.get(transaction_id)
        created_at = _first(
            event,
            "logical_time",
            "logical_time_utc",
            "created_at_utc",
            "observed_time_utc",
        )
        if created_at is not None:
            created_at = _utc(created_at, "CREATED_AT_UTC")
        source_ids = [event_id]
        record_id = _first(record, "transaction_record_id", "record_id", "row_id")
        if isinstance(record_id, str) and record_id:
            source_ids.append(record_id)
        decision_id = decision_record.get("decision_id")
        if isinstance(decision_id, str) and decision_id:
            source_ids.append(decision_id)
        if isinstance(package_id, str) and package_id:
            source_ids.append(package_id)

        row_seed = {
            "transaction_id": transaction_id,
            "creation_ledger_event_id": event_id,
            "inclusion_policy_version": INCLUSION_POLICY_VERSION,
        }
        rows.append(
            {
                "schema_id": "uvlm.triadicbrain.aep01.transaction_population_row.v1",
                "population_row_id": "POP-" + sha256_bytes(canonical_bytes(row_seed))[:24],
                "period_id": _first(record, "period_id", default=_first(event, "period_id")),
                "transaction_id": transaction_id,
                "creation_ledger_event_id": event_id,
                "created_at_utc": created_at,
                "lineage_role": "REPAIR_CHILD" if parent_id else "PARENT",
                "parent_transaction_id": parent_id,
                "admission_status": admission,
                "transaction_state": state,
                "business_state": business_state,
                "human_decision": decision,
                "decision_recorded": decision != "PENDING",
                "terminal": terminal,
                "nonterminal": not terminal,
                "finalization_complete": finalization_complete,
                "incomplete": incomplete,
                "adverse": adverse,
                "sealed": sealed,
                "package_finalized": package_finalized,
                "package_id": package_id,
                "package_sha256": package_sha256,
                "open_advisory_finding_ids": advisory_ids,
                "binding_finding_ids": binding_ids,
                "selected_repair_finding_ids": selected_ids,
                "exclusion_status": "AUTHORIZED_DISCLOSED" if exclusion else "NOT_EXCLUDED",
                "exclusion_reason": exclusion.get("reason") if exclusion else None,
                "source_row_ids": sorted(source_ids),
                "source_ordinal": ordinal,
                "nonassurance": NONASSURANCE_NOTICE,
                "contains_assurance_conclusion": False,
                "authority_effect": AUTHORITY_EFFECT,
            }
        )

    # A repair child is a real transaction and its parent must be in the same
    # complete population (or reconciliation must later hold).
    return sorted(rows, key=lambda row: (row["transaction_id"], row["population_row_id"]))


def _ids(values: Iterable[Any], label: str) -> set[str]:
    result: set[str] = set()
    for value in values:
        if isinstance(value, str):
            transaction_id = _text(value, label)
        else:
            row = _as_mapping(value, label)
            transaction_id = _text(row.get("transaction_id"), label)
        if transaction_id in result:
            raise PeriodContractError(f"DUPLICATE_{label}")
        result.add(transaction_id)
    return result


def reconcile_population(
    creation_ledger_rows: Sequence[Any],
    population_rows: Sequence[Any],
    *,
    transaction_records: Mapping[str, Any] | Sequence[Any] | None = None,
    transaction_root_ids: Sequence[Any] | None = None,
    sealed_package_manifests: Sequence[Any] | None = None,
) -> dict[str, Any]:
    """Compare independent population surfaces and HOLD on every difference."""

    ledger_ids = _ids(creation_ledger_rows, "LEDGER_TRANSACTION_ID")
    rows = [_as_mapping(value, "POPULATION_ROW") for value in population_rows]
    report_ids = _ids(rows, "REPORT_TRANSACTION_ID")
    differences: list[dict[str, str]] = []

    def add_set_difference(source: str, expected: set[str], observed: set[str]) -> None:
        for transaction_id in sorted(expected - observed):
            differences.append(
                {"transaction_id": transaction_id, "source": source, "reason": "EXPECTED_ID_MISSING"}
            )
        for transaction_id in sorted(observed - expected):
            differences.append(
                {"transaction_id": transaction_id, "source": source, "reason": "UNEXPECTED_ID_PRESENT"}
            )

    add_set_difference("REPORT_POPULATION", ledger_ids, report_ids)

    record_ids: set[str] | None = None
    if transaction_records is not None:
        record_ids = set(_index_records(transaction_records))
        for transaction_id in sorted(record_ids - ledger_ids):
            differences.append(
                {
                    "transaction_id": transaction_id,
                    "source": "TRANSACTION_RECORDS",
                    "reason": "RECORD_WITHOUT_CREATION_EVENT",
                }
            )

    root_ids: set[str] | None = None
    if transaction_root_ids is not None:
        root_ids = _ids(transaction_root_ids, "TRANSACTION_ROOT_ID")
        add_set_difference("TRANSACTION_ROOTS", ledger_ids, root_ids)

    package_ids: set[str] | None = None
    if sealed_package_manifests is not None:
        package_ids = _ids(sealed_package_manifests, "SEALED_PACKAGE_TRANSACTION_ID")
        for transaction_id in sorted(package_ids - ledger_ids):
            differences.append(
                {
                    "transaction_id": transaction_id,
                    "source": "SEALED_PACKAGES",
                    "reason": "PACKAGE_WITHOUT_CREATION_EVENT",
                }
            )
        sealed_rows = {str(row["transaction_id"]) for row in rows if row.get("sealed") is True}
        add_set_difference("SEALED_PACKAGE_STATE", sealed_rows, package_ids)

    for row in rows:
        parent_id = row.get("parent_transaction_id")
        if parent_id is not None and parent_id not in ledger_ids:
            differences.append(
                {
                    "transaction_id": str(row["transaction_id"]),
                    "source": "REPAIR_LINEAGE",
                    "reason": "PARENT_TRANSACTION_NOT_IN_POPULATION",
                }
            )

    for difference in differences:
        difference["difference_id"] = "DIFF-" + sha256_bytes(
            canonical_bytes(difference)
        )[:24]
    unexplained_ids = sorted({row["transaction_id"] for row in differences})
    admission_counts = Counter(str(row.get("admission_status", "UNKNOWN")) for row in rows)
    final_state_counts = Counter(str(row.get("transaction_state", "UNKNOWN")) for row in rows)
    exclusion_rows = [
        {
            "reason": row.get("exclusion_reason"),
            "status": row.get("exclusion_status"),
            "transaction_id": row.get("transaction_id"),
        }
        for row in rows
        if row.get("exclusion_status") != "NOT_EXCLUDED"
    ]
    return {
        "schema_id": "uvlm.triadicbrain.aep01.population_reconciliation.v1",
        "status": "PASS" if not differences else "HOLD",
        "inclusion_source": "TRANSACTION_CREATION_LEDGER",
        "inclusion_policy_version": INCLUSION_POLICY_VERSION,
        "ledger_created_count": len(ledger_ids),
        "report_population_count": len(report_ids),
        "transaction_record_count": len(record_ids) if record_ids is not None else None,
        "transaction_root_count": len(root_ids) if root_ids is not None else None,
        "sealed_package_count": len(package_ids) if package_ids is not None else None,
        "admission_state_distribution": dict(sorted(admission_counts.items())),
        "final_state_distribution": dict(sorted(final_state_counts.items())),
        "exclusions": exclusion_rows,
        "exclusion_count": len(exclusion_rows),
        "unexplained_difference_count": len(unexplained_ids),
        "unexplained_transaction_ids": unexplained_ids,
        "differences": differences,
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "authority_effect": AUTHORITY_EFFECT,
    }


def population_document(rows: Sequence[Any]) -> dict[str, Any]:
    normalized = [copy.deepcopy(dict(_as_mapping(row, "POPULATION_ROW"))) for row in rows]
    normalized.sort(key=lambda row: (str(row.get("transaction_id")), str(row.get("population_row_id"))))
    period_ids = {
        row.get("period_id")
        for row in normalized
        if isinstance(row.get("period_id"), str) and row.get("period_id")
    }
    unknown_period_count = sum(not row.get("period_id") for row in normalized)
    period_scope = (
        "EMPTY_POPULATION"
        if not normalized
        else "SINGLE_PERIOD"
        if len(period_ids) == 1 and unknown_period_count == 0
        else "SINGLE_PERIOD_WITH_UNKNOWN_ROWS"
        if len(period_ids) == 1
        else "MULTI_PERIOD_OR_UNRESOLVED_SCOPE"
    )
    role_counts = Counter(str(row.get("lineage_role")) for row in normalized)
    document = {
        "schema_id": "uvlm.triadicbrain.aep01.transaction_population.v1",
        "period_id": next(iter(period_ids)) if len(period_ids) == 1 else None,
        "period_ids": sorted(period_ids),
        "period_scope": period_scope,
        "unknown_period_row_count": unknown_period_count,
        "inclusion_source": "TRANSACTION_CREATION_LEDGER",
        "inclusion_policy_version": INCLUSION_POLICY_VERSION,
        "population_count": len(normalized),
        "parent_transaction_count": role_counts["PARENT"],
        "repair_child_count": role_counts["REPAIR_CHILD"],
        "rows": normalized,
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "authority_effect": AUTHORITY_EFFECT,
    }
    document["population_identity"] = sha256_bytes(canonical_bytes(document))
    return document


def population_json_bytes(rows: Sequence[Any]) -> bytes:
    return canonical_bytes(population_document(rows))


def _csv_value(value: Any) -> str:
    if value is None:
        return ""
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (list, dict)):
        return canonical_bytes(value).decode("utf-8").rstrip("\n")
    return unicodedata.normalize("NFC", str(value))


def population_csv_bytes(rows: Sequence[Any]) -> bytes:
    normalized = [dict(_as_mapping(row, "POPULATION_ROW")) for row in rows]
    normalized.sort(key=lambda row: (str(row.get("transaction_id")), str(row.get("population_row_id"))))
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(POPULATION_COLUMNS), extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in normalized:
        writer.writerow({column: _csv_value(row.get(column)) for column in POPULATION_COLUMNS})
    return unicodedata.normalize("NFC", stream.getvalue()).encode("utf-8")


def export_population(rows: Sequence[Any]) -> dict[str, Any]:
    json_payload = population_json_bytes(rows)
    csv_payload = population_csv_bytes(rows)
    return {
        "document": population_document(rows),
        "json_bytes": json_payload,
        "json_sha256": sha256_bytes(json_payload),
        "csv_bytes": csv_payload,
        "csv_sha256": sha256_bytes(csv_payload),
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "authority_effect": AUTHORITY_EFFECT,
    }


def _nonnegative_int(value: Any, label: str) -> int:
    if type(value) is not int or value < 0:
        raise PeriodContractError(f"{label}_MUST_BE_NONNEGATIVE_INTEGER")
    return value


def _sha256_text(value: Any, label: str) -> str:
    text = _text(value, label)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise PeriodContractError(f"{label}_INVALID")
    return text


def _row_digest_entries(
    rows: Sequence[Mapping[str, Any]],
    *,
    label: str,
    id_fields: Sequence[str],
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        row_id: str | None = None
        for field in id_fields:
            value = row.get(field)
            if isinstance(value, str) and value:
                row_id = _text(value, f"{label}_ROW_ID")
                break
        if row_id is None:
            raise PeriodContractError(f"{label}_ROW_ID_MISSING")
        if row_id in seen:
            raise PeriodContractError(f"DUPLICATE_{label}_ROW_ID")
        seen.add(row_id)
        entries.append({"row_id": row_id, "sha256": sha256_bytes(canonical_bytes(dict(row)))})
    return sorted(entries, key=lambda entry: entry["row_id"])


def _digest_entry_map(value: Any, label: str) -> dict[str, str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise PeriodContractError(f"{label}_MUST_BE_ARRAY")
    result: dict[str, str] = {}
    observed_order: list[str] = []
    for raw_entry in value:
        entry = _as_mapping(raw_entry, label)
        if set(entry) != {"row_id", "sha256"}:
            raise PeriodContractError(f"{label}_ENTRY_FIELDS_INVALID")
        row_id = _text(entry.get("row_id"), f"{label}_ROW_ID")
        if row_id in result:
            raise PeriodContractError(f"{label}_DUPLICATE_ROW_ID")
        result[row_id] = _sha256_text(entry.get("sha256"), f"{label}_SHA256")
        observed_order.append(row_id)
    if observed_order != sorted(observed_order):
        raise PeriodContractError(f"{label}_NOT_CANONICALLY_SORTED")
    return result


def _changed_digest_ids(previous: Mapping[str, str], current: Mapping[str, str]) -> list[str]:
    return sorted(
        row_id
        for row_id in set(previous) | set(current)
        if previous.get(row_id) != current.get(row_id)
    )


def _metric_identity_is_valid(metric: Mapping[str, Any]) -> bool:
    source = copy.deepcopy(dict(metric))
    observed = source.pop("metric_identity", None)
    return isinstance(observed, str) and observed == sha256_bytes(canonical_bytes(source))


def _metric_change_digest_entries(
    metrics: Sequence[Mapping[str, Any]],
) -> list[dict[str, str]]:
    comparison_rows: list[dict[str, Any]] = []
    for metric in metrics:
        row = copy.deepcopy(dict(metric))
        for field in (
            "metric_identity",
            "period_id",
            "period_revision_id",
            "period_scope",
            "source_population_sha256",
            "unknown_period_row_count",
        ):
            row.pop(field, None)
        comparison_rows.append(row)
    return _row_digest_entries(
        comparison_rows,
        label="METRIC_CHANGE",
        id_fields=("metric_id",),
    )


def project_period_control_summary_v1(period_revision: Mapping[str, Any]) -> dict[str, Any]:
    """Project a rich period revision into the exact supplied closed-v1 shape.

    The authenticated ``period_control_summary.v1`` schema has
    ``additionalProperties: false`` at its root.  Revision custody, late-evidence
    lineage, identities, and the full nonassurance notice therefore remain in
    the distinct revision envelope returned by :func:`build_period_revision`.
    This projection is deliberately lossy and contains no unrecognized root
    members.
    """

    source = _as_mapping(period_revision, "PERIOD_REVISION")
    revision_number = source.get("revision_number")
    if type(revision_number) is not int or revision_number < 1:
        raise PeriodContractError("REVISION_NUMBER_INVALID")

    population_identity = _text(source.get("population_identity"), "POPULATION_IDENTITY")
    if len(population_identity) != 64 or any(
        character not in "0123456789abcdef" for character in population_identity
    ):
        raise PeriodContractError("POPULATION_IDENTITY_INVALID")

    population_source = _as_mapping(source.get("population_counts"), "POPULATION_COUNTS")
    population_counts = {
        key: _nonnegative_int(population_source.get(key), f"POPULATION_COUNT_{key.upper()}")
        for key in ("created", "sealed", "refused", "incomplete", "repair_children")
    }

    control_source = _as_mapping(source.get("control_results"), "CONTROL_RESULTS")
    control_results = {
        result: _nonnegative_int(control_source.get(result), f"CONTROL_RESULT_{result}")
        for result in CONTROL_RESULTS
    }

    metrics_source = source.get("metrics")
    if isinstance(metrics_source, (str, bytes)) or not isinstance(metrics_source, Sequence):
        raise PeriodContractError("METRICS_MUST_BE_ARRAY")
    metrics = [
        copy.deepcopy(dict(_as_mapping(metric, "METRIC"))) for metric in metrics_source
    ]

    reconciliation_source = _as_mapping(source.get("reconciliation"), "RECONCILIATION")
    reconciliation_status = reconciliation_source.get("status")
    if reconciliation_status not in {"PASS", "FAIL", "HOLD"}:
        raise PeriodContractError("RECONCILIATION_STATUS_INVALID")
    reconciliation = {
        "status": reconciliation_status,
        "unexplained_difference_count": _nonnegative_int(
            reconciliation_source.get("unexplained_difference_count"),
            "RECONCILIATION_UNEXPLAINED_DIFFERENCE_COUNT",
        ),
    }

    management_status = source.get("management_representation_status")
    if management_status not in {
        "NOT_PREPARED",
        "DRAFT",
        "HUMAN_ADOPTED_UNSIGNED",
        "HUMAN_SIGNED",
    }:
        raise PeriodContractError("MANAGEMENT_REPRESENTATION_STATUS_INVALID")
    if source.get("assurance_status") != "NO_ASSURANCE_PROVIDED":
        raise PeriodContractError("ASSURANCE_STATUS_INVALID")
    if source.get("authority_effect") != AUTHORITY_EFFECT:
        raise PeriodContractError("AUTHORITY_EFFECT_INVALID")

    summary = {
        "schema_id": PERIOD_CONTROL_SUMMARY_V1_SCHEMA_ID,
        "period_id": _text(source.get("period_id"), "PERIOD_ID"),
        "revision_id": _text(source.get("revision_id"), "REVISION_ID"),
        "revision_number": revision_number,
        "start_utc": _utc(source.get("start_utc"), "START_UTC"),
        "end_utc": _utc(source.get("end_utc"), "END_UTC"),
        "inclusion_policy_version": _text(
            source.get("inclusion_policy_version"), "INCLUSION_POLICY_VERSION"
        ),
        "population_identity": population_identity,
        "population_counts": population_counts,
        "control_results": control_results,
        "open_exception_count": _nonnegative_int(
            source.get("open_exception_count"), "OPEN_EXCEPTION_COUNT"
        ),
        "metrics": metrics,
        "reconciliation": reconciliation,
        "preparer_posture": _text(source.get("preparer_posture"), "PREPARER_POSTURE"),
        "management_representation_status": management_status,
        "assurance_status": "NO_ASSURANCE_PROVIDED",
        "authority_effect": AUTHORITY_EFFECT,
    }
    parent_revision_id = source.get("parent_revision_id")
    if parent_revision_id is not None:
        summary["parent_revision_id"] = _text(parent_revision_id, "PARENT_REVISION_ID")
    return summary


def build_period_revision(
    *,
    period_id: str,
    revision_number: int,
    start_utc: str,
    end_utc: str,
    created_at_utc: str,
    population_rows: Sequence[Any],
    reconciliation: Mapping[str, Any],
    metrics: Sequence[Any] = (),
    control_rows: Sequence[Any] = (),
    finding_rows: Sequence[Any] = (),
    evidence_rows: Sequence[Any] = (),
    previous_revision: Mapping[str, Any] | None = None,
    creation_reason: str = "INITIAL_PERIOD_CLOSE",
    changed_population_ids: Sequence[str] = (),
    changed_evidence_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Create a rich deterministic envelope bound to a retained predecessor.

    The envelope embeds an exact supplied-v1 control-summary projection while
    retaining the additional immutable lineage fields under its own distinct
    schema identifier.
    """

    period_id = _text(period_id, "PERIOD_ID")
    if not isinstance(revision_number, int) or isinstance(revision_number, bool) or revision_number < 1:
        raise PeriodContractError("REVISION_NUMBER_INVALID")
    start_utc = _utc(start_utc, "START_UTC")
    end_utc = _utc(end_utc, "END_UTC")
    created_at_utc = _utc(created_at_utc, "CREATED_AT_UTC")
    if datetime.fromisoformat(start_utc[:-1] + "+00:00") > datetime.fromisoformat(
        end_utc[:-1] + "+00:00"
    ):
        raise PeriodContractError("PERIOD_RANGE_INVALID")
    if datetime.fromisoformat(created_at_utc[:-1] + "+00:00") < datetime.fromisoformat(
        end_utc[:-1] + "+00:00"
    ):
        raise PeriodContractError("REVISION_CREATED_BEFORE_PERIOD_END")
    creation_reason = _text(creation_reason, "CREATION_REASON")

    normalized_rows = [copy.deepcopy(dict(_as_mapping(row, "POPULATION_ROW"))) for row in population_rows]
    if any(row.get("period_id") != period_id for row in normalized_rows):
        raise PeriodContractError("POPULATION_ROW_PERIOD_MISMATCH_OR_MISSING")
    period_start = datetime.fromisoformat(start_utc[:-1] + "+00:00")
    period_end = datetime.fromisoformat(end_utc[:-1] + "+00:00")
    for row in normalized_rows:
        created_at = _utc(row.get("created_at_utc"), "POPULATION_ROW_CREATED_AT_UTC")
        created = datetime.fromisoformat(created_at[:-1] + "+00:00")
        if created < period_start or created > period_end:
            raise PeriodContractError("POPULATION_ROW_OUTSIDE_CLOSED_PERIOD_SCOPE")
    normalized_metrics = [copy.deepcopy(dict(_as_mapping(row, "METRIC"))) for row in metrics]
    normalized_controls = [
        copy.deepcopy(dict(_as_mapping(row, "CONTROL_ROW"))) for row in control_rows
    ]
    normalized_findings = [
        copy.deepcopy(dict(_as_mapping(row, "FINDING"))) for row in finding_rows
    ]
    normalized_evidence = [
        copy.deepcopy(dict(_as_mapping(row, "EVIDENCE_ROW"))) for row in evidence_rows
    ]
    population = population_document(normalized_rows)
    population_row_digests = _row_digest_entries(
        normalized_rows,
        label="POPULATION",
        id_fields=("population_row_id",),
    )
    evidence_row_digests = _row_digest_entries(
        [*normalized_controls, *normalized_findings, *normalized_evidence],
        label="EVIDENCE",
        id_fields=(
            "evidence_id",
            "execution_id",
            "finding_id",
            "event_sha256",
            "event_id",
            "change_id",
            "verification_id",
            "package_id",
            "transaction_id",
            "row_id",
        ),
    )
    metric_row_digests = _row_digest_entries(
        normalized_metrics,
        label="METRIC",
        id_fields=("metric_id",),
    )
    metric_change_digests = _metric_change_digest_entries(normalized_metrics)
    revision_id = f"{period_id}-R{revision_number:04d}"
    metric_population_sha256 = sha256_bytes(
        canonical_bytes(
            sorted(
                normalized_rows,
                key=lambda row: (
                    str(row.get("transaction_id")),
                    str(row.get("population_row_id")),
                ),
            )
        )
    )
    for metric in normalized_metrics:
        if not _metric_identity_is_valid(metric):
            raise PeriodContractError("METRIC_IDENTITY_INVALID")
        if metric.get("period_id") != period_id:
            raise PeriodContractError("METRIC_PERIOD_ID_MISMATCH")
        if metric.get("period_revision_id") != revision_id:
            raise PeriodContractError("METRIC_REVISION_ID_MISMATCH")
        if metric.get("source_population_sha256") != metric_population_sha256:
            raise PeriodContractError("METRIC_POPULATION_IDENTITY_MISMATCH")
    if not normalized_metrics:
        raise PeriodContractError("PERIOD_METRICS_REQUIRED")
    try:
        from .metrics import MetricContractError, metrics_document

        metrics_document(normalized_metrics)
    except MetricContractError as exc:
        raise PeriodContractError(f"PERIOD_METRICS_INVALID:{exc}") from exc

    changed_population = _string_list(changed_population_ids, "CHANGED_POPULATION_IDS")
    changed_evidence = _string_list(changed_evidence_ids, "CHANGED_EVIDENCE_IDS")
    predecessor: dict[str, Any] | None = None
    parent_revision_id: str | None = None
    before_metric_digest: str | None = None
    changed_metric_ids: list[str] = []
    if previous_revision is None:
        if revision_number != 1:
            raise PeriodContractError("REVISION_PREDECESSOR_REQUIRED")
        if creation_reason != "INITIAL_PERIOD_CLOSE":
            raise PeriodContractError("INITIAL_REVISION_REASON_INVALID")
        if changed_population or changed_evidence:
            raise PeriodContractError("INITIAL_REVISION_MUST_NOT_DECLARE_CHANGES")
    else:
        previous = copy.deepcopy(dict(_as_mapping(previous_revision, "PREVIOUS_REVISION")))
        if set(previous) != PERIOD_REVISION_ENVELOPE_FIELDS:
            raise PeriodContractError("PREVIOUS_REVISION_FIELDS_INVALID")
        previous_without_identity = copy.deepcopy(previous)
        previous_identity = previous_without_identity.pop("revision_identity", None)
        if previous_identity != sha256_bytes(canonical_bytes(previous_without_identity)):
            raise PeriodContractError("PREVIOUS_REVISION_IDENTITY_INVALID")
        try:
            if previous.get("period_control_summary_v1") != project_period_control_summary_v1(previous):
                raise PeriodContractError("PREVIOUS_REVISION_V1_PROJECTION_INVALID")
        except PeriodContractError as exc:
            raise PeriodContractError("PREVIOUS_REVISION_V1_PROJECTION_INVALID") from exc
        if previous.get("period_id") != period_id:
            raise PeriodContractError("REVISION_PERIOD_MISMATCH")
        if previous.get("start_utc") != start_utc or previous.get("end_utc") != end_utc:
            raise PeriodContractError("REVISION_CLOSED_PERIOD_SCOPE_CHANGED")
        if previous.get("inclusion_policy_version") != INCLUSION_POLICY_VERSION:
            raise PeriodContractError("REVISION_INCLUSION_POLICY_CHANGED")
        if previous.get("revision_number") != revision_number - 1:
            raise PeriodContractError("REVISION_SEQUENCE_INVALID")
        if creation_reason == "INITIAL_PERIOD_CLOSE":
            raise PeriodContractError("SUCCESSOR_REVISION_REASON_INVALID")
        previous_created_at = _utc(previous.get("created_at_utc"), "PREVIOUS_CREATED_AT_UTC")
        if datetime.fromisoformat(created_at_utc[:-1] + "+00:00") < datetime.fromisoformat(
            previous_created_at[:-1] + "+00:00"
        ):
            raise PeriodContractError("REVISION_CREATED_AT_PRECEDES_PARENT")
        parent_revision_id = _text(previous.get("revision_id"), "PARENT_REVISION_ID")
        previous_sha256 = sha256_bytes(canonical_bytes(previous))
        predecessor = {
            "revision_id": parent_revision_id,
            "revision_sha256": previous_sha256,
            "retained": True,
            "superseded_but_retained": True,
        }
        before_metric_digest = sha256_bytes(canonical_bytes(previous.get("metrics", [])))
        expected_population_changes = _changed_digest_ids(
            _digest_entry_map(previous.get("population_row_digests"), "PREVIOUS_POPULATION_DIGESTS"),
            _digest_entry_map(population_row_digests, "CURRENT_POPULATION_DIGESTS"),
        )
        expected_evidence_changes = _changed_digest_ids(
            _digest_entry_map(previous.get("evidence_row_digests"), "PREVIOUS_EVIDENCE_DIGESTS"),
            _digest_entry_map(evidence_row_digests, "CURRENT_EVIDENCE_DIGESTS"),
        )
        changed_metric_ids = _changed_digest_ids(
            _digest_entry_map(previous.get("metric_change_digests"), "PREVIOUS_METRIC_CHANGE_DIGESTS"),
            _digest_entry_map(metric_change_digests, "CURRENT_METRIC_CHANGE_DIGESTS"),
        )
        if changed_population != expected_population_changes:
            raise PeriodContractError("CHANGED_POPULATION_IDS_INEXACT")
        if changed_evidence != expected_evidence_changes:
            raise PeriodContractError("CHANGED_EVIDENCE_IDS_INEXACT")
        if not expected_population_changes and not expected_evidence_changes:
            raise PeriodContractError("REVISION_CHANGE_LINEAGE_REQUIRED")

    control_counts = Counter(str(row.get("result")) for row in normalized_controls)
    unknown_results = set(control_counts) - set(CONTROL_RESULTS)
    if unknown_results:
        raise PeriodContractError("UNKNOWN_CONTROL_RESULT")
    open_exceptions = 0
    for row in normalized_findings:
        if str(row.get("status", "OPEN")).upper() in FINDING_OPEN_STATES:
            open_exceptions += 1

    population_counts = {
        "created": len(normalized_rows),
        "parent_transactions": sum(row.get("lineage_role") == "PARENT" for row in normalized_rows),
        "repair_children": sum(row.get("lineage_role") == "REPAIR_CHILD" for row in normalized_rows),
        "admitted": sum(row.get("admission_status") == "ADMITTED" for row in normalized_rows),
        "refused": sum(row.get("admission_status") == "REFUSED" for row in normalized_rows),
        "sealed": sum(row.get("sealed") is True for row in normalized_rows),
        "incomplete": sum(row.get("incomplete") is True for row in normalized_rows),
        "adverse": sum(row.get("adverse") is True for row in normalized_rows),
    }
    result = {
        "schema_id": PERIOD_REVISION_ENVELOPE_SCHEMA_ID,
        "period_id": period_id,
        "revision_id": revision_id,
        "revision_number": revision_number,
        "parent_revision_id": parent_revision_id,
        "created_at_utc": created_at_utc,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "inclusion_policy_version": INCLUSION_POLICY_VERSION,
        "creation_reason": creation_reason,
        "changed_population_ids": changed_population,
        "changed_evidence_ids": changed_evidence,
        "changed_metric_ids": changed_metric_ids,
        "population_identity": population["population_identity"],
        "metric_population_sha256": metric_population_sha256,
        "population_row_digests": population_row_digests,
        "evidence_row_digests": evidence_row_digests,
        "metric_row_digests": metric_row_digests,
        "metric_change_digests": metric_change_digests,
        "population_counts": population_counts,
        "control_results": {name: control_counts[name] for name in CONTROL_RESULTS},
        "open_exception_count": open_exceptions,
        "metrics": normalized_metrics,
        "before_metric_digest": before_metric_digest,
        "after_metric_digest": sha256_bytes(canonical_bytes(normalized_metrics)),
        "reconciliation": copy.deepcopy(dict(reconciliation)),
        "preparer_posture": "SYSTEM_GENERATED",
        "management_representation_status": "NOT_PREPARED",
        "predecessor_retention": predecessor,
        "assurance_status": "NO_ASSURANCE_PROVIDED",
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "opinion_generated_or_prefilled": False,
        "authority_effect": AUTHORITY_EFFECT,
    }
    result["period_control_summary_v1"] = project_period_control_summary_v1(result)
    result["revision_identity"] = sha256_bytes(canonical_bytes(result))
    return result


def verify_revision_lineage(previous: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, Any]:
    previous_copy = copy.deepcopy(dict(_as_mapping(previous, "PREVIOUS_REVISION")))
    current_copy = copy.deepcopy(dict(_as_mapping(current, "CURRENT_REVISION")))
    expected_sha256 = sha256_bytes(canonical_bytes(previous_copy))
    mismatches: list[str] = []

    def mismatch_if(condition: bool, code: str) -> None:
        if condition:
            mismatches.append(code)

    def validate_envelope(source: Mapping[str, Any], label: str) -> None:
        mismatch_if(set(source) != PERIOD_REVISION_ENVELOPE_FIELDS, f"{label}_FIELDS")
        without_identity = copy.deepcopy(dict(source))
        observed_identity = without_identity.pop("revision_identity", None)
        mismatch_if(
            observed_identity != sha256_bytes(canonical_bytes(without_identity)),
            f"{label}_REVISION_IDENTITY",
        )
        mismatch_if(source.get("schema_id") != PERIOD_REVISION_ENVELOPE_SCHEMA_ID, f"{label}_SCHEMA")
        revision_number = source.get("revision_number")
        period_id = source.get("period_id")
        expected_revision_id = (
            f"{period_id}-R{revision_number:04d}"
            if isinstance(period_id, str)
            and period_id
            and type(revision_number) is int
            and revision_number >= 1
            else None
        )
        mismatch_if(source.get("revision_id") != expected_revision_id, f"{label}_REVISION_ID")
        try:
            start = _utc(source.get("start_utc"), f"{label}_START_UTC")
            end = _utc(source.get("end_utc"), f"{label}_END_UTC")
            created = _utc(source.get("created_at_utc"), f"{label}_CREATED_AT_UTC")
            mismatch_if(
                datetime.fromisoformat(start[:-1] + "+00:00")
                > datetime.fromisoformat(end[:-1] + "+00:00"),
                f"{label}_PERIOD_RANGE",
            )
            mismatch_if(
                datetime.fromisoformat(created[:-1] + "+00:00")
                < datetime.fromisoformat(end[:-1] + "+00:00"),
                f"{label}_CREATED_BEFORE_PERIOD_END",
            )
        except PeriodContractError:
            mismatches.append(f"{label}_TIME")
        mismatch_if(
            source.get("inclusion_policy_version") != INCLUSION_POLICY_VERSION,
            f"{label}_INCLUSION_POLICY",
        )
        try:
            _sha256_text(source.get("population_identity"), f"{label}_POPULATION_IDENTITY")
            _sha256_text(
                source.get("metric_population_sha256"),
                f"{label}_METRIC_POPULATION_SHA256",
            )
        except PeriodContractError:
            mismatches.append(f"{label}_POPULATION_IDENTITIES")
        mismatch_if(source.get("nonassurance") != NONASSURANCE_NOTICE, f"{label}_NONASSURANCE")
        mismatch_if(source.get("assurance_status") != "NO_ASSURANCE_PROVIDED", f"{label}_ASSURANCE")
        mismatch_if(source.get("contains_assurance_conclusion") is not False, f"{label}_CONCLUSION")
        mismatch_if(source.get("opinion_generated_or_prefilled") is not False, f"{label}_OPINION")
        mismatch_if(source.get("authority_effect") != AUTHORITY_EFFECT, f"{label}_AUTHORITY")
        mismatch_if(source.get("preparer_posture") != "SYSTEM_GENERATED", f"{label}_PREPARER")
        mismatch_if(
            source.get("management_representation_status") != "NOT_PREPARED",
            f"{label}_MANAGEMENT_REPRESENTATION",
        )

        metrics_value = source.get("metrics")
        if isinstance(metrics_value, (str, bytes)) or not isinstance(metrics_value, Sequence):
            mismatches.append(f"{label}_METRICS")
            metrics_rows: list[Mapping[str, Any]] = []
        else:
            metrics_rows = []
            for metric in metrics_value:
                if not isinstance(metric, Mapping):
                    mismatches.append(f"{label}_METRIC_SHAPE")
                    continue
                metrics_rows.append(metric)
                mismatch_if(not _metric_identity_is_valid(metric), f"{label}_METRIC_IDENTITY")
                mismatch_if(metric.get("period_id") != period_id, f"{label}_METRIC_PERIOD")
                mismatch_if(
                    metric.get("period_revision_id") != source.get("revision_id"),
                    f"{label}_METRIC_REVISION",
                )
                mismatch_if(
                    metric.get("source_population_sha256")
                    != source.get("metric_population_sha256"),
                    f"{label}_METRIC_POPULATION",
                )
        mismatch_if(
            source.get("after_metric_digest") != sha256_bytes(canonical_bytes(metrics_rows)),
            f"{label}_AFTER_METRIC_DIGEST",
        )
        try:
            metric_digests = _digest_entry_map(
                source.get("metric_row_digests"), f"{label}_METRIC_DIGESTS"
            )
            expected_metric_digests = {
                str(metric.get("metric_id")): sha256_bytes(canonical_bytes(dict(metric)))
                for metric in metrics_rows
                if isinstance(metric.get("metric_id"), str) and metric.get("metric_id")
            }
            mismatch_if(metric_digests != expected_metric_digests, f"{label}_METRIC_DIGESTS")
            metric_change_digests = _digest_entry_map(
                source.get("metric_change_digests"), f"{label}_METRIC_CHANGE_DIGESTS"
            )
            expected_metric_change_digests = {
                entry["row_id"]: entry["sha256"]
                for entry in _metric_change_digest_entries(metrics_rows)
            }
            mismatch_if(
                metric_change_digests != expected_metric_change_digests,
                f"{label}_METRIC_CHANGE_DIGESTS",
            )
            population_digests = _digest_entry_map(
                source.get("population_row_digests"), f"{label}_POPULATION_DIGESTS"
            )
            evidence_digests = _digest_entry_map(
                source.get("evidence_row_digests"), f"{label}_EVIDENCE_DIGESTS"
            )
            counts = source.get("population_counts")
            mismatch_if(
                not isinstance(counts, Mapping) or counts.get("created") != len(population_digests),
                f"{label}_POPULATION_COUNT",
            )
            # Force evaluation so malformed maps are rejected even when empty.
            _ = evidence_digests
        except PeriodContractError:
            mismatches.append(f"{label}_ROW_DIGESTS")
        try:
            changed_population = _string_list(
                source.get("changed_population_ids"), f"{label}_CHANGED_POPULATION_IDS"
            )
            changed_evidence = _string_list(
                source.get("changed_evidence_ids"), f"{label}_CHANGED_EVIDENCE_IDS"
            )
            changed_metrics = _string_list(
                source.get("changed_metric_ids"), f"{label}_CHANGED_METRIC_IDS"
            )
            mismatch_if(changed_population != source.get("changed_population_ids"), f"{label}_CHANGED_POPULATION_ORDER")
            mismatch_if(changed_evidence != source.get("changed_evidence_ids"), f"{label}_CHANGED_EVIDENCE_ORDER")
            mismatch_if(changed_metrics != source.get("changed_metric_ids"), f"{label}_CHANGED_METRIC_ORDER")
        except PeriodContractError:
            mismatches.append(f"{label}_CHANGED_IDS")
        try:
            mismatch_if(
                source.get("period_control_summary_v1")
                != project_period_control_summary_v1(source),
                f"{label}_V1_PROJECTION",
            )
        except PeriodContractError:
            mismatches.append(f"{label}_V1_PROJECTION")
        if revision_number == 1:
            mismatch_if(source.get("parent_revision_id") is not None, f"{label}_INITIAL_PARENT")
            mismatch_if(source.get("predecessor_retention") is not None, f"{label}_INITIAL_RETENTION")
            mismatch_if(source.get("before_metric_digest") is not None, f"{label}_INITIAL_BEFORE_METRICS")
            mismatch_if(source.get("creation_reason") != "INITIAL_PERIOD_CLOSE", f"{label}_INITIAL_REASON")
            mismatch_if(source.get("changed_population_ids") != [], f"{label}_INITIAL_POPULATION_CHANGES")
            mismatch_if(source.get("changed_evidence_ids") != [], f"{label}_INITIAL_EVIDENCE_CHANGES")
            mismatch_if(source.get("changed_metric_ids") != [], f"{label}_INITIAL_METRIC_CHANGES")

    validate_envelope(previous_copy, "PREVIOUS")
    validate_envelope(current_copy, "CURRENT")
    retention = current_copy.get("predecessor_retention")
    mismatch_if(not isinstance(retention, Mapping), "PREDECESSOR_RETENTION")
    if isinstance(retention, Mapping):
        mismatch_if(
            set(retention)
            != {"revision_id", "revision_sha256", "retained", "superseded_but_retained"},
            "PREDECESSOR_RETENTION_FIELDS",
        )
        mismatch_if(retention.get("retained") is not True, "PREDECESSOR_NOT_RETAINED")
        mismatch_if(
            retention.get("superseded_but_retained") is not True,
            "PREDECESSOR_NOT_MARKED_SUPERSEDED_RETAINED",
        )
        mismatch_if(retention.get("revision_id") != previous_copy.get("revision_id"), "PREDECESSOR_ID")
        mismatch_if(retention.get("revision_sha256") != expected_sha256, "PREDECESSOR_DIGEST")
    mismatch_if(current_copy.get("parent_revision_id") != previous_copy.get("revision_id"), "PARENT_ID")
    mismatch_if(
        current_copy.get("revision_number") != previous_copy.get("revision_number", 0) + 1,
        "REVISION_SEQUENCE",
    )
    mismatch_if(current_copy.get("period_id") != previous_copy.get("period_id"), "PERIOD_ID")
    mismatch_if(current_copy.get("start_utc") != previous_copy.get("start_utc"), "PERIOD_START")
    mismatch_if(current_copy.get("end_utc") != previous_copy.get("end_utc"), "PERIOD_END")
    try:
        previous_created = _utc(previous_copy.get("created_at_utc"), "PREVIOUS_CREATED_AT_UTC")
        current_created = _utc(current_copy.get("created_at_utc"), "CURRENT_CREATED_AT_UTC")
        mismatch_if(
            datetime.fromisoformat(current_created[:-1] + "+00:00")
            < datetime.fromisoformat(previous_created[:-1] + "+00:00"),
            "REVISION_CREATED_AT_ORDER",
        )
    except PeriodContractError:
        mismatches.append("REVISION_CREATED_AT_ORDER")
    mismatch_if(
        current_copy.get("inclusion_policy_version") != previous_copy.get("inclusion_policy_version"),
        "INCLUSION_POLICY",
    )
    mismatch_if(current_copy.get("creation_reason") == "INITIAL_PERIOD_CLOSE", "SUCCESSOR_REASON")
    mismatch_if(
        current_copy.get("before_metric_digest")
        != sha256_bytes(canonical_bytes(previous_copy.get("metrics", []))),
        "BEFORE_METRIC_DIGEST",
    )
    try:
        expected_population_changes = _changed_digest_ids(
            _digest_entry_map(previous_copy.get("population_row_digests"), "PREVIOUS_POPULATION_DIGESTS"),
            _digest_entry_map(current_copy.get("population_row_digests"), "CURRENT_POPULATION_DIGESTS"),
        )
        expected_evidence_changes = _changed_digest_ids(
            _digest_entry_map(previous_copy.get("evidence_row_digests"), "PREVIOUS_EVIDENCE_DIGESTS"),
            _digest_entry_map(current_copy.get("evidence_row_digests"), "CURRENT_EVIDENCE_DIGESTS"),
        )
        expected_metric_changes = _changed_digest_ids(
            _digest_entry_map(previous_copy.get("metric_change_digests"), "PREVIOUS_METRIC_CHANGE_DIGESTS"),
            _digest_entry_map(current_copy.get("metric_change_digests"), "CURRENT_METRIC_CHANGE_DIGESTS"),
        )
        mismatch_if(current_copy.get("changed_population_ids") != expected_population_changes, "CHANGED_POPULATION_IDS")
        mismatch_if(current_copy.get("changed_evidence_ids") != expected_evidence_changes, "CHANGED_EVIDENCE_IDS")
        mismatch_if(current_copy.get("changed_metric_ids") != expected_metric_changes, "CHANGED_METRIC_IDS")
        mismatch_if(not expected_population_changes and not expected_evidence_changes, "NO_REVISION_CHANGE")
    except PeriodContractError:
        mismatches.append("CHANGE_DIGEST_MAPS")
    return {
        "status": "PASS" if not mismatches else "HOLD",
        "previous_revision_id": previous_copy.get("revision_id"),
        "previous_revision_sha256": expected_sha256,
        "current_revision_id": current_copy.get("revision_id"),
        "mismatches": sorted(set(mismatches)),
        "source_evidence_mutated": False,
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "opinion_generated_or_prefilled": False,
        "authority_effect": AUTHORITY_EFFECT,
    }


verify_period_revision_immutability = verify_revision_lineage
