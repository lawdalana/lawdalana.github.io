"""Fail-closed gift qualification. Synthetic fixtures live only in tests."""
from datetime import date, datetime
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


def sources_verified(ids, sources: dict[str, dict], *, allow_community_excerpt: bool = False) -> bool:
    if not isinstance(ids, list) or not ids:
        return False
    for source_id in ids:
        row = sources.get(source_id)
        if not isinstance(row, dict):
            return False
        parsed = urlparse(str(row.get('url', '')))
        observed = row.get('access_state') == 'complete'
        if allow_community_excerpt and row.get('tier') == 'community' and row.get('access_state') == 'indexed_excerpt':
            observed = all(isinstance(row.get(field),str) and row[field].strip()
                           for field in ('evidence_excerpt','locator','retrieval_note'))
        if (parsed.scheme not in ('http', 'https') or not parsed.hostname or
                row.get('review_state') != 'verified' or not observed or
                not valid_date(row.get('retrieved_at'))):
            return False
    return True


def _validate_community(item: dict, sources: dict[str, dict]) -> None:
    evidence=item['purchase_evidence']
    if (item.get('category')!='gifts' or evidence.get('kind')!='community_opinion_synthesis' or
            evidence.get('selection') not in ('buy_in_china','conditional') or
            evidence.get('market_claim_status')!='reported_not_verified'):
        raise ValueError('community curation needs a recommendation and explicit unverified-market status')
    for field in ('rationale','counterpoints','disclosure'):
        if any(not isinstance(evidence.get(field,{}).get(lang),str) or not evidence[field][lang].strip()
               for lang in ('th','zh-Hans')):
            raise ValueError('community curation requires bilingual '+field)
    if any(evidence.get(field) is True for field in ('guarantees_current_absence','guarantees_price_advantage')):
        raise ValueError('community opinions cannot guarantee live market absence or price advantage')
    observations=evidence.get('observations')
    if not isinstance(observations,list) or not observations:
        raise ValueError('community recommendation needs actual attributed observations')
    positive=False
    for observation in observations:
        if not isinstance(observation,dict):
            raise ValueError('community observation must be an object')
        source_id=observation.get('source_id')
        if not isinstance(source_id,str):
            raise ValueError('community source ID must be a string')
        row=sources.get(source_id,{})
        if (source_id not in item.get('source_ids',[]) or not isinstance(row,dict) or row.get('tier')!='community' or
                not sources_verified([source_id],sources,allow_community_excerpt=True) or
                not isinstance(observation.get('locator'),str) or not observation['locator'].strip() or
                not isinstance(observation.get('excerpt'),str) or
                not observation['excerpt'].strip() or 'published_at' not in observation):
            raise ValueError('missing observed community source, comment context or short excerpt')
        reviewed=row.get('reviewed_excerpts',[])
        reviewed=list(reviewed) if isinstance(reviewed,list) else []
        reviewed.append(row.get('evidence_excerpt'))
        excerpt=' '.join(observation['excerpt'].split())
        if not any(isinstance(text,str) and excerpt in ' '.join(text.split()) for text in reviewed):
            raise ValueError('community observation exceeds the reviewed source excerpt scope')
        published=observation['published_at']
        if published is not None and not valid_date(published):
            try:
                if datetime.fromisoformat(published).date()>date.today():
                    raise ValueError('future publication timestamp')
            except (TypeError,ValueError) as exc:
                raise ValueError('invalid/future community publication date or ISO timestamp') from exc
        if observation.get('stance') not in ('recommend','china_value','thai_available','avoid','mixed'):
            raise ValueError('unknown community stance')
        positive=positive or observation['stance'] in ('recommend','china_value')
    if not positive:
        raise ValueError('negative-only community comments do not qualify a recommended gift')


def evaluate_gift(item: dict, sources: dict[str, dict], minimum_saving: Decimal, *, policy: str = 'verified_market') -> dict:
    result = {'qualified': False, 'route': None, 'saving_percent': None, 'market_verified': False, 'reasons': []}
    try:
        if policy not in ('verified_market','community_curated'):
            raise ValueError('unsupported gift policy')
        evidence=item.get('purchase_evidence')
        if not isinstance(evidence,dict):
            raise ValueError('purchase evidence must be an object')
        if evidence.get('route')=='C':
            if policy!='community_curated':
                raise ValueError('community curation requires explicit dataset policy opt-in')
            _validate_community(item,sources)
            result.update(qualified=True,route='C',qualification_basis='community_curation')
            return result
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
        result.update(qualified=True, route=route, market_verified=True, qualification_basis='verified_market')
    except (KeyError, ValueError, TypeError, AttributeError, InvalidOperation) as exc:
        result['reasons'].append(str(exc))
    return result
