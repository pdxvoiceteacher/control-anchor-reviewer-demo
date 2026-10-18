"""Exact actor, plane, and reason policy for AEP01 custody transitions."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from . import AUTHORITY_EFFECT
from .custody import ZERO_SIDE_EFFECTS
from .models import ActorClass, Plane, TransactionState


class TransitionPolicyError(ValueError):
    """A custody event did not match the only actor allowed for its transition."""


_SERVICE_RULES: dict[
    tuple[TransactionState, TransactionState],
    tuple[ActorClass, Plane, str, str],
] = {
    (TransactionState.CREATED, TransactionState.ADMISSION_PENDING): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "ADMISSION_EVALUATION_STARTED",
    ),
    (TransactionState.ADMISSION_PENDING, TransactionState.ADMITTED): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "TASK_ADMITTED",
    ),
    (TransactionState.ADMISSION_PENDING, TransactionState.REFUSED): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "TASK_REFUSED_AND_RETAINED_IN_POPULATION",
    ),
    (TransactionState.ADMITTED, TransactionState.INPUTS_BOUND): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "SOURCE_PROMPT_MODEL_SETTINGS_BOUND",
    ),
    (TransactionState.INPUTS_BOUND, TransactionState.CANDIDATE_PENDING): (
        ActorClass.SERVICE_MODEL_ADAPTER,
        Plane.AI_EXECUTION,
        "SERVICE-MODEL-ADAPTER",
        "CAPTURED_CANDIDATE_IMPORT_PENDING",
    ),
    (TransactionState.INPUTS_BOUND, TransactionState.OBSERVED_EVENT_BOUND): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "NON_MODEL_EVENT_BOUND_NO_PROVIDER",
    ),
    (TransactionState.OBSERVED_EVENT_BOUND, TransactionState.CONTROLS_PENDING): (
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-CONTROL-EXECUTOR",
        "VERSIONED_CONTROL_EXECUTION_STARTED",
    ),
    (TransactionState.CANDIDATE_PENDING, TransactionState.CANDIDATE_CAPTURED): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "RAW_CANDIDATE_CAPTURED",
    ),
    (TransactionState.CANDIDATE_PENDING, TransactionState.CANDIDATE_FAILED): (
        ActorClass.SERVICE_INGRESS,
        Plane.INGRESS_QUARANTINE,
        "SERVICE-INGRESS",
        "RAW_CANDIDATE_FAILURE_RETAINED",
    ),
    (TransactionState.CANDIDATE_CAPTURED, TransactionState.CONTROLS_PENDING): (
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-CONTROL-EXECUTOR",
        "VERSIONED_CONTROL_EXECUTION_STARTED",
    ),
    (TransactionState.CANDIDATE_FAILED, TransactionState.CONTROLS_PENDING): (
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-CONTROL-EXECUTOR",
        "VERSIONED_CONTROL_EXECUTION_STARTED",
    ),
    (TransactionState.CONTROLS_PENDING, TransactionState.CONTROLS_COMPLETE): (
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-CONTROL-EXECUTOR",
        "ALL_42_CONTROL_RESULTS_RECORDED",
    ),
    (TransactionState.CONTROLS_PENDING, TransactionState.CONTROLS_INCOMPLETE): (
        ActorClass.SERVICE_CONTROL_EXECUTOR,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-CONTROL-EXECUTOR",
        "CONTROL_EXECUTION_INCOMPLETE_RETAINED",
    ),
    (TransactionState.CONTROLS_COMPLETE, TransactionState.SOPHIA_COMPLETE): (
        ActorClass.SERVICE_SOPHIA_AUDITOR,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-SOPHIA-AUDITOR",
        "INDEPENDENT_REVIEW_FINDINGS_RECORDED",
    ),
    (TransactionState.CONTROLS_INCOMPLETE, TransactionState.SOPHIA_COMPLETE): (
        ActorClass.SERVICE_SOPHIA_AUDITOR,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-SOPHIA-AUDITOR",
        "INDEPENDENT_REVIEW_FINDINGS_RECORDED",
    ),
    (TransactionState.CONTROLS_COMPLETE, TransactionState.SOPHIA_FAILED): (
        ActorClass.SERVICE_SOPHIA_AUDITOR,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-SOPHIA-AUDITOR",
        "INDEPENDENT_REVIEW_FAILURE_RETAINED",
    ),
    (TransactionState.CONTROLS_INCOMPLETE, TransactionState.SOPHIA_FAILED): (
        ActorClass.SERVICE_SOPHIA_AUDITOR,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-SOPHIA-AUDITOR",
        "INDEPENDENT_REVIEW_FAILURE_RETAINED",
    ),
    (TransactionState.SOPHIA_COMPLETE, TransactionState.ATLAS_COMPLETE): (
        ActorClass.SERVICE_ATLAS_ORIENTER,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-ATLAS-ORIENTER",
        "MANAGEMENT_ORIENTATION_RECORDED_WITH_NO_AUTHORITY",
    ),
    (TransactionState.SOPHIA_FAILED, TransactionState.ATLAS_COMPLETE): (
        ActorClass.SERVICE_ATLAS_ORIENTER,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-ATLAS-ORIENTER",
        "MANAGEMENT_ORIENTATION_RECORDED_WITH_NO_AUTHORITY",
    ),
    (TransactionState.SOPHIA_COMPLETE, TransactionState.ATLAS_FAILED): (
        ActorClass.SERVICE_ATLAS_ORIENTER,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-ATLAS-ORIENTER",
        "MANAGEMENT_ORIENTATION_FAILURE_RETAINED",
    ),
    (TransactionState.SOPHIA_FAILED, TransactionState.ATLAS_FAILED): (
        ActorClass.SERVICE_ATLAS_ORIENTER,
        Plane.AUDIT_ORIENTATION,
        "SERVICE-ATLAS-ORIENTER",
        "MANAGEMENT_ORIENTATION_FAILURE_RETAINED",
    ),
    (TransactionState.ATLAS_COMPLETE, TransactionState.HUMAN_DECISION_PENDING): (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "HUMAN_DECISION_REQUIRED",
    ),
    (TransactionState.ATLAS_FAILED, TransactionState.HUMAN_DECISION_PENDING): (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "HUMAN_DECISION_REQUIRED",
    ),
    (TransactionState.REPAIR_REQUESTED, TransactionState.REPAIR_CHILD_CREATED): (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "IMMUTABLE_REPAIR_CHILD_CREATED",
    ),
    (TransactionState.FINALIZATION_PENDING, TransactionState.SEALED): (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "PACKAGE_SEALED_HASH_CHAIN_ONLY",
    ),
    (TransactionState.FINALIZATION_PENDING, TransactionState.FINALIZATION_FAILED): (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "FINALIZATION_FAILURE_RETAINED",
    ),
}

for _state in (
    TransactionState.APPROVED,
    TransactionState.HELD,
    TransactionState.REJECTED,
    TransactionState.REPAIR_CHILD_CREATED,
    TransactionState.REFUSED,
):
    _SERVICE_RULES[(_state, TransactionState.FINALIZATION_PENDING)] = (
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN,
        Plane.CONTROL_EVIDENCE,
        "SERVICE-EVIDENCE-CUSTODIAN",
        "FINALIZATION_STARTED",
    )

_HUMAN_TARGET_REASONS = {
    TransactionState.APPROVED: "HUMAN_DECISION_APPROVE",
    TransactionState.HELD: "HUMAN_DECISION_HOLD",
    TransactionState.REJECTED: "HUMAN_DECISION_REJECT",
    TransactionState.REPAIR_REQUESTED: "HUMAN_DECISION_REQUEST_REPAIR",
}


def validate_transition_event_semantics(
    event: Mapping[str, Any],
    source: TransactionState,
    target: TransactionState,
    *,
    decision_actor_id: str | None = None,
) -> None:
    """Require exact write authority for one state-transition custody event."""

    if source is TransactionState.HUMAN_DECISION_PENDING:
        expected = (
            ActorClass.HUMAN_REVIEWER,
            Plane.HUMAN_DECISION,
            decision_actor_id,
            _HUMAN_TARGET_REASONS.get(target),
        )
        if expected[2] is None or expected[3] is None:
            raise TransitionPolicyError("TRANSITION_HUMAN_DECISION_BINDING_INVALID")
    else:
        expected = _SERVICE_RULES.get((source, target))
        if expected is None:
            raise TransitionPolicyError("TRANSITION_SEMANTIC_RULE_UNAVAILABLE")
    actor_class, plane, actor_id, reason = expected
    if (
        event.get("actor_class") != actor_class.value
        or event.get("plane") != plane.value
        or event.get("actor_id") != actor_id
        or event.get("reason_codes") != [reason]
        or event.get("result") != "PASS"
        or event.get("authority_effect") != AUTHORITY_EFFECT
        or event.get("side_effects") != ZERO_SIDE_EFFECTS
    ):
        raise TransitionPolicyError("TRANSITION_ACTOR_PLANE_OR_REASON_INVALID")


def validate_recovery_event_semantics(event: Mapping[str, Any]) -> None:
    """Require the sole bounded identity for a recovery observation event."""

    if (
        event.get("actor_class") != ActorClass.SYSTEM_RECOVERY_ACTOR.value
        or event.get("plane") != Plane.CONTROL_EVIDENCE.value
        or event.get("actor_id") != "SYSTEM-RECOVERY"
        or event.get("reason_codes") != ["DETERMINISTIC_PENDING_TRANSITION_REENTRY"]
        or event.get("result") != "PASS"
        or event.get("authority_effect") != AUTHORITY_EFFECT
        or event.get("side_effects") != ZERO_SIDE_EFFECTS
    ):
        raise TransitionPolicyError("RECOVERY_ACTOR_PLANE_OR_REASON_INVALID")


__all__ = [
    "TransitionPolicyError",
    "validate_recovery_event_semantics",
    "validate_transition_event_semantics",
]
