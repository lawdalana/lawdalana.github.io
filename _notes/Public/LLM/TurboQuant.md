---
title: TurboQuant
notetype: feed
date: 2026-04-04
last_modified: 2026-09-16
tags: [llm, quantization, kv-cache, compression, vector-search, google-research]
---

# [TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate](https://arxiv.org/abs/2504.19874)

> **บีบอัด KV cache ของ LLM ได้สูงสุด 6x ตามผลที่รายงาน โดยไม่ต้อง fine-tune หรือใช้ข้อมูล calibration ส่วนผลต่อความแม่นยำขึ้นกับจำนวนบิตและงานที่ทดสอบ**

---

## 🔥 ทำไมต้องสนใจ

เมื่อรัน LLM ใน production ต้องเผื่อหน่วยความจำให้ทั้ง **model weights และ KV cache** โดย KV cache อาจกลายเป็นคอขวดเมื่อ context ยาวหรือมีผู้ใช้พร้อมกันจำนวนมาก

ทุกครั้งที่ transformer สร้าง token ใหม่ ระบบจะเก็บ key vector และ value vector ของ token นั้นในแต่ละ attention layer ข้อมูลชุดนี้คือ KV cache ซึ่ง **มีขนาดเพิ่มเป็นสัดส่วนกับความยาว context**

| Model | Context | KV Cache Size |
| :--- | :--- | :--- |
| Llama-3.1-8B | 128K | **ใหญ่กว่า model weights** |
| 70B model + 512 users | — | ~512 GB เฉพาะ cache |

Google Research เสนอ **TurboQuant** เพื่อบีบอัด KV cache แบบ **online** หรือระหว่าง inference โดยรายงานอัตราการบีบอัดได้ถึง **6x** และการรักษาคุณภาพในงานที่ทดสอบ

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

บทความนี้อธิบายกระบวนการผ่านอัลกอริทึม 2 ส่วน:

### Stage 1: PolarQuant — Heavy Lifting

![TurboQuant01](/assets/img/Other/LLM/TurboQuant01.avif)

**หลักการ:** เมื่อหมุน vector ด้วย random orthogonal matrix แต่ละ coordinate จะมีการกระจายแบบ **concentrated Beta distribution** ซึ่งประมาณได้ด้วย $\mathcal{N}(0, 1/d)$ เมื่อ $d$ ซึ่งเป็นจำนวนมิติของ vector มีค่าสูง

$$x' = R \cdot x \quad \text{where } R \sim \text{QR}(\text{Gaussian}(d \times d))$$

**ทำไมสำคัญ?**

| Traditional VQ | PolarQuant |
| :--- | :--- |
| ต้องคำนวณและเก็บ scale factors ทุก block | อธิบายการกระจายได้โดยไม่ต้องเรียนรู้จากชุดข้อมูล |
| เพิ่ม overhead 1-2 bits/number | ใช้ pre-computed Lloyd-Max quantizer |
| Overhead ลดพื้นที่ที่ประหยัดได้จากการบีบอัด | **ไม่ต้องเก็บ scale factor ต่อ block** |

**ขั้นตอน:**

1. Random rotate vector → coordinates อยู่ใน Beta distribution ที่รู้ล่วงหน้า
2. แปลงเป็น **polar coordinates** (radius + angle)
3. Angle distribution มี concentration สูง → ไม่ต้อง normalize
4. ใช้ **Lloyd-Max quantizer** (pre-computed สำหรับ Beta distribution) → ไม่ต้องเก็บ per-block constants

> **Companion paper:** [[PolarQuant]] — AISTATS 2026

### Stage 2: QJL — 1-bit Error Correction

![TurboQuant02](/assets/img/Other/LLM/TurboQuant02.avif)

Stage 1 ลดความคลาดเคลื่อนแบบ MSE แต่ยังมี **อคติในการประมาณ inner product** ซึ่งส่งผลต่อ attention scores

**QJL แก้ปัญหานี้ด้วย:**

$$\text{residual} = x - \text{PolarQuant}(x)$$
$$\text{QJL}(\text{residual}) \rightarrow \text{sign bits } \{+1, -1\}$$

