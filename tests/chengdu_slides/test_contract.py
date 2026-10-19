"""Contract checks catch incomplete publication and broken bilingual records."""
import unittest
import json
import tempfile
from copy import deepcopy
from pathlib import Path
from fixtures import sample_dataset

try:
    from scripts.chengdu_slides.model import load_dataset
    from scripts.chengdu_slides.validation import validate_category, validate_dataset
except ImportError:
    load_dataset = validate_category = validate_dataset = None


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(callable(validate_dataset), 'content validation is not implemented')
        self.assertTrue(callable(load_dataset), 'dataset loading is not implemented')

    def test_dataset_loader_joins_files_and_does_not_invent_missing_records(self):
        data = sample_dataset()
        with tempfile.TemporaryDirectory() as directory:
            for key, value in data.items():
                Path(directory, key + '.json').write_text(json.dumps(value), encoding='utf-8')
            self.assertEqual(load_dataset(Path(directory)), data)
            Path(directory, 'gifts.json').unlink()
            with self.assertRaises(FileNotFoundError):
                load_dataset(Path(directory))

    def test_synthetic_small_dataset_only_passes_nonpublication_mode(self):
        data = sample_dataset()
        self.assertEqual(validate_dataset(data), [])
        self.assertTrue(validate_dataset(data, publication=True))

    def test_missing_or_unreviewed_source_is_rejected(self):
        for change in ['missing', 'unreviewed', 'bad-date']:
            data = sample_dataset()
            if change == 'missing': data['sources'] = []
            if change == 'unreviewed': data['sources'][0]['review_state'] = 'candidate'
            if change == 'bad-date': data['sources'][0]['retrieved_at'] = 'bad'
            with self.subTest(change=change):
                self.assertTrue(validate_dataset(data))

    def test_duplicate_ids_or_identity_cannot_inflate_counts(self):
        for key in ['id', 'identity_key']:
            data = sample_dataset()
            duplicate = deepcopy(data['attractions'][0])
            if key == 'id': duplicate['identity_key'] = 'other-identity'
            else: duplicate['id'] = 'other-id'
            data['attractions'].append(duplicate)
            with self.subTest(key=key):
                self.assertTrue(validate_dataset(data))

    def test_both_languages_and_two_distinct_units_are_required(self):
        for change in ['language', 'unit', 'kind']:
            data = sample_dataset(); item = data['attractions'][0]
            if change == 'language': del item['units'][0]['body']['zh-Hans']
            if change == 'unit': item['units'].pop()
            if change == 'kind': item['units'][1]['kind'] = 'intro'
            with self.subTest(change=change):
                self.assertTrue(validate_dataset(data))

    def test_mismatched_or_unresolved_fact_tokens_are_rejected(self):
        for text in ['完全不同 {other}', '价格 {price} {missing}']:
            data = sample_dataset()
            data['attractions'][0]['units'][0]['body']['zh-Hans'] = [text]
            with self.subTest(text=text):
                self.assertTrue(validate_dataset(data))

    def test_missing_practical_detail_or_date_is_rejected(self):
        for key in ['transport', 'tickets', 'opening', 'cautions', 'observed_at']:
            data = sample_dataset()
            del data['attractions'][0]['details'][key]
            with self.subTest(key=key):
                self.assertTrue(validate_dataset(data))

    def test_category_gate_requires_fifteen_distinct_entries(self):
        self.assertTrue(validate_category(sample_dataset(), 'attractions'))
        with self.assertRaises(ValueError):
            validate_category(sample_dataset(), 'not-a-category')

    def test_duplicate_source_ids_are_rejected(self):
        data = sample_dataset(); data['sources'].append(deepcopy(data['sources'][0]))
        self.assertTrue(validate_dataset(data))

    def test_unsupported_stage_cannot_be_published(self):
        data = sample_dataset(); data['attractions'][0]['stage'] = 'discovered'
        self.assertTrue(validate_dataset(data, publication=True))


if __name__ == '__main__':
    unittest.main()
