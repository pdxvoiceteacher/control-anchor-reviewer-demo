"""Closed, local validation for the commission-supplied AEP01 schemas.

The original eight documents are exact byte copies from the authenticated
v1.0.0 predecessor embedded in the controlling v1.1.0 commission.  Four more
are exact copies from the authenticated real-world operability supplement.  The
default validator is a small standard-library implementation of every assertion
keyword used by those documents.  It neither resolves remote references nor
imports an optional validator.  Callers must explicitly select
``engine="jsonschema"`` to use the locally installed :mod:`jsonschema` engine.

Validation establishes conformance to the bounded schema only.  It is not an
assurance conclusion, a compliance determination, or evidence of truth or
control effectiveness.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import stat
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from .canonical import CanonicalError, canonical_bytes


CONTROLLING_COMMISSION_SHA256 = (
    "9dcbc797387da7e987adac7057202146f4bb4d0c4a47a903eda62534dfcff18b"
)
EMBEDDED_PREDECESSOR_COMMISSION_SHA256 = (
    "6219b4d1052d146b6d4aa8e45dafeb7631b5f5c5e366181e4be31a030d1eaf1d"
)
SCHEMA_DIALECT = "https://json-schema.org/draft/2020-12/schema"
VALIDATION_NOTICE = "SYSTEM-GENERATED CONTROL EVIDENCE — NO ASSURANCE PROVIDED."

SCHEMA_SHA256: dict[str, str] = {
    "control_execution_result.v1.schema.json": (
        "5ca1bc104cc78c34d3e75c71c14685ab5beb6c31161ce32141c1a4acc7cff96a"
    ),
    "custody_event.v1.schema.json": (
        "d28d406fbf9856eb702eb2e397a1c2ccf96db997012e853cd9f4b84fe232c1a1"
    ),
    "evidence_package_manifest.v1.schema.json": (
        "14cd6f1c57a038f8b7eda6a45beab474b52a4cd1f22712eda089ee74c1ec7438"
    ),
    "management_representation.v1.schema.json": (
        "e406d764c0c40f60ddd9140d7a7896c902425af450c6075ee476b5b0ce981247"
    ),
    "period_control_summary.v1.schema.json": (
        "c474eb2f25a178725b70becfe84206a9507620627e50792a2976d253ab63f0fe"
    ),
    "poc01_final_base_receipt.v1.schema.json": (
        "ce9bd6f9ccd4044ea3c1540c1a95c22da5339a88c69b620c272b7c3635728f32"
    ),
    "practitioner_annotation.v1.schema.json": (
        "bfea54065bbf0ca4d49fa1be1b7849a9d0c5abdeb33ac5c607305b375ea5eb6b"
    ),
    "segregation_posture.v1.schema.json": (
        "cddd13b6ee2a928231963f058553ceb48d4dd35c97387c44e360540487e9cdc5"
    ),
    "open_world_proof_receipt.v1.schema.json": (
        "4df3283fa8b370fa77a0472d41fbea5244631f272916078bf0fe5450d0889d36"
    ),
    "provider_adapter_manifest.v1.schema.json": (
        "b1d28d4f994700879c9abea27b75e8a8f0a81d71ce17af67a2a2dc58170ecf33"
    ),
    "retention_record.v1.schema.json": (
        "707b622c9242b35a7e5f989c2b8c3694bf12aec8342f63e39824607fff65f196"
    ),
    "transaction_registry_row.v1.schema.json": (
        "f06c1b9683b8d373ff9f3e9f11d9de5091afbba8a700db83b9e7eb9dc61ba9cb"
    ),
}

SCHEMA_ID_TO_FILENAME: dict[str, str] = {
    "uvlm.triadicbrain.aep01.control_execution_result.v1": (
        "control_execution_result.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.custody_event.v1": "custody_event.v1.schema.json",
    "uvlm.triadicbrain.aep01.evidence_package_manifest.v1": (
        "evidence_package_manifest.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.management_representation.v1": (
        "management_representation.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.period_control_summary.v1": (
        "period_control_summary.v1.schema.json"
    ),
    "uvlm.triadicbrain.poc01.final_base_receipt.v1": (
        "poc01_final_base_receipt.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.practitioner_annotation.v1": (
        "practitioner_annotation.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.segregation_posture.v1": (
        "segregation_posture.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.open_world_proof_receipt.v1": (
        "open_world_proof_receipt.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.provider_adapter_manifest.v1": (
        "provider_adapter_manifest.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.retention_record.v1": (
        "retention_record.v1.schema.json"
    ),
    "uvlm.triadicbrain.aep01.transaction_registry_row.v1": (
        "transaction_registry_row.v1.schema.json"
    ),
}

_SCHEMA_DIRECTORY = Path(__file__).with_name("schemas")
_MAX_LOCAL_JSON_BYTES = 16 * 1024 * 1024
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_RFC3339_DATE_TIME = re.compile(
    r"^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})T"
    r"(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?)"
    r"(?P<zone>Z|[+-][0-9]{2}:[0-9]{2})$"
)
_ANNOTATION_KEYWORDS = {"$id", "$schema", "title"}
_ASSERTION_KEYWORDS = {
    "$defs",
    "$ref",
    "additionalProperties",
    "anyOf",
    "const",
    "enum",
    "format",
    "items",
    "maxLength",
    "minItems",
    "minLength",
    "minimum",
    "oneOf",
    "pattern",
    "properties",
    "required",
    "type",
    "uniqueItems",
}
_SUPPORTED_KEYWORDS = _ANNOTATION_KEYWORDS | _ASSERTION_KEYWORDS


class SchemaValidationError(ValueError):
    """A schema source or instance failed closed validation."""

    def __init__(
        self,
        code: str,
        *,
        instance_path: str = "$",
        schema_path: str = "$",
        detail: str | None = None,
    ) -> None:
        self.code = code
        self.instance_path = instance_path
        self.schema_path = schema_path
        self.detail = detail
        suffix = f":{detail}" if detail else ""
        super().__init__(f"{code}@{instance_path}<{schema_path}>{suffix}")


def _reject_constant(value: str) -> None:
    raise SchemaValidationError("NONFINITE_JSON_NUMBER", detail=value)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SchemaValidationError("DUPLICATE_JSON_MEMBER", detail=key)
        result[key] = value
    return result


def _parse_json_bytes(payload: bytes, *, label: str) -> Any:
    if (
        type(payload) is not bytes
        or not payload
        or len(payload) > _MAX_LOCAL_JSON_BYTES
    ):
        raise SchemaValidationError("JSON_BYTES_EMPTY_OR_INVALID", detail=label)
    if payload.startswith(b"\xef\xbb\xbf"):
        raise SchemaValidationError("UTF8_BOM_PROHIBITED", detail=label)
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SchemaValidationError("JSON_UTF8_INVALID", detail=label) from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except SchemaValidationError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise SchemaValidationError("JSON_PARSE_INVALID", detail=label) from exc


def _require_json_instance(value: Any) -> None:
    try:
        canonical_bytes(value)
    except (CanonicalError, RecursionError) as exc:
        raise SchemaValidationError("INSTANCE_NOT_BOUNDED_JSON_VALUE") from exc


def _read_local_bytes(path: Path, *, label: str) -> bytes:
    if not isinstance(path, Path):
        raise SchemaValidationError("LOCAL_PATH_INVALID", detail=label)
    if str(path).startswith(("\\\\", "//")):
        raise SchemaValidationError("NETWORK_PATH_PROHIBITED", detail=str(path))
    try:
        before = path.lstat()
    except OSError as exc:
        raise SchemaValidationError("LOCAL_FILE_UNREADABLE", detail=label) from exc
    if (
        not stat.S_ISREG(before.st_mode)
        or before.st_nlink != 1
        or getattr(before, "st_file_attributes", 0)
        & _FILE_ATTRIBUTE_REPARSE_POINT
        or before.st_size < 1
        or before.st_size > _MAX_LOCAL_JSON_BYTES
    ):
        raise SchemaValidationError("LOCAL_FILE_NOT_BOUNDED_ORDINARY", detail=label)
    try:
        payload = path.read_bytes()
        after = path.lstat()
    except OSError as exc:
        raise SchemaValidationError("LOCAL_FILE_UNREADABLE", detail=label) from exc
    before_identity = (
        before.st_dev,
        before.st_ino,
        before.st_mode,
        before.st_nlink,
        before.st_size,
        before.st_mtime_ns,
    )
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_identity != after_identity or len(payload) != after.st_size:
        raise SchemaValidationError("LOCAL_FILE_CHANGED_DURING_READ", detail=label)
    return payload


def _schema_bytes(filename: str) -> bytes:
    if filename not in SCHEMA_SHA256 or Path(filename).name != filename:
        raise SchemaValidationError("SCHEMA_NAME_UNKNOWN", detail=filename)
    path = _SCHEMA_DIRECTORY / filename
    try:
        payload = _read_local_bytes(path, label=filename)
    except SchemaValidationError as exc:
        raise SchemaValidationError("SCHEMA_FILE_UNREADABLE", detail=filename) from exc
    observed = hashlib.sha256(payload).hexdigest()
    if observed != SCHEMA_SHA256[filename]:
        raise SchemaValidationError(
            "SCHEMA_DIGEST_MISMATCH",
            detail=f"{filename}:{observed}",
        )
    return payload


def load_schema(filename_or_id: str) -> dict[str, Any]:
    """Load a digest-authenticated supplied schema without remote resolution."""

    filename = SCHEMA_ID_TO_FILENAME.get(filename_or_id, filename_or_id)
    value = _parse_json_bytes(_schema_bytes(filename), label=filename)
    if not isinstance(value, dict):
        raise SchemaValidationError("SCHEMA_ROOT_NOT_OBJECT", detail=filename)
    if value.get("$schema") != SCHEMA_DIALECT:
        raise SchemaValidationError("SCHEMA_DIALECT_MISMATCH", detail=filename)
    return copy.deepcopy(value)


def schema_inventory() -> tuple[dict[str, str], ...]:
    """Return stable identities for all eight authenticated supplied schemas."""

    inverse = {filename: schema_id for schema_id, filename in SCHEMA_ID_TO_FILENAME.items()}
    return tuple(
        {
            "filename": filename,
            "schema_id": inverse[filename],
            "sha256": digest,
        }
        for filename, digest in sorted(SCHEMA_SHA256.items())
    )


def _schema_child_path(parent: str, token: str) -> str:
    escaped = token.replace("~", "~0").replace("/", "~1")
    return f"{parent}/{escaped}"


def _assert_schema_supported(schema: Any, *, path: str = "$") -> None:
    if isinstance(schema, bool):
        return
    if not isinstance(schema, dict):
        raise SchemaValidationError("SCHEMA_NODE_NOT_OBJECT", schema_path=path)
    unknown = sorted(set(schema) - _SUPPORTED_KEYWORDS)
    if unknown:
        raise SchemaValidationError(
            "SCHEMA_KEYWORD_UNSUPPORTED",
            schema_path=path,
            detail=",".join(unknown),
        )
    declared_type = schema.get("type")
    if declared_type is not None:
        declared_types = [declared_type] if isinstance(declared_type, str) else declared_type
        allowed_types = {"null", "boolean", "integer", "number", "string", "array", "object"}
        if (
            not isinstance(declared_types, list)
            or not declared_types
            or any(item not in allowed_types for item in declared_types)
            or len(set(declared_types)) != len(declared_types)
        ):
            raise SchemaValidationError("SCHEMA_TYPE_DECLARATION_INVALID", schema_path=path)
    required = schema.get("required", [])
    if (
        not isinstance(required, list)
        or any(not isinstance(item, str) for item in required)
        or len(set(required)) != len(required)
    ):
        raise SchemaValidationError("SCHEMA_REQUIRED_INVALID", schema_path=path)
    enumeration = schema.get("enum")
    if enumeration is not None and (
        not isinstance(enumeration, list) or not enumeration
    ):
        raise SchemaValidationError("SCHEMA_ENUM_INVALID", schema_path=path)
    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise SchemaValidationError("SCHEMA_PATTERN_INVALID", schema_path=path)
        try:
            re.compile(pattern)
        except re.error as exc:
            raise SchemaValidationError("SCHEMA_PATTERN_INVALID", schema_path=path) from exc
    if "format" in schema and schema["format"] != "date-time":
        raise SchemaValidationError("SCHEMA_FORMAT_UNSUPPORTED", schema_path=path)
    for keyword in ("minItems", "minLength", "maxLength"):
        value = schema.get(keyword)
        if value is not None and (type(value) is not int or value < 0):
            raise SchemaValidationError(
                "SCHEMA_BOUND_INVALID",
                schema_path=f"{path}/{keyword}",
            )
    minimum = schema.get("minimum")
    if minimum is not None and (
        type(minimum) not in {int, float} or not math.isfinite(minimum)
    ):
        raise SchemaValidationError("SCHEMA_BOUND_INVALID", schema_path=f"{path}/minimum")
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        raise SchemaValidationError("SCHEMA_PROPERTIES_INVALID", schema_path=path)
    for key, child in properties.items():
        if not isinstance(key, str):
            raise SchemaValidationError("SCHEMA_PROPERTY_NAME_INVALID", schema_path=path)
        _assert_schema_supported(
            child,
            path=_schema_child_path(f"{path}/properties", key),
        )
    definitions = schema.get("$defs", {})
    if not isinstance(definitions, dict):
        raise SchemaValidationError("SCHEMA_DEFS_INVALID", schema_path=path)
    for key, child in definitions.items():
        _assert_schema_supported(child, path=_schema_child_path(f"{path}/$defs", key))
    if "items" in schema:
        _assert_schema_supported(schema["items"], path=f"{path}/items")
    additional = schema.get("additionalProperties", True)
    if not isinstance(additional, bool):
        _assert_schema_supported(additional, path=f"{path}/additionalProperties")
    alternatives = schema.get("anyOf", [])
    if not isinstance(alternatives, list) or ("anyOf" in schema and not alternatives):
        raise SchemaValidationError("SCHEMA_ANY_OF_INVALID", schema_path=path)
    for index, child in enumerate(alternatives):
        _assert_schema_supported(child, path=f"{path}/anyOf/{index}")
    exact_alternatives = schema.get("oneOf", [])
    if not isinstance(exact_alternatives, list) or (
        "oneOf" in schema and not exact_alternatives
    ):
        raise SchemaValidationError("SCHEMA_ONE_OF_INVALID", schema_path=path)
    for index, child in enumerate(exact_alternatives):
        _assert_schema_supported(child, path=f"{path}/oneOf/{index}")
    unique_items = schema.get("uniqueItems")
    if unique_items is not None and type(unique_items) is not bool:
        raise SchemaValidationError("SCHEMA_UNIQUE_ITEMS_INVALID", schema_path=path)
    reference = schema.get("$ref")
    if reference is not None and (
        not isinstance(reference, str) or not reference.startswith("#/")
    ):
        raise SchemaValidationError(
            "REMOTE_OR_UNSUPPORTED_SCHEMA_REFERENCE",
            schema_path=f"{path}/$ref",
        )


def _resolve_local_reference(root_schema: Mapping[str, Any], reference: str) -> Any:
    if not reference.startswith("#/"):
        raise SchemaValidationError("REMOTE_SCHEMA_REFERENCE_PROHIBITED", detail=reference)
    current: Any = root_schema
    for encoded in reference[2:].split("/"):
        token = encoded.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, Mapping) or token not in current:
            raise SchemaValidationError("LOCAL_SCHEMA_REFERENCE_MISSING", detail=reference)
        current = current[token]
    return current


def _is_type(instance: Any, expected: str) -> bool:
    if expected == "null":
        return instance is None
    if expected == "boolean":
        return type(instance) is bool
    if expected == "integer":
        return type(instance) is int
    if expected == "number":
        return type(instance) in {int, float} and math.isfinite(instance)
    if expected == "string":
        return type(instance) is str
    if expected == "array":
        return type(instance) is list
    if expected == "object":
        return type(instance) is dict
    raise SchemaValidationError("SCHEMA_TYPE_UNSUPPORTED", detail=expected)


def _json_equal(left: Any, right: Any) -> bool:
    """Compare JSON values without Python's ``True == 1`` coercion."""

    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if left is None or right is None:
        return left is right
    if type(left) in {int, float} and type(right) in {int, float}:
        return left == right
    return type(left) is type(right) and left == right


