"""Asset provenance and containment checks; actual image decode is a browser gate."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
import hashlib
import math
import re
from .evidence import valid_date


def _photo_license(name, url):
    if not isinstance(name,str) or not isinstance(url,str):return False
    parsed=urlparse(url)
    if parsed.scheme!='https' or parsed.hostname!='creativecommons.org':return False
    if name in ('Public domain','CC0','CC0 1.0','CC0-1.0'):
        return parsed.path.startswith(('/publicdomain/mark/1.0/','/publicdomain/zero/1.0/'))
    match=re.fullmatch(r'CC (BY(?:-SA)?) ([1-4]\.\d)(?: [a-z-]+)?',name)
    if not match or match[2] not in ('1.0','2.0','2.5','3.0','4.0'):return False
    base='/licenses/'+match[1].lower()+'/'+match[2]
    return parsed.path==base or parsed.path.startswith(base+'/')


def validate_assets(data: dict, site_root: Path) -> list[dict]:
    errors = []
    photographs=data.get('meta',{}).get('visual_policy')=='licensed_photography'
    assets = {}
    root = site_root.resolve()
    def issue(path, message):
        errors.append({'code': 'asset', 'path': path, 'message': message})
    for row in data.get('assets', []):
        aid = row.get('id')
        if not aid or aid in assets:
            issue(str(aid), 'missing or duplicate asset ID')
        assets[aid] = row
        kind = row.get('kind')
        if photographs and kind not in ('photo','font'):
            issue(str(aid),'the photographic edition requires actual photos, not the old diagrams')
        if kind not in ('photo', 'diagram', 'font'):
            issue(str(aid), 'only meaningful photos/diagrams and licensed fonts are supported')
        for field in ('path', 'creator', 'license', 'license_url', 'source_url', 'modifications'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                issue(str(aid), f'missing {field}')
        raw = row.get('path', '')
        path = PurePosixPath(raw)
        folder = 'fonts' if kind == 'font' else 'images'
        expected = root / 'slides' / 'chengdu' / folder
        resolved = (root / raw).resolve()
        if (urlparse(raw).scheme or path.is_absolute() or '..' in path.parts or
                not resolved.is_relative_to(expected) or not resolved.is_file()):
            issue(str(aid), 'asset path must resolve to an existing file inside the deck asset folder')
        for field in ('license_url', 'source_url'):
            parsed = urlparse(row.get(field, ''))
            if parsed.scheme not in ('http', 'https') or not parsed.hostname:
                issue(str(aid), f'{field} requires a provenance URL')
        if kind in ('font','photo'):
            notice = row.get('license_path','')
            notice_path = (root / notice).resolve() if isinstance(notice,str) else root
            if not notice or not notice_path.is_relative_to(expected) or not notice_path.is_file() or notice_path.stat().st_size == 0:
                issue(str(aid), 'asset needs a nonempty contained local license notice')
        if kind=='photo':
            if (row.get('license_checked') is not True or row.get('photo_review')!='approved' or
                    not _photo_license(row.get('license',''),row.get('license_url',''))):
                issue(str(aid),'photo needs reviewed attribution and an explicit CC BY/BY-SA/CC0/public-domain license')
            if not valid_date(row.get('retrieved_at')):
                issue(str(aid),'photo provenance needs its actual retrieval date')
            if (not isinstance(row.get('sha256'),str) or not resolved.is_relative_to(expected) or not resolved.is_file() or
                    row['sha256']!=hashlib.sha256(resolved.read_bytes()).hexdigest()):
                issue(str(aid),'photo bytes must match the reviewed source derivative')
            if path.suffix.lower() not in ('.jpg','.jpeg','.png','.webp'):
                issue(str(aid),'photographic edition needs a decoded bitmap, not an SVG drawing')
            scope=row.get('depiction_scope')
            if scope not in ('exact_place','dish_example','product_example','cultural_context','ingredient_context'):
                issue(str(aid),'photo subject scope must be explicit')
            if scope!='exact_place' and (row.get('illustrative') is not True or any(not row.get('disclosure',{}).get(lang) for lang in ('th','zh-Hans'))):
                issue(str(aid),'example dishes/products/context must not imply actual restaurant plates or current shop stock')
            focal=row.get('focal_point',[50,50])
            if not isinstance(focal,list) or len(focal)!=2 or any(type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=100 for value in focal):
                issue(str(aid),'photo focal point must be two finite percentages within its image bounds')
        if kind != 'font':
            if row.get('meaningful') is not True:
                issue(str(aid), 'decorative-only image does not satisfy slide visual requirement')
            if any(not isinstance(row.get(dim), (int, float)) or row[dim] < 256 for dim in ('width', 'height')):
                issue(str(aid), 'subject visual is missing dimensions or is too small')
            if not row.get('subject'):
                issue(str(aid), 'visual subject must be documented')
            if row.get('illustrative') and any(not row.get('disclosure', {}).get(lang) for lang in ('th', 'zh-Hans')):
                issue(str(aid), 'generic illustrative photo requires disclosure in both languages')
    units = list(data.get('support', []))
    for category in ('attractions', 'restaurants', 'gifts'):
        for item in data.get(category, []):
            units.extend(item.get('units', []))
    for unit in units:
        row = assets.get(unit.get('asset_id'))
        if row is None or row.get('kind') == 'font':
            issue(unit.get('id', 'unknown-unit'), 'every content unit needs a meaningful local subject visual')
    return errors
