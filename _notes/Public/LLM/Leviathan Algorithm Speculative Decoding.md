---
title: "Leviathan Algorithm: Speculative Decoding with Rejection Sampling"
notetype: feed
date: 2026-05-09
last_modified: 2026-05-09
tags: [llm, speculative-decoding, inference, rejection-sampling, probability, google]
status: published
---

# Leviathan Algorithm: Speculative Decoding

> Algorithm จาก Google (2022) ที่เร่ง LLM inference 2-3× โดย **output quality เหมือนเดิมเป๊ะ** — mathematically proven distribution-preserving

## Paper

- **"Fast Inference from Transformers via Speculative Decoding"**
- Authors: Yaniv Leviathan, Matan Kalman, Yossi Matias (Google)
- Published: November 2022
- [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)
- Demo: 2-3× speedup บน T5-XXL โดย output identical

## ปัญหาที่แก้

LLM generate text ทีละ token → **ช้า** เพราะ:

```
Step 1: model(input) → token₁     (~30ms)
Step 2: model(input + token₁) → token₂  (~30ms)
Step 3: model(input + token₁₂) → token₃ (~30ms)
...
K tokens = K × 30ms (serial, ไม่มีทาง parallelize)
```

**Key insight:** "งานยากส่วนใหญ่มีงานย่อยที่ง่ายกว่า ซึ่ง model เล็กทำได้ดีพอสมควร"

## แนวคิดหลัก

```
ใช้ model เล็ก (draft/fast) ทาย token ล่วงหน้าหลายตัว
→ ส่งให้ model ใหญ่ (target) ตรวจทีเดียว (parallel)
→ ถ้าถูก = ประหยัดเวลา
→ ถ้าผิด = แก้ด้วย residual sampling (output ยังเหมือน target เป๊ะ)
```

## Algorithm ทีละขั้นตอน

### Pseudocode

```
Input:  Target model p(x), Draft model q(x), Prefix x<t, Budget γ
Output: Token ที่ sample จาก p(x) เป๊ะ

───────────────────────────────────────────────────
STEP 1: DRAFT — Model เล็กทาย γ tokens
───────────────────────────────────────────────────
For i = 1 to γ:
    x̃ᵢ ~ q(x | x<t, x̃₁, ..., x̃ᵢ₋₁)
    // Draft model generate token ทีละตัว (เร็ว ~3ms/ตัว)

───────────────────────────────────────────────────
STEP 2: VERIFY — Model ใหญ่ตรวจทุก position พร้อมกัน
───────────────────────────────────────────────────
Run p(x) on [x<t, x̃₁, x̃₂, ..., x̃γ]
→ ได้ p(x) สำหรับทุก position (ทำ 1 forward pass)

───────────────────────────────────────────────────
STEP 3: ACCEPT/REJECT — Rejection sampling
───────────────────────────────────────────────────
For i = 1 to γ:
    r = Uniform(0, 1)   // สุ่มเลข 0-1
    
    If r < min(1, p(x̃ᵢ) / q(x̃ᵢ)):
        ✅ ACCEPT x̃ᵢ
        Continue to next token
    
    Else:
        ❌ REJECT at position i
        Sample x_new from residual: Normalize(max(0, p(x) - q(x)))
        Return: x<t, x̃₁, ..., x̃ᵢ₋₁, x_new
        STOP

───────────────────────────────────────────────────
STEP 4: BONUS TOKEN — ถ้า accept หมดทุกตัว
───────────────────────────────────────────────────
If all γ tokens accepted:
    bonus = sample from p(x at position γ+1)
    // Logit มีอยู่แล้วจาก Step 2 → ฟรี!
    Return: x<t, x̃₁, ..., x̃γ, bonus
```

## ตัวอย่าง Concrete

### Input: "The cat sat on"

```
Target model (7B): ช้า 30ms/step, แม่น
Draft model (100M): เร็ว 3ms/step, พอใช้
γ = 4 (draft 4 tokens)
```

### Step 1: Draft

```
Draft model generates:
  x̃₁ = "the"   q = 0.45
  x̃₂ = "mat"   q = 0.30
  x̃₃ = "and"   q = 0.25
  x̃₄ = "looked" q = 0.15
```

### Step 2: Verify

```
Target model run 1 forward pass on "The cat sat on the mat and looked"
→ ได้ p(x) สำหรับทุก position:

Position 1: p("the")  = 0.50
Position 2: p("mat")  = 0.20
Position 3: p("and")  = 0.30
Position 4: p("looked") = 0.05
```

### Step 3: Accept/Reject

