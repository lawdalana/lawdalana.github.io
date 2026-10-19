"""Explicitly SYNTHETIC unit-test records. Never publish as travel evidence."""
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / '_data' / 'chengdu_slides'


def sample_sources():
    return {'fixture-source': {'id': 'fixture-source', 'url': 'https://example.invalid/SYNTHETIC',
            'publisher': 'SYNTHETIC TEST FIXTURE', 'tier': 'official',
            'retrieved_at': '2026-10-19', 'access_state': 'complete',
            'review_state': 'verified', 'supported_facts': ['SYNTHETIC ONLY']}}


def sample_price_evidence():
    identity = {'sku': 'SYNTHETIC-1', 'size': '100g', 'grade': 'A',
                'quantity': 1, 'edition': 'standard', 'authentic': True,
                'stock': 'available', 'observed_at': '2026-10-19',
                'source_ids': ['fixture-source']}
    item = {'id': 'fixture-gift', 'identity_key': 'SYNTHETIC-1', 'category': 'gifts',
        'availability': {'verified': True, 'accessible': True, 'pickup_closed': False,
                         'source_ids': ['fixture-source']},
        'purchase_evidence': {'route': 'P',
            'china_offer': dict(identity, price_cny='70'),
            'thai_offer': dict(identity, price_thb='500'),
            'currency_rate': {'thb_per_cny': '5', 'observed_at': '2026-10-19',
                              'source_ids': ['fixture-source']},
            'china_fees_thb': '0', 'thai_delivery_thb': '0',
            'exclusions': 'SYNTHETIC: travel costs excluded'}}
    return item, sample_sources()


def sample_absence_evidence():
    item, sources = sample_price_evidence()
    item['purchase_evidence'] = {'route': 'E', 'exact_product': 'SYNTHETIC-1',
        'wording': 'not_found_in_checked_searches', 'searches': [{
            'url': 'https://shopee.co.th/search?keyword=SYNTHETIC-1',
            'query_terms': ['SYNTHETIC-1'], 'observed_at': '2026-10-19',
            'scope': 'SYNTHETIC: first result page', 'access_state': 'complete',
            'exact_match_found': False, 'source_ids': ['fixture-source']}]}
    return item, sources


def sample_dataset():
    unit = {'id': 'fixture-intro', 'kind': 'intro',
        'title': {'th': 'ข้อมูลทดสอบ', 'zh-Hans': '测试数据'},
        'body': {'th': ['ราคา {price}'], 'zh-Hans': ['价格 {price}']},
        'fact_ids': ['price'], 'source_ids': ['fixture-source'],
        'asset_id': 'fixture-image', 'alt': {'th': 'ภาพทดสอบ', 'zh-Hans': '测试图片'}}
    item = {'id': 'fixture-attraction', 'identity_key': 'SYNTHETIC-ATTRACTION',
        'name': {'th': 'สถานที่สมมติ', 'zh-Hans': '虚构景点'}, 'category': 'attractions',
        'stage': 'editorial_ready', 'source_ids': ['fixture-source'],
        'facts': {'price': '50 CNY'}, 'details': {
            'location': 'SYNTHETIC', 'highlights': 'SYNTHETIC', 'transport': 'SYNTHETIC',
            'tickets': 'SYNTHETIC', 'opening': 'SYNTHETIC', 'duration': 'editorial estimate',
            'cautions': 'SYNTHETIC', 'observed_at': '2026-10-19'},
        'units': [unit, dict(deepcopy(unit), id='fixture-details', kind='details')]}
    return {'meta': {'target_per_category': 15, 'minimum_saving_percent': '30'},
        'sources': list(sample_sources().values()), 'assets': [], 'attractions': [item],
        'restaurants': [], 'gifts': [], 'support': []}