def _valid_date_time(value: str) -> bool:
    match = _RFC3339_DATE_TIME.fullmatch(value)
    if match is None:
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _validation_error(
    code: str,
    *,
    instance_path: str,
    schema_path: str,
    detail: str | None = None,
) -> None:
    raise SchemaValidationError(
        code,
        instance_path=instance_path,
        schema_path=schema_path,
        detail=detail,
    )


def _validate_closed(
    instance: Any,
    schema: Any,
    *,
    root_schema: Mapping[str, Any],
    instance_path: str = "$",
    schema_path: str = "$",
) -> None:
    if schema is True:
        return
    if schema is False:
        _validation_error(
            "FALSE_SCHEMA_REJECTED_INSTANCE",
            instance_path=instance_path,
            schema_path=schema_path,
        )
    if not isinstance(schema, Mapping):
        _validation_error(
            "SCHEMA_NODE_NOT_OBJECT",
            instance_path=instance_path,
            schema_path=schema_path,
        )

    if "$ref" in schema:
        reference = schema["$ref"]
        if not isinstance(reference, str):
            _validation_error(
                "SCHEMA_REFERENCE_INVALID",
                instance_path=instance_path,
                schema_path=f"{schema_path}/$ref",
            )
        target = _resolve_local_reference(root_schema, reference)
        _validate_closed(
            instance,
            target,
            root_schema=root_schema,
            instance_path=instance_path,
            schema_path=f"{schema_path}/$ref({reference})",
        )

    if "anyOf" in schema:
        alternatives = schema["anyOf"]
        matched = False
        for index, alternative in enumerate(alternatives):
            try:
                _validate_closed(
                    instance,
                    alternative,
                    root_schema=root_schema,
                    instance_path=instance_path,
                    schema_path=f"{schema_path}/anyOf/{index}",
                )
            except SchemaValidationError:
                continue
            matched = True
            break
        if not matched:
            _validation_error(
                "ANY_OF_NO_MATCH",
                instance_path=instance_path,
                schema_path=f"{schema_path}/anyOf",
            )

    if "oneOf" in schema:
        match_count = 0
        for index, alternative in enumerate(schema["oneOf"]):
            try:
                _validate_closed(
                    instance,
                    alternative,
                    root_schema=root_schema,
                    instance_path=instance_path,
                    schema_path=f"{schema_path}/oneOf/{index}",
                )
            except SchemaValidationError:
                continue
            match_count += 1
        if match_count != 1:
            _validation_error(
                "ONE_OF_MATCH_COUNT_INVALID",
                instance_path=instance_path,
                schema_path=f"{schema_path}/oneOf",
                detail=str(match_count),
            )

    if "type" in schema:
        expected = schema["type"]
        expected_types = [expected] if isinstance(expected, str) else expected
        if not isinstance(expected_types, list) or not expected_types or not all(
            isinstance(item, str) for item in expected_types
        ):
            _validation_error(
                "SCHEMA_TYPE_DECLARATION_INVALID",
                instance_path=instance_path,
                schema_path=f"{schema_path}/type",
            )
        if not any(_is_type(instance, item) for item in expected_types):
            _validation_error(
                "TYPE_MISMATCH",
                instance_path=instance_path,
                schema_path=f"{schema_path}/type",
                detail="|".join(expected_types),
            )

    if "const" in schema and not _json_equal(instance, schema["const"]):
        _validation_error(
            "CONST_MISMATCH",
            instance_path=instance_path,
            schema_path=f"{schema_path}/const",
        )
    if "enum" in schema and not any(
        _json_equal(instance, candidate) for candidate in schema["enum"]
    ):
        _validation_error(
            "ENUM_MISMATCH",
            instance_path=instance_path,
            schema_path=f"{schema_path}/enum",
        )

    if isinstance(instance, str):
        pattern = schema.get("pattern")
        if pattern is not None:
            try:
                matched = re.search(pattern, instance) is not None
            except re.error as exc:
                raise SchemaValidationError(
                    "SCHEMA_PATTERN_INVALID",
                    instance_path=instance_path,
                    schema_path=f"{schema_path}/pattern",
                ) from exc
            if not matched:
                _validation_error(
                    "PATTERN_MISMATCH",
                    instance_path=instance_path,
                    schema_path=f"{schema_path}/pattern",
                )
        if "minLength" in schema and len(instance) < schema["minLength"]:
            _validation_error(
                "STRING_TOO_SHORT",
                instance_path=instance_path,
                schema_path=f"{schema_path}/minLength",
            )
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            _validation_error(
                "STRING_TOO_LONG",
                instance_path=instance_path,
                schema_path=f"{schema_path}/maxLength",
            )
        if schema.get("format") == "date-time" and not _valid_date_time(instance):
            _validation_error(
                "DATE_TIME_FORMAT_INVALID",
                instance_path=instance_path,
                schema_path=f"{schema_path}/format",
            )

    if type(instance) in {int, float} and type(instance) is not bool:
        if "minimum" in schema and instance < schema["minimum"]:
            _validation_error(
                "NUMBER_BELOW_MINIMUM",
                instance_path=instance_path,
                schema_path=f"{schema_path}/minimum",
            )

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            _validation_error(
                "ARRAY_TOO_SHORT",
                instance_path=instance_path,
                schema_path=f"{schema_path}/minItems",
            )
        if "items" in schema:
            for index, item in enumerate(instance):
                _validate_closed(
                    item,
                    schema["items"],
                    root_schema=root_schema,
                    instance_path=f"{instance_path}/{index}",
                    schema_path=f"{schema_path}/items",
                )
        if schema.get("uniqueItems") is True:
            for index, item in enumerate(instance):
                if any(_json_equal(item, prior) for prior in instance[:index]):
                    _validation_error(
                        "ARRAY_ITEMS_NOT_UNIQUE",
                        instance_path=f"{instance_path}/{index}",
                        schema_path=f"{schema_path}/uniqueItems",
                    )

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                _validation_error(
                    "REQUIRED_PROPERTY_MISSING",
                    instance_path=instance_path,
                    schema_path=f"{schema_path}/required",
                    detail=key,
                )
        properties = schema.get("properties", {})
        for key, child_schema in properties.items():
            if key in instance:
                _validate_closed(
                    instance[key],
                    child_schema,
                    root_schema=root_schema,
                    instance_path=_schema_child_path(instance_path, key),
                    schema_path=_schema_child_path(f"{schema_path}/properties", key),
                )
        extras = sorted(set(instance) - set(properties))
        additional = schema.get("additionalProperties", True)
        if additional is False and extras:
            _validation_error(
                "ADDITIONAL_PROPERTY_PROHIBITED",
                instance_path=_schema_child_path(instance_path, extras[0]),
                schema_path=f"{schema_path}/additionalProperties",
                detail=extras[0],
            )
        if isinstance(additional, Mapping):
            for key in extras:
                _validate_closed(
                    instance[key],
                    additional,
                    root_schema=root_schema,
                    instance_path=_schema_child_path(instance_path, key),
                    schema_path=f"{schema_path}/additionalProperties",
                )


