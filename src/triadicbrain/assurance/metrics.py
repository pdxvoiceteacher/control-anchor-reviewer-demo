"""Reproducible, drill-through period metrics without a compliance score."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

from .canonical import canonical_bytes, sha256_bytes


NONASSURANCE_NOTICE = "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED."
AUTHORITY_EFFECT = "NONE"
METRIC_VERSION = "1.0.0"
CALCULATION_VERSION = "aep01.metrics.v1"
CONTROL_RESULTS = {"PASS", "FAIL", "HOLD", "NOT_EXECUTED", "ERROR"}
OPEN_STATES = {"OPEN", "UNRESOLVED", "PENDING", "MANAGEMENT_RESPONSE_PROVIDED"}

METRIC_NAMES = {
    "MET-001": "transactions_created",
    "MET-002": "transactions_admitted",
    "MET-003": "transactions_refused",
    "MET-004": "transactions_sealed",
    "MET-005": "transactions_incomplete",
    "MET-006": "human_approvals",
    "MET-007": "approved_with_open_advisories",
    "MET-008": "human_holds",
    "MET-009": "human_rejections",
    "MET-010": "repair_requests",
    "MET-011": "repair_children_completed",
    "MET-012": "required_control_pass_rate",
    "MET-013": "control_failures",
    "MET-014": "control_holds",
    "MET-015": "controls_not_executed",
    "MET-016": "open_exceptions",
    "MET-017": "overrides",
    "MET-018": "unauthorized_attempts",
    "MET-019": "configuration_changes",
    "MET-020": "unapproved_change_attempts",
    "MET-021": "custody_verification_failures",
    "MET-022": "population_reconciliation_difference",
    "MET-023": "mean_human_review_seconds",
    "MET-024": "provider_unavailable_count",
    "MET-025": "period_revision_count",
    "MET-026": "evidence_packages_with_external_signature",
}
METRIC_FIELDS = {
    "schema_id",
    "metric_id",
    "metric_version",
    "name",
    "value",
    "unit",
    "numerator",
    "denominator",
    "filters",
    "null_count",
    "null_treatment",
    "source_row_ids",
    "source_row_digests",
    "source_row_count",
    "calculation_version",
    "precision",
    "rounding",
    "human_adjudication",
    "limitations",
    "claim_ceiling",
    "nonassurance",
    "contains_assurance_conclusion",
    "opinion_generated_or_prefilled",
    "authority_effect",
    "period_id",
    "period_scope",
    "unknown_period_row_count",
    "period_revision_id",
    "source_population_sha256",
    "metric_identity",
}


class MetricContractError(ValueError):
    """A requested metric would be incomplete or non-reproducible."""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        result = to_dict()
        if isinstance(result, Mapping):
            return result
    raise MetricContractError(f"{label}_MUST_BE_OBJECT")


def _row_id(row: Mapping[str, Any], prefix: str) -> str:
    for key in (
        "population_row_id",
        "execution_id",
        "finding_id",
        "review_id",
        "revision_id",
        "event_sha256",
        "event_id",
        "change_id",
        "verification_id",
        "package_id",
        "difference_id",
        "transaction_id",
        "row_id",
    ):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    raise MetricContractError(f"{prefix}_SOURCE_ROW_ID_MISSING")


def _rows(values: Sequence[Any], label: str) -> list[Mapping[str, Any]]:
    result = [_mapping(value, label) for value in values]
    ids = [_row_id(row, label) for row in result]
    if len(ids) != len(set(ids)):
        raise MetricContractError(f"DUPLICATE_{label}_ROW_ID")
    return result


def _utc_datetime(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise MetricContractError(f"{label}_MUST_BE_UTC_Z")
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise MetricContractError(f"{label}_INVALID") from exc


def _metric(
    metric_id: str,
    *,
    value: int | float | None,
    unit: str,
    rows: Sequence[Mapping[str, Any]],
    numerator: int | None = None,
    denominator: int | None = None,
    filters: Mapping[str, Any] | None = None,
    null_count: int = 0,
    human_adjudication: str = "NONE",
    limitations: Sequence[str] = (),
    precision: int | None = None,
) -> dict[str, Any]:
    if metric_id not in METRIC_NAMES:
        raise MetricContractError("UNKNOWN_METRIC_ID")
    if isinstance(value, float) and not math.isfinite(value):
        raise MetricContractError("NONFINITE_METRIC_VALUE")
    source_pairs = sorted(
        ((_row_id(row, metric_id), sha256_bytes(canonical_bytes(dict(row)))) for row in rows),
        key=lambda item: item[0],
    )
    source_ids = [row_id for row_id, _digest in source_pairs]
    if len(source_ids) != len(set(source_ids)):
        raise MetricContractError(f"{metric_id}_DUPLICATE_SOURCE_ROW_ID")
    result = {
        "schema_id": "uvlm.triadicbrain.aep01.period_metric.v1",
        "metric_id": metric_id,
        "metric_version": METRIC_VERSION,
        "name": METRIC_NAMES[metric_id],
        "value": value,
        "unit": unit,
        "numerator": numerator,
        "denominator": denominator,
        "filters": dict(filters or {}),
        "null_count": null_count,
        "null_treatment": "Null and unavailable values are disclosed and never coerced to PASS.",
        "source_row_ids": source_ids,
        "source_row_digests": [
            {"row_id": row_id, "sha256": digest} for row_id, digest in source_pairs
        ],
        "source_row_count": len(source_ids),
        "calculation_version": CALCULATION_VERSION,
        "precision": precision,
        "rounding": "ROUND_HALF_EVEN_TO_DECLARED_PRECISION" if precision is not None else "NOT_APPLICABLE",
        "human_adjudication": human_adjudication,
        "limitations": list(limitations),
        "claim_ceiling": "Operational evidence metric only; no compliance or assurance conclusion.",
        "nonassurance": NONASSURANCE_NOTICE,
        "contains_assurance_conclusion": False,
        "opinion_generated_or_prefilled": False,
        "authority_effect": AUTHORITY_EFFECT,
    }
    result["metric_identity"] = sha256_bytes(canonical_bytes(result))
    return result


def derive_metrics(
    population_rows: Sequence[Any],
    *,
    period_id: str | None = None,
    period_revision_id: str | None = None,
    control_rows: Sequence[Any] = (),
    finding_rows: Sequence[Any] = (),
    custody_rows: Sequence[Any] = (),
    change_rows: Sequence[Any] = (),
    verification_rows: Sequence[Any] = (),
    package_rows: Sequence[Any] = (),
    human_review_rows: Sequence[Any] = (),
    period_revision_rows: Sequence[Any] = (),
    reconciliation: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Derive the commissioned metric dictionary with exact row drill-through."""
    population = _rows(population_rows, "POPULATION")
    observed_period_ids = {
        str(row["period_id"])
        for row in population
        if isinstance(row.get("period_id"), str) and row.get("period_id")
    }
    unknown_period_row_count = sum(not row.get("period_id") for row in population)
    if period_id is None:
        if len(observed_period_ids) == 1:
            effective_period_id = next(iter(observed_period_ids))
            period_scope = (
                "SINGLE_PERIOD"
                if unknown_period_row_count == 0
                else "SINGLE_PERIOD_WITH_UNKNOWN_ROWS"
            )
        elif not observed_period_ids:
            effective_period_id = "UNRESOLVED_PERIOD_SCOPE"
            period_scope = "EMPTY_OR_ALL_ROWS_UNKNOWN"
        else:
            effective_period_id = "MULTI_PERIOD_STORE_SCOPE"
            period_scope = "MULTI_PERIOD"
    else:
        if not isinstance(period_id, str) or not period_id:
            raise MetricContractError("METRIC_PERIOD_ID_INVALID")
        effective_period_id = period_id
        if observed_period_ids and observed_period_ids != {effective_period_id}:
            raise MetricContractError("METRIC_PERIOD_ID_MISMATCH")
        period_scope = (
            "DECLARED_PERIOD"
            if unknown_period_row_count == 0
            else "DECLARED_PERIOD_WITH_UNKNOWN_ROWS_INCLUDED_FOR_COMPLETENESS"
        )
    if period_revision_id is not None and (
        not isinstance(period_revision_id, str) or not period_revision_id
    ):
        raise MetricContractError("METRIC_PERIOD_REVISION_ID_INVALID")
    metric_population_identity = sha256_bytes(
        canonical_bytes(
            sorted(
                (dict(row) for row in population),
                key=lambda row: (str(row.get("transaction_id")), str(row.get("population_row_id"))),
            )
        )
    )
    controls = _rows(control_rows, "CONTROL")
    findings = _rows(finding_rows, "FINDING")
    custody = _rows(custody_rows, "CUSTODY")
    changes = _rows(change_rows, "CHANGE")
    verifications = _rows(verification_rows, "VERIFICATION")
    packages = _rows(package_rows, "PACKAGE")
    human_reviews = _rows(human_review_rows, "HUMAN_REVIEW")
    period_revisions = _rows(period_revision_rows, "PERIOD_REVISION")

    for row in controls:
        if str(row.get("result")) not in CONTROL_RESULTS:
            raise MetricContractError("UNKNOWN_CONTROL_RESULT")

    def population_matching(predicate: Any) -> list[Mapping[str, Any]]:
        return [row for row in population if predicate(row)]

    created = population
    admitted = population_matching(lambda row: row.get("admission_status") == "ADMITTED")
    refused = population_matching(
        lambda row: row.get("admission_status") == "REFUSED" or row.get("transaction_state") == "REFUSED"
    )
    sealed = population_matching(lambda row: row.get("sealed") is True)
    incomplete = population_matching(
        lambda row: row.get("incomplete") is True
        or ("incomplete" not in row and row.get("nonterminal") is True)
    )
    approvals = population_matching(lambda row: row.get("human_decision") == "APPROVE")
    approved_advisory = population_matching(
        lambda row: row.get("human_decision") == "APPROVE"
        and bool(row.get("open_advisory_finding_ids"))
    )
    holds = population_matching(lambda row: row.get("human_decision") == "HOLD")
    rejections = population_matching(lambda row: row.get("human_decision") == "REJECT")
    repairs = population_matching(lambda row: row.get("human_decision") == "REQUEST_REPAIR")
    repair_children = population_matching(
        lambda row: row.get("lineage_role") == "REPAIR_CHILD" and row.get("sealed") is True
    )

    metrics = [
        _metric("MET-001", value=len(created), unit="count", rows=created),
        _metric("MET-002", value=len(admitted), unit="count", rows=admitted, filters={"admission_status": "ADMITTED"}),
        _metric("MET-003", value=len(refused), unit="count", rows=refused, filters={"admission_status": "REFUSED"}),
        _metric("MET-004", value=len(sealed), unit="count", rows=sealed, filters={"sealed": True}),
        _metric(
            "MET-005",
            value=len(incomplete),
            unit="count",
            rows=incomplete,
            filters={"finalization_complete": False},
            human_adjudication="HUMAN_FOLLOW_UP",
        ),
        _metric("MET-006", value=len(approvals), unit="count", rows=approvals, filters={"human_decision": "APPROVE"}),
        _metric(
            "MET-007",
            value=len(approved_advisory),
            unit="count",
            rows=approved_advisory,
            filters={"human_decision": "APPROVE", "open_advisory_finding": True},
            human_adjudication="HUMAN_INTERPRETATION",
            limitations=("Approval does not resolve an advisory finding.",),
        ),
        _metric("MET-008", value=len(holds), unit="count", rows=holds, filters={"human_decision": "HOLD"}),
        _metric("MET-009", value=len(rejections), unit="count", rows=rejections, filters={"human_decision": "REJECT"}),
        _metric(
            "MET-010",
            value=len(repairs),
            unit="count",
            rows=repairs,
            filters={"human_decision": "REQUEST_REPAIR"},
        ),
        _metric(
            "MET-011",
            value=len(repair_children),
            unit="count",
            rows=repair_children,
            filters={"lineage_role": "REPAIR_CHILD", "sealed": True},
        ),
    ]

    required_controls = [
        row
        for row in controls
        if row.get("required") is True
        or row.get("delivery_tier") == "P0_CORE"
        or (
            row.get("delivery_tier") == "P0_WHEN_APPLICABLE"
            and row.get("applicability") == "APPLICABLE"
        )
        or ("required" not in row and "delivery_tier" not in row)
    ]
    required_passes = [row for row in required_controls if row.get("result") == "PASS"]
    denominator = len(required_controls)
    ratio = round(len(required_passes) / denominator, 6) if denominator else None
    metrics.append(
        _metric(
            "MET-012",
            value=ratio,
            unit="ratio",
            rows=required_controls,
            numerator=len(required_passes),
            denominator=denominator,
            filters={"required": True, "result_numerator": "PASS", "not_executed_in_denominator": True},
            null_count=1 if denominator == 0 else 0,
            human_adjudication="NOT_A_COMPLIANCE_SCORE",
            limitations=("The ratio does not establish control effectiveness.",),
            precision=6,
        )
    )

    for metric_id, result_value in (
        ("MET-013", "FAIL"),
        ("MET-014", "HOLD"),
        ("MET-015", "NOT_EXECUTED"),
    ):
        selected = [row for row in controls if row.get("result") == result_value]
        metrics.append(
            _metric(metric_id, value=len(selected), unit="count", rows=selected, filters={"result": result_value})
        )

    open_findings = [row for row in findings if str(row.get("status", "OPEN")).upper() in OPEN_STATES]
    overrides = [
        row
        for row in findings
        if str(
            row.get("finding_type", row.get("finding_class", row.get("type", "")))
        ).upper()
        == "HUMAN_OVERRIDE"
    ]
    unauthorized = [
        row
        for row in custody
        if "UNAUTHORIZED" in " ".join(str(item) for item in row.get("reason_codes", [])).upper()
        or str(row.get("result", "")).upper() == "DENIED"
    ]
    material_changes = [row for row in changes if row.get("effective") is True]
    unapproved_changes = [
        row
        for row in changes
        if row.get("approved") is False or str(row.get("status", "")).upper() in {"DENIED", "MISSING_APPROVAL"}
    ]
    custody_failures = [
        row
        for row in verifications
        if str(row.get("status", row.get("result", ""))).upper() in {"FAIL", "HOLD", "MISMATCH"}
    ]
    difference_count = 0
    difference_rows: list[Mapping[str, Any]] = []
    if reconciliation is not None:
        difference_count = int(reconciliation.get("unexplained_difference_count", 0))
        difference_rows = [
            _mapping(row, "RECONCILIATION_DIFFERENCE")
            for row in reconciliation.get("differences", [])
        ]
    population_transaction_ids = {
        str(row.get("transaction_id")) for row in population if row.get("transaction_id")
    }
    review_transaction_ids: set[str] = set()
    review_durations: list[float] = []
    for row in human_reviews:
        transaction_id = row.get("transaction_id")
        if not isinstance(transaction_id, str) or transaction_id not in population_transaction_ids:
            raise MetricContractError("HUMAN_REVIEW_TRANSACTION_NOT_IN_POPULATION")
        if transaction_id in review_transaction_ids:
            raise MetricContractError("DUPLICATE_HUMAN_REVIEW_TRANSACTION")
        review_transaction_ids.add(transaction_id)
        started = _utc_datetime(row.get("review_started_at_utc"), "REVIEW_STARTED_AT_UTC")
        completed = _utc_datetime(row.get("review_completed_at_utc"), "REVIEW_COMPLETED_AT_UTC")
        if completed < started:
            raise MetricContractError("HUMAN_REVIEW_TIME_RANGE_INVALID")
        if row.get("time_posture") != "OBSERVED_START_AND_END_UTC":
            raise MetricContractError("HUMAN_REVIEW_TIME_POSTURE_INVALID")
        review_durations.append((completed - started).total_seconds())
    review_nulls = len(population_transaction_ids - review_transaction_ids)
    mean_seconds = (
        round(sum(review_durations) / len(review_durations), 3)
        if review_durations
        else None
    )
    provider_unavailable = population_matching(
        lambda row: row.get("transaction_state") == "PROVIDER_UNAVAILABLE"
        or "PROVIDER_UNAVAILABLE" in row.get("reason_codes", [])
    )
    externally_signed = [
        row
        for row in packages
        if row.get("signature_posture") == "ED25519_EXTERNAL_SIGNER"
        and row.get("signature_verified") is True
    ]
    revised_period_rows: list[Mapping[str, Any]] = []
    seen_revision_numbers: set[int] = set()
    for row in period_revisions:
        row_period_id = row.get("period_id")
        if row_period_id != effective_period_id:
            raise MetricContractError("PERIOD_REVISION_ROW_PERIOD_MISMATCH")
        revision_number = row.get("revision_number")
        if type(revision_number) is not int or revision_number < 1:
            raise MetricContractError("PERIOD_REVISION_ROW_NUMBER_INVALID")
        if revision_number in seen_revision_numbers:
            raise MetricContractError("DUPLICATE_PERIOD_REVISION_NUMBER")
        seen_revision_numbers.add(revision_number)
        if revision_number <= 1:
            raise MetricContractError("PERIOD_REVISION_SOURCE_MUST_BE_POST_INITIAL_CLOSE")
        expected_revision_id = f"{effective_period_id}-R{revision_number:04d}"
        if row.get("revision_id") != expected_revision_id:
            raise MetricContractError("PERIOD_REVISION_ROW_IDENTITY_INVALID")
        revised_period_rows.append(row)
    expected_revision_numbers: set[int] | None = None
    if period_revision_id is not None:
        prefix = f"{effective_period_id}-R"
        suffix = period_revision_id[len(prefix) :] if period_revision_id.startswith(prefix) else ""
        if len(suffix) != 4 or not suffix.isdigit() or int(suffix) < 1:
            raise MetricContractError("METRIC_PERIOD_REVISION_ID_INVALID")
        expected_revision_numbers = set(range(2, int(suffix) + 1))
        if seen_revision_numbers != expected_revision_numbers:
            raise MetricContractError("PERIOD_REVISION_SOURCE_POPULATION_INCOMPLETE")
    elif revised_period_rows:
        raise MetricContractError("PERIOD_REVISION_ID_REQUIRED_FOR_REVISION_ROWS")
    revision_count_limitation = (
        "A revision count is unavailable without a bound current period revision identity."
        if expected_revision_numbers is None
        else "Every post-initial revision record through the bound current revision is included."
    )
    metrics.extend(
        [
            _metric(
                "MET-016",
                value=len(open_findings),
                unit="count",
                rows=open_findings,
                filters={"status": sorted(OPEN_STATES)},
                human_adjudication="RISK_CONCLUSION_EXTERNAL",
            ),
            _metric("MET-017", value=len(overrides), unit="count", rows=overrides, filters={"type": "HUMAN_OVERRIDE"}),
            _metric("MET-018", value=len(unauthorized), unit="count", rows=unauthorized, filters={"privileged_action": "DENIED"}),
            _metric("MET-019", value=len(material_changes), unit="count", rows=material_changes, filters={"effective": True}),
            _metric("MET-020", value=len(unapproved_changes), unit="count", rows=unapproved_changes, filters={"approved": False}),
            _metric(
                "MET-021",
                value=len(custody_failures),
                unit="count",
                rows=custody_failures,
                filters={"verification_mismatch": True},
            ),
            _metric(
                "MET-022",
                value=difference_count,
                unit="count",
                rows=difference_rows,
                filters={"difference_class": "UNEXPLAINED"},
                human_adjudication="MUST_BE_ZERO_TO_CLOSE",
            ),
            _metric(
                "MET-023",
                value=mean_seconds,
                unit="seconds",
                rows=human_reviews,
                null_count=review_nulls,
                filters={
                    "duration_calculation": "review_completed_at_utc - review_started_at_utc",
                    "time_posture": "OBSERVED_START_AND_END_UTC",
                },
                human_adjudication="TIME_SOURCE_LIMITS",
                precision=3,
            ),
            _metric(
                "MET-024",
                value=len(provider_unavailable),
                unit="count",
                rows=provider_unavailable,
                filters={"transaction_state": "PROVIDER_UNAVAILABLE"},
            ),
            _metric(
                "MET-025",
                value=(len(revised_period_rows) if expected_revision_numbers is not None else None),
                unit="count",
                rows=revised_period_rows,
                filters={"revision_number": ">1"},
                null_count=1 if expected_revision_numbers is None else 0,
                limitations=(revision_count_limitation,),
            ),
            _metric(
                "MET-026",
                value=len(externally_signed),
                unit="count",
                rows=externally_signed,
                filters={"signature_posture": "ED25519_EXTERNAL_SIGNER", "signature_verified": True},
                limitations=("A valid signature proves bounded identity and integrity properties, not truth.",),
            ),
        ]
    )
    if [metric["metric_id"] for metric in metrics] != list(METRIC_NAMES):
        raise MetricContractError("METRIC_DICTIONARY_INCOMPLETE")
    for metric in metrics:
        metric.pop("metric_identity", None)
        metric["period_id"] = effective_period_id
        metric["period_scope"] = period_scope
        metric["unknown_period_row_count"] = unknown_period_row_count
        metric["period_revision_id"] = period_revision_id
        metric["source_population_sha256"] = metric_population_identity
        metric["metric_identity"] = sha256_bytes(canonical_bytes(metric))
    return metrics


