"""Behavior checks for the downloadable CPU-only GSQ/RCO teaching examples.

Breaks caught: incorrect softmax derivatives, export of soft rather than grid
weights, lost budget retraction, and independent argmax replacing knapsack.
Run: python3 -m unittest discover -s tests -p 'test_quantization_examples.py' -v
"""
import importlib.util
import itertools
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_demo(name):
  path = ROOT / 'assets' / 'examples' / 'quantization' / (name + '.py')
  if not path.is_file():
    raise AssertionError('Downloadable example is missing: ' + str(path))
  spec = importlib.util.spec_from_file_location(name, path)
  assert spec is not None and spec.loader is not None
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module


class GSQTests(unittest.TestCase):
  def test_softmax_survives_large_logits(self):
    g = load_demo('gsq_demo')
    self.assertEqual(g.softmax([1000, 1000]), [0.5, 0.5])

  def test_relaxation_gradients_match_independent_finite_differences(self):
    g = load_demo('gsq_demo')
    logits = [[0.2, -0.1, 0.3, 0.0], [-0.4, 0.5, 0.1, 0.2]]
    noise = [[0.1, -0.2, 0.3, -0.1], [0.0, 0.1, -0.1, 0.2]]
    x, y, scale, tau = [[1., 2.], [2., -1.]], [0.4, -0.3], 0.7, 0.8
    loss, grad, gs = g.loss_and_grad(logits, scale, x, y, noise, tau)
    self.assertTrue(math.isfinite(loss))
    eps = 1e-6
    for i in range(2):
      for k in range(4):
        plus, minus = [r[:] for r in logits], [r[:] for r in logits]
        plus[i][k] += eps
        minus[i][k] -= eps
        fd = (g.loss_and_grad(plus, scale, x, y, noise, tau)[0]
              - g.loss_and_grad(minus, scale, x, y, noise, tau)[0]) / (2 * eps)
        self.assertAlmostEqual(grad[i][k], fd, places=7)
    fd = (g.loss_and_grad(logits, scale + eps, x, y, noise, tau)[0]
          - g.loss_and_grad(logits, scale - eps, x, y, noise, tau)[0]) / (2 * eps)
    self.assertAlmostEqual(gs, fd, places=7)

  def test_hard_export_is_on_grid_and_improves_actual_output_loss(self):
    g = load_demo('gsq_demo')
    result = g.run_demo(seed=7)
    self.assertLess(result['hard_mse'], result['rtn_mse'] * 0.5)
    self.assertTrue(all(q in [-2, -1, 0, 1] for q in result['codes']))
    self.assertTrue(math.isfinite(result['scale']))
    for q, w in zip(result['codes'], result['weights']):
      self.assertAlmostEqual(w, q * result['scale'])

  def test_seeded_example_is_reproducible(self):
    g = load_demo('gsq_demo')
    self.assertEqual(g.run_demo(seed=7), g.run_demo(seed=7))

  def test_temperature_must_be_positive(self):
    g = load_demo('gsq_demo')
    with self.assertRaises(ValueError):
      g.loss_and_grad([[0.] * 4], 1., [[1.]], [0.], [[0.] * 4], 0.)


