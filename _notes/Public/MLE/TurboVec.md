---
title: TurboVec — Vector Index บน TurboQuant
notetype: feed
date: 2026-05-26
last_modified: 2026-05-26
tags: [vector-search, quantization, turboquant, FAISS, RAG, rust, python]
status: published
---

# [TurboVec](https://github.com/RyanCodrai/turbovec) — Vector Index บน Google's TurboQuant

> **10M documents (dim=1536)** จาก **31 GB → 4 GB** — search เร็วกว่า FAISS โดยไม่ต้อง train codebook

- [TurboVec — Vector Index บน Google's TurboQuant](#turbovec--vector-index-บน-googles-turboquant)
  - [❓ คืออะไร](#-คืออะไร)
  - [จุดเด่นหลัก](#จุดเด่นหลัก)
  - [TurboQuant Algorithm ทำงานยังไง](#turboquant-algorithm-ทำงานยังไง)
  - [เปรียบเทียบกับ FAISS](#เปรียบเทียบกับ-faiss)
  - [Recall Benchmarks](#recall-benchmarks)
  - [Python API](#python-api)
  - [IdMapIndex — Stable IDs + Delete](#idmapindex--stable-ids--delete)
  - [Hybrid Retrieval (Filtered Search)](#hybrid-retrieval-filtered-search)
  - [Framework Integrations](#framework-integrations)
  - [Rust API](#rust-api)
  - [Use Cases](#use-cases)
  - [TurboQuant Paper (ICLR 2026)](#turboquant-paper-iclr-2026)
  - [References](#references)

---

## ❓ คืออะไร

**TurboVec** คือ vector index library เขียนด้วย **Rust** + Python bindings ที่ build บน Google Research's **TurboQuant** algorithm (ICLR 2026)

- **Author:** Ryan Codrai
- **License:** MIT
- **PyPI:** `turbovec` v0.5.3 (Python ≥3.9)
- **crates.io:** `turbovec`
- **★ 2,900+** GitHub stars
- **Paper:** [TurboQuant (arXiv:2504.19874)](https://arxiv.org/abs/2504.19874)

Core idea: ใช้ **data-oblivious quantization** (random rotation + Lloyd-Max scalar quantizer) บีบอัด vectors โดยไม่ต้อง train codebook เลย — ผลคือ compression 16x แต่ recall ยังดีกว่า FAISS PQ

---

## จุดเด่นหลัก

| Feature | รายละเอียด |
|---------|-----------|
| **Compression** | 16x (float32 → 2-bit) — 10M docs dim=1536 จาก **31 GB → 4 GB** |
| **Speed** | เร็วกว่า FAISS FastScan **12-20% บน ARM**, 1-6% บน x86 |
| **No Training** | Data-oblivious — add vectors → indexed ทันที ไม่ต้อง k-means |
| **Filtered Search** | Allowlist filter ทำใน SIMD kernel — ไม่ over-fetch |
| **Recall** | ดีกว่า FAISS PQ **0.4-3.4 points** ที่ R@1 (OpenAI d=1536+) |
| **Pure Local** | ไม่มี managed service, เหมาะ air-gapped RAG |
| **SIMD Kernels** | Hand-written NEON (ARM) + AVX-512BW (x86) + AVX2 fallback |

---

## TurboQuant Algorithm ทำงานยังไง

TurboQuant ใช้ insight ง่ายๆ: **random rotation ทำให้ทุก coordinate ตาม distribution ที่รู้** → ไม่ต้องดู data เลย

### 5 Steps

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. Normalize │ ──► │ 2. Random    │ ──► │ 3. Lloyd-Max │ ──► │ 4. Bit-pack  │ ──► │ 5. Length    │
│  strip norm   │     │   Rotation   │     │   Quantize   │     │  tight bytes │     │ renormalize  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Normalize** — ดึง norm ออกจาก vector, เก็บเป็น float แยก → vector กลายเป็น unit direction บน hypersphere

2. **Random Rotation** — คูณทุก vector ด้วย random orthogonal matrix เดียวกัน
   - หลัง rotation → แต่ละ coordinate ตาม **Beta distribution** ที่ converge เป็น $N(0, \frac{1}{d})$ ใน high dimensions
   - เป็น **data-oblivious** — ไม่สนใจ input distribution

3. **Lloyd-Max Scalar Quantization** — รู้ distribution แล้ว → precompute optimal bucket boundaries
   - 2-bit = 4 buckets, 4-bit = 16 buckets
   - คำนวณจาก math, ไม่ต้องใช้ data
   - Distortion อยู่ภายใน **2.7× ของ Shannon's lower bound**

4. **Bit-pack** — แต่ละ coordinate เป็น integer เล็ก → pack แน่น
   - dim=1536: 6,144 bytes (FP32) → 384 bytes (2-bit) = **16× compression**

5. **Length-renormalized Scoring** — scalar quantization underestimate inner products
   - เก็บ $\frac{\|v\|}{\langle u, \hat{x} \rangle}$ ต่อ vector
   - Search kernel คูณ scalar → **unbiased estimator** โดยไม่เสีย search-time cost

> **Encoding cost:** เพิ่มแค่ 1 dot product/dim ต่อ vector — sub-second สำหรับ 1M vectors ที่ d=1536

---

## เปรียบเทียบกับ FAISS

| Aspect | TurboVec | FAISS PQ |
|--------|----------|----------|
| **Training** | ไม่ต้อง train | ต้อง k-means++ |
| **Rebuild** | ไม่ต้อง | เมื่อ corpus เปลี่ยน |
| **Compression** | 16× (2-bit) | ~8× (8-bit) |
| **ARM speed** | 12-20% เร็วกว่า | baseline |
| **x86 speed** | 1-6% เร็วกว่า (4-bit) | baseline |
| **Recall (d=1536+)** | ดีกว่า 0.4-3.4 pts | baseline |
| **Filtering** | In-kernel (SIMD block) | Post-fetch |
| **Privacy** | Pure local | Pure local |
| **Add vectors** | Instant, no calibration | Need retrain |

**สรุป:** TurboVec ชนะเรื่อง convenience (ไม่ต้อง train) + compression + ARM speed ส่วน FAISS ยังแข็งแกร่งเรื่อง ecosystem และ features ที่หลากหลายกว่า

---

## Recall Benchmarks

เปรียบเทียบกับ FAISS `IndexPQ` (LUT256, nbits=8, float32 LUT) — 100K vectors, k=64

| Setting | TurboQuant vs FAISS R@1 |
|---------|----------------------|
| OpenAI d=1536, 4-bit | **+0.4 ~ +3.4 points** |
| OpenAI d=3072, 4-bit | **+0.4 ~ +3.4 points** |
| GloVe d=200, 4-bit | +0.3 points |
| GloVe d=200, 2-bit | -1.2 points (close by k≈16) |

ทั้งคู่ converge → R@1 = 1.0 ที่ k=4 สำหรับ OpenAI embeddings

> **หมายเหตุ:** FAISS baseline ที่ใช้เปรียบเทียบเป็น **LUT256 (float32 LUT)** ซึ่งแม่นกว่า u8-LUT ใน paper ต้นฉบับ — เป็น baseline ที่แข็งแกร่งกว่า

---

## Python API

### Install

```bash
pip install turbovec
```

### Basic Usage

```python
from turbovec import TurboQuantIndex

# สร้าง index — bit_width เลือก 2 หรือ 4
index = TurboQuantIndex(dim=1536, bit_width=4)

# Add vectors (ไม่ต้อง train!)
index.add(vectors)           # np.ndarray shape (n, dim), float32
index.add(more_vectors)      # เพิ่มได้เรื่อยๆ

# Search
scores, indices = index.search(query, k=10)

# Save / Load
index.write("my_index.tq")
loaded = TurboQuantIndex.load("my_index.tq")
```

> `dim` เป็น optional — ถ้าไม่ใส่จะ infer จาก first `add()` call

---

## IdMapIndex — Stable IDs + Delete

ถ้าต้องการ external IDs ที่ไม่เปลี่ยนตอน delete:

```python
import numpy as np
from turbovec import IdMapIndex

idx = IdMapIndex(dim=1536, bit_width=4)
idx.add_with_ids(vectors, np.array([1001, 1002, 1003], dtype=np.uint64))

scores, ids = idx.search(query, k=10)   # ids เป็น uint64 external ids
idx.remove(1002)                         # O(1) by id
```

| Method | Notes |
|--------|-------|
| `add_with_ids(vectors, ids)` | `ids` เป็น uint64 array |
| `remove(id) -> bool` | O(1), hash-table backed |
| `search(queries, k, allowlist=...)` | Filtered search |
| `id in idx` | Membership check |

---

## Hybrid Retrieval (Filtered Search)

ของจริง — BM25/SQL กรอง candidates ก่อน แล้ว dense rerank:

```python
import numpy as np
from turbovec import IdMapIndex

idx = IdMapIndex(dim=1536, bit_width=4)
idx.add_with_ids(vectors, ids)

# Stage 1: SQL/BM25 กรอง candidates
allowed = np.array(
    db.execute("SELECT id FROM docs WHERE tenant=?", (t,)).fetchall(),
    dtype=np.uint64
)

# Stage 2: Dense rerank ใน candidate set
scores, ids = idx.search(query, k=10, allowlist=allowed)
```

**ทำไมดีกว่า post-filter:**
- Kernel ไม่ insert disallowed vectors เข้า heap เลย
- ได้ `min(k, len(allowed))` results เสมอ — ไม่มี -1/NaN padding
- Selective allowlists → skip SIMD blocks ที่ไม่มี allowed slots → เร็วขึ้น

---

## Framework Integrations

Drop-in replacements — เปลี่ยนแค่ import, pipeline เดิมทำงานได้เหมือนเดิม

| Framework | Install | Replaces |
|-----------|---------|----------|
| **LangChain** | `pip install turbovec[langchain]` | `InMemoryVectorStore` |
| **LlamaIndex** | `pip install turbovec[llama-index]` | `SimpleVectorStore` |
| **Haystack** | `pip install turbovec[haystack]` | `InMemoryDocumentStore` |
| **Agno** | `pip install turbovec[agno]` | `LanceDb` |

---

## Rust API

```rust
use turbovec::TurboQuantIndex;

let mut index = TurboQuantIndex::new(1536, 4);
index.add(&vectors);
let results = index.search(&queries, 10);
index.write("index.tv").unwrap();
let loaded = TurboQuantIndex::load("index.tv").unwrap();
```

```rust
use turbovec::IdMapIndex;

let mut index = IdMapIndex::new(1536, 4);
index.add_with_ids(&vectors, &[1001, 1002, 1003]);
let (scores, ids) = index.search(&queries, 10);
index.remove(1002);
```

### File Formats

**`.tv`** — TurboQuantIndex:
- Header: `bit_width` (u8) + `dim` (u32) + `n_vectors` (u32)
- Packed codes + norms (f32)

**`.tvim`** — IdMapIndex:
- Magic "TVIM" + version byte + core payload + `slot_to_id` (u64 array)

---

## Use Cases

1. **🤖 RAG Systems** — ลด RAM จาก 31GB → 4GB สำหรับ 10M docs
2. **📱 On-device / Edge Search** — บีบอัดได้มาก, ไม่ต้อง managed service
3. **🔒 Air-gapped Environments** — pure local, ไม่มี data ออกจากเครื่อง
4. **🔍 Hybrid Retrieval** — BM25 + dense rerank ด้วย filtered search
5. **⚡ KV Cache Quantization** — 3.5 bits/channel โดย quality-neutral
6. **🏗️ Multi-tenant SaaS** — allowlist filter ต่อ tenant ใน kernel เลย

---

## TurboQuant Paper (ICLR 2026)

**Title:** *TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate*
**Authors:** Google Research
**arXiv:** [2504.19874](https://arxiv.org/abs/2504.19874)

### Key Contributions

- **Data-oblivious algorithm** ที่ achieve near-optimal distortion rate (within ~2.7× of Shannon lower bound) ทุก bit-width ทุก dimension
- **Two-stage approach** สำหรับ unbiased inner product:
  1. MSE quantizer (Lloyd-Max)
  2. 1-bit Quantized JL (QJL) transform บน residual
- **KV cache quantization:** quality-neutral ที่ **3.5 bits/channel**, marginal degradation ที่ **2.5 bits/channel**
- **ANN search:** recall ดีกว่า PQ เดิม, indexing time เกือบเป็น **zero**
- **Formal proof** ของ information-theoretic lower bounds สำหรับ vector quantization

### ทำไม TurboQuant ถึงใกล้ optimal

$$\text{Distortion ratio} = \frac{\text{TurboQuant distortion}}{\text{Shannon lower bound}} \approx 2.7$$

Random rotation ทำให้ coordinates independent → scalar quantizer แต่ละตัว optimal → distortion ใกล้ theoretical limit

---

## References

- [TurboVec GitHub](https://github.com/RyanCodrai/turbovec) — Rust + Python implementation
- [TurboQuant Paper (arXiv:2504.19874)](https://arxiv.org/abs/2504.19874) — ICLR 2026
- [RaBitQ (arXiv:2405.12497)](https://arxiv.org/abs/2405.12497) — Source ของ length-renormalization technique (SIGMOD 2024)
- [FAISS FastScan](https://github.com/facebookresearch/faiss/wiki/Fast-accumulation-of-PQ-and-AQ-codes-(FastScan)) — SIMD kernel reference
- [turboquant-py](https://pypi.org/project/turboquant-py/) — Community reference implementation

