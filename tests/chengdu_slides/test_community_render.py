"""Community curation remains visibly attributed in imports and published rendering."""
from copy import deepcopy
from html.parser import HTMLParser
import tempfile
import unittest
from pathlib import Path
from fixtures import sample_dataset
from test_community_evidence import community_fixture
from scripts.chengdu_slides.prepare_research import prepare_report
from scripts.chengdu_slides.render import render_deck
from scripts.chengdu_slides.validation import validate_dataset


def report_fixture():
    report=sample_dataset();minimal,sources=community_fixture();gift=deepcopy(report['attractions'][0])
    gift.update(minimal);gift['name']={'th':'ตราประทับสมมติ','zh-Hans':'虚构印章'};gift['visual_theme']='seal'
    gift['details']={key:'SYNTHETIC' for key in ['product','buying_channel','price','authenticity','carriage','cautions']}
    gift['details']['observed_at']='2026-10-19'
    for unit in gift['units']:
        unit['id']='synthetic-gift-'+unit['kind'];unit['source_ids']=gift['source_ids']
    for source in sources.values():source['citation_number']=17
    report['sources']+=list(sources.values());report['gifts']=[gift]
    meta=dict(report['meta'],gift_policy='community_curated')
    return report,meta


class CommunityRenderingTests(unittest.TestCase):
    def test_market_counterpoint_pages_follow_gifts_instead_of_flooding_the_opening(self):
        import re
        data=sample_dataset();unit=deepcopy(data['attractions'][0]['units'][0])
        unit.update(id='market-counterpoint',placement='after_gifts',facts=deepcopy(data['attractions'][0]['facts']))
        data['support']=[unit]
        rendered=render_deck(data)
        ids=re.findall(r'<section class="slide" id="([^"]+)"',rendered)
        self.assertEqual(ids,['fixture-intro--th','fixture-intro--zh-Hans','fixture-details--th','fixture-details--zh-Hans','market-counterpoint--th','market-counterpoint--zh-Hans'])

    def test_approved_community_report_keeps_supported_gifts_and_disclosed_images(self):
        report,meta=report_fixture()
        with tempfile.TemporaryDirectory() as directory:
            data=prepare_report(report,Path(directory),meta)
            self.assertEqual(len(data['gifts']),1)
            self.assertEqual(validate_dataset(data),[])
            self.assertTrue(all(u['asset_id'] for u in data['gifts'][0]['units']))
            self.assertIn('ชุมชน',data['support'][2]['title']['th'])

    def test_invalid_opinion_evidence_is_not_silently_imported_as_recommendation(self):
        report,meta=report_fixture();report['gifts'][0]['purchase_evidence']['observations']=[]
        with tempfile.TemporaryDirectory() as directory,self.assertRaises(ValueError):
            prepare_report(report,Path(directory),meta)

    def test_market_policy_does_not_import_community_records_without_opt_in(self):
        report,meta=report_fixture();meta.pop('gift_policy')
        with tempfile.TemporaryDirectory() as directory:
            data=prepare_report(report,Path(directory),meta)
            self.assertEqual(data['gifts'],[])

    def test_published_render_still_discloses_community_basis_on_both_languages(self):
        report,meta=report_fixture()
        data=deepcopy(report);data['meta']=dict(meta,status='published')
        result=render_deck(data)
        self.assertEqual(result.count('data-evidence-route="C"'),4)
        self.assertEqual(result.count('class="evidence-mark"'),4)
        self.assertIn('สรุปความเห็น ไม่ใช่ยืนยันราคา',result)
        self.assertIn('意见汇总',result)
        self.assertIn('[17] SYNTHETIC DISCUSSION',result)
        self.assertIn('2024-02-03',result)
        class Marks(HTMLParser):
            def __init__(self):super().__init__();self.draft_marks=0
            def handle_starttag(self,tag,attrs):
                if 'draft-mark' in (dict(attrs).get('class') or '').split():self.draft_marks+=1
        marks=Marks();marks.feed(result)
        self.assertEqual(marks.draft_marks,0)