def _validate_with_jsonschema(instance: Any, schema: Mapping[str, Any]) -> None:
    """Use jsonschema only after an explicit engine request by the caller."""

    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise SchemaValidationError("JSONSCHEMA_ENGINE_UNAVAILABLE") from exc
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    except Exception as exc:  # jsonschema exposes several version-specific subclasses
        raise SchemaValidationError("JSONSCHEMA_ENGINE_FAILURE", detail=type(exc).__name__) from exc
    if errors:
        first = errors[0]
        instance_path = "$" + "".join(f"/{part}" for part in first.path)
        schema_path = "$" + "".join(f"/{part}" for part in first.schema_path)
        raise SchemaValidationError(
            "JSONSCHEMA_INSTANCE_INVALID",
            instance_path=instance_path,
            schema_path=schema_path,
            detail=first.validator,
        )


def _validation_receipt(
    *,
    schema_id: str,
    filename: str,
    schema_sha256: str,
    engine: str,
) -> dict[str, Any]:
    return {
        "authority_effect": "NONE",
        "engine": engine,
        "network_used": False,
        "notice": VALIDATION_NOTICE,
        "result": "PASS",
        "schema_filename": filename,
        "schema_id": schema_id,
        "schema_sha256": schema_sha256,
    }


def validate_instance(
    instance: Mapping[str, Any],
    *,
    schema_id: str | None = None,
    engine: str = "closed",
) -> dict[str, Any]:
    """Validate an object against an authenticated, locally bundled schema.

    The default ``closed`` engine uses only the Python standard library.  The
    optional ``jsonschema`` engine is never imported unless named explicitly.
    """

    if not isinstance(instance, Mapping):
        raise SchemaValidationError("INSTANCE_ROOT_NOT_OBJECT")
    declared = instance.get("schema_id")
    selected = schema_id if schema_id is not None else declared
    if not isinstance(selected, str) or selected not in SCHEMA_ID_TO_FILENAME:
        raise SchemaValidationError("DECLARED_SCHEMA_ID_UNKNOWN", detail=str(selected))
    if declared != selected:
        raise SchemaValidationError(
            "DECLARED_SCHEMA_ID_MISMATCH",
            detail=f"declared={declared};selected={selected}",
        )
    filename = SCHEMA_ID_TO_FILENAME[selected]
    schema = load_schema(filename)
    _assert_schema_supported(schema)
    copied = copy.deepcopy(dict(instance))
    _require_json_instance(copied)
    if engine == "closed":
        _validate_closed(copied, schema, root_schema=schema)
    elif engine == "jsonschema":
        _validate_with_jsonschema(copied, schema)
    else:
        raise SchemaValidationError("VALIDATION_ENGINE_UNKNOWN", detail=engine)
    return _validation_receipt(
        schema_id=selected,
        filename=filename,
        schema_sha256=SCHEMA_SHA256[filename],
        engine=engine,
    )


