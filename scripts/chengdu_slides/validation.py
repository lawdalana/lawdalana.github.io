"""Validate factual completeness and bilingual contracts independently of rendering."""
from decimal import Decimal
from string import Formatter
from urllib.parse import urlparse
from .evidence import evaluate_gift, sources_verified, valid_date

CATEGORIES = ('attractions', 'restaurants', 'gifts')
DETAILS = {
    'attractions': ('location', 'highlights', 'transport', 'tickets', 'opening', 'duration', 'cautions', 'observed_at'),
    'restaurants': ('branch', 'address', 'specialties', 'budget', 'opening', 'transport', 'cautions', 'observed_at'),
    'gifts': ('product', 'buying_channel', 'price', 'authenticity', 'carriage', 'cautions', 'observed_at'),
}
LANGS = ('th', 'zh-Hans')


def _finding(code, path, message):
    return {'code': code, 'path': path, 'message': message}


def _tokens(lines):
    result = set()
    for line in lines:
        for _, name, spec, conversion in Formatter().parse(line):
            if name is not None:
                if not name.isidentifier() or spec or conversion:
                    raise ValueError('only plain named fact tokens are allowed')
                result.add(name)
    return result


def _validate(data, *, publication=False, only=None):
    errors = []
    policy=data.get('meta',{}).get('gift_policy','verified_market')
    community_policy=policy=='community_curated'
    categories = (only,) if only else CATEGORIES
    rows = data.get('sources', [])
    sources = {row['id']: row for row in rows if isinstance(row, dict) and isinstance(row.get('id'), str)}
    ids = [row.get('id') for row in rows if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        errors.append(_finding('duplicate-source', 'sources', 'source IDs must be unique'))
    for key, row in sources.items():
        if not key or not sources_verified([key], sources,allow_community_excerpt=community_policy):
            errors.append(_finding('source-review', f'sources/{key}', 'source must have a verified accessible dated observation'))
        if publication and urlparse(row.get('url', '')).hostname == 'example.invalid':
            errors.append(_finding('synthetic-source', f'sources/{key}', 'synthetic test sources cannot be published'))
    item_ids, identities, unit_ids = set(), set(), set()
    assets = {row.get('id') for row in data.get('assets', []) if isinstance(row, dict)}
    for category in categories:
        items = data.get(category, [])
        if not isinstance(items, list):
            errors.append(_finding('array', category, 'category must be an array'))
            continue
        if (publication or only) and len(items) < 15:
            errors.append(_finding('category-target', category, 'at least 15 distinct qualified entries required'))
        for index, item in enumerate(items):
            path = f'{category}/{index}'
            if not isinstance(item, dict):
                errors.append(_finding('item', path, 'item must be an object')); continue
            item_id, identity = item.get('id'), item.get('identity_key')
            if not item_id or item_id in item_ids or not identity or identity in identities:
                errors.append(_finding('identity', path, 'missing/duplicate item ID or identity'))
            item_ids.add(item_id); identities.add(identity)
            if item.get('category') != category:
                errors.append(_finding('category', path, 'category does not match file'))
            if publication and item.get('stage') != 'editorial_ready':
                errors.append(_finding('editorial-stage', path, 'discovery records cannot be published'))
            purchase_evidence=item.get('purchase_evidence')
            community_item=(community_policy and category=='gifts' and isinstance(purchase_evidence,dict)
                            and purchase_evidence.get('route')=='C')
            if not sources_verified(item.get('source_ids'), sources,allow_community_excerpt=community_item):
                errors.append(_finding('item-sources', path, 'relevant verified source references required'))
            for lang in LANGS:
                if not item.get('name', {}).get(lang):
                    errors.append(_finding('name-language', path, f'missing {lang} name'))
            details = item.get('details', {})
            for field in DETAILS[category]:
                if not details.get(field):
                    errors.append(_finding('practical-detail', path, f'missing {field}'))
            if not valid_date(details.get('observed_at')):
                errors.append(_finding('date', path, 'invalid/future observation date'))
            if category == 'gifts':
                eligibility = evaluate_gift(item, sources, Decimal('30'),policy=policy)
                if not eligibility['qualified']:
                    errors.append(_finding('gift-evidence', path, '; '.join(eligibility['reasons'])))
            units = item.get('units', [])
            if not isinstance(units, list) or not {'intro', 'details'} <= {u.get('kind') for u in units if isinstance(u, dict)}:
                errors.append(_finding('content-units', path, 'distinct intro and details content units required'))
                continue
            if community_item and isinstance(purchase_evidence,dict):
                observations=purchase_evidence.get('observations',[])
                observed_ids={row.get('source_id') for row in observations if isinstance(row,dict) and isinstance(row.get('source_id'),str)} if isinstance(observations,list) else set()
                cited_ids={identity for unit in units if isinstance(unit,dict) and isinstance(unit.get('source_ids'),list) for identity in unit['source_ids'] if isinstance(identity,str)}
                if not observed_ids<=cited_ids:
                    errors.append(_finding('community-citation-scope',path,'every qualifying observation and countervoice must remain visibly cited on the gift pages'))
            for unit in units:
                if not isinstance(unit, dict):
                    errors.append(_finding('unit', path, 'unit must be an object')); continue
                uid = unit.get('id')
                if not uid or uid in unit_ids:
                    errors.append(_finding('unit-id', path, 'missing/duplicate unit ID'))
                unit_ids.add(uid)
                bodies = unit.get('body', {})
                token_sets = []
                for lang in LANGS:
                    body = bodies.get(lang)
                    if (not unit.get('title', {}).get(lang) or not isinstance(body, list) or not body or
                            not all(isinstance(line, str) and line.strip() for line in body)):
                        errors.append(_finding('bilingual-content', path, f'missing/full {lang} text required'))
                        continue
                    try:
                        token_sets.append(_tokens(body))
                    except ValueError as exc:
                        errors.append(_finding('fact-token', path, str(exc)))
                facts = item.get('facts', {})
                if token_sets and (any(tokens != token_sets[0] for tokens in token_sets) or
                                   not token_sets[0] <= set(facts) or
                                   token_sets[0] != set(unit.get('fact_ids', []))):
                    errors.append(_finding('fact-parity', path, 'translations must share resolved canonical fact tokens'))
                if not sources_verified(unit.get('source_ids'), sources,allow_community_excerpt=community_item):
                    errors.append(_finding('unit-source', path, 'unit needs relevant source references'))
                if publication and (unit.get('asset_id') not in assets or
                                    any(not unit.get('alt', {}).get(lang) for lang in LANGS)):
                    errors.append(_finding('visual', path, 'meaningful asset and bilingual alternative text required'))
    if publication and not only and not data.get('support'):
        errors.append(_finding('support', 'support', 'paired supporting content required'))
    if not only:
        from .pagination import validate_pagination
        errors.extend(validate_pagination(data))
    return errors


def validate_category(data: dict, category: str) -> list[dict]:
    if category not in CATEGORIES:
        raise ValueError(f'unknown category: {category}')
    return _validate(data, only=category)


def validate_dataset(data: dict, *, publication: bool = False) -> list[dict]:
    return _validate(data, publication=publication)
