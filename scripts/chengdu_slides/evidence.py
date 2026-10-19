"""Fail-closed gift qualification. Synthetic fixtures live only in tests."""
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse


def valid_date(value) -> bool:
    try:
        return isinstance(value, str) and date.fromisoformat(value) <= date.today()
    except ValueError:
        return False


def money(value: str, *, allow_zero: bool = False) -> Decimal:
    try:
        if not isinstance(value, str) or not value.strip():
            raise ValueError('money must be an explicit decimal string')
        result = Decimal(value)
        if not result.is_finite() or result < 0 or (not allow_zero and result == 0):
            raise ValueError('money/rate must be finite and positive; fees may be zero')
        return result
    except (InvalidOperation, TypeError) as exc:
        raise ValueError('invalid decimal money/rate') from exc


def calculate_saving(china_cny: str, thb_per_cny: str, thai_thb: str, *,
                     china_fees_thb: str = '0', thai_delivery_thb: str = '0') -> Decimal:
    china_cost = money(china_cny) * money(thb_per_cny) + money(china_fees_thb, allow_zero=True)
    thai_cost = money(thai_thb) + money(thai_delivery_thb, allow_zero=True)
    return (thai_cost - china_cost) / thai_cost * Decimal('100')


def sources_verified(ids, sources: dict[str, dict]) -> bool:
    if not isinstance(ids, list) or not ids:
        return False
    for source_id in ids:
        row = sources.get(source_id)
        if not isinstance(row, dict):
            return False
        parsed = urlparse(str(row.get('url', '')))
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname or
                row.get('review_state') != 'verified' or row.get('access_state') != 'complete' or
                not valid_date(row.get('retrieved_at'))):
            return False
    return True


def evaluate_gift(item: dict, sources: dict[str, dict], minimum_saving: Decimal) -> dict:
    result = {'qualified': False, 'route': None, 'saving_percent': None, 'reasons': []}
    try:
        if not minimum_saving.is_finite() or minimum_saving < 0 or minimum_saving > 100:
            raise ValueError('invalid saving threshold')
        availability = item['availability']
        if (availability.get('verified') is not True or availability.get('accessible') is not True or
                availability.get('pickup_closed') is not False or
                not sources_verified(availability.get('source_ids'), sources)):
            raise ValueError('China purchase channel/availability has not been verified accessible')
        evidence = item['purchase_evidence']
        route = evidence.get('route')
        if route == 'E':
            if (not evidence.get('exact_product') or
                    evidence['exact_product'] != item.get('identity_key') or
                    evidence.get('wording') != 'not_found_in_checked_searches'):
                raise ValueError('absence claim needs exact identity and bounded wording')
            searches = evidence.get('searches')
            if not isinstance(searches, list) or not searches:
                raise ValueError('no actual search observations')
            for search in searches:
                parsed = urlparse(search.get('url', ''))
                if (search.get('access_state') != 'complete' or
                        search.get('exact_match_found') is not False or
                        parsed.scheme != 'https' or parsed.hostname != 'shopee.co.th' or
                        not search.get('query_terms') or not search.get('scope') or
                        not valid_date(search.get('observed_at')) or
                        not sources_verified(search.get('source_ids'), sources)):
                    raise ValueError('incomplete, blocked, matching, or unsourced Shopee observation')
        elif route == 'P':
            china, thai, rate = evidence['china_offer'], evidence['thai_offer'], evidence['currency_rate']
            for field in ('sku', 'size', 'grade', 'quantity', 'edition'):
                if not china.get(field) or china[field] != thai.get(field):
                    raise ValueError(f'not like-for-like: {field}')
            for offer in (china, thai):
                if (offer.get('authentic') is not True or offer.get('stock') != 'available' or
                        not valid_date(offer.get('observed_at')) or
                        not sources_verified(offer.get('source_ids'), sources)):
                    raise ValueError('offer lacks verified authenticity, stock, date, or source')
            if (not valid_date(rate.get('observed_at')) or
                    not sources_verified(rate.get('source_ids'), sources) or
                    not evidence.get('exclusions')):
                raise ValueError('rate/date/cost exclusions not evidenced')
            saving = calculate_saving(china['price_cny'], rate['thb_per_cny'], thai['price_thb'],
                                      china_fees_thb=evidence['china_fees_thb'],
                                      thai_delivery_thb=evidence['thai_delivery_thb'])
            result['saving_percent'] = saving
            if saving < minimum_saving:
                raise ValueError('documented saving is below the threshold')
        else:
            raise ValueError('no supported purchase-evidence route')
        result.update(qualified=True, route=route)
    except (KeyError, ValueError, TypeError, AttributeError, InvalidOperation) as exc:
        result['reasons'].append(str(exc))
    return result