def validate_schema_set(*, engine: str = "closed") -> dict[str, Any]:
    """Authenticate all schema bytes and check every definition locally."""

    observed_names = {
        path.name for path in _SCHEMA_DIRECTORY.glob("*.schema.json") if path.is_file()
    }
    expected_names = set(SCHEMA_SHA256)
    if observed_names != expected_names:
        difference = sorted(observed_names ^ expected_names)
        raise SchemaValidationError("SCHEMA_INVENTORY_MISMATCH", detail=",".join(difference))
    for filename in sorted(SCHEMA_SHA256):
        schema = load_schema(filename)
        _assert_schema_supported(schema)
        if engine == "jsonschema":
            try:
                from jsonschema import Draft202012Validator
            except ImportError as exc:
                raise SchemaValidationError("JSONSCHEMA_ENGINE_UNAVAILABLE") from exc
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:
                raise SchemaValidationError(
                    "JSONSCHEMA_METASCHEMA_FAILURE",
                    detail=f"{filename}:{type(exc).__name__}",
                ) from exc
        elif engine != "closed":
            raise SchemaValidationError("VALIDATION_ENGINE_UNKNOWN", detail=engine)
    return {
        "authority_effect": "NONE",
        "controlling_commission_sha256": CONTROLLING_COMMISSION_SHA256,
        "embedded_predecessor_commission_sha256": (
            EMBEDDED_PREDECESSOR_COMMISSION_SHA256
        ),
        "engine": engine,
        "network_used": False,
        "notice": VALIDATION_NOTICE,
        "result": "PASS",
        "schema_count": len(SCHEMA_SHA256),
        "schemas": [dict(row) for row in schema_inventory()],
    }


