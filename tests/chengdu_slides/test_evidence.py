"""Guards against false qualification and incorrect price arithmetic."""
import unittest
from copy import deepcopy
from decimal import Decimal
from fixtures import sample_absence_evidence, sample_price_evidence

try:
    from scripts.chengdu_slides.evidence import calculate_saving, evaluate_gift
except ImportError:
    calculate_saving = evaluate_gift = None


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(calculate_saving), 'calculate_saving is not implemented')
        self.assertTrue(callable(evaluate_gift), 'evaluate_gift is not implemented')

    def test_price_threshold_uses_unrounded_decimal(self):
        self.assertEqual(calculate_saving('70', '5', '500'), Decimal('30'))
        self.assertLess(calculate_saving('70.001', '5', '500'), Decimal('30'))

    def test_documented_fees_change_saving(self):
        self.assertEqual(calculate_saving('70', '5', '500', china_fees_thb='50'), Decimal('20'))
        self.assertEqual(calculate_saving('100', '5', '500'), Decimal('0'))

    def test_nonpositive_or_nonfinite_money_is_rejected(self):
        for value in ['0', '-1', 'NaN', 'Infinity', '-Infinity', 'not-money', '']:
            for position in range(3):
                args = ['70', '5', '500']; args[position] = value
                with self.subTest(value=value, position=position), self.assertRaises(ValueError):
                    calculate_saving(*args)

    def test_invalid_fees_are_rejected(self):
        for value in ['-1', 'NaN', 'Infinity', '']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                calculate_saving('70', '5', '500', china_fees_thb=value)

    def test_price_route_applies_threshold_after_costs_unrounded(self):
        item, sources = sample_price_evidence()
        self.assertTrue(evaluate_gift(item, sources, Decimal('30'))['qualified'])
        item['purchase_evidence']['china_offer']['price_cny'] = '70.001'
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])
        item['purchase_evidence']['china_offer']['price_cny'] = '70'
        item['purchase_evidence']['china_fees_thb'] = '1'
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_mismatched_product_identity_is_rejected(self):
        for key, different in [('sku', 'OTHER'), ('size', '200g'), ('grade', 'B'),
                               ('edition', 'regional-other'), ('quantity', 2)]:
            item, sources = sample_price_evidence()
            item['purchase_evidence']['thai_offer'][key] = different
            with self.subTest(key=key):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_blocked_search_never_qualifies(self):
        item, sources = sample_absence_evidence()
        self.assertTrue(evaluate_gift(item, sources, Decimal('30'))['qualified'])
        item['purchase_evidence']['searches'][0]['access_state'] = 'blocked'
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_missing_or_positive_match_search_never_qualifies(self):
        for field in ['url', 'query_terms', 'observed_at', 'scope', 'source_ids']:
            item, sources = sample_absence_evidence()
            del item['purchase_evidence']['searches'][0][field]
            with self.subTest(field=field):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])
        item, sources = sample_absence_evidence()
        item['purchase_evidence']['searches'][0]['exact_match_found'] = True
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_closed_pickup_without_verified_alternative_is_rejected(self):
        item, sources = sample_price_evidence()
        item['availability']['pickup_closed'] = True
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_unknown_stock_or_channel_is_rejected(self):
        for mutate in ['stock', 'accessible', 'verified', 'authentic']:
            item, sources = sample_price_evidence()
            if mutate in ['accessible', 'verified']:
                item['availability'][mutate] = False
            elif mutate == 'authentic':
                item['purchase_evidence']['china_offer']['authentic'] = False
            else:
                item['purchase_evidence']['china_offer']['stock'] = 'unknown'
            with self.subTest(mutate=mutate):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_unverified_missing_or_blocked_source_is_rejected(self):
        for change in ['missing', 'unreviewed', 'blocked']:
            item, sources = sample_price_evidence()
            if change == 'missing': sources.clear()
            if change == 'unreviewed': sources['fixture-source']['review_state'] = 'candidate'
            if change == 'blocked': sources['fixture-source']['access_state'] = 'blocked'
            with self.subTest(change=change):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_future_or_invalid_evidence_date_is_rejected(self):
        for value in ['2099-01-01', '2026-99-99', '', None]:
            item, sources = sample_price_evidence()
            item['purchase_evidence']['currency_rate']['observed_at'] = value
            with self.subTest(value=value):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_claimed_qualified_flag_does_not_override_evidence(self):
        item, sources = sample_price_evidence()
        item['qualified'] = True
        item['purchase_evidence'] = {}
        self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])

    def test_missing_fee_assumptions_or_exclusions_are_rejected(self):
        for key in ['china_fees_thb', 'thai_delivery_thb', 'exclusions']:
            item, sources = sample_price_evidence()
            del item['purchase_evidence'][key]
            with self.subTest(key=key):
                self.assertFalse(evaluate_gift(item, sources, Decimal('30'))['qualified'])


if __name__ == '__main__':
    unittest.main()
