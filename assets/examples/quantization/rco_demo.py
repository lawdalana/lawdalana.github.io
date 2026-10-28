#!/usr/bin/env python3
"""CPU-only RCO geometry / budget-DP teaching example; standard library only.

Not an LLM search implementation: no model gradients, Adam, or Gumbel-STE
training loop. These primitives illustrate the continuous/discrete distinction.
The DP optimizes supplied ADDITIVE LOGIT SCORES, not the joint LLM loss.
"""
import json
import math


def softmax(values):
  maximum = max(values)
  exps = [math.exp(v - maximum) for v in values]
  return [v / sum(exps) for v in exps]


def expected_cost(alpha, weights, costs):
  return sum(w * sum(p * c for p, c in zip(softmax(row), costs))
             for w, row in zip(weights, alpha))


def budget_normal(alpha, weights, costs):
  probs = [softmax(row) for row in alpha]
  return [[w * p * (c - sum(pk * ck for pk, ck in zip(row, costs)))
           for p, c in zip(row, costs)] for w, row in zip(weights, probs)]


def project(vector, normal):
  dot = sum(x * n for row, nr in zip(vector, normal) for x, n in zip(row, nr))
  squared = sum(n * n for row in normal for n in row)
  if squared == 0:
    raise ValueError('degenerate budget normal')
  return [[x - dot / squared * n for x, n in zip(row, nr)]
          for row, nr in zip(vector, normal)]


def retract(alpha, weights, costs, budget, tolerance=1e-11):
  if not min(costs) * sum(weights) < budget < max(costs) * sum(weights):
    raise ValueError('finite softmax requires a strictly interior budget')
  def shifted(t):
    return [[a + t * c for a, c in zip(row, costs)] for row in alpha]
  low, high = -1., 1.
  for _ in range(80):
    if expected_cost(shifted(low), weights, costs) <= budget <= expected_cost(shifted(high), weights, costs):
      break
    low *= 2
    high *= 2
  else:
    raise ArithmeticError('failed to bracket budget')
  for _ in range(100):
    middle = (low + high) / 2
    cost = expected_cost(shifted(middle), weights, costs)
    if abs(cost - budget) <= tolerance:
      return shifted(middle)
    if cost < budget:
      low = middle
    else:
      high = middle
  raise ArithmeticError('budget did not converge within tolerance')


def knapsack(scores, sizes, costs, budget):
  """Exact multiple-choice DP in INTEGER cost units; one option per group."""
  if (not scores or len(scores) != len(sizes)
      or any(len(row) != len(costs) for row in scores)
      or not costs or any(type(v) is not int or v <= 0 for v in sizes + costs)
      or type(budget) is not int or budget < 0):
    raise ValueError('use positive integer sizes/costs and matching nonempty rows')
  # Sparse reachable states: used cost -> (summed score, option-index list).
  states = {0: (0, [])}
  for row, size in zip(scores, sizes):
    following = {}
    for used, (score, choices) in states.items():
      for k, cost in enumerate(costs):
        total, value = used + size * cost, score + row[k]
        if total <= budget and (total not in following or value > following[total][0]):
          following[total] = (value, choices + [k])
    states = following
  if not states:
    raise ValueError('no discrete assignment fits budget')
  used = max(states, key=lambda b: (states[b][0], -b))
  score, choices = states[used]
  return choices, used, score


def modeled_bytes(sizes, bits, group_size=128, scale_bits=16, fixed_bytes=0):
  """Simplified per-tensor packed payload + ceil-group scales + fixed cost.

  Not a GGUF/safetensors serializer. Real row boundaries, zero points,
  padding, headers and untouched tensors must be modeled separately.
  """
  return (sum(math.ceil(n * b / 8) for n, b in zip(sizes, bits))
          + sum(math.ceil(n / group_size) * math.ceil(scale_bits / 8) for n in sizes)
          + fixed_bytes)


def run_demo():
  alpha, sizes, costs = [[0.] * 3 for _ in range(3)], [1, 2, 1], [2, 3, 4]
  retracted = retract(alpha, sizes, costs, 10.5)
  normal = budget_normal(retracted, sizes, costs)
  gradient = [[1., 2., 3.], [-1., 3., 4.], [2., 0., -2.]]
  tangent = project(gradient, normal)
  dot = sum(g * n for row, nr in zip(tangent, normal) for g, n in zip(row, nr))
  scores = [[0, 1, 5], [0, 1, 4], [0, 0, 0]]
  argmax = [max(range(3), key=lambda k: row[k]) for row in scores]
  choice, used, score = knapsack(scores, sizes, costs, 10)
  bits = [costs[k] for k in choice]
  return {'continuous_cost_before': expected_cost(alpha, sizes, costs),
          'continuous_cost_after': expected_cost(retracted, sizes, costs),
          'tangent_dot_normal': dot, 'argmax_bits': [costs[k] for k in argmax],
          'argmax_cost': sum(w * costs[k] for w, k in zip(sizes, argmax)),
          'dp_bits': bits, 'dp_cost': used, 'dp_score': score,
          'payload_average_bits': used / sum(sizes),
          'modeled_file_bytes': modeled_bytes([n * 1_000_000 for n in sizes], bits, fixed_bytes=100_000)}


if __name__ == '__main__':
  print(json.dumps(run_demo(), indent=2))
