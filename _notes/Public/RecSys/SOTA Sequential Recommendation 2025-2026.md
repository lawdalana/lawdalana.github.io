---
title: "State-of-the-Art Sequential Recommendation Systems (2025-2026)"
notetype: feed
date: 2026-06-15
last_modified: 2026-09-16
tags: [recommendation-system, sequential-recommendation, LLM, foundation-model, survey, SOTA]
status: published
---

## Overview: สามคลื่นของ Sequential Recommendation

### คลื่นที่ 1: Classical Sequential Models (2018-2022)

โมเดลกลุ่มนี้วางรากฐานให้วิธีที่พัฒนาตามมา และยังใช้เป็น baseline ในการเปรียบเทียบ

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
| **FEARec** | 2023 | วิเคราะห์ลำดับข้อมูลโดยแยกส่วนความถี่ต่ำและสูง |
| **BSARec** | 2024 | Bipartite Spatial-Temporal Aggregation |
| **TiSRec** | 2025 | Time Interval-wise Segmentation — แบ่ง sequence ตาม time gap |

### คลื่นที่ 3: LLM-Powered & Agent-Based (2024-2026) ← SOTA ปัจจุบัน

| Model | Year | สิ่งที่สำคัญ |
|---|---|---|
| **P5** | 2023 | รุ่นแรกที่ใช้ LLM เป็น recommendation engine (T5-based) |
| **LLM-Emb SeqRec** | 2024 | ใช้ LLM embeddings เป็นค่าเริ่มต้นของ SASRec/BERT4Rec และช่วยให้ผลลัพธ์ดีขึ้น |
| **ReaRec** | 2025-2026 | Reasoning-augmented framework — multi-step reasoning ตอน inference |
| **GenAIR** | 2026 | Generative Archetype-grounded Item Representations (WWW 2026 Oral) |
| **Agent4Rec** | 2024 | LLM agent-based recommender simulator (1,000 agents) |
| **RecAgent** | 2025 | ใช้ LLM agents จำลองพฤติกรรมผู้ใช้ |
| **MemRec** | 2026 | Collaborative Memory-Augmented Agentic Recommender |
| **FindRec** | 2025 | Stein-Guided Entropic Flow สำหรับ Multi-Modal SeqRec (WWW 2025) |

---

## SOTA แบ่งตาม Category ปัจจุบัน

### 🏆 Pure Sequential (ไม่ใช้ LLM)

1. **FEARec** — Frequency-enhanced ยังเป็น top performer บนหลาย benchmarks
2. **BSARec** — Spatial-temporal aggregation แข่งสูสี
3. **FMLP-Rec** — คุ้มที่สุดด้าน efficiency (เร็ว + แม่นยำ)

### 🏆 LLM-Enhanced Sequential

1. **ReaRec** (2025-2026) — เพิ่มการให้เหตุผลหลายขั้นระหว่าง inference ให้กับโมเดลพื้นฐานที่มีอยู่ และได้รับการอ้างอิง 73 ครั้งในเวลาไม่นาน
2. **GenAIR** (2026, WWW Oral) — LLM สร้าง item archetype → behavioral calibration
3. **LLM-init SASRec/BERT4Rec** — ใช้ LLM embeddings initialize แล้ว fine-tune

### 🏆 Agentic Recommendation (Emerging)

1. **Agent4Rec** — Simulation framework ที่ใช้ LLM agents เป็น users
2. **RecAgent** — ขยายจากโมเดลแนะนำแบบดั้งเดิมไปสู่ agents ที่แทนผู้ใช้และ item
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

LLM ถูกนำมาใช้ร่วมกับสถาปัตยกรรมเดิมมากขึ้น:

- ใช้ LLM embeddings เป็นค่าเริ่มต้นของโมเดลเดิม เพื่อช่วยให้ผลลัพธ์ดีขึ้น
- ใช้ LLM agents เพิ่มความสามารถในการสนทนาและให้เหตุผลแก่ระบบแนะนำ

### 2. Reasoning-Augmented Recommendation

**ReaRec** ได้รับการอ้างอิง 73 ครั้งใน ~6 เดือน สะท้อนความสนใจต่อการใช้ reasoning ในระบบแนะนำ

> แนวคิดคือให้โมเดลคิดอย่างเป็นขั้นตอนก่อนเสนอคำแนะนำ

### 3. Agentic Recommender Systems

บทบาทขยับจากโมเดลที่ให้ผลแนะนำ ไปสู่ agent ที่โต้ตอบ อธิบาย และปรับคำแนะนำได้:

- Benchmarks ใหม่เกิดขึ้น (AgentRecBench, RecoWorld)
- ใช้ LLM เป็น user simulator และ recommender

### 4. Foundation Models for Recommendation

- Pre-train ด้วยข้อมูลจากหลายโดเมน แล้ว fine-tune สำหรับโดเมนที่ต้องการใช้งาน
- Semantic IDs แทน traditional item IDs
- Multi-modal (ข้อความ + รูป + behavior)

### 5. Efficiency Still Matters

แนวทางของ FMLP-Rec ซึ่งแทน attention ด้วย MLP+filter ยังให้ผลดีและทำงานได้เร็ว โมเดลที่เรียบง่ายและใช้ทรัพยากรคุ้มค่าจึงยังสำคัญสำหรับ production

---

## สรุป: ใครคือ SOTA ตอนนี้?

| มุมมอง | คำตอบ |
|---|---|
| **Pure accuracy** | FEARec / BSARec + LLM enhancement |
| **LLM era** | ReaRec (reasoning) / GenAIR (archetype) |
| **Production-friendly** | FMLP-Rec (efficiency) / SASRec (simplicity) |
| **Emerging** | Agent-based (Agent4Rec, RecAgent, MemRec) |
| **All-rounder** | ReaRec เป็น framework สำหรับเสริมความสามารถให้โมเดลพื้นฐาน |

**[[CL4SRec]]** เป็นงานสำคัญที่เริ่มนำ contrastive learning มาใช้กับ sequential recommendation งานที่ต่อยอดภายหลังให้ผลดีขึ้น ทั้งการพัฒนา contrastive learning เช่น CoSeRec และ ICLRec และการใช้แนวทางอื่น เช่น LLM, reasoning และ agent

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
