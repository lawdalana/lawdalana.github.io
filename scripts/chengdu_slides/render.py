"""Deterministic paired HTML renderer; release builds reject incomplete evidence."""
import hashlib
import html
import json
import base64
import mimetypes
import re
from pathlib import Path
from urllib.parse import urlparse
from .model import load_dataset
from .validation import validate_dataset
from .asset_validation import validate_assets
from .pagination import ordered_entries, unit_pages, validate_pagination

ROOT = Path(__file__).resolve().parents[2]
LANGS = ('th', 'zh-Hans')


def _e(value):
    return html.escape(str(value), quote=True)


def _safe_url(value):
    return value if urlparse(value).scheme in ('http', 'https') else '#'


def _source_link(source: dict, lang: str) -> str:
    label=source.get('publisher',source.get('id','source'))
    if source.get('citation_number'):
        label='['+str(source['citation_number'])+'] '+label
    if source.get('tier')=='community':
        label+=' · '+str(source.get('published_at') or ('ไม่ทราบวันโพสต์' if lang=='th' else '发布日期不详'))
        if source.get('access_state')=='indexed_excerpt':label+=' · '+('ข้อความบางส่วน' if lang=='th' else '节选')
    return '<a target="_blank" rel="noopener noreferrer" href="'+_e(_safe_url(source['url']))+'">'+_e(label)+'</a>'


def _reference_links(ids: list, sources: dict, lang: str) -> str:
    groups={}
    for identity in ids:
        if identity not in sources:continue
        source=sources[identity]
        key=('community',identity) if source.get('tier')=='community' else ('publisher',source.get('publisher',identity))
        groups.setdefault(key,[]).append(source)
    parts=[]
    for key,rows in groups.items():
        if key[0]=='community' or len(rows)==1:
            parts.append(_source_link(rows[0],lang));continue
        by_url={}
        for row in rows:by_url.setdefault(row['url'],[]).append(row)
        links=[]
        for url,aliases in by_url.items():
            citations=', '.join(str(row.get('citation_number') or row['id']) for row in aliases)
            title=' / '.join(dict.fromkeys(row.get('title',row['id']) for row in aliases))
            links.append('<a target="_blank" rel="noopener noreferrer" href="'+_e(_safe_url(url))+'" title="'+_e(title)+'">['+_e(citations)+']</a>')
        parts.append('<span class="reference-group">'+_e(key[1])+' '+' '.join(links)+'</span>')
    return ' · '.join(parts)


def content_version(data: dict) -> str:
    digest = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode())
    for relative in ('scripts/chengdu_slides/render.py', 'scripts/chengdu_slides/pagination.py', 'scripts/chengdu_slides/viewport-base.css'):
        template = ROOT / relative
        if template.is_file(): digest.update(template.read_bytes())
    for name in ('deck.css', 'deck.js'):
        path = ROOT / 'slides/chengdu' / name
        if path.exists(): digest.update(path.read_bytes())
    for asset in sorted(data.get('assets', []), key=lambda a: a.get('id', '')):
        path = ROOT / asset.get('path', '_missing_asset')
        if path.is_file(): digest.update(path.read_bytes())
        notice=ROOT/asset.get('license_path','_missing_license')
        if asset.get('license_path') and notice.is_file():digest.update(notice.read_bytes())
    return digest.hexdigest()[:16]


