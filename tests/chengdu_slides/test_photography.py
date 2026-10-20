"""Strict photographs are provenance-gated; synthetic bytes test only metadata policy."""
from copy import deepcopy
import hashlib,tempfile,unittest
from pathlib import Path
from fixtures import sample_dataset
from scripts.chengdu_slides.asset_validation import validate_assets
from scripts.chengdu_slides.render import render_deck,render_standalone
from html.parser import HTMLParser


class Sections(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.images=[]
    def handle_starttag(self,tag,attrs):
        row=dict(attrs)
        if tag=='section' and 'slide' in (row.get('class') or '').split():self.rows.append(row)
        if tag=='img':self.images.append(row)


class PhotographyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        folder=self.root/'slides/chengdu/images';folder.mkdir(parents=True)
        (folder/'test.webp').write_bytes(b'SYNTHETIC PHOTO BOUNDARY TEST; NOT AN ACTUAL IMAGE')
        (folder/'PHOTO_CREDITS.md').write_text('SYNTHETIC test-only rights record')
        self.data=sample_dataset();self.data['meta']['visual_policy']='licensed_photography'
        self.asset={'id':'fixture-image','kind':'photo','path':'slides/chengdu/images/test.webp','subject':'SYNTHETIC test only',
            'meaningful':True,'width':1600,'height':1000,'creator':'SYNTHETIC photographer','license':'CC BY-SA 4.0',
            'license_url':'https://creativecommons.org/licenses/by-sa/4.0/','source_url':'https://example.invalid/SYNTHETIC-PHOTO',
            'modifications':'SYNTHETIC resize test','license_path':'slides/chengdu/images/PHOTO_CREDITS.md','retrieved_at':'2026-10-20',
            'sha256':hashlib.sha256((folder/'test.webp').read_bytes()).hexdigest(),'license_checked':True,'photo_review':'approved',
            'depiction_scope':'exact_place','illustrative':False,'focal_point':[50,50]}
        self.data['assets']=[self.asset]

    def test_explicit_photography_policy_rejects_the_old_drawing(self):
        self.asset['kind']='diagram';self.assertTrue(validate_assets(self.data,self.root))

    def test_photo_rights_and_visual_review_cannot_be_implied(self):
        self.assertEqual(validate_assets(self.data,self.root),[])
        for key,value in [('license_checked',False),('photo_review','pending'),('license','All rights reserved'),('license_url','https://creativecommons.org/licenses/by-nc/4.0/'),('retrieved_at',None),('sha256','0'*64),('license_path','slides/chengdu/images/missing.md')]:
            original=self.asset[key];self.asset[key]=value
            with self.subTest(key=key):self.assertTrue(validate_assets(self.data,self.root))
            self.asset[key]=original

    def test_actual_license_url_without_a_trailing_slash_is_preserved(self):
        self.asset['license_url']='https://creativecommons.org/licenses/by-sa/4.0'
        self.assertEqual(validate_assets(self.data,self.root),[])
        self.assertEqual(self.asset['license_url'],'https://creativecommons.org/licenses/by-sa/4.0')

    def test_removing_the_edition_flag_cannot_bypass_photo_rights(self):
        self.data['meta'].pop('visual_policy')
        self.asset['license_checked']=False
        self.assertTrue(validate_assets(self.data,self.root))

    def test_nonexistent_cc_license_version_is_not_an_explicit_license(self):
        self.asset.update(license='CC BY 4.9',license_url='https://creativecommons.org/licenses/by/4.9/')
        self.assertTrue(validate_assets(self.data,self.root))

    def test_offline_photo_export_retains_the_complete_local_rights_notice(self):
        result=render_standalone(self.data,self.root)
        self.assertTrue('id="photo-license-notices"' in result,'photo rights notices missing from offline file')
        self.assertTrue('SYNTHETIC test-only rights record' in result)

    def test_photo_of_a_similar_dish_needs_explicit_bilingual_context(self):
        self.asset['depiction_scope']='dish_example';self.assertTrue(validate_assets(self.data,self.root))
        self.asset.update(illustrative=True,disclosure={'th':'ภาพเมนูตัวอย่าง ไม่ใช่ภาพจากร้านนี้','zh-Hans':'菜品示意照片，非该门店实拍。'})
        self.assertEqual(validate_assets(self.data,self.root),[])

    def test_photo_focal_point_cannot_inject_css_or_escape_bounds(self):
        for point in ([300,50],['50;background:url(https://example.invalid)',50],[float('nan'),50]):
            self.asset['focal_point']=point;self.assertTrue(validate_assets(self.data,self.root))

    def test_photo_layout_is_paired_and_credit_marks_image_modification(self):
        parser=Sections();text=render_deck(self.data);parser.feed(text)
        for first,second in zip(parser.rows[::2],parser.rows[1::2]):
            self.assertIn('photo-slide',first['class']);self.assertEqual(first['data-layout'],second['data-layout'])
        self.assertIn('data-visual-kind="photo"',text);self.assertIn('photo-modification',text)
        self.assertTrue(all(image.get('style')=='object-position:50% 50%' for image in parser.images))

    def test_photo_chapter_is_inserted_immediately_before_its_category(self):
        item=deepcopy(self.data['attractions'][0]);chapter=deepcopy(item['units'][0]);chapter.update(id='food-chapter',kind='photo-chapter',placement='before_restaurants',facts=item['facts'])
        self.data['support']=[chapter];parser=Sections();parser.feed(render_deck(self.data))
        self.assertEqual(parser.rows[0]['data-item-id'],item['id'])
        self.assertEqual(parser.rows[-2]['data-pair-id'],'food-chapter')
        self.assertEqual(parser.rows[-2]['data-layout'],'chapter')
