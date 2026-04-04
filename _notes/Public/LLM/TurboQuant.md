---
title: TurboQuant
notetype: feed
date: 2026-04-04
last_modified: 2026-04-04
tags: [llm, quantization, kv-cache, compression, vector-search, google-research]
---

# [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](https://arxiv.org/abs/2504.19874)

> **บีบอัด memory LLM ได้ 6x โดยไม่สูญเสีย accuracy เลย — plug-and-play, ไม่ต้อง fine-tune, ไม่ต้อง calibration data**

---

## 🔥 ทำไมต้องสนใจ

ถ้าคุณเคยรัน LLM ใน production คุณจะรู้ว่า **model weights ไม่ใช่ปัญหา memory หลัก** — **KV cache ต่างหาก** ที่กิน memory มหาศาล

ทุกครั้งที่ transformer สร้าง token ใหม่ มันต้องเก็บ key vector + value vector สำหรับ token นั้นทุก attention layer ชุด vectors ทั้งหมดนี้คือ "working memory" ของโมเดล และมัน **โตขึ้น linear กับ context length**

| Model | Context | KV Cache Size |
| :--- | :--- | :--- |
| Llama-3.1-8B | 128K | **ใหญ่กว่า model weights** |
| 70B model + 512 users | — | ~512 GB เฉพาะ cache |

Google Research เอา **TurboQuant** มาแก้ปัญหานี้โดยตรง — compress KV cache แบบ **online** (real-time ระหว่าง inference) ได้ **6x** โดย **zero accuracy loss**

---

## 📋 Paper Info

