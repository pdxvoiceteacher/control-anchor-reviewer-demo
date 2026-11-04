"""Standard-library public entry-point checks; synthetic data only."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ucc_demo import demonstration
from triadicbrain.assurance.ucc_plan import execute_plan, validate_plan


class PublicUCCTests(unittest.TestCase):
    def test_real_plan_consumer_preserves_pass_fail_hold_and_human_boundary(self):
        result = demonstration()
        self.assertEqual([row["result"] for row in result["rows"]], ["PASS", "PASS", "NOT_EXECUTED"])
        self.assertEqual(result["rows"][0]["computed_total"], "13.00")
        self.assertEqual(result["wrong_total"]["result"], "FAIL")
        self.assertEqual(result["missing_total"]["result"], "HOLD")
        self.assertEqual(result["authority_effect"], "NONE")
        self.assertFalse(result["provider_invoked"])
        self.assertTrue(all(row["human_procedure"] == "NOT_EXECUTED" for row in result["rows"]))

    def test_unsupported_executable_operation_is_rejected(self):
        plan = {"schema_id": "control-anchor.ucc-plan.v1", "plan_id": "ADVERSE", "version": 1,
                "steps": [{"id": "CODE", "title": "Cannot execute arbitrary code",
                           "kind": "executable", "phase": "result", "operation": "eval",
                           "arguments": {"code": "print('not executed')"}}]}
        with self.assertRaisesRegex(ValueError, "UNKNOWN_EXECUTABLE_OPERATION"):
            validate_plan(plan)


if __name__ == "__main__":
    unittest.main()