def render_deck(data: dict, *, measure: bool = False) -> str:
    if not measure:
        findings=validate_pagination(data)
        if findings:raise ValueError(json.dumps(findings,ensure_ascii=False))
    sources = {row['id']: row for row in data.get('sources', [])}
    assets = {row['id']: row for row in data.get('assets', [])}
    entries = ordered_entries(data)
    sections, options = [], []
    numbers={lang:0 for lang in LANGS}
    draft = data.get('meta', {}).get('status') != 'published'
    version = content_version(data)
    for item, unit in entries:
        asset = assets.get(unit.get('asset_id'), {})
        photo=asset.get('kind')=='photo'
        layout=('chapter' if unit.get('kind') in ('photo-chapter','photo-cover') else 'details' if unit.get('kind')=='details' else 'feature') if photo else 'standard'
        slide_class='slide photo-slide layout-'+layout if photo else 'slide'
        focal=asset.get('focal_point',[50,50])
        if not isinstance(focal,list) or len(focal)!=2 or any(type(value) not in (int,float) or not 0<=value<=100 for value in focal):focal=[50,50]
        image_style='object-position:'+format(focal[0],'g')+'% '+format(focal[1],'g')+'%'
        asset_path = asset.get('path', '')
        if asset_path.startswith('slides/chengdu/'):
            asset_path = asset_path[len('slides/chengdu/'):]
        facts = item.get('facts', {}) if item else unit.get('facts', {})
        category = item.get('category', 'guide') if item else 'guide'
        community_evidence=item.get('purchase_evidence',{}) if item else {}
        community=community_evidence.get('route')=='C'
        pair = unit['id']
        primary_start=numbers['th']+1
        for page in unit_pages(unit):
            lang=page['lang']; sid=page['id']; numbers[lang]+=1
            title = unit.get('title', {}).get(lang, '')
            bullets = ''.join('<li>' + _e(text.format_map(facts)) + '</li>' for text in page['body'])
            refs = _reference_links(unit.get('source_ids',[]),sources,lang)
            opinion_label=community_evidence['disclosure'][lang] if community else unit.get('opinion_disclosure',{}).get(lang,'')
            opinion_note='<div class="evidence-mark" role="note">'+_e(opinion_label)+'</div>' if opinion_label else ''
            route_attribute=' data-evidence-route="C"' if community else ''
            credit = _e(asset.get('attribution') or asset.get('creator', ''))
            license_name = _e(asset.get('license', ''))
            credit_link = _e(_safe_url(asset.get('source_url', '')))
            license_link = _e(_safe_url(asset.get('license_url', '')))
            disclosure = asset.get('disclosure', {}).get(lang, '') if asset.get('illustrative') else ''
            caption = _e(disclosure or asset.get('caption', {}).get(lang, ''))
            continuation=page['continuation']
            continuation_label=('<span class="continuation">'+_e(str(continuation['part'])+' / '+str(continuation['total']))+'</span>') if continuation else ''
            photo_modification='<span class="photo-modification">'+('ปรับขนาด/ครอป/โทนสีจากต้นฉบับ' if lang=='th' else '原图已缩放／裁切及轻调色。')+'</span>' if photo else ''
            item_name = item.get('name', {}).get(lang, '') if item else 'CHENGDU · 成都'
            warning = '<span class="draft-mark">DRAFT · ยังไม่ผ่านเกณฑ์เผยแพร่ / 尚未达到发布标准</span>' if draft else ''
            aliases=[identity+'--'+lang for identity in unit.get('legacy_ids',[])] if page['part']==1 else []
            sections.append(f'''<section class="{slide_class}" id="{_e(sid)}" lang="{lang}" data-slide-id="{_e(sid)}" data-pair-id="{_e(pair)}" data-lang="{lang}" data-page-part="{page['part']}" data-page-total="{page['total']}" data-primary-page="{primary_start+page['primary']}" data-legacy-ids="{_e(json.dumps(aliases))}" data-layout="{layout}" data-visual-kind="{_e(asset.get('kind',''))}" data-item-id="{_e(item.get('id','') if item else '')}" data-kind="{_e(unit.get('kind','guide'))}" data-fact-ids="{_e(json.dumps(unit.get('fact_ids', [])))}" data-source-ids="{_e(json.dumps(unit.get('source_ids', [])))}"{route_attribute} aria-labelledby="title-{_e(sid)}">
<div class="folio"><span class="seal">蜀</span><a class="site-return" href="https://lawdalana.github.io/" aria-label="กลับหน้าเว็บ / 返回网站首页">CHENGDU FIELD NOTES</a><span>{_e(category.upper())} · {'ไทย' if lang=='th' else '中文'}</span></div>
<div class="spread"><figure class="visual"><img src="{_e(asset_path)}" style="{image_style}" alt="{_e(unit.get('alt',{}).get(lang,''))}" loading="lazy" decoding="async"><figcaption>{caption}<span><a href="{credit_link}" title="{_e(asset.get('source_title',''))}" target="_blank" rel="noopener noreferrer">{credit}</a> · <a href="{license_link}" target="_blank" rel="noopener noreferrer">{license_name}</a></span>{photo_modification}</figcaption></figure>
<article class="copy"><div class="eyebrow">{_e(item_name)}{continuation_label}</div>{opinion_note}<h2 id="title-{_e(sid)}">{_e(title)}</h2><div class="rule"></div><ul>{bullets}</ul></article></div>
<footer>{warning}<span class="references">{refs}</span><span class="page-no">{numbers[lang]:03d}</span></footer></section>''')
            label=(item_name+' · ' if item else '')+title
            if page['total']>1:label+=' · '+str(page['part'])+'/'+str(page['total'])
            options.append('<option value="' + _e(sid) + '">' + _e(f'{numbers[lang]:03d} · {label} · {lang}') + '</option>')
    styles_path = ROOT / 'slides/chengdu/deck.css'
    script_path = ROOT / 'slides/chengdu/deck.js'
    styles = (ROOT / 'scripts/chengdu_slides/viewport-base.css').read_text()
    styles += '\n' + (styles_path.read_text() if styles_path.exists() else '')
    script = script_path.read_text() if script_path.exists() else ''
    reading_tail=styles.partition('/* === READING VIEW:')[2]
    reading_fallback=('/* === READING VIEW:'+reading_tail).replace('html.reading','html').replace('.reading ','') if reading_tail else ''
    title = data.get('meta', {}).get('title', {}).get('th', 'Chengdu · 成都')
    return f'''<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="content-version" content="{version}"><title>{_e(title)}</title><style>{styles}</style></head><body>
<div class="deck-viewport"><main class="deck-stage" id="deckStage">{''.join(sections)}</main></div>
<nav class="deck-controls" id="deckControls" aria-label="Slide navigation"><button type="button" id="prev" aria-label="Previous slide">←</button><output id="progress" aria-live="polite"></output><button type="button" id="next" aria-label="Next slide">→</button><button type="button" id="pair">ไทย / 中文</button><select id="contents" aria-label="สารบัญ / 目录">{''.join(options)}</select><button type="button" id="read">อ่าน / 阅读</button><button type="button" id="fullscreen" aria-label="Full screen">⛶</button></nav>
<button type="button" id="toolbar" class="reading-toolbar-toggle" aria-controls="deckControls" aria-expanded="true" aria-label="แถบควบคุม / 控制栏">☰</button>
<noscript><style>{reading_fallback}.deck-controls,.reading-toolbar-toggle{{display:none!important}}</style><p>JavaScript ปิดอยู่: อ่านสไลด์ตามลำดับด้านล่าง / JavaScript 已关闭，可依次阅读。</p></noscript>
<script>{script}</script></body></html>'''


