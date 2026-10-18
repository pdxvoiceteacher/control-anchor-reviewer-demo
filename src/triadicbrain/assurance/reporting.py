"""Deterministic report and export artifacts for a closed AEP01 period.

These helpers create derived, read-only evidence projections.  They never call
an AI provider, modify canonical transaction evidence, prefill a management or
practitioner conclusion, or grant runtime authority.
"""

from __future__ import annotations

import csv
import html
import io
import json
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import (
    AUTHORITY_EFFECT,
    NONASSURANCE_HEADLINE,
    NONASSURANCE_NOTICE,
    PRODUCT_NAME,
    REPORT_NOTICE,
    VERSION,
)
from .canonical import (
    canonical_bytes,
    read_canonical_file,
    require_existing_root,
    require_single_link_file,
    sha256_bytes,
    strict_load_object,
)


MANAGEMENT_REPRESENTATION_NOTICE = (
    "MANAGEMENT-PREPARED OR MANAGEMENT-ADOPTED REPRESENTATION\n"
    "HUMAN IDENTITY AND APPROVAL REQUIRED"
)
PRACTITIONER_WORK_PRODUCT_NOTICE = (
    "INDEPENDENT PRACTITIONER WORK PRODUCT\n"
    "NOT AUTHORED, APPROVED, OR ISSUED BY CONTROL ANCHOR"
)
ZERO_REPORT_EFFECTS = {
    "canonical_evidence_written": False,
    "deployment_performed": False,
    "memory_written": False,
    "network_used": False,
    "provider_invoked": False,
    "publication_performed": False,
}
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
_CLOSURE_FILES = {
    "PERIOD_PACKAGE_MANIFEST.json",
    "SHA256SUMS.txt",
    "VERIFICATION_RECEIPT.json",
}


class ReportingError(ValueError):
    """A report/export could not be created or verified truthfully."""


def report_boundary() -> dict[str, Any]:
    """Return the exact, reusable nonassurance boundary for derived outputs."""

    return {
        "authority_effect": AUTHORITY_EFFECT,
        "contains_assurance_conclusion": False,
        "effects": dict(ZERO_REPORT_EFFECTS),
        "nonauthority": NONASSURANCE_NOTICE,
        "opinion_generated_or_prefilled": False,
        "report_notice": REPORT_NOTICE,
        "system_evidence_headline": NONASSURANCE_HEADLINE,
    }


def report_document(
    schema_id: str,
    rows_name: str,
    rows: Sequence[Mapping[str, Any]],
    **fields: Any,
) -> dict[str, Any]:
    """Build a bounded report envelope with the mandatory exact notice."""

    result = {
        "schema_id": schema_id,
        rows_name: [dict(row) for row in rows],
        "count": len(rows),
        "nonauthority": NONASSURANCE_NOTICE,
        **report_boundary(),
        **fields,
    }
    return result


def report_csv_bytes(
    rows: Sequence[Mapping[str, Any]],
    fieldnames: Sequence[str],
) -> bytes:
    """Render a stable CSV whose every data row carries both required labels."""

    names = [str(name) for name in fieldnames]
    if len(names) != len(set(names)) or any(not name for name in names):
        raise ReportingError("CSV_FIELDNAMES_INVALID")
    boundary_names = [
        "system_evidence_headline",
        "report_notice",
        "authority_effect",
    ]
    names = [name for name in names if name not in boundary_names] + boundary_names
    source_rows = [dict(row) for row in rows]
    if not source_rows:
        source_rows = {name: "" for name in names}
        source_rows = [source_rows | {"record_status": "NO_ROWS"}]
        if "record_status" not in names:
            names.insert(0, "record_status")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=names, lineterminator="\n")
    writer.writeheader()
    for source in source_rows:
        rendered: dict[str, str] = {}
        for name in names:
            value = source.get(name)
            if isinstance(value, (dict, list)):
                rendered[name] = canonical_bytes(value).decode("utf-8").rstrip("\n")
            elif value is True:
                rendered[name] = "true"
            elif value is False:
                rendered[name] = "false"
            elif value is None:
                rendered[name] = ""
            else:
                rendered[name] = str(value)
        rendered["system_evidence_headline"] = NONASSURANCE_HEADLINE
        rendered["report_notice"] = REPORT_NOTICE
        rendered["authority_effect"] = AUTHORITY_EFFECT
        writer.writerow(rendered)
    return stream.getvalue().encode("utf-8")


