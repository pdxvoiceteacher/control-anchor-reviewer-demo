"""Read-only verification for AEP01 transaction evidence packages.

Verification proves only bounded byte identity, declared topology, and internal
consistency.  It does not establish truth, compliance, control effectiveness,
or an assurance conclusion.
"""

from __future__ import annotations

import io
import os
import stat
import unicodedata
import zipfile
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from . import (
    AUTHORITY_EFFECT,
    NONASSURANCE_NOTICE,
    PRODUCT_NAME,
    REPORT_NOTICE,
    VERSION,
)
from .canonical import (
    canonical_bytes,
    is_link_like,
    read_ordinary_bytes,
    require_safe_ancestors,
    sha256_bytes,
    strict_loads,
)
from .claims import claim_control_observations, derive_candidate_claim_map
from .controls import (
    CONTROL_IDS,
    P0_CORE,
    P0_WHEN_APPLICABLE,
    P1,
    PRELIMINARY_P0_CORE_PASS_OBSERVATIONS,
    RESULTS,
    delivery_tier,
    preliminary_platform_observations,
    render_control_catalog_csv,
    render_framework_crosswalk_csv,
)
from .custody import ZERO_SIDE_EFFECTS, verify_events
from .models import TransactionState, validate_transition
from .review_policy import (
    ApprovalEffect,
    ReviewPolicyError,
    ReviewPolicyProfile,
    discover_review_policy_registry,
)
from .reporting import render_transaction_review_html
from .schema_validation import SchemaValidationError, validate_instance
from .transition_policy import (
    TransitionPolicyError,
    validate_recovery_event_semantics,
    validate_transition_event_semantics,
)
from .transaction_package import (
    CONTROL_MEMBERS,
    CORE_CONTENT_MEMBERS,
    FIXED_ZIP_TIME,
    MAX_PACKAGE_BYTES,
    MAX_PACKAGE_DIRECTORIES,
    MAX_PACKAGE_FILES,
)


class VerificationError(ValueError):
    """A package failed a closed read-only verification rule."""


def _verify_optional_review_policy(
    payloads: Mapping[str, bytes],
    *,
    review_policy: ReviewPolicyProfile,
    transaction_id: str,
    created_at_utc: str,
    source_media_type: str,
    prompt: str,
    model_identity: str,
    raw_candidate: bytes,
    original_source: bytes,
    findings: list[dict[str, Any]],
    decision: Mapping[str, Any],
) -> None:
    """Dispatch optional package validation without knowing a plug-in's domain."""

    evaluation_name = "21_REVIEW_POLICY_EVALUATION.json"
    repair_name = "22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json"
    if review_policy.profile_id == "STANDARD":
        if evaluation_name in payloads or repair_name in payloads:
            raise VerificationError("UNEXPECTED_REVIEW_POLICY_EVIDENCE")
        return
    try:
        registry = discover_review_policy_registry(review_policy.profile_id)
        expected_profile = registry.resolve(review_policy.profile_id)
        runtime = registry.runtime(review_policy.profile_id)
    except Exception as exc:
        raise VerificationError("REVIEW_POLICY_PROFILE_REPLAY_FAILED") from exc
    if review_policy.as_dict() != expected_profile.as_dict():
        raise VerificationError("REVIEW_POLICY_PROFILE_BINDING_INVALID")
    try:
        runtime.verify_package(
            payloads,
            review_policy=review_policy,
            transaction_id=transaction_id,
            created_at_utc=created_at_utc,
            source_media_type=source_media_type,
            prompt=prompt,
            model_identity=model_identity,
            raw_candidate=raw_candidate,
            original_source=original_source,
            findings=findings,
            decision=decision,
        )
    except VerificationError:
        raise
    except Exception as exc:
        raise VerificationError("REVIEW_POLICY_PACKAGE_VERIFICATION_FAILED") from exc


def _verify_live_review_policy(
    package_location: Path | None,
    payloads: Mapping[str, bytes],
) -> None:
    """Delegate live-chain replay for a selected optional review policy."""

    if package_location is None or "21_REVIEW_POLICY_EVALUATION.json" not in payloads:
        return
    configuration = _json(
        payloads["04_PROMPT_AND_CONFIGURATION_MANIFEST.json"],
        "CONFIGURATION_MANIFEST_INVALID",
    )
    review_policy = configuration.get("review_policy")
    if not isinstance(review_policy, Mapping):
        raise VerificationError("REVIEW_POLICY_PROFILE_INVALID")
    profile_id = review_policy.get("profile_id")
    if profile_id == "STANDARD":
        return
    if type(profile_id) is not str:
        raise VerificationError("REVIEW_POLICY_PROFILE_INVALID")
    try:
        registry = discover_review_policy_registry(profile_id)
        runtime = registry.runtime(profile_id)
        runtime.verify_live_package(package_location, payloads)
    except VerificationError:
        raise
    except Exception as exc:
        raise VerificationError("REVIEW_POLICY_LIVE_REPLAY_FAILED") from exc