- **Title:** TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate
- **Authors:** Amir Zandieh, Vahab Mirrokni, Majid Daliri (NYU), Majid Hadian, Praneeth Kacham, Insu Han (KAIST), Lars Gottesbüren, Rajesh Jayaram — Google Research
- **Venue:** **ICLR 2026**, Rio de Janeiro
- **arXiv:** [2504.19874](https://arxiv.org/abs/2504.19874)
- **Blog:** [research.google/blog/turboquant](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)
- **Submitted:** April 28, 2025 | **Blog post:** March 24, 2026

---

## 🧱 สถาปัตยกรรม: Two-Stage Pipeline

TurboQuant ผสาน 2 algorithm เข้าด้วยกัน:

### Stage 1: PolarQuant — Heavy Lifting

![TurboQuant01](/assets/img/Other/LLM/TurboQuant01.avif)

**หลักการ:** ถ้าเราหมุน (rotate) vector ด้วย random orthogonal matrix → coordinates จะ follow **concentrated Beta distribution** ≈ $\mathcal{N}(0, 1/d)$ โดยที่ $d$ คือ vector dimension

$$x' = R \cdot x \quad \text{where } R \sim \text{QR}(\text{Gaussian}(d \times d))$$

**ทำไมสำคัญ?**

| Traditional VQ | PolarQuant |
| :--- | :--- |
| ต้องคำนวณ + เก็บ scale factors ทุก block | Distribution เป็น known + data-independent |
| เพิ่ม overhead 1-2 bits/number | ใช้ pre-computed Lloyd-Max quantizer |
| Overhead กิน compression gain | **Zero overhead!** |

**ขั้นตอน:**
1. Random rotate vector → coordinates อยู่ใน Beta distribution ที่รู้ล่วงหน้า
2. แปลงเป็น **polar coordinates** (radius + angle)
3. Angle distribution มี concentration สูง → ไม่ต้อง normalize
4. ใช้ **Lloyd-Max quantizer** (pre-computed สำหรับ Beta distribution) → ไม่ต้องเก็บ per-block constants

> **Companion paper:** [[PolarQuant]] — AISTATS 2026

### Stage 2: QJL — 1-bit Error Correction

![TurboQuant02](/assets/img/Other/LLM/TurboQuant02.avif)

Stage 1 ให้ MSE-optimal quantization แต่มี **bias ใน inner product estimation** → attention scores คลาดเคลื่อน

**QJL แก้ปัญหานี้ด้วย:**

$$\text{residual} = x - \text{PolarQuant}(x)$$
$$\text{QJL}(\text{residual}) \rightarrow \text{sign bits } \{+1, -1\}$$

1. เอา residual error จาก Stage 1
2. ใช้ **Quantized Johnson-Lindenstrauss Transform** → compress เหลือ 1 bit/sign
3. ใช้ **unbiased estimator** ที่ balance high-precision query + low-precision data
4. ผลลัพธ์: **unbiased inner product** → attention scores แม่นยำ

> **Companion paper:** QJL (Quantized JL) — AAAI 2025

---

## 📊 Results

### KV Cache Compression

| Bits/Channel | ผลลัพธ์ | Compression |
| :--- | :--- | :--- |
| **3.5 bits** | **Zero accuracy loss** (absolute quality neutrality) | ~4.5x |
| **3 bits** | 99.5% attention fidelity | **~5x** |
| **2.5 bits** | Marginal quality degradation | ~6x |

### Benchmarks

ทดสอบบน standard long-context benchmarks:
- **LongBench**, **Needle In A Haystack**, **ZeroSCROLLS**, **RULER**, **L-Eval**
- Models: **Gemma**, **Mistral**
- ผล: **Outperform** existing product quantization ใน recall
- **Indexing time → virtually zero** (vs PQ ที่ต้อง train codebook)

### Mathematical Optimality

$$\text{TurboQuant distortion} \approx 2.7 \times \text{Shannon's lower bound}$$

พิสูจน์โดยใช้:
- **Shannon's lower bound** สำหรับ information-theoretic limit
- **Yao's minimax principle** สำหรับ randomized algorithms
- ผล: TurboQuant ใกล้เคียง theoretical optimal โดยต่างเพียง constant factor ≈ 2.7

---

## 💥 Impact

### สำหรับ AI Infrastructure
- **ลด GPU memory 6x** → serve users เยอะขึ้นบน hardware เดิม
- **ลด inference cost** อย่างมีนัยสำลัก
- **เปิด context window ยาวขึ้น** (1M+ tokens) โดยไม่ OOM
- Plug-and-play: ไม่ต้อง fine-tune, ไม่ต้อง calibration data

### สำหรับ Vector Search
- Compress embeddings ใน vector databases
- Indexing time เกือบ 0 (ไม่ต้อง train codebook)
- Recall ดีกว่า PQ เดิม

### Industry Reaction (48 ชั่วโมงแรก)
- 📉 Memory chip stocks **ตก**
- 🚀 Community port ไป **llama.cpp**, **MLX framework** แล้ว
- 💬 Cloudflare CEO เรียกว่า **"Google's DeepSeek moment"**

---

## 🔗 Community Resources

| Resource | Link |
| :--- | :--- |
| PyTorch implementation (unofficial) | [github.com/tonbistudio/turboquant-pytorch](https://github.com/tonbistudio/turboquant-pytorch) |
| ik_llama.cpp implementation | [Issue #1509](https://github.com/ikawrakow/ik_llama.cpp/issues/1509) |
| llama.cpp integration tracking | [Discussion #20969](https://github.com/ggml-org/llama.cpp/discussions/20969) |
| SGLang feature request | [Issue #21618](https://github.com/sgl-project/sglang/issues/21618) |
| Triton kernel implementation | [dejan.ai/blog/turboquant](https://dejan.ai/blog/turboquant/) |
| Independent analysis | [turboquant.net](https://turboquant.net/) |

> ⚠️ **ยังไม่มี official open-source implementation จาก Google** (April 2026)

---

## 📚 Related Work

- **ITQ3_S** ([arXiv:2603.27914](https://arxiv.org/abs/2603.27914)) — Interleaved Ternary Quantization ใช้ TurboQuant เป็น rotation-domain strategy ผ่าน Fast Walsh-Hadamard Transform (FWHT) สำหรับ 3-bit inference
- [[Gemma2]] — Google's open-source LLM ที่ใช้ทดสอบ TurboQuant
- [[Grouped Query Attention]] — Attention optimization ที่ช่วยลด KV cache size
- [[Speculative Sampling]] — อีก technique หนึ่งสำหรับ speed up LLM inference

---

## ⚖️ TurboQuant vs Traditional Methods

| คุณลักษณะ | Traditional VQ (PQ, GPTQ, AWQ) | TurboQuant |
| :--- | :--- | :--- |
| **Quantization mode** | Offline (weights) | **Online** (KV cache real-time) |
| **Calibration data** | ต้องมี | **ไม่ต้อง** |
| **Fine-tuning** | บาง method ต้อง | **ไม่ต้อง** |
| **Overhead** | 1-2 bits/number (scale factors) | **Zero overhead** |
| **Inner product bias** | มี | **ไม่มี** (QJL unbiased) |
| **Theoretical guarantee** | Heuristic | **Near-optimal** (2.7× Shannon bound) |
| **Indexing time** | นาน (train codebook) | **~0** (data-oblivious) |

---

## 🧠 สรุปสั้น

TurboQuant คือ **algorithm บีบอัด KV cache ที่ near-optimal ทางทฤษฎี** โดยใช้ 2-stage pipeline:

1. **PolarQuant** → random rotate + scalar quantize → compression หลัก, zero overhead
2. **QJL** → 1-bit residual correction → eliminate inner product bias

ผลลัพธ์: **6x memory reduction, zero accuracy loss, plug-and-play**

นี่คือ breakthrough ที่เปลี่ยน landscape ของ LLM inference — ลด cost, เพิ่ม capacity, เปิดโลก context window ยาวๆ โดยไม่ต้องซื้อ GPU เพิ่ม
