#!/usr/bin/env python3
"""CPU-only GSQ-inspired teaching example; Python standard library only.

This is not the official GSQ trainer or an LLM benchmark. It demonstrates
Gumbel-Softmax, analytic reconstruction gradients, joint scale learning, and
HARD grid export on one tiny linear layer. Uses SGD, not the paper's Lion;
RTN, not GPTQ initialization; no block staging or model-level distillation.
"""
import json
import math
import random

GRID = [-2, -1, 0, 1]


def softmax(values):
  maximum = max(values)
  exps = [math.exp(v - maximum) for v in values]
  total = sum(exps)
  return [v / total for v in exps]


def mse(weights, x, targets):
  return sum((sum(w * v for w, v in zip(weights, row)) - y) ** 2
             for row, y in zip(x, targets)) / len(x)


def loss_and_grad(logits, scale, x, targets, noise, temperature):
  """Return output MSE, dL/dlogits, dL/dscale for FIXED sampled noise."""
  if temperature <= 0:
    raise ValueError('temperature must be positive')
  probs = [softmax([(l + n) / temperature for l, n in zip(lr, nr)])
           for lr, nr in zip(logits, noise)]
  means = [sum(p * q for p, q in zip(row, GRID)) for row in probs]
  weights = [scale * q for q in means]
  residuals = [sum(w * v for w, v in zip(weights, row)) - y
               for row, y in zip(x, targets)]
  loss = sum(e * e for e in residuals) / len(x)
  dw = [2 * sum(e * row[i] for e, row in zip(residuals, x)) / len(x)
        for i in range(len(weights))]
  dl = [[dw[i] * scale * p * (q - means[i]) / temperature
         for p, q in zip(row, GRID)] for i, row in enumerate(probs)]
  ds = sum(d * q for d, q in zip(dw, means))
  return loss, dl, ds


def run_demo(seed=7):
  rng = random.Random(seed)
  original = [-0.9, 0.35]
  x = [[1., 1.], [1., 0.9], [1.1, 1.], [2., 2.1], [-1., -1.]]
  targets = [sum(w * v for w, v in zip(original, row)) for row in x]
  scale = 0.5
  rtn_codes = [min(GRID, key=lambda q: abs(scale * q - w)) for w in original]
  rtn_weights = [q * scale for q in rtn_codes]
  # Warm-start near RTN, with room for the categorical probabilities to move.
  logits = [[-0.5 * (q - w / scale) ** 2 for q in GRID] for w in original]
  best = (mse(rtn_weights, x, targets), rtn_codes[:], scale)
  for step in range(3000):
    temperature = 1.0 * (0.05 ** (step / 2999))
    dl = [[0.] * len(GRID) for _ in original]
    ds = 0.
    # Independent Gumbel samples reduce gradient variance when averaged.
    for _ in range(8):
      noise = [[-math.log(-math.log(max(1e-12, min(1 - 1e-12, rng.random()))))
                for _ in GRID] for _ in original]
      _, sample_dl, sample_ds = loss_and_grad(logits, scale, x, targets, noise, temperature)
      for i in range(len(original)):
        for k in range(len(GRID)):
          dl[i][k] += sample_dl[i][k] / 8
      ds += sample_ds / 8
    logits = [[l - 0.1 * g for l, g in zip(lr, gr)] for lr, gr in zip(logits, dl)]
    scale -= 0.01 * ds
    codes = [GRID[max(range(len(GRID)), key=lambda k: row[k])] for row in logits]
    hard_loss = mse([q * scale for q in codes], x, targets)
    # Select checkpoints by hard calibration MSE, never by soft training loss.
    if hard_loss < best[0]:
      best = (hard_loss, codes[:], scale)
  hard_loss, codes, scale = best
  return {'seed': seed, 'rtn_codes': rtn_codes, 'rtn_mse': mse(rtn_weights, x, targets),
          'codes': codes, 'scale': scale, 'weights': [q * scale for q in codes],
          'hard_mse': hard_loss}


if __name__ == '__main__':
  print(json.dumps(run_demo(), indent=2))