def _safe_member(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name:
        raise VerificationError("PACKAGE_MEMBER_PATH_INVALID")
    if unicodedata.normalize("NFC", name) != name:
        raise VerificationError("PACKAGE_MEMBER_PATH_NOT_NFC")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise VerificationError("PACKAGE_MEMBER_PATH_INVALID")
    if ":" in name or name != name.strip():
        raise VerificationError("PACKAGE_MEMBER_PATH_INVALID")
    return name


def _json(payload: bytes, error: str) -> dict[str, Any]:
    try:
        value = strict_loads(payload)
    except Exception as exc:
        raise VerificationError(error) from exc
    if not isinstance(value, dict) or canonical_bytes(value) != payload:
        raise VerificationError(error)
    return value


def _jsonl(payload: bytes, error: str) -> list[dict[str, Any]]:
    if not payload:
        return []
    if not payload.endswith(b"\n"):
        raise VerificationError(error)
    rows: list[dict[str, Any]] = []
    for raw in payload.splitlines(keepends=True):
        row = _json(raw, error)
        rows.append(row)
    if b"".join(canonical_bytes(row) for row in rows) != payload:
        raise VerificationError(error)
    return rows


def _checksum_map(payload: bytes) -> dict[str, str]:
    try:
        text = payload.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError("CHECKSUM_FILE_INVALID") from exc
    if not text or not text.endswith("\n") or "\r" in text:
        raise VerificationError("CHECKSUM_FILE_INVALID")
    result: dict[str, str] = {}
    prior = ""
    for line in text.splitlines():
        if len(line) < 67 or line[64:66] != "  ":
            raise VerificationError("CHECKSUM_FILE_INVALID")
        digest, name = line[:64], _safe_member(line[66:])
        if any(char not in "0123456789abcdef" for char in digest):
            raise VerificationError("CHECKSUM_FILE_INVALID")
        if name in result or (prior and name <= prior):
            raise VerificationError("CHECKSUM_FILE_ORDER_OR_DUPLICATE")
        prior = name
        result[name] = digest
    return result


def _member_rows(payloads: Mapping[str, bytes]) -> list[dict[str, Any]]:
    def media_type(name: str) -> str:
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

    def object_type(name: str) -> str:
        stem = PurePosixPath(name).name.rsplit(".", 1)[0]
        if len(stem) > 3 and stem[:2].isdigit() and stem[2] == "_":
            stem = stem[3:]
        return stem.upper()

    return [
        {
            "bytes": len(payloads[name]),
            "confidentiality": "PUBLIC_SYNTHETIC",
            "media_type": media_type(name),
            "object_type": object_type(name),
            "path": name,
            "required": True,
            "sha256": sha256_bytes(payloads[name]),
        }
        for name in sorted(payloads)
    ]


def _verify_control_rows(payload: bytes, transaction_id: str) -> list[dict[str, Any]]:
    rows = _jsonl(payload, "CONTROL_RESULTS_INVALID")
    if len(rows) != len(CONTROL_IDS):
        raise VerificationError("CONTROL_RESULTS_INCOMPLETE")
    if [row.get("control_id") for row in rows] != list(CONTROL_IDS):
        raise VerificationError("CONTROL_RESULTS_ORDER_INVALID")
    seen: set[str] = set()
    for sequence, row in enumerate(rows, 1):
        control_id = row.get("control_id")
        if control_id in seen or row.get("transaction_id") != transaction_id:
            raise VerificationError("CONTROL_RESULT_IDENTITY_INVALID")
        seen.add(str(control_id))
        if row.get("result") not in RESULTS or row.get("authority_effect") != AUTHORITY_EFFECT:
            raise VerificationError("CONTROL_RESULT_SEMANTICS_INVALID")
        try:
            validate_instance(row)
        except SchemaValidationError as exc:
            raise VerificationError("CONTROL_RESULT_SCHEMA_INVALID") from exc
        if (
            row.get("actor_id") != "SERVICE-CONTROL-EXECUTOR"
            or row.get("plane") != "CONTROL_EVIDENCE"
            or row.get("sequence") != sequence
            or row.get("execution_id") != f"CEX-{transaction_id}-{sequence:03d}"
            or row.get("procedure_id") != f"PROC-{control_id}-001"
            or row.get("control_version") != "1.0.0"
            or row.get("procedure_version") != "1.0.0"
            or row.get("frequency") != "ON_EACH_TRANSACTION"
            or row.get("method") != "automated"
            or row.get("superseded") is not False
            or row.get("side_effects")
            != {
                "memory_written": False,
                "network_used": False,
                "provider_invoked": False,
            }
        ):
            raise VerificationError("CONTROL_RESULT_WRITER_OR_PROCEDURE_INVALID")
        expected = row.get("expected_condition")
        if (
            not isinstance(expected, Mapping)
            or expected.get("delivery_tier") != delivery_tier(str(control_id))
            or expected.get("population_subject") != transaction_id
        ):
            raise VerificationError("CONTROL_RESULT_EXPECTED_CONDITION_INVALID")
        applicability = expected.get("applicability")
        if control_id in P1 and (
            applicability != "P1_DEFERRED" or row.get("result") != "NOT_EXECUTED"
        ):
            raise VerificationError("P1_CONTROL_RESULT_INVALID")
        if control_id in P0_WHEN_APPLICABLE and applicability == "NOT_APPLICABLE" and row.get("result") != "NOT_EXECUTED":
            raise VerificationError("INAPPLICABLE_CONTROL_RESULT_INVALID")
        reason_codes = row.get("reason_codes")
        observed_condition = row.get("observed_condition")
        if (
            not isinstance(reason_codes, list)
            or not reason_codes
            or len(reason_codes) != len(set(reason_codes))
            or any(type(reason) is not str or not reason for reason in reason_codes)
            or type(observed_condition) is not str
            or not observed_condition.strip()
            or (
                row.get("result") == "PASS"
                and reason_codes
                not in (
                    ["AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"],
                    ["SYNTHETIC_PILOT_CONDITION_OBSERVED"],
                )
            )
        ):
            raise VerificationError("CONTROL_RESULT_OBSERVATION_INVALID")
        if row.get("result") == "PASS" and control_id in P0_CORE:
            if (
                observed_condition
                != PRELIMINARY_P0_CORE_PASS_OBSERVATIONS.get(str(control_id))
                or reason_codes
                != ["AUTHENTICATED_PLATFORM_CONDITION_OBSERVED"]
            ):
                raise VerificationError("P0_CORE_PASS_NOT_PLATFORM_DERIVED")
        claimed = row.get("canonical_result_sha256")
        expected = sha256_bytes(
            canonical_bytes({**row, "canonical_result_sha256": None})
        )
        if claimed != expected:
            raise VerificationError("CONTROL_RESULT_DIGEST_INVALID")
    return rows


def _expected_control_derived_findings(
    transaction_id: str,
    control_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reconstruct every system-origin exception from verified control rows."""

    rows: list[dict[str, Any]] = []
    for control in control_rows:
        result = control["result"]
        if result not in {"FAIL", "HOLD", "ERROR"}:
            continue
        control_id = str(control["control_id"])
        rows.append(
            {
                "affected_controls": [control_id],
                "authority_effect": AUTHORITY_EFFECT,
                "due_date": None,
                "evidence_refs": list(control["evidence_refs"]),
                "finding_class": (
                    "SYSTEM_ERROR" if result == "ERROR" else "CONTROL_EXCEPTION"
                ),
                "finding_id": (
                    "finding_"
                    f"{sha256_bytes(canonical_bytes([transaction_id, control_id]))[:24]}"
                ),
                "origin": "VERSIONED_CONTROL_EXECUTION",
                "owner": "UNASSIGNED",
                "resolution": None,
                "risk_posture": "REVIEW_REQUIRED",
                "status": "OPEN",
                "summary": (
                    f"Control {control_id} recorded {result}; "
                    "human attention is required."
                ),
                "supersedes": None,
                "transaction_id": transaction_id,
            }
        )
    return sorted(rows, key=lambda row: row["finding_id"])


def _require_fields(row: Mapping[str, Any], fields: set[str], error: str) -> None:
    if set(row) != fields:
        raise VerificationError(error)


def _verify_cross_record_bindings(
    payloads: Mapping[str, bytes],
    *,
    transaction_id: str,
    status: Mapping[str, Any],
    manifest: Mapping[str, Any],
    control_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recompute identities that hashes alone cannot semantically relate."""

    system = _json(payloads["01_AI_SYSTEM_IDENTITY.json"], "SYSTEM_IDENTITY_INVALID")
    request = _json(payloads["02_REQUEST_AUTHORITY_AND_CONSENT.json"], "REQUEST_RECORD_INVALID")
    source = _json(payloads["03_SOURCE_AND_RETRIEVAL_MANIFEST.json"], "SOURCE_MANIFEST_INVALID")
    configuration = _json(payloads["04_PROMPT_AND_CONFIGURATION_MANIFEST.json"], "CONFIGURATION_MANIFEST_INVALID")
    invocation = _json(payloads["05_MODEL_INVOCATION_RECORD.json"], "MODEL_INVOCATION_RECORD_INVALID")
    claim_map = _json(payloads["07_CANDIDATE_AND_CLAIM_MAP.json"], "CLAIM_MAP_INVALID")
    review = _json(payloads["10_SOPHIA_AUDIT_PACKET.json"], "REVIEW_PACKET_INVALID")
    orientation = _json(payloads["11_ATLAS_POSTURE_PACKET.json"], "ORIENTATION_PACKET_INVALID")
    decision = _json(payloads["12_HUMAN_DECISION.json"], "HUMAN_DECISION_INVALID")
    findings = _jsonl(payloads["09_FINDINGS_AND_EXCEPTIONS.jsonl"], "FINDINGS_INVALID")

    _require_fields(
        system,
        {
            "authority_effect",
            "model_identity",
            "model_identity_posture",
            "product_name",
            "product_version",
            "system_id",
            "transaction_id",
            "use_case_id",
        },
        "SYSTEM_IDENTITY_FIELDS_INVALID",
    )
    _require_fields(
        request,
        {
            "admission_status",
            "authority_effect",
            "consent_posture",
            "requester_authority_posture",
            "transaction_id",
        },
        "REQUEST_RECORD_FIELDS_INVALID",
    )
    _require_fields(
        source,
        {
            "authority_effect",
            "availability_limitation",
            "ingestion_method",
            "normalization_profile",
            "normalized_bytes",
            "normalized_sha256",
            "original_bytes",
            "original_sha256",
            "privacy_classification",
            "source_media_type",
            "transaction_id",
            "user_declaration",
        },
        "SOURCE_MANIFEST_FIELDS_INVALID",
    )
    _require_fields(
        configuration,
        {
            "authority_effect",
            "control_catalog_version",
            "effective_configuration_sha256",
            "feature_flags",
            "prompt_components",
            "review_policy",
            "secret_references",
            "settings",
            "transaction_id",
        },
        "CONFIGURATION_MANIFEST_FIELDS_INVALID",
    )
    _require_fields(
        invocation,
        {
            "authority_effect",
            "candidate_bytes",
            "candidate_sha256",
            "capture_time_posture",
            "invocation_mode",
            "limitations",
            "model_identity",
            "provider_identity",
            "provider_invoked",
            "raw_capture_method",
            "transaction_id",
        },
        "MODEL_INVOCATION_FIELDS_INVALID",
    )
    _require_fields(
        claim_map,
        {
            "authority_effect",
            "candidate_sha256",
            "claim_extraction_status",
            "claims",
            "nonauthority",
            "schema_id",
            "transaction_id",
        },
        "CLAIM_MAP_FIELDS_INVALID",
    )
    _require_fields(
        review,
        {
            "authority_effect",
            "finding_count",
            "finding_ids",
            "limitations",
            "nonauthority",
            "result",
            "schema_id",
            "transaction_id",
        },
        "REVIEW_PACKET_FIELDS_INVALID",
    )
    _require_fields(
        orientation,
        {
            "authority_effect",
            "finding_count",
            "management_attention",
            "nonauthority",
            "schema_id",
            "transaction_id",
        },
        "ORIENTATION_PACKET_FIELDS_INVALID",
    )
    pending_decision_fields = {
        "authority_effect",
        "decision",
        "nonauthority",
        "reason",
        "transaction_id",
    }
    recorded_decision_fields = {
        "actor_authentication_posture",
        "actor_id",
        "authority_effect",
        "conditions",
        "csrf_replay_protection",
        "decision",
        "decision_id",
        "decision_time_utc",
        "nonauthority",
        "override_records",
        "parent_evidence_digests",
        "rationale",
        "selected_finding_ids",
        "side_effects",
        "signature_posture",
        "time_posture",
        "transaction_id",
        "ui_session_version",
        "unresolved_findings_acknowledged",
    }
    expected_decision_fields = (
        pending_decision_fields
        if decision.get("decision") == "PENDING"
        else recorded_decision_fields
    )
    _require_fields(
        decision, expected_decision_fields, "HUMAN_DECISION_FIELDS_INVALID"
    )

    raw_candidate = payloads["06_RAW_CANDIDATE_CAPTURE.bin"]
    original_source = payloads["source/original.bin"]
    normalized_source = payloads["source/normalized.txt"]
    raw_sha = sha256_bytes(raw_candidate)
    source_sha = sha256_bytes(original_source)
    normalized_sha = sha256_bytes(normalized_source)
    non_model_event = configuration.get('settings',{}).get('processing_kind')=='NON_MODEL_EVENT'
    if non_model_event and (raw_candidate != b'' or system.get('model_identity')!='NOT_APPLICABLE_NON_MODEL_EVENT'):
        raise VerificationError('NON_MODEL_EVENT_CANDIDATE_SUBSTITUTION')
    if (
        invocation.get("invocation_mode") != ("NON_MODEL_EVENT_NO_INVOCATION" if non_model_event else "CAPTURED_CANDIDATE")
        or invocation.get("provider_invoked") is not False
        or invocation.get("candidate_bytes") != len(raw_candidate)
        or invocation.get("candidate_sha256") != raw_sha
        or claim_map.get("candidate_sha256") != raw_sha
        or system.get("model_identity") != invocation.get("model_identity")
        or system.get("product_name") != PRODUCT_NAME
        or system.get("product_version") != VERSION
        or system.get("model_identity_posture")
        != ("NOT_APPLICABLE_NON_MODEL_EVENT" if non_model_event else "USER_DECLARED_NOT_INDEPENDENTLY_VERIFIED")
    ):
        raise VerificationError("CANDIDATE_MODEL_IDENTITY_BINDING_INVALID")
    if (
        source.get("original_bytes") != len(original_source)
        or source.get("original_sha256") != source_sha
        or source.get("normalized_bytes") != len(normalized_source)
        or source.get("normalized_sha256") != normalized_sha
        or source.get("ingestion_method") != "CAPTURED_BYTES"
    ):
        raise VerificationError("SOURCE_BYTE_IDENTITY_BINDING_INVALID")
    expected_claim_map = derive_candidate_claim_map(
        transaction_id=transaction_id,
        candidate_bytes=raw_candidate,
        source_bytes=original_source,
    )
    if claim_map != expected_claim_map:
        raise VerificationError("CANDIDATE_CLAIM_MAP_BINDING_INVALID")
    expected_claim_controls = {} if non_model_event else claim_control_observations(expected_claim_map)
    controls_by_id = {row["control_id"]: row for row in control_rows}
    for control_id, observation in expected_claim_controls.items():
        row = controls_by_id.get(control_id)
        if (
            row is None
            or row.get("result") != observation["result"]
            or row.get("observed_condition") != observation["observed_condition"]
            or row.get("reason_codes") != observation["reason_codes"]
            or row.get("expected_condition", {}).get("applicability")
            != "APPLICABLE"
        ):
            raise VerificationError("CANDIDATE_CLAIM_CONTROL_BINDING_INVALID")
    custody_rows = _jsonl(
        payloads["14_CUSTODY_EVENTS.jsonl"], "CUSTODY_EVENTS_INVALID"
    )
    operations = {row.get("operation") for row in custody_rows}
    captured_route = (
        "STATE_TRANSITION:CANDIDATE_PENDING->CANDIDATE_CAPTURED" in operations
    )
    failed_route = (
        "STATE_TRANSITION:CANDIDATE_PENDING->CANDIDATE_FAILED" in operations
    )
    event_route = "STATE_TRANSITION:INPUTS_BOUND->OBSERVED_EVENT_BOUND" in operations
    if event_route != non_model_event or (event_route and (captured_route or failed_route)):
        raise VerificationError('NON_MODEL_EVENT_ROUTE_BINDING_INVALID')
    if not event_route and captured_route == failed_route and status.get("business_state") != "REFUSED":
        raise VerificationError("CANDIDATE_CAPTURE_ROUTE_BINDING_INVALID")
    allowed_preliminary = (
        {}
        if status.get("business_state") == "REFUSED" or non_model_event
        else preliminary_platform_observations(candidate_captured=captured_route)
    )
    for control_id in P0_CORE:
        row = controls_by_id[control_id]
        if row.get("result") != "PASS":
            continue
        expected_observation = allowed_preliminary.get(control_id)
        if (
            expected_observation is None
            or row.get("observed_condition")
            != expected_observation["observed_condition"]
            or row.get("reason_codes") != expected_observation["reason_codes"]
        ):
            raise VerificationError("P0_CORE_PASS_ROUTE_BINDING_INVALID")
    if non_model_event:
        for row in control_rows:
            event_procedure=row['control_id'] in (*P0_CORE,*P0_WHEN_APPLICABLE)
            if (row.get('result')!='NOT_EXECUTED'
                or event_procedure and (row.get('reason_codes')!=['NON_MODEL_EVENT_NO_CANDIDATE_PROCEDURE']
                    or row.get('observed_condition')!='Non-model event: this model/candidate procedure is not applicable. Executed event-policy results are separately bound.')
                or not event_procedure and row.get('reason_codes')!=['P1_DEFERRED_NOT_EXECUTED']):
                raise VerificationError('NON_MODEL_EVENT_PROCEDURE_FABRICATION')
    normalization_profile = source.get("normalization_profile")
    if normalization_profile == "UTF8_NFC_LF_V1":
        try:
            normalized_expected = unicodedata.normalize(
                "NFC",
                original_source.decode("utf-8", "strict")
                .replace("\r\n", "\n")
                .replace("\r", "\n"),
            )
        except UnicodeDecodeError as exc:
            raise VerificationError("SOURCE_NORMALIZATION_INVALID") from exc
        if not normalized_expected.endswith("\n"):
            normalized_expected += "\n"
        if normalized_expected.encode("utf-8") != normalized_source:
            raise VerificationError("SOURCE_NORMALIZATION_INVALID")
    elif normalization_profile == "BINARY_SOURCE_NO_TEXT_PROJECTION":
        if normalized_source != b"":
            raise VerificationError("SOURCE_NORMALIZATION_INVALID")
    else:
        raise VerificationError("SOURCE_NORMALIZATION_PROFILE_INVALID")
    prompt_components = configuration.get("prompt_components")
    feature_flags = configuration.get("feature_flags")
    try:
        review_policy = ReviewPolicyProfile.from_mapping(configuration["review_policy"])
    except (KeyError, ReviewPolicyError, TypeError, ValueError) as exc:
        raise VerificationError("REVIEW_POLICY_PROFILE_INVALID") from exc
    if (
        not isinstance(prompt_components, list)
        or len(prompt_components) != 1
        or not isinstance(prompt_components[0], Mapping)
        or set(prompt_components[0]) != {"kind", "text"}
        or prompt_components[0].get("kind") != "USER"
        or not isinstance(configuration.get("settings"), Mapping)
        or configuration.get("effective_configuration_sha256")
        != sha256_bytes(
            canonical_bytes(
                {
                    "prompt": prompt_components[0].get("text"),
                    "settings": dict(configuration["settings"]),
                }
            )
        )
        or not isinstance(feature_flags, Mapping)
        or dict(feature_flags)
        != {
            "optional_review_policy_selected": review_policy.profile_id != "STANDARD",
            "remote_provider": False,
        }
        or configuration.get("secret_references") != []
        or configuration.get("control_catalog_version") != "1.0.0"
    ):
        raise VerificationError("CONFIGURATION_IDENTITY_BINDING_INVALID")
    _verify_optional_review_policy(
        payloads,
        review_policy=review_policy,
        transaction_id=transaction_id,
        created_at_utc=str(status.get("created_at_utc")),
        source_media_type=str(source.get("source_media_type")),
        prompt=str(prompt_components[0]["text"]),
        model_identity=str(system.get("model_identity")),
        raw_candidate=raw_candidate,
        original_source=original_source,
        findings=findings,
        decision=decision,
    )
    predecessor_dependency = manifest.get("predecessor_review_dependency")
    if (
        status.get("state") != "SEALED"
        or not isinstance(status.get("period_id"), str)
        or not status["period_id"]
        or request.get("admission_status")
        != ("REFUSED" if status.get("business_state") == "REFUSED" else "ADMITTED")
    ):
        raise VerificationError("TRANSACTION_STATUS_BINDING_INVALID")

    expected_refs = [
        {
            "object_id": "SOURCE-ORIGINAL",
            "path": "source/original.bin",
            "sha256": source_sha,
        },
        {
            "object_id": "RAW-CANDIDATE",
            "path": "06_RAW_CANDIDATE_CAPTURE.bin",
            "sha256": raw_sha,
        },
    ]
    if any(row.get("evidence_refs") != expected_refs for row in control_rows):
        raise VerificationError("CONTROL_EVIDENCE_REFERENCE_BINDING_INVALID")

    finding_ids: list[str] = []
    for row in findings:
        finding_id = row.get("finding_id")
        if (
            row.get("transaction_id") != transaction_id
            or not isinstance(finding_id, str)
            or not finding_id
            or row.get("status") != "OPEN"
            or row.get("authority_effect") != AUTHORITY_EFFECT
            or not isinstance(row.get("evidence_refs"), list)
            or row.get("origin")
            not in {"VERSIONED_CONTROL_EXECUTION", "INDEPENDENT_REVIEW_POLICY"}
            or set(row)
            != {
                "affected_controls",
                "authority_effect",
                "due_date",
                "evidence_refs",
                "finding_class",
                "finding_id",
                "origin",
                "owner",
                "resolution",
                "risk_posture",
                "status",
                "summary",
                "supersedes",
                "transaction_id",
            }
        ):
            raise VerificationError("FINDING_IDENTITY_INVALID")
        finding_ids.append(finding_id)
    if finding_ids != sorted(set(finding_ids)):
        raise VerificationError("FINDING_ORDER_OR_DUPLICATE_INVALID")
    observed_control_findings = [
        row for row in findings if row.get("origin") == "VERSIONED_CONTROL_EXECUTION"
    ]
    if observed_control_findings != _expected_control_derived_findings(
        transaction_id, control_rows
    ):
        raise VerificationError("CONTROL_DERIVED_FINDINGS_BINDING_INVALID")
    if (
        review.get("transaction_id") != transaction_id
        or review.get("finding_count") != len(findings)
        or review.get("finding_ids") != finding_ids
        or orientation.get("transaction_id") != transaction_id
        or orientation.get("finding_count") != len(findings)
        or orientation.get("management_attention") is not bool(findings)
    ):
        raise VerificationError("REVIEW_FINDING_BINDING_INVALID")

    selected = decision.get("selected_finding_ids", [])
    if (
        decision.get("transaction_id") != transaction_id
        or not isinstance(selected, list)
        or selected != sorted(set(selected))
        or not set(selected).issubset(finding_ids)
        or (decision.get("decision") == "REQUEST_REPAIR" and not selected)
        or (decision.get("decision") != "REQUEST_REPAIR" and selected)
    ):
        raise VerificationError("HUMAN_DECISION_FINDING_BINDING_INVALID")
    binding_open = [
        row
        for row in findings
        if row.get("finding_class")
        in {"BINDING_FINDING", "CONTROL_EXCEPTION", "SYSTEM_ERROR", "POLICY_REFUSAL"}
    ]
    p0_blocking = [
        row
        for row in control_rows
        if row.get("control_id") not in P1
        and isinstance(row.get("expected_condition"), Mapping)
        and row["expected_condition"].get("applicability") == "APPLICABLE"
        and row.get("result") in {"FAIL", "HOLD", "ERROR"}
    ]
    if (
        decision.get("decision") == "APPROVE"
        and (
            binding_open
            or p0_blocking
            or (
                review_policy.approval_effect is ApprovalEffect.BINDING
                and bool(findings)
            )
        )
    ):
        raise VerificationError("HUMAN_DECISION_APPROVAL_POLICY_INVALID")
    if (
        decision.get("decision") == "REQUEST_REPAIR"
        and review_policy.repair_selection_supported is not True
    ):
        raise VerificationError("HUMAN_DECISION_REPAIR_POLICY_INVALID")
    if decision.get("decision") == "PENDING":
        if status.get("business_state") != "REFUSED":
            raise VerificationError("HUMAN_DECISION_STATUS_BINDING_INVALID")
    elif status.get("business_state") != decision.get("decision"):
        raise VerificationError("HUMAN_DECISION_STATUS_BINDING_INVALID")

    if (
        manifest.get("created_at_utc") != status.get("created_at_utc")
        or manifest.get("finalized_at_utc") != status.get("finalized_at_utc")
        or manifest.get("parent_transaction_id")
        != status.get("parent_transaction_id")
        or manifest.get("state") != status.get("business_state")
        or manifest.get("segregation_posture")
        != status.get("segregation_posture")
        or manifest.get("signing_posture") != status.get("signing_posture")
        or not isinstance(predecessor_dependency, Mapping)
        or predecessor_dependency.get("status") != "HOLD"
    ):
        raise VerificationError("PACKAGE_MANIFEST_STATUS_BINDING_INVALID")
    for row in (system, request, source, configuration, invocation, claim_map):
        if row.get("transaction_id") != transaction_id or row.get("authority_effect") != AUTHORITY_EFFECT:
            raise VerificationError("RECORD_TRANSACTION_ID_OR_AUTHORITY_INVALID")
    return findings, decision


def _verify_custody_semantics(
    rows: list[dict[str, Any]],
    transaction_id: str,
    payloads: Mapping[str, bytes],
) -> None:
    """Bind the valid chain to this package and replay its state transitions."""

    first = rows[0]
    initial_configuration = _json(payloads['04_PROMPT_AND_CONFIGURATION_MANIFEST.json'],'CONFIGURATION_MANIFEST_INVALID')
    non_model_event = initial_configuration.get('settings',{}).get('processing_kind')=='NON_MODEL_EVENT'
    if (
        first.get("ledger_id") != f"ledger_{transaction_id}"
        or first.get("transaction_id") != transaction_id
        or first.get("actor_class") != "SERVICE_INGRESS"
        or first.get("actor_id") != "SERVICE-INGRESS"
        or first.get("plane") != "INGRESS_QUARANTINE"
        or first.get("reason_codes") != (["NON_MODEL_EVENT_ROUTE"] if non_model_event else ["CAPTURED_OUTPUT_ROUTE"])
        or first.get("result") != "PASS"
        or first.get("authority_effect") != AUTHORITY_EFFECT
        or first.get("side_effects") != ZERO_SIDE_EFFECTS
        or first.get("operation") != "TRANSACTION_CREATED"
        or first.get("subject_type") != "TRANSACTION"
        or first.get("subject_id") != transaction_id
        or set(first.get("output_digests", {}))
        != {
            "quarantine/candidate.bin",
            "quarantine/source.bin",
            "quarantine/source.normalized",
            "transaction.json",
        }
        or first["output_digests"].get("quarantine/candidate.bin")
        != sha256_bytes(payloads["06_RAW_CANDIDATE_CAPTURE.bin"])
        or first["output_digests"].get("quarantine/source.bin")
        != sha256_bytes(payloads["source/original.bin"])
        or first["output_digests"].get("quarantine/source.normalized")
        != sha256_bytes(payloads["source/normalized.txt"])
    ):
        raise VerificationError("CUSTODY_PACKAGE_IDENTITY_INVALID")
    status = _json(
        payloads["00_STATUS_AND_NONASSURANCE.json"], "STATUS_RECORD_INVALID"
    )
    parent_transaction_id = status.get("parent_transaction_id")
    root_transaction_id = transaction_id
    if parent_transaction_id is not None:
        if "13_REPAIR_LINEAGE.json" not in payloads:
            raise VerificationError("CUSTODY_INITIAL_STATE_IDENTITY_INVALID")
        lineage = _json(
            payloads["13_REPAIR_LINEAGE.json"], "REPAIR_LINEAGE_INVALID"
        )
        root_transaction_id = lineage.get("root_transaction_id")
        if (
            lineage.get("child_transaction_id") != transaction_id
            or lineage.get("parent_transaction_id") != parent_transaction_id
            or not isinstance(root_transaction_id, str)
            or not root_transaction_id
        ):
            raise VerificationError("CUSTODY_INITIAL_STATE_IDENTITY_INVALID")
    created_at = status.get("created_at_utc")
    if not isinstance(created_at, str):
        raise VerificationError("CUSTODY_INITIAL_STATE_TIME_INVALID")
    try:
        last_logical_time = datetime.fromisoformat(created_at[:-1] + "+00:00")
    except (TypeError, ValueError) as exc:
        raise VerificationError("CUSTODY_INITIAL_STATE_TIME_INVALID") from exc
    if (
        not created_at.endswith("Z")
        or last_logical_time.tzinfo is None
        or last_logical_time.utcoffset() != timezone.utc.utcoffset(last_logical_time)
        or first.get("logical_time") != created_at
        or first.get("input_digests") != {}
    ):
        raise VerificationError("CUSTODY_INITIAL_STATE_TIME_INVALID")
    current_state: dict[str, Any] = {
        "authority_effect": AUTHORITY_EFFECT,
        "current_state": TransactionState.CREATED.value,
        "last_transition_id": None,
        "logical_time_utc": created_at,
        "parent_transaction_id": parent_transaction_id,
        "root_transaction_id": root_transaction_id,
        "schema_id": "uvlm.triadicbrain.aep01.transaction_state.v1",
        "sequence": 0,
        "transaction_id": transaction_id,
    }
    current = TransactionState.CREATED
    current_state_digest = sha256_bytes(canonical_bytes(current_state))
    system = _json(
        payloads["01_AI_SYSTEM_IDENTITY.json"], "SYSTEM_IDENTITY_INVALID"
    )
    source_record = _json(
        payloads["03_SOURCE_AND_RETRIEVAL_MANIFEST.json"],
        "SOURCE_MANIFEST_INVALID",
    )
    configuration = _json(
        payloads["04_PROMPT_AND_CONFIGURATION_MANIFEST.json"],
        "CONFIGURATION_MANIFEST_INVALID",
    )
    invocation = _json(
        payloads["05_MODEL_INVOCATION_RECORD.json"],
        "MODEL_INVOCATION_RECORD_INVALID",
    )
    control_rows = _jsonl(
        payloads["08_CONTROL_EXECUTION_RESULTS.jsonl"],
        "CONTROL_RESULTS_INVALID",
    )
    operations = [row.get("operation") for row in rows]
    candidate_captured = any(
        operation == "STATE_TRANSITION:CANDIDATE_PENDING->CANDIDATE_CAPTURED"
        for operation in operations
    )
    candidate_failed = any(
        operation == "STATE_TRANSITION:CANDIDATE_PENDING->CANDIDATE_FAILED"
        for operation in operations
    )
    if candidate_captured and candidate_failed:
        raise VerificationError("CUSTODY_CANDIDATE_ROUTE_INVALID")
    event_bound = 'STATE_TRANSITION:INPUTS_BOUND->OBSERVED_EVENT_BOUND' in operations
    if event_bound != non_model_event or (event_bound and (candidate_captured or candidate_failed)):
        raise VerificationError('CUSTODY_EVENT_ROUTE_INVALID')
    applicable_controls = sorted(
        str(row["control_id"])
        for row in control_rows
        if row.get("control_id") in P0_WHEN_APPLICABLE
        and isinstance(row.get("expected_condition"), Mapping)
        and row["expected_condition"].get("applicability") == "APPLICABLE"
    )
    prompt_components = configuration.get("prompt_components")
    transaction_record = {
        "applicable_controls": applicable_controls,
        "authority_effect": AUTHORITY_EFFECT,
        "candidate_captured": candidate_captured,
        "candidate_sha256": sha256_bytes(payloads["06_RAW_CANDIDATE_CAPTURE.bin"]),
        "created_at_utc": created_at,
        "identity": {
            "parent_transaction_id": parent_transaction_id,
            "root_transaction_id": root_transaction_id,
            "transaction_id": transaction_id,
        },
        "model_identity": invocation.get("model_identity"),
        "normalization_profile": source_record.get("normalization_profile"),
        "normalized_source_sha256": sha256_bytes(payloads["source/normalized.txt"]),
        "period_id": status.get("period_id"),
        "prompt": (
            prompt_components[0].get("text")
            if isinstance(prompt_components, list)
            and len(prompt_components) == 1
            and isinstance(prompt_components[0], Mapping)
            else None
        ),
        "review_policy": configuration.get("review_policy"),
        "schema_id": "uvlm.triadicbrain.aep01.transaction_registration.v1",
        "settings": configuration.get("settings"),
        "source_media_type": source_record.get("source_media_type"),
        "source_sha256": sha256_bytes(payloads["source/original.bin"]),
        "system_id": system.get("system_id"),
        "transaction_id": transaction_id,
        "use_case_id": system.get("use_case_id"),
    }
    if first.get("output_digests", {}).get("transaction.json") != sha256_bytes(
        canonical_bytes(transaction_record)
    ):
        raise VerificationError("CUSTODY_TRANSACTION_RECORD_BINDING_INVALID")
    decision_record = _json(
        payloads["12_HUMAN_DECISION.json"], "HUMAN_DECISION_INVALID"
    )
    for event in rows[1:]:
        if (
            event.get("ledger_id") != f"ledger_{transaction_id}"
            or event.get("transaction_id") != transaction_id
        ):
            raise VerificationError("CUSTODY_PACKAGE_IDENTITY_INVALID")
        operation = event.get("operation")
        if isinstance(operation, str) and operation.startswith("STATE_TRANSITION:"):
            try:
                route = operation.removeprefix("STATE_TRANSITION:")
                source_value, target_value = route.split("->", 1)
                source_state = TransactionState(source_value)
                target_state = validate_transition(source_state, target_value)
            except (TypeError, ValueError) as exc:
                raise VerificationError("CUSTODY_TRANSITION_INVALID") from exc
            logical_time = event.get("logical_time")
            try:
                parsed_logical_time = datetime.fromisoformat(
                    logical_time[:-1] + "+00:00"
                )
            except (AttributeError, TypeError, ValueError) as exc:
                raise VerificationError("CUSTODY_TRANSITION_TIME_INVALID") from exc
            if (
                not logical_time.endswith("Z")
                or parsed_logical_time.tzinfo is None
                or parsed_logical_time.utcoffset()
                != timezone.utc.utcoffset(parsed_logical_time)
                or parsed_logical_time < last_logical_time
            ):
                raise VerificationError("CUSTODY_TRANSITION_TIME_INVALID")
            transition_id = f"tr_{sha256_bytes(canonical_bytes({
                'from': source_state.value,
                'sequence': event.get('sequence'),
                'to': target_state.value,
                'transaction_id': transaction_id,
            }))[:32]}"
            expected_state = {
                **current_state,
                "current_state": target_state.value,
                "last_transition_id": transition_id,
                "logical_time_utc": logical_time,
                "sequence": current_state["sequence"] + 1,
            }
            expected_state_digest = sha256_bytes(canonical_bytes(expected_state))
            expected_outputs = {"state.json"}
            route_evidence = {
                (
                    TransactionState.CONTROLS_PENDING,
                    TransactionState.CONTROLS_COMPLETE,
                ): {
                    "review/control_results.jsonl": "08_CONTROL_EXECUTION_RESULTS.jsonl"
                },
                (
                    TransactionState.CONTROLS_COMPLETE,
                    TransactionState.SOPHIA_COMPLETE,
                ): {
                    "review/findings.jsonl": "09_FINDINGS_AND_EXCEPTIONS.jsonl",
                    "review/independent_review.json": "10_SOPHIA_AUDIT_PACKET.json",
                },
                (
                    TransactionState.SOPHIA_COMPLETE,
                    TransactionState.ATLAS_COMPLETE,
                ): {"review/orientation.json": "11_ATLAS_POSTURE_PACKET.json"},
            }
            for evidence_name, package_name in route_evidence.get(
                (source_state, target_state), {}
            ).items():
                expected_outputs.add(evidence_name)
                if event.get("output_digests", {}).get(evidence_name) != sha256_bytes(
                    payloads[package_name]
                ):
                    raise VerificationError("CUSTODY_ROUTE_EVIDENCE_BINDING_INVALID")
            if source_state is TransactionState.HUMAN_DECISION_PENDING:
                expected_outputs.add("review/human_decision.json")
                if event.get("output_digests", {}).get(
                    "review/human_decision.json"
                ) != sha256_bytes(payloads["12_HUMAN_DECISION.json"]):
                    raise VerificationError("CUSTODY_DECISION_BINDING_INVALID")
                if (
                    target_state is TransactionState.REPAIR_REQUESTED
                    and "22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json" in payloads
                ):
                    expected_outputs.add(
                        "review/review_policy_repair_authorization.json"
                    )
                    if event.get("output_digests", {}).get(
                        "review/review_policy_repair_authorization.json"
                    ) != sha256_bytes(
                        payloads["22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json"]
                    ):
                        raise VerificationError(
                            "CUSTODY_REVIEW_POLICY_REPAIR_BINDING_INVALID"
                        )
            if source_state is TransactionState.REPAIR_REQUESTED:
                expected_outputs.add("review/repair_lineage.json")
                if (
                    "13_REPAIR_LINEAGE.json" not in payloads
                    or event.get("output_digests", {}).get(
                        "review/repair_lineage.json"
                    )
                    != sha256_bytes(payloads["13_REPAIR_LINEAGE.json"])
                ):
                    raise VerificationError("CUSTODY_REPAIR_BINDING_INVALID")
            if (
                source_state is TransactionState.FINALIZATION_PENDING
                and target_state is TransactionState.SEALED
            ):
                expected_outputs.add("evidence_content_root")
                content_rows = [
                    {
                        "bytes": len(payload),
                        "path": name,
                        "sha256": sha256_bytes(payload),
                    }
                    for name, payload in sorted(payloads.items())
                    if name != "14_CUSTODY_EVENTS.jsonl"
                    and name not in CONTROL_MEMBERS
                ]
                if event.get("output_digests", {}).get(
                    "evidence_content_root"
                ) != sha256_bytes(canonical_bytes(content_rows)):
                    raise VerificationError("CUSTODY_CONTENT_ROOT_INVALID")
            if (
                source_state is not current
                or event.get("subject_type") != "TRANSACTION"
                or event.get("subject_id") != transaction_id
                or set(event.get("input_digests", {})) != {"state.json"}
                or set(event.get("output_digests", {})) != expected_outputs
                or event.get("input_digests", {}).get("state.json")
                != current_state_digest
                or event.get("output_digests", {}).get("state.json")
                != expected_state_digest
            ):
                raise VerificationError("CUSTODY_TRANSITION_INVALID")
            decision_actor_id = None
            if source_state is TransactionState.HUMAN_DECISION_PENDING:
                decision_actor_id = decision_record.get("actor_id")
                decision_targets = {
                    "APPROVE": TransactionState.APPROVED,
                    "HOLD": TransactionState.HELD,
                    "REJECT": TransactionState.REJECTED,
                    "REQUEST_REPAIR": TransactionState.REPAIR_REQUESTED,
                }
                if (
                    decision_targets.get(decision_record.get("decision"))
                    is not target_state
                    or decision_record.get("decision_time_utc")
                    != event.get("logical_time")
                ):
                    raise VerificationError("CUSTODY_DECISION_TRANSITION_INVALID")
            try:
                validate_transition_event_semantics(
                    event,
                    source_state,
                    target_state,
                    decision_actor_id=decision_actor_id,
                )
            except TransitionPolicyError as exc:
                raise VerificationError("CUSTODY_TRANSITION_ACTOR_POLICY_INVALID") from exc
            current = target_state
            current_state = expected_state
            current_state_digest = expected_state_digest
            last_logical_time = parsed_logical_time
        elif operation == "RECOVER_INTERRUPTED_TRANSITION":
            receipt_name = f"recovery/{event.get('subject_id')}.json"
            if (
                event.get("subject_type") != "TRANSITION"
                or not isinstance(event.get("subject_id"), str)
                or not event["subject_id"].startswith("tr_")
                or set(event.get("input_digests", {})) != {"pending_journal"}
                or set(event.get("output_digests", {}))
                != {"recovery_receipt", "state.json"}
                or receipt_name not in payloads
                or event.get("output_digests", {}).get("recovery_receipt")
                != sha256_bytes(payloads[receipt_name])
                or current_state_digest is None
                or event.get("output_digests", {}).get("state.json")
                != current_state_digest
            ):
                raise VerificationError("CUSTODY_RECOVERY_EVENT_INVALID")
            try:
                validate_recovery_event_semantics(event)
            except TransitionPolicyError as exc:
                raise VerificationError("CUSTODY_RECOVERY_ACTOR_POLICY_INVALID") from exc
        else:
            raise VerificationError("CUSTODY_OPERATION_INVALID")
    if (
        current is not TransactionState.SEALED
        or rows[-1].get("operation")
        != "STATE_TRANSITION:FINALIZATION_PENDING->SEALED"
    ):
        raise VerificationError("CUSTODY_FINAL_STATE_INVALID")


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _verify_repair_lineage(
    payloads: Mapping[str, bytes],
    transaction_id: str,
    decision: Mapping[str, Any],
) -> None:
    if "13_REPAIR_LINEAGE.json" not in payloads:
        return
    repair = _json(payloads["13_REPAIR_LINEAGE.json"], "REPAIR_LINEAGE_INVALID")
    fields = {
        "authority_effect",
        "changed_inputs",
        "child_transaction_id",
        "execution_posture",
        "inherited_inputs",
        "input_comparison",
        "nonauthority",
        "parent_decision_id",
        "parent_evidence",
        "parent_transaction_id",
        "repair_intent_sha256",
        "resolved_finding_ids",
        "resulting_evidence",
        "root_transaction_id",
        "schema_id",
        "selected_finding_ids",
    }
    if (
        set(repair) != fields
        or repair.get("schema_id") != "uvlm.triadicbrain.aep01.repair_lineage.v1"
        or repair.get("authority_effect") != AUTHORITY_EFFECT
        or repair.get("execution_posture") != "REAL_CAPTURED_OUTPUT_CHILD_ROUTE"
        or repair.get("inherited_inputs")
        != ["model_identity", "period_id", "review_policy", "system_id", "use_case_id"]
        or repair.get("resolved_finding_ids") != []
    ):
        raise VerificationError("REPAIR_LINEAGE_SEMANTICS_INVALID")
    parent_id = repair.get("parent_transaction_id")
    child_id = repair.get("child_transaction_id")
    root_id = repair.get("root_transaction_id")
    selected = repair.get("selected_finding_ids")
    changed = repair.get("changed_inputs")
    if (
        type(parent_id) is not str
        or type(child_id) is not str
        or type(root_id) is not str
        or parent_id == child_id
        or transaction_id not in {parent_id, child_id}
        or not isinstance(selected, list)
        or not selected
        or selected != sorted(set(selected))
        or not isinstance(changed, list)
        or not changed
        or changed != sorted(set(changed))
    ):
        raise VerificationError("REPAIR_LINEAGE_IDENTITY_INVALID")
    comparison = repair.get("input_comparison")
    if not isinstance(comparison, Mapping) or set(comparison) != {
        "candidate",
        "prompt",
        "settings",
        "source",
    }:
        raise VerificationError("REPAIR_LINEAGE_COMPARISON_INVALID")
    observed_changed: list[str] = []
    for name in ("candidate", "prompt", "settings", "source"):
        row = comparison[name]
        if (
            not isinstance(row, Mapping)
            or set(row) != {"changed", "child_sha256", "parent_sha256"}
            or type(row.get("changed")) is not bool
            or not _is_sha256(row.get("child_sha256"))
            or not _is_sha256(row.get("parent_sha256"))
            or (row["changed"] is (row["child_sha256"] == row["parent_sha256"]))
        ):
            raise VerificationError("REPAIR_LINEAGE_COMPARISON_INVALID")
        if row["changed"]:
            observed_changed.append(name)
    if changed != observed_changed:
        raise VerificationError("REPAIR_LINEAGE_CHANGED_INPUTS_INVALID")
    parent_evidence = repair.get("parent_evidence")
    resulting = repair.get("resulting_evidence")
    if (
        not isinstance(parent_evidence, Mapping)
        or set(parent_evidence)
        != {
            "candidate_sha256",
            "control_results_sha256",
            "decision_sha256",
            "findings_sha256",
        }
        or not all(_is_sha256(value) for value in parent_evidence.values())
        or not isinstance(resulting, Mapping)
        or set(resulting)
        != {
            "candidate_sha256",
            "control_results_sha256",
            "findings_sha256",
            "transaction_record_sha256",
        }
        or not all(_is_sha256(value) for value in resulting.values())
    ):
        raise VerificationError("REPAIR_LINEAGE_EVIDENCE_INVALID")
    configuration = _json(
        payloads["04_PROMPT_AND_CONFIGURATION_MANIFEST.json"],
        "CONFIGURATION_MANIFEST_INVALID",
    )
    prompt = configuration["prompt_components"][0]["text"]
    settings = dict(configuration["settings"])
    current_digests = {
        "candidate": sha256_bytes(payloads["06_RAW_CANDIDATE_CAPTURE.bin"]),
        "prompt": sha256_bytes(canonical_bytes({"value": prompt})),
        "settings": sha256_bytes(canonical_bytes({"value": settings})),
        "source": sha256_bytes(payloads["source/original.bin"]),
    }
    side = "parent_sha256" if transaction_id == parent_id else "child_sha256"
    if any(comparison[name][side] != digest for name, digest in current_digests.items()):
        raise VerificationError("REPAIR_LINEAGE_CURRENT_INPUT_BINDING_INVALID")
    if transaction_id == parent_id:
        if (
            decision.get("decision") != "REQUEST_REPAIR"
            or decision.get("decision_id") != repair.get("parent_decision_id")
            or decision.get("selected_finding_ids") != selected
            or parent_evidence
            != {
                "candidate_sha256": current_digests["candidate"],
                "control_results_sha256": sha256_bytes(
                    payloads["08_CONTROL_EXECUTION_RESULTS.jsonl"]
                ),
                "decision_sha256": sha256_bytes(payloads["12_HUMAN_DECISION.json"]),
                "findings_sha256": sha256_bytes(
                    payloads["09_FINDINGS_AND_EXCEPTIONS.jsonl"]
                ),
            }
        ):
            raise VerificationError("REPAIR_LINEAGE_PARENT_BINDING_INVALID")
    else:
        if (
            resulting.get("candidate_sha256") != current_digests["candidate"]
            or resulting.get("control_results_sha256")
            != sha256_bytes(payloads["08_CONTROL_EXECUTION_RESULTS.jsonl"])
            or resulting.get("findings_sha256")
            != sha256_bytes(payloads["09_FINDINGS_AND_EXCEPTIONS.jsonl"])
        ):
            raise VerificationError("REPAIR_LINEAGE_CHILD_BINDING_INVALID")
    intent = {
        "authority_effect": AUTHORITY_EFFECT,
        "changed_inputs": changed,
        "child_transaction_id": child_id,
        "input_comparison": dict(comparison),
        "parent_decision_id": repair.get("parent_decision_id"),
        "parent_evidence": dict(parent_evidence),
        "parent_transaction_id": parent_id,
        "root_transaction_id": root_id,
        "schema_id": "uvlm.triadicbrain.aep01.repair_intent.v1",
        "selected_finding_ids": selected,
    }
    if repair.get("repair_intent_sha256") != sha256_bytes(canonical_bytes(intent)):
        raise VerificationError("REPAIR_INTENT_DIGEST_INVALID")


