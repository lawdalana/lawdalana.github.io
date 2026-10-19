"""SYNTHETIC opinion evidence: qualifies attribution, never current market truth."""
from copy import deepcopy
from decimal import Decimal
import unittest
from fixtures import sample_dataset
from scripts.chengdu_slides.evidence import evaluate_gift
from scripts.chengdu_slides.validation import validate_dataset


def community_fixture():
    source={'id':'synthetic-community','url':'https://example.invalid/SYNTHETIC-COMMUNITY',
            'publisher':'SYNTHETIC DISCUSSION','tier':'community','retrieved_at':'2026-10-19',
            'published_at':'2024-02-03','access_state':'complete','review_state':'verified',
            'locator':'SYNTHETIC reply4','evidence_excerpt':'SYNTHETIC: worth considering a locally made seal',
            'retrieval_note':'SYNTHETIC TEST ONLY; not a real traveler comment',
            'supported_facts':['SYNTHETIC recommendation; not current stock evidence']}
    evidence={'route':'C','kind':'community_opinion_synthesis','selection':'conditional',
              'market_claim_status':'reported_not_verified',
              'rationale':{'th':'ความเห็นสมมติแนะนำงานทำเฉพาะชิ้น','zh-Hans':'虚构讨论建议考虑定制品'},
              'counterpoints':{'th':'อาจหาได้ในไทย ต้องเทียบคุณภาพจริง','zh-Hans':'泰国可能有售，须比较实物品质'},
              'disclosure':{'th':'สรุปความเห็น ไม่ใช่ยืนยันราคา สต็อก หรือการไม่มีขาย',
                            'zh-Hans':'意见汇总，不代表核实价格、现货或停售'},
              'observations':[{'source_id':source['id'],'locator':'SYNTHETIC reply4',
                               'excerpt':source['evidence_excerpt'],'stance':'recommend','published_at':'2024-02-03'}]}
    item={'id':'synthetic-seal','identity_key':'SYNTHETIC-SEAL','category':'gifts',
          'source_ids':[source['id']],'purchase_evidence':evidence}
    return item,{source['id']:source}


def community_dataset():
    data=sample_dataset();item,sources=community_fixture();gift=deepcopy(data['attractions'][0]);gift.update(item)
    gift['name']={'th':'ของฝากสมมติ','zh-Hans':'虚构礼品'}
    gift['details']={field:'SYNTHETIC' for field in ['product','buying_channel','price','authenticity','carriage','cautions']}
    gift['details']['observed_at']='2026-10-19'
    for unit in gift['units']:
        unit['id']='synthetic-gift-'+unit['kind'];unit['source_ids']=[item['source_ids'][0]]
    data['sources']+=list(sources.values());data['gifts']=[gift];data['meta']['gift_policy']='community_curated'
    return data