1. นำส่วนความคลาดเคลื่อนที่เหลือ (residual error) จาก Stage 1 มาใช้
2. ใช้ **Quantized Johnson-Lindenstrauss Transform** → compress เหลือ 1 bit/sign
3. ใช้ **unbiased estimator** ที่คำนวณร่วมกันระหว่าง query แบบ precision สูงกับข้อมูลที่บีบอัดแล้ว
4. ผลลัพธ์คือ **ค่าประมาณ inner product ที่ไม่มีอคติ** หมายถึงค่าเฉลี่ยของค่าประมาณตรงกับค่าจริง

> **Companion paper:** QJL (Quantized JL) — AAAI 2025

---

## 🧮 การคำนวณ Step-by-Step (เจาะลึก)

> ส่วนนี้ใช้ตัวอย่างและโค้ดเชิงแนวคิดอธิบายขั้นตอนการคำนวณ สำหรับอ่านประกอบงานวิจัยก่อนพัฒนา implementation จริง

### ขั้นตอนที่ 1: Random Rotation (Pre-conditioning)

**เป้าหมาย:** แปลง vector ให้มีการกระจายที่อธิบายได้ทางคณิตศาสตร์

**คุณสมบัติสำคัญ 2 ข้อ (จาก Gaussian random variables):**
1. **Fact 1:** คูณ vector ใดๆ ด้วย random matrix ที่มี entries แจกแจงแบบ Gaussian → ผลลัพธ์เป็น multivariate Gaussian centered at zero
   $$S \cdot x \sim \mathcal{N}(0, \|x\|^2 \cdot I_m)$$
2. **Fact 2:** ความยาวของ Gaussian vector ในมิติสูงจะ **กระจุกตัว** ใกล้ $\sqrt{d}$
   $$f_R(r) = \frac{2}{2^{d/2} \cdot \Gamma(d/2)} r^{d-1} \exp(-r^2/2)$$

**วิธีทำ:**
```python
import numpy as np

# สร้าง random rotation matrix
G = np.random.randn(d, d)        # d = head dimension (เช่น 128)
Pi, _ = np.linalg.qr(G)          # QR decomposition → orthogonal matrix

# Pre-condition: rotate vector
y = Pi @ x                        # x = KV cache vector (d-dimensional)
# ตอนนี้ y ~ N(0, σ²) ทุก coordinate
```

> **สำคัญ:** Matrix `Pi` สร้างครั้งเดียว → reuse ทุกครั้ง ไม่ต้องสร้างใหม่

---

### ขั้นตอนที่ 2: Recursive Polar Transform

**เป้าหมาย:** แปลง vector จำนวน d มิติให้เป็นรัศมีสุดท้าย 1 ค่า และชุดมุมที่มีการกระจายแบบกระจุกตัว

**หลักการ:** จับคู่ coordinates แล้วแปลงเป็นพิกัดเชิงขั้ว เก็บค่ามุมไว้ และนำรัศมีที่ได้ไปคำนวณในรอบถัดไป

```
ตัวอย่าง d=8:

Level 0 (raw coordinates):  [x₁, x₂, x₃, x₄, x₅, x₆, x₇, x₈]
                               ↕    ↕    ↕    ↕    ↕    ↕    ↕    ↕
จับคู่:                       (x₁,x₂) (x₃,x₄) (x₅,x₆) (x₇,x₈)
                               ↕       ↕       ↕       ↕
แปลง polar:              (r₁,θ₁) (r₂,θ₂) (r₃,θ₃) (r₄,θ₄)
                           ↕       ↕       ↕       ↕
เก็บ:                   θ₁      θ₂      θ₃      θ₄   → angles[0] (4 angles)

Level 1 (radii):          [r₁, r₂, r₃, r₄]
จับคู่:                   (r₁,r₂)  (r₃,r₄)
แปลง polar:              (R₁,ψ₁)  (R₂,ψ₂)
เก็บ:                   ψ₁      ψ₂               → angles[1] (2 angles)

Level 2 (radii):          [R₁, R₂]
จับคู่:                   (R₁,R₂)
แปลง polar:              (R_final, ψ_final)
เก็บ:                   ψ_final                   → angles[2] (1 angle)

ผลลัพธ์: R_final + angles[0..2]
```

