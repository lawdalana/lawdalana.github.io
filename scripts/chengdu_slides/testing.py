"""Build a conspicuously synthetic, ignored navigation fixture for browser tests."""
import json
import shutil
import sys
from pathlib import Path
from .render import render_deck


def main():
    root=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(root/'tests/chengdu_slides'))
    from fixtures import sample_dataset
    data=sample_dataset();data['meta']['status']='research_incomplete'
    data['assets']=[{'id':'fixture-image','path':'slides/chengdu/images/fixture.svg',
                    'creator':'SYNTHETIC TEST FIXTURE','license':'CC0-1.0',
                    'license_url':'https://creativecommons.org/publicdomain/zero/1.0/',
                    'source_url':'https://example.invalid/SYNTHETIC','kind':'diagram'}]
    folder=root/'_reports/chengdu-slides/fixture'
    (folder/'images').mkdir(parents=True,exist_ok=True)
    (folder/'images/fixture.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900"><rect width="900" height="900" fill="#ddd"/><text x="40" y="100" font-size="40">SYNTHETIC TEST ONLY</text></svg>')
    shutil.copytree(root/'slides/chengdu/fonts',folder/'fonts',dirs_exist_ok=True)
    rendered=render_deck(data)
    (folder/'index.html').write_text(rendered,encoding='utf-8')
    print(json.dumps({'synthetic_fixture':True,'slides':rendered.count('<section class="slide"'),'publication_allowed':False}))


if __name__=='__main__':main()
