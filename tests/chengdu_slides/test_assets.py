"""Asset policy tests: do not treat a logo, hotlink, or unlicensed file as a photo."""
import tempfile
import unittest
from pathlib import Path
from fixtures import sample_dataset
try:
    from scripts.chengdu_slides.asset_validation import validate_assets
except ImportError:
    validate_assets = None


class AssetTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(validate_assets), 'asset validation is not implemented')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = sample_dataset()
        image = self.root / 'slides/chengdu/images/fixture.svg'
        image.parent.mkdir(parents=True)
        image.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480"><rect width="640" height="480" fill="red"/></svg>')
        self.data['assets'] = [{'id': 'fixture-image', 'path': 'slides/chengdu/images/fixture.svg',
            'kind': 'diagram', 'subject': 'SYNTHETIC TEST IMAGE', 'meaningful': True,
            'creator': 'Test fixture', 'license': 'CC0-1.0',
            'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
            'source_url': 'https://example.invalid/test-only', 'modifications': 'none',
            'width': 640, 'height': 480, 'illustrative': False}]

    def test_all_content_units_have_local_meaningful_cleared_visuals(self):
        self.assertEqual(validate_assets(self.data, self.root), [])
        for field in ['path', 'creator', 'license', 'license_url', 'source_url', 'modifications']:
            original = self.data['assets'][0].pop(field)
            with self.subTest(field=field):
                self.assertTrue(validate_assets(self.data, self.root))
            self.data['assets'][0][field] = original
        self.data['assets'][0]['kind'] = 'logo'
        self.assertTrue(validate_assets(self.data, self.root))

    def test_asset_paths_cannot_escape_deck_or_hotlink(self):
        for path in ['../secret.jpg', '/etc/passwd', 'https://outside.test/photo.jpg',
                     'slides/chengdu/images/../../../.git/config', 'slides/chengdu/images/missing.jpg']:
            self.data['assets'][0]['path'] = path
            with self.subTest(path=path):
                self.assertTrue(validate_assets(self.data, self.root))

    def test_generic_dish_photo_requires_illustration_disclosure(self):
        self.data['assets'][0]['illustrative'] = True
        self.assertTrue(validate_assets(self.data, self.root))
        self.data['assets'][0]['disclosure'] = {'th': 'ภาพประกอบ ไม่ใช่ภาพจากร้านนี้',
                                              'zh-Hans': '示意图，非该门店实拍'}
        self.assertEqual(validate_assets(self.data, self.root), [])

    def test_unassigned_or_tiny_visual_fails(self):
        self.data['attractions'][0]['units'][0]['asset_id'] = 'missing'
        self.assertTrue(validate_assets(self.data, self.root))
        self.data['attractions'][0]['units'][0]['asset_id'] = 'fixture-image'
        self.data['assets'][0]['width'] = 1
        self.assertTrue(validate_assets(self.data, self.root))

    def test_embedded_font_requires_a_real_contained_license_notice(self):
        font=dict(self.data['assets'][0],id='fixture-font',kind='font',path='slides/chengdu/fonts/fixture.woff2',license='OFL-1.1')
        folder=self.root/'slides/chengdu/fonts';folder.mkdir(parents=True)
        (folder/'fixture.woff2').write_bytes(b'SYNTHETIC FONT TEST ONLY')
        self.data['assets'].append(font)
        self.assertTrue(validate_assets(self.data,self.root))
        font['license_path']='slides/chengdu/fonts/fixture_OFL.txt'
        (folder/'fixture_OFL.txt').write_text('SYNTHETIC TEST NOTICE ONLY')
        self.assertEqual(validate_assets(self.data,self.root),[])
        font['license_path']='../../outside-license.txt'
        self.assertTrue(validate_assets(self.data,self.root))

    def test_fonts_have_local_files_and_license_records(self):
        font = dict(self.data['assets'][0], id='fixture-font', kind='font',
                    path='slides/chengdu/fonts/missing.woff2', license='OFL-1.1')
        self.data['assets'].append(font)
        self.assertTrue(validate_assets(self.data, self.root))


if __name__ == '__main__':
    unittest.main()
