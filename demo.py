"""Small offline harness over the extracted implementation; no new product engine."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from triadicbrain.assurance.production_cli import main as production_main
from triadicbrain.assurance.transaction import register_platform_observed_transaction

SOURCE_COMMIT = "139932846cb1b6bf1571158464d89513d4e381f8"
FIXTURES = ROOT / "fixtures"
ACTOR = "SCRIPTED-DEMO-REVIEWER-NOT-THOMAS"
CAPTURE = "TX-SYNTHETIC-001"
PARENT = "TX-SYNTHETIC-REPAIR"
CHILD = "TX-SYNTHETIC-REPAIR-R1"


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def cli(*args: object) -> tuple[int, str, str]:
    """Call the actual parser/dispatcher and retain its UTF-8 output exactly."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = production_main([str(arg) for arg in args])
    return code, out.getvalue(), err.getvalue()


def checked(*args: object) -> str:
    code, out, err = cli(*args)
    if code != 0:
        raise RuntimeError(f"CLI {args[0]} failed: {err.strip()}")
    return out


def captured_args(candidate: str = "candidate.txt") -> list[object]:
    return ["--source-file", FIXTURES / "source.txt", "--prompt-file",
            FIXTURES / "prompt.txt", "--settings-file", FIXTURES / "settings.json",
            "--candidate-file", FIXTURES / candidate]


def new_store(store: Path) -> None:
    checked("init", "--output", store, "--predecessor-commit", SOURCE_COMMIT,
            "--predecessor-receipt-sha256", sha((FIXTURES / "predecessor-anchor.json").read_bytes()),
            "--logical-time", "2026-10-18T10:00:00Z")


def register_capture(store: Path, transaction_id: str = CAPTURE) -> dict:
    return json.loads(checked("register", "--store", store, "--transaction-id", transaction_id,
        "--period-id", "SYNTHETIC-2026-10", "--use-case-id", "SYNTHETIC-WORKSHOP",
        "--system-id", "SYNTHETIC-OFFLINE", "--source-media-type", "text/plain",
        "--model-identity", "SYNTHETIC-AUTHORED-FIXTURE-NO-MODEL",
        *captured_args(), "--logical-time", "2026-10-18T10:00:01Z"))


def register_scripted_advisory(store: Path) -> dict:
    # The existing CLI cannot inject findings. Reuse the source test's explicit
    # platform-observed boundary for this one scripted repair fixture.
    return register_platform_observed_transaction(store,
        transaction_id=PARENT, period_id="SYNTHETIC-2026-10",
        use_case_id="SYNTHETIC-WORKSHOP", system_id="SYNTHETIC-OFFLINE",
        source_bytes=(FIXTURES / "source.txt").read_bytes(), source_media_type="text/plain",
        prompt=(FIXTURES / "prompt.txt").read_text("utf-8"),
        model_identity="SYNTHETIC-AUTHORED-FIXTURE-NO-MODEL",
        settings=json.loads((FIXTURES / "settings.json").read_bytes()),
        raw_candidate_bytes=(FIXTURES / "candidate.txt").read_bytes(),
        logical_time_utc="2026-10-18T10:00:04Z", admitted=True, candidate_captured=True,
        review_findings=[json.loads((FIXTURES / "advisory.json").read_bytes())])


def decide(store: Path, txid: str, *, repair: bool = False, time: str) -> None:
    selected = ["--finding-id", "F-SCRIPTED-ADVISORY-001"] if repair else []
    checked("decide", "--store", store, "--transaction-id", txid,
            "--decision", "REQUEST_REPAIR" if repair else "APPROVE", *selected,
            "--rationale-file", FIXTURES / ("request-repair.txt" if repair else "approve.txt"),
            "--actor-id", ACTOR, "--logical-time", time)


def repair_child(store: Path, *, changed: str = "candidate") -> dict:
    return json.loads(checked("repair", "--store", store, "--parent-transaction-id", PARENT,
        "--child-transaction-id", CHILD, "--changed-input", changed,
        *captured_args("repaired-candidate.txt"), "--logical-time", "2026-10-18T10:00:06Z"))


