"""Renderer behavior: pairing, escaping, deterministic output, and release gating."""
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
from fixtures import sample_dataset, DATA_DIR, ROOT
try:
    from scripts.chengdu_slides.render import render_deck, build_deck
except ImportError:
    render_deck = build_deck = None


class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.slides=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag == 'section' and 'slide' in a.get('class','').split():
            self.slides.append(a)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(render_deck), 'renderer is not implemented')
        self.assertTrue(callable(build_deck), 'release builder is not implemented')
        self.data=sample_dataset()
        self.data['assets']=[{'id':'fixture-image','path':'slides/chengdu/images/fixture.svg',
            'creator':'Synthetic fixture','license':'CC0-1.0',
            'license_url':'https://creativecommons.org/publicdomain/zero/1.0/',
            'source_url':'https://example.invalid/fixture','kind':'diagram'}]

    def test_render_is_deterministic(self):
        self.assertEqual(render_deck(self.data),render_deck(self.data))

    def test_all_pairs_are_adjacent_th_then_zh_hans(self):
        parser=SlideParser(); parser.feed(render_deck(self.data))
        self.assertEqual(len(parser.slides),4)
        for th,zh in zip(parser.slides[::2],parser.slides[1::2]):
            self.assertEqual((th['data-lang'],zh['data-lang']),('th','zh-Hans'))
            self.assertEqual(th['data-pair-id'],zh['data-pair-id'])
            self.assertEqual(th['data-source-ids'],zh['data-source-ids'])
            self.assertEqual(th['data-fact-ids'],zh['data-fact-ids'])

    def test_body_text_is_escaped_not_executable_html(self):
        self.data['attractions'][0]['units'][0]['body']['th']=['<script>alert(1)</script>']
        rendered=render_deck(self.data)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',rendered)
        self.assertNotIn('<script>alert(1)</script>',rendered)

    def test_translations_share_one_logical_page_number(self):
        import re
        from scripts.chengdu_slides.render import render_deck as render
        rendered=render(self.data)
        numbers=re.findall(r'class="page-no">(\d+)</span>',rendered)
        self.assertEqual(numbers,['001','001','002','002'])

    def test_fact_values_are_identical_in_both_languages(self):
        rendered=render_deck(self.data)
        self.assertEqual(rendered.count('50 CNY'),4)

    def test_no_javascript_still_exposes_content(self):
        rendered=render_deck(self.data)
        self.assertIn('<noscript>',rendered)
        self.assertIn('ข้อมูลทดสอบ',rendered)
        self.assertIn('测试数据',rendered)

    def test_inline_styles_and_script_have_no_runtime_cdn_dependency(self):
        rendered=render_deck(self.data)
        self.assertIn('<style>',rendered)
        self.assertIn('<script>',rendered)
        self.assertNotIn('<script src=',rendered)
        self.assertNotIn('fonts.googleapis.com',rendered)

    def test_incomplete_data_is_visibly_marked_as_draft(self):
        self.assertIn('DRAFT',render_deck(self.data))

    def test_release_build_rejects_incomplete_or_unqualified_data(self):
        import tempfile,json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);data_dir=root/'_data/chengdu_slides';data_dir.mkdir(parents=True)
            for key,value in sample_dataset().items():
                (data_dir/(key+'.json')).write_text(json.dumps(value,ensure_ascii=False))
            with self.assertRaises(ValueError):
                build_deck(data_dir,root)
            self.assertFalse((root/'slides/chengdu/index.html').exists())

    def test_standalone_draft_embeds_real_images_and_fonts_without_runtime_fetches(self):
        from scripts.chengdu_slides import render as rendering
        standalone=getattr(rendering,'render_standalone',None)
        self.assertTrue(callable(standalone),'standalone exporter is not implemented')
        from scripts.chengdu_slides.model import load_dataset
        result=standalone(load_dataset(DATA_DIR),ROOT)
        import mimetypes
        data=load_dataset(DATA_DIR)
        mimes={mimetypes.guess_type(asset['path'])[0] for asset in data['assets'] if asset['kind']!='font'}
        for mime in mimes:
            self.assertIsNotNone(mime);assert mime is not None
            self.assertTrue('data:'+mime+';base64,' in result,'actual image MIME not embedded: '+mime)
        for required in ('data:font/woff2;base64,','DRAFT','font-license-notices','SIL OPEN FONT LICENSE','photo-license-notices'):
            self.assertTrue(required in result,'missing offline feature: '+required)
        for remaining in ('src="images/',"url('fonts/"):
            self.assertFalse(remaining in result,'unembedded runtime asset: '+remaining)

    def test_preview_cannot_write_into_public_slide_route(self):
        from scripts.chengdu_slides import render as rendering
        preview=getattr(rendering,'build_preview',None)
        self.assertTrue(callable(preview),'contained preview builder is not implemented')
        with self.assertRaises(ValueError):
            preview(DATA_DIR,ROOT,ROOT/'slides/chengdu')


if __name__=='__main__': unittest.main()
