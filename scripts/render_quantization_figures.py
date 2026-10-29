#!/usr/bin/env python3
"""Rebuild six original GSQ/RCO explanatory SVGs (standard library only).

Quantitative diagrams consume the existing, executed educational demos.
The temperature and geometry drawings are explicitly illustrative, not LLM
measurements. No network, image model, external font, or raster asset is used.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)
COLORS = {'ink': '#172842', 'muted': '#52617a', 'teal': '#087f78',
          'coral': '#c84b41', 'violet': '#7255b7', 'blue': '#3174b9',
          'amber': '#a96a0a', 'line': '#cbd4e3', 'paper': '#f4f7fc'}


def node(parent, tag, **attrs):
  return ET.SubElement(parent, '{' + SVG_NS + '}' + tag,
                       {k.replace('_', '-'): format(v, '.14g') if isinstance(v, float) else str(v)
                        for k, v in attrs.items()})


def text(parent, x, y, value, size=28, color='ink', weight=400, anchor='start'):
  result = node(parent, 'text', x=x, y=y, fill=COLORS.get(color, color),
                font_size=size, font_weight=weight, text_anchor=anchor)
  result.text = str(value)
  return result


def rect(parent, x, y, width, height, fill='#ffffff', radius=0, **attrs):
  return node(parent, 'rect', x=x, y=y, width=width, height=height,
              fill=COLORS.get(fill, fill), rx=radius, **attrs)


def line(parent, x1, y1, x2, y2, color='line', arrow=False, **attrs):
  return node(parent, 'line', x1=x1, y1=y1, x2=x2, y2=y2,
              stroke=COLORS.get(color, color), stroke_width=3,
              **({'marker-end': 'url(#arrow-' + color + ')'} if arrow else {}), **attrs)


def circle(parent, x, y, radius, color='ink'):
  return node(parent, 'circle', cx=x, cy=y, r=radius, fill=COLORS.get(color, color))


def canvas(number, title, subtitle, height, provenance='illustrative', metadata=None):
  svg = ET.Element('{' + SVG_NS + '}svg', {'width': '800', 'height': str(height),
    'viewBox': '0 0 800 ' + str(height), 'role': 'img',
    'aria-labelledby': 'title description', 'data-provenance': provenance})
  node(svg, 'title', id='title').text = title
  node(svg, 'desc', id='description').text = subtitle
  node(svg, 'metadata').text = json.dumps(metadata or {'scope': 'conceptual illustration'}, sort_keys=True)
  defs = node(svg, 'defs')
  node(defs, 'style').text = 'text{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}'
  for color in ['ink', 'coral', 'teal', 'amber', 'violet']:
    marker = node(defs, 'marker', id='arrow-' + color, viewBox='0 0 10 10',
                  refX=8, refY=5, markerWidth=9, markerHeight=9, orient='auto-start-reverse')
    node(marker, 'path', d='M 0 0 L 10 5 L 0 10 Z', fill=COLORS[color])
  rect(svg, 0, 0, 800, height, 'paper', 24)
  text(svg, 44, 40, 'ILLUSTRATED GUIDE  /  ' + str(number).zfill(2), 22, 'muted', 700)
  text(svg, 44, 96, title, 39, weight=750)
  text(svg, 44, 140, subtitle, 27, 'muted')
  return svg


def load_demo(name):
  path = ROOT / 'assets/examples/quantization' / (name + '.py')
  spec = importlib.util.spec_from_file_location(name, path)
  assert spec is not None and spec.loader is not None
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


def sample_data():
  gsq, rco = load_demo('gsq_demo'), load_demo('rco_demo')
  result = gsq.run_demo(seed=7)
  x = [[1., 1.], [1., .9], [1.1, 1.], [2., 2.1], [-1., -1.]]
  original, rtn = [-.9, .35], [-1., .5]
  targets = [sum(a * b for a, b in zip(original, row)) for row in x]
  errors = {name: [abs(sum(a * b for a, b in zip(weights, row)) - target)
                   for row, target in zip(x, targets)]
            for name, weights in [('rtn', rtn), ('optimized', result['weights'])]}
  assert math.isclose(sum(v * v for v in errors['rtn']) / len(x), result['rtn_mse'], abs_tol=1e-12)
  assert math.isclose(sum(v * v for v in errors['optimized']) / len(x), result['hard_mse'], abs_tol=1e-12)
  return gsq, result, errors, rco.run_demo()


def soft_to_hard(gsq):
  logits, noise = [-1.2, -.2, .9, .1], [.05, -.1, .15, -.05]
  svg = canvas(1, 'GSQ: from soft to hard', 'Same grid, different assignment sharpness', 1100)
  rect(svg, 44, 180, 712, 74, '#e8edf8', 14)
  text(svg, 400, 228, '2-bit grid codes:  −2    −1    0    1', 31, anchor='middle', weight=600)
  for y, temperature, label in [(284, 1.5, 'High T = 1.5'), (594, .15, 'Low T = 0.15')]:
    rect(svg, 44, y, 712, 282, radius=16)
    probs = gsq.softmax([(a + b) / temperature for a, b in zip(logits, noise)])
    mean = sum(p * q for p, q in zip(probs, gsq.GRID))
    text(svg, 70, y + 43, label, 31, weight=650)
    text(svg, 726, y + 43, 'soft q = ' + format(mean, '.3f'), 27, 'muted', anchor='end')
    group = node(svg, 'g', data_temperature=temperature)
    baseline = y + 216
    line(group, 100, baseline, 710, baseline)
    for code, p, center in zip(gsq.GRID, probs, [150, 315, 480, 645]):
      height = 130 * p
      rect(group, center - 38, baseline - height, 76, height,
           'teal' if code == 0 else 'violet', 3, data_probability=p, data_code=code)
      text(group, center, baseline - height - 15, format(p * 100, '.1f') + '%', 26, 'muted', anchor='middle')
      text(group, center, baseline + 38, code, 30, anchor='middle')
  rect(svg, 44, 916, 712, 110, '#e1f2ef', 16)
  text(svg, 400, 958, 'Hard export: code 0 × learned scale', 31, 'teal', 700, 'middle')
  text(svg, 400, 999, 'No probabilities or Gumbel noise at inference', 26, 'teal', anchor='middle')
  text(svg, 400, 1066, 'Illustrative logits + fixed noise; not an LLM result', 24, 'muted', anchor='middle')
  return svg


def pipeline():
  svg = canvas(2, 'GSQ: training → export', 'Learning the assignment is an offline step', 1120)
  stages = [
    ('Pretrained + calibration', 'Collect reference outputs for reconstruction', 'blue'),
    ('GPTQ warm start', 'Initial integer codes + group scales', 'blue'),
    ('Learn logits + scales', 'Backpropagate through soft Gumbel choices', 'violet'),
    ('Anneal + check hard loss', 'Sharper choices; verify the actual grid values', 'violet'),
    ('Freeze, pack and verify', 'Hard codes + scales become the checkpoint', 'teal')]
  for i, (title, description, color) in enumerate(stages):
    y = 186 + i * 164
    rect(svg, 44, y, 712, 126, radius=16)
    circle(svg, 89, y + 53, 26, color)
    text(svg, 89, y + 63, i + 1, 29, '#ffffff', 700, 'middle')
    text(svg, 134, y + 48, title, 32, color, 700)
    text(svg, 134, y + 91, description, 25, 'muted')
    if i < len(stages) - 1:
      line(svg, 400, y + 130, 400, y + 151, 'ink', True)
  rect(svg, 44, 1034, 712, 54, '#e1f2ef', 12)
  text(svg, 400, 1070, 'Inference: no sampling or auxiliary logits', 27, 'teal', 600, 'middle')
  return svg


def output_errors(result, errors):
  svg = canvas(3, 'GSQ: output error matters', 'Actual seeded toy run • calibration samples only', 960,
               'synthetic-demo', result)
  text(svg, 70, 202, 'Absolute output error', 28, weight=650)
  rect(svg, 70, 225, 20, 20, 'coral', 3)
  text(svg, 104, 244, 'RTN', 26, 'coral', 600)
  rect(svg, 250, 225, 20, 20, 'teal', 3)
  text(svg, 284, 244, 'Optimized hard weights', 26, 'teal', 600)
  for tick in [0., .05, .1]:
    y = 530 - tick * 2200
    line(svg, 105, y, 720, y, 'line', stroke_dasharray='5 6')
    text(svg, 90, y + 9, format(tick, '.2f'), 24, 'muted', anchor='end')
  for i, center in enumerate([185, 295, 405, 515, 625]):
    for name, offset, color in [('rtn', -31, 'coral'), ('optimized', 5, 'teal')]:
      value = errors[name][i]
      rect(svg, center + offset, 530 - value * 2200, 26, value * 2200, color, 2,
           data_series=name, data_sample=i + 1, data_value=value)
    text(svg, center, 572, 'S' + str(i + 1), 28, anchor='middle')
  text(svg, 400, 615, 'Original target = zero error (same y-axis for all bars)', 24, 'muted', anchor='middle')
  for x, label, value, color in [(44, 'RTN output MSE', result['rtn_mse'], 'coral'),
                                  (414, 'Hard output MSE', result['hard_mse'], 'teal')]:
    rect(svg, x, 650, 342, 132, radius=16)
    text(svg, x + 24, 692, label, 27, color, 650)
    text(svg, x + 24, 747, format(value, '.6f'), 39, color, 750)
  rect(svg, 44, 814, 712, 100, '#e8edf8', 14)
  text(svg, 400, 852, 'Weight MSE: 0.01625 → 0.12235', 30, weight=650, anchor='middle')
  text(svg, 400, 891, 'Weights get farther away; output error gets smaller', 25, 'muted', anchor='middle')
  text(svg, 400, 942, 'Synthetic data • no held-out or LLM benchmark claim', 23, 'muted', anchor='middle')
  return svg


def allocation(result):
  svg = canvas(4, 'RCO: spend bits selectively', 'Cost = parameter count × chosen bitwidth', 1000,
               'synthetic-demo', result)
  rect(svg, 44, 178, 712, 58, '#e8edf8', 12)
  text(svg, 400, 217, 'Same budget: 10 million payload bits', 29, weight=650, anchor='middle')
  for name, y, title, bits, status, color in [
      ('argmax', 265, 'Independent argmax', result['argmax_bits'], '14 > 10', 'coral'),
      ('dp', 580, 'Constrained DP', result['dp_bits'], '10 ≤ 10', 'teal')]:
    rect(svg, 44, y, 712, 288, radius=16)
    text(svg, 70, y + 45, title, 32, weight=700)
    text(svg, 720, y + 45, status, 32, color, 750, 'end')
    for i, (label, size, precision, fill) in enumerate(zip('ABC', [1, 2, 1], bits, ['blue', 'violet', 'teal'])):
      baseline = y + 100 + i * 66
      text(svg, 70, baseline, label + ' · ' + str(size) + 'M params', 26, weight=650)
      text(svg, 70, baseline + 28, str(precision) + '-bit', 24, 'muted')
      cost = size * precision
      rect(svg, 310, baseline - 13, 45 * cost, 29, fill, 5,
           data_allocation=name, data_cost=cost, data_parameters=size, data_bits=precision)
      text(svg, 310 + 45 * cost + 15, baseline + 10, cost, 28, fill, 700)
  text(svg, 400, 922, 'B has twice the parameters → twice the cost', 28, weight=600, anchor='middle')
  text(svg, 400, 966, 'Toy scores; payload only, before scales and overhead', 25, 'muted', anchor='middle')
  return svg


def manifold():
  svg = canvas(5, 'RCO: protect the budget', 'Projection, retraction and transport are different', 1060)
  rect(svg, 44, 180, 712, 398, radius=16)
  node(svg, 'path', d='M 100 480 Q 400 120 700 480', fill='none', stroke=COLORS['blue'], stroke_width=5)
  text(svg, 485, 475, 'C(α) = B', 32, 'blue', 650)
  line(svg, 170, 393, 430, 237, 'muted', stroke_dasharray='7 6')
  line(svg, 250, 345, 345, 200, 'coral', True)
  text(svg, 365, 215, 'raw update', 26, 'coral')
  line(svg, 250, 345, 370, 273, 'teal', True)
  text(svg, 152, 275, '1', 31, 'teal', 750)
  line(svg, 370, 273, 370, 301.8, 'amber', True)
  text(svg, 405, 294, '2', 31, 'amber', 750)
  line(svg, 370, 301.8, 500, 286.2, 'violet', True)
  text(svg, 510, 292, '3', 31, 'violet', 750)
  circle(svg, 250, 345, 8, 'blue')
  circle(svg, 370, 301.8, 8, 'blue')
  text(svg, 203, 383, 'α', 31, 'blue', 650)
  text(svg, 345, 356, 'α new', 28, 'blue', 650)
  text(svg, 400, 540, 'Schematic curve, not literal high-dimensional logits', 25, 'muted', anchor='middle')
  for i, (title, detail, color) in enumerate([
      ('Project', 'Remove the normal part of the gradient', 'teal'),
      ('Retract', 'Restore the budget along the cost-shift direction', 'amber'),
      ('Transport', 'Align Adam’s first moment to the new tangent', 'violet')]):
    y = 610 + i * 128
    rect(svg, 44, y, 712, 106, radius=14)
    circle(svg, 86, y + 46, 24, color)
    text(svg, 86, y + 56, i + 1, 29, '#ffffff', 700, 'middle')
    text(svg, 130, y + 39, title, 31, color, 700)
    text(svg, 130, y + 80, detail, 24, 'muted')
  text(svg, 400, 1034, 'Expected budget here; constrained DP handles hard choices', 24, 'muted', anchor='middle')
  return svg


def file_budget(result):
  sizes, bits = [1_000_000, 2_000_000, 1_000_000], result['dp_bits']
  payload = sum((n * b + 7) // 8 for n, b in zip(sizes, bits))
  groups = sum((n + 127) // 128 for n in sizes)
  values = [payload, groups * 2, 100_000]
  total = sum(values)
  assert total == result['modeled_file_bytes']
  svg = canvas(6, 'RCO: count every byte', '4M-parameter toy • not a serialized checkpoint', 950,
               'synthetic-demo', {'components': values, 'groups': groups, 'total': total})
  text(svg, 400, 230, format(total, ','), 62, weight=750, anchor='middle')
  text(svg, 400, 275, 'modeled bytes', 30, 'muted', anchor='middle')
  cursor = 60.
  for value, color in zip(values, ['teal', 'violet', 'amber']):
    width = 680 * value / total
    rect(svg, cursor, 316, width, 58, color, data_bytes=value)
    cursor += width
  cards = [('Packed codes', 'Mixed [4, 2, 2]-bit weights', 'teal'),
           ('FP16 scales', format(groups, ',') + ' groups × 2 bytes', 'violet'),
           ('Fixed overhead', 'Untouched tensors / metadata reserve', 'amber')]
  for i, ((label, detail, color), value) in enumerate(zip(cards, values)):
    y = 416 + i * 128
    rect(svg, 44, y, 712, 106, radius=14)
    circle(svg, 80, y + 42, 11, color)
    text(svg, 106, y + 44, label, 30, color, 650)
    text(svg, 720, y + 44, format(value, ','), 32, color, 750, 'end')
    text(svg, 106, y + 82, detail, 24, 'muted')
  text(svg, 400, 859, '1,250,000 + 62,502 + 100,000', 32, weight=600, anchor='middle')
  text(svg, 400, 915, 'No zero-points or row padding in this simplified model', 25, 'muted', anchor='middle')
  return svg


def render_figures():
  gsq, result, errors, rco = sample_data()
  figures = {'gsq-soft-to-hard.svg': soft_to_hard(gsq),
             'gsq-optimization-pipeline.svg': pipeline(),
             'gsq-output-reconstruction.svg': output_errors(result, errors),
             'rco-bit-allocation.svg': allocation(rco),
             'rco-budget-manifold.svg': manifold(),
             'rco-file-budget.svg': file_budget(rco)}
  return {name: ET.tostring(svg, encoding='unicode') + '\n' for name, svg in figures.items()}


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--output', type=Path, default=ROOT / 'assets/img/LLM/GSQ-RCO')
  args = parser.parse_args()
  args.output.mkdir(parents=True, exist_ok=True)
  for name, source in render_figures().items():
    (args.output / name).write_text(source, encoding='utf-8')
    print(args.output / name)


if __name__ == '__main__':
  main()
