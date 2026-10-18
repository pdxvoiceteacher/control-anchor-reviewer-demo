"""Closed vocabularies and identities for AEP01 transaction evidence."""

from __future__ import annotations

import re
import secrets
import unicodedata
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .canonical import canonical_bytes, sha256_bytes


class ModelError(ValueError):
    """An AEP01 model value failed its closed contract."""


class ControlOutcome(StrEnum):
    """The complete control-result vocabulary; there is no implicit green state."""

    PASS = "PASS"
    FAIL = "FAIL"
    HOLD = "HOLD"
    NOT_EXECUTED = "NOT_EXECUTED"
    ERROR = "ERROR"


CONTROL_OUTCOMES = tuple(item.value for item in ControlOutcome)


class TransactionState(StrEnum):
    CREATED = "CREATED"
    ADMISSION_PENDING = "ADMISSION_PENDING"
    ADMITTED = "ADMITTED"
    REFUSED = "REFUSED"
    INPUTS_BOUND = "INPUTS_BOUND"
    OBSERVED_EVENT_BOUND = "OBSERVED_EVENT_BOUND"
    CANDIDATE_PENDING = "CANDIDATE_PENDING"
    CANDIDATE_CAPTURED = "CANDIDATE_CAPTURED"
    CANDIDATE_FAILED = "CANDIDATE_FAILED"
    CONTROLS_PENDING = "CONTROLS_PENDING"
    CONTROLS_COMPLETE = "CONTROLS_COMPLETE"
    CONTROLS_INCOMPLETE = "CONTROLS_INCOMPLETE"
    SOPHIA_COMPLETE = "SOPHIA_COMPLETE"
    SOPHIA_FAILED = "SOPHIA_FAILED"
    ATLAS_COMPLETE = "ATLAS_COMPLETE"
    ATLAS_FAILED = "ATLAS_FAILED"
    HUMAN_DECISION_PENDING = "HUMAN_DECISION_PENDING"
    APPROVED = "APPROVED"
    HELD = "HELD"
    REJECTED = "REJECTED"
    REPAIR_REQUESTED = "REPAIR_REQUESTED"
    REPAIR_CHILD_CREATED = "REPAIR_CHILD_CREATED"
    FINALIZATION_PENDING = "FINALIZATION_PENDING"
    SEALED = "SEALED"
    FINALIZATION_FAILED = "FINALIZATION_FAILED"


class Plane(StrEnum):
    AI_EXECUTION = "AI_EXECUTION"
    INGRESS_QUARANTINE = "INGRESS_QUARANTINE"
    CONTROL_EVIDENCE = "CONTROL_EVIDENCE"
    AUDIT_ORIENTATION = "AUDIT_ORIENTATION"
    HUMAN_DECISION = "HUMAN_DECISION"
    PRACTITIONER_ACCESS = "PRACTITIONER_ACCESS"


class ActorClass(StrEnum):
    HUMAN_TASK_REQUESTER = "HUMAN_TASK_REQUESTER"
    HUMAN_CONTROL_OWNER = "HUMAN_CONTROL_OWNER"
    HUMAN_REVIEWER = "HUMAN_REVIEWER"
    HUMAN_MANAGEMENT_APPROVER = "HUMAN_MANAGEMENT_APPROVER"
    HUMAN_PRACTITIONER = "HUMAN_PRACTITIONER"
    SERVICE_INGRESS = "SERVICE_INGRESS"
    SERVICE_MODEL_ADAPTER = "SERVICE_MODEL_ADAPTER"
    SERVICE_EVIDENCE_CUSTODIAN = "SERVICE_EVIDENCE_CUSTODIAN"
    SERVICE_CONTROL_EXECUTOR = "SERVICE_CONTROL_EXECUTOR"
    SERVICE_SOPHIA_AUDITOR = "SERVICE_SOPHIA_AUDITOR"
    SERVICE_ATLAS_ORIENTER = "SERVICE_ATLAS_ORIENTER"
    SERVICE_PERIOD_AGGREGATOR = "SERVICE_PERIOD_AGGREGATOR"
    SERVICE_EXPORTER = "SERVICE_EXPORTER"
    SERVICE_EXTERNAL_SIGNER = "SERVICE_EXTERNAL_SIGNER"
    SYSTEM_RECOVERY_ACTOR = "SYSTEM_RECOVERY_ACTOR"