def _verify_recovery_receipts(
    payloads: Mapping[str, bytes],
    transaction_id: str,
    recovery_names: set[str],
    custody_rows: list[dict[str, Any]],
) -> None:
    recovery_events = [
        row
        for row in custody_rows
        if row.get("operation") == "RECOVER_INTERRUPTED_TRANSITION"
    ]
    event_ids = [row.get("subject_id") for row in recovery_events]
    if len(event_ids) != len(set(event_ids)):
        raise VerificationError("RECOVERY_EVENT_DUPLICATE")
    expected_names = {f"recovery/{event_id}.json" for event_id in event_ids}
    if recovery_names != expected_names:
        raise VerificationError("RECOVERY_RECEIPT_EVENT_TOPOLOGY_INVALID")
    for event in recovery_events:
        transition_id = event["subject_id"]
        name = f"recovery/{transition_id}.json"
        recovery = _json(payloads[name], "RECOVERY_RECEIPT_INVALID")
        observation = recovery.get("journal_observation")
        event_index = custody_rows.index(event)
        if event_index == 0:
            raise VerificationError("RECOVERY_EVENT_PREDECESSOR_INVALID")
        predecessor = custody_rows[event_index - 1]
        predecessor_operation = predecessor.get("operation")
        if (
            not isinstance(predecessor_operation, str)
            or not predecessor_operation.startswith("STATE_TRANSITION:")
        ):
            raise VerificationError("RECOVERY_EVENT_PREDECESSOR_INVALID")
        try:
            route = predecessor_operation.removeprefix("STATE_TRANSITION:")
            source_value, target_value = route.split("->", 1)
            source_state = TransactionState(source_value)
            target_state = validate_transition(source_state, target_value)
        except (TypeError, ValueError) as exc:
            raise VerificationError("RECOVERY_EVENT_PREDECESSOR_INVALID") from exc
        expected_transition_id = f"tr_{sha256_bytes(canonical_bytes({
            'from': source_state.value,
            'sequence': predecessor.get('sequence'),
            'to': target_state.value,
            'transaction_id': transaction_id,
        }))[:32]}"
        original_targets = []
        if source_state is TransactionState.HUMAN_DECISION_PENDING:
            original_targets.append("review/human_decision.json")
        if source_state is TransactionState.REPAIR_REQUESTED:
            original_targets.append("review/repair_lineage.json")
        original_targets.extend(("state.json", "custody_events.jsonl"))
        if (
            set(recovery)
            != {
                "authority_effect",
                "journal_observation",
                "nonauthority",
                "result",
                "schema_id",
                "transaction_id",
                "transition_id",
            }
            or recovery.get("schema_id")
            != "uvlm.triadicbrain.aep01.transition_recovery_receipt.v1"
            or recovery.get("transaction_id") != transaction_id
            or recovery.get("transition_id") != transition_id
            or transition_id != expected_transition_id
            or recovery.get("authority_effect") != AUTHORITY_EFFECT
            or recovery.get("result") != "RECOVERED"
            or not isinstance(observation, Mapping)
            or set(observation)
            != {
                "applied_target_prefix_count",
                "cause_posture",
                "next_pending_target_path",
                "pending_journal_sha256",
                "pending_transition_id",
                "target_count",
            }
            or observation.get("pending_transition_id") != transition_id
            or observation.get("cause_posture") != "UNOBSERVED_PROCESS_INTERRUPTION"
            or not _is_sha256(observation.get("pending_journal_sha256"))
            or type(observation.get("applied_target_prefix_count")) is not int
            or type(observation.get("target_count")) is not int
            or not 0
            <= observation["applied_target_prefix_count"]
            <= observation["target_count"]
            or event.get("input_digests")
            != {"pending_journal": observation["pending_journal_sha256"]}
            or event.get("output_digests", {}).get("recovery_receipt")
            != sha256_bytes(payloads[name])
            or event.get("logical_time") != predecessor.get("logical_time")
            or observation.get("target_count") != len(original_targets)
        ):
            raise VerificationError("RECOVERY_RECEIPT_BINDING_INVALID")
        next_path = observation.get("next_pending_target_path")
        prefix = observation["applied_target_prefix_count"]
        expected_next = original_targets[prefix] if prefix < len(original_targets) else None
        if next_path != expected_next:
            raise VerificationError("RECOVERY_RECEIPT_NEXT_TARGET_INVALID")