def _read_explicit_json(value: Mapping[str, Any] | bytes | Path, *, label: str) -> dict[str, Any]:
    if isinstance(value, Mapping):
        result = copy.deepcopy(dict(value))
        _require_json_instance(result)
        return result
    if isinstance(value, Path):
        payload = _read_local_bytes(value, label=label)
    elif type(value) is bytes:
        payload = value
    else:
        raise SchemaValidationError("EXPLICIT_JSON_INPUT_INVALID", detail=label)
    parsed = _parse_json_bytes(payload, label=label)
    if not isinstance(parsed, dict):
        raise SchemaValidationError("EXPLICIT_JSON_ROOT_NOT_OBJECT", detail=label)
    _require_json_instance(parsed)
    return parsed


def validate_poc01_final_base_receipt(
    receipt: Mapping[str, Any] | bytes | Path,
    *,
    schema_bytes: bytes | None = None,
    schema_path: Path | None = None,
    expected_schema_sha256: str = SCHEMA_SHA256[
        "poc01_final_base_receipt.v1.schema.json"
    ],
    engine: str = "closed",
) -> dict[str, Any]:
    """Validate a POC01 receipt from explicit object, bytes, or path.

    An explicit schema source is accepted for base-authentication workflows but
    must match its caller-supplied expected SHA-256.  Remote schema retrieval is
    never attempted.  Supplying both schema inputs fails closed.
    """

    if schema_bytes is not None and schema_path is not None:
        raise SchemaValidationError("MULTIPLE_EXPLICIT_SCHEMA_SOURCES")
    record = _read_explicit_json(receipt, label="poc01-final-base-receipt")
    schema_filename = "poc01_final_base_receipt.v1.schema.json"
    if schema_path is not None:
        if not isinstance(schema_path, Path):
            raise SchemaValidationError("EXPLICIT_SCHEMA_PATH_INVALID")
        if str(schema_path).startswith(("\\\\", "//")):
            raise SchemaValidationError(
                "NETWORK_PATH_PROHIBITED",
                detail=str(schema_path),
            )
        try:
            supplied_schema_bytes = _read_local_bytes(
                schema_path,
                label="poc01-receipt-schema",
            )
        except SchemaValidationError as exc:
            raise SchemaValidationError(
                "EXPLICIT_SCHEMA_UNREADABLE",
                detail=str(schema_path),
            ) from exc
    elif schema_bytes is not None:
        if type(schema_bytes) is not bytes or not schema_bytes:
            raise SchemaValidationError("EXPLICIT_SCHEMA_BYTES_INVALID")
        supplied_schema_bytes = schema_bytes
    else:
        supplied_schema_bytes = _schema_bytes(schema_filename)
    if type(expected_schema_sha256) is not str or not _HEX64.fullmatch(
        expected_schema_sha256
    ):
        raise SchemaValidationError("EXPECTED_SCHEMA_DIGEST_INVALID")
    observed_sha256 = hashlib.sha256(supplied_schema_bytes).hexdigest()
    if observed_sha256 != expected_schema_sha256:
        raise SchemaValidationError(
            "EXPLICIT_SCHEMA_DIGEST_MISMATCH",
            detail=observed_sha256,
        )
    schema = _parse_json_bytes(supplied_schema_bytes, label="poc01-receipt-schema")
    if not isinstance(schema, dict):
        raise SchemaValidationError("SCHEMA_ROOT_NOT_OBJECT")
    if schema.get("$schema") != SCHEMA_DIALECT:
        raise SchemaValidationError("SCHEMA_DIALECT_MISMATCH")
    properties = schema.get("properties")
    declared_schema_id = (
        properties.get("schema_id") if isinstance(properties, Mapping) else None
    )
    if not isinstance(declared_schema_id, Mapping) or declared_schema_id.get(
        "const"
    ) != "uvlm.triadicbrain.poc01.final_base_receipt.v1":
        raise SchemaValidationError("POC01_SCHEMA_ID_CONTRACT_MISMATCH")
    _assert_schema_supported(schema)
    if engine == "closed":
        _validate_closed(record, schema, root_schema=schema)
    elif engine == "jsonschema":
        _validate_with_jsonschema(record, schema)
    else:
        raise SchemaValidationError("VALIDATION_ENGINE_UNKNOWN", detail=engine)
    return _validation_receipt(
        schema_id="uvlm.triadicbrain.poc01.final_base_receipt.v1",
        filename=schema_filename if schema_path is None else str(schema_path),
        schema_sha256=observed_sha256,
        engine=engine,
    )


__all__ = [
    "CONTROLLING_COMMISSION_SHA256",
    "EMBEDDED_PREDECESSOR_COMMISSION_SHA256",
    "SCHEMA_DIALECT",
    "SCHEMA_ID_TO_FILENAME",
    "SCHEMA_SHA256",
    "SchemaValidationError",
    "load_schema",
    "schema_inventory",
    "validate_instance",
    "validate_poc01_final_base_receipt",
    "validate_schema_set",
]
