---
title: "CL4SRec: Contrastive Learning for Sequential Recommendation"
notetype: feed
date: 2026-06-15
last_modified: 2026-06-15
tags: [recommendation-system, contrastive-learning, sequential-recommendation, deep-learning, self-supervised]
status: published
---

## Paper Info

- **Title:** Contrastive Learning for Sequential Recommendation
- **Authors:** Xu Xie, Fei Sun, Zhaoyang Liu, Shiwen Wu, Jinyang Gao, Bolin Ding, Bin Cui
- **Affiliations:** Peking University & Alibaba Group
- **Venue:** SIGIR 2021
- **ArXiv:** [2010.14395](https://arxiv.org/abs/2010.14395)
- **Citations:** 1,140+ (as of 2026)
- **Code:** [GitHub](https://github.com/RUCAIBox/CIKM2021-CL4SRec)

---

## Problem Statement

Sequential recommendation methods capture user's dynamic interests from historical interactions but suffer from **data sparsity**. Traditional methods (e.g., [[SASRec]]) rely solely on the next-item prediction task to optimize parameters, making it difficult to learn high-quality user representations.

> The objective function of predictive self-supervised learning is almost the same as the goal of sequential recommendation. Applying another same objective function on the same data cannot help.

**Key insight:** Applying another predictive self-supervised task on the same data doesn't help (same objective). Instead, contrastive learning introduces a *different* learning signal.

---

## Methodology

### Core Idea

CL4SRec combines:
1. **Traditional sequential prediction** (next-item recommendation)
2. **Contrastive learning** (self-supervised signal from augmented sequences)

Inspired by **SimCLR** (computer vision), adapted for recommendation sequences.

### Architecture

```
Original sequence → [Augmentation ai] → Encoder f(·) → si_ai
                   [Augmentation aj] → Encoder f(·) → si_aj
                                                        ↓
                            Contrastive Loss (positive pair)
                            + Recommendation Loss (next item)
```

**Encoder:** SASRec (Transformer-based, unidirectional)
- Item embedding + Position embedding
- Multi-head self-attention (causal mask)
- Position-wise feed-forward network
- 2 Transformer blocks, 2 heads, d=64

### Three Data Augmentation Operators

| Augmentation | Parameter | Description |
|---|---|---|
| **Crop** | η (ratio) | Select continuous sub-sequence of length ⌊η × \|s\|⌋ |
| **Mask** | γ (ratio) | Replace γ fraction of items with [mask] token |
| **Reorder** | β (ratio) | Shuffle a continuous sub-sequence of length ⌊β × \|s\|⌋ |

### Contrastive Loss

For a mini-batch of N users, apply 2 random augmentations → 2N augmented sequences.
- **Positive pair:** Two augmented views from the same user
- **Negative samples:** 2(N-1) augmented sequences from other users in the batch

$$L_{cl}(s_u^{a_i}, s_u^{a_j}) = -\log \frac{\exp(\text{sim}(s_u^{a_i}, s_u^{a_j}))}{\exp(\text{sim}(s_u^{a_i}, s_u^{a_j})) + \sum_{s^- \in S^-} \exp(\text{sim}(s_u^{a_i}, s^-))}$$

### Multi-task Training

$$L_{total} = L_{main} + \lambda L_{cl}$$

**Key design choice:** Removed SimCLR's non-linear projection head — direct improvement.

---

## Datasets

| Dataset | #Users | #Items | #Actions | Avg.Length | Density |
|---|---|---|---|---|---|
| Beauty | 22,363 | 12,101 | 198,502 | 8.8 | 0.07% |
| Sports | 25,598 | 18,357 | 296,337 | 8.3 | 0.05% |
| Yelp | 30,983 | 29,227 | 321,087 | 10.3 | 0.04% |
| ML-1M | 6,040 | 3,953 | 1,000,209 | 165.6 | 4.19% |

---

## Results

### Overall Performance (improvement over best baseline)

| Dataset | HR@5 | HR@10 | NDCG@5 | NDCG@10 |
|---|---|---|---|---|
| Beauty | +14.12% | +8.10% | +7.77% | +8.33% |
| Sports | +18.38% | +17.98% | +5.45% | +15.54% |
| Yelp | +8.06% | +11.50% | +6.70% | +8.92% |
| ML-1M | +3.52% | +1.18% | +2.16% | +1.20% |

**Average improvement:** 7.37%–11.02% on ranking metrics

### Key Findings

1. **Augmentation choice matters per dataset** — Mask works best on Sports, Crop on Yelp
2. **Optimal augmentation ratio** peaks then deteriorates (e.g., mask γ≈0.5 on Yelp)
3. **λ weight** — Too high hurts performance; contrastive loss should not dominate
4. **All augmentations help** — Even individually, each augmentation improves over SASRec baseline
5. **Better on sparse datasets** — Larger gains on sparse data (Sports, Yelp) vs dense (ML-1M)

---

## Architecture Details

- Embedding dimension: d = 64
- Transformer blocks: 2
- Attention heads: 2
- Max sequence length: T = 50 (ML-1M: T = 20)
- Optimizer: Adam (lr=0.001, β1=0.9, β2=0.999)
- Batch size: 256
- No projection head (unlike SimCLR)

---

## Significance & Impact

- **First work** to apply contrastive learning to sequential recommendation
- Inspired many follow-ups: [[CoSeRec]], [[ICLRec]], [[DuoRec]], MCLRec, etc.
- Showed that sequence-level self-supervised signals complement item-level signals
- Demonstrated that simple augmentations (crop/mask/reorder) are effective for recommendation

## Limitations

- Augmentation operators are relatively simple
- Negative samples only from in-batch (limited diversity)
- No item-side information utilized (ID-only)
- Performance gains smaller on dense datasets

## Related Papers

- **S3-Rec** (Zhou et al., 2020) — Self-supervised pre-training for sequential rec
- **SASRec** (Kang & McAuley, 2018) — Self-attentive sequential rec (base model)
- **SimCLR** (Chen et al., 2020) — Contrastive learning framework (CV inspiration)
- **CoSeRec** — Improves CL4SRec with item association-aware augmentations
- **ICLRec** — Intent contrastive learning for sequential rec
- **DuoRec** — Enhancement-guided contrastive learning