**Code:**
```python
def polar_transform(y):
    r = y.clone()
    angles = []
    n_levels = int(np.log2(len(y)))

    for level in range(n_levels):
        a = r[0::2]   # even indices
        b = r[1::2]   # odd indices

        # คำนวณ angle: ψ = atan2(b, a)
        level_angles = torch.atan2(b, a)

        if level == 0:
            # Level 1: coordinates อาจติดลบ → [0, 2π)
            level_angles = level_angles % (2 * np.pi)
        # Level 2+: radii เป็นบวกเสมอ → [0, π/2]

        # คำนวณ radius ใหม่: R = √(a² + b²)
        new_r = torch.sqrt(a**2 + b**2)

        angles.append(level_angles)
        r = new_r   # carry radii ไป level ต่อไป

    return angles, r  # angles[0..log₂d-1], R_final
```

---

### ขั้นตอนที่ 3: ทำไม Angle ถึง Concentrate?

แนวคิดสำคัญของ PolarQuant คือ:

**Level 1:** มุมกระจายอย่างสม่ำเสมอบน $[0, 2\pi)$ จึงต้องใช้หลายบิตเพื่อแทนช่วงค่าที่กว้าง

**Level 2+:** แต่ละ radius เป็น norm ของ sub-vector ที่ยาวขึ้นเรื่อยๆ:

| Level | แต่ละ radius สรุปกี่ coordinates | Angle range | Distribution |
| :--- | :--- | :--- | :--- |
| 1 | 2 | $[0, 2\pi)$ | Uniform (กว้าง) |
| 2 | 4 | $[0, \pi/2]$ | $\sin^{1}(2\theta)$ (เริ่มกระจุก) |
| 3 | 8 | $[0, \pi/2]$ | $\sin^{3}(2\theta)$ (กระจุกมาก) |
| 4 | 16 | $[0, \pi/2]$ | $\sin^{7}(2\theta)$ (แน่นมาก) |
| 7 (d=128) | 128 | $[0, \pi/2]$ | กระจุกในช่วงแคบรอบ $\pi/4$ → **1 bit พอ!** |

**สูตร PDF ของ angle ที่ level $\ell$:**

$$f_{\psi^{(\ell)}}(\psi) = \frac{\Gamma(2^\ell - 1)}{2^{2^{\ell-1}-2} \cdot \Gamma(2^\ell - 2)^2} \sin^{(2^{\ell-1}-1)}(2\psi)$$

**Intuition:**
- Level สูงขึ้น → radius เป็น norm ของ sub-vector ที่ยาวขึ้น
- Fact 2 บอกว่า norm ของ vector ยาวๆ ใน high dimension concentrate แน่นมากรอบ $\sqrt{d}$
- ดังนั้น $r_1 \approx r_2$ เกือบตลอด → $\arctan(r_2/r_1) \approx \pi/4$
- ยิ่ง level สูง angle ยิ่งไปรวมตัวแน่นรอบ $\pi/4$

---

### ขั้นตอนที่ 4: สร้าง Codebook (Lloyd-Max Quantizer)

**เป้าหมาย:** สร้าง lookup table ของ quantization buckets ที่เหมาะสมที่สุดสำหรับแต่ละ level

เมื่อทราบการกระจายของมุมในแต่ละ level ล่วงหน้า จึงสร้าง codebook แบบ **offline ไว้ครั้งเดียว** ได้

```python
def build_codebook(n_bits, lo, hi, level):
    n_codes = 2 ** n_bits          # จำนวน buckets
    n_grid = 10000
    theta = torch.linspace(lo, hi, n_grid)

    # 1. คำนวณ PDF ของ angle ที่ level นี้
    exponent = (1 << level) - 1     # 2^(ℓ-1) - 1
    sin2theta = torch.sin(2 * theta)
    pdf = torch.pow(sin2theta.clamp(min=0), exponent)

    # 2. แปลงเป็น CDF
    weights = pdf / pdf.sum()
    cdf = torch.cumsum(weights, dim=0)

    # 3. หา centroids ด้วย inverse CDF (Lloyd-Max)
    centroids = torch.zeros(n_codes)
    for i in range(n_codes):
        target = (i + 0.5) / n_codes   # จุดกลางของแต่ละ bucket
        idx = torch.searchsorted(cdf, target)
        centroids[i] = theta[idx]

    return centroids
```

