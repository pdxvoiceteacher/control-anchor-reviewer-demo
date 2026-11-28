"""Opt-in synthetic approval-evidence demo: python -S -B approval_control_demo.py."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from triadicbrain.assurance.ucc_plan import execute_plan, plan_digest


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
    if not path.is_file():
        raise ValueError("expected a regular local file")
    with path.open("rb") as handle:
        raw = handle.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("input file exceeds byte limit")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_keys,
                       parse_constant=_reject_constant)
    if type(value) is not dict:
        raise ValueError("expected a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def review_supplied_inputs(plan_path, context_path):
    """Run the existing result-phase UCC interpreter on two caller-supplied files."""
    plan, plan_file_sha = _load_input(plan_path)
    context, context_file_sha = _load_input(context_path)
    checks = execute_plan(plan, context, phase="result")
    if not checks:
        raise ValueError("plan has no result-phase checks")
    return {
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, help="local result-phase UCC plan JSON file")
    parser.add_argument("--context", type=Path, help="local evidence context JSON file")
    args = parser.parse_args(argv)
    if (args.plan is None) != (args.context is None):
        parser.error("--plan and --context must be supplied together")
    try:
        result = (demonstration() if args.plan is None
                  else review_supplied_inputs(args.plan, args.context))
        # Escape control characters and non-ASCII safely on Windows consoles.
        payload = json.dumps(result, indent=2)
    except (OSError, ValueError, TypeError, RecursionError):
        parser.error("invalid or unreadable plan/context; no checks were reported")
    print(payload)


if __name__ == "__main__":
    main()