class CommunityEvidenceTests(unittest.TestCase):
    def test_observation_must_match_the_reviewed_source_scope(self):
        for access in ('complete','indexed_excerpt'):
            item,sources=community_fixture();sources['synthetic-community']['access_state']=access
            item['purchase_evidence']['observations'][0]['excerpt']='SYNTHETIC invented recommendation not present in reviewed text'
            with self.subTest(access=access):self.assertFalse(self.assess(item,sources)['qualified'])

    def test_locator_must_be_a_nonblank_string(self):
        for locator in ('   ',7,{'reply':4},['reply4']):
            item,sources=community_fixture();item['purchase_evidence']['observations'][0]['locator']=locator
            with self.subTest(locator=locator):self.assertFalse(self.assess(item,sources)['qualified'])

    def test_community_observations_cannot_disappear_from_visible_unit_citations(self):
        data=community_dataset()
        for unit in data['gifts'][0]['units']:unit['source_ids']=data['attractions'][0]['source_ids']
        self.assertIn('community-citation-scope',{error['code'] for error in validate_dataset(data)})

    def test_every_observed_countervoice_remains_cited_somewhere_in_the_gift(self):
        data=community_dataset();gift=data['gifts'][0];other=deepcopy(data['sources'][-1]);other['id']='synthetic-countervoice'
        data['sources'].append(other);gift['source_ids'].append(other['id'])
        observation=deepcopy(gift['purchase_evidence']['observations'][0]);observation.update(source_id=other['id'],stance='mixed')
        gift['purchase_evidence']['observations'].append(observation)
        self.assertIn('community-citation-scope',{error['code'] for error in validate_dataset(data)})
        gift['units'][-1]['source_ids'].append(other['id'])
        self.assertEqual(validate_dataset(data),[])

    def test_malformed_evidence_returns_findings_instead_of_crashing(self):
        for value in (None,False,[], 'SYNTHETIC malformed'):
            data=community_dataset();data['gifts'][0]['purchase_evidence']=value
            with self.subTest(value=value):self.assertIn('gift-evidence',{error['code'] for error in validate_dataset(data)})

    def assess(self,item,sources,**kwargs):
        try:return evaluate_gift(item,sources,Decimal('30'),policy='community_curated',**kwargs)
        except TypeError as exc:self.fail('community policy is not implemented: '+str(exc))

    def test_community_policy_qualifies_attributed_selection_not_market_truth(self):
        item,sources=community_fixture();result=self.assess(item,sources)
        self.assertTrue(result['qualified']);self.assertFalse(result['market_verified'])
        self.assertIsNone(result['saving_percent']);self.assertEqual(result['route'],'C')

    def test_community_does_not_silently_weaken_default_market_policy(self):
        item,sources=community_fixture()
        self.assertFalse(evaluate_gift(item,sources,Decimal('30'))['qualified'])

    def test_missing_observation_or_locator_cannot_be_replaced_by_qualified_flag(self):
        for field in ['observations','rationale','counterpoints','disclosure','market_claim_status']:
            item,sources=community_fixture();item['qualified']=True
            del item['purchase_evidence'][field]
            self.assertFalse(self.assess(item,sources)['qualified'])
        item,sources=community_fixture();del item['purchase_evidence']['observations'][0]['locator']
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_commercial_article_is_not_treated_as_a_community_voice(self):
        item,sources=community_fixture();sources['synthetic-community']['tier']='secondary'
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_indexed_excerpt_is_bounded_and_requires_explicit_access_note(self):
        item,sources=community_fixture();sources['synthetic-community']['access_state']='indexed_excerpt'
        self.assertTrue(self.assess(item,sources)['qualified'])
        del sources['synthetic-community']['retrieval_note']
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_bilingual_disclosure_is_required(self):
        item,sources=community_fixture();del item['purchase_evidence']['disclosure']['zh-Hans']
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_negative_only_voices_do_not_count_as_recommended_gifts(self):
        item,sources=community_fixture();item['purchase_evidence']['observations'][0]['stance']='avoid'
        self.assertFalse(self.assess(item,sources)['qualified'])
        item['purchase_evidence']['selection']='skip'
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_counter_voice_is_retained_without_becoming_a_universal_claim(self):
        item,sources=community_fixture();other=deepcopy(item['purchase_evidence']['observations'][0]);other['stance']='thai_available'
        item['purchase_evidence']['observations'].append(other)
        self.assertTrue(self.assess(item,sources)['qualified'])
        item['purchase_evidence']['guarantees_current_absence']=True
        self.assertFalse(self.assess(item,sources)['qualified'])

    def test_future_post_is_rejected_but_explicitly_unknown_date_is_not_invented(self):
        item,sources=community_fixture();item['purchase_evidence']['observations'][0]['published_at']='2099-01-01'
        self.assertFalse(self.assess(item,sources)['qualified'])
        item['purchase_evidence']['observations'][0]['published_at']=None
        self.assertTrue(self.assess(item,sources)['qualified'])

    def test_full_iso_comment_timestamp_is_preserved_not_truncated_to_fit_a_date(self):
        item,sources=community_fixture()
        original='2024-02-03T17:51:00+07:00'
        item['purchase_evidence']['observations'][0]['published_at']=original
        self.assertTrue(self.assess(item,sources)['qualified'])
        self.assertEqual(item['purchase_evidence']['observations'][0]['published_at'],original)

    def test_dataset_policy_opt_in_allows_observed_community_excerpts_only_for_gifts(self):
        data=sample_dataset();item,sources=community_fixture();gift=deepcopy(data['attractions'][0])
        gift.update(item);gift['name']={'th':'ของฝากสมมติ','zh-Hans':'虚构礼品'}
        gift['details']={field:'SYNTHETIC' for field in ['product','buying_channel','price','authenticity','carriage','cautions']};gift['details']['observed_at']='2026-10-19'
        for unit in gift['units']:
            unit['id']='synthetic-gift-'+unit['kind'];unit['source_ids']=[item['source_ids'][0]]
        data['sources']+=list(sources.values());data['gifts']=[gift]
        data['sources'][-1]['access_state']='indexed_excerpt';data['meta']['gift_policy']='community_curated'
        self.assertEqual(validate_dataset(data),[])
        data['meta'].pop('gift_policy')
        self.assertTrue(validate_dataset(data))