def build_deck(data_dir: Path, site_root: Path) -> dict:
    data = load_dataset(data_dir)
    findings = validate_dataset(data, publication=True) + validate_assets(data, site_root)
    if findings:
        raise ValueError(json.dumps(findings, ensure_ascii=False))
    if data.get('meta', {}).get('status') != 'published':
        raise ValueError('publication status is not approved')
    target = site_root / 'slides/chengdu'
    target.mkdir(parents=True, exist_ok=True)
    rendered = render_deck(data)
    manifest = {'content_version': content_version(data),
        'counts': {key: len(data[key]) for key in ('attractions', 'restaurants', 'gifts')},
        'slides': rendered.count('<section class="slide'),
        'language_pages':{lang:rendered.count('data-lang="'+lang+'"') for lang in LANGS},
        'topics':len(ordered_entries(data)),
        'pagination_policy':data.get('meta',{}).get('pagination_policy','paired')}
    (target/'index.html').write_text(rendered, encoding='utf-8')
    (target/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest


def render_standalone(data: dict, site_root: Path, *, publication: bool = False) -> str:
    """Embed local visual/font bytes; release mode still enforces all publication gates."""
    import copy
    draft=copy.deepcopy(data)
    findings=validate_assets(draft,site_root)
    if publication:
        findings+=validate_dataset(draft,publication=True)
        if draft.get('meta',{}).get('status')!='published':
            findings.append({'code':'publication-status','path':'meta/status','message':'publication status is not approved'})
    else:
        draft['meta']['status']='research_incomplete'
    if findings:raise ValueError(json.dumps(findings,ensure_ascii=False))
    result=render_deck(draft)
    embedded={}
    for asset in draft.get('assets',[]):
        relative=str(Path(asset['path']).relative_to('slides/chengdu'))
        mime='font/woff2' if relative.endswith('.woff2') else mimetypes.guess_type(relative)[0]
        if not mime:raise ValueError('unknown asset MIME type: '+relative)
        uri='data:'+mime+';base64,'+base64.b64encode((site_root/asset['path']).read_bytes()).decode('ascii')
        embedded[_e(relative)]=uri
    def inline(match):
        path=match.group(1) or match.group(2)
        if path not in embedded:return match.group(0)
        return 'src="'+embedded[path]+'"' if match.group(1) is not None else "url('"+embedded[path]+"')"
    result=re.sub(r'''src="([^"]+)"|url\('([^']+)'\)''',inline,result)
    notices=[{'font':asset['id'],'license':asset['license'],'source_url':asset['source_url'],
              'copyright_and_license_notice':(site_root/asset['license_path']).read_text(encoding='utf-8')}
             for asset in draft.get('assets',[]) if asset.get('kind')=='font']
    payload=json.dumps(notices,ensure_ascii=False).replace('<','\\u003c')
    result=result.replace('</head>','<script type="application/json" id="font-license-notices">'+payload+'</script></head>')
    photo_notices={asset['license_path']:(site_root/asset['license_path']).read_text(encoding='utf-8')
                   for asset in draft.get('assets',[]) if asset.get('kind')=='photo'}
    photo_payload=json.dumps(photo_notices,ensure_ascii=False).replace('<',r'\u003c')
    result=result.replace('</head>','<script type="application/json" id="photo-license-notices">'+photo_payload+'</script></head>')
    return result


def build_preview(data_dir: Path, site_root: Path, output_dir: Path) -> dict:
    """Produce an explicitly incomplete local preview, never in a public route."""
    import shutil
    allowed = (site_root / '_reports').resolve()
    output = output_dir.resolve()
    if not output.is_relative_to(allowed):
        raise ValueError('draft preview output must be inside the ignored _reports directory')
    data = load_dataset(data_dir)
    data['meta']['status'] = 'research_incomplete'
    if not any(data.get(key) for key in ('support','attractions','restaurants','gifts')):
        raise ValueError('no actual content to preview')
    findings = validate_dataset(data, publication=False) + validate_assets(data, site_root)
    if findings:
        raise ValueError(json.dumps(findings,ensure_ascii=False))
    output.mkdir(parents=True,exist_ok=True)
    for asset in data.get('assets',[]):
        relative=Path(asset['path']).relative_to('slides/chengdu')
        destination=output/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(site_root/asset['path'],destination)
    for notice in {asset['license_path'] for asset in data.get('assets',[]) if asset.get('license_path')}:
        destination=output/Path(notice).relative_to('slides/chengdu')
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(site_root/notice,destination)
    for license_file in (site_root/'slides/chengdu/fonts').glob('*_OFL.txt'):
        destination=output/'fonts'/license_file.name
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(license_file,destination)
    rendered=render_deck(data)
    manifest={'preview':True,'status':'research_incomplete','content_version':content_version(data),
              'counts':{key:len(data.get(key,[])) for key in ('attractions','restaurants','gifts')},
              'slides':rendered.count('<section class="slide'),
              'language_pages':{lang:rendered.count('data-lang="'+lang+'"') for lang in LANGS},
              'topics':len(ordered_entries(data)),
              'release_findings':validate_dataset(data,publication=True)}
    (output/'index.html').write_text(rendered,encoding='utf-8')
    (output/'Chengdu_Thai_Chinese_Draft.html').write_text(render_standalone(data,site_root),encoding='utf-8')
    (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest
