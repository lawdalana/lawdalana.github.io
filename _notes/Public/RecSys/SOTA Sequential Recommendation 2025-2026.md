---
title: "State-of-the-Art Sequential Recommendation Systems (2025-2026)"
notetype: feed
date: 2026-06-15
last_modified: 2026-06-15
tags: [recommendation-system, sequential-recommendation, LLM, foundation-model, survey, SOTA]
status: published
---

## Overview: สามคลื่นของ Sequential Recommendation

### คลื่นที่ 1: Classical Sequential Models (2018-2022)

โมเดลที่เป็น foundation และยังเป็น baseline ที่ใช้เปรียบเทียบทุกวันนี้

| Model | Year | สิ่งที่สำคัญ |
|---|---|---|
| **GRU4Rec** | 2016 | RNN-based session recommendation |
| **Caser** | 2018 | CNN-based sequential pattern |
| **[[SASRec]]** | 2018 | Transformer (self-attention) สำหรับ SeqRec |
| **BERT4Rec** | 2019 | Bidirectional Transformer (cloze task) |
| **S3-Rec** | 2020 | Self-supervised pre-training (MIP, MAP, SPD, AAC) |
| **[[CL4SRec]]** | 2021 | Contrastive learning + augmentation (crop/mask/reorder) |
| **CoSeRec** | 2022 | ปรับปรุง CL4SRec ด้วย item association-aware augmentation |
| **ICLRec** | 2022 | Intent contrastive learning |
| **DuoRec** | 2022 | Enhancement-guided contrastive learning |

### คลื่นที่ 2: Frequency & Architecture Enhancements (2022-2024)

| Model | Year | สิ่งที่สำคัญ |
|---|---|---|
| **FMLP-Rec** | 2022 | แทน self-attention ด้วย Filter-enhanced MLP (Fourier) — เร็วกว่าและดีกว่า |
| **FEARec** | 2023 | Frequency-enhanced analysis — decompose sequences เป็น low/high frequency |
| **BSARec** | 2024 | Bipartite Spatial-Temporal Aggregation |
| **TiSRec** | 2025 | Time Interval-wise Segmentation — แบ่ง sequence ตาม time gap |

### คลื่นที่ 3: LLM-Powered & Agent-Based (2024-2026) ← SOTA ปัจจุบัน

| Model | Year | สิ่งที่สำคัญ |
|---|---|---|
| **P5** | 2023 | รุ่นแรกที่ใช้ LLM เป็น recommendation engine (T5-based) |
| **LLM-Emb SeqRec** | 2024 | ใช้ LLM embeddings มา initialize SASRec/BERT4Rec → gains ชัดเจน |
| **ReaRec** | 2025-2026 | Reasoning-augmented framework — multi-step reasoning ตอน inference |
| **GenAIR** | 2026 | Generative Archetype-grounded Item Representations (WWW 2026 Oral) |
| **Agent4Rec** | 2024 | LLM agent-based recommender simulator (1,000 agents) |
| **RecAgent** | 2025 | LLM agents ที่ model user behavior แบบ simulation |
| **MemRec** | 2026 | Collaborative Memory-Augmented Agentic Recommender |
| **FindRec** | 2025 | Stein-Guided Entropic Flow สำหรับ Multi-Modal SeqRec (WWW 2025) |

---

## SOTA แบ่งตาม Category ปัจจุบัน

### 🏆 Pure Sequential (ไม่ใช้ LLM)

1. **FEARec** — Frequency-enhanced ยังเป็น top performer บนหลาย benchmarks
2. **BSARec** — Spatial-temporal aggregation แข่งสูสี
3. **FMLP-Rec** — คุ้มที่สุดด้าน efficiency (เร็ว + แม่นยำ)

### 🏆 LLM-Enhanced Sequential