def report_jsonl_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    """Render report rows as canonical JSON Lines with the exact notice."""

    return b"".join(
        canonical_bytes(
            dict(row)
            | {
                "authority_effect": AUTHORITY_EFFECT,
                "report_notice": REPORT_NOTICE,
                "system_evidence_headline": NONASSURANCE_HEADLINE,
            }
        )
        for row in rows
    )


def render_transaction_review_html(
    *,
    transaction_id: str,
    business_state: str,
    open_findings: Sequence[Mapping[str, Any]],
    product_name: str = PRODUCT_NAME,
) -> bytes:
    """Render the canonical, deterministic transaction review HTML.

    Transaction finalization and independent verification call this same pure
    function so a report cannot pass verification using a weaker duplicate
    template.  Supplied finding text is escaped and no script is emitted.
    """

    if not transaction_id or not business_state or not product_name:
        raise ReportingError("TRANSACTION_REVIEW_IDENTITY_INVALID")
    findings = [dict(row) for row in open_findings]
    finding_items = "".join(
        "<li><code>"
        + html.escape(str(row.get("finding_id", "UNKNOWN")))
        + "</code> — "
        + html.escape(str(row.get("finding_class", "UNKNOWN")))
        + " — "
        + html.escape(str(row.get("status", "UNKNOWN")))
        + " — "
        + html.escape(str(row.get("summary", "No additional summary recorded.")))
        + "</li>"
        for row in findings
    )
    approval_resolution_notice = (
        "<p><strong>Approval did not close or resolve the open advisory findings. "
        "They remain visible, addressable, exportable, and bound to this evidence package.</strong></p>"
        if business_state == "APPROVE" and findings
        else ""
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>"
        + html.escape(product_name)
        + " transaction review</title></head><body><header><p><strong>"
        + html.escape(NONASSURANCE_HEADLINE)
        + "</strong></p><p><strong>"
        + html.escape(REPORT_NOTICE)
        + "</strong></p></header><main><h1>AI workflow evidence</h1><dl><dt>Transaction</dt><dd>"
        + html.escape(transaction_id)
        + "</dd><dt>State</dt><dd>"
        + html.escape(business_state)
        + "</dd><dt>Provider invoked</dt><dd>No</dd><dt>Authority effect</dt><dd>NONE</dd></dl>"
        + "<h2>Open findings ("
        + str(len(findings))
        + ")</h2><ul>"
        + finding_items
        + "</ul>"
        + approval_resolution_notice
        + "<p>This review does not decide criteria, materiality, scope, evidence sufficiency, control effectiveness, compliance, or an audit opinion.</p></main></body></html>\n"
    ).encode("utf-8")


def management_representation_template(
    *,
    period_id: str,
    evidence_package_sha256: str,
    known_exception_ids: Sequence[str],
) -> dict[str, Any]:
    """Return an unadopted supplied-v1 management template.

    Required human-owned fields remain explicit placeholders.  No assertion,
    criteria selection, approval, identity authentication, or signature is
    fabricated by the product.
    """

    if not re.fullmatch(r"[0-9a-f]{64}", evidence_package_sha256):
        raise ReportingError("MANAGEMENT_TEMPLATE_EVIDENCE_DIGEST_INVALID")
    return {
        "schema_id": "uvlm.triadicbrain.aep01.management_representation.v1",
        "representation_id": f"MGMT-REP-TEMPLATE-{period_id}",
        "organization": {"name": "[MANAGEMENT MUST COMPLETE]"},
        "responsible_person": {
            "actor_id": "[HUMAN MUST COMPLETE]",
            "authentication_posture": "NOT_AUTHENTICATED_TEMPLATE_ONLY",
            "name": "[HUMAN MUST COMPLETE]",
            "role": "[HUMAN MUST COMPLETE]",
        },
        "period_id": period_id,
        "scope": "[MANAGEMENT MUST DEFINE AND ADOPT SCOPE]",
        "criteria_references": [],
        "assertions": [],
        "known_exceptions": sorted(set(known_exception_ids)),
        "evidence_package_sha256": evidence_package_sha256,
        "adoption_status": "DRAFT",
        "signature_posture": "UNSIGNED",
        "nonauthority": MANAGEMENT_REPRESENTATION_NOTICE + "\n" + REPORT_NOTICE,
        "authority_effect": "MANAGEMENT_REPRESENTATION_ONLY",
    }


