"""Opt-in synthetic approval-evidence demo: python -S -B approval_control_demo.py."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from triadicbrain.assurance.ucc_plan import execute_plan


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


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, ensure_ascii=False))
