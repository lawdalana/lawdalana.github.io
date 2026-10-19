import tempfile
import unittest
from pathlib import Path
from fixtures import sample_dataset
from scripts.chengdu_slides.prepare_research import prepare_report
from scripts.chengdu_slides.validation import validate_dataset
from scripts.chengdu_slides.asset_validation import validate_assets


class PreparationTests(unittest.TestCase):
    def test_import_preserves_real_counts_and_does_not_invent_gifts(self):
        report=sample_dataset()
        from copy import deepcopy
        restaurant=deepcopy(report['attractions'][0])
        restaurant.update(id='fixture-restaurant',identity_key='SYNTHETIC-RESTAURANT',category='restaurants')
        restaurant['details']={key:'SYNTHETIC' for key in ['branch','address','specialties','budget','opening','transport','cautions']}
        restaurant['details']['observed_at']='2026-10-19'
        for unit in restaurant['units']:
            unit['id']='fixture-restaurant-'+unit['kind']
        report['restaurants']=[restaurant]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            data=prepare_report(report,root,report['meta'])
            self.assertEqual(len(data['attractions']),1)
            self.assertEqual(len(data['restaurants']),1)
            self.assertEqual(data['gifts'],[])
            self.assertEqual(data['meta']['status'],'research_incomplete')
            self.assertEqual(validate_dataset(data),[])
            self.assertEqual(validate_assets(data,root),[])
            self.assertTrue(validate_dataset(data,publication=True))

    def test_dense_units_are_split_without_dropping_or_reordering_translations(self):
        report=sample_dataset();unit=report['attractions'][0]['units'][0]
        unit['body']={'th':['ข้อมูล '+str(i) for i in range(6)],'zh-Hans':['资料 '+str(i) for i in range(6)]};unit['fact_ids']=[]
        with tempfile.TemporaryDirectory() as directory:
            data=prepare_report(report,Path(directory),report['meta'])
            parts=[u for u in data['attractions'][0]['units'] if u['kind']=='intro']
            self.assertEqual(len(parts),2)
            for lang in ['th','zh-Hans']:
                self.assertEqual([line for part in parts for line in part['body'][lang]],unit['body'][lang])
            self.assertEqual(parts[0]['id'],unit['id'])

    def test_mismatched_bilingual_bullet_boundaries_fail_before_pagination(self):
        report=sample_dataset();report['attractions'][0]['units'][0]['body']['zh-Hans'].append('额外资料')
        with tempfile.TemporaryDirectory() as directory,self.assertRaises(ValueError):
            prepare_report(report,Path(directory),report['meta'])

    def test_each_content_unit_has_a_disclosed_local_subject_illustration(self):
        report=sample_dataset()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);data=prepare_report(report,root,report['meta'])
            assets={a['id']:a for a in data['assets']}
            units=data['support']+[u for cat in ['attractions','restaurants'] for item in data[cat] for u in item['units']]
            for unit in units:
                asset=assets[unit['asset_id']]
                self.assertTrue((root/asset['path']).is_file())
                self.assertTrue(asset['illustrative'])
                self.assertIn('ไม่ใช่ภาพถ่าย',unit['alt']['th'])