def _metadata_rows(
    store_root: Path,
    transaction_records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in sorted(transaction_records, key=lambda row: str(row.get("transaction_id"))):
        transaction_id = str(record.get("transaction_id", ""))
        metadata = read_canonical_file(
            Path(store_root) / "transactions" / transaction_id / "transaction.json"
        )
        rows.append(
            {
                "transaction_id": transaction_id,
                "system_id": metadata.get("system_id"),
                "use_case_id": metadata.get("use_case_id"),
                "model_identity": metadata.get("model_identity"),
                "model_identity_posture": "USER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
                "invocation_mode": "CAPTURED_OUTPUT",
                "provider_invoked": False,
                "settings": metadata.get("settings"),
                "prompt_sha256": sha256_bytes(str(metadata.get("prompt", "")).encode("utf-8")),
                "source_sha256": metadata.get("source_sha256"),
                "candidate_sha256": metadata.get("candidate_sha256"),
            }
        )
    return rows


def build_period_output_payloads(
    *,
    store_root: Path,
    period_revision: Mapping[str, Any],
    population_rows: Sequence[Mapping[str, Any]],
    transaction_records: Sequence[Mapping[str, Any]],
    control_rows: Sequence[Mapping[str, Any]],
    finding_rows: Sequence[Mapping[str, Any]],
    decision_rows: Sequence[Mapping[str, Any]],
    repair_lineage_rows: Sequence[Mapping[str, Any]],
    package_rows: Sequence[Mapping[str, Any]],
    reconciliation: Mapping[str, Any],
    metrics: Mapping[str, Any],
    practitioner_index: Mapping[str, Any],
    control_delivery_status: Sequence[Mapping[str, Any]],
    deferred_features: Sequence[Mapping[str, Any]],
    predecision_control_rows: Sequence[Mapping[str, Any]] = (),
    lifecycle_rows: Sequence[Mapping[str, Any]] = (),
    current_control_rows: Sequence[Mapping[str, Any]] = (),
    lifecycle_coverage_status: Mapping[str, Any] | None = None,
    effective_negative_control_rows: Sequence[Mapping[str, Any]] = (),
) -> dict[str, bytes]:
    """Build the commissioned flat period/report artifact set in memory."""

    revision = dict(period_revision)
    period_id = str(revision.get("period_id", ""))
    if not period_id:
        raise ReportingError("PERIOD_ID_MISSING")
    metadata_rows = _metadata_rows(Path(store_root), transaction_records)
    finding_ids = [
        str(row.get("finding_id"))
        for row in finding_rows
        if isinstance(row.get("finding_id"), str)
    ]
    evidence_binding = sha256_bytes(
        canonical_bytes(
            {
                "package_roots": sorted(
                    str(row.get("package_root_sha256")) for row in package_rows
                ),
                "period_revision_identity": revision.get("revision_identity"),
                "population_identity": revision.get("population_identity"),
            }
        )
    )
    scope = {
        "schema_id": "uvlm.triadicbrain.aep01.period_scope_and_criteria.v1",
        "period_id": period_id,
        "period_revision_id": revision.get("revision_id"),
        "scope_status": "SYNTHETIC_PILOT_SCOPE_DECLARED",
        "scope": "Deterministic synthetic captured-output pilot population only.",
        "criteria_selection_status": "MANAGEMENT_INPUT_REQUIRED_NOT_DETERMINED_BY_PRODUCT",
        "criteria_references": [],
        "materiality_status": "NOT_DETERMINED",
        "evidence_sufficiency_status": "NOT_DETERMINED",
        "control_effectiveness_status": "NOT_DETERMINED",
        **report_boundary(),
    }
    control_summary = report_document(
        "uvlm.triadicbrain.aep01.period_control_summary_report.v1",
        "control_summary_records",
        [dict(revision.get("period_control_summary_v1", {}))],
        period_id=period_id,
        supplied_v1_projection_path="PERIOD_CONTROL_SUMMARY_SUPPLIED_V1.json",
    )
    exceptions = report_document(
        "uvlm.triadicbrain.aep01.period_exceptions_report.v1",
        "findings_and_exceptions",
        finding_rows,
        period_id=period_id,
        open_exception_count=sum(
            str(row.get("status", "OPEN")).upper() in {"OPEN", "HELD", "UNRESOLVED"}
            for row in finding_rows
        ),
    )
    activity = report_document(
        "uvlm.triadicbrain.aep01.period_activity_report.v1",
        "transactions",
        population_rows,
        period_id=period_id,
        period_revision_id=revision.get("revision_id"),
        population_identity=revision.get("population_identity"),
    )
    status_counts = Counter(str(row.get("result", "UNKNOWN")) for row in control_rows)
    summary = {
        "schema_id": "uvlm.triadicbrain.aep01.period_summary.v1",
        "period_id": period_id,
        "period_revision_id": revision.get("revision_id"),
        "population_counts": revision.get("population_counts"),
        "control_result_counts": dict(sorted(status_counts.items())),
        "finding_count": len(finding_rows),
        "reconciliation_status": reconciliation.get("status"),
        **report_boundary(),
    }
    management_template = management_representation_template(
        period_id=period_id,
        evidence_package_sha256=evidence_binding,
        known_exception_ids=finding_ids,
    )
    p1_status = {
        "schema_id": "uvlm.triadicbrain.aep01.deferred_machine_export_status.v1",
        "status": "NOT_EXECUTED",
        "record_kind": "DEFERRED_FEATURE_STATUS_NOT_AN_OSCAL_DOCUMENT",
        "reason": "OSCAL export and validation are P1 under the controlling v1.1.0 commission.",
        **report_boundary(),
    }
    practitioner = {
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_evidence_index_report.v1",
        "practitioner_work_product_notice": PRACTITIONER_WORK_PRODUCT_NOTICE,
        "index": dict(practitioner_index),
        **report_boundary(),
    }
    investor = {
        "schema_id": "uvlm.triadicbrain.aep01.investor_walkthrough.v1",
        "product_name": PRODUCT_NAME,
        "product_version": VERSION,
        "category": "AI controls evidence and audit-readiness software",
        "plain_language_workflow": [
            "Data intake",
            "AI execution or imported output",
            "Secure output capture",
            "Automated control checks",
            "Independent review",
            "Human approval workflow",
            "Evidence finalization",
            "Period reporting and auditor access",
        ],
        "observed_pilot_facts": {
            "captured_or_imported_output_only": True,
            "complete_population_count": len(population_rows),
            "provider_invoked": False,
            "reconciliation_status": reconciliation.get("status"),
            "transaction_package_count": len(package_rows),
        },
        "prohibited_claims_made": [],
        **report_boundary(),
    }
    investor_html = _simple_html(
        "Plain-language investor walkthrough",
        [
            ("What this is", "AI controls evidence and audit-readiness software."),
            (
                "What ran",
                f"A deterministic synthetic population of {len(population_rows)} records using captured or imported output; no provider was invoked.",
            ),
            (
                "What was produced",
                f"{len(package_rows)} transaction evidence packages and a period reconciliation with status {reconciliation.get('status')}.",
            ),
            (
                "What this does not mean",
                "No compliance, control-effectiveness, audit, certification, or assurance conclusion is provided.",
            ),
        ],
    )
    period_html = _period_html(period_id, population_rows, control_rows, finding_rows)

    access_rows = [
        {
            "role": role,
            "access_posture": posture,
            "observed_operating_system_separation": False,
            "register_status": "DECLARED_LOGICAL_PERMISSION_MODEL",
        }
        for role, posture in (
            ("AI output importer", "QUARANTINE_WRITE_ONLY"),
            ("Control executor", "CONTROL_RESULT_WRITE_ONLY"),
            ("Independent reviewer", "FINDING_WRITE_ONLY"),
            ("Human reviewer", "DECISION_WRITE_ONLY"),
            ("Reporting view", "CANONICAL_EVIDENCE_READ_ONLY"),
            ("Practitioner", "CANONICAL_READ_ONLY_SEPARATE_ANNOTATION_DOMAIN"),
        )
    ]
    change_rows = [
        {
            "transaction_id": row["transaction_id"],
            "configuration_sha256": sha256_bytes(
                canonical_bytes(
                    {
                        "model_identity": row["model_identity"],
                        "prompt_sha256": row["prompt_sha256"],
                        "settings": row["settings"],
                    }
                )
            ),
            "scenario": next(
                (
                    source.get("scenario")
                    for source in transaction_records
                    if source.get("transaction_id") == row["transaction_id"]
                ),
                None,
            ),
            "change_posture": "TRANSACTION_BOUND_CONFIGURATION_SNAPSHOT",
        }
        for row in metadata_rows
    ]
    incident_rows = [
        {
            "finding_id": row.get("finding_id"),
            "transaction_id": row.get("transaction_id"),
            "finding_class": row.get("finding_class"),
            "status": row.get("status"),
            "owner": row.get("owner"),
            "resolution": row.get("resolution"),
            "repair_lineage_present": any(
                row.get("finding_id") in lineage.get("selected_finding_ids", [])
                for lineage in repair_lineage_rows
            ),
        }
        for row in finding_rows
    ]
    metrics_report = dict(metrics) | report_boundary()
    reconciliation_report = dict(reconciliation) | report_boundary()
    delivery_report = report_document(
        "uvlm.triadicbrain.aep01.control_delivery_status.v1",
        "controls",
        control_delivery_status,
        period_id=period_id,
    )
    deferred_report = report_document(
        "uvlm.triadicbrain.aep01.deferred_feature_register.v1",
        "features",
        deferred_features,
        period_id=period_id,
        all_nonexecuted=all(
            row.get("status") in {"NOT_EXECUTED", "DEFERRED"}
            for row in deferred_features
        ),
    )
    decision_report = report_document(
        "uvlm.triadicbrain.aep01.human_decision_register.v1",
        "decisions",
        decision_rows,
        period_id=period_id,
    )
    repair_report = report_document(
        "uvlm.triadicbrain.aep01.repair_lineage_register.v1",
        "repair_lineages",
        repair_lineage_rows,
        period_id=period_id,
    )
    offline = {
        "schema_id": "uvlm.triadicbrain.aep01.offline_verification_instructions.v1",
        "period_id": period_id,
        "requires_ai_model": False,
        "requires_network": False,
        "procedure": [
            "Read PERIOD_PACKAGE_MANIFEST.json without executing report content.",
            "Recompute SHA-256 for every declared member.",
            "Compare the exact member set and SHA256SUMS.txt entries.",
            "Run the local exact period verifier and retain its receipt.",
        ],
        **report_boundary(),
    }
    predecision_report = report_document(
        "uvlm.triadicbrain.aep01.predecision_control_execution_population.v1",
        "control_executions",
        predecision_control_rows,
        period_id=period_id,
        immutable_source_posture="RETAINED_WITHOUT_PROMOTION_OR_REWRITE",
    )
    lifecycle_report = report_document(
        "uvlm.triadicbrain.aep01.control_lifecycle_ledger_report.v1",
        "lifecycle_executions",
        lifecycle_rows,
        period_id=period_id,
        append_only=True,
    )
    current_projection_report = report_document(
        "uvlm.triadicbrain.aep01.current_control_projection.v1",
        "current_control_executions",
        current_control_rows,
        period_id=period_id,
        projection_only=True,
        source_history_mutated=False,
    )
    coverage_report = dict(lifecycle_coverage_status or {}) | {
        "schema_id": "uvlm.triadicbrain.aep01.lifecycle_control_coverage_report.v1",
        "period_id": period_id,
        **report_boundary(),
    }
    negative_reconciliation = report_document(
        "uvlm.triadicbrain.aep01.effective_p0_negative_control_reconciliation.v1",
        "negative_controls",
        effective_negative_control_rows,
        period_id=period_id,
        coverage_status=(
            "COMPLETE"
            if effective_negative_control_rows
            and all(row.get("status") == "PASS" for row in effective_negative_control_rows)
            else "INCOMPLETE"
        ),
        pass_count=sum(
            row.get("status") == "PASS" for row in effective_negative_control_rows
        ),
        not_executed_count=sum(
            row.get("status") == "NOT_EXECUTED"
            for row in effective_negative_control_rows
        ),
    )

    json_outputs = {
        "PERIOD_SCOPE_AND_CRITERIA.json": scope,
        "PERIOD_ACTIVITY_REPORT.json": activity,
        "PERIOD_SUMMARY.json": summary,
        "PERIOD_CONTROL_SUMMARY.json": control_summary,
        "PERIOD_CONTROL_SUMMARY_SUPPLIED_V1.json": dict(
            revision.get("period_control_summary_v1", {})
        ),
        "PERIOD_EXCEPTIONS_REPORT.json": exceptions,
        "PERIOD_METRICS.json": metrics_report,
        "POPULATION_COMPLETENESS_RECONCILIATION.json": reconciliation_report,
        "MANAGEMENT_REPRESENTATION_TEMPLATE.json": management_template,
        "OSCAL_ASSESSMENT_PLAN_PROFILE.json": p1_status
        | {"requested_output": "OSCAL_ASSESSMENT_PLAN_PROFILE"},
        "OSCAL_ASSESSMENT_RESULTS.json": p1_status
        | {"requested_output": "OSCAL_ASSESSMENT_RESULTS"},
        "OSCAL_TRANSFORMATION_RECEIPT.json": p1_status
        | {"requested_output": "OSCAL_TRANSFORMATION_RECEIPT"},
        "PRACTITIONER_EVIDENCE_INDEX.json": practitioner,
        "HUMAN_DECISION_REGISTER.json": decision_report,
        "REPAIR_LINEAGE_REGISTER.json": repair_report,
        "PLAIN_LANGUAGE_INVESTOR_WALKTHROUGH.json": investor,
        "CONTROL_DELIVERY_STATUS.json": delivery_report,
        "DEFERRED_FEATURE_REGISTER.json": deferred_report,
        "OFFLINE_VERIFICATION_INSTRUCTIONS.json": offline,
        "PREDECISION_CONTROL_EXECUTION_POPULATION.json": predecision_report,
        "CONTROL_LIFECYCLE_LEDGER.json": lifecycle_report,
        "CURRENT_CONTROL_PROJECTION.json": current_projection_report,
        "P0_CONTROL_LIFECYCLE_COVERAGE.json": coverage_report,
        "EFFECTIVE_P0_NEGATIVE_CONTROL_RECONCILIATION.json": negative_reconciliation,
    }
    payloads = {name: canonical_bytes(value) for name, value in json_outputs.items()}
    payloads.update(
        {
            "SYSTEM_AND_MODEL_INVENTORY.csv": report_csv_bytes(
                metadata_rows,
                (
                    "transaction_id",
                    "system_id",
                    "use_case_id",
                    "model_identity",
                    "model_identity_posture",
                    "invocation_mode",
                    "provider_invoked",
                    "prompt_sha256",
                    "settings",
                    "source_sha256",
                    "candidate_sha256",
                ),
            ),
            "TRANSACTION_POPULATION.csv": report_csv_bytes(
                population_rows,
                tuple(sorted({key for row in population_rows for key in row})),
            ),
            "CONTROL_EXECUTION_POPULATION.csv": report_csv_bytes(
                control_rows,
                tuple(sorted({key for row in control_rows for key in row})),
            ),
            "PREDECISION_CONTROL_EXECUTION_POPULATION.csv": report_csv_bytes(
                predecision_control_rows,
                tuple(
                    sorted(
                        {key for row in predecision_control_rows for key in row}
                    )
                ),
            ),
            "CONTROL_LIFECYCLE_LEDGER.jsonl": report_jsonl_bytes(lifecycle_rows),
            "CURRENT_CONTROL_PROJECTION.csv": report_csv_bytes(
                current_control_rows,
                tuple(sorted({key for row in current_control_rows for key in row})),
            ),
            "EFFECTIVE_P0_NEGATIVE_CONTROL_RECONCILIATION.csv": report_csv_bytes(
                effective_negative_control_rows,
                tuple(
                    sorted(
                        {
                            key
                            for row in effective_negative_control_rows
                            for key in row
                        }
                    )
                ),
            ),
            "FINDING_AND_EXCEPTION_POPULATION.csv": report_csv_bytes(
                finding_rows,
                tuple(sorted({key for row in finding_rows for key in row})),
            ),
            "CHANGE_AND_CONFIGURATION_REGISTER.csv": report_csv_bytes(
                change_rows,
                ("transaction_id", "configuration_sha256", "scenario", "change_posture"),
            ),
            "ACCESS_AND_PRIVILEGE_REGISTER.csv": report_csv_bytes(
                access_rows,
                (
                    "role",
                    "access_posture",
                    "observed_operating_system_separation",
                    "register_status",
                ),
            ),
            "INCIDENT_AND_REMEDIATION_REGISTER.csv": report_csv_bytes(
                incident_rows,
                (
                    "finding_id",
                    "transaction_id",
                    "finding_class",
                    "status",
                    "owner",
                    "resolution",
                    "repair_lineage_present",
                ),
            ),
            "PERIOD_REPORT.html": period_html,
            "PLAIN_LANGUAGE_INVESTOR_WALKTHROUGH.html": investor_html,
        }
    )
    return dict(sorted(payloads.items()))


def _simple_html(title: str, sections: Sequence[tuple[str, str]]) -> bytes:
    section_html = "".join(
        f"<section><h2>{html.escape(heading)}</h2><p>{html.escape(text)}</p></section>"
        for heading, text in sections
    )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)} · {html.escape(PRODUCT_NAME)}</title></head>"
        f"<body><header><p>{html.escape(NONASSURANCE_HEADLINE)}</p>"
        f"<p><strong>{html.escape(REPORT_NOTICE)}</strong></p><h1>{html.escape(title)}</h1>"
        "</header><main>" + section_html
        + "<p>Authority effect: NONE. Provider invoked: false. Network used: false.</p>"
        "</main></body></html>\n"
    ).encode("utf-8")


