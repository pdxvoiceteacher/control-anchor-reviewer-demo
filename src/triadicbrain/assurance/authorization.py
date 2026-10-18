"""Deny-by-default authorization for the six AEP01 planes."""

from __future__ import annotations

from enum import StrEnum
from types import MappingProxyType
from typing import Any

from . import AUTHORITY_EFFECT
from .models import ActorClass, Plane


class AuthorizationError(PermissionError):
    """A privileged platform action was denied by the closed role policy."""


class Action(StrEnum):
    READ_APPROVED_INPUT = "READ_APPROVED_INPUT"
    REGISTER_TRANSACTION = "REGISTER_TRANSACTION"
    ADMIT_OR_REFUSE = "ADMIT_OR_REFUSE"
    WRITE_RAW_CANDIDATE = "WRITE_RAW_CANDIDATE"
    WRITE_CONTROL_RESULT = "WRITE_CONTROL_RESULT"
    APPEND_CUSTODY_EVENT = "APPEND_CUSTODY_EVENT"
    WRITE_SOPHIA_FINDING = "WRITE_SOPHIA_FINDING"
    WRITE_ATLAS_POSTURE = "WRITE_ATLAS_POSTURE"
    SUBMIT_HUMAN_DECISION = "SUBMIT_HUMAN_DECISION"
    APPEND_PRACTITIONER_ANNOTATION = "APPEND_PRACTITIONER_ANNOTATION"
    SEAL_TRANSACTION_PACKAGE = "SEAL_TRANSACTION_PACKAGE"
    AGGREGATE_PERIOD = "AGGREGATE_PERIOD"
    EXPORT_EVIDENCE = "EXPORT_EVIDENCE"
    APPLY_EXTERNAL_SIGNATURE = "APPLY_EXTERNAL_SIGNATURE"
    RECOVER_INTERRUPTED_TRANSITION = "RECOVER_INTERRUPTED_TRANSITION"
    MUTATE_FINALIZED_EVIDENCE = "MUTATE_FINALIZED_EVIDENCE"
    GENERATE_ASSURANCE_OPINION = "GENERATE_ASSURANCE_OPINION"


_ROLE_PLANE: dict[ActorClass, Plane] = {
    ActorClass.HUMAN_TASK_REQUESTER: Plane.INGRESS_QUARANTINE,
    ActorClass.HUMAN_CONTROL_OWNER: Plane.CONTROL_EVIDENCE,
    ActorClass.HUMAN_REVIEWER: Plane.HUMAN_DECISION,
    ActorClass.HUMAN_MANAGEMENT_APPROVER: Plane.HUMAN_DECISION,
    ActorClass.HUMAN_PRACTITIONER: Plane.PRACTITIONER_ACCESS,
    ActorClass.SERVICE_INGRESS: Plane.INGRESS_QUARANTINE,
    ActorClass.SERVICE_MODEL_ADAPTER: Plane.AI_EXECUTION,
    ActorClass.SERVICE_EVIDENCE_CUSTODIAN: Plane.CONTROL_EVIDENCE,
    ActorClass.SERVICE_CONTROL_EXECUTOR: Plane.CONTROL_EVIDENCE,
    ActorClass.SERVICE_SOPHIA_AUDITOR: Plane.AUDIT_ORIENTATION,
    ActorClass.SERVICE_ATLAS_ORIENTER: Plane.AUDIT_ORIENTATION,
    ActorClass.SERVICE_PERIOD_AGGREGATOR: Plane.CONTROL_EVIDENCE,
    ActorClass.SERVICE_EXPORTER: Plane.CONTROL_EVIDENCE,
    ActorClass.SERVICE_EXTERNAL_SIGNER: Plane.CONTROL_EVIDENCE,
    ActorClass.SYSTEM_RECOVERY_ACTOR: Plane.CONTROL_EVIDENCE,
}


_READERS = frozenset(ActorClass)
_ALLOWED: dict[ActorClass, frozenset[Action]] = {
    role: frozenset({Action.READ_APPROVED_INPUT}) for role in _READERS
}
_ALLOWED.update(
    {
        ActorClass.HUMAN_TASK_REQUESTER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.REGISTER_TRANSACTION}
        ),
        ActorClass.HUMAN_CONTROL_OWNER: frozenset({Action.READ_APPROVED_INPUT}),
        ActorClass.HUMAN_REVIEWER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.SUBMIT_HUMAN_DECISION}
        ),
        ActorClass.HUMAN_MANAGEMENT_APPROVER: frozenset(
            {Action.READ_APPROVED_INPUT}
        ),
        ActorClass.HUMAN_PRACTITIONER: frozenset(
            {
                Action.READ_APPROVED_INPUT,
                Action.APPEND_PRACTITIONER_ANNOTATION,
            }
        ),
        ActorClass.SERVICE_INGRESS: frozenset(
            {
                Action.READ_APPROVED_INPUT,
                Action.REGISTER_TRANSACTION,
                Action.ADMIT_OR_REFUSE,
                Action.WRITE_RAW_CANDIDATE,
            }
        ),
        ActorClass.SERVICE_MODEL_ADAPTER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.WRITE_RAW_CANDIDATE}
        ),
        ActorClass.SERVICE_EVIDENCE_CUSTODIAN: frozenset(
            {
                Action.READ_APPROVED_INPUT,
                Action.APPEND_CUSTODY_EVENT,
                Action.SEAL_TRANSACTION_PACKAGE,
            }
        ),
        ActorClass.SERVICE_CONTROL_EXECUTOR: frozenset(
            {Action.READ_APPROVED_INPUT, Action.WRITE_CONTROL_RESULT}
        ),
        ActorClass.SERVICE_SOPHIA_AUDITOR: frozenset(
            {Action.READ_APPROVED_INPUT, Action.WRITE_SOPHIA_FINDING}
        ),
        ActorClass.SERVICE_ATLAS_ORIENTER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.WRITE_ATLAS_POSTURE}
        ),
        ActorClass.SERVICE_PERIOD_AGGREGATOR: frozenset(
            {Action.READ_APPROVED_INPUT, Action.AGGREGATE_PERIOD}
        ),
        ActorClass.SERVICE_EXPORTER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.EXPORT_EVIDENCE}
        ),
        ActorClass.SERVICE_EXTERNAL_SIGNER: frozenset(
            {Action.READ_APPROVED_INPUT, Action.APPLY_EXTERNAL_SIGNATURE}
        ),
        ActorClass.SYSTEM_RECOVERY_ACTOR: frozenset(
            {
                Action.READ_APPROVED_INPUT,
                Action.RECOVER_INTERRUPTED_TRANSITION,
            }
        ),
    }
)