def seal(store: Path, txid: str, time: str) -> None:
    checked("finalize", "--store", store, "--transaction-id", txid, "--logical-time", time)


def run_demo(output: Path) -> dict:
    output = output.absolute()
    # Fresh output only: never erase or overwrite a previous run.
    output.mkdir(parents=False, exist_ok=False)
    store = output / "store"
    new_store(store)
    snapshot = register_capture(store)
    if snapshot["provider_invoked"] is not False:
        raise AssertionError("Unexpected provider invocation")
    decide(store, CAPTURE, time="2026-10-18T10:00:02Z")
    seal(store, CAPTURE, "2026-10-18T10:00:03Z")

    register_scripted_advisory(store)
    parent = store / "transactions" / PARENT
    protected = [parent / "quarantine" / "candidate.bin", parent / "review" / "findings.jsonl"]
    before = [p.read_bytes() for p in protected]
    decide(store, PARENT, repair=True, time="2026-10-18T10:00:05Z")
    lineage = repair_child(store)["lineage"]
    if before != [p.read_bytes() for p in protected] or lineage["resolved_finding_ids"] != []:
        raise AssertionError("Parent preservation or nonresolution mismatch")
    decide(store, CHILD, time="2026-10-18T10:00:07Z")
    seal(store, CHILD, "2026-10-18T10:00:08Z")

    verified = {}
    for txid in (CAPTURE, CHILD):
        for suffix in ("", ".zip"):
            key = txid + suffix
            receipt = json.loads(checked("verify", "--package", store / "packages" / key))
            if receipt["result"] != "PASS":
                raise AssertionError("Verification failed")
            verified[key] = receipt["result"]

    exports = {}
    for format_name in ("json", "jsonl", "csv"):
        payload = checked("export", "--store", store, "--format", format_name).encode("utf-8")
        target = output / f"practitioner.{format_name}"
        target.write_bytes(payload)
        if target.read_bytes() != payload:
            raise AssertionError("Export reopen changed bytes")
        exports[target.name] = sha(payload)
    reopened = json.loads((output / "practitioner.json").read_bytes())
    if not reopened.get("evidence_items"):
        raise AssertionError("Reopened practitioner export is empty")
    report = checked("report", "--store", store, "--view", "practitioner", "--format", "html")
    (output / "review.html").write_bytes(report.encode("utf-8"))

    package = store / "packages" / CAPTURE
    tampered = output / "tampered-disposable-copy"
    shutil.copytree(package, tampered)
    (tampered / "source" / "original.bin").write_bytes(b"SYNTHETIC TAMPERING\n")
    code, _, error = cli("verify", "--package", tampered)
    if code != 3 or "HOLD:" not in error:
        raise AssertionError("Tampered copy was not rejected")
    # Verify the retained original again after attacking only the disposable copy.
    if json.loads(checked("verify", "--package", package))["result"] != "PASS":
        raise AssertionError("Original package changed")
    summary = {
        "demonstration": "OFFLINE EVIDENCE AND REVIEW COMPONENT DEMONSTRATION",
        "source_commit": SOURCE_COMMIT, "provider_invoked": False,
        "review_decision": "SCRIPTED_NOT_THOMAS_APPROVAL",
        "repair_finding": "INJECTED_SYNTHETIC_ADVISORY_NOT_AI_DISCOVERED",
        "parent_candidate_and_findings_unchanged": True,
        "resolved_finding_ids": lineage["resolved_finding_ids"],
        "verified_packages": verified, "practitioner_export_sha256": exports,
        "practitioner_reopened_items": len(reopened["evidence_items"]),
        "tampered_copy_exit_code": code, "tampered_copy_rejection": error.strip(),
        "original_package_after_tamper": "PASS", "public_release_review": "HOLD",
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("demo-output"))
    args = parser.parse_args()
    print(json.dumps(run_demo(args.output), indent=2))
