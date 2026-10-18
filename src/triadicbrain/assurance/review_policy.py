"""Generic, optional review-policy profiles with a built-in Standard profile.

Optional profiles are loaded only when explicitly registered and resolved.  No
specialized review package is imported by the core platform at startup.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import pkgutil
import re
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from . import AUTHORITY_EFFECT
from .models import require_identifier


class ReviewPolicyError(ValueError):
    """A review-policy request failed its bounded generic contract."""


class ApprovalEffect(StrEnum):
    ADVISORY = "ADVISORY"
    BINDING = "BINDING"


class ReviewPolicyEvaluationStatus(StrEnum):
    """Closed outcomes for an optional review-policy execution."""

    INVOKED = "INVOKED"
    NOT_EXECUTED = "NOT_EXECUTED"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class ReviewPolicyEvaluationRequest:
    """Generic captured-output input to a selected review-policy plug-in.

    The request contains only already-captured local evidence.  A plug-in is
    not a model provider and receives no write capability for authoritative
    AEP records.
    """

    profile_id: str
    transaction_id: str
    source_bytes: bytes
    source_media_type: str
    task: str
    model_identity: str
    candidate_bytes: bytes
    logical_time_utc: str
    parent_evaluation: Mapping[str, Any] | None = None
    repair_authorization: Mapping[str, Any] | None = None
    parent_candidate_bytes: bytes | None = None

    def __post_init__(self) -> None:
        try:
            require_identifier(self.profile_id, "review_policy_profile_id")
            require_identifier(self.transaction_id, "transaction_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_ID_INVALID") from exc
        if type(self.source_bytes) is not bytes or type(self.candidate_bytes) is not bytes:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_BYTES_INVALID")
        _required_text(self.source_media_type, "source_media_type", maximum=256)
        _required_text(self.task, "task", maximum=65536)
        _required_text(self.model_identity, "model_identity", maximum=512)
        _required_text(self.logical_time_utc, "logical_time_utc", maximum=64)
        for name, value in (
            ("parent_evaluation", self.parent_evaluation),
            ("repair_authorization", self.repair_authorization),
        ):
            if value is not None and not isinstance(value, Mapping):
                raise ReviewPolicyError(f"REVIEW_POLICY_EVALUATION_MAPPING_INVALID:{name}")
        if self.parent_candidate_bytes is not None and type(self.parent_candidate_bytes) is not bytes:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_PARENT_BYTES_INVALID")


@dataclass(frozen=True, slots=True)
class ReviewPolicyEvaluation:
    """Serializable, non-authoritative result returned by a plug-in."""

    profile_id: str
    transaction_id: str
    status: ReviewPolicyEvaluationStatus
    adapter_id: str
    input_bindings: Mapping[str, Any]
    artifacts: Mapping[str, Any]
    receipts: tuple[Mapping[str, Any], ...]
    findings: tuple[Mapping[str, Any], ...]
    projection: Mapping[str, str]
    parent_binding: Mapping[str, Any] | None = None
    failure: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        try:
            require_identifier(self.profile_id, "review_policy_profile_id")
            require_identifier(self.transaction_id, "transaction_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_ID_INVALID") from exc
        try:
            object.__setattr__(self, "status", ReviewPolicyEvaluationStatus(self.status))
        except (TypeError, ValueError) as exc:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_STATUS_INVALID") from exc
        _required_text(self.adapter_id, "adapter_id", maximum=128)
        for name, value in (
            ("input_bindings", self.input_bindings),
            ("artifacts", self.artifacts),
            ("projection", self.projection),
        ):
            if not isinstance(value, Mapping):
                raise ReviewPolicyError(f"REVIEW_POLICY_EVALUATION_MAPPING_INVALID:{name}")
        if not isinstance(self.receipts, tuple) or any(
            not isinstance(row, Mapping) for row in self.receipts
        ):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_RECEIPTS_INVALID")
        if not isinstance(self.findings, tuple) or any(
            not isinstance(row, Mapping) for row in self.findings
        ):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_FINDINGS_INVALID")
        if self.parent_binding is not None and not isinstance(self.parent_binding, Mapping):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_PARENT_INVALID")
        if self.failure is not None and not isinstance(self.failure, Mapping):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_FAILURE_INVALID")
        if self.status is ReviewPolicyEvaluationStatus.INVOKED and self.failure is not None:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_RESULT_CONTRADICTORY")
        if self.status is not ReviewPolicyEvaluationStatus.INVOKED and self.failure is None:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_FAILURE_REQUIRED")

    def as_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "artifacts": dict(self.artifacts),
            "authority_effect": AUTHORITY_EFFECT,
            "effects": {
                "memory_written": False,
                "network_used": False,
                "provider_invoked": False,
                "publication_performed": False,
            },
            "external_compliance_criteria": False,
            "failure": None if self.failure is None else dict(self.failure),
            "findings": [dict(row) for row in self.findings],
            "input_bindings": dict(self.input_bindings),
            "nonauthority": (
                "Optional review-policy findings are namespaced internal review "
                "signals, not external compliance criteria, an assurance opinion, "
                "or a control-effectiveness conclusion."
            ),
            "parent_binding": (
                None if self.parent_binding is None else dict(self.parent_binding)
            ),
            "profile_id": self.profile_id,
            "projection": dict(self.projection),
            "receipts": [dict(row) for row in self.receipts],
            "schema_id": "uvlm.triadicbrain.aep01.review_policy_evaluation.v1",
            "status": self.status.value,
            "transaction_id": self.transaction_id,
        }


def _required_text(value: Any, field: str, *, maximum: int = 512) -> str:
    if type(value) is not str or not value.strip() or len(value) > maximum:
        raise ReviewPolicyError(f"REVIEW_POLICY_TEXT_INVALID:{field}")
    try:
        # The identifier validator is intentionally not used for display text.
        value.encode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ReviewPolicyError(f"REVIEW_POLICY_TEXT_INVALID:{field}") from exc
    if unicodedata.normalize("NFC", value) != value:
        raise ReviewPolicyError(f"REVIEW_POLICY_TEXT_NOT_NFC:{field}")
    return value


def _text_tuple(value: Any, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ReviewPolicyError(f"REVIEW_POLICY_LIST_INVALID:{field}")
    rows = tuple(_required_text(item, field, maximum=256) for item in value)
    if len(rows) != len(set(rows)):
        raise ReviewPolicyError(f"REVIEW_POLICY_LIST_DUPLICATE:{field}")
    return rows


@dataclass(frozen=True, slots=True)
class ReviewPolicyProfile:
    profile_id: str
    profile_version: str
    display_name: str
    policy_source: str
    finding_rules: tuple[str, ...]
    approval_effect: ApprovalEffect
    repair_selection_supported: bool
    required_evidence: tuple[str, ...]
    authority_effect: str = AUTHORITY_EFFECT

    def __post_init__(self) -> None:
        try:
            require_identifier(self.profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        _required_text(self.profile_version, "profile_version", maximum=64)
        _required_text(self.display_name, "display_name")
        _required_text(self.policy_source, "policy_source")
        object.__setattr__(
            self, "finding_rules", _text_tuple(self.finding_rules, "finding_rules")
        )
        try:
            object.__setattr__(self, "approval_effect", ApprovalEffect(self.approval_effect))
        except (TypeError, ValueError) as exc:
            raise ReviewPolicyError("REVIEW_POLICY_APPROVAL_EFFECT_INVALID") from exc
        if type(self.repair_selection_supported) is not bool:
            raise ReviewPolicyError("REVIEW_POLICY_REPAIR_FLAG_INVALID")
        object.__setattr__(
            self,
            "required_evidence",
            _text_tuple(self.required_evidence, "required_evidence"),
        )
        if self.authority_effect != AUTHORITY_EFFECT:
            raise ReviewPolicyError("REVIEW_POLICY_AUTHORITY_EFFECT_PROHIBITED")

    def as_dict(self) -> dict[str, Any]:
        return {
            "approval_effect": self.approval_effect.value,
            "authority_effect": self.authority_effect,
            "display_name": self.display_name,
            "finding_rules": list(self.finding_rules),
            "policy_source": self.policy_source,
            "profile_id": self.profile_id,
            "profile_version": self.profile_version,
            "repair_selection_supported": self.repair_selection_supported,
            "required_evidence": list(self.required_evidence),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ReviewPolicyProfile":
        required = {
            "approval_effect",
            "authority_effect",
            "display_name",
            "finding_rules",
            "policy_source",
            "profile_id",
            "profile_version",
            "repair_selection_supported",
            "required_evidence",
        }
        if set(value) != required:
            raise ReviewPolicyError("REVIEW_POLICY_FIELDS_INVALID")
        return cls(
            profile_id=value["profile_id"],
            profile_version=value["profile_version"],
            display_name=value["display_name"],
            policy_source=value["policy_source"],
            finding_rules=tuple(value["finding_rules"])
            if isinstance(value["finding_rules"], Sequence)
            and not isinstance(value["finding_rules"], (str, bytes))
            else value["finding_rules"],
            approval_effect=value["approval_effect"],
            repair_selection_supported=value["repair_selection_supported"],
            required_evidence=tuple(value["required_evidence"])
            if isinstance(value["required_evidence"], Sequence)
            and not isinstance(value["required_evidence"], (str, bytes))
            else value["required_evidence"],
            authority_effect=value["authority_effect"],
        )


STANDARD_PROFILE = ReviewPolicyProfile(
    profile_id="STANDARD",
    profile_version="1.0.0",
    display_name="Standard review",
    policy_source="BUILT_IN",
    finding_rules=(),
    approval_effect=ApprovalEffect.ADVISORY,
    repair_selection_supported=True,
    required_evidence=(
        "CONTROL_CHECK_RESULTS",
        "INDEPENDENT_REVIEW_FINDINGS",
    ),
)


_MODULE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]{0,254}$")
_ATTRIBUTE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,127}$")
ProfileFactory = Callable[[], ReviewPolicyProfile | Mapping[str, Any]]
PolicyEvaluator = Callable[[ReviewPolicyEvaluationRequest], ReviewPolicyEvaluation]


@dataclass(frozen=True, slots=True)
class ReviewPolicyRuntime:
    """Opaque lifecycle hooks owned by one optional review-policy plug-in."""

    replay_lifecycle: Callable[..., Any]
    authorize_repair: Callable[..., Mapping[str, Any]]
    verify_package: Callable[..., None]
    verify_live_package: Callable[..., None]

    def __post_init__(self) -> None:
        if not all(
            callable(value)
            for value in (
                self.replay_lifecycle,
                self.authorize_repair,
                self.verify_package,
                self.verify_live_package,
            )
        ):
            raise ReviewPolicyError("REVIEW_POLICY_RUNTIME_INVALID")


class ReviewPolicyRegistry:
    """Profile registry whose optional module loaders remain lazy."""

    def __init__(self) -> None:
        self._profiles: dict[str, ReviewPolicyProfile] = {
            STANDARD_PROFILE.profile_id: STANDARD_PROFILE
        }
        self._loaders: dict[str, tuple[str, str] | ProfileFactory] = {}
        self._evaluators: dict[str, PolicyEvaluator] = {}
        self._runtimes: dict[str, ReviewPolicyRuntime] = {}
        self._disabled: set[str] = set()

    def register_profile(self, profile: ReviewPolicyProfile) -> None:
        if not isinstance(profile, ReviewPolicyProfile):
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_INVALID")
        if profile.profile_id == STANDARD_PROFILE.profile_id:
            raise ReviewPolicyError("STANDARD_PROFILE_REPLACEMENT_PROHIBITED")
        if profile.profile_id in self._profiles or profile.profile_id in self._loaders:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_DUPLICATE")
        self._profiles[profile.profile_id] = profile

    def register_optional(
        self,
        profile_id: str,
        module_name: str,
        *,
        attribute: str = "review_policy_profile",
    ) -> None:
        try:
            require_identifier(profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        if (
            type(module_name) is not str
            or not _MODULE_NAME.fullmatch(module_name)
            or type(attribute) is not str
            or not _ATTRIBUTE_NAME.fullmatch(attribute)
        ):
            raise ReviewPolicyError("REVIEW_POLICY_LOADER_INVALID")
        if profile_id in self._profiles or profile_id in self._loaders:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_DUPLICATE")
        self._loaders[profile_id] = (module_name, attribute)

    def register_factory(self, profile_id: str, factory: ProfileFactory) -> None:
        try:
            require_identifier(profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        if not callable(factory):
            raise ReviewPolicyError("REVIEW_POLICY_FACTORY_INVALID")
        if profile_id in self._profiles or profile_id in self._loaders:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_DUPLICATE")
        self._loaders[profile_id] = factory

    def register_evaluator(
        self, profile_id: str, evaluator: PolicyEvaluator
    ) -> None:
        """Bind an evaluator without executing or importing its dependencies."""

        try:
            requested = require_identifier(profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        if requested not in self._profiles and requested not in self._loaders:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATOR_PROFILE_UNKNOWN")
        if requested in self._evaluators:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATOR_DUPLICATE")
        if not callable(evaluator):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATOR_INVALID")
        self._evaluators[requested] = evaluator

    def register_runtime(
        self, profile_id: str, runtime: ReviewPolicyRuntime
    ) -> None:
        """Bind optional lifecycle behavior without granting core authority."""

        try:
            requested = require_identifier(profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        if requested not in self._profiles and requested not in self._loaders:
            raise ReviewPolicyError("REVIEW_POLICY_RUNTIME_PROFILE_UNKNOWN")
        if requested in self._runtimes:
            raise ReviewPolicyError("REVIEW_POLICY_RUNTIME_DUPLICATE")
        if not isinstance(runtime, ReviewPolicyRuntime):
            raise ReviewPolicyError("REVIEW_POLICY_RUNTIME_INVALID")
        self._runtimes[requested] = runtime

    def disable(self, profile_id: str) -> None:
        if profile_id == STANDARD_PROFILE.profile_id:
            raise ReviewPolicyError("STANDARD_PROFILE_DISABLE_PROHIBITED")
        self._disabled.add(profile_id)

    def enable(self, profile_id: str) -> None:
        self._disabled.discard(profile_id)

    def resolve(self, profile_id: str = STANDARD_PROFILE.profile_id) -> ReviewPolicyProfile:
        try:
            requested = require_identifier(profile_id, "review_policy_profile_id")
        except ValueError as exc:
            raise ReviewPolicyError("REVIEW_POLICY_PROFILE_ID_INVALID") from exc
        if requested in self._disabled:
            raise ReviewPolicyError("REVIEW_POLICY_DISABLED")
        known = self._profiles.get(requested)
        if known is not None:
            return known
        loader = self._loaders.get(requested)
        if loader is None:
            raise ReviewPolicyError("REVIEW_POLICY_UNAVAILABLE")
        try:
            if isinstance(loader, tuple):
                module_name, attribute = loader
                candidate = getattr(importlib.import_module(module_name), attribute)
                produced = candidate() if callable(candidate) else candidate
            else:
                produced = loader()
        except ReviewPolicyError:
            raise
        except Exception as exc:
            raise ReviewPolicyError("REVIEW_POLICY_LOAD_FAILED") from exc
        if isinstance(produced, ReviewPolicyProfile):
            profile = produced
        elif isinstance(produced, Mapping):
            profile = ReviewPolicyProfile.from_mapping(produced)
        else:
            raise ReviewPolicyError("REVIEW_POLICY_FACTORY_RESULT_INVALID")
        if profile.profile_id != requested:
            raise ReviewPolicyError("REVIEW_POLICY_FACTORY_ID_MISMATCH")
        self._profiles[requested] = profile
        return profile

    def available_profile_ids(self) -> tuple[str, ...]:
        return tuple(sorted((set(self._profiles) | set(self._loaders)) - self._disabled))

    def has_evaluator(self, profile_id: str) -> bool:
        return profile_id not in self._disabled and profile_id in self._evaluators

    def runtime(self, profile_id: str) -> ReviewPolicyRuntime:
        profile = self.resolve(profile_id)
        runtime = self._runtimes.get(profile.profile_id)
        if runtime is None or profile.profile_id in self._disabled:
            raise ReviewPolicyError("REVIEW_POLICY_RUNTIME_UNAVAILABLE")
        return runtime

    def evaluate(
        self,
        profile_id: str,
        request: ReviewPolicyEvaluationRequest,
    ) -> ReviewPolicyEvaluation:
        profile = self.resolve(profile_id)
        if request.profile_id != profile.profile_id:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_PROFILE_MISMATCH")
        evaluator = self._evaluators.get(profile.profile_id)
        if evaluator is None:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATOR_UNAVAILABLE")
        try:
            result = evaluator(request)
        except ReviewPolicyError:
            raise
        except Exception as exc:
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_FAILED") from exc
        if not isinstance(result, ReviewPolicyEvaluation):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATOR_RESULT_INVALID")
        if (
            result.profile_id != profile.profile_id
            or result.transaction_id != request.transaction_id
        ):
            raise ReviewPolicyError("REVIEW_POLICY_EVALUATION_RESULT_MISMATCH")
        return result


_PLUGIN_ENTRY_POINT_GROUP = "control_anchor.review_policy_plugins"
_PLUGIN_NAMESPACE = f"{__package__}.optional_profiles"


def discover_review_policy_registry(profile_id: str) -> ReviewPolicyRegistry:
    """Discover a plug-in only after a nonstandard profile is selected.

    Installed distributions use entry points.  The namespace scan keeps local
    source-tree compatibility tests possible without making any plug-in a core
    import.  An unavailable selected profile remains an explicit error.
    """

    requested = require_identifier(profile_id, "review_policy_profile_id")
    registry = ReviewPolicyRegistry()
    if requested == STANDARD_PROFILE.profile_id:
        return registry

    try:
        entry_points = importlib.metadata.entry_points()
        selected = (
            entry_points.select(group=_PLUGIN_ENTRY_POINT_GROUP)
            if hasattr(entry_points, "select")
            else entry_points.get(_PLUGIN_ENTRY_POINT_GROUP, ())
        )
    except Exception as exc:
        raise ReviewPolicyError("REVIEW_POLICY_DISCOVERY_FAILED") from exc
    for entry_point in sorted(selected, key=lambda item: (item.name, item.value)):
        try:
            registrar = entry_point.load()
            if not callable(registrar):
                raise TypeError("registrar is not callable")
            registrar(registry)
        except ReviewPolicyError:
            raise
        except Exception as exc:
            raise ReviewPolicyError("REVIEW_POLICY_DISCOVERY_FAILED") from exc
        if requested in registry.available_profile_ids():
            return registry

    try:
        namespace = importlib.import_module(_PLUGIN_NAMESPACE)
    except ModuleNotFoundError:
        return registry
    paths = getattr(namespace, "__path__", None)
    if paths is None:
        raise ReviewPolicyError("REVIEW_POLICY_DISCOVERY_FAILED")
    for discovered in sorted(
        pkgutil.iter_modules(paths, namespace.__name__ + "."),
        key=lambda item: item.name,
    ):
        try:
            module = importlib.import_module(discovered.name)
            registrar = getattr(module, "register_review_policy_plugin")
            if not callable(registrar):
                raise TypeError("registrar is not callable")
            registrar(registry)
        except ReviewPolicyError:
            raise
        except Exception as exc:
            raise ReviewPolicyError("REVIEW_POLICY_DISCOVERY_FAILED") from exc
        if requested in registry.available_profile_ids():
            return registry
    return registry


def load_review_policy(
    profile_id: str = STANDARD_PROFILE.profile_id,
    *,
    enabled: bool = True,
    registry: ReviewPolicyRegistry | None = None,
) -> ReviewPolicyProfile:
    """Resolve a profile, falling back to Standard only when plugins are disabled."""

    if type(enabled) is not bool:
        raise ReviewPolicyError("REVIEW_POLICY_ENABLED_FLAG_INVALID")
    selected = registry if registry is not None else ReviewPolicyRegistry()
    if not enabled:
        return selected.resolve(STANDARD_PROFILE.profile_id)
    return selected.resolve(profile_id)


__all__ = [
    "ApprovalEffect",
    "ReviewPolicyError",
    "ReviewPolicyEvaluation",
    "ReviewPolicyEvaluationRequest",
    "ReviewPolicyEvaluationStatus",
    "ReviewPolicyProfile",
    "ReviewPolicyRegistry",
    "ReviewPolicyRuntime",
    "STANDARD_PROFILE",
    "discover_review_policy_registry",
    "load_review_policy",
]
