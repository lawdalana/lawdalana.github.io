"""Behavior checks for generated, data-grounded article illustrations.

Catch drift between plotted geometry and the executable examples; do not test
stylistic wording. Run with unittest discover -s tests -p 'test_quantization*.py'.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / 'scripts/render_quantization_figures.py'
NS = {'s': 'http://www.w3.org/2000/svg'}


def load_generator():
  if not GENERATOR.is_file():
    raise AssertionError('The reproducible SVG generator is missing')
  spec = importlib.util.spec_from_file_location('quantization_figures', GENERATOR)
  assert spec is not None and spec.loader is not None
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


class QuantizationFigureTests(unittest.TestCase):
  def test_six_accessible_self_contained_vector_figures_are_produced(self):
    figures = load_generator().render_figures()
    self.assertEqual(len(figures), 6)
    self.assertEqual(sum(n.startswith('gsq-') for n in figures), 3)
    self.assertEqual(sum(n.startswith('rco-') for n in figures), 3)
    for name, source in figures.items():
      with self.subTest(name=name):
        svg = ET.fromstring(source)
        self.assertTrue(svg.findtext('s:title', namespaces=NS))
        self.assertTrue(svg.findtext('s:desc', namespaces=NS))
        self.assertEqual(svg.get('role'), 'img')
        self.assertIn(svg.get('data-provenance'), ['illustrative', 'synthetic-demo'])
        self.assertIsNone(svg.find('.//s:script', NS))
        self.assertIsNone(svg.find('.//s:foreignObject', NS))
        for el in svg.iter():
          for key, value in el.attrib.items():
            self.assertFalse(key.lower().startswith('on'), key)
            if key.endswith('href'):
              self.assertTrue(value.startswith('#'), 'No remote SVG resources')

  def test_temperature_chart_uses_the_same_sample_and_valid_probabilities(self):
    svg = ET.fromstring(load_generator().render_figures()['gsq-soft-to-hard.svg'])
    rows = svg.findall('.//s:g[@data-temperature]', NS)
    self.assertEqual(len(rows), 2)
    distributions = []
    for row in rows:
      bars = row.findall('s:rect[@data-probability]', NS)
      p = [float(b.attrib['data-probability']) for b in bars]
      self.assertAlmostEqual(sum(p), 1., places=12)
      for bar, value in zip(bars, p):
        self.assertAlmostEqual(float(bar.attrib['height']), value * 130, places=5)
      distributions.append(p)
    self.assertAlmostEqual(distributions[0][0], 0.1072652307341338, places=12)
    self.assertAlmostEqual(distributions[1][2], 0.9986054768839242, places=12)
    self.assertGreater(max(distributions[1]), max(distributions[0]))

  def test_output_error_bars_are_actual_seeded_demo_residuals_on_one_scale(self):
    svg = ET.fromstring(load_generator().render_figures()['gsq-output-reconstruction.svg'])
    metadata = json.loads(svg.findtext('s:metadata', namespaces=NS) or '{}')
    self.assertAlmostEqual(metadata['rtn_mse'], 0.00421, places=12)
    self.assertAlmostEqual(metadata['hard_mse'], 0.0007347016581720856, places=14)
    rtn = svg.findall('.//s:rect[@data-series="rtn"]', NS)
    optimized = svg.findall('.//s:rect[@data-series="optimized"]', NS)
    self.assertEqual(len(rtn), 5)
    self.assertEqual(len(optimized), 5)
    self.assertAlmostEqual(float(rtn[3].attrib['data-value']), .115, places=12)
    self.assertAlmostEqual(float(optimized[0].attrib['data-value']), .0004330559324141614, places=12)
    for bar in rtn + optimized:
      value = float(bar.attrib['data-value'])
      self.assertAlmostEqual(float(bar.attrib['height']), 2200 * value, places=5)
      self.assertAlmostEqual(float(bar.attrib['y']) + float(bar.attrib['height']), 530., places=5)

  def test_allocation_bars_preserve_parameter_weighting_and_a_shared_cost_axis(self):
    svg = ET.fromstring(load_generator().render_figures()['rco-bit-allocation.svg'])
    metadata = json.loads(svg.findtext('s:metadata', namespaces=NS) or '{}')
    self.assertEqual(metadata['argmax_cost'], 14)
    self.assertEqual(metadata['dp_cost'], 10)
    for allocation, expected in [('argmax', [4, 8, 2]), ('dp', [4, 4, 2])]:
      bars = svg.findall('.//s:rect[@data-allocation="' + allocation + '"]', NS)
      self.assertEqual([int(b.attrib['data-cost']) for b in bars], expected)
      for bar, cost in zip(bars, expected):
        self.assertAlmostEqual(float(bar.attrib['width']), 45 * cost, places=6)

  def test_stacked_byte_bar_contains_real_payload_scales_and_overhead(self):
    svg = ET.fromstring(load_generator().render_figures()['rco-file-budget.svg'])
    bars = svg.findall('.//s:rect[@data-bytes]', NS)
    values = [int(b.attrib['data-bytes']) for b in bars]
    self.assertEqual(values, [1_250_000, 62_502, 100_000])
    self.assertEqual(sum(values), 1_412_502)
    self.assertAlmostEqual(sum(float(b.attrib['width']) for b in bars), 680., places=5)
    for bar, value in zip(bars, values):
      self.assertAlmostEqual(float(bar.attrib['width']) / 680, value / 1_412_502, places=8)

  def test_cli_writes_the_same_six_parseable_svg_assets(self):
    self.assertTrue(GENERATOR.is_file(), 'The reproducible SVG generator is missing')
    with tempfile.TemporaryDirectory(prefix='quantization-figures-') as folder:
      result = subprocess.run(['python3', str(GENERATOR), '--output', folder], capture_output=True, text=True)
      self.assertEqual(result.returncode, 0, result.stderr)
      paths = sorted(Path(folder).glob('*.svg'))
      self.assertEqual(len(paths), 6)
      for path in paths:
        ET.parse(path)


if __name__ == '__main__':
  unittest.main()