**ตัวอย่างการจัดสรร bits:**

```python
codebooks = [
    build_codebook(n_bits=4, lo=0, hi=2*np.pi, level=0),  # Level 1: 16 entries
    build_codebook(n_bits=2, lo=0, hi=np.pi/2, level=1),   # Level 2: 4 entries
    build_codebook(n_bits=2, lo=0, hi=np.pi/2, level=2),   # Level 3: 4 entries
    build_codebook(n_bits=2, lo=0, hi=np.pi/2, level=3),   # Level 4: 4 entries
]
```

> **Level 1** ใช้ 4 bits (16 buckets) เพราะ angle ยังกว้าง | **Level 2+** ใช้แค่ 2 bits (4 buckets) เพราะ angle กระจุกแล้ว

---

### ขั้นตอนที่ 5: Quantize (บีบอัด)

```python
def quantize(angles, codebooks):
    indices = []
    for level, level_angles in enumerate(angles):
        # หา bucket ที่ใกล้ที่สุดสำหรับแต่ละ angle
        cb = codebooks[level]
        diffs = torch.cdist(level_angles.unsqueeze(1), cb.unsqueeze(1))
        idx = diffs.argmin(dim=1)
        indices.append(idx)
    return indices   # ส่งเก็บแทน angles จริง (ประหยัด bits มาก)
```

**ตัวอย่างการคำนวณพื้นที่ที่ประหยัดได้:**

d=128 → 7 levels
- Level 1: 64 angles × 4 bits = 256 bits
- Level 2: 32 angles × 2 bits = 64 bits
- Level 3: 16 angles × 2 bits = 32 bits
- Level 4: 8 angles × 2 bits = 16 bits
- Level 5: 4 angles × 2 bits = 8 bits
- Level 6: 2 angles × 2 bits = 4 bits
- Level 7: 1 angle × 2 bits = 2 bits
- R_final: 1 FP16 = 16 bits
- **รวม: 398 bits** vs **128 × 16 = 2048 bits (FP16)** → **~5.1x compression**

---

### ขั้นตอนที่ 6: Dequantize (กู้คืน)

```python
def dequantize(indices, codebooks, R_final, Pi):
    # 1. กู้คืน angles จาก codebook
    angles = []
    for level, level_indices in enumerate(indices):
        level_angles = codebooks[level][level_indices]
        angles.append(level_angles)

    # 2. Inverse polar transform
    r = R_final
    for level in reversed(range(len(angles))):
        level_angles = angles[level]
        half = len(level_angles)
        # สร้างใหม่จาก (r, θ) → (a, b)
        a = r * torch.cos(level_angles)    # even indices
        b = r * torch.sin(level_angles)    # odd indices
        # Interleave a, b
        r = torch.stack([a, b], dim=-1).flatten()

    # 3. Inverse rotation
    x_hat = Pi.T @ r   # คูณด้วย transpose
    return x_hat
```

---

### ขั้นตอนที่ 7: QJL — 1-bit Residual Correction

Stage 1 (PolarQuant) ลดความคลาดเคลื่อนแบบ MSE แต่ยังมี **อคติในการประมาณ inner product** ซึ่งส่งผลต่อ attention scores

**ทำไมมี bias?**
- MSE-optimal quantizer ลด $\|x - \hat{x}\|^2$ → แต่ไม่ได้รับประกันว่า $\langle y, \hat{x} \rangle \approx \langle y, x \rangle$
- Attention = inner product (Q·Kᵀ) → bias ตรงนี้ส่งผลตรงๆ

**QJL แก้ปัญหา:**

```python
# 1. คำนวณ residual
residual = x - x_hat   # ส่วนที่หายไปจาก quantization

# 2. สร้าง random projection matrix S
S = np.random.randn(m, d)   # m << d (เช่น m = 32)

# 3. Project + quantize เหลือ 1 bit
projected = S @ residual
sign_bits = np.sign(projected)   # +1 หรือ -1 เท่านั้น (1 bit)

# 4. Unbiased estimator
# เวลาคำนวณ attention score:
score_hat = <y, x_hat> + (1/m) * <sign(S@y), sign_bits>
# ค่า expectation ของ correction term = <y, residual>
# ดังนั้น E[score_hat] = <y, x> พอดี! (unbiased)
```

