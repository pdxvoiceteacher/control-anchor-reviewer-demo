"""Real local paths and retained supplied-input views; no Mac emulation claim."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import demo
import approval_control_demo as approval
from reviewer_output import private_output, scratch_parent
from triadicbrain.assurance.canonical import CanonicalError, read_ordinary_bytes


class ReviewerExperienceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=scratch_parent())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_fresh_ordinary_output_and_original_evidence(self):
        output = private_output(self.root / 'output')
        evidence = output / 'original.txt'
        evidence.write_bytes(b'original evidence\n')
        self.assertEqual(read_ordinary_bytes(evidence), b'original evidence\n')
        if os.name != 'nt':
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o700)
        with self.assertRaises(FileExistsError):
            private_output(output)
        self.assertEqual(evidence.read_bytes(), b'original evidence\n')

    def test_hard_linked_evidence_is_rejected(self):
        source = self.root / 'source.json'
        source.write_bytes(b'{}')
        alias = self.root / 'alias.json'
        try:
            os.link(source, alias)
        except OSError as exc:
            self.skipTest('Host cannot create test hard link: ' + str(exc))
        for candidate in (source, alias):
            with self.assertRaises(CanonicalError):
                approval._load_input(candidate)

    def test_system_scratch_alias_is_resolved_but_supplied_link_is_not(self):
        real = self.root / 'real'
        real.mkdir()
        alias = self.root / 'alias'
        try:
            alias.symlink_to(real, target_is_directory=True)
        except OSError as exc:
            self.skipTest('Host cannot create test symlink: ' + str(exc))
        with mock.patch('tempfile.gettempdir', return_value=str(alias)):
            self.assertEqual(scratch_parent(), real)
            with tempfile.TemporaryDirectory(dir=scratch_parent()) as scratch:
                self.assertEqual(Path(scratch).parent, real)
        with self.assertRaises(CanonicalError):
            scratch_parent(alias)
        with self.assertRaises(CanonicalError):
            demo.run_demo(alias / 'output')
        self.assertFalse((real / 'output').exists())
        source = real / 'source.json'
        source.write_bytes(b'{}')
        with self.assertRaises(CanonicalError):
            approval._load_input(alias / 'source.json')

    @unittest.skipUnless(os.name == 'nt', 'Windows junction observation only')
    def test_reparse_parent_still_rejected(self):
        real = self.root / 'real'
        real.mkdir()
        alias = self.root / 'junction'
        result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(alias), str(real)],
                                capture_output=True, timeout=10)
        if result.returncode:
            self.skipTest('Host cannot create test junction')
        self.addCleanup(alias.rmdir)
        # Real Windows reparse alias; not a mocked Mac or Apple Silicon run.
        with mock.patch('tempfile.gettempdir', return_value=str(alias)):
            self.assertEqual(scratch_parent(), real)
        with self.assertRaises(CanonicalError):
            scratch_parent(alias)
        with self.assertRaises(CanonicalError):
            private_output(alias / 'output')
        self.assertFalse((real / 'output').exists())

    def test_supplied_result_changes_and_saved_page_reopens_without_execution(self):
        plans = (
            ('COUNT', 'number_range', {'path': '/source/count', 'minimum': 2, 'maximum': 4},
             {'source': {'count': 3}}, {'source': {'count': 1}}),
            ('DATE', 'date_order', {'earlier': '/source/date', 'later': '/evidence/due'},
             {'source': {'date': '2027-02-09'}, 'evidence': {'due': '2027-02-09'}},
             {'source': {'date': '2027-02-10'}, 'evidence': {'due': '2027-02-09'}}),
        )
        for name, operation, arguments, passing, failing in plans:
            plan = {'schema_id': 'control-anchor.ucc-plan.v1', 'plan_id': name, 'version': 1,
                    'steps': [{'id': name, 'title': '<input check>', 'kind': 'executable',
                               'phase': 'result', 'operation': operation, 'arguments': arguments},
                              {'id': 'PERSON', 'title': 'Authenticate the source', 'kind': 'human_procedure',
                               'phase': 'result', 'operation': None,
                               'arguments': {'procedure': 'Verify facts and authority before acting.'}}]}
            plan_path = self.root / (name + '-plan.json')
            plan_path.write_text(json.dumps(plan), encoding='utf-8')
            identities = []
            for context, expected in ((passing, 'PASS'), (failing, 'FAIL'), ({'source': {}}, 'HOLD')):
                with self.subTest(plan=name, result=expected):
                    context_path = self.root / (name + '-' + expected + '.json')
                    raw = (json.dumps(context) + '\n').encode('utf-8')
                    context_path.write_bytes(raw)
                    output = self.root / (name + '-' + expected)
                    completed = subprocess.run([sys.executable, '-S', '-B', str(ROOT / 'approval_control_demo.py'),
                        '--plan', str(plan_path), '--context', str(context_path), '--output', str(output)],
                        capture_output=True, text=True, timeout=15)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    saved = json.loads((output / 'result.json').read_bytes())
                    self.assertEqual(saved, json.loads(completed.stdout))
                    self.assertEqual(saved['checks'][0]['result'], expected)
                    self.assertEqual(saved['checks'][1]['result'], 'NOT_EXECUTED')
                    self.assertEqual(saved['human_decision'], 'NOT_PERFORMED')
                    self.assertEqual((output / 'context.json').read_bytes(), raw)
                    self.assertEqual((output / 'plan.json').read_bytes(), plan_path.read_bytes())
                    self.assertEqual(saved['context_file_sha256'], hashlib.sha256(raw).hexdigest())
                    identities.append(saved['context_file_sha256'])
                    before = demo.file_digests(output)
                    with mock.patch.object(approval, 'execute_plan', side_effect=AssertionError('no replay')):
                        page = approval.render_supplied_review(saved)
                    self.assertEqual(page, (output / 'review.html').read_bytes())
                    self.assertIn(f'{name}: {expected}'.encode(), page)
                    self.assertIn(b'NOT_PERFORMED', page)
                    self.assertIn(b'NOT_EXECUTED', page)
                    self.assertIn(b'does not establish source truth', page)
                    self.assertIn(b'href="context.json"', page)
                    self.assertNotIn(b'<input check>', page)
                    if expected == 'HOLD':
                        self.assertIn(b'REQUIRED_INPUT_MISSING', page)
                        self.assertFalse(next(iter(saved['checks'][0]['input_bindings'].values()))['present'])
                    self.assertEqual(demo.file_digests(output), before)
            self.assertEqual(len(set(identities)), 3)


if __name__ == '__main__':
    unittest.main()