def _period_html(
    period_id: str,
    population_rows: Sequence[Mapping[str, Any]],
    control_rows: Sequence[Mapping[str, Any]],
    finding_rows: Sequence[Mapping[str, Any]],
) -> bytes:
    rows = "".join(
        "<tr>"
        f"<td><a href=\"../../../packages/{html.escape(str(row.get('transaction_id')), quote=True)}/18_HUMAN_READABLE_REVIEW.html\">{html.escape(str(row.get('transaction_id')))}</a></td>"
        f"<td>{html.escape(str(row.get('transaction_state')))}</td>"
        f"<td>{html.escape(str(row.get('human_decision')))}</td>"
        f"<td>{html.escape(str(row.get('adverse')))}</td>"
        "</tr>"
        for row in population_rows
    )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Period AI activity report · {html.escape(PRODUCT_NAME)}</title>"
        "<style>body{font:16px/1.5 system-ui;max-width:72rem;margin:auto;padding:1rem}"
        "table{border-collapse:collapse;width:100%}th,td{border:1px solid #777;padding:.5rem;text-align:left}"
        "a:focus{outline:3px solid #b45f06;outline-offset:2px}</style></head><body>"
        f"<header><p>{html.escape(NONASSURANCE_HEADLINE)}</p><p><strong>{html.escape(REPORT_NOTICE)}</strong></p>"
        f"<h1>Period AI activity report: {html.escape(period_id)}</h1></header><main>"
        f"<p>Complete population: {len(population_rows)} transactions. Control executions: {len(control_rows)}. Findings and exceptions: {len(finding_rows)}.</p>"
        "<table><caption>Complete transaction population with package drill-through</caption>"
        "<thead><tr><th>Transaction</th><th>State</th><th>Human decision</th><th>Adverse</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "<p>Raw JSON/JSONL/CSV exports, independent sampling, and verification are available in the adjacent practitioner and period artifacts.</p>"
        "</main></body></html>\n"
    ).encode("utf-8")


