"""Public demonstration contract, with actual extracted package consumers."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import retrosynthesis_demo


class RetrosynthesisDemoTests(unittest.TestCase):
    def test_real_reconstruction_and_all_five_comparison_dispositions(self):
        result = retrosynthesis_demo.demonstration()
        self.assertTrue(result["sophia_reconstruction_matches"])
        self.assertFalse(result["full_sophia_evaluation_performed"])
        self.assertFalse(result["provider_invoked"])
        report = result["comparison"]
        self.assertEqual([row["disposition"] for row in report["comparisons"]],
            ["EXACT_DUPLICATE", "RELATED_HYPOTHESIS", "DECLARED_REFERENCE_ROLE_CONFLICT", "UNKNOWN_COMPARISON", "NEEDS_TEST"])
        self.assertEqual(report["authority_effect"], "NONE")
        self.assertEqual(report["interpretation_status"], "NOT_ESTABLISHED")
        self.assertEqual(report["human_decision"], "PENDING")
        for name in ("lookup_performed", "retention_performed", "context_supplied", "dispatch_performed"):
            self.assertFalse(report[name])
        self.assertTrue(all(not row["independent_corroboration_established"] for row in report["comparisons"]))


if __name__ == "__main__":
    unittest.main()