def _verify_payloads(
    payloads: Mapping[str, bytes],
    *,
    source: str,
    package_location: Path | None = None,
) -> dict[str, Any]:
    if len(payloads) > MAX_PACKAGE_FILES or sum(map(len, payloads.values())) > MAX_PACKAGE_BYTES:
        raise VerificationError("PACKAGE_BOUNDS_EXCEEDED")
    names = list(payloads)
    folded: set[str] = set()
    for name in names:
        _safe_member(name)
        key = unicodedata.normalize("NFC", name).casefold()
        if key in folded:
            raise VerificationError("PACKAGE_MEMBER_COLLISION")
        folded.add(key)

    expected = set(CORE_CONTENT_MEMBERS) | set(CONTROL_MEMBERS)
    if "13_REPAIR_LINEAGE.json" in payloads:
        expected.add("13_REPAIR_LINEAGE.json")
    for optional_policy_member in (
        "21_REVIEW_POLICY_EVALUATION.json",
        "22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json",
    ):
        if optional_policy_member in payloads:
            expected.add(optional_policy_member)
    recovery_names = {
        name
        for name in payloads
        if name.startswith("recovery/") and name.endswith(".json")
    }
    if any(
        len(PurePosixPath(name).parts) != 2
        or not PurePosixPath(name).name.startswith("tr_")
        for name in recovery_names
    ):
        raise VerificationError("RECOVERY_RECEIPT_PATH_INVALID")
    expected.update(recovery_names)
    if set(payloads) != expected:
        raise VerificationError("PACKAGE_TOPOLOGY_INVALID")

    status = _json(payloads["00_STATUS_AND_NONASSURANCE.json"], "STATUS_RECORD_INVALID")
    transaction_id = status.get("transaction_id")
    if set(status) != {
        "authority_effect",
        "business_state",
        "created_at_utc",
        "finalized_at_utc",
        "nonauthority",
        "notice",
        "parent_transaction_id",
        "period_id",
        "report_notice",
        "schema_id",
        "segregation_posture",
        "signing_posture",
        "state",
        "transaction_id",
    }:
        raise VerificationError("STATUS_RECORD_FIELDS_INVALID")
    if not isinstance(transaction_id, str) or not transaction_id:
        raise VerificationError("TRANSACTION_ID_INVALID")
    if status.get("authority_effect") != AUTHORITY_EFFECT:
        raise VerificationError("STATUS_AUTHORITY_INVALID")
    if (
        NONASSURANCE_NOTICE not in str(status.get("notice", ""))
        or status.get("report_notice") != REPORT_NOTICE
    ):
        raise VerificationError("NONASSURANCE_NOTICE_MISSING")

    manifest = _json(
        payloads["15_EVIDENCE_PACKAGE_MANIFEST.json"], "PACKAGE_MANIFEST_INVALID"
    )
    try:
        validate_instance(manifest)
    except SchemaValidationError as exc:
        raise VerificationError("PACKAGE_MANIFEST_SCHEMA_INVALID") from exc
    content = {
        name: payload
        for name, payload in payloads.items()
        if name not in CONTROL_MEMBERS
    }
    rows = _member_rows(content)
    if manifest.get("members") != rows:
        raise VerificationError("PACKAGE_MANIFEST_MEMBER_BINDING_INVALID")
    package_root = sha256_bytes(canonical_bytes(rows))
    if (
        manifest.get("package_root_sha256") != package_root
        or manifest.get("transaction_id") != transaction_id
        or manifest.get("authority_effect") != AUTHORITY_EFFECT
        or manifest.get("schema_id")
        != "uvlm.triadicbrain.aep01.evidence_package_manifest.v1"
        or manifest.get("finalized") is not True
        or manifest.get("effects")
        != {
            "memory_written": False,
            "network_used": False,
            "provider_invoked": False,
            "publication_performed": False,
        }
        or REPORT_NOTICE not in str(manifest.get("nonauthority", ""))
    ):
        raise VerificationError("PACKAGE_MANIFEST_IDENTITY_INVALID")

    checksums = _checksum_map(payloads["16_SHA256SUMS.txt"])
    checksum_scope = set(content) | {"15_EVIDENCE_PACKAGE_MANIFEST.json"}
    if set(checksums) != checksum_scope:
        raise VerificationError("CHECKSUM_SCOPE_INVALID")
    for name, digest in checksums.items():
        if sha256_bytes(payloads[name]) != digest:
            raise VerificationError("CHECKSUM_MISMATCH")

    receipt = _json(payloads["17_VERIFICATION_RECEIPT.json"], "VERIFICATION_RECEIPT_INVALID")
    if receipt != {
        "authority_effect": AUTHORITY_EFFECT,
        "checksums_sha256": sha256_bytes(payloads["16_SHA256SUMS.txt"]),
        "manifest_sha256": sha256_bytes(payloads["15_EVIDENCE_PACKAGE_MANIFEST.json"]),
        "model_or_provider_required": False,
        "nonauthority": NONASSURANCE_NOTICE,
        "package_root_sha256": package_root,
        "report_notice": REPORT_NOTICE,
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.verification_receipt.v1",
        "transaction_id": transaction_id,
        "verification_scope": "DECLARED_MEMBERS_CHECKSUMS_AND_CUSTODY_IDENTITY_ONLY",
    }:
        raise VerificationError("VERIFICATION_RECEIPT_BINDING_INVALID")

    control_rows = _verify_control_rows(
        payloads["08_CONTROL_EXECUTION_RESULTS.jsonl"], transaction_id
    )
    finding_rows, decision_record = _verify_cross_record_bindings(
        payloads,
        transaction_id=transaction_id,
        status=status,
        manifest=manifest,
        control_rows=control_rows,
    )
    custody_rows = _jsonl(payloads["14_CUSTODY_EVENTS.jsonl"], "CUSTODY_LEDGER_INVALID")
    custody_receipt = verify_events(custody_rows)
    if (
        custody_receipt.get("result") != "PASS"
        or custody_receipt.get("transaction_id") != transaction_id
        or custody_receipt.get("ledger_id") != f"ledger_{transaction_id}"
    ):
        raise VerificationError("CUSTODY_CHAIN_INVALID")
    _verify_custody_semantics(custody_rows, transaction_id, payloads)
    for name in (
        "01_AI_SYSTEM_IDENTITY.json",
        "02_REQUEST_AUTHORITY_AND_CONSENT.json",
        "03_SOURCE_AND_RETRIEVAL_MANIFEST.json",
        "04_PROMPT_AND_CONFIGURATION_MANIFEST.json",
        "05_MODEL_INVOCATION_RECORD.json",
        "07_CANDIDATE_AND_CLAIM_MAP.json",
        "10_SOPHIA_AUDIT_PACKET.json",
        "11_ATLAS_POSTURE_PACKET.json",
        "12_HUMAN_DECISION.json",
    ):
        row = _json(payloads[name], f"CANONICAL_RECORD_INVALID:{name}")
        if row.get("transaction_id") != transaction_id:
            raise VerificationError(f"RECORD_TRANSACTION_ID_MISMATCH:{name}")
    for name in (
        "21_REVIEW_POLICY_EVALUATION.json",
        "22_REVIEW_POLICY_REPAIR_AUTHORIZATION.json",
    ):
        if name in payloads:
            row = _json(payloads[name], f"CANONICAL_RECORD_INVALID:{name}")
            if row.get("transaction_id") != transaction_id:
                raise VerificationError(f"RECORD_TRANSACTION_ID_MISMATCH:{name}")
    decision = _json(payloads["12_HUMAN_DECISION.json"], "HUMAN_DECISION_INVALID")
    if decision.get("decision") != "PENDING":
        reviewed = decision.get("parent_evidence_digests")
        if not isinstance(reviewed, Mapping) or reviewed != {
            "control_results_sha256": sha256_bytes(
                payloads["08_CONTROL_EXECUTION_RESULTS.jsonl"]
            ),
            "findings_sha256": sha256_bytes(
                payloads["09_FINDINGS_AND_EXCEPTIONS.jsonl"]
            ),
        }:
            raise VerificationError("HUMAN_DECISION_EVIDENCE_BINDING_INVALID")
    _verify_repair_lineage(payloads, transaction_id, decision)
    _verify_recovery_receipts(
        payloads,
        transaction_id,
        recovery_names,
        custody_rows,
    )
    _verify_live_review_policy(package_location, payloads)

    for name in ("09_FINDINGS_AND_EXCEPTIONS.jsonl",):
        _jsonl(payloads[name], f"CANONICAL_RECORD_INVALID:{name}")
    expected_html = render_transaction_review_html(
        transaction_id=transaction_id,
        business_state=str(status["business_state"]),
        open_findings=[row for row in finding_rows if row.get("status") == "OPEN"],
        product_name=PRODUCT_NAME,
    )
    if payloads["18_HUMAN_READABLE_REVIEW.html"] != expected_html:
        raise VerificationError("HTML_TRANSACTION_REPORT_BINDING_INVALID")
    if (
        payloads["19_FRAMEWORK_CROSSWALK_SNAPSHOT.csv"]
        != render_framework_crosswalk_csv()
        or payloads["20_CONTROL_CATALOG_SNAPSHOT.csv"]
        != render_control_catalog_csv()
    ):
        raise VerificationError("STATIC_CONTROL_SNAPSHOT_BINDING_INVALID")

    return {
        "authority_effect": AUTHORITY_EFFECT,
        "control_result_count": len(control_rows),
        "custody_event_count": len(custody_rows),
        "member_count": len(payloads),
        "model_or_provider_required": False,
        "nonauthority": NONASSURANCE_NOTICE,
        "package_root_sha256": package_root,
        "result": "PASS",
        "schema_id": "uvlm.triadicbrain.aep01.package_verification.v1",
        "source": source,
        "transaction_id": transaction_id,
    }