def metrics_document(metrics: Sequence[Any]) -> dict[str, Any]:
    rows = [dict(_mapping(metric, "METRIC")) for metric in metrics]
    rows.sort(key=lambda row: str(row.get("metric_id")))
    if [row.get("metric_id") for row in rows] != list(METRIC_NAMES):
        raise MetricContractError("METRIC_DICTIONARY_INCOMPLETE")
    for row in rows:
        if set(row) != METRIC_FIELDS:
            raise MetricContractError("METRIC_FIELDS_INVALID")
        metric_id = row.get("metric_id")
        if (
            row.get("schema_id") != "uvlm.triadicbrain.aep01.period_metric.v1"
            or row.get("metric_version") != METRIC_VERSION
            or row.get("name") != METRIC_NAMES.get(str(metric_id))
            or row.get("calculation_version") != CALCULATION_VERSION
            or row.get("contains_assurance_conclusion") is not False
            or row.get("opinion_generated_or_prefilled") is not False
            or row.get("nonassurance") != NONASSURANCE_NOTICE
            or row.get("authority_effect") != AUTHORITY_EFFECT
        ):
            raise MetricContractError("METRIC_CONTRACT_INVALID")
        observed_identity = row.get("metric_identity")
        core = dict(row)
        core.pop("metric_identity", None)
        if observed_identity != sha256_bytes(canonical_bytes(core)):
            raise MetricContractError("METRIC_IDENTITY_INVALID")
        source_ids = row.get("source_row_ids")
        source_digests = row.get("source_row_digests")
        if (
            not isinstance(source_ids, list)
            or source_ids != sorted(source_ids)
            or len(source_ids) != len(set(source_ids))
            or row.get("source_row_count") != len(source_ids)
            or not isinstance(source_digests, list)
            or source_digests
            != [
                {"row_id": item.get("row_id"), "sha256": item.get("sha256")}
                for item in source_digests
                if isinstance(item, Mapping)
            ]
            or [item["row_id"] for item in source_digests] != source_ids
            or any(
                not isinstance(item.get("sha256"), str)
                or len(item["sha256"]) != 64
                or any(character not in "0123456789abcdef" for character in item["sha256"])
                for item in source_digests
            )
        ):
            raise MetricContractError("METRIC_SOURCE_DRILL_THROUGH_INVALID")
    period_ids = {row.get("period_id") for row in rows}
    period_scopes = {row.get("period_scope") for row in rows}
    unknown_period_counts = {row.get("unknown_period_row_count") for row in rows}
    revision_ids = {row.get("period_revision_id") for row in rows}
    population_ids = {row.get("source_population_sha256") for row in rows}
    if (
        len(period_ids) != 1
        or len(period_scopes) != 1
        or len(unknown_period_counts) != 1
        or len(revision_ids) != 1
        or len(population_ids) != 1
    ):
        raise MetricContractError("METRIC_REPORT_IDENTITY_MIXED")
    document = {
        "schema_id": "uvlm.triadicbrain.aep01.period_metrics.v1",
        "period_id": next(iter(period_ids)),
        "period_scope": next(iter(period_scopes)),
        "unknown_period_row_count": next(iter(unknown_period_counts)),
        "period_revision_id": next(iter(revision_ids)),
        "source_population_sha256": next(iter(population_ids)),
        "calculation_version": CALCULATION_VERSION,
        "metric_count": len(rows),
        "metrics": rows,
        "contains_compliance_score": False,
        "contains_assurance_conclusion": False,
        "opinion_generated_or_prefilled": False,
        "nonassurance": NONASSURANCE_NOTICE,
        "authority_effect": AUTHORITY_EFFECT,
    }
    document["metrics_identity"] = sha256_bytes(canonical_bytes(document))
    return document
