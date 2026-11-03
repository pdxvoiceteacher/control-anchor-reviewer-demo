"""Offline contracts for the generated public navigation map."""
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'docs/brain-map'
spec=importlib.util.spec_from_file_location('brain_builder', ROOT/'tools/build_brain_map.py')
builder=importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)

class BrainMapTests(unittest.TestCase):
    def setUp(self): self.data=json.loads((DIR/'map.json').read_text())
    def test_generated_views_are_current(self):
        for name,text in builder.render(self.data).items():
            self.assertEqual((DIR/name).read_text(),text,name)
    def test_unique_families_and_explicit_boundaries(self):
        families=self.data['families']; ids=[f['id'] for f in families]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),9)
        for f in families:
            self.assertIn(f['status'],builder.LABELS)
            self.assertTrue(f['summary'] and f['boundary'] and f['links'])
            if f['status']=='coded': self.assertTrue(any(p.startswith('src/') for _,p in f['links']))
    def test_only_existing_local_public_sources(self):
        spec=importlib.util.spec_from_file_location('integrity',ROOT/'tools/check_public_integrity.py')
        integrity=importlib.util.module_from_spec(spec);spec.loader.exec_module(integrity)
        for f in self.data['families']:
            for _,link in f['links']:
                parsed=urlsplit(link)
                self.assertFalse(parsed.scheme or parsed.netloc)
                path=(ROOT/parsed.path).resolve()
                self.assertTrue(path.is_relative_to(ROOT) and path.is_file(),link)
                if parsed.fragment:
                    self.assertIn(parsed.fragment,integrity.markdown_anchors(path.read_text()),link)
    def test_svg_accessible_and_static(self):
        root=ET.fromstring((DIR/'brain-map.svg').read_text())
        tags={el.tag.split('}')[-1] for el in root.iter()}
        self.assertTrue({'title','desc'}<=tags)
        self.assertFalse({'script','foreignObject','image','a'} & tags)
        self.assertEqual(root.attrib['viewBox'],'0 0 1080 760')
    def test_explorer_has_native_links_and_no_network_dependencies(self):
        text=(DIR/'explorer.html').read_text()
        self.assertNotIn('<script',text)
        self.assertNotIn('<iframe',text)
        self.assertNotIn(' src=',text)
        self.assertIn('lang="en"',text)
        self.assertIn(':focus-visible',text)
        self.assertIn('code{overflow-wrap:anywhere}',text)
        for f in self.data['families']:
            self.assertIn(f'<a href="#{f["id"]}" aria-label=',text)
            self.assertIn(f'<section id="{f["id"]}" tabindex="-1">',text)
            self.assertIn(f'](#{f["id"]})',(DIR/'README.md').read_text())
        self.assertNotIn('triadicbrain-open-alpha',text)
    def test_frontpage_has_graphic_and_all_families(self):
        text=(ROOT/'README.md').read_text()
        self.assertIn('docs/brain-map/brain-map.svg',text)
        for f in self.data['families']: self.assertIn('docs/brain-map/README.md#'+f['id'],text)
if __name__=='__main__':unittest.main()
