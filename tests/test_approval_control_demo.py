"""Public entry-point and adverse checks over fictional records only."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from approval_control_demo import evaluate_evidence


class ApprovalControlDemoTests(unittest.TestCase):
    def test_cli_distinguishes_exact_approval_acknowledgment_and_missing_evidence(self):
        completed = subprocess.run(
            [sys.executable, "-S", "-B", str(ROOT / "approval_control_demo.py")],
            cwd=ROOT, capture_output=True, check=True, text=True, timeout=15,
        )
        self.assertEqual(completed.stderr, "")
        result = json.loads(completed.stdout)
        self.assertTrue(result["synthetic"])
        self.assertFalse(result["provider_invoked"])
        self.assertEqual(result["authority_effect"], "NONE")
        self.assertEqual(result["human_decision"], "NOT_PERFORMED")
        expected = {"explicit_approval": "PASS", "acknowledgment": "FAIL", "missing_statement": "HOLD"}
        self.assertEqual(set(result["cases"]), set(expected))
        self.assertEqual(len({row["plan_sha256"] for case in result["cases"].values()
                              for row in case["checks"]}), 1)
        decisions = {}
        common = {"item": "DEMO-PO-17", "revision": 2, "recorded_on": "2026-11-06"}
        for name, status in expected.items():
            with self.subTest(case=name):
                case = result["cases"][name]
                record = dict(case["supplied_record"])
                record.pop("statement", None)
                self.assertEqual(record, common)
                rows = {row["control_id"]: row for row in case["checks"]}
                self.assertEqual(set(rows), {"ITEM", "REVISION", "DECISION", "TIMING", "REVIEW"})
                self.assertEqual([rows[key]["result"] for key in ("ITEM", "REVISION", "TIMING")],
                                 ["PASS", "PASS", "PASS"])
                self.assertEqual(rows["DECISION"]["result"], status)
                self.assertEqual(rows["REVIEW"]["result"], "NOT_EXECUTED")
                binding = rows["DECISION"]["input_bindings"]["/source/statement"]
                self.assertEqual(binding["present"], name != "missing_statement")
                if name == "missing_statement":
                    self.assertIsNone(binding["sha256"])
                    self.assertEqual(rows["DECISION"]["observation"], "REQUIRED_INPUT_MISSING")
                decisions[name] = binding["sha256"]
        self.assertNotEqual(decisions["explicit_approval"], decisions["acknowledgment"])

    def test_same_approval_text_does_not_pass_wrong_revision_or_late_record(self):
        record = {"item": "DEMO-PO-17", "revision": 2, "recorded_on": "2026-11-06",
                  "statement": "APPROVE"}
        for field, wrong_value, failed_check in (
            ("item", "DEMO-PO-18", "ITEM"),
            ("revision", 1, "REVISION"),
            ("revision", "2", "REVISION"),
            ("recorded_on", "2026-11-07", "TIMING"),
        ):
            with self.subTest(field=field, wrong_value=wrong_value):
                rows = {row["control_id"]: row for row in
                        evaluate_evidence({**record, field: wrong_value})}
                self.assertEqual(rows["DECISION"]["result"], "PASS")
                self.assertEqual(rows[failed_check]["result"], "FAIL")
                self.assertEqual(rows["REVIEW"]["result"], "NOT_EXECUTED")


if __name__ == "__main__":
    unittest.main()
