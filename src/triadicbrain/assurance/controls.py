"""Versioned control execution for the AI Controls Evidence Platform.

Control rows are system-generated evidence, not conclusions about compliance,
design adequacy, or operating effectiveness.  The five-value result vocabulary
is intentionally closed; inapplicability and P1 deferral are expressed as
metadata and never as a sixth, implicitly green outcome.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Mapping, Sequence
from typing import Any

from .canonical import canonical_bytes, sha256_bytes


CONTROL_VERSION = "1.0.0"
PROCEDURE_VERSION = "1.0.0"
RESULTS = ("PASS", "FAIL", "HOLD", "NOT_EXECUTED", "ERROR")

P0_CORE = (
    "AI-GOV-01",
    "AI-GOV-02",
    "AI-AUT-01",
    "AI-MOD-02",
    "AI-CFG-01",
    "AI-DAT-01",
    "AI-ING-01",
    "AI-QTN-01",
    "AI-QTN-02",
    "AI-SOD-01",
    "AI-SOD-02",
    "AI-EVD-01",
    "AI-EVD-02",
    "AI-EVD-03",
    "AI-HUM-01",
    "AI-RPR-01",
    "AI-AUD-01",
    "AI-ATL-01",
    "AI-MON-01",
    "AI-MON-02",
    "AI-EXC-01",
    "AI-ACC-01",
    "AI-BCR-01",
    "AI-SEC-01",
    "AI-REP-01",
)

P0_WHEN_APPLICABLE = (
    "AI-RSK-01",
    "AI-CFG-02",
    "AI-CFG-03",
    "AI-DAT-03",
    "AI-PRM-01",
    "AI-CLM-01",
    "AI-CLM-02",
    "AI-HUM-02",
    "AI-CHG-01",
    "AI-PRV-01",
)

P1 = (
    "AI-MOD-01",
    "AI-DAT-02",
    "AI-TIA-01",
    "AI-TIA-02",
    "AI-TPR-01",
    "AI-OSC-01",
    "AI-RET-01",
)

CONTROL_TITLES = {
    "AI-GOV-01": "Registered AI business use",
    "AI-GOV-02": "Named owners and reviewers",
    "AI-RSK-01": "Documented risk level",
    "AI-AUT-01": "Approved intake before processing",
    "AI-MOD-01": "Approved model list administration",
    "AI-MOD-02": "Model and version recorded",
    "AI-CFG-01": "Prompt and settings recorded",
    "AI-CFG-02": "Approved configuration change",
    "AI-CFG-03": "Configuration drift check",
    "AI-DAT-01": "Source data identity",
    "AI-DAT-02": "Search and retrieval history",
    "AI-DAT-03": "Data classification and permitted use",
    "AI-PRM-01": "Effective prompt record",
    "AI-ING-01": "Safe input validation",
    "AI-QTN-01": "Exact raw AI output capture",
    "AI-QTN-02": "AI output cannot bypass controls",
    "AI-CLM-01": "Claims linked to source evidence",
    "AI-CLM-02": "Unsupported claims exposed",
    "AI-TIA-01": "Optional review-profile rules",
    "AI-TIA-02": "Optional advisory repair support",
    "AI-SOD-01": "Role-based authorization",
    "AI-SOD-02": "AI cannot write control evidence",
    "AI-EVD-01": "All required control results present",
    "AI-EVD-02": "Hash-linked audit history",
    "AI-EVD-03": "Finalized evidence cannot be overwritten",
    "AI-HUM-01": "Named human decision",
    "AI-HUM-02": "Override and rationale recorded",
    "AI-RPR-01": "Repair creates a separate child record",
    "AI-AUD-01": "Independent review cannot rewrite output",
    "AI-ATL-01": "Dashboard cannot grant authority",
    "AI-MON-01": "Reproducible period metrics",
    "AI-MON-02": "Complete transaction population",
    "AI-CHG-01": "Change and rollback history",
    "AI-EXC-01": "Issue and remediation lifecycle",
    "AI-TPR-01": "Provider responsibility record",
    "AI-PRV-01": "Authorized redacted views",
    "AI-ACC-01": "Independent auditor access",
    "AI-OSC-01": "Standards-format export validation",
    "AI-BCR-01": "Safe recovery after interruption",
    "AI-SEC-01": "Secrets and credentials isolated",
    "AI-RET-01": "Retention and legal-hold history",
    "AI-REP-01": "Evidence separated from assurance conclusions",
}

CONTROL_IDS = tuple(sorted((*P0_CORE, *P0_WHEN_APPLICABLE, *P1)))
if len(CONTROL_IDS) != 42 or set(CONTROL_IDS) != set(CONTROL_TITLES):
    raise RuntimeError("AEP01_CONTROL_CATALOG_INTERNAL_MISMATCH")


# These are the only P0-core facts that the transaction route can establish
# before a human decision.  They are deliberately closed and shared with the
# independent verifier: arbitrary caller-supplied prose cannot turn a P0-core
# result green merely by using an allowed reason code and recomputing hashes.
PRELIMINARY_P0_CORE_PASS_OBSERVATIONS = {
    "AI-GOV-01": "The use case and transaction were registered in the creation ledger.",
    "AI-AUT-01": "The task reached ADMITTED before input or candidate processing.",
    "AI-MOD-02": "The user-declared model identity was captured with its limitation.",
    "AI-CFG-01": "The exact prompt and settings digest inputs were captured.",
    "AI-DAT-01": "Original and normalized source identities were recorded separately.",
    "AI-ING-01": "Bounded types, sizes, identifiers, and canonical metadata were validated.",
    "AI-QTN-01": "The opaque raw candidate bytes were captured with exact size and SHA-256.",
    "AI-QTN-02": "Candidate bytes were not parsed as authoritative control evidence.",
    "AI-SOD-01": "The closed role/action authorization matrix was applied.",
    "AI-SOD-02": "The model-adapter role has no control-result or decision write permission.",
    "AI-EVD-01": "One explicit result was created for every catalogued control.",
    "AI-EVD-02": "The transaction custody history is monotonic and hash linked.",
    "AI-EXC-01": "Negative control results are projected to open issue records.",
}
if not set(PRELIMINARY_P0_CORE_PASS_OBSERVATIONS).issubset(P0_CORE):
    raise RuntimeError("PRELIMINARY_P0_CORE_OBSERVATION_SET_INVALID")


def preliminary_platform_observations(
    *, candidate_captured: bool,
) -> dict[str, dict[str, Any]]:
    """Return the closed predecision P0-core observations for a known route."""

    if type(candidate_captured) is not bool:
        raise ControlError("CANDIDATE_CAPTURE_POSTURE_BOOL_REQUIRED")
    observed = dict(PRELIMINARY_P0_CORE_PASS_OBSERVATIONS)
    if not candidate_captured:
        observed.pop("AI-QTN-01", None)
    return {
        control_id: {
            "observed_condition": reason,
            "reason_codes": ["AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"],
            "result": "PASS",
        }
        for control_id, reason in observed.items()
    }


class ControlError(ValueError):
    """A control execution request failed its closed local contract."""


def delivery_tier(control_id: str) -> str:
    if control_id in P0_CORE:
        return "P0_CORE"
    if control_id in P0_WHEN_APPLICABLE:
        return "P0_WHEN_APPLICABLE"
    if control_id in P1:
        return "P1"
    raise ControlError("UNKNOWN_CONTROL_ID")


def catalog_rows() -> list[dict[str, Any]]:
    """Return the effective v1.1 control-delivery catalog in stable order."""

    return [
        {
            "control_id": control_id,
            "control_version": CONTROL_VERSION,
            "delivery_tier": delivery_tier(control_id),
            "display_name": CONTROL_TITLES[control_id],
            "nonauthority": (
                "This control definition and its execution record do not establish "
                "compliance, design adequacy, or operating effectiveness."
            ),
        }
        for control_id in CONTROL_IDS
    ]


def render_control_catalog_csv() -> bytes:
    """Render the exact catalog snapshot embedded in evidence packages."""

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=[
            "control_id",
            "control_version",
            "delivery_tier",
            "display_name",
            "nonauthority",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(catalog_rows())
    return buffer.getvalue().encode("utf-8")


def render_framework_crosswalk_csv() -> bytes:
    """Render the bounded, explicitly proposed generic crosswalk snapshot."""

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(
        ["control_id", "framework", "relationship", "status", "limitation"]
    )
    for control_id in CONTROL_IDS:
        writer.writerow(
            [
                control_id,
                "GENERIC_AI_CONTROL_DOMAIN",
                "PROPOSED_CONTEXTUAL_MAPPING",
                "PROPOSED",
                "Not regulator, standards-body, auditor, or certifier approval.",
            ]
        )
    return buffer.getvalue().encode("utf-8")


def _default_observation(
    control_id: str,
    applicable_controls: set[str],
) -> tuple[str, bool, str, list[str]]:
    tier = delivery_tier(control_id)
    if tier == "P1":
        return (
            "NOT_EXECUTED",
            False,
            "P1 feature is outside the effective AEP01 P0 route.",
            ["P1_DEFERRED_NOT_EXECUTED"],
        )
    if tier == "P0_WHEN_APPLICABLE" and control_id not in applicable_controls:
        return (
            "NOT_EXECUTED",
            False,
            "The versioned applicability condition was not activated.",
            ["NOT_APPLICABLE_RECORDED_AS_NOT_EXECUTED"],
        )
    return (
        "NOT_EXECUTED",
        True,
        "No authenticated procedure observation was supplied for this control.",
        ["PROCEDURE_OBSERVATION_NOT_SUPPLIED"],
    )


def execute_controls(
    *,
    transaction_id: str,
    period_id: str,
    evidence_refs: Sequence[Mapping[str, Any]],
    applicable_controls: Sequence[str] = (),
    overrides: Mapping[str, Mapping[str, Any]] | None = None,
    observed_time_utc: str | None = None,
) -> list[dict[str, Any]]:
    """Execute the effective catalog and return one explicit result per control.

    ``overrides`` is an internal test/pilot condition projection, not a way for
    candidate/model bytes to write results.  Callers must construct it from
    admitted platform state, never by parsing the candidate as control JSON.
    """

    if not isinstance(transaction_id, str) or not transaction_id:
        raise ControlError("INVALID_TRANSACTION_ID")
    if not isinstance(period_id, str) or not period_id:
        raise ControlError("INVALID_PERIOD_ID")
    applicable = set(applicable_controls)
    if not applicable.issubset(P0_WHEN_APPLICABLE):
        raise ControlError("INVALID_APPLICABILITY_SET")
    supplied = dict(overrides or {})
    if not set(supplied).issubset(CONTROL_IDS):
        raise ControlError("UNKNOWN_CONTROL_OVERRIDE")
    rows: list[dict[str, Any]] = []
    for sequence, control_id in enumerate(CONTROL_IDS, 1):
        result, applicable_value, observation, reasons = _default_observation(
            control_id, applicable
        )
        if control_id in supplied:
            override = supplied[control_id]
            if not isinstance(override, Mapping):
                raise ControlError("CONTROL_OVERRIDE_OBJECT_REQUIRED")
            allowed = {"result", "observed_condition", "reason_codes", "exception_ids"}
            if set(override) - allowed:
                raise ControlError("CONTROL_OVERRIDE_FIELDS_INVALID")
            requested_result = override.get("result", result)
            if control_id in P1 and requested_result != "NOT_EXECUTED":
                raise ControlError("P1_CONTROL_RESULT_MUST_BE_NOT_EXECUTED")
            if (
                control_id in P0_WHEN_APPLICABLE
                and control_id not in applicable
                and requested_result != "NOT_EXECUTED"
            ):
                raise ControlError("INAPPLICABLE_CONTROL_RESULT_MUST_BE_NOT_EXECUTED")
            if "observed_condition" not in override or "reason_codes" not in override:
                raise ControlError("CONTROL_OVERRIDE_OBSERVATION_REQUIRED")
            supplied_observation = override["observed_condition"]
            supplied_reasons = override["reason_codes"]
            if (
                type(supplied_observation) is not str
                or not supplied_observation.strip()
                or isinstance(supplied_reasons, (str, bytes))
                or not isinstance(supplied_reasons, Sequence)
                or not supplied_reasons
                or any(type(item) is not str or not item for item in supplied_reasons)
                or len(supplied_reasons) != len(set(supplied_reasons))
            ):
                raise ControlError("CONTROL_OVERRIDE_OBSERVATION_INVALID")
            if requested_result == "PASS" and control_id in P0_CORE:
                expected_observation = PRELIMINARY_P0_CORE_PASS_OBSERVATIONS.get(
                    control_id
                )
                if (
                    supplied_observation != expected_observation
                    or list(supplied_reasons)
                    != ["AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"]
                ):
                    raise ControlError("P0_CORE_PASS_NOT_PLATFORM_DERIVED")
            result = requested_result
            observation = supplied_observation
            reasons = list(supplied_reasons)
        if result not in RESULTS:
            raise ControlError("CONTROL_RESULT_INVALID")
        exception_value = supplied.get(control_id, {}).get("exception_ids", ())
        if isinstance(exception_value, (str, bytes)) or not isinstance(
            exception_value, Sequence
        ):
            raise ControlError("CONTROL_OVERRIDE_EXCEPTION_IDS_INVALID")
        exceptions = list(exception_value)
        if (
            any(type(item) is not str or not item for item in exceptions)
            or len(exceptions) != len(set(exceptions))
        ):
            raise ControlError("CONTROL_OVERRIDE_EXCEPTION_IDS_INVALID")
        row: dict[str, Any] = {
            "actor_id": "SERVICE-CONTROL-EXECUTOR",
            "authority_effect": "NONE",
            "canonical_result_sha256": "",
            "control_id": control_id,
            "control_type": "detective",
            "control_version": CONTROL_VERSION,
            "evidence_refs": [dict(reference) for reference in evidence_refs],
            "exceptions": exceptions,
            "execution_id": f"CEX-{transaction_id}-{sequence:03d}",
            "expected_condition": {
                "applicability": "APPLICABLE" if applicable_value else (
                    "P1_DEFERRED" if control_id in P1 else "NOT_APPLICABLE"
                ),
                "condition": "The versioned bounded control condition is met.",
                "delivery_tier": delivery_tier(control_id),
                "population_subject": transaction_id,
                "trigger": "TRANSACTION_CONTROL_EXECUTION",
            },
            "frequency": "ON_EACH_TRANSACTION",
            "human_judgment_required": control_id in {"AI-GOV-02", "AI-HUM-01", "AI-HUM-02"},
            "method": "automated",
            "observed_condition": observation,
            "observed_time_utc": observed_time_utc,
            "period_id": period_id,
            "plane": "CONTROL_EVIDENCE",
            "procedure_id": f"PROC-{control_id}-001",
            "procedure_version": PROCEDURE_VERSION,
            "reason_codes": reasons,
            "result": result,
            "schema_id": "uvlm.triadicbrain.aep01.control_execution_result.v1",
            "sequence": sequence,
            "side_effects": {
                "memory_written": False,
                "network_used": False,
                "provider_invoked": False,
            },
            "superseded": False,
            "transaction_id": transaction_id,
        }
        row["canonical_result_sha256"] = sha256_bytes(
            canonical_bytes({**row, "canonical_result_sha256": None})
        )
        rows.append(row)
    if len(rows) != 42 or [row["control_id"] for row in rows] != list(CONTROL_IDS):
        raise ControlError("CONTROL_RESULT_COMPLETENESS_FAILED")
    return rows


def summarize_results(rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts = {name: 0 for name in RESULTS}
    seen: set[str] = set()
    for row in rows:
        control_id = row.get("control_id")
        result = row.get("result")
        if control_id not in CONTROL_IDS or control_id in seen or result not in counts:
            raise ControlError("CONTROL_RESULT_SET_INVALID")
        seen.add(str(control_id))
        counts[str(result)] += 1
    if seen != set(CONTROL_IDS):
        raise ControlError("CONTROL_RESULT_SET_INCOMPLETE")
    return counts
