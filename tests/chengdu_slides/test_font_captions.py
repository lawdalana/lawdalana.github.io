"""Image captions must participate in local font coverage before release."""
import tempfile,unittest
from pathlib import Path
from scripts.chengdu_slides import subset_fonts


class FontCaptionTests(unittest.TestCase):
    def test_optional_photo_caption_corpus_is_included_without_changing_canonical_data(self):
        collect=getattr(subset_fonts,'collect_text',None)
        self.assertTrue(callable(collect),'photo-caption corpus support is missing')
        assert callable(collect)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);data=root/'_data/chengdu_slides';data.mkdir(parents=True)
            original='{"caption":"实景摄影"}';(data/'assets.json').write_text(original)
            extra=root/'photo-preview.json';extra.write_text('{"caption":"缩放裁切"}')
            text=subset_fonts.collect_text(root,extra)
            self.assertIn('实景摄影',text);self.assertIn('缩放裁切',text)
            self.assertEqual((data/'assets.json').read_text(),original)

    def test_fixed_interface_captions_are_included_too(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'scripts/chengdu_slides';source.mkdir(parents=True)
            (source/'render.py').write_text("label = '裁切及轻调色'")
            self.assertIn('裁切及轻调色',subset_fonts.collect_text(root))