class RCOTests(unittest.TestCase):
  def test_expected_cost_uses_parameter_counts_not_unweighted_mean(self):
    r = load_demo('rco_demo')
    self.assertAlmostEqual(r.expected_cost([[0.] * 3] * 3, [1, 2, 1], [2, 3, 4]), 12.)

  def test_normal_is_derivative_of_budget(self):
    r = load_demo('rco_demo')
    alpha, weights, costs = [[0.1, 0.7, -0.2], [1., 0., -1.]], [1, 2], [2, 3, 4]
    normal = r.budget_normal(alpha, weights, costs)
    eps = 1e-6
    for i in range(2):
      for k in range(3):
        plus, minus = [v[:] for v in alpha], [v[:] for v in alpha]
        plus[i][k] += eps
        minus[i][k] -= eps
        fd = (r.expected_cost(plus, weights, costs) - r.expected_cost(minus, weights, costs)) / (2 * eps)
        self.assertAlmostEqual(normal[i][k], fd, places=7)

  def test_projection_and_transported_momentum_are_tangent(self):
    r = load_demo('rco_demo')
    a, w, c = [[0.] * 3] * 3, [1, 2, 1], [2, 3, 4]
    n = r.budget_normal(a, w, c)
    gradient = [[1., 2., 3.], [-1., 3., 4.], [2., 0., -2.]]
    tangent = r.project(gradient, n)
    self.assertAlmostEqual(sum(x * y for row, nr in zip(tangent, n) for x, y in zip(row, nr)), 0., places=12)
    moved = r.retract([[v - .1 * g for v, g in zip(ar, gr)] for ar, gr in zip(a, tangent)], w, c, 10.5)
    transported = r.project(tangent, r.budget_normal(moved, w, c))
    self.assertAlmostEqual(sum(x * y for row, nr in zip(transported, r.budget_normal(moved, w, c)) for x, y in zip(row, nr)), 0., places=12)

  def test_retraction_fixes_finite_step_budget_drift(self):
    r = load_demo('rco_demo')
    a = [[1., -3., 2.], [-2., 1., 0.], [0., 0., 1.]]
    result = r.retract(a, [1, 2, 1], [2, 3, 4], 10.5)
    self.assertAlmostEqual(r.expected_cost(result, [1, 2, 1], [2, 3, 4]), 10.5, places=9)
    self.assertEqual(a[0], [1., -3., 2.])

  def test_retraction_rejects_unreachable_or_endpoint_budget(self):
    r = load_demo('rco_demo')
    for budget in [7, 8, 16, 17]:
      with self.subTest(budget=budget), self.assertRaises(ValueError):
        r.retract([[0.] * 3] * 3, [1, 2, 1], [2, 3, 4], budget)

  def test_dp_beats_argmax_and_matches_exhaustive_optimum(self):
    r = load_demo('rco_demo')
    scores, sizes, costs = [[0, 1, 5], [0, 1, 4], [0, 0, 0]], [1, 2, 1], [2, 3, 4]
    assignment, used, score = r.knapsack(scores, sizes, costs, 10)
    self.assertEqual((assignment, used, score), ([2, 0, 0], 10, 5))
    feasible = [(sum(scores[i][k] for i, k in enumerate(ks)), ks) for ks in itertools.product(range(3), repeat=3)
                if sum(sizes[i] * costs[k] for i, k in enumerate(ks)) <= 10]
    self.assertEqual(score, max(s for s, _ in feasible))
    self.assertLessEqual(used, 10)

  def test_discrete_solution_can_leave_budget_unused(self):
    r = load_demo('rco_demo')
    self.assertEqual(r.knapsack([[10, 0]], [1], [2, 4], 3), ([0], 2, 10))

  def test_dp_rejects_infeasible_budget_and_noninteger_costs(self):
    r = load_demo('rco_demo')
    for budget, costs in [(1, [2, 4]), (5, [2.5, 4])]:
      with self.subTest(budget=budget), self.assertRaises(ValueError):
        r.knapsack([[1, 2]], [1], costs, budget)

  def test_cli_demo_reports_feasible_allocation_and_modeled_bytes(self):
    r = load_demo('rco_demo')
    result = r.run_demo()
    self.assertEqual(result['dp_bits'], [4, 2, 2])
    self.assertEqual(result['dp_cost'], 10)
    self.assertEqual(result['modeled_file_bytes'], 1_412_502)
    self.assertAlmostEqual(result['continuous_cost_after'], 10.5, places=9)
    self.assertLess(abs(result['tangent_dot_normal']), 1e-12)

  def test_file_accounting_includes_group_scales_and_fixed_overhead(self):
    r = load_demo('rco_demo')
    self.assertEqual(r.modeled_bytes([1_000_000, 2_000_000, 1_000_000], [4, 2, 2], 128, 16, 100_000), 1_412_502)


if __name__ == '__main__':
  unittest.main()
