"""Strict canonical JSON and bounded local file operations for AEP01.

The declared profile is UTF-8 without a byte-order mark, NFC-normalized text,
lexicographically sorted object keys, compact JSON separators, finite numbers,
and exactly one trailing LF.  It is a project profile, not a claim of RFC 8785
conformance.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import stat
import unicodedata
from collections.abc import Mapping
from pathlib import Path
from typing import Any


MAX_CANONICAL_BYTES = 16 * 1024 * 1024
_UTF8_BOM = b"\xef\xbb\xbf"


class CanonicalError(ValueError):
    """A canonical object or bounded file operation failed closed."""


def _validate_text(value: str, *, key: bool = False) -> None:
    if unicodedata.normalize("NFC", value) != value:
        raise CanonicalError("JSON_KEY_NOT_NFC" if key else "JSON_TEXT_NOT_NFC")
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise CanonicalError("JSON_TEXT_SURROGATE_PROHIBITED")


def _validate_json_value(value: Any) -> None:
    value_type = type(value)
    if value is None or value_type is bool or value_type is int:
        return
    if value_type is float:
        if not math.isfinite(value):
            raise CanonicalError("NONFINITE_JSON_NUMBER")
        return
    if value_type is str:
        _validate_text(value)
        return
    if value_type is list:
        for item in value:
            _validate_json_value(item)
        return
    if value_type is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise CanonicalError("JSON_OBJECT_KEY_NOT_STRING")
            _validate_text(key, key=True)
            _validate_json_value(item)
        return
    raise CanonicalError("VALUE_NOT_JSON_COMPATIBLE")


def canonical_bytes(value: Any) -> bytes:
    """Return canonical UTF-8 JSON followed by exactly one LF."""

    _validate_json_value(value)
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError) as exc:
        raise CanonicalError("VALUE_NOT_CANONICAL_JSON") from exc
    return encoded + b"\n"


def sha256_bytes(payload: bytes) -> str:
    if type(payload) is not bytes:
        raise CanonicalError("SHA256_INPUT_NOT_BYTES")
    return hashlib.sha256(payload).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _strict_pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in rows:
        if key in result:
            raise CanonicalError("DUPLICATE_JSON_MEMBER")
        result[key] = value
    return result


def _reject_nonfinite(_: str) -> None:
    raise CanonicalError("NONFINITE_JSON_NUMBER")


def strict_loads(
    payload: bytes,
    *,
    maximum_bytes: int = MAX_CANONICAL_BYTES,
) -> Any:
    """Parse only bytes already encoded in the declared canonical profile."""

    if type(payload) is not bytes:
        raise CanonicalError("CANONICAL_INPUT_NOT_BYTES")
    if type(maximum_bytes) is not int or maximum_bytes < 1:
        raise CanonicalError("CANONICAL_SIZE_LIMIT_INVALID")
    if not payload or len(payload) > maximum_bytes:
        raise CanonicalError("CANONICAL_BYTES_EMPTY_OR_OVERSIZE")
    if payload.startswith(_UTF8_BOM):
        raise CanonicalError("UTF8_BOM_PROHIBITED")
    if not payload.endswith(b"\n"):
        raise CanonicalError("TRAILING_LF_REQUIRED")
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CanonicalError("UTF8_INVALID") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_nonfinite,
        )
    except CanonicalError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise CanonicalError("JSON_INVALID") from exc
    _validate_json_value(value)
    if canonical_bytes(value) != payload:
        raise CanonicalError("JSON_NOT_CANONICAL")
    return value


def strict_load_object(
    payload: bytes,
    *,
    maximum_bytes: int = MAX_CANONICAL_BYTES,
) -> dict[str, Any]:
    value = strict_loads(payload, maximum_bytes=maximum_bytes)
    if type(value) is not dict:
        raise CanonicalError("CANONICAL_OBJECT_REQUIRED")
    return value


def require_integer(
    value: Any,
    label: str,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    """Validate an integral contract field without accepting bool as int."""

    if type(value) is not int:
        raise CanonicalError(f"INTEGER_REQUIRED:{label}")
    if minimum is not None and value < minimum:
        raise CanonicalError(f"INTEGER_BELOW_MINIMUM:{label}")
    if maximum is not None and value > maximum:
        raise CanonicalError(f"INTEGER_ABOVE_MAXIMUM:{label}")
    return value


def is_link_like(path: Path) -> bool:
    """Return true for symlinks, junctions, or Windows reparse points."""

    candidate = Path(path)
    try:
        junction_probe = getattr(candidate, "is_junction", None)
        attributes = getattr(candidate.lstat(), "st_file_attributes", 0)
        return bool(
            candidate.is_symlink()
            or (junction_probe and junction_probe())
            or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        )
    except (FileNotFoundError, OSError):
        return candidate.is_symlink()


def _absolute_path(path: str | os.PathLike[str]) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute() or candidate == Path(candidate.anchor):
        raise CanonicalError("BOUNDED_ABSOLUTE_PATH_REQUIRED")
    return candidate


def require_safe_ancestors(
    path: str | os.PathLike[str],
    *,
    include_leaf: bool = True,
) -> Path:
    """Reject links/reparse points in every existing lexical path component."""

    candidate = _absolute_path(path)
    cursor = Path(candidate.anchor)
    end = len(candidate.parts) if include_leaf else max(1, len(candidate.parts) - 1)
    for part in candidate.parts[1:end]:
        cursor = cursor / part
        if os.path.lexists(cursor) and is_link_like(cursor):
            raise CanonicalError("PATH_ANCESTOR_LINK_PROHIBITED")
    if include_leaf and os.path.lexists(candidate) and is_link_like(candidate):
        raise CanonicalError("PATH_LEAF_LINK_PROHIBITED")
    return candidate


def _ordinary_directory(path: Path) -> bool:
    try:
        return path.is_dir() and not is_link_like(path)
    except OSError:
        return False


def _safe_parent_for_new(path: str | os.PathLike[str]) -> Path:
    candidate = require_safe_ancestors(path, include_leaf=False)
    leaf = candidate.name
    reserved_probe = getattr(os.path, "isreserved", None)
    reserved = (
        bool(reserved_probe(leaf))
        if callable(reserved_probe)
        else bool(getattr(candidate, "is_reserved", lambda: False)())
    )
    if (
        not leaf
        or leaf in {".", ".."}
        or leaf != leaf.strip()
        or leaf.endswith(".")
        or ":" in leaf
        or "\x00" in leaf
        or unicodedata.normalize("NFC", leaf) != leaf
        or reserved
    ):
        raise CanonicalError("OUTPUT_LEAF_NAME_UNSAFE")
    if os.path.lexists(candidate):
        raise CanonicalError("FRESH_PATH_ALREADY_EXISTS")
    parent = candidate.parent
    if not _ordinary_directory(parent):
        raise CanonicalError("OUTPUT_PARENT_NOT_ORDINARY_DIRECTORY")
    try:
        resolved_parent = parent.resolve(strict=True)
    except OSError as exc:
        raise CanonicalError("OUTPUT_PARENT_UNRESOLVABLE") from exc
    resolved = resolved_parent / candidate.name
    if resolved.parent != resolved_parent:
        raise CanonicalError("OUTPUT_PATH_ESCAPES_PARENT")
    return resolved


def require_new_root(path: str | os.PathLike[str]) -> Path:
    """Validate, but do not create, a fresh bounded root path."""

    return _safe_parent_for_new(path)


def require_existing_root(path: str | os.PathLike[str]) -> Path:
    candidate = require_safe_ancestors(path)
    if not _ordinary_directory(candidate):
        raise CanonicalError("EXISTING_ROOT_NOT_ORDINARY_DIRECTORY")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise CanonicalError("EXISTING_ROOT_UNRESOLVABLE") from exc
    if resolved == Path(resolved.anchor):
        raise CanonicalError("EXISTING_ROOT_UNBOUNDED")
    return resolved


def require_single_link_file(path: str | os.PathLike[str]) -> Path:
    candidate = require_safe_ancestors(path)
    try:
        metadata = candidate.stat()
    except OSError as exc:
        raise CanonicalError("FILE_UNREADABLE") from exc
    if (
        is_link_like(candidate)
        or not stat.S_ISREG(metadata.st_mode)
        or metadata.st_nlink != 1
    ):
        raise CanonicalError("ORDINARY_SINGLE_LINK_FILE_REQUIRED")
    return candidate


def read_ordinary_bytes(
    path: str | os.PathLike[str],
    *,
    maximum_bytes: int = MAX_CANONICAL_BYTES,
) -> bytes:
    """Read one bounded ordinary file while its full identity stays stable.

    A path-only ``read_bytes`` can race with a link or replacement operation.
    This routine authenticates both the opened descriptor and the path before
    and after the read, and rejects hardlinks, reparse points, type changes,
    size changes, and timestamp/identity changes.  Empty ordinary files are
    allowed because append-only ledgers legitimately begin empty.
    """

    if type(maximum_bytes) is not int or maximum_bytes < 0:
        raise CanonicalError("FILE_BYTE_LIMIT_INVALID")
    candidate = require_single_link_file(path)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    descriptor: int | None = None
    try:
        path_before = candidate.lstat()
        descriptor = os.open(candidate, flags)
        opened_before = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened_before.st_mode)
            or opened_before.st_nlink != 1
            or opened_before.st_size < 0
            or opened_before.st_size > maximum_bytes
        ):
            raise CanonicalError("ORDINARY_BOUNDED_FILE_REQUIRED")
        chunks: list[bytes] = []
        remaining = opened_before.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                raise CanonicalError("FILE_CHANGED_DURING_READ")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(descriptor, 1):
            raise CanonicalError("FILE_CHANGED_DURING_READ")
        opened_after = os.fstat(descriptor)
        path_after = candidate.lstat()
        require_single_link_file(candidate)
    except CanonicalError:
        raise
    except OSError as exc:
        raise CanonicalError("FILE_UNREADABLE") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    identity = lambda value: (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
    )
    if not (
        identity(path_before)
        == identity(opened_before)
        == identity(opened_after)
        == identity(path_after)
    ):
        raise CanonicalError("FILE_CHANGED_DURING_READ")
    payload = b"".join(chunks)
    if len(payload) != opened_before.st_size:
        raise CanonicalError("FILE_CHANGED_DURING_READ")
    return payload


def sha256_file(path: str | os.PathLike[str]) -> str:
    """Hash one ordinary file while descriptor and path identity stay stable."""

    candidate = require_single_link_file(path)
    digest = hashlib.sha256()
    descriptor: int | None = None
    try:
        path_before = candidate.lstat()
        descriptor = os.open(
            candidate, os.O_RDONLY | getattr(os, "O_BINARY", 0)
        )
        opened_before = os.fstat(descriptor)
        if not stat.S_ISREG(opened_before.st_mode) or opened_before.st_nlink != 1:
            raise CanonicalError("ORDINARY_SINGLE_LINK_FILE_REQUIRED")
        observed_bytes = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            observed_bytes += len(chunk)
            digest.update(chunk)
        opened_after = os.fstat(descriptor)
        path_after = candidate.lstat()
        require_single_link_file(candidate)
    except CanonicalError:
        raise
    except OSError as exc:
        raise CanonicalError("FILE_UNREADABLE") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    identity = lambda value: (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
    )
    if (
        identity(path_before)
        != identity(opened_before)
        or identity(opened_before) != identity(opened_after)
        or identity(opened_after) != identity(path_after)
        or observed_bytes != opened_before.st_size
    ):
        raise CanonicalError("FILE_CHANGED_DURING_READ")
    return digest.hexdigest()


def read_canonical_file(
    path: str | os.PathLike[str],
    *,
    maximum_bytes: int = MAX_CANONICAL_BYTES,
) -> dict[str, Any]:
    payload = read_ordinary_bytes(path, maximum_bytes=maximum_bytes)
    if not payload:
        raise CanonicalError("CANONICAL_BYTES_EMPTY_OR_OVERSIZE")
    return strict_load_object(payload, maximum_bytes=maximum_bytes)


def _temporary_peer(path: Path, purpose: str) -> Path:
    return path.parent / f".{path.name}.{purpose}-{secrets.token_hex(16)}.tmp"


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    offset = 0
    while offset < len(view):
        written = os.write(descriptor, view[offset:])
        if type(written) is not int or written <= 0:
            raise OSError("short write")
        offset += written


def _write_private_temp(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    descriptor = os.open(path, flags, 0o600)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise OSError("temporary file is not an ordinary single-link file")
        _write_all(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def write_exclusive_bytes(path: str | os.PathLike[str], payload: bytes) -> Path:
    """Atomically publish complete bytes to one fresh, single-link file."""

    if type(payload) is not bytes:
        raise CanonicalError("WRITE_PAYLOAD_NOT_BYTES")
    target = _safe_parent_for_new(path)
    temporary = _temporary_peer(target, "create")
    linked = False
    try:
        _write_private_temp(temporary, payload)
        os.link(temporary, target)
        linked = True
        temporary.unlink()
        linked = False
        require_single_link_file(target)
    except FileExistsError as exc:
        raise CanonicalError("EXCLUSIVE_OUTPUT_EXISTS") from exc
    except CanonicalError:
        raise
    except OSError as exc:
        raise CanonicalError("EXCLUSIVE_OUTPUT_FAILED") from exc
    finally:
        try:
            if linked and os.path.lexists(target):
                target.unlink()
        except OSError:
            pass
        try:
            temporary.unlink()
        except (FileNotFoundError, OSError):
            pass
    return target


def write_exclusive_object(
    path: str | os.PathLike[str],
    value: Mapping[str, Any],
) -> Path:
    if not isinstance(value, Mapping):
        raise CanonicalError("CANONICAL_OBJECT_REQUIRED")
    return write_exclusive_bytes(path, canonical_bytes(dict(value)))


def replace_bytes_atomic(
    path: str | os.PathLike[str],
    payload: bytes,
    *,
    expected_sha256: str | None = None,
) -> Path:
    """Atomically replace one ordinary single-link file, optionally using CAS."""

    if type(payload) is not bytes:
        raise CanonicalError("WRITE_PAYLOAD_NOT_BYTES")
    target = require_single_link_file(path)
    if expected_sha256 is not None:
        if (
            type(expected_sha256) is not str
            or len(expected_sha256) != 64
            or any(character not in "0123456789abcdef" for character in expected_sha256)
        ):
            raise CanonicalError("EXPECTED_SHA256_INVALID")
        if sha256_file(target) != expected_sha256:
            raise CanonicalError("REPLACE_PRECONDITION_FAILED")
    temporary = _temporary_peer(target, "replace")
    try:
        _write_private_temp(temporary, payload)
        # Recheck the link posture immediately before the bounded promotion.
        require_single_link_file(target)
        if expected_sha256 is not None and sha256_file(target) != expected_sha256:
            raise CanonicalError("REPLACE_PRECONDITION_FAILED")
        os.replace(temporary, target)
        require_single_link_file(target)
    except CanonicalError:
        raise
    except OSError as exc:
        raise CanonicalError("ATOMIC_REPLACE_FAILED") from exc
    finally:
        try:
            temporary.unlink()
        except (FileNotFoundError, OSError):
            pass
    return target


def replace_object_atomic(
    path: str | os.PathLike[str],
    value: Mapping[str, Any],
    *,
    expected_sha256: str | None = None,
) -> Path:
    if not isinstance(value, Mapping):
        raise CanonicalError("CANONICAL_OBJECT_REQUIRED")
    return replace_bytes_atomic(
        path,
        canonical_bytes(dict(value)),
        expected_sha256=expected_sha256,
    )


__all__ = [
    "CanonicalError",
    "MAX_CANONICAL_BYTES",
    "canonical_bytes",
    "is_link_like",
    "read_ordinary_bytes",
    "read_canonical_file",
    "replace_bytes_atomic",
    "replace_object_atomic",
    "require_existing_root",
    "require_integer",
    "require_new_root",
    "require_safe_ancestors",
    "require_single_link_file",
    "sha256_bytes",
    "sha256_file",
    "sha256_value",
    "strict_load_object",
    "strict_loads",
    "write_exclusive_bytes",
    "write_exclusive_object",
]
