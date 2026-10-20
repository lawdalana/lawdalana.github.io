"""Site integration and deployment fingerprints are consumer-visible contracts."""
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fixtures import sample_dataset
from scripts.chengdu_slides import render


class Links(HTMLParser):
    def __init__(self):super().__init__();self.return_links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='a' and 'site-return' in (attrs.get('class') or '').split():self.return_links.append(attrs)


class SiteIntegrationTests(unittest.TestCase):
    def test_presentation_has_an_accessible_return_link_to_the_actual_site(self):
        parser=Links();parser.feed(render.render_deck(sample_dataset()))
        self.assertTrue(parser.return_links)
        for link in parser.return_links:
            self.assertEqual(link['href'],'https://lawdalana.github.io/')
            self.assertTrue(link.get('aria-label'))

    def test_template_changes_invalidate_the_live_content_fingerprint(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);template=root/'scripts/chengdu_slides/render.py';template.parent.mkdir(parents=True)
            template.write_text('# SYNTHETIC template version one\n')
            with patch.object(render,'ROOT',root):
                first=render.content_version(sample_dataset())
                template.write_text('# SYNTHETIC different template\n')
                self.assertNotEqual(render.content_version(sample_dataset()),first)