```
Token 1: "the"
  p/q = 0.50/0.45 = 1.11 → min(1, 1.11) = 1.0
  r = 0.7 < 1.0 → ✅ ACCEPT

Token 2: "mat"
  p/q = 0.20/0.30 = 0.67
  r = 0.5 < 0.67 → ✅ ACCEPT (โชคดี)

Token 3: "and"
  p/q = 0.30/0.25 = 1.20 → min(1, 1.20) = 1.0
  r = 0.3 < 1.0 → ✅ ACCEPT

Token 4: "looked"
  p/q = 0.05/0.15 = 0.33
  r = 0.8 > 0.33 → ❌ REJECT!
  → Sample from residual: max(0, p-q)
  → p("floor") = 0.25, q("floor") = 0.05 → residual = 0.20
  → p("couch") = 0.20, q("couch") = 0.03 → residual = 0.17
  → Normalize & sample → เลือก "floor"
```

### Result

```
Output: "The cat sat on the mat and floor"
→ 3 tokens accepted + 1 corrected = 4 tokens จาก 1 target forward pass

Time:  4 × 3ms (draft) + 1 × 30ms (verify) = 42ms
vs AR: 4 × 30ms = 120ms
→ Speedup: 2.86×
```

## p/q Ratio หมายถึงอะไร

```
p(x) = target model probability (model ใหญ่ "อยาก" token นี้แค่ไหน)
q(x) = draft model probability (model เล็ก "อยาก" token นี้แค่ไหน)

p/q > 1 → Target เห็นด้วยมากกว่า draft → ACCEPT แน่นอน
p/q = 1 → เห็นตรงกัน → ACCEPT แน่นอน
p/q < 1 → Target ไม่เห็นด้วยเท่า draft → ACCEPT ด้วย probability p/q
p/q ≈ 0 → Target ไม่เห็นด้วยเลย → REJECT แทบแน่นอน
```

**Intuition:** ถ้า draft model ทายแม่น (q ≈ p) → p/q ≈ 1 → accept บ่อย → speedup มาก

## Residual Distribution (ทำไม output ไม่เบ้)

เมื่อ reject → ต้องเลือก token ใหม่ให้ **distribution ยังตรงกับ target**

$$\text{residual}(x) = \max(0,\ p(x) - q(x))$$

$$x_{\text{new}} \sim \frac{\text{residual}(x)}{\sum_x \text{residual}(x)}$$

### ตัวอย่างคำนวณ

```
Vocab = {A, B, C, D}

Token  p(x)  q(x)  p-q    residual
A      0.50  0.30  +0.20   0.20  ← target อยากมากกว่า draft
B      0.20  0.40  -0.20   0.00  ← draft อยากมากกว่า → ไม่ต้องชดเชย
C      0.15  0.15   0.00   0.00
D      0.15  0.15   0.00   0.00

Sum of residual = 0.20
P(new = A) = 0.20/0.20 = 100%
→ เลือก A เสมอเมื่อ reject ในกรณีนี้
```

### Proof ว่า output ไม่เบ้

$$P(\text{output} = x) = P(\text{accept}) \cdot q(x) + P(\text{reject}) \cdot \frac{\max(0, p(x)-q(x))}{\sum \max(0, p-q)} = p(x)$$

ทุก token มีโอกาสถูกเลือกเท่ากับ target model distribution **เป๊ะ** — ไม่มี approximation

## Bonus Token

ถ้า draft tokens ทั้ง γ ตัวถูก accept → ได้ **+1 token ฟรี**

```
ทำไมฟรี?
  Verify phase รัน target model บน [prefix + γ draft tokens]
  → Forward pass คำนวณ logits ทุก position รวมถึง position γ+1
  → Logit มีอยู่แล้ว → sample ได้เลยไม่ต้องคำนวณเพิ่ม

ผล:
  γ=5, accept หมด → ได้ 6 tokens จาก 1 verify
  → Throughput เพิ่ม 1/γ = 20%
```

## Speedup Analysis

### เมื่อไรจะเร็วกว่า autoregressive

$$\text{Speedup} = \frac{\text{time}_{AR}}{\text{time}_{spec}} = \frac{\gamma \cdot T_{target}}{T_{draft} + T_{verify}}$$

Break-even: เมื่อ acceptance rate เพียงพอ

$$\text{acceptance\_rate} > \frac{T_{target}}{T_{target} + T_{draft}}$$

### ตัวอย่าง

```
Target: 30ms/step, Draft: 3ms/step, γ=5

ถ้า acceptance rate = 90%:
  Average accepted = 0.9 + 0.9² + 0.9³ + 0.9⁴ + 0.9⁵ ≈ 3.7 tokens
  + bonus ถ้า accept หมด = 0.9⁵ ≈ 0.59 extra
  Total ≈ 4.3 tokens per cycle
  Time = 5×3ms + 30ms = 45ms
  vs AR: 4.3 × 30ms = 129ms
  → Speedup: 2.87×

ถ้า acceptance rate = 50%:
  Average accepted ≈ 0.97 tokens + bonus ≈ 0.03
  Total ≈ 1.0 tokens per cycle
  Time = 5×3ms + 30ms = 45ms
  vs AR: 1.0 × 30ms = 30ms
  → SLOWER than AR! (1.5× ช้าลง)
```

### Acceptance Rate vs Speedup

| Acceptance Rate | Avg Accepted | Speedup |
|----------------|-------------|---------|
| 95% | ~4.3 + 0.77 bonus | **3.4×** |
| 90% | ~3.7 + 0.59 bonus | **2.9×** |
| 80% | ~2.5 + 0.33 bonus | **2.1×** |
| 70% | ~1.7 + 0.17 bonus | **1.5×** |
| 60% | ~1.1 + 0.08 bonus | **1.0×** (break-even) |
| 50% | ~0.97 + 0.03 bonus | **0.7×** (ช้าลง!) |

## Implementation Notes

### ใน Rust

```rust
fn leviathan_verify(
    draft_tokens: &[TokenId],
    draft_probs: &[Vec<f32>],     // q(x) สำหรับแต่ละ position
    target_probs: &[Vec<f32>],    // p(x) จาก target model
    rng: &mut impl Rng,
) -> LeviathanResult {
    let mut accepted = Vec::new();
    
    for i in 0..draft_tokens.len() {
        let token = draft_tokens[i];
        let p = target_probs[i][token];  // target probability
        let q = draft_probs[i][token];   // draft probability
        
        let accept_prob = (p / q).min(1.0);
        let r: f64 = rng.gen();          // uniform [0, 1)
        
        if r < accept_prob {
            accepted.push(token);
        } else {
            // REJECT → sample from residual distribution
            let residual: Vec<f32> = target_probs[i].iter()
                .zip(draft_probs[i].iter())
                .map(|(&p, &q)| (p - q).max(0.0))
                .collect();
            let replacement = sample_from_distribution(&residual, rng);
            accepted.push(replacement);
            return LeviathanResult { accepted, rejected_at: Some(i) };
        }
    }
    
    // All accepted → bonus token from target p(x) at position γ
    let bonus = sample_from_distribution(&target_probs.last().unwrap(), rng);
    accepted.push(bonus);
    
    LeviathanResult { accepted, rejected_at: None }
}
```

### Numerical Stability

```
⚠️ ทำใน log-space เพื่อความแม่นยำ:

log(p/q) = log_p - log_q

ถ้า log_p - log_q > 0 → accept แน่นอน
ถ้า log_p - log_q ≤ 0 → accept with probability exp(log_p - log_q)

Residual ใน log-space:
log_residual = log(max(0, exp(log_p) - exp(log_q)))
→ ใช้ logsumexp trick เพื่อความเสถียร
```

## ใครใช้แล้ว

| System | Status | Notes |
|--------|--------|-------|
| **Google T5X** | Production | Original paper demo |
| **vLLM** | Production | `--speculative-decoding` flag |
| **HuggingFace TGI** | Production | Built-in speculative decoding |
| **TensorRT-LLM** | Production | NVIDIA optimized |
| **llama.cpp** | Experimental | Draft model support |
| **chimere** | Dev | Rust MoE inference runtime |

## Limitations

1. **ต้องการ model asymmetry มาก** — Draft model ต้องเล็กกว่า target 10× ขึ้นไปจึงคุ้ม
2. **Acceptance rate ต่ำ = ช้าลง** — ถ้า draft ไม่แม่น → overhead เกินประโยชน์
3. **Memory สำหรับ 2 models** — ต้อง load draft + target พร้อมกัน
4. **Distribution matching ไม่แม่นถ้าคำนวณ float ไม่ระวัง** — Need log-space operations

## ความสัมพันธ์กับ Methods อื่น

```
Speculative Decoding Family Tree:

Leviathan (2022) ─── Linear Draft + Rejection Sampling
    │
    ├── SpecInfer (2023) ─── Tree Verification
    │
    ├── Medusa (2024) ─── Multiple Heads (no separate draft model)
    │
    ├── EAGLE (2024) ─── Feature-level Drafting
    │   └── EAGLE-2 (2024) ─── Dynamic Draft Tree
    │
    └── DDTree ─── Best-First Search Tree
```

## Papers ที่เกี่ยวข้อง

- **Leviathan et al. 2022** — [arXiv:2211.17192](https://arxiv.org/abs/2211.17192): Original speculative decoding
- **Chen et al. 2023** — [arXiv:2305.09781](https://arxiv.org/abs/2305.09781): SpecInfer tree-based verification
- **Cai et al. 2024** — [arXiv:2401.10774](https://arxiv.org/abs/2401.10774): Medusa multi-head decoding
- **Li et al. 2024** — [arXiv:2401.15077](https://arxiv.org/abs/2401.15077): EAGLE feature-level speculative sampling
- **Li et al. 2024** — [arXiv:2406.16858](https://arxiv.org/abs/2406.16858): EAGLE-2 dynamic draft trees

---

*Leviathan Algorithm = ใช้ rejection sampling เพื่อรับประกันว่า output ตรงกับ target model เป๊ะ โดยใช้ draft model เร่งความเร็ว. กุญแจสำคัญคือ residual distribution ที่ชดเชยส่วนต่างระหว่าง p และ q ให้ output ไม่เบ้*
