"""Release export preserves approval state without weakening preview safety."""
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
import unittest
from scripts.chengdu_slides.model import load_dataset
from scripts.chengdu_slides.render import render_standalone
ROOT=Path(__file__).resolve().parents[2]


class Marks(HTMLParser):
    def __init__(self):super().__init__();self.drafts=0;self.opinions=0
    def handle_starttag(self,tag,attrs):
        classes=(dict(attrs).get('class') or '').split()
        self.drafts+='draft-mark' in classes;self.opinions+='evidence-mark' in classes


class ReleaseExportTests(unittest.TestCase):
    def test_approved_export_retains_opinion_markers_without_a_draft_label(self):
        data=load_dataset(ROOT/'_data/chengdu_slides')
        if data['meta']['status']!='published':self.skipTest('actual release dataset is not yet approved')
        parser=Marks();parser.feed(render_standalone(data,ROOT,publication=True))
        self.assertEqual(parser.drafts,0);self.assertGreater(parser.opinions,0)

    def test_publication_export_rejects_unapproved_metadata(self):
        data=load_dataset(ROOT/'_data/chengdu_slides');data['meta']['status']='research_incomplete'
        with self.assertRaises(ValueError):render_standalone(data,ROOT,publication=True)

    def test_default_export_remains_explicitly_a_draft(self):
        data=load_dataset(ROOT/'_data/chengdu_slides');original=deepcopy(data)
        parser=Marks();parser.feed(render_standalone(data,ROOT))
        self.assertGreater(parser.drafts,0);self.assertEqual(data,original)