if set(_ROLE_PLANE) != set(ActorClass) or set(_ALLOWED) != set(ActorClass):
    raise RuntimeError("AEP01_AUTHORIZATION_TABLE_INCOMPLETE")
if any(
    forbidden in actions
    for actions in _ALLOWED.values()
    for forbidden in (
        Action.MUTATE_FINALIZED_EVIDENCE,
        Action.GENERATE_ASSURANCE_OPINION,
    )
):
    raise RuntimeError("AEP01_PROHIBITED_ACTION_GRANTED")


ROLE_PLANES = MappingProxyType(dict(_ROLE_PLANE))
PERMISSIONS = MappingProxyType(dict(_ALLOWED))


def _actor(value: Any) -> ActorClass | None:
    try:
        return ActorClass(value)
    except (TypeError, ValueError):
        return None


def _action(value: Any) -> Action | None:
    try:
        return Action(value)
    except (TypeError, ValueError):
        return None


def plane_for_actor(actor_class: Any) -> Plane:
    actor = _actor(actor_class)
    if actor is None:
        raise AuthorizationError("AUTHORIZATION_ACTOR_UNKNOWN")
    return _ROLE_PLANE[actor]


def authorize(
    actor_class: Any,
    action: Any,
    *,
    target_plane: Any | None = None,
) -> dict[str, Any]:
    """Return a nonauthoritative allow/deny decision without throwing on unknowns."""

    actor = _actor(actor_class)
    requested = _action(action)
    plane: Plane | None = None
    if target_plane is not None:
        try:
            plane = Plane(target_plane)
        except (TypeError, ValueError):
            plane = None

    allowed = actor is not None and requested is not None
    reason = "AUTHORIZED_BY_EXACT_ROLE_ACTION"
    if actor is None:
        allowed = False
        reason = "AUTHORIZATION_ACTOR_UNKNOWN"
    elif requested is None:
        allowed = False
        reason = "AUTHORIZATION_ACTION_UNKNOWN"
    elif target_plane is not None and plane is None:
        allowed = False
        reason = "AUTHORIZATION_TARGET_PLANE_UNKNOWN"
    elif requested not in _ALLOWED[actor]:
        allowed = False
        reason = "AUTHORIZATION_DENY_BY_DEFAULT"
    elif plane is not None and _ROLE_PLANE[actor] != plane:
        # Approved reads may cross planes.  The model adapter's sole write is
        # delivery of exact raw bytes to the ingress quarantine endpoint.
        model_to_quarantine = (
            actor == ActorClass.SERVICE_MODEL_ADAPTER
            and requested == Action.WRITE_RAW_CANDIDATE
            and plane == Plane.INGRESS_QUARANTINE
        )
        if requested != Action.READ_APPROVED_INPUT and not model_to_quarantine:
            allowed = False
            reason = "AUTHORIZATION_CROSS_PLANE_WRITE_DENIED"

    return {
        "action": requested.value if requested is not None else "UNKNOWN",
        "actor_class": actor.value if actor is not None else "UNKNOWN",
        "allowed": allowed,
        "authority_effect": AUTHORITY_EFFECT,
        "reason_code": reason,
        "target_plane": plane.value if plane is not None else None,
    }


def require_authorized(
    actor_class: Any,
    action: Any,
    *,
    target_plane: Any | None = None,
) -> dict[str, Any]:
    decision = authorize(actor_class, action, target_plane=target_plane)
    if decision["allowed"] is not True:
        raise AuthorizationError(str(decision["reason_code"]))
    return decision


def permission_matrix() -> dict[str, dict[str, Any]]:
    """Return the complete role posture, including every explicit denial."""

    all_actions = set(Action)
    return {
        role.value: {
            "allowed_actions": sorted(action.value for action in _ALLOWED[role]),
            "denied_actions": sorted(
                action.value for action in all_actions - _ALLOWED[role]
            ),
            "plane": _ROLE_PLANE[role].value,
        }
        for role in sorted(ActorClass, key=lambda item: item.value)
    }


__all__ = [
    "Action",
    "AuthorizationError",
    "PERMISSIONS",
    "ROLE_PLANES",
    "authorize",
    "permission_matrix",
    "plane_for_actor",
    "require_authorized",
]
