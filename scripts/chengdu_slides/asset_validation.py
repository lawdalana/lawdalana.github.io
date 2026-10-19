"""Asset provenance and containment checks; actual image decode is a browser gate."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


def validate_assets(data: dict, site_root: Path) -> list[dict]:
    errors = []
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
        if kind == 'font':
            notice = row.get('license_path','')
            notice_path = (root / notice).resolve() if isinstance(notice,str) else root
            if not notice or not notice_path.is_relative_to(expected) or not notice_path.is_file() or notice_path.stat().st_size == 0:
                issue(str(aid), 'font needs a nonempty local license notice inside the font folder')
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
