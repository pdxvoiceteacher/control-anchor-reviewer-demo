"""Exercise the real CI gate with small disposable positive/adverse repositories."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_public_integrity as gate


class PublicIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.txt').write_bytes(b'SYNTHETIC source\n')
        (self.root / 'space file.txt').write_bytes(b'SYNTHETIC second file\n')
        (self.root / 'README.md').write_text(
            '# Overview\n[second](#overview-1)\n## Overview\n'
            '[encoded filename](space%20file.txt)\n'
            '```text\n[not a link](missing-in-code.txt)\n```\n', encoding='utf-8')
        self.tracked = {'SOURCE_MANIFEST.json', 'source.txt', 'space file.txt', 'README.md'}
        rows = []
        for relative in sorted(self.tracked - {'SOURCE_MANIFEST.json'}):
            raw = (self.root / relative).read_bytes()
            rows.append({'path': relative, 'bytes': len(raw),
                         'candidate_sha256': hashlib.sha256(raw).hexdigest()})
        source = next(r for r in rows if r['path'] == 'source.txt')
        raw = (self.root / 'source.txt').read_bytes()
        source['original_sha256'] = source['candidate_sha256']
        source['original_git_blob'] = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        self.manifest = {'copied_files': [source],
                         'new_or_adapted_files': [r for r in rows if r is not source]}
        self.save()

    def save(self):
        (self.root / 'SOURCE_MANIFEST.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_complete_fixture_encoded_filename_and_duplicate_heading(self):
        self.assertEqual(gate.check_manifest(self.root, self.tracked), [])
        self.assertEqual(gate.check_links(self.root, self.tracked), [])

    def test_tamper_cannot_be_hidden_by_changing_only_candidate_hash(self):
        raw = b'CHANGED SYNTHETIC source\n'
        (self.root / 'source.txt').write_bytes(raw)
        self.assertTrue(any('SHA256 mismatch' in e for e in gate.check_manifest(self.root, self.tracked)))
        row = self.manifest['copied_files'][0]
        row.update(candidate_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
        self.save()
        self.assertIn('extracted source identity mismatch: source.txt', gate.check_manifest(self.root, self.tracked))

    def test_unlisted_tracked_file_and_duplicate_manifest_path_fail(self):
        self.assertIn('tracked file missing from manifest: extra.txt',
                      gate.check_manifest(self.root, self.tracked | {'extra.txt'}))
        self.manifest['new_or_adapted_files'].append(self.manifest['copied_files'][0])
        self.save()
        self.assertIn('duplicate manifest path: source.txt', gate.check_manifest(self.root, self.tracked))

    def test_missing_target_and_anchor_fail(self):
        (self.root / 'README.md').write_text('# Overview\n[absent](missing.txt)\n[anchor](#absent)\n', encoding='utf-8')
        errors = gate.check_links(self.root, self.tracked)
        self.assertTrue(any('missing local target: missing.txt' in e for e in errors))
        self.assertTrue(any('missing local anchor: #absent' in e for e in errors))

    def test_manifest_and_link_escape_fail(self):
        self.manifest['copied_files'][0]['path'] = '../outside.txt'
        self.save()
        self.assertTrue(any('unsafe repository path' in e for e in gate.check_manifest(self.root, self.tracked)))
        (self.root / 'README.md').write_text('[outside](../outside.md)\n', encoding='utf-8')
        self.assertTrue(any('link outside repository' in e for e in gate.check_links(self.root, self.tracked)))


if __name__ == '__main__':
    unittest.main()
