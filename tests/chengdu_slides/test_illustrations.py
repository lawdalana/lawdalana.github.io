"""Generated illustrations must remain explicitly non-documentary and contained."""
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree
from fixtures import sample_dataset, sample_sources
try:
    from scripts.chengdu_slides.illustrations import write_illustration
except ImportError:
    write_illustration=None


class IllustrationTests(unittest.TestCase):
    def test_subject_visual_is_original_and_clearly_not_a_photograph(self):
        self.assertTrue(callable(write_illustration), 'illustration writer not implemented')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            result=write_illustration(sample_dataset()['attractions'][0],sample_sources(),root)
            path=root/result['path']
            tree=ElementTree.fromstring(path.read_text())
            self.assertEqual(tree.attrib['viewBox'],'0 0 1100 1100')
            self.assertTrue(result['illustrative'])
            self.assertIn('ไม่ใช่ภาพถ่าย',result['disclosure']['th'])
            self.assertIn('非',result['disclosure']['zh-Hans'])
            self.assertIn('ORIGINAL ILLUSTRATION',path.read_text())
            self.assertIn('fixture-attraction',path.read_text())

    def test_gift_subject_theme_and_nonproduct_photo_disclosure_are_retained(self):
        item=sample_dataset()['attractions'][0]
        item.update(category='gifts',id='synthetic-seal',visual_theme='stone-name-chop')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);result=write_illustration(item,sample_sources(),root)
            self.assertEqual(result.get('visual_theme'),'stone-name-chop')
            tree=ElementTree.fromstring((root/result['path']).read_text())
            self.assertEqual(tree.attrib.get('data-subject-kind'),'seal')
            self.assertIn('สินค้า',result['disclosure']['th'])
            self.assertIn('商品',result['disclosure']['zh-Hans'])

    def test_known_gift_types_do_not_fall_back_to_an_unrelated_generic_picture(self):
        cases=[('panda-post-postcards','panda-post-ink','postcard'),('chengdu-city-tshirt','chengdu-city-wear','tshirt'),('china-city-canvas-tote','city-landmark-canvas','tote'),('custom-floral-name-calligraphy','floral-calligraphy-paper','calligraphy'),('bestore-walnut-stuffed-dates','walnut-date-snack','snack')]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for identity,theme,expected in cases:
                item=sample_dataset()['attractions'][0];item.update(category='gifts',id=identity,visual_theme=theme)
                asset=write_illustration(item,sample_sources(),root)
                tree=ElementTree.fromstring((root/asset['path']).read_text())
                with self.subTest(identity=identity):self.assertEqual(tree.attrib.get('data-subject-kind'),expected)

    def test_item_identifier_cannot_write_outside_image_directory(self):
        self.assertTrue(callable(write_illustration), 'illustration writer not implemented')
        data=sample_dataset(); data['attractions'][0]['id']='../../outside'
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            write_illustration(data['attractions'][0],sample_sources(),Path(directory))