**ทำไมใช้แค่ 1 bit?**
- Johnson-Lindenstrauss lemma: random projection ในมิติสูงจะ **preserve inner products** ได้ดี
- แม้ quantize เหลือ 1 bit (sign) ก็ยัง preserve unbiasedness
- Overhead: เพียง $m$ bits (เช่น 32 bits) vs ประหยัดได้หลายร้อย bits → คุ้มมาก

---

### สรุป Pipeline ทั้งหมด

```
┌──────────────────────────────────────────────────────────────┐
│                    ENCODE (Quantize)                         │
│                                                              │
│  x (d-dim FP16)                                             │
│    │                                                         │
│    ├─① Random Rotate: y = Π · x                              │
│    │   (Π = pre-computed orthogonal matrix)                   │
│    │                                                         │
│    ├─② Polar Transform: y → angles[] + R_final              │
│    │   (recursive log₂d levels)                              │
│    │                                                         │
│    ├─③ Quantize angles: index[level] → codebook[level]       │
│    │   (Lloyd-Max, pre-computed per level)                    │
│    │                                                         │
│    └─④ QJL residual: sign(S · (x - x̂)) → 1-bit codes       │
│                                                              │
│  Output: indices + R_final + sign_bits                       │
│  Size: ~3-3.5 bits/channel vs 16 bits/channel (FP16)        │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    DECODE (Attention)                        │
│                                                              │
│  indices + R_final + sign_bits                               │
│    │                                                         │
│    ├─⑤ Lookup codebook → reconstruct angles                  │
│    │                                                         │
│    ├─⑥ Inverse polar transform → ŷ                          │
│    │                                                         │
│    ├─⑦ Inverse rotation: x̂ = Πᵀ · ŷ                        │
│    │                                                         │
│    └─⑧ QJL correction: score = ⟨q,x̂⟩ + QJL_correction     │
│       → Unbiased attention score!                            │
└──────────────────────────────────────────────────────────────┘
```

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
- ผล: ให้ recall สูงกว่า product quantization ที่ใช้เปรียบเทียบ
- **Indexing time → virtually zero** (vs PQ ที่ต้อง train codebook)

### Mathematical Optimality

$$\text{TurboQuant distortion} \approx 2.7 \times \text{Shannon's lower bound}$$

พิสูจน์โดยใช้:
- **Shannon's lower bound** สำหรับ information-theoretic limit
- **Yao's minimax principle** สำหรับ randomized algorithms
- ผล: ความคลาดเคลื่อนของ TurboQuant ใกล้ค่าต่ำสุดทางทฤษฎี โดยต่างกันเป็นสัดส่วนคงที่ ≈ 2.7

---

## 💥 Impact

### สำหรับ AI Infrastructure
- **ลดพื้นที่เก็บ KV cache 6x** เพื่อรองรับผู้ใช้เพิ่มขึ้นบน hardware เดิม
- **ลดต้นทุน inference** ได้อย่างมีนัยสำคัญ
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
- [[Speculative Sampling]] — อีกเทคนิคหนึ่งที่ช่วยเร่ง LLM inference

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

TurboQuant เป็น **อัลกอริทึมบีบอัด KV cache ที่ให้ความคลาดเคลื่อนใกล้ค่าต่ำสุดทางทฤษฎี** บทความนี้สรุปเป็นกระบวนการ 2 ส่วน:

1. **PolarQuant** → random rotate + scalar quantize → compression หลัก, zero overhead
2. **QJL** → 1-bit residual correction → eliminate inner product bias

ผลที่รายงานคือ **ลดพื้นที่เก็บ KV cache ได้ถึง 6x และรักษาคุณภาพในงานที่ทดสอบ โดยไม่ต้องฝึกโมเดลใหม่**

แนวทางนี้ช่วยลดต้นทุน เพิ่มจำนวนคำขอที่รองรับ และเผื่อพื้นที่ให้ context ยาวขึ้นได้บน GPU เดิม โดยต้องตรวจทั้งคุณภาพและประสิทธิภาพกับงานที่จะนำไปใช้
