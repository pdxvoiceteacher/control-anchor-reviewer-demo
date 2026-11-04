"""Run one bounded UCC plan over synthetic supplied data, without side effects."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from triadicbrain.assurance.ucc_plan import execute_plan


def demonstration():
    plan = {
        "schema_id": "control-anchor.ucc-plan.v1",
        "plan_id": "PUBLIC-EXPENSE-CHECK",
        "version": 1,
        "steps": [
            {"id": "TOTAL", "title": "Compare supplied line items with supplied total",
             "kind": "executable", "phase": "result", "operation": "compare_total",
             "arguments": {"terms": ["/source/items", "/source/tax"],
                           "right": "/source/total", "tolerance": "0.00"}},
            {"id": "SECTIONS", "title": "Check declared report sections contain text",
             "kind": "executable", "phase": "result", "operation": "required_sections",
             "arguments": {"path": "/source/sections", "sections": ["finding", "uncertainty"]}},
            {"id": "REVIEW", "title": "Human review remains separate",
             "kind": "human_procedure", "phase": "result", "operation": None,
             "arguments": {"procedure": "Assess the actual supporting evidence before any decision."}},
        ],
    }
    source = {"items": "12.10", "tax": "0.90", "total": "13.00",
              "sections": {"finding": "Supplied fields reconcile.",
                           "uncertainty": "Source truth has not been established."}}
    return {
        "synthetic": True,
        "provider_invoked": False,
        "authority_effect": "NONE",
        "rows": execute_plan(plan, {"source": source}, phase="result"),
        "wrong_total": execute_plan(plan, {"source": dict(source, total="13.01")}, phase="result")[0],
        "missing_total": execute_plan(plan, {"source": {k: v for k, v in source.items() if k != "total"}}, phase="result")[0],
    }


if __name__ == "__main__":
    print(json.dumps(demonstration(), indent=2, ensure_ascii=False))