class Decision(StrEnum):
    APPROVE = "APPROVE"
    HOLD = "HOLD"
    REJECT = "REJECT"
    REQUEST_REPAIR = "REQUEST_REPAIR"


_ALLOWED_TRANSITIONS: dict[TransactionState, frozenset[TransactionState]] = {
    TransactionState.CREATED: frozenset({TransactionState.ADMISSION_PENDING}),
    TransactionState.ADMISSION_PENDING: frozenset(
        {TransactionState.ADMITTED, TransactionState.REFUSED}
    ),
    TransactionState.ADMITTED: frozenset({TransactionState.INPUTS_BOUND}),
    TransactionState.REFUSED: frozenset({TransactionState.FINALIZATION_PENDING}),
    TransactionState.INPUTS_BOUND: frozenset({TransactionState.CANDIDATE_PENDING, TransactionState.OBSERVED_EVENT_BOUND}),
    TransactionState.OBSERVED_EVENT_BOUND: frozenset({TransactionState.CONTROLS_PENDING}),
    TransactionState.CANDIDATE_PENDING: frozenset(
        {TransactionState.CANDIDATE_CAPTURED, TransactionState.CANDIDATE_FAILED}
    ),
    TransactionState.CANDIDATE_CAPTURED: frozenset(
        {TransactionState.CONTROLS_PENDING}
    ),
    TransactionState.CANDIDATE_FAILED: frozenset(
        {TransactionState.CONTROLS_PENDING}
    ),
    TransactionState.CONTROLS_PENDING: frozenset(
        {TransactionState.CONTROLS_COMPLETE, TransactionState.CONTROLS_INCOMPLETE}
    ),
    TransactionState.CONTROLS_COMPLETE: frozenset(
        {TransactionState.SOPHIA_COMPLETE, TransactionState.SOPHIA_FAILED}
    ),
    TransactionState.CONTROLS_INCOMPLETE: frozenset(
        {TransactionState.SOPHIA_COMPLETE, TransactionState.SOPHIA_FAILED}
    ),
    TransactionState.SOPHIA_COMPLETE: frozenset(
        {TransactionState.ATLAS_COMPLETE, TransactionState.ATLAS_FAILED}
    ),
    TransactionState.SOPHIA_FAILED: frozenset(
        {TransactionState.ATLAS_COMPLETE, TransactionState.ATLAS_FAILED}
    ),
    TransactionState.ATLAS_COMPLETE: frozenset(
        {TransactionState.HUMAN_DECISION_PENDING}
    ),
    TransactionState.ATLAS_FAILED: frozenset(
        {TransactionState.HUMAN_DECISION_PENDING}
    ),
    TransactionState.HUMAN_DECISION_PENDING: frozenset(
        {
            TransactionState.APPROVED,
            TransactionState.HELD,
            TransactionState.REJECTED,
            TransactionState.REPAIR_REQUESTED,
        }
    ),
    TransactionState.APPROVED: frozenset({TransactionState.FINALIZATION_PENDING}),
    TransactionState.HELD: frozenset({TransactionState.FINALIZATION_PENDING}),
    TransactionState.REJECTED: frozenset({TransactionState.FINALIZATION_PENDING}),
    TransactionState.REPAIR_REQUESTED: frozenset(
        {TransactionState.REPAIR_CHILD_CREATED}
    ),
    TransactionState.REPAIR_CHILD_CREATED: frozenset(
        {TransactionState.FINALIZATION_PENDING}
    ),
    TransactionState.FINALIZATION_PENDING: frozenset(
        {TransactionState.SEALED, TransactionState.FINALIZATION_FAILED}
    ),
    TransactionState.SEALED: frozenset(),
    TransactionState.FINALIZATION_FAILED: frozenset(),
}

if set(_ALLOWED_TRANSITIONS) != set(TransactionState):
    raise RuntimeError("AEP01_TRANSACTION_STATE_TABLE_INCOMPLETE")


def require_control_outcome(value: Any) -> ControlOutcome:
    try:
        return ControlOutcome(value)
    except (TypeError, ValueError) as exc:
        raise ModelError("CONTROL_OUTCOME_INVALID") from exc


def require_state(value: Any) -> TransactionState:
    try:
        return TransactionState(value)
    except (TypeError, ValueError) as exc:
        raise ModelError("TRANSACTION_STATE_INVALID") from exc


