"""Fixture-independent command line for the AEP01 production build.

Only captured or imported local bytes enter this dispatcher.  The module has
no pilot, demo, provider, model-download, deployment, publication, merge, or
release route.  The deterministic pilot remains available solely through the
explicit fixture-included compatibility entry point.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import AUTHORITY_EFFECT, PRODUCT_NAME, REPORT_NOTICE
from .canonical import (
    MAX_CANONICAL_BYTES,
    canonical_bytes,
    read_ordinary_bytes,
    strict_loads,
)
from .models import Decision
from .reporting import verify_period_output_directory
from .transaction import (
    create_evidence_store,
    create_repair_child,
    finalize_transaction,
    register_captured_transaction,
    submit_human_decision,
)
from .verification import verify_transaction_directory, verify_transaction_zip
from .web import (
    LOOPBACK_HOSTS,
    NONASSURANCE_HEADLINE,
    build_evidence_report,
    build_investor_view,
    build_management_view,
    build_practitioner_export,
    build_practitioner_view,
    build_transaction_view,
    render_html_view,
    serve_read_only,
)


MAX_LOCAL_INPUT_BYTES = 32 * 1024 * 1024


def _port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("port must be an integer") from exc
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be from 1 through 65535")
    return port


def _add_store(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--store", required=True, type=Path)


def _add_captured_inputs(parser: argparse.ArgumentParser, *, repair: bool = False) -> None:
    parser.add_argument("--source-file", required=True, type=Path)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--settings-file", required=True, type=Path)
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--logical-time", required=True)
    if repair:
        parser.add_argument("--changed-input", action="append", required=True)


def build_parser(*, prog: str = "triadicbrain") -> argparse.ArgumentParser:
    """Build the fixture-independent captured-output command surface."""

    parser = argparse.ArgumentParser(
        prog=prog,
        description=(
            f"{PRODUCT_NAME}. Captured/imported output only. {NONASSURANCE_HEADLINE}."
        ),
    )
    commands = parser.add_subparsers(dest="assurance_command", required=True)

    init = commands.add_parser("init", help="create a fresh bounded local evidence store")
    init.add_argument("--output", required=True, type=Path)
    init.add_argument("--predecessor-commit", required=True)
    init.add_argument("--predecessor-receipt-sha256", required=True)
    init.add_argument("--logical-time", required=True)

    register = commands.add_parser(
        "register", help="register one deterministic captured-output transaction"
    )
    _add_store(register)
    register.add_argument("--transaction-id", required=True)
    register.add_argument("--period-id", required=True)
    register.add_argument("--use-case-id", required=True)
    register.add_argument("--system-id", required=True)
    register.add_argument("--source-media-type", required=True)
    register.add_argument("--model-identity", required=True)
    _add_captured_inputs(register)
    register.add_argument("--review-profile", default="STANDARD")
    register.add_argument("--disable-review-policy", action="store_true")

    decide = commands.add_parser("decide", help="record one explicit human decision")
    _add_store(decide)
    decide.add_argument("--transaction-id", required=True)
    decide.add_argument(
        "--decision",
        required=True,
        choices=tuple(item.value for item in Decision),
    )
    decide.add_argument("--finding-id", action="append", default=[])
    decide.add_argument("--rationale-file", required=True, type=Path)
    decide.add_argument("--actor-id", required=True)
    decide.add_argument("--logical-time", required=True)

    repair = commands.add_parser(
        "repair", help="create a repair workflow run from captured output"
    )
    _add_store(repair)
    repair.add_argument("--parent-transaction-id", required=True)
    repair.add_argument("--child-transaction-id", required=True)
    _add_captured_inputs(repair, repair=True)

    finalize = commands.add_parser(
        "finalize", help="seal one finalizable transaction and deterministic ZIP"
    )
    _add_store(finalize)
    finalize.add_argument("--transaction-id", required=True)
    finalize.add_argument("--logical-time", required=True)

    verify = commands.add_parser(
        "verify", help="verify a package without executing a model or package content"
    )
    verify.add_argument("--package", required=True, type=Path)

    verify_period = commands.add_parser(
        "verify-period",
        help="verify an exact period-output member set and checksums offline",
    )
    verify_period.add_argument("--period-output", required=True, type=Path)

    report = commands.add_parser("report", help="render a read-only evidence view")
    _add_store(report)
    report.add_argument(
        "--view",
        choices=("evidence", "management", "investor", "practitioner", "transaction"),
        default="evidence",
    )
    report.add_argument("--format", choices=("json", "html"), default="json")
    report.add_argument("--period-id")
    report.add_argument("--transaction-id")

    export = commands.add_parser(
        "export",
        help="stream a complete read-only practitioner JSON, JSONL, or CSV export",
    )
    _add_store(export)
    export.add_argument("--format", choices=("json", "jsonl", "csv"), required=True)
    export.add_argument("--period-id")

    serve = commands.add_parser(
        "serve", help="serve read-only views on an explicitly selected loopback"
    )
    _add_store(serve)
    serve.add_argument(
        "--host", choices=tuple(sorted(LOOPBACK_HOSTS)), default="127.0.0.1"
    )
    serve.add_argument("--port", type=_port, default=8765)
    return parser


def _absolute(path: Path, *, strict: bool) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    # Keep the lexical path so bounded downstream checks can reject a link-like
    # ancestor. ``strict`` documents whether the eventual operation expects an
    # existing or fresh target.
    _ = strict
    return candidate.absolute()


def _read_bytes(path: Path, label: str, *, maximum: int = MAX_LOCAL_INPUT_BYTES) -> bytes:
    try:
        return read_ordinary_bytes(
            _absolute(path, strict=True), maximum_bytes=maximum
        )
    except (OSError, ValueError) as exc:
        raise ValueError(f"{label}_BOUNDED_ORDINARY_FILE_REQUIRED") from exc


def _read_text(path: Path, label: str) -> str:
    payload = _read_bytes(path, label)
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label}_UTF8_INVALID") from exc
    if text.startswith("\ufeff"):
        raise ValueError(f"{label}_UTF8_BOM_PROHIBITED")
    if unicodedata.normalize("NFC", text) != text:
        raise ValueError(f"{label}_TEXT_NOT_NFC")
    return text


def _read_json(path: Path, label: str) -> Any:
    payload = _read_bytes(path, label, maximum=MAX_CANONICAL_BYTES)
    try:
        return strict_loads(payload)
    except ValueError as exc:
        raise ValueError(f"{label}_CANONICAL_JSON_INVALID") from exc


def _object_file(path: Path | None, label: str) -> dict[str, Any]:
    if path is None:
        return {}
    value = _read_json(path, label)
    if type(value) is not dict:
        raise ValueError(f"{label}_OBJECT_REQUIRED")
    return value


def _emit_json(value: Mapping[str, Any]) -> None:
    payload = canonical_bytes(dict(value))
    stream = getattr(sys.stdout, "buffer", None)
    if stream is not None:
        stream.write(payload)
        stream.flush()
    else:
        sys.stdout.write(payload.decode("utf-8"))


def _emit_bytes(payload: bytes) -> None:
    stream = getattr(sys.stdout, "buffer", None)
    if stream is not None:
        stream.write(payload)
        stream.flush()
    else:
        sys.stdout.write(payload.decode("utf-8"))


def _report(args: argparse.Namespace) -> int:
    builders = {
        "evidence": build_evidence_report,
        "management": build_management_view,
        "investor": build_investor_view,
        "practitioner": build_practitioner_view,
    }
    if args.view == "transaction":
        if not args.transaction_id:
            raise ValueError("TRANSACTION_ID_REQUIRED_FOR_TRANSACTION_VIEW")
        if args.period_id is not None:
            raise ValueError("PERIOD_ID_NOT_VALID_FOR_TRANSACTION_VIEW")
        payload = build_transaction_view(
            _absolute(args.store, strict=True), args.transaction_id
        )
    else:
        if args.transaction_id is not None:
            raise ValueError("TRANSACTION_ID_ONLY_VALID_FOR_TRANSACTION_VIEW")
        payload = builders[args.view](
            _absolute(args.store, strict=True),
            period_id=args.period_id,
        )
    if args.format == "json":
        _emit_json(payload)
    else:
        rendered = render_html_view(args.view, payload).decode("utf-8")
        sys.stdout.write(rendered)
    return 0


def dispatch(args: argparse.Namespace) -> int:
    """Execute one parsed fixture-independent assurance command."""

    command = args.assurance_command
    if command == "init":
        result = create_evidence_store(
            _absolute(args.output, strict=False),
            predecessor_commit=args.predecessor_commit,
            predecessor_receipt_sha256=args.predecessor_receipt_sha256,
            created_at_utc=args.logical_time,
        )
        _emit_json(result)
        return 0 if result.get("result") == "PASS" else 3
    if command == "register":
        result = register_captured_transaction(
            _absolute(args.store, strict=True),
            transaction_id=args.transaction_id,
            period_id=args.period_id,
            use_case_id=args.use_case_id,
            system_id=args.system_id,
            source_bytes=_read_bytes(args.source_file, "SOURCE"),
            source_media_type=args.source_media_type,
            prompt=_read_text(args.prompt_file, "PROMPT"),
            model_identity=args.model_identity,
            settings=_object_file(args.settings_file, "SETTINGS"),
            raw_candidate_bytes=_read_bytes(args.candidate_file, "CANDIDATE"),
            logical_time_utc=args.logical_time,
            review_profile_id=args.review_profile,
            review_policy_enabled=not args.disable_review_policy,
        )
        _emit_json(result)
        return 0
    if command == "decide":
        result = submit_human_decision(
            _absolute(args.store, strict=True),
            args.transaction_id,
            decision=args.decision,
            selected_finding_ids=tuple(sorted(args.finding_id)),
            rationale=_read_text(args.rationale_file, "RATIONALE"),
            actor_id=args.actor_id,
            logical_time_utc=args.logical_time,
        )
        _emit_json(result)
        return 0
    if command == "repair":
        result = create_repair_child(
            _absolute(args.store, strict=True),
            args.parent_transaction_id,
            child_transaction_id=args.child_transaction_id,
            changed_inputs=tuple(sorted(args.changed_input)),
            source_bytes=_read_bytes(args.source_file, "SOURCE"),
            prompt=_read_text(args.prompt_file, "PROMPT"),
            settings=_object_file(args.settings_file, "SETTINGS"),
            raw_candidate_bytes=_read_bytes(args.candidate_file, "CANDIDATE"),
            logical_time_utc=args.logical_time,
        )
        _emit_json(result)
        return 0
    if command == "finalize":
        result = finalize_transaction(
            _absolute(args.store, strict=True),
            args.transaction_id,
            logical_time_utc=args.logical_time,
        )
        _emit_json(result)
        return 0 if result.get("result") == "PASS" else 3
    if command == "verify":
        package = _absolute(args.package, strict=True)
        result = (
            verify_transaction_directory(package)
            if package.is_dir()
            else verify_transaction_zip(package)
        )
        _emit_json(result)
        return 0 if result.get("result") == "PASS" else 3
    if command == "verify-period":
        result = verify_period_output_directory(
            _absolute(args.period_output, strict=True)
        )
        _emit_json(result)
        return 0 if result.get("result") == "PASS" else 3
    if command == "report":
        return _report(args)
    if command == "export":
        _, payload = build_practitioner_export(
            _absolute(args.store, strict=True),
            args.format,
            period_id=args.period_id,
        )
        _emit_bytes(payload)
        return 0
    if command == "serve":
        status = {
            "authority_effect": AUTHORITY_EFFECT,
            "headline": NONASSURANCE_HEADLINE,
            "host": args.host,
            "network_effect": "EXPLICIT_LOOPBACK_SERVER_ONLY",
            "port": args.port,
            "provider_invoked": False,
            "report_notice": REPORT_NOTICE,
            "store": str(_absolute(args.store, strict=True)),
        }
        _emit_json(status)
        try:
            serve_read_only(_absolute(args.store, strict=True), args.host, args.port)
        except KeyboardInterrupt:
            pass
        return 0
    raise ValueError("UNKNOWN_ASSURANCE_COMMAND")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return dispatch(args)
    except (OSError, PermissionError, ValueError) as exc:
        # Never echo source, prompt, rationale, or candidate bytes.
        print(f"HOLD: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_parser", "dispatch", "main"]
