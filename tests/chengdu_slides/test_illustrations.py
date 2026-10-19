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

    def test_item_identifier_cannot_write_outside_image_directory(self):
        self.assertTrue(callable(write_illustration), 'illustration writer not implemented')
        data=sample_dataset(); data['attractions'][0]['id']='../../outside'
        with tempfile.TemporaryDirectory() as directory, self.assertRaises(ValueError):
            write_illustration(data['attractions'][0],sample_sources(),Path(directory))
