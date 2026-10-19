"""Load the explicit canonical JSON bundle; never invent missing records."""
import json
from pathlib import Path

PARTS = ('meta', 'sources', 'assets', 'attractions', 'restaurants', 'gifts', 'support')


def load_dataset(data_dir: Path) -> dict:
    data = {}
    for name in PARTS:
        with (data_dir / (name + '.json')).open(encoding='utf-8') as handle:
            value = json.load(handle)
        expected = dict if name == 'meta' else list
        if not isinstance(value, expected):
            raise ValueError(f'{name}.json must contain a {expected.__name__}')
        data[name] = value
    return data
