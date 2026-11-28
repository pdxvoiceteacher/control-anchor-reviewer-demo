"""Opt-in synthetic approval-evidence demo: python -S -B approval_control_demo.py."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from triadicbrain.assurance.ucc_plan import execute_plan, plan_digest
from triadicbrain.assurance.canonical import read_ordinary_bytes, write_exclusive_bytes
from triadicbrain.assurance.web import render_html_view
from reviewer_output import private_output, review_questions


def evaluate_evidence(record):
    """Apply one fictional policy to supplied fields without granting authority."""
    plan = {
        "schema_id": "control-anchor.ucc-plan.v1",
        "plan_id": "FICTIONAL-PURCHASE-APPROVAL",
        "version": 1,
        "steps": [
            {"id": "ITEM", "title": "Match the purchase item",
             "kind": "executable", "phase": "result", "operation": "equals",
             "arguments": {"path": "/source/item", "expected": "DEMO-PO-17"}},
            {"id": "REVISION", "title": "Match the effective purchase revision",
             "kind": "executable", "phase": "result", "operation": "equals",
             "arguments": {"path": "/source/revision", "expected": 2}},
            {"id": "DECISION", "title": "Require an explicit approval statement",
             "kind": "executable", "phase": "result", "operation": "equals",
             "arguments": {"path": "/source/statement", "expected": "APPROVE"}},
            {"id": "TIMING", "title": "Check the declared date against the stated deadline",
             "kind": "executable", "phase": "result", "operation": "date_order",
             "arguments": {"earlier": "/source/recorded_on", "later": "/evidence/deadline"}},
            {"id": "REVIEW", "title": "Human authority remains separate",
             "kind": "human_procedure", "phase": "result", "operation": None,
             "arguments": {"procedure": "Authenticate the underlying record and verify actual signatory authority before deciding."}},
        ],
    }
    return execute_plan(plan, {"source": record, "evidence": {"deadline": "2026-11-06"}}, phase="result")


def demonstration():
    """Keep item, revision and date fixed; change only the evidence statement."""
    common = {"item": "DEMO-PO-17", "revision": 2, "recorded_on": "2026-11-06"}
    cases = {
        "explicit_approval": {**common, "statement": "APPROVE"},
        "acknowledgment": {**common, "statement": "ACKNOWLEDGE"},
        "missing_statement": dict(common),
    }
    return {
        "synthetic": True,
        "provider_invoked": False,
        "authority_effect": "NONE",
        "human_decision": "NOT_PERFORMED",
        "limits": ("PASS checks supplied values only. No signature, source truth, or actual "
                   "signatory authority is verified; no purchase or release is authorized."),
        "cases": {name: {"supplied_record": record, "checks": evaluate_evidence(record)}
                  for name, record in cases.items()},
    }


MAX_FILE_BYTES = 256 * 1024


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(_value):
    raise ValueError("non-finite JSON constant")


def _load_input(path):
    raw = read_ordinary_bytes(path.absolute(), maximum_bytes=MAX_FILE_BYTES)
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys,
                       parse_constant=_reject_constant)
    if type(value) is not dict:
        raise ValueError("expected a JSON object")
    return value, hashlib.sha256(raw).hexdigest(), raw


def review_supplied_inputs(plan_path, context_path, output=None):
    """Run the existing result-phase UCC interpreter on two caller-supplied files."""
    plan, plan_file_sha, plan_raw = _load_input(plan_path)
    context, context_file_sha, context_raw = _load_input(context_path)
    checks = execute_plan(plan, context, phase="result")
    if not checks:
        raise ValueError("plan has no result-phase checks")
    result = {
        "mode": "SUPPLIED_LOCAL_INPUTS",
        "source_status": "SUPPLIED_NOT_AUTHENTICATED",
        "phase": "result",
        "plan_file_sha256": plan_file_sha,
        "context_file_sha256": context_file_sha,
        "validated_plan_sha256": plan_digest(plan),
        "provider_invoked": False,
        "authority_effect": "NONE",
        "human_decision": "NOT_PERFORMED",
        "checks": checks,
    }
    if output is not None:
        output = private_output(output)
        # Preserve the bytes actually consumed, not a reread or normalized copy.
        for name, raw in (("plan.json", plan_raw), ("context.json", context_raw),
                          ("result.json", (json.dumps(result, indent=2) + "\n").encode("utf-8"))):
            write_exclusive_bytes(output / name, raw)
        reopened = json.loads(read_ordinary_bytes(output / "result.json"))
        if reopened != result:
            raise ValueError("saved result differs")
        page = render_supplied_review(reopened)
        write_exclusive_bytes(output / "review.html", page)
    return result


def render_supplied_review(result):
    """Read-only projection of retained results; never execute a check here."""
    checks = result["checks"]
    verified = [(f"{row['control_id']}: {row['result']} - {row['observation']}",
                 "result.json") for row in checks]
    originals = [("Exact supplied control plan: " + result["plan_file_sha256"], "plan.json"),
                 ("Exact supplied evidence: " + result["context_file_sha256"], "context.json")]
    decisions = [("Human decision: " + result["human_decision"] + ". Authority effect: "
                  + result["authority_effect"] + ". Supplied facts are not authenticated.", None),
                 ("Decide whether the evidence is true and sufficient and whether the control is appropriate. "
                  "FAIL needs examination; HOLD means required evidence is missing. Neither authorizes action.", None)]
    decisions.extend((row['title'] + ": " + row['result'] + " - " + row.get('procedure', ''), None)
                     for row in checks if row['kind'] != 'executable')
    page = render_html_view("practitioner", result).decode("utf-8")
    start, end = page.index('<nav '), page.index('</nav>') + len('</nav>')
    page = page[:start] + '<nav><a href="result.json">Retained check results</a></nav>' + page[end:]
    return page.replace("<main>", "<main>" + review_questions(verified, originals, decisions), 1).encode("utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, help="local result-phase UCC plan JSON file")
    parser.add_argument("--context", type=Path, help="local evidence context JSON file")
    parser.add_argument("--output", type=Path, help="fresh private directory for exact supplied inputs, results and review.html")
    args = parser.parse_args(argv)
    if (args.plan is None) != (args.context is None):
        parser.error("--plan and --context must be supplied together")
    if args.output is not None and args.plan is None:
        parser.error("--output requires --plan and --context")
    try:
        result = (demonstration() if args.plan is None
                  else review_supplied_inputs(args.plan, args.context, args.output))
        # Escape control characters and non-ASCII safely on Windows consoles.
        payload = json.dumps(result, indent=2)
    except (OSError, ValueError, TypeError, RecursionError):
        parser.error("invalid or unreadable plan/context; no checks were reported")
    print(payload)


if __name__ == "__main__":
    main()
