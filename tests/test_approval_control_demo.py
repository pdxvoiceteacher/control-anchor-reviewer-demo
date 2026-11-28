"""Public entry-point and adverse checks over fictional records only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
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


    def run_supplied(self, plan, context):
        with TemporaryDirectory() as temp:
            plan_path = Path(temp) / "plan.json"
            context_path = Path(temp) / "context.json"
            plan_bytes, context_bytes = (
                value if isinstance(value, bytes) else json.dumps(value).encode("utf-8")
                for value in (plan, context)
            )
            plan_path.write_bytes(plan_bytes)
            context_path.write_bytes(context_bytes)
            completed = subprocess.run(
                [sys.executable, "-S", "-B", str(ROOT / "approval_control_demo.py"),
                 "--plan", str(plan_path), "--context", str(context_path)],
                cwd=ROOT, capture_output=True, text=True, timeout=15,
            )
            return (completed, hashlib.sha256(plan_bytes).hexdigest(),
                    hashlib.sha256(context_bytes).hexdigest())

    def test_local_files_drive_different_policies_and_observations(self):
        cases = (
            ("RETURN-CUTOFF", "date_order",
             {"earlier": "/source/returned", "later": "/evidence/cutoff"},
             {"source": {"returned": "2027-02-09"}, "evidence": {"cutoff": "2027-02-09"}},
             {"source": {"returned": "2027-02-10"}, "evidence": {"cutoff": "2027-02-09"}}),
            ("STOCK-COUNT", "number_range",
             {"path": "/source/units", "minimum": 18, "maximum": 21},
             {"source": {"units": 19}}, {"source": {"units": 17}}),
        )
        plan_ids = []
        for name, operation, arguments, passing, failing in cases:
            plan = {"schema_id": "control-anchor.ucc-plan.v1", "plan_id": name, "version": 1,
                    "steps": [{"id": "CHECK", "title": name, "kind": "executable", "phase": "result",
                               "operation": operation, "arguments": arguments}]}
            bindings = []
            for context, expected in ((passing, "PASS"), (failing, "FAIL"), ({"source": {}}, "HOLD")):
                with self.subTest(name=name, expected=expected):
                    completed, plan_sha, context_sha = self.run_supplied(plan, context)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    result = json.loads(completed.stdout)
                    self.assertEqual(result["mode"], "SUPPLIED_LOCAL_INPUTS")
                    self.assertEqual(result["source_status"], "SUPPLIED_NOT_AUTHENTICATED")
                    self.assertEqual(result["authority_effect"], "NONE")
                    self.assertFalse(result["provider_invoked"])
                    self.assertEqual(result["human_decision"], "NOT_PERFORMED")
                    self.assertNotIn("cases", result)
                    self.assertEqual(result["plan_file_sha256"], plan_sha)
                    self.assertEqual(result["context_file_sha256"], context_sha)
                    self.assertEqual(len(result["checks"]), 1)
                    check = result["checks"][0]
                    self.assertEqual(check["result"], expected)
                    self.assertEqual(check["plan_sha256"], result["validated_plan_sha256"])
                    bindings.append(context_sha)
            self.assertEqual(len(set(bindings)), 3)
            plan_ids.append(plan_sha)
        self.assertEqual(len(set(plan_ids)), 2)

    def test_bad_files_emit_no_result_and_do_not_echo_input(self):
        step = {"id": "CHECK", "title": "Check", "kind": "executable", "phase": "result",
                "operation": "field_present", "arguments": {"path": "/source/value"}}
        plan = {"schema_id": "control-anchor.ucc-plan.v1", "plan_id": "CHECK",
                "version": 1, "steps": [step]}
        for supplied_plan, context in (
            (plan, b'{"source":{},"source":{"value":"UNREPORTED"}}'),
            (plan, b'{"source":{"value":NaN}}'),
            (plan, b" " * (256 * 1024 + 1)),
            (plan, ["not a context object"]),
            ({**plan, "steps": [{**step, "phase": "admission"}]}, {"source": {}}),
            ({**plan, "steps": [{**step, "operation": "not_supported"}]}, {"source": {}}),
        ):
            completed, _, _ = self.run_supplied(supplied_plan, context)
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(completed.stdout, "")
            self.assertNotIn("UNREPORTED", completed.stderr)

    def test_one_argument_cannot_silently_fall_back_to_scripted_demo(self):
        result = subprocess.run(
            [sys.executable, "-S", "-B", str(ROOT / "approval_control_demo.py"),
             "--plan", "no-file.json"],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
