"""Read-only local views for AEP01 evidence stores.

The view layer derives display projections from canonical store records.  The
transaction drill-through exposes exact raw source and candidate bytes in an
explicit base64 envelope so a locally authorized practitioner can inspect or
export them without changing their identity.  No view provides a mutation
endpoint or writes generated pages back into the evidence store.  The optional
HTTP server can bind only to an explicitly requested loopback address.
"""

from __future__ import annotations

import html
import json
import socket
from base64 import b64encode
from collections import Counter
from collections.abc import Mapping, Sequence
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from . import (
    AUTHORITY_EFFECT,
    BRAND_STATUS,
    NONASSURANCE_HEADLINE,
    PRODUCT_CATEGORY,
    PRODUCT_NAME,
    PRODUCT_VENDOR,
    PRODUCT_VERSION,
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
from .metrics import derive_metrics, metrics_document
from .models import require_identifier
from .period import (
    build_population_rows,
    population_document,
    reconcile_population,
)
from .practitioner import build_practitioner_index
from .reporting import report_csv_bytes, report_document, report_jsonl_bytes
from .transaction import (
    STATE_SCHEMA_ID,
    STORE_SCHEMA_ID,
    read_creation_ledger,
)


PRODUCT_EXPLANATION = (
    "Control Anchor records what data entered an AI workflow, which model and "
    "settings were used, what the AI produced, which controls ran, what problems "
    "were found, what a person decided, and whether the evidence was "
    "preserved—without allowing the AI model to rewrite its own audit trail."
)
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1"})
MAX_VIEW_FILE_BYTES = 32 * 1024 * 1024
DATA_FLOW_QUESTIONS = (
    "What data entered the workflow?",
    "Who submitted it, for what purpose, and under what authority?",
    "What data was sent to an AI model, or was the output imported instead?",
    "Which model, version, prompt, settings, tools, and source records were used?",
    "What exact output did the AI produce?",
    "What automated and human control checks ran?",
    "What issues, exceptions, failures, or overrides were recorded?",
    "Who approved, held, rejected, or requested repair?",
    "What was finalized, retained, exported, or withheld?",
    "How can another person verify the record without rerunning the AI?",
)


class ViewError(ValueError):
    """A requested display projection could not be derived safely."""


def _store(path: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = candidate.resolve(strict=True)
    root = require_existing_root(candidate)
    manifest = read_canonical_file(root / "store_manifest.json")
    if manifest.get("schema_id") != STORE_SCHEMA_ID:
        raise ViewError("EVIDENCE_STORE_MANIFEST_INVALID")
    return root


def _jsonl(path: Path) -> list[dict[str, Any]]:
    candidate = require_single_link_file(path)
    if candidate.stat().st_size > MAX_VIEW_FILE_BYTES:
        raise ViewError("VIEW_INPUT_OVERSIZE")
    payload = candidate.read_bytes()
    if not payload:
        return []
    if not payload.endswith(b"\n"):
        raise ViewError("JSONL_TRAILING_LF_REQUIRED")
    try:
        rows = [strict_load_object(line) for line in payload.splitlines(keepends=True)]
    except ValueError as exc:
        raise ViewError("JSONL_INVALID") from exc
    if b"".join(canonical_bytes(row) for row in rows) != payload:
        raise ViewError("JSONL_NOT_CANONICAL")
    return rows


def _optional_object(path: Path) -> dict[str, Any] | None:
    return read_canonical_file(path) if path.exists() else None


def _optional_jsonl(path: Path) -> list[dict[str, Any]]:
    return _jsonl(path) if path.exists() else []


def _package_manifest(root: Path, transaction_id: str) -> dict[str, Any] | None:
    path = root / "packages" / transaction_id / "15_EVIDENCE_PACKAGE_MANIFEST.json"
    return _optional_object(path)


def _display_finding(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return a non-secret finding projection and normalize its period type."""

    finding_class = str(row.get("finding_class", row.get("finding_type", "UNKNOWN")))
    period_type = (
        "BINDING_FINDING"
        if finding_class
        in {"BINDING_FINDING", "CONTROL_EXCEPTION", "POLICY_REFUSAL", "SYSTEM_ERROR"}
        else finding_class
    )
    return {
        "affected_controls": list(row.get("affected_controls", [])),
        "finding_class": finding_class,
        "finding_id": row.get("finding_id"),
        "finding_type": period_type,
        "origin": row.get("origin"),
        "risk_posture": row.get("risk_posture"),
        "status": row.get("status"),
        "summary": row.get("summary"),
        "transaction_id": row.get("transaction_id"),
    }


def _display_control(row: Mapping[str, Any]) -> dict[str, Any]:
    expected = row.get("expected_condition")
    expected = expected if isinstance(expected, Mapping) else {}
    return {
        "applicability": expected.get("applicability"),
        "control_id": row.get("control_id"),
        "delivery_tier": expected.get("delivery_tier"),
        "exceptions": list(row.get("exceptions", [])),
        "execution_id": row.get("execution_id"),
        "reason_codes": list(row.get("reason_codes", [])),
        "result": row.get("result"),
        "transaction_id": row.get("transaction_id"),
    }


def _raw_item(payload: bytes, *, media_type: str, object_id: str) -> dict[str, Any]:
    """Envelope exact bytes without normalizing or silently decoding them."""

    result: dict[str, Any] = {
        "base64": b64encode(payload).decode("ascii"),
        "bytes": len(payload),
        "content_encoding": "base64",
        "media_type": media_type,
        "object_id": object_id,
        "sha256": sha256_bytes(payload),
    }
    try:
        decoded = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        result["utf8_text"] = None
        result["utf8_status"] = "NOT_UTF8"
    else:
        result["utf8_text"] = decoded
        result["utf8_status"] = "EXACT_UTF8_DECODE"
    return result


def _data_flow_answers(
    *,
    metadata: Mapping[str, Any],
    state: Mapping[str, Any],
    controls: Sequence[Mapping[str, Any]],
    findings: Sequence[Mapping[str, Any]],
    decision: Mapping[str, Any] | None,
    custody: Sequence[Mapping[str, Any]],
    package: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    """Answer the commissioned ten questions in their exact required order."""

    transaction_id = str(metadata.get("transaction_id"))
    source_digest = metadata.get("source_sha256")
    candidate_digest = metadata.get("candidate_sha256")
    captured = bool(metadata.get("candidate_captured"))
    decision_value = decision.get("decision") if decision is not None else "PENDING"
    package_status = (
        "FINALIZED_CHECKSUM_PACKAGE_PRESENT"
        if package is not None
        else "NOT_FINALIZED_OR_WITHHELD"
    )
    answers = [
        {
            "answer_status": "RECORDED",
            "answer": "Original and normalized local source records were captured separately and assigned SHA-256 identities.",
            "evidence": {
                "media_type": metadata.get("source_media_type"),
                "normalization_profile": metadata.get("normalization_profile"),
                "normalized_source_sha256": metadata.get("normalized_source_sha256"),
                "original_source_sha256": source_digest,
            },
        },
        {
            "answer_status": "PARTIAL_USER_DECLARATION",
            "answer": "The registered use case and local authority posture are recorded; submitter identity and a separate business-purpose narrative were not captured by this transaction schema.",
            "evidence": {
                "authority_posture": "LOCAL_DECLARED_NOT_EXTERNAL_AUTHORITY",
                "business_purpose_proxy": metadata.get("use_case_id"),
                "required_human_reviewer": "AUTHORIZED_HUMAN_REVIEWER_ROLE",
                "submitter_identity": "NOT_CAPTURED",
            },
        },
        {
            "answer_status": "RECORDED",
            "answer": "P0 imported caller-supplied captured output. It did not send data to or invoke an AI provider.",
            "evidence": {
                "candidate_captured": captured,
                "invocation_mode": "CAPTURED_OUTPUT",
                "provider_invoked": False,
                "source_sent_to_provider": False,
            },
        },
        {
            "answer_status": "RECORDED_WITH_DECLARATION_LIMITS",
            "answer": "The declared model identity, exact prompt, settings, and source identities are bound in the transaction record; no tools were granted and the model declaration was not independently verified.",
            "evidence": {
                "model_identity": metadata.get("model_identity"),
                "model_identity_posture": "USER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
                "prompt": metadata.get("prompt"),
                "settings": metadata.get("settings"),
                "source_sha256": source_digest,
                "tools_granted": [],
            },
        },
        {
            "answer_status": "RECORDED" if captured else "NOT_EXECUTED",
            "answer": "Exact raw candidate bytes are available in the explicit raw-output envelope and remain distinct from all authoritative evidence records.",
            "evidence": {
                "candidate_bytes_available": True,
                "candidate_sha256": candidate_digest,
                "candidate_capture_status": "CAPTURED" if captured else "FAILED_OR_EMPTY_CAPTURE",
            },
        },
        {
            "answer_status": "RECORDED",
            "answer": "Versioned control executions, independent review, orientation, and any human decision are listed with their evidence references.",
            "evidence": {
                "control_execution_count": len(controls),
                "control_execution_ids": [row.get("execution_id") for row in controls],
                "human_decision_recorded": decision is not None,
            },
        },
        {
            "answer_status": "RECORDED",
            "answer": "Findings, exceptions, failures, holds, not-executed procedures, and recorded overrides remain visible and are not collapsed into a favorable status.",
            "evidence": {
                "finding_ids": [row.get("finding_id") for row in findings],
                "unfavorable_control_execution_ids": [
                    row.get("execution_id")
                    for row in controls
                    if row.get("result") in {"FAIL", "HOLD", "ERROR", "NOT_EXECUTED"}
                ],
            },
        },
        {
            "answer_status": "RECORDED" if decision is not None else "PENDING",
            "answer": "The human decision record identifies the decision, actor, rationale, selected findings, and evidence shown; no missing decision is treated as approval.",
            "evidence": decision if decision is not None else {"decision": "PENDING"},
        },
        {
            "answer_status": "RECORDED",
            "answer": "Finalization and retention are shown from the state and package manifest; absent packages remain explicitly withheld or nonfinalized.",
            "evidence": {
                "current_state": state.get("current_state"),
                "package_status": package_status,
                "package_id": package.get("package_id") if package else None,
                "package_root_sha256": package.get("package_root_sha256") if package else None,
                "retention_posture": "BOUNDED_LOCAL_EVIDENCE_RECORDS_ONLY",
                "transaction_id": transaction_id,
            },
        },
        {
            "answer_status": "AVAILABLE" if package is not None else "PENDING_FINALIZATION",
            "answer": "Another person can recompute canonical identities, the custody hash chain, and package checksums locally without rerunning an AI model or using a network.",
            "evidence": {
                "custody_event_count": len(custody),
                "model_required": False,
                "network_required": False,
                "package_manifest_available": package is not None,
                "verification_command": (
                    f"control-anchor verify --package <store>/packages/{transaction_id}.zip"
                    if package is not None
                    else None
                ),
            },
        },
    ]
    if len(answers) != len(DATA_FLOW_QUESTIONS):
        raise ViewError("DATA_FLOW_ANSWER_COUNT_INVALID")
    return [
        {"ordinal": index, "question": question, **answer}
        for index, (question, answer) in enumerate(
            zip(DATA_FLOW_QUESTIONS, answers, strict=True), 1
        )
    ]


def _unavailable_data_flow_answers(reason: str) -> list[dict[str, Any]]:
    return [
        {
            "answer": "The canonical record needed to answer this question is incomplete or unreadable; no favorable fact is inferred.",
            "answer_status": "UNAVAILABLE",
            "evidence": {"reason": reason},
            "ordinal": ordinal,
            "question": question,
        }
        for ordinal, question in enumerate(DATA_FLOW_QUESTIONS, 1)
    ]


def _transaction_record(
    root: Path,
    transaction_id: str,
    snapshot: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any] | None]:
    tx = root / "transactions" / transaction_id
    if not tx.is_dir() or tx.is_symlink():
        return (
            {
                "admission_status": "PENDING",
                "data_flow_answers": _unavailable_data_flow_answers(
                    "TRANSACTION_ROOT_MISSING_OR_INVALID"
                ),
                "human_decision": "PENDING",
                "parent_transaction_id": snapshot.get("parent_transaction_id"),
                "period_id": snapshot.get("period_id"),
                "transaction_id": transaction_id,
                "transaction_state": "INCOMPLETE_REGISTRATION",
            },
            [],
            [],
            None,
        )
    metadata = read_canonical_file(tx / "transaction.json")
    state = read_canonical_file(tx / "state.json")
    if (
        metadata.get("schema_id")
        != "uvlm.triadicbrain.aep01.transaction_registration.v1"
        or metadata.get("transaction_id") != transaction_id
        or state.get("schema_id") != STATE_SCHEMA_ID
        or state.get("transaction_id") != transaction_id
    ):
        raise ViewError("TRANSACTION_RECORD_IDENTITY_INVALID")
    decision = _optional_object(tx / "review" / "human_decision.json")
    exact_findings = _optional_jsonl(tx / "review" / "findings.jsonl")
    exact_controls = _optional_jsonl(tx / "review" / "control_results.jsonl")
    custody = _optional_jsonl(tx / "custody_events.jsonl")
    findings = [_display_finding(row) for row in exact_findings]
    controls = [_display_control(row) for row in exact_controls]
    package = _package_manifest(root, transaction_id)
    state_value = str(state.get("current_state", snapshot.get("state", "UNKNOWN")))
    admission = "REFUSED" if (
        state_value == "REFUSED" or (package is not None and package.get("state") == "REFUSED")
    ) else (
        "PENDING"
        if state_value in {"CREATED", "ADMISSION_PENDING", "INCOMPLETE_REGISTRATION"}
        else "ADMITTED"
    )
    decision_value = str(decision.get("decision")) if decision is not None else "PENDING"
    adverse_control = any(
        row.get("result") in {"FAIL", "HOLD", "ERROR"}
        or (
            row.get("result") == "NOT_EXECUTED"
            and row.get("applicability") == "APPLICABLE"
        )
        for row in controls
    )
    adverse = bool(
        admission == "REFUSED"
        or state_value
        in {
            "ATLAS_FAILED",
            "CANDIDATE_FAILED",
            "CONTROLS_INCOMPLETE",
            "FINALIZATION_FAILED",
            "HELD",
            "REJECTED",
            "SOPHIA_FAILED",
        }
        or decision_value in {"HOLD", "REJECT"}
        or adverse_control
    )
    record = {
        "adverse": adverse,
        "admission_status": admission,
        "candidate_sha256": metadata.get("candidate_sha256"),
        "data_flow_answers": _data_flow_answers(
            metadata=metadata,
            state=state,
            controls=exact_controls,
            findings=exact_findings,
            decision=decision,
            custody=custody,
            package=package,
        ),
        "human_decision": decision if decision is not None else "PENDING",
        "identity": metadata.get("identity"),
        "model_identity": metadata.get("model_identity"),
        "parent_transaction_id": metadata.get("identity", {}).get("parent_transaction_id"),
        "period_id": metadata.get("period_id"),
        "provider_invoked": False,
        "review_policy": metadata.get("review_policy"),
        "sealed": state_value == "SEALED",
        "source_sha256": metadata.get("source_sha256"),
        "system_id": metadata.get("system_id"),
        "transaction_id": transaction_id,
        "transaction_state": state_value,
        "use_case_id": metadata.get("use_case_id"),
    }
    if package is not None:
        record["package"] = {
            "finalized": package.get("finalized"),
            "package_id": package.get("package_id"),
            "package_sha256": package.get("package_root_sha256"),
            "signature_posture": package.get("signing_posture"),
        }
    return record, controls, findings, package


def build_evidence_report(
    store_root: Path,
    *,
    period_id: str | None = None,
) -> dict[str, Any]:
    """Build a complete in-memory report without changing the evidence store."""

    root = _store(Path(store_root))
    if period_id is not None:
        period_id = require_identifier(period_id, "period_id")
    manifest = read_canonical_file(root / "store_manifest.json")
    ledger = read_creation_ledger(root)
    records: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    packages: list[dict[str, Any]] = []
    selected_ledger: list[dict[str, Any]] = []
    transaction_root_ids: list[str] = []
    for event in ledger:
        transaction_id = str(event["transaction_id"])
        projection_valid = True
        try:
            record, tx_controls, tx_findings, package = _transaction_record(
                root,
                transaction_id,
                {
                    "parent_transaction_id": event.get("parent_transaction_id"),
                    "period_id": event.get("period_id"),
                },
            )
        except (OSError, ValueError):
            # Population authority is the append-only creation ledger.  A
            # damaged or partial transaction must therefore remain visible
            # instead of making the whole population silently disappear.
            projection_valid = False
            record = {
                "admission_status": "PENDING",
                "adverse": True,
                "data_flow_answers": _unavailable_data_flow_answers(
                    "EVIDENCE_RECORD_UNREADABLE_OR_INCOMPLETE"
                ),
                "human_decision": "PENDING",
                "parent_transaction_id": event.get("parent_transaction_id"),
                "period_id": event.get("period_id"),
                "projection_error": "EVIDENCE_RECORD_UNREADABLE_OR_INCOMPLETE",
                "transaction_id": transaction_id,
                "transaction_state": "INCOMPLETE_REGISTRATION",
            }
            tx_controls = []
            tx_findings = []
            package = None
        if period_id is not None and record.get("period_id") not in {period_id, None}:
            continue
        if period_id is not None:
            record["period_filter_disposition"] = (
                "MATCHED_DECLARED_PERIOD"
                if record.get("period_id") == period_id
                else "UNKNOWN_PERIOD_INCLUDED_FOR_COMPLETENESS"
            )
        selected_ledger.append(event)
        records.append(record)
        tx_root = root / "transactions" / transaction_id
        if projection_valid and tx_root.is_dir() and not tx_root.is_symlink():
            transaction_root_ids.append(transaction_id)
        controls.extend(tx_controls)
        findings.extend(tx_findings)
        if package is not None:
            packages.append(dict(package))

    rows = build_population_rows(
        selected_ledger,
        transaction_records=records,
        finding_rows=findings,
    )
    reconciliation = reconcile_population(
        selected_ledger,
        rows,
        transaction_records=records,
        transaction_root_ids=transaction_root_ids,
        sealed_package_manifests=packages,
    )
    metric_rows = derive_metrics(
        rows,
        control_rows=controls,
        finding_rows=findings,
        package_rows=packages,
        reconciliation=reconciliation,
    )
    population = population_document(rows)
    state_counts = Counter(str(row.get("transaction_state")) for row in rows)
    decision_counts = Counter(str(row.get("human_decision")) for row in rows)
    control_counts = Counter(str(row.get("result")) for row in controls)
    finding_counts = Counter(str(row.get("finding_class")) for row in findings)
    attention = [
        {
            "adverse": row.get("adverse"),
            "binding_finding_ids": row.get("binding_finding_ids", []),
            "human_decision": row.get("human_decision"),
            "open_advisory_finding_ids": row.get("open_advisory_finding_ids", []),
            "transaction_id": row.get("transaction_id"),
            "transaction_state": row.get("transaction_state"),
        }
        for row in rows
        if row.get("adverse") is True
        or row.get("open_advisory_finding_ids")
        or row.get("binding_finding_ids")
        or row.get("nonterminal") is True
    ]
    result = {
        "authority_effect": AUTHORITY_EFFECT,
        "contains_assurance_conclusion": False,
        "controls": controls,
        "data_flow_question_order": list(DATA_FLOW_QUESTIONS),
        "data_flow_question_coverage": {
            "answer_count_per_transaction": len(DATA_FLOW_QUESTIONS),
            "all_population_rows_included": len(records) == len(selected_ledger),
            "missing_facts_are_reported_as_unavailable_not_inferred": True,
        },
        "effects": {
            "canonical_evidence_written": False,
            "deployment_performed": False,
            "memory_written": False,
            "network_used": False,
            "provider_invoked": False,
            "publication_performed": False,
        },
        "findings": findings,
        "headline": NONASSURANCE_HEADLINE,
        "management_attention": attention,
        "metrics": metrics_document(metric_rows),
        "opinion_generated_or_prefilled": False,
        "period_filter": period_id,
        "population": population,
        "product_name": PRODUCT_NAME,
        "product_version": VERSION,
        "reconciliation": reconciliation,
        "report_notice": REPORT_NOTICE,
        "schema_id": "uvlm.triadicbrain.aep01.read_only_evidence_report.v1",
        "segregation_posture": manifest.get("segregation_posture"),
        "signing_posture": manifest.get("signing_posture"),
        "store_identity": sha256_bytes(canonical_bytes(manifest)),
        "summary": {
            "control_result_counts": dict(sorted(control_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "finding_counts": dict(sorted(finding_counts.items())),
            "management_attention_count": len(attention),
            "state_counts": dict(sorted(state_counts.items())),
            "transaction_count": len(rows),
        },
        "transactions": records,
    }
    result["report_identity"] = sha256_bytes(canonical_bytes(result))
    return result


def build_management_view(store_root: Path, *, period_id: str | None = None) -> dict[str, Any]:
    report = build_evidence_report(store_root, period_id=period_id)
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "contains_assurance_conclusion": False,
        "headline": NONASSURANCE_HEADLINE,
        "limitations": [
            "Management must determine applicable criteria, scope, materiality, and response.",
            "Approval does not by itself resolve an advisory finding.",
            "Hashes establish bounded identity and integrity properties, not truth or control effectiveness.",
        ],
        "management_attention": report["management_attention"],
        "metrics": report["metrics"],
        "opinion_generated_or_prefilled": False,
        "population": report["population"],
        "reconciliation": report["reconciliation"],
        "report_identity": report["report_identity"],
        "report_notice": REPORT_NOTICE,
        "schema_id": "uvlm.triadicbrain.aep01.management_view.v1",
        "summary": report["summary"],
        "view_posture": "READ_ONLY_SYSTEM_GENERATED",
    }


def build_investor_view(store_root: Path, *, period_id: str | None = None) -> dict[str, Any]:
    report = build_evidence_report(store_root, period_id=period_id)
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "brand_status": BRAND_STATUS,
        "category": PRODUCT_CATEGORY,
        "contains_assurance_conclusion": False,
        "headline": NONASSURANCE_HEADLINE,
        "operating_posture": {
            "captured_or_imported_output_p0": True,
            "canonical_evidence_write_from_view": False,
            "model_can_approve_own_output": False,
            "network_used_to_build_view": False,
            "provider_invoked": False,
            "remote_evidence_service": False,
            "segregation_posture": report["segregation_posture"],
        },
        "plain_language_product_explanation": PRODUCT_EXPLANATION,
        "product_name": PRODUCT_NAME,
        "product_version": PRODUCT_VERSION,
        "vendor_presentation": PRODUCT_VENDOR,
        "report_identity": report["report_identity"],
        "report_notice": REPORT_NOTICE,
        "schema_id": "uvlm.triadicbrain.aep01.investor_view.v1",
        "summary": report["summary"],
        "view_posture": "READ_ONLY_SYSTEM_GENERATED",
    }


def build_practitioner_view(
    store_root: Path,
    *,
    period_id: str | None = None,
) -> dict[str, Any]:
    report = build_evidence_report(store_root, period_id=period_id)
    population_rows = report["population"]["rows"]
    package_rows = [
        record["package"] | {"transaction_id": record["transaction_id"]}
        for record in report["transactions"]
        if isinstance(record.get("package"), Mapping)
    ]
    evidence_rows = [
        *[
            (str(row.get("execution_id") or row.get("control_id")), row)
            for row in report["controls"]
        ],
        *[
            (str(row.get("finding_id")), row)
            for row in report["findings"]
        ],
        *[
            (str(row.get("package_id") or row.get("transaction_id")), row)
            for row in package_rows
        ],
    ]
    live_period_id = (
        report["population"].get("period_id")
        or period_id
        or "ALL-STORE-EVIDENCE"
    )
    period_stub = {
        "period_id": live_period_id,
        "population_counts": {"created": len(population_rows)},
        "population_identity": report["population"]["population_identity"],
        "population_row_digests": [
            {
                "row_id": row.get("population_row_id"),
                "sha256": sha256_bytes(canonical_bytes(row)),
            }
            for row in population_rows
        ],
        "evidence_row_digests": [
            {"row_id": object_id, "sha256": sha256_bytes(canonical_bytes(row))}
            for object_id, row in evidence_rows
        ],
        "revision_id": f"{live_period_id}-R0001",
        "revision_number": 1,
    }
    period_stub["revision_identity"] = sha256_bytes(canonical_bytes(period_stub))
    index = build_practitioner_index(
        period_revision=period_stub,
        population_rows=population_rows,
        control_rows=report["controls"],
        finding_rows=report["findings"],
        package_rows=package_rows,
    )
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "annotation_surface": {
            "allowed_record_types": ["ANNOTATION", "MAPPING_CHALLENGE"],
            "canonical_evidence_write_permitted": False,
            "challenge_states": [
                "OPEN",
                "MANAGEMENT_RESPONSE_PROVIDED",
                "ACCEPTED",
                "REJECTED",
                "PARTIALLY_ACCEPTED",
                "SUPERSEDED",
            ],
            "storage_domain": "SEPARATE_PRACTITIONER_OUTPUT_ONLY",
            "view_endpoint_accepts_writes": False,
        },
        "contains_assurance_conclusion": False,
        "evidence_index": index,
        "headline": NONASSURANCE_HEADLINE,
        "independence_boundary": {
            "canonical_evidence_write_permitted": False,
            "criteria_determined": False,
            "evidence_sufficiency_determined": False,
            "materiality_determined": False,
            "opinion_generated_or_prefilled": False,
            "sample_sufficiency_determined": False,
        },
        "report_identity": report["report_identity"],
        "report_notice": REPORT_NOTICE,
        "raw_export_surface": {
            "formats": ["CSV", "JSON", "JSONL"],
            "routes": [
                "/api/practitioner/export.csv",
                "/api/practitioner/export.json",
                "/api/practitioner/export.jsonl",
            ],
            "source_mutation_permitted": False,
        },
        "sampling_surface": {
            "complete_frame_available": True,
            "modes": [
                "MANUAL_SELECTION",
                "DETERMINISTIC_RANDOM_SELECTION_WITH_PRACTITIONER_SEED",
                "EXTERNAL_SAMPLE_IMPORT",
            ],
            "representative_claim": False,
            "sample_sufficiency_determined": False,
            "sampling_controlled_by_practitioner": True,
            "vendor_selects_seed": False,
        },
        "schema_id": "uvlm.triadicbrain.aep01.practitioner_view.v1",
        "transaction_drill_through_routes": [
            f"/transaction/{row.get('transaction_id')}"
            for row in population_rows
        ],
        "view_posture": "READ_ONLY_COMPLETE_POPULATION",
    }


def build_transaction_view(store_root: Path, transaction_id: str) -> dict[str, Any]:
    """Return complete read-only drill-through, including exact raw envelopes."""

    transaction_id = require_identifier(transaction_id, "transaction_id")
    root = _store(Path(store_root))
    report = build_evidence_report(root)
    records = [
        row for row in report["transactions"] if row.get("transaction_id") == transaction_id
    ]
    if len(records) != 1:
        raise ViewError("TRANSACTION_NOT_FOUND")
    transaction_root = root / "transactions" / transaction_id
    if not transaction_root.is_dir() or transaction_root.is_symlink():
        raise ViewError("TRANSACTION_EVIDENCE_NOT_AVAILABLE")
    metadata = read_canonical_file(transaction_root / "transaction.json")
    state = read_canonical_file(transaction_root / "state.json")
    exact_controls = _optional_jsonl(transaction_root / "review" / "control_results.jsonl")
    exact_findings = _optional_jsonl(transaction_root / "review" / "findings.jsonl")
    custody = _optional_jsonl(transaction_root / "custody_events.jsonl")
    decision = _optional_object(transaction_root / "review" / "human_decision.json")
    independent_review = _optional_object(
        transaction_root / "review" / "independent_review.json"
    )
    orientation = _optional_object(transaction_root / "review" / "orientation.json")
    repair_lineage = _optional_object(transaction_root / "review" / "repair_lineage.json")
    recovery = (
        [
            read_canonical_file(path)
            for path in sorted(
                (transaction_root / "recovery").glob("*.json"),
                key=lambda item: item.name,
            )
        ]
        if (transaction_root / "recovery").is_dir()
        else []
    )
    package = _package_manifest(root, transaction_id)
    verification: dict[str, Any]
    package_directory = root / "packages" / transaction_id
    package_archive = root / "packages" / f"{transaction_id}.zip"
    if package is not None and package_directory.is_dir() and package_archive.is_file():
        from .verification import verify_transaction_directory, verify_transaction_zip

        try:
            directory_result = verify_transaction_directory(package_directory)
            archive_result = verify_transaction_zip(package_archive)
        except (OSError, ValueError) as exc:
            verification = {
                "result": "HOLD",
                "reason_code": type(exc).__name__,
                "provider_or_model_required": False,
            }
        else:
            verification = {
                "archive": archive_result,
                "directory": directory_result,
                "provider_or_model_required": False,
                "result": (
                    "PASS"
                    if directory_result.get("result") == archive_result.get("result") == "PASS"
                    else "HOLD"
                ),
            }
    else:
        verification = {
            "provider_or_model_required": False,
            "reason_code": "PACKAGE_NOT_FINALIZED",
            "result": "NOT_EXECUTED",
        }
    source = require_single_link_file(transaction_root / "quarantine" / "source.bin").read_bytes()
    normalized = require_single_link_file(
        transaction_root / "quarantine" / "source.normalized"
    ).read_bytes()
    candidate = require_single_link_file(
        transaction_root / "quarantine" / "candidate.bin"
    ).read_bytes()
    return {
        "authority_effect": AUTHORITY_EFFECT,
        "audit_log": custody,
        "contains_assurance_conclusion": False,
        "control_results": exact_controls,
        "data_and_model_details": {
            "invocation_mode": "CAPTURED_OUTPUT",
            "model_identity": metadata.get("model_identity"),
            "model_identity_posture": "USER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
            "prompt": metadata.get("prompt"),
            "provider_invoked": False,
            "settings": metadata.get("settings"),
            "source_media_type": metadata.get("source_media_type"),
            "tools_granted": [],
        },
        "data_flow_answers": _data_flow_answers(
            metadata=metadata,
            state=state,
            controls=exact_controls,
            findings=exact_findings,
            decision=decision,
            custody=custody,
            package=package,
        ),
        "findings": exact_findings,
        "headline": NONASSURANCE_HEADLINE,
        "human_decision": decision if decision is not None else {"decision": "PENDING"},
        "independent_review": independent_review,
        "orientation": orientation,
        "package_manifest": package,
        "raw_evidence": {
            "candidate": _raw_item(
                candidate,
                media_type="application/octet-stream",
                object_id="RAW-AI-OUTPUT",
            ),
            "normalized_source": _raw_item(
                normalized,
                media_type="text/plain; charset=utf-8",
                object_id="NORMALIZED-SOURCE-PROJECTION",
            ),
            "original_source": _raw_item(
                source,
                media_type=str(metadata.get("source_media_type", "application/octet-stream")),
                object_id="ORIGINAL-SOURCE",
            ),
        },
        "raw_candidate_exposed": True,
        "raw_export_authorization_posture": "LOCAL_CALLER_MUST_BE_AUTHORIZED_FOR_STORE_ACCESS",
        "raw_source_exposed": True,
        "record": records[0],
        "recovery_records": recovery,
        "report_notice": REPORT_NOTICE,
        "repair_lineage": repair_lineage,
        "schema_id": "uvlm.triadicbrain.aep01.transaction_drill_through.v1",
        "source_evidence_mutated": False,
        "verification": verification,
    }


def build_practitioner_export(
    store_root: Path,
    format_name: str,
    *,
    period_id: str | None = None,
) -> tuple[str, bytes]:
    """Build a complete read-only population export with the exact notice."""

    view = build_practitioner_view(store_root, period_id=period_id)
    index = view["evidence_index"]
    rows = index.get("evidence_items", [])
    if not isinstance(rows, list):
        raise ViewError("PRACTITIONER_INDEX_ROWS_INVALID")
    selected = format_name.upper()
    if selected == "JSON":
        payload = canonical_bytes(
            report_document(
                "uvlm.triadicbrain.aep01.practitioner_raw_export_report.v1",
                "evidence_items",
                rows,
                format="JSON",
                index_identity=index.get("index_identity"),
                practitioner_work_product_notice=(
                    "INDEPENDENT PRACTITIONER WORK PRODUCT\n"
                    "NOT AUTHORED, APPROVED, OR ISSUED BY CONTROL ANCHOR"
                ),
            )
        )
        return "application/json; charset=utf-8", payload
    if selected == "JSONL":
        return "application/x-ndjson; charset=utf-8", report_jsonl_bytes(rows)
    if selected == "CSV":
        projected = [
            {
                "adverse": row.get("adverse"),
                "drill_through": row.get("drill_through"),
                "object_id": row.get("object_id"),
                "object_type": row.get("object_type"),
                "read_only": row.get("read_only"),
                "sha256": row.get("sha256"),
                "source_snapshot": row.get("source_snapshot"),
            }
            for row in rows
            if isinstance(row, Mapping)
        ]
        return "text/csv; charset=utf-8", report_csv_bytes(
            projected,
            (
                "object_type",
                "object_id",
                "sha256",
                "adverse",
                "read_only",
                "drill_through",
                "source_snapshot",
            ),
        )
    raise ViewError("PRACTITIONER_EXPORT_FORMAT_INVALID")


def _summary_cards(summary: Mapping[str, Any]) -> str:
    cards = (
        ("Transactions", summary.get("transaction_count", 0)),
        ("Management attention", summary.get("management_attention_count", 0)),
        ("Reconciled states", len(summary.get("state_counts", {}))),
        ("Finding classes", len(summary.get("finding_counts", {}))),
    )
    return "".join(
        f'<div class="card"><strong>{html.escape(str(value))}</strong><span>{html.escape(label)}</span></div>'
        for label, value in cards
    )


def _cell(value: Any) -> str:
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if value is None:
        value = "—"
    return html.escape(str(value))


def _table(
    columns: Sequence[tuple[str, str]],
    rows: Sequence[Mapping[str, Any]],
    *,
    transaction_links: bool = False,
) -> str:
    heading = "".join(f"<th scope=\"col\">{html.escape(label)}</th>" for label, _ in columns)
    rendered_rows: list[str] = []
    for row in rows:
        cells: list[str] = []
        for _, key in columns:
            value = row.get(key)
            rendered = _cell(value)
            if transaction_links and key == "transaction_id" and isinstance(value, str):
                rendered = f'<a href="/transaction/{html.escape(value, quote=True)}">{rendered}</a>'
            cells.append(f"<td>{rendered}</td>")
        rendered_rows.append("<tr>" + "".join(cells) + "</tr>")
    if not rendered_rows:
        rendered_rows.append(f'<tr><td colspan="{len(columns)}">No rows in this projection.</td></tr>')
    return f'<div class="table-wrap"><table><thead><tr>{heading}</tr></thead><tbody>{"".join(rendered_rows)}</tbody></table></div>'


def _plain_view_content(view_name: str, payload: Mapping[str, Any]) -> str:
    if view_name == "investor":
        posture = payload.get("operating_posture")
        posture = posture if isinstance(posture, Mapping) else {}
        return (
            "<h3>What the product does</h3>"
            f"<p>{_cell(payload.get('plain_language_product_explanation'))}</p>"
            "<h3>Bounded operating status</h3>"
            + _table(
                (("Capability or effect", "name"), ("Observed value", "value")),
                [
                    {
                        "name": (
                            "Segregation Status"
                            if key == "segregation_posture"
                            else key.replace("_", " ").title()
                        ),
                        "value": value,
                    }
                    for key, value in sorted(posture.items())
                ],
            )
        )
    if view_name == "management":
        rows = payload.get("management_attention")
        rows = rows if isinstance(rows, list) else []
        return (
            "<h3>Items requiring management attention</h3>"
            + _table(
                (
                    ("Transaction", "transaction_id"),
                    ("State", "transaction_state"),
                    ("Human decision", "human_decision"),
                    ("Advisory findings", "open_advisory_finding_ids"),
                    ("Binding findings", "binding_finding_ids"),
                ),
                rows,
                transaction_links=True,
            )
        )
    if view_name == "practitioner":
        index = payload.get("evidence_index")
        index = index if isinstance(index, Mapping) else {}
        rows = index.get("evidence_items")
        rows = rows if isinstance(rows, list) else []
        projected = [
            {
                "adverse": row.get("adverse"),
                "object_id": row.get("object_id"),
                "object_type": row.get("object_type"),
                "sha256": row.get("sha256"),
                "transaction_id": (
                    row.get("drill_through", {}).get("transaction_id")
                    if isinstance(row.get("drill_through"), Mapping)
                    else None
                ),
            }
            for row in rows
            if isinstance(row, Mapping)
        ]
        return (
            "<h3>Independent practitioner evidence index</h3>"
            "<p>Complete-population access is read-only. Sampling, criteria, materiality, sufficiency, and any opinion remain practitioner decisions.</p>"
            + _table(
                (
                    ("Object type", "object_type"),
                    ("Object ID", "object_id"),
                    ("Transaction", "transaction_id"),
                    ("Adverse", "adverse"),
                    ("SHA-256", "sha256"),
                ),
                projected,
                transaction_links=True,
            )
        )
    if view_name == "transaction":
        controls = payload.get("control_results")
        controls = controls if isinstance(controls, list) else []
        findings = payload.get("findings")
        findings = findings if isinstance(findings, list) else []
        answers = payload.get("data_flow_answers")
        answers = answers if isinstance(answers, list) else []
        raw = payload.get("raw_evidence")
        raw = raw if isinstance(raw, Mapping) else {}
        answer_rows = [
            {
                "answer": row.get("answer"),
                "evidence": row.get("evidence"),
                "ordinal": row.get("ordinal"),
                "question": row.get("question"),
                "status": row.get("answer_status"),
            }
            for row in answers
            if isinstance(row, Mapping)
        ]
        raw_rows = [
            {
                "bytes": item.get("bytes"),
                "encoding": item.get("content_encoding"),
                "media_type": item.get("media_type"),
                "object": name,
                "sha256": item.get("sha256"),
            }
            for name, item in sorted(raw.items())
            if isinstance(item, Mapping)
        ]
        return (
            "<h3>Ten data-flow questions</h3>"
            + _table(
                (
                    ("#", "ordinal"),
                    ("Question", "question"),
                    ("Status", "status"),
                    ("Answer", "answer"),
                    ("Evidence", "evidence"),
                ),
                answer_rows,
            )
            + "<h3>Exact raw evidence envelopes</h3>"
            + "<p>Raw bytes are exposed only in the machine-readable projection below as base64, with byte length and SHA-256. No normalization or provider rerun occurs.</p>"
            + _table(
                (
                    ("Object", "object"),
                    ("Media type", "media_type"),
                    ("Bytes", "bytes"),
                    ("SHA-256", "sha256"),
                    ("Encoding", "encoding"),
                ),
                raw_rows,
            )
            + "<h3>Control execution results</h3>"
            + _table(
                (
                    ("Control", "control_id"),
                    ("Tier", "delivery_tier"),
                    ("Applicability", "applicability"),
                    ("Result", "result"),
                    ("Reason codes", "reason_codes"),
                ),
                controls,
            )
            + "<h3>Findings and exceptions</h3>"
            + _table(
                (
                    ("Finding", "finding_id"),
                    ("Class", "finding_class"),
                    ("Status", "status"),
                    ("Risk status", "risk_posture"),
                    ("Summary", "summary"),
                ),
                findings,
            )
        )
    population = payload.get("population")
    population = population if isinstance(population, Mapping) else {}
    rows = population.get("rows")
    rows = rows if isinstance(rows, list) else []
    return (
        "<h3>Complete transaction population</h3>"
        + _table(
            (
                ("Transaction", "transaction_id"),
                ("Lineage", "lineage_role"),
                ("State", "transaction_state"),
                ("Decision", "human_decision"),
                ("Adverse", "adverse"),
                ("Sealed", "sealed"),
            ),
            rows,
            transaction_links=True,
        )
    )


def render_html_view(view_name: str, payload: Mapping[str, Any]) -> bytes:
    """Render one escaped, script-free report page."""

    title = {
        "evidence": "Evidence population",
        "management": "Management view",
        "investor": "Investor view",
        "practitioner": "Practitioner workspace",
        "transaction": "Transaction drill-through",
    }.get(view_name, "Evidence population")
    summary = payload.get("summary") if isinstance(payload.get("summary"), Mapping) else {}
    if not summary and isinstance(payload.get("record"), Mapping):
        record = payload["record"]
        summary = {
            "transaction_count": 1,
            "management_attention_count": 0,
            "state_counts": {str(record.get("transaction_state")): 1},
            "finding_counts": {},
        }
    body = _summary_cards(summary)
    details = html.escape(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2), quote=False
    )
    plain_content = _plain_view_content(view_name, payload)
    boundary_text = (
        "Read-only local projection. Authority effect: NONE. Exact raw source and candidate bytes are available in explicit base64 envelopes in the machine-readable projection."
        if view_name == "transaction"
        else "Read-only local projection. Authority effect: NONE. Raw source and candidate bytes appear only in authorized transaction drill-through."
    )
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · {html.escape(PRODUCT_NAME)}</title>
<style>
:root{{--ink:#12212d;--muted:#55636e;--paper:#f7f4ed;--panel:#fff;--accent:#0b6574;--warn:#7a3e00}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}}
header,main,nav{{max-width:1120px;margin:auto;padding:1rem 1.25rem}}header{{padding-top:2rem}}h1{{font-size:clamp(1.6rem,4vw,2.6rem);margin:.2rem 0}}
.notice{{border-left:.4rem solid var(--warn);background:#fff3dc;padding:1rem;font-weight:700}}nav a{{color:var(--accent);margin-right:1rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem;margin:1rem 0}}.card{{background:var(--panel);border:1px solid #d8d4ca;padding:1rem;border-radius:.5rem}}
.card strong,.card span{{display:block}}.card strong{{font-size:1.7rem}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#10212b;color:#edf8fa;padding:1rem;border-radius:.5rem;max-height:48rem;overflow:auto}}
.table-wrap{{overflow:auto;background:var(--panel);border:1px solid #d8d4ca;border-radius:.5rem}}table{{width:100%;border-collapse:collapse}}th,td{{padding:.65rem;text-align:left;vertical-align:top;border-bottom:1px solid #e5e1d8}}th{{background:#e9f0f1}}td{{max-width:28rem;overflow-wrap:anywhere}}
.boundary{{color:var(--muted)}}a:focus{{outline:3px solid #e69f00;outline-offset:3px}}
</style></head><body>
<header><p>{html.escape(PRODUCT_VENDOR)} · {html.escape(PRODUCT_CATEGORY)} · Product version {html.escape(PRODUCT_VERSION)}</p><h1>{html.escape(PRODUCT_NAME)} — {html.escape(title)}</h1><p>{html.escape(BRAND_STATUS)}</p><p class="notice"><strong>{html.escape(NONASSURANCE_HEADLINE)}</strong><br>{html.escape(REPORT_NOTICE)}</p></header>
<nav aria-label="Evidence views"><a href="/">Evidence</a><a href="/management">Management</a><a href="/investor">Investor</a><a href="/practitioner">Practitioner</a></nav>
<main><h2>{html.escape(title)}</h2><p class="boundary">{html.escape(boundary_text)}</p><section class="cards">{body}</section>{plain_content}<details><summary>Machine-readable projection</summary><pre>{details}</pre></details></main>
</body></html>\n"""
    return document.encode("utf-8")


def route_view(store_root: Path, target: str) -> tuple[int, str, bytes]:
    """Resolve a GET target to a read-only response without starting a server."""

    parsed = urlsplit(target)
    path = unquote(parsed.path)
    if "\x00" in path or "\\" in path or ".." in path.split("/"):
        raise ViewError("REQUEST_PATH_INVALID")
    html_routes = {
        "/": ("evidence", build_evidence_report),
        "/management": ("management", build_management_view),
        "/investor": ("investor", build_investor_view),
        "/practitioner": ("practitioner", build_practitioner_view),
    }
    api_routes = {
        "/api/report": build_evidence_report,
        "/api/management": build_management_view,
        "/api/investor": build_investor_view,
        "/api/practitioner": build_practitioner_view,
    }
    if path in html_routes:
        name, builder = html_routes[path]
        payload = builder(store_root)
        return 200, "text/html; charset=utf-8", render_html_view(name, payload)
    if path in api_routes:
        return 200, "application/json; charset=utf-8", canonical_bytes(api_routes[path](store_root))
    export_prefix = "/api/practitioner/export."
    if path.startswith(export_prefix) and path.count("/") == 3:
        suffix = path[len(export_prefix) :]
        format_name = {"csv": "CSV", "json": "JSON", "jsonl": "JSONL"}.get(suffix)
        if format_name is None:
            raise ViewError("PRACTITIONER_EXPORT_FORMAT_INVALID")
        content_type, payload = build_practitioner_export(store_root, format_name)
        return 200, content_type, payload
    api_transaction_prefix = "/api/transaction/"
    if path.startswith(api_transaction_prefix) and path.count("/") == 3:
        payload = build_transaction_view(store_root, path[len(api_transaction_prefix) :])
        return 200, "application/json; charset=utf-8", canonical_bytes(payload)
    prefix = "/transaction/"
    if path.startswith(prefix) and path.count("/") == 2:
        payload = build_transaction_view(store_root, path[len(prefix) :])
        return 200, "text/html; charset=utf-8", render_html_view("transaction", payload)
    return 404, "application/json; charset=utf-8", canonical_bytes(
        {
            "authority_effect": AUTHORITY_EFFECT,
            "error": "VIEW_NOT_FOUND",
            "headline": NONASSURANCE_HEADLINE,
            "report_notice": REPORT_NOTICE,
        }
    )


class _IPv6ThreadingHTTPServer(ThreadingHTTPServer):
    address_family = socket.AF_INET6


def serve_read_only(store_root: Path, host: str, port: int) -> None:
    """Serve an evidence store until interrupted; loopback GET/HEAD only."""

    if host not in LOOPBACK_HOSTS:
        raise ViewError("NON_LOOPBACK_BIND_PROHIBITED")
    if type(port) is not int or not 1 <= port <= 65535:
        raise ViewError("PORT_INVALID")
    root = _store(Path(store_root))

    class Handler(BaseHTTPRequestHandler):
        server_version = "ControlAnchor/0"
        sys_version = ""

        def _send(self, *, head: bool = False) -> None:
            try:
                status, content_type, payload = route_view(root, self.path)
            except (OSError, ValueError) as exc:
                status = 400
                content_type = "application/json; charset=utf-8"
                payload = canonical_bytes(
                    {
                        "authority_effect": AUTHORITY_EFFECT,
                        "error": type(exc).__name__,
                        "headline": NONASSURANCE_HEADLINE,
                        "report_notice": REPORT_NOTICE,
                    }
                )
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            if not head:
                self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            self._send()

        def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            self._send(head=True)

        def _deny_mutation(self) -> None:
            payload = canonical_bytes(
                {
                    "authority_effect": AUTHORITY_EFFECT,
                    "error": "READ_ONLY_VIEW_METHOD_NOT_ALLOWED",
                    "headline": NONASSURANCE_HEADLINE,
                    "report_notice": REPORT_NOTICE,
                }
            )
            self.send_response(405)
            self.send_header("Allow", "GET, HEAD")
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        do_POST = _deny_mutation  # type: ignore[assignment]
        do_PUT = _deny_mutation  # type: ignore[assignment]
        do_PATCH = _deny_mutation  # type: ignore[assignment]
        do_DELETE = _deny_mutation  # type: ignore[assignment]

        def log_message(self, format: str, *args: object) -> None:
            # Never copy URLs, query text, or evidence into console logs.
            return

    server_type = _IPv6ThreadingHTTPServer if host == "::1" else ThreadingHTTPServer
    with server_type((host, port), Handler) as server:
        server.serve_forever()


__all__ = [
    "DATA_FLOW_QUESTIONS",
    "LOOPBACK_HOSTS",
    "NONASSURANCE_HEADLINE",
    "PRODUCT_EXPLANATION",
    "REPORT_NOTICE",
    "ViewError",
    "build_evidence_report",
    "build_investor_view",
    "build_management_view",
    "build_practitioner_view",
    "build_practitioner_export",
    "build_transaction_view",
    "render_html_view",
    "route_view",
    "serve_read_only",
]
