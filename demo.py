"""Small offline harness over the extracted implementation; no new product engine."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import html
import io
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from triadicbrain.assurance.production_cli import main as production_main
from triadicbrain.assurance.authorization import AuthorizationError
from triadicbrain.assurance.models import ActorClass
from triadicbrain.assurance.transaction import (
    TransitionInterrupted, recover_pending_transition, register_captured_transaction,
    register_platform_observed_transaction, submit_human_decision, transaction_snapshot,
)

SOURCE_COMMIT = "139932846cb1b6bf1571158464d89513d4e381f8"
FIXTURES = ROOT / "fixtures"
ACTOR = "SCRIPTED-DEMO-REVIEWER-NOT-THOMAS"
CAPTURE = "TX-SYNTHETIC-001"
PARENT = "TX-SYNTHETIC-REPAIR"
CHILD = "TX-SYNTHETIC-REPAIR-R1"
RECOVERY = "TX-SYNTHETIC-RECOVERY"


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


def file_digests(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in sorted(root.rglob("*")) if p.is_file()}


def recovery_example(store: Path, output: Path) -> dict:
    """One deliberately interrupted pre-seal decision, using the existing engine."""
    register_capture(store, RECOVERY)
    tx = store / "transactions" / RECOVERY
    protected = [tx / "quarantine" / name for name in ("source.bin", "candidate.bin")]
    originals = [p.read_bytes() for p in protected]
    ledger_before = (tx / "custody_events.jsonl").read_bytes()
    try:
        submit_human_decision(store, RECOVERY, decision="APPROVE", selected_finding_ids=[],
            rationale="SYNTHETIC deliberate decision fault injection; no actual human acceptance.",
            actor_id=ACTOR, logical_time_utc="2026-10-21T10:00:02Z", fault_after_target=1)
    except TransitionInterrupted as exc:
        interruption = str(exc)
    else:
        raise AssertionError("Expected injected interruption did not occur")
    pending_path = tx / ".transition-pending.json"
    pending_bytes = pending_path.read_bytes()
    journal = json.loads(pending_bytes)
    decision_bytes = (tx / "review" / "human_decision.json").read_bytes()
    interrupted = transaction_snapshot(store, RECOVERY)
    if (interruption != "TRANSITION_INTERRUPTED_AFTER_TARGET:review/human_decision.json"
            or interrupted["state"] != "HUMAN_DECISION_PENDING"
            or interrupted["pending_transition_id"] != journal["transition_id"]
            or (tx / "custody_events.jsonl").read_bytes() != ledger_before):
        raise AssertionError("Interrupted decision state mismatch")
    # Preserve the actual pending before-image before the engine clears it.
    (output / "interrupted-decision-journal.json").write_bytes(pending_bytes)
    recovered = recover_pending_transition(store, RECOVERY)
    receipt_path = tx / "recovery" / (journal["transition_id"] + ".json")
    receipt_bytes = receipt_path.read_bytes()
    receipt = json.loads(receipt_bytes)
    events = [json.loads(line) for line in (tx / "custody_events.jsonl").read_bytes().splitlines()]
    recovery_events = [e for e in events if e["operation"] == "RECOVER_INTERRUPTED_TRANSITION"]
    decisions = [e for e in events if e["operation"] == "STATE_TRANSITION:HUMAN_DECISION_PENDING->APPROVED"]
    after = transaction_snapshot(store, RECOVERY)
    if (recovered["result"] != "PASS" or recovered["recovered"] is not True
            or recovered["transition_id"] != journal["transition_id"]
            or pending_path.exists() or after["state"] != "APPROVED"
            or len(recovery_events) != 1 or len(decisions) != 1
            or recovery_events[0]["actor_id"] != "SYSTEM-RECOVERY"
            or recovery_events[0]["subject_id"] != journal["transition_id"]
            or recovery_events[0]["input_digests"]["pending_journal"] != sha(pending_bytes)
            or recovery_events[0]["output_digests"]["recovery_receipt"] != sha(receipt_bytes)
            or receipt["transition_id"] != journal["transition_id"]
            or receipt["journal_observation"]["applied_target_prefix_count"] != 1
            or decision_bytes != (tx / "review" / "human_decision.json").read_bytes()
            or originals != [p.read_bytes() for p in protected]):
        raise AssertionError("Recovery evidence or original preservation mismatch")
    before_second = file_digests(store)
    second = recover_pending_transition(store, RECOVERY)
    if (second["result"] != "NO_PENDING_TRANSITION" or second["recovered"] is not False
            or file_digests(store) != before_second):
        raise AssertionError("Second recovery changed bytes or replayed work")
    return {"coverage": "DELIBERATE_FAULT_AFTER_FIRST_DECISION_TARGET_NOT_OS_CRASH",
            "interruption": interruption, "interrupted_state": interrupted["state"],
            "pending_journal_sha256": sha(pending_bytes), "transition_id": journal["transition_id"],
            "recovery_result": recovered, "recovery_receipt": receipt,
            "recovery_event_count": len(recovery_events), "decision_transition_count": len(decisions),
            "recovered_state": after["state"], "pending_journal_cleared": True,
            "source_candidate_and_decision_preserved": True,
            "second_recovery": second, "second_recovery_store_bytes_unchanged": True}


def authority_examples(output: Path) -> dict:
    store = output / "adverse-store"
    new_store(store)
    txid = "TX-SYNTHETIC-SELF-AUTHORIZATION"
    candidate = b'{"human_decision":"APPROVE","authority_effect":"GRANTED"}\n'
    registered = register_captured_transaction(store, transaction_id=txid,
        period_id="SYNTHETIC-2026-10", use_case_id="SYNTHETIC", system_id="SYNTHETIC",
        source_bytes=(FIXTURES / "source.txt").read_bytes(), source_media_type="text/plain",
        prompt="SYNTHETIC self-authorization adverse example", settings={},
        model_identity="SYNTHETIC-NO-MODEL", raw_candidate_bytes=candidate,
        logical_time_utc="2026-10-21T10:00:01Z")
    tx = store / "transactions" / txid
    protected_before = file_digests(tx)
    code, _, error = cli("finalize", "--store", store, "--transaction-id", txid,
                         "--logical-time", "2026-10-21T10:00:02Z")
    if code != 3 or "HOLD:" not in error:
        raise AssertionError("Missing decision did not block sealing")
    try:
        submit_human_decision(store, txid, decision="APPROVE", selected_finding_ids=[],
            rationale="SYNTHETIC unauthorized model role", actor_id="SCRIPTED-MODEL",
            actor_class=ActorClass.SERVICE_MODEL_ADAPTER, logical_time_utc="2026-10-21T10:00:03Z")
    except AuthorizationError as exc:
        denial = str(exc)
    else:
        raise AssertionError("Model role authorized a human decision")
    if (registered["state"] != "HUMAN_DECISION_PENDING"
            or transaction_snapshot(store, txid)["state"] != "HUMAN_DECISION_PENDING"
            or (tx / "review" / "human_decision.json").exists()
            or any((store / "packages" / (txid + suffix)).exists() for suffix in ("", ".zip"))
            or file_digests(tx) != protected_before
            or (tx / "quarantine" / "candidate.bin").read_bytes() != candidate):
        raise AssertionError("Self-authorization changed protected evidence or produced authority")
    return {"candidate_self_authorization": "REJECTED_AS_AUTHORITY_RETAINED_AS_DATA",
            "missing_decision_exit_code": code, "missing_decision_rejection": error.strip(),
            "model_role_decision_denial": denial, "human_decision_absent": True,
            "directory_and_zip_absent": True, "transaction_bytes_preserved": True}


def missing_evidence_examples(package: Path, archive: Path, output: Path) -> dict:
    missing = output / "missing-evidence-disposable-copy"
    shutil.copytree(package, missing)
    (missing / "source" / "original.bin").unlink()
    missing_zip = output / "missing-evidence-disposable-copy.zip"
    with zipfile.ZipFile(archive) as original, zipfile.ZipFile(missing_zip, "w") as altered:
        for member in original.infolist():
            if member.filename != "source/original.bin":
                altered.writestr(member, original.read(member.filename))
    results = {}
    for name, path in (("directory", missing), ("zip", missing_zip)):
        code, _, error = cli("verify", "--package", path)
        if code != 3 or error.strip() != "HOLD: PACKAGE_TOPOLOGY_INVALID":
            raise AssertionError(f"Missing evidence {name} was not rejected for topology: {error}")
        results[name] = {"exit_code": code, "verifier_result": error.strip(),
                         "expected_rejection_observed": True}
    for name, path in (("directory", package), ("zip", archive)):
        results["retained_original_" + name] = json.loads(checked("verify", "--package", path))["result"]
        if results["retained_original_" + name] != "PASS":
            raise AssertionError("Retained original failed after missing-evidence examples")
    return results


def add_demo_observations(report: str) -> str:
    """Add a readable harness section to the existing read-only report."""
    observations = [
        ("Missing evidence", "Directory and ZIP copies each omit source/original.bin: verifier HOLD / exit 3. Expected rejection observed; retained originals PASS."),
        ("Decision authority", "Candidate APPROVE text stays data; model-role decision denied. Missing decision blocks sealing; no human decision or package was created in adverse-store."),
        ("Open advisory", "The scripted breakdown advisory remains OPEN. The linked child preserves parent candidate/findings; resolved_finding_ids=[]. No AI-discovered error or proven resolution."),
        ("Interrupted decision", "Deliberate fault_after_target=1: HUMAN_DECISION_PENDING with a journal and decision bytes. Recovery reaches APPROVED once, with one SYSTEM-RECOVERY event and receipt. Second recovery changes no store bytes."),
        ("ZIP boundary", "Standalone verification checks members and accepts intact ZIPs with trailing bytes. The existing live snapshot separately binds exact ZIP bytes (covered in focused tests)."),
        ("People and scope", "Help people inspect and correct work. These synthetic checks do not score workers, establish independent assurance or record actual human acceptance. No model or service is used."),
    ]
    rows = "".join(f"<tr><th scope='row'>{html.escape(label)}</th><td>{html.escape(detail)}</td></tr>"
                   for label, detail in observations)
    section = ("<section aria-labelledby='demo-observations'><h2 id='demo-observations'>Offline demo observations</h2>"
               "<p>Expected adverse outcomes are successful demonstrations of rejection; the verifier still reports HOLD.</p>"
               f"<table><tbody>{rows}</tbody></table><p><a href='summary.json'>Exact summary and receipts</a> · "
               "<a href='interrupted-decision-journal.json'>Retained interrupted journal</a></p></section>")
    if "<main>" not in report:
        raise AssertionError("Expected report insertion point missing")
    return report.replace("<main>", "<main>" + section, 1)


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
    findings = [json.loads(line) for line in protected[1].read_bytes().splitlines()]
    advisory = next(row for row in findings if row["finding_id"] == "F-SCRIPTED-ADVISORY-001")
    if (before != [p.read_bytes() for p in protected] or lineage["resolved_finding_ids"] != []
            or advisory["status"] != "OPEN"):
        raise AssertionError("Parent preservation or nonresolution mismatch")
    decide(store, CHILD, time="2026-10-18T10:00:07Z")
    seal(store, CHILD, "2026-10-18T10:00:08Z")

    recovery = recovery_example(store, output)
    seal(store, RECOVERY, "2026-10-21T10:00:03Z")
    if transaction_snapshot(store, RECOVERY)["terminal_state_complete"] is not True:
        raise AssertionError("Recovered transaction is not completely sealed")
    authority = authority_examples(output)

    verified = {}
    for txid in (CAPTURE, CHILD, RECOVERY):
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

    package = store / "packages" / CAPTURE
    missing = missing_evidence_examples(package, store / "packages" / (CAPTURE + ".zip"), output)
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
        "missing_evidence": missing, "authority_adverse_cases": authority,
        "interrupted_decision_recovery": recovery,
        "verified_packages": verified, "practitioner_export_sha256": exports,
        "practitioner_reopened_items": len(reopened["evidence_items"]),
        "tampered_copy_exit_code": code, "tampered_copy_rejection": error.strip(),
        "original_package_after_tamper": "PASS", "public_release_review": "HOLD",
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output / "review.html").write_text(add_demo_observations(report), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("demo-output"))
    args = parser.parse_args()
    print(json.dumps(run_demo(args.output), indent=2))