def allowed_transitions(value: Any) -> tuple[TransactionState, ...]:
    state = require_state(value)
    return tuple(sorted(_ALLOWED_TRANSITIONS[state], key=lambda item: item.value))


def validate_transition(current: Any, requested: Any) -> TransactionState:
    source = require_state(current)
    target = require_state(requested)
    if target not in _ALLOWED_TRANSITIONS[source]:
        raise ModelError("TRANSACTION_STATE_TRANSITION_PROHIBITED")
    return target


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_KIND = re.compile(r"^[a-z][a-z0-9_]{0,23}$")


def require_identifier(value: Any, label: str = "identifier") -> str:
    if (
        type(value) is not str
        or unicodedata.normalize("NFC", value) != value
        or not _IDENTIFIER.fullmatch(value)
    ):
        raise ModelError(f"IDENTIFIER_INVALID:{label}")
    return value


def make_identifier(kind: str, *seed: Any) -> str:
    """Create a collision-resistant identifier; seeded calls are deterministic."""

    if type(kind) is not str or not _KIND.fullmatch(kind):
        raise ModelError("IDENTIFIER_KIND_INVALID")
    material: list[Any]
    if seed:
        material = list(seed)
    else:
        material = [secrets.token_hex(32)]
    try:
        digest = sha256_bytes(canonical_bytes({"kind": kind, "seed": material}))
    except ValueError as exc:
        raise ModelError("IDENTIFIER_SEED_INVALID") from exc
    return f"{kind}_{digest[:32]}"


@dataclass(frozen=True, slots=True)
class TransactionIdentity:
    transaction_id: str
    parent_transaction_id: str | None = None
    root_transaction_id: str | None = None

    def __post_init__(self) -> None:
        transaction_id = require_identifier(self.transaction_id, "transaction_id")
        parent = self.parent_transaction_id
        root = self.root_transaction_id
        if parent is None:
            if root is None:
                object.__setattr__(self, "root_transaction_id", transaction_id)
            elif require_identifier(root, "root_transaction_id") != transaction_id:
                raise ModelError("ROOT_TRANSACTION_IDENTITY_MISMATCH")
            return
        require_identifier(parent, "parent_transaction_id")
        if parent == transaction_id:
            raise ModelError("TRANSACTION_CANNOT_PARENT_ITSELF")
        if root is None:
            raise ModelError("CHILD_ROOT_TRANSACTION_REQUIRED")
        require_identifier(root, "root_transaction_id")
        if root == transaction_id:
            raise ModelError("CHILD_ROOT_TRANSACTION_INVALID")

    @property
    def is_repair_child(self) -> bool:
        return self.parent_transaction_id is not None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "parent_transaction_id": self.parent_transaction_id,
            "root_transaction_id": self.root_transaction_id,
            "transaction_id": self.transaction_id,
        }


def new_transaction_identity(
    *,
    seed: Any | None = None,
    parent: TransactionIdentity | None = None,
) -> TransactionIdentity:
    material = () if seed is None else (seed,)
    transaction_id = make_identifier("tx", *material)
    if parent is None:
        return TransactionIdentity(transaction_id)
    return TransactionIdentity(
        transaction_id,
        parent_transaction_id=parent.transaction_id,
        root_transaction_id=parent.root_transaction_id,
    )


REPORTABLE_FAILURE_STATES = frozenset(
    {
        TransactionState.REFUSED,
        TransactionState.CANDIDATE_FAILED,
        TransactionState.CONTROLS_INCOMPLETE,
        TransactionState.SOPHIA_FAILED,
        TransactionState.ATLAS_FAILED,
        TransactionState.HELD,
        TransactionState.REJECTED,
        TransactionState.FINALIZATION_FAILED,
    }
)
TERMINAL_TRANSACTION_STATES = frozenset(
    {TransactionState.SEALED, TransactionState.FINALIZATION_FAILED}
)


__all__ = [
    "ActorClass",
    "CONTROL_OUTCOMES",
    "ControlOutcome",
    "Decision",
    "ModelError",
    "Plane",
    "REPORTABLE_FAILURE_STATES",
    "TERMINAL_TRANSACTION_STATES",
    "TransactionIdentity",
    "TransactionState",
    "allowed_transitions",
    "make_identifier",
    "new_transaction_identity",
    "require_control_outcome",
    "require_identifier",
    "require_state",
    "validate_transition",
]
