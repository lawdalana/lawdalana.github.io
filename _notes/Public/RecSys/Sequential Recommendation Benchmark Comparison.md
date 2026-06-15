---
title: "Sequential Recommendation: Benchmark Comparison"
notetype: feed
date: 2026-06-15
last_modified: 2026-06-15
tags: [recommendation-system, benchmark, NDCG, HR, evaluation, comparison]
status: published
---

## Evaluation Protocol

- **Method:** Leave-one-out
- **Ranking:** Full item set (no negative sampling)
- **Metrics:** HR@N (Hit Rate), NDCG@N (Normalized Discounted Cumulative Gain)
- **Source:** FEARec paper (SIGIR 2023) — same evaluation protocol across all models

> ⚠️ ตัวเลขจาก FEARec paper ซึ่ง reimplement baselines เอง → อาจมี bias นิดหน่อย

---

## Beauty Dataset (Sparse — Density 0.07%)

| Model | HR@5 | HR@10 | NDCG@5 | NDCG@10 |
|---|---|---|---|---|
| BPR-MF | 0.0120 | 0.0299 | 0.0040 | 0.0053 |
| GRU4Rec | 0.0164 | 0.0365 | 0.0086 | 0.0142 |
| Caser | 0.0259 | 0.0418 | 0.0127 | 0.0253 |
| [[SASRec]] | 0.0365 | 0.0627 | 0.0236 | 0.0281 |
| BERT4Rec | 0.0193 | 0.0401 | 0.0187 | 0.0254 |
| FMLP-Rec | 0.0398 | 0.0632 | 0.0258 | 0.0333 |
| **[[CL4SRec]]** | 0.0401 | 0.0683 | 0.0223 | 0.0317 |
| CoSeRec | 0.0537 | 0.0752 | 0.0361 | 0.0430 |
| DuoRec | 0.0546 | 0.0845 | 0.0352 | 0.0443 |
| **FEARec** | **0.0597** | **0.0884** | **0.0366** | **0.0459** |

---

## Sports Dataset (Sparse — Density 0.05%)

| Model | HR@5 | HR@10 | NDCG@5 | NDCG@10 |
|---|---|---|---|---|
| BPR-MF | 0.0092 | 0.0188 | 0.0040 | 0.0051 |
| GRU4Rec | 0.0137 | 0.0274 | 0.0096 | 0.0137 |
| Caser | 0.0139 | 0.0231 | 0.0085 | 0.0126 |
| [[SASRec]] | 0.0218 | 0.0336 | 0.0127 | 0.0169 |
| BERT4Rec | 0.0176 | 0.0326 | 0.0105 | 0.0153 |
| FMLP-Rec | 0.0218 | 0.0344 | 0.0144 | 0.0185 |
| **[[CL4SRec]]** | 0.0227 | 0.0374 | 0.0129 | 0.0184 |
| CoSeRec | 0.0287 | 0.0437 | 0.0196 | 0.0242 |
| DuoRec | 0.0326 | 0.0498 | 0.0208 | 0.0262 |
| **FEARec** | **0.0353** | **0.0547** | **0.0216** | **0.0272** |

---

## ML-1M Dataset (Dense — Density 4.19%)

| Model | HR@5 | HR@10 | NDCG@5 | NDCG@10 |
|---|---|---|---|---|
| BPR-MF | 0.0078 | 0.0162 | 0.0052 | 0.0079 |
| GRU4Rec | 0.0763 | 0.1658 | 0.0385 | 0.0671 |
| Caser | 0.0816 | 0.1593 | 0.0372 | 0.0624 |
| [[SASRec]] | 0.1087 | 0.1904 | 0.0638 | 0.0910 |
| BERT4Rec | 0.0733 | 0.1323 | 0.0432 | 0.0619 |
| FMLP-Rec | 0.1109 | 0.1932 | 0.0657 | 0.0918 |
| **[[CL4SRec]]** | 0.1147 | 0.1975 | 0.0662 | 0.0928 |
| CoSeRec | 0.1262 | 0.2212 | 0.0761 | 0.1021 |
| DuoRec | 0.2038 | 0.2946 | 0.1390 | 0.1680 |
| **FEARec** | **0.2212** | **0.3123** | **0.1523** | **0.1861** |