def verify_transaction_directory(package_directory: Path) -> dict[str, Any]:
    """Verify a closed on-disk package without writing or repairing it."""

    root = Path(package_directory)
    if not root.is_absolute() or not root.is_dir() or is_link_like(root):
        raise VerificationError("PACKAGE_DIRECTORY_INVALID")
    payloads: dict[str, bytes] = {}
    directories: set[str] = set()
    observed_keys: set[str] = set()
    total = 0
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise VerificationError("PACKAGE_DIRECTORY_ENUMERATION_FAILED") from exc
        if len(entries) > MAX_PACKAGE_FILES + MAX_PACKAGE_DIRECTORIES:
            raise VerificationError("PACKAGE_TOPOLOGY_BOUNDS_EXCEEDED")
        child_directories: list[Path] = []
        for entry in entries:
            path = Path(entry.path)
            require_safe_ancestors(path)
            try:
                before = path.lstat()
            except OSError as exc:
                raise VerificationError("PACKAGE_MEMBER_LSTAT_FAILED") from exc
            name = _safe_member(path.relative_to(root).as_posix())
            key = unicodedata.normalize("NFC", name).casefold()
            if key in observed_keys:
                raise VerificationError("PACKAGE_MEMBER_COLLISION")
            observed_keys.add(key)
            if stat.S_ISDIR(before.st_mode):
                if is_link_like(path):
                    raise VerificationError("PACKAGE_DIRECTORY_LINK_PROHIBITED")
                directories.add(name)
                if len(directories) > MAX_PACKAGE_DIRECTORIES:
                    raise VerificationError("PACKAGE_DIRECTORY_BOUNDS_EXCEEDED")
                child_directories.append(path)
                continue
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_nlink != 1
                or is_link_like(path)
            ):
                raise VerificationError("PACKAGE_MEMBER_IRREGULAR")
            if before.st_size < 0 or before.st_size > MAX_PACKAGE_BYTES:
                raise VerificationError("PACKAGE_BOUNDS_EXCEEDED")
            total += before.st_size
            if len(payloads) >= MAX_PACKAGE_FILES or total > MAX_PACKAGE_BYTES:
                raise VerificationError("PACKAGE_BOUNDS_EXCEEDED")
            try:
                payload = read_ordinary_bytes(
                    path, maximum_bytes=before.st_size
                )
            except (OSError, ValueError) as exc:
                raise VerificationError(
                    "PACKAGE_MEMBER_CHANGED_DURING_READ"
                ) from exc
            after = path.lstat()
            if (
                len(payload) != before.st_size
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
                raise VerificationError("PACKAGE_MEMBER_CHANGED_DURING_READ")
            payloads[name] = payload
        pending.extend(reversed(child_directories))
    expected_directories: set[str] = set()
    for name in payloads:
        parts = name.split("/")[:-1]
        for index in range(1, len(parts) + 1):
            expected_directories.add("/".join(parts[:index]))
    if directories != expected_directories:
        raise VerificationError("PACKAGE_DIRECTORY_TOPOLOGY_INVALID")
    return _verify_payloads(
        payloads, source="DIRECTORY", package_location=root
    )


def verify_transaction_zip(package_zip: Path) -> dict[str, Any]:
    """Verify a deterministic stored ZIP without extracting it."""

    path = Path(package_zip)
    require_safe_ancestors(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or is_link_like(path):
        raise VerificationError("PACKAGE_ZIP_INVALID")
    if before.st_size < 1 or before.st_size > MAX_PACKAGE_BYTES + 1024 * 1024:
        raise VerificationError("PACKAGE_ZIP_BOUNDS_EXCEEDED")
    try:
        raw = read_ordinary_bytes(
            path, maximum_bytes=MAX_PACKAGE_BYTES + 1024 * 1024
        )
    except (OSError, ValueError) as exc:
        raise VerificationError("PACKAGE_ZIP_CHANGED_DURING_READ") from exc
    after = path.lstat()
    if (
        len(raw) != before.st_size
        or (before.st_size, before.st_mtime_ns, before.st_nlink)
        != (after.st_size, after.st_mtime_ns, after.st_nlink)
        or is_link_like(path)
    ):
        raise VerificationError("PACKAGE_ZIP_CHANGED_DURING_READ")
    payloads: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(raw), "r") as archive:
        infos = archive.infolist()
        if len(infos) > MAX_PACKAGE_FILES or [info.filename for info in infos] != sorted(
            info.filename for info in infos
        ):
            raise VerificationError("PACKAGE_ZIP_ORDER_OR_BOUNDS_INVALID")
        folded: set[str] = set()
        total = 0
        for info in infos:
            name = _safe_member(info.filename)
            key = unicodedata.normalize("NFC", name).casefold()
            if key in folded or name in payloads:
                raise VerificationError("PACKAGE_ZIP_MEMBER_COLLISION")
            folded.add(key)
            mode = (info.external_attr >> 16) & 0xFFFF
            if (
                info.is_dir()
                or stat.S_IFMT(mode) != stat.S_IFREG
                or info.date_time != FIXED_ZIP_TIME
                or info.compress_type != zipfile.ZIP_STORED
                or info.flag_bits & 0x1
                or info.extra
                or info.comment
            ):
                raise VerificationError("PACKAGE_ZIP_MEMBER_METADATA_INVALID")
            if info.file_size < 0 or info.file_size > MAX_PACKAGE_BYTES:
                raise VerificationError("PACKAGE_BOUNDS_EXCEEDED")
            total += info.file_size
            if total > MAX_PACKAGE_BYTES:
                raise VerificationError("PACKAGE_BOUNDS_EXCEEDED")
        if archive.comment or archive.testzip() is not None:
            raise VerificationError("PACKAGE_ZIP_CRC_OR_COMMENT_INVALID")
        for info in infos:
            name = info.filename
            payload = archive.read(info)
            if len(payload) != info.file_size:
                raise VerificationError("PACKAGE_ZIP_MEMBER_SIZE_MISMATCH")
            payloads[name] = payload
    result = _verify_payloads(payloads, source="ZIP", package_location=path)
    result["zip_bytes"] = len(raw)
    result["zip_sha256"] = sha256_bytes(raw)
    return result