def build_period_package_manifest(period_root: Path) -> dict[str, Any]:
    """Inventory every existing ordinary core member in one flat period root."""

    root = require_existing_root(Path(period_root))
    members: list[dict[str, Any]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.name in _CLOSURE_FILES:
            continue
        if not _SAFE_NAME.fullmatch(path.name):
            raise ReportingError(f"PERIOD_MEMBER_NAME_INVALID:{path.name}")
        member = require_single_link_file(path)
        payload = member.read_bytes()
        members.append(
            {
                "bytes": len(payload),
                "path": path.name,
                "sha256": sha256_bytes(payload),
            }
        )
    if not members:
        raise ReportingError("PERIOD_PACKAGE_EMPTY")
    core = {
        "schema_id": "uvlm.triadicbrain.aep01.period_package_manifest.v1",
        "manifest_profile": "FLAT_EXACT_MEMBER_SET_SHA256_V1",
        "members": members,
        "member_count": len(members),
        "closure_files_excluded_to_avoid_self_reference": sorted(_CLOSURE_FILES),
        "nonauthority": NONASSURANCE_NOTICE,
        **report_boundary(),
    }
    core["package_root_sha256"] = sha256_bytes(canonical_bytes(members))
    return core


def build_sha256s(period_root: Path, manifest: Mapping[str, Any]) -> bytes:
    """Build exact checksum text for manifest members plus the manifest."""

    root = require_existing_root(Path(period_root))
    names = [str(row["path"]) for row in manifest.get("members", [])]
    names.append("PERIOD_PACKAGE_MANIFEST.json")
    lines = [f"# {REPORT_NOTICE}\n"]
    for name in sorted(names):
        if not _SAFE_NAME.fullmatch(name):
            raise ReportingError("CHECKSUM_MEMBER_NAME_INVALID")
        payload = require_single_link_file(root / name).read_bytes()
        lines.append(f"{sha256_bytes(payload)}  {name}\n")
    return "".join(lines).encode("utf-8")


def verify_period_output_directory(period_root: Path) -> dict[str, Any]:
    """Verify a period artifact directory offline without executing content."""

    root = require_existing_root(Path(period_root))
    manifest = read_canonical_file(root / "PERIOD_PACKAGE_MANIFEST.json")
    if (
        manifest.get("schema_id")
        != "uvlm.triadicbrain.aep01.period_package_manifest.v1"
        or manifest.get("report_notice") != REPORT_NOTICE
        or manifest.get("authority_effect") != AUTHORITY_EFFECT
        or set(manifest.get("effects", {}).values()) != {False}
    ):
        raise ReportingError("PERIOD_MANIFEST_BOUNDARY_INVALID")
    rows = manifest.get("members")
    if not isinstance(rows, list) or manifest.get("member_count") != len(rows):
        raise ReportingError("PERIOD_MANIFEST_MEMBERS_INVALID")
    names = [str(row.get("path")) for row in rows if isinstance(row, Mapping)]
    if names != sorted(names) or len(names) != len(set(names)):
        raise ReportingError("PERIOD_MANIFEST_MEMBER_ORDER_INVALID")
    observed_names = sorted(
        path.name
        for path in root.iterdir()
        if path.name not in _CLOSURE_FILES
    )
    if names != observed_names:
        raise ReportingError("PERIOD_MANIFEST_EXACT_MEMBER_SET_MISMATCH")
    for row in rows:
        name = str(row.get("path"))
        if not _SAFE_NAME.fullmatch(name):
            raise ReportingError("PERIOD_MEMBER_NAME_INVALID")
        payload = require_single_link_file(root / name).read_bytes()
        if row.get("bytes") != len(payload) or row.get("sha256") != sha256_bytes(payload):
            raise ReportingError(f"PERIOD_MEMBER_IDENTITY_MISMATCH:{name}")
        if name != "PERIOD_CONTROL_SUMMARY_SUPPLIED_V1.json" and REPORT_NOTICE.encode("utf-8") not in payload:
            raise ReportingError(f"PERIOD_REPORT_NOTICE_MISSING:{name}")
    if manifest.get("package_root_sha256") != sha256_bytes(canonical_bytes(rows)):
        raise ReportingError("PERIOD_PACKAGE_ROOT_MISMATCH")
    checksum_payload = require_single_link_file(root / "SHA256SUMS.txt").read_bytes()
    expected_checksum = build_sha256s(root, manifest)
    if checksum_payload != expected_checksum:
        raise ReportingError("PERIOD_CHECKSUM_FILE_MISMATCH")
    return {
        "schema_id": "uvlm.triadicbrain.aep01.period_verification_receipt.v1",
        "result": "PASS",
        "verification_scope": "EXACT_MEMBER_SET_AND_SHA256_OFFLINE",
        "period_package_root_sha256": manifest.get("package_root_sha256"),
        "member_count": len(rows),
        "manifest_sha256": sha256_bytes(canonical_bytes(manifest)),
        "sha256s_sha256": sha256_bytes(checksum_payload),
        "model_or_provider_required": False,
        **report_boundary(),
    }


def build_artifact_inventory(
    root: Path,
    *,
    excluded_paths: Sequence[str] = (),
) -> dict[str, Any]:
    """Inventory all ordinary files below a pilot root before its own write."""

    base = require_existing_root(Path(root))
    excluded = sorted(set(excluded_paths))
    members: list[dict[str, Any]] = []
    for path in sorted(base.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        relative = path.relative_to(base).as_posix()
        if relative in excluded:
            continue
        payload = require_single_link_file(path).read_bytes()
        members.append(
            {"bytes": len(payload), "path": relative, "sha256": sha256_bytes(payload)}
        )
    result = {
        "schema_id": "uvlm.triadicbrain.aep01.complete_artifact_inventory.v1",
        "inventory_scope": "ALL_ORDINARY_FILES_PRESENT_BEFORE_THIS_INVENTORY_AND_PILOT_RESULT",
        "declared_exclusions": excluded,
        "members": members,
        "member_count": len(members),
        "inventory_root_sha256": sha256_bytes(canonical_bytes(members)),
        **report_boundary(),
    }
    return result


def parse_report_json(payload: bytes) -> dict[str, Any]:
    """Parse one canonical report object for focused tests and callers."""

    result = strict_load_object(payload)
    if result.get("report_notice") != REPORT_NOTICE:
        raise ReportingError("REPORT_NOTICE_MISSING")
    return result


__all__ = [
    "MANAGEMENT_REPRESENTATION_NOTICE",
    "PRACTITIONER_WORK_PRODUCT_NOTICE",
    "ReportingError",
    "ZERO_REPORT_EFFECTS",
    "build_artifact_inventory",
    "build_period_output_payloads",
    "build_period_package_manifest",
    "build_sha256s",
    "management_representation_template",
    "parse_report_json",
    "report_boundary",
    "report_csv_bytes",
    "report_document",
    "report_jsonl_bytes",
    "render_transaction_review_html",
    "verify_period_output_directory",
]