1. **ReaRec** (2025-2026) — เพิ่ม multi-step reasoning ตอน inference บน base model ที่มี → Cited 73 ในเวลาสั้น
2. **GenAIR** (2026, WWW Oral) — LLM สร้าง item archetype → behavioral calibration
3. **LLM-init SASRec/BERT4Rec** — ใช้ LLM embeddings initialize แล้ว fine-tune

### 🏆 Agentic Recommendation (Emerging)

1. **Agent4Rec** — Simulation framework ที่ใช้ LLM agents เป็น users
2. **RecAgent** — ทะลุกรอบ traditional → user + item agents
3. **AgentRecBench** (NeurIPS 2026) — Benchmark สำหรับ LLM agent-based recommenders
4. **MemRec** — Memory-augmented agents

---

## Evolution Map

```
SASRec (2018) → CL4SRec (2021) → FEARec (2023) → ReaRec/GenAIR (2025-26)
     ↓                ↓                ↓                    ↓
  Transformer    +Contrastive    +Frequency         +LLM Reasoning
```

---

## Key Trends 2025-2026

### 1. LLM Integration เป็น Mainstream

ไม่ใช่แค่ใช้ LLM แยก แต่ integrate เข้ากับ traditional architectures:
- LLM embeddings → initialize traditional models = gains ชัดเจน
- LLM agents → redefine ว่า "recommendation" คืออะไร (conversational, reasoning)

### 2. Reasoning-Augmented Recommendation

**ReaRec** (73 citations ใน ~6 เดือน) = trend ที่ร้อนแรงสุด

> "Think before recommend" — multi-step reasoning ก่อนให้คำแนะนำ

### 3. Agentic Recommender Systems

เปลี่ยนจาก model → agent ที่สามารถ interact, explain, และ refine:
- Benchmarks ใหม่เกิดขึ้น (AgentRecBench, RecoWorld)
- ใช้ LLM เป็น user simulator และ recommender

### 4. Foundation Models for Recommendation

- Pre-train บน cross-domain data → fine-tune บน specific domain
- Semantic IDs แทน traditional item IDs
- Multi-modal (ข้อความ + รูป + behavior)

### 5. Efficiency Still Matters

FMLP-Rec approach (แทน attention ด้วย MLP+filter) ยังได้ผลดีและเร็วกว่า — สำหรับ production: โมเดลง่ายๆ ที่ efficient ยังเป็นที่ต้องการ

---

## สรุป: ใครคือ SOTA ตอนนี้?

| มุมมอง | คำตอบ |
|---|---|
| **Pure accuracy** | FEARec / BSARec + LLM enhancement |
| **LLM era** | ReaRec (reasoning) / GenAIR (archetype) |
| **Production-friendly** | FMLP-Rec (efficiency) / SASRec (simplicity) |
| **Emerging** | Agent-based (Agent4Rec, RecAgent, MemRec) |
| **All-rounder** | ReaRec framework ที่สามารถ augment บน base model ใดๆ |

**[[CL4SRec]]** เป็น milestone สำคัญ (paper แรกที่ apply CL กับ SeqRec) แต่ตอนนี้มี follow-ups ที่ทำได้ดีกว่าแล้ว ทั้งในแกน contrastive (CoSeRec, ICLRec) และแกนอื่น (LLM, reasoning, agent)

---

## References

- [CL4SRec](https://arxiv.org/abs/2010.14395) (SIGIR 2021) — 1,140+ citations
- [FEARec](https://arxiv.org/abs/2304.09184) (SIGIR 2023)
- [FMLP-Rec](https://arxiv.org/abs/2202.08865) (CIKM 2022)
- [ReaRec](https://arxiv.org/abs/2503.02229) (TKDE 2026) — 73 citations
- [GenAIR](https://arxiv.org/abs/2606.11023) (WWW 2026 Oral)
- [LLM-Enhanced SeqRec](https://arxiv.org/abs/2402.01339) (2024)
- Survey: "A survey of foundation model-powered recommender systems" (2025)
- Survey: "A survey on sequential recommendation" (Frontiers of CS, 2026, 63 citations)