---

## Gap Analysis: แต่ละรุ่นต่างกันแค่ไหน?

### บน Beauty (Sparse) — เทียบจาก SASRec baseline (HR@10)

| Model | HR@10 | Δ vs SASRec | % Improvement |
|---|---|---|---|
| SASRec | 0.0627 | — | baseline |
| FMLP-Rec | 0.0632 | +0.0005 | +0.8% |
| CL4SRec | 0.0683 | +0.0056 | +8.9% |
| CoSeRec | 0.0752 | +0.0125 | +19.9% |
| DuoRec | 0.0845 | +0.0218 | +34.8% |
| **FEARec** | **0.0884** | +0.0257 | **+41.0%** |

### บน ML-1M (Dense) — เทียบจาก SASRec baseline (HR@10)

| Model | HR@10 | Δ vs SASRec | % Improvement |
|---|---|---|---|
| SASRec | 0.1904 | — | baseline |
| FMLP-Rec | 0.1932 | +0.0028 | +1.5% |
| CL4SRec | 0.1975 | +0.0071 | +3.7% |
| CoSeRec | 0.2212 | +0.0308 | +16.2% |
| DuoRec | 0.2946 | +0.1042 | +54.7% |
| **FEARec** | **0.3123** | +0.1219 | **+64.0%** |

---

## Visual Gap Summary

```
Beauty (Sparse) HR@10:
SASRec     ████████████████████  0.0627
CL4SRec    ████████████████████  0.0683  (+8.9%)
CoSeRec    ███████████████████████  0.0752  (+19.9%)
DuoRec     ██████████████████████████  0.0845  (+34.8%)
FEARec     ███████████████████████████  0.0884  (+41.0%)

ML-1M (Dense) HR@10:
SASRec     ████████████████████  0.1904
CL4SRec    ████████████████████  0.1975  (+3.7%)
CoSeRec    █████████████████████  0.2212  (+16.2%)
DuoRec     █████████████████████████████  0.2946  (+54.7%)
FEARec     ██████████████████████████████  0.3123  (+64.0%)
```

---

## สรุป Gap ระหว่างรุ่น

| เปรียบเทียบ | Gap โดยเฉลี่ย | ข้อสังเกต |
|---|---|---|
| SASRec → CL4SRec | **+3.7% ถึง +8.9%** | Contrastive learning ช่วยเรื่อง sparse data |
| CL4SRec → CoSeRec | **+10% ถึง +12%** | Item-aware augmentation ดีกว่า generic |
| CoSeRec → DuoRec | **+10% ถึง +33%** | Model-level augmentation > data-level |
| DuoRec → FEARec | **+4% ถึง +9%** | Frequency domain ให้มุมใหม่ |
| SASRec → FEARec | **+41% ถึง +64%** | สะสมทั้งหมด = ใหญ่มาก |

### Key Takeaways

1. **แต่ละขั้นพัฒนาเพิ่ม ~10-20%** สะสมไปเรื่อยๆ
2. **DuoRec และ FEARec คือก้าวกระโดดใหญ่สุด** — จาก contrastive/data augmentation → model-level + frequency domain
3. **Sparse datasets** ได้ประโยชน์จาก contrastive learning มากกว่า dense datasets
4. **Dense datasets (ML-1M)** ได้ประโยชน์จาก DuoRec/FEARec มากกว่า (+54-64%)
5. **LLM-enhanced รุ่นใหม่** (ReaRec, GenAIR) คาดว่าจะเพิ่มอีก 5-15% บน FEARec baseline

---

## References

- [FEARec Paper (SIGIR 2023)](https://arxiv.org/abs/2304.09184) — Source of all benchmark numbers
- [CL4SRec Paper (SIGIR 2021)](https://arxiv.org/abs/2010.14395)
- [FMLP-Rec Paper (CIKM 2022)](https://arxiv.org/abs/2202.08865)
- [DuoRec Paper (WWW 2022)](https://arxiv.org/abs/2110.05730)
- [CoSeRec Paper (CIKM 2022)](https://arxiv.org/abs/2206.01788)
