---
title: "GSQ: Gumbel-Softmax Quantization บีบอัดน้ำหนัก LLM ให้แม่นยำในบิตต่ำ"
notetype: feed
date: 2026-10-28
last_modified: 2026-10-28
tags: [GSQ, Gumbel-Softmax, quantization, LLM, model-compression, low-precision, PTQ]
status: published
permalink: /notes/gsq-gumbel-softmax-quantization
---

<link rel="stylesheet" href="/assets/css/quantization-articles.css">
<div class="quantization-article" markdown="1">

> **ขอบเขตและที่มา:** บทความนี้อธิบายงาน *GSQ: Highly-Accurate Low-Precision Scalar Quantization for LLMs via Gumbel-Softmax Sampling* โดย Alireza Dadgarnia และคณะ อ้างอิง paper **arXiv:2604.18556v2** และโค้ดของผู้วิจัยที่ตรวจเมื่อ **28 ตุลาคม 2026** ตัวเลข benchmark เป็น **ผลที่ผู้วิจัยรายงาน** ไม่ใช่ผลทดสอบ LLM ของผู้เขียน ส่วนตัวอย่าง Python ด้านล่างเป็น **การสาธิตขนาดเล็กที่รันจริงบน CPU** ไม่ใช่การทำซ้ำ pipeline ทั้ง paper.[1][2]

## TL;DR

- **GSQ เป็นวิธี post-training weight quantization**: เริ่มจากโมเดลที่ฝึกแล้ว แล้วเรียนรู้ว่าจะจับน้ำหนักแต่ละตัวลงจุดใดบน quantization grid พร้อมปรับ scale ของแต่ละกลุ่ม ไม่ใช่การฝึก LLM ใหม่จากศูนย์.[1]
- จุดสำคัญไม่ใช่ “มีค่าให้เลือกมากขึ้น” แต่คือ **เลือกค่าจากชุดเดิมให้เหมาะกับ output ของโมเดลมากขึ้น** โดยใช้ Gumbel-Softmax ทำให้การเลือกแบบไม่ต่อเนื่องมีตัวแทนที่คำนวณ gradient ได้.[1]
- ระหว่างปรับแต่งมี logits และ soft weights แต่ตอน export ต้องเหลือ **hard integer codes + scales** ไม่ต้องพก logits หรือสุ่ม Gumbel ระหว่าง inference.[1][12]
- Paper ครอบคลุม ternary, 2-bit และการเลื่อนไปยังจุดข้างเคียงสำหรับบิตสูงขึ้น ผลลัพธ์หลักยังเป็น scalar quantization ที่ออกแบบให้ใช้กับ kernel ที่รองรับรูปแบบนั้นได้.[1]
- “น้ำหนัก 2 บิต” ไม่เท่ากับ “ไฟล์ทุกส่วนใช้ 2 บิตต่อพารามิเตอร์” และไม่เท่ากับ “VRAM ทั้งระบบลดตามสัดส่วนเดียวกัน” ต้องนับ scale, tensor ที่ไม่ quantize, packing และหน่วยความจำระหว่างรันด้วย.[1][2]

**อ่านต่อเรื่องการแบ่งงบระหว่าง layer:** [[RCO: Riemannian Constrained Optimization จัดสรรบิตภายใต้งบขนาดโมเดล]]

## 1. ปัญหาของการปัดน้ำหนัก: ใกล้ค่าเดิมที่สุด อาจไม่รักษา output ได้ดีที่สุด

สมมติว่า linear layer รับเวกเตอร์ $x$ แล้วคำนวณ

$$
y=Wx.
$$

การ quantize แบบง่ายอาจหาน้ำหนักใหม่ $\hat W$ โดยปัดแต่ละสมาชิกไปยังจุดที่ใกล้ที่สุด เช่น

$$
\hat w_i=s\,\operatorname{round}(w_i/s),
$$

แล้ว clip ให้อยู่ในช่วงของ integer grid การทำเช่นนี้สนใจความคลาดเคลื่อนของ **ตัวน้ำหนัก** แต่ข้อมูลจริงอาจมี feature ที่สัมพันธ์กันหรือบางทิศทางมีความสำคัญมากกว่าทิศทางอื่น GSQ จึงมองโจทย์เป็นการลด **ความคลาดเคลื่อนของ output บน calibration data** ไม่ใช่แค่ลดระยะห่างรายพิกัด.[1]

สำหรับ input ตัวอย่างหลายชุดที่วางเป็นคอลัมน์ของ $X$ ให้พิจารณา

$$
\mathcal L_{\mathrm{rec}}
=\|\hat WX-WX\|_F^2.
$$

เขียนใหม่ได้เป็น

$$
\mathcal L_{\mathrm{rec}}
=\operatorname{tr}\!\left[(\hat W-W)XX^T(\hat W-W)^T\right].
$$

**ข้อสังเกตจากสมการ:** $XX^T$ ทำให้ข้อผิดพลาดของน้ำหนักแต่ละพิกัดเชื่อมโยงกัน หาก feature สองตัวสัมพันธ์กัน การปรับน้ำหนักสองตัวร่วมกันอาจรักษาผลคูณกับ input ได้ดีกว่าการปัดแยกกัน ตัวอย่างในหัวข้อ 7 จะแสดงกรณีที่ weight MSE แย่ลง แต่ output MSE ดีขึ้นอย่างชัดเจน

ไม่ได้แปลว่า GPTQ เป็นเพียง round-to-nearest: GSQ ใช้ GPTQ เป็นจุดเริ่มต้นใน pipeline หลัก แล้วทำ discrete-assignment refinement ต่ออีกชั้น.[1]

## 2. แยก format ออกจากวิธีหาค่าที่จะเก็บ

ให้กลุ่มน้ำหนักหนึ่งกลุ่มมี scale $s$ และ integer grid $\mathcal G$ น้ำหนักที่ export จะอยู่ในรูป

$$
\hat w_i=sq_i,\qquad q_i\in\mathcal G.
$$

ตัวอย่าง 2-bit ใน paper ใช้

$$
\mathcal G_2=\{-2,-1,0,1\}.
$$

นี่คือชุด integer แบบ signed ที่มีสี่ระดับ ไม่ใช่การใช้สี่ค่าที่สมมาตรรอบศูนย์ในความหมายเชิงเรขาคณิตทุกจุด คำว่า symmetric quantization ในบริบทนี้หมายถึงการไม่มี learned zero-point แบบ asymmetric quantizer และ paper อนุญาตให้ scale เป็นลบได้ด้วย.[1]

สิ่งที่ GSQ เปลี่ยนคือ **การหาค่า $q_i$ และ $s$** ไม่ใช่บังคับให้ runtime ต้องตีความ categorical distribution ตลอดไป ผลลัพธ์หลังจบ optimization ยังคงส่งต่อเป็น grid assignments และ scales ได้.[1][12]

เปรียบเทียบให้เห็นระดับของโจทย์:

| ส่วน | คำถามที่ตอบ |
|---|---|
| Quantization format | มีค่าอะไรให้เก็บได้บ้าง และ pack บิตอย่างไร? |
| GSQ | ภายใต้ format นี้ ควรเลือก code และ scale ใด? |
| Mixed-precision allocation เช่น RCO | แต่ละ layer ควรใช้ format/bitwidth ใดภายใต้งบรวม? |
| Inference kernel | อ่านค่าที่ pack ไว้และคำนวณได้เร็วแค่ไหน? |

## 3. Gumbel-Softmax ทำให้การเลือกค่าบน grid เรียนรู้ได้อย่างไร

### 3.1 จาก hard assignment เป็น logits

แทนการเลือก $q_i$ ทันที ให้แต่ละน้ำหนักมี logits

$$
\ell_i=(\ell_{i1},\ldots,\ell_{iK}),
$$

โดย $K=\lvert\mathcal G\rvert$ และ $v_k$ คือค่าลำดับที่ $k$ บน grid ในกรณี 2-bit จึงมีสี่ logits ต่อหนึ่งน้ำหนัก ส่วน scale แชร์กันภายในกลุ่ม.[1]

### 3.2 เติม Gumbel noise แล้วทำ softmax

สุ่ม

$$
u_{ik}\sim\operatorname{Uniform}(0,1),
\qquad g_{ik}=-\log(-\log u_{ik}),
$$

แล้วคำนวณ soft assignment ในรูปแบบที่ implementation ใช้

$$
p_{ik}
=\frac{\exp\left((\kappa\ell_{ik}+g_{ik})/\tau\right)}
{\sum_j\exp\left((\kappa\ell_{ij}+g_{ij})/\tau\right)}.
$$

ที่นี่ $\tau>0$ คือ temperature และ $\kappa$ คือ logit multiplier ไม่ใช่ quantization scale $s$; โค้ดต้นฉบับมีตัวแปรชื่อ `scale` สำหรับ multiplier นี้ ขณะที่ group scales เก็บแยกกัน จึงต้องระวังชื่อที่ดูคล้ายกัน.[12]

ใช้ค่าเฉลี่ยแบบ soft มาประกอบน้ำหนักชั่วคราว

$$
\tilde q_i=\sum_k p_{ik}v_k,
\qquad \tilde w_i=s\tilde q_i.
$$

จากนั้นคำนวณ reconstruction loss ด้วย $\tilde W$ แล้ว backpropagate ไปยัง logits และ scales พร้อมกัน ระหว่างฝึก $\tilde q_i$ อาจเป็นค่าที่ **ไม่อยู่บน grid จริง** ได้ เพราะมันเป็นเพียงตัวแทนแบบต่อเนื่องสำหรับ optimization.[1]

### 3.3 ทำไมต้อง anneal และทำไมยังต้องตรวจ hard loss

เมื่อ temperature สูง distribution จะนุ่มกว่าและมี gradient ผ่านหลาย candidate เมื่อค่อย ๆ ลด temperature การเลือกจะใกล้ one-hot มากขึ้น แต่การมี soft loss ต่ำไม่ได้พิสูจน์ว่าการเลือกค่าเดียวหลัง export จะดีเท่ากัน.[1]

ตัวอย่างเชิงแนวคิด: หาก grid มีเพียง 0 กับ 1 แล้ว soft mixture เท่ากับ 0.49 ก็อาจ fit เป้าหมาย 0.49 ได้พอดี แต่ checkpoint ที่เก็บได้จริงต้องเลือก 0 หรือ 1 ดังนั้นควรประเมิน **hard reconstruction loss** ระหว่างปรับแต่งและหลัง export ด้วย

สุดท้ายเลือกแบบไม่มี Gumbel noise

$$
q_i^{\mathrm{hard}}=v_{\operatorname{argmax}_k\ell_{ik}},
\qquad \hat w_i=sq_i^{\mathrm{hard}}.
$$

โค้ด `get_hard_weights()` ของผู้วิจัยทำ argmax ของ logits แล้วคูณ scales จริง ไม่ได้ export probability vector.[12]

### 3.4 Gradient ที่ใช้ในตัวอย่าง CPU

เมื่อให้ $\kappa=1$ และตรึง noise ที่สุ่มใน forward pass ไว้ อนุพันธ์รายพิกัดคือ

$$
\frac{\partial\tilde w_i}{\partial\ell_{ik}}
=\frac{s}{\tau}p_{ik}(v_k-\tilde q_i).
$$

จึงคำนวณ gradient ของ toy linear layer ด้วย standard library ได้โดยไม่ต้องติดตั้ง PyTorch ในตัวอย่างที่แนบมา เราตรวจอนุพันธ์ทั้ง logits และ scale เทียบกับ central finite differences แล้ว ส่วนโค้ดต้นฉบับใช้ custom autograd และ replay RNG state เพื่อใช้ Gumbel sample เดิมใน backward.[12]

## 4. GSQ ไม่ได้มีแค่รูปแบบเดียว

### 4.1 Ternary: mask × sign × scale

สำหรับค่าที่เลือกได้ $\lbrace -s,0,s\rbrace$ paper เขียน

$$
\hat{\mathbf w}=s\,\mathbf m\odot\mathbf b,
\quad m_i\in\{0,1\},\quad b_i\in\{-1,+1\}.
$$

- mask กำหนดว่าจะเป็นศูนย์หรือไม่
- sign กำหนดเครื่องหมายของค่าที่ไม่เป็นศูนย์
- scale กำหนดขนาดของค่าทั้งกลุ่ม

GSQ จึงใช้ binary decisions สองชุด ไม่ใช่จำเป็นต้องใช้สาม logits แบบ categorical ตรง ๆ ในทุก implementation และการเริ่มจากค่า zero ยังเปิดทางให้เปลี่ยนเป็น nonzero ภายหลังได้.[1]

คำว่า “1.58-bit” มาจากอัตราเชิงข้อมูล $\log_2 3\approx1.58496$ บิตต่อ trit **ไม่ใช่หลักฐานว่าไฟล์จริงเก็บได้เท่านี้ทันที** หากเก็บ mask และ sign เป็นสอง bitplanes แบบตรงไปตรงมา ก็ยังใช้สองบิตต่อ weight ก่อนนับ scale ต้องมี packing ที่เหมาะสมจึงจะเข้าใกล้อัตราของ ternary ได้

### 4.2 2-bit: เรียนรู้ทั้งสี่จุด

แต่ละน้ำหนักมีสี่ logits สำหรับ $\lbrace -2,-1,0,1\rbrace$ เพราะจำนวน candidate ยังเล็ก จึงค้นการเลือกค่าภายใน grid ได้โดยตรง ในรูปแบบ group-wise จะมี scale ต่อกลุ่มแทน scale เดียวทั้งโมเดล.[1]

### 4.3 มากกว่า 2 บิต: local-shift แทน full-grid logits

หากเพิ่มจำนวนบิตแล้วใช้ logits ครบทุกจุด จำนวน auxiliary parameters จะโตตาม $2^b$ ผู้วิจัยจึงเริ่มจาก grid index ที่ GPTQ หาไว้ $j_i^0$ แล้วให้เลือกเพียง

$$
\delta_i\in\{-2,-1,0,1,2\},
\qquad
j_i=\operatorname{clip}(j_i^0+\delta_i,1,2^b).
$$

จึงมีห้า logits ต่อ coordinate แทนการมี logits สำหรับทั้ง grid เช่น 16 จุดที่ 4-bit นี่คือ **การจำกัดบริเวณค้นหาแถวจุดเริ่มต้น** ไม่ใช่การลด format ปลายทางให้เหลือเพียงห้าค่า.[1]

## 5. Pipeline จริง: มากกว่า softmax หนึ่งบรรทัด

Paper และ repository ประกอบด้วยขั้นตอนสำคัญต่อไปนี้.[1][2]

```text
pretrained model + calibration data
            ↓
GPTQ initialization: assignments + group scales
            ↓
initialize learnable logits around that solution
            ↓
optimize reconstruction with Gumbel-Softmax
  ├─ update assignments and scales jointly
  ├─ anneal temperature / logit multiplier
  └─ use layer, attention, block or expert objectives as appropriate
            ↓
freeze hard assignments
            ↓
optional final scale-only refinement in specified experiments
            ↓
pack codes + scales → verify quality and actual storage
```

ใน dense models ของ paper v2 มี within-block staging: เริ่ม query/key แยกกัน ตามด้วย value/output ร่วมกันภายใต้ attention reconstruction แล้วจึง MLP ภายใต้ block reconstruction แต่ละ block ที่เสร็จแล้วถูกตรึง และ block ถัดไปรับ input จาก prefix ที่ quantize ไปแล้ว.[1]

Paper ใช้ Lion เพื่อรับมือกับ gradient ที่เล็กลงเมื่อ categorical distribution อิ่มตัว และใช้ gradient accumulation ที่สุ่ม Gumbel ใหม่ในแต่ละ microbatch เพื่อช่วยลด sampling variance การแทนที่ทั้งหมดด้วย SGD ในตัวอย่างสอนจึงไม่ใช่การทำซ้ำสูตรฝึกของผู้วิจัย.[1]

**Calibration สำคัญ:** paper ใช้ FineWeb-Edu สำหรับ Llama และ OpenThoughts สำหรับ Kimi-K2.5 โดยงบหลักคือ 4096 sequences ความยาว 4096 tokens; Llama ทำ blockwise 20 epochs และ Kimi 10 epochs สำหรับ 2-bit Llama มี scale-only fine-tuning เพิ่มอีกหนึ่ง epoch.[1]

Post-training จึงหมายถึงเริ่มจาก pretrained weights ไม่ได้หมายถึงไม่ใช้ข้อมูล ไม่ทำ gradient optimization หรือไม่เสียเวลา GPU

## 6. “2 บิต” ประหยัดพื้นที่จริงเท่าไร

**ตัวอย่างบัญชีพื้นที่ ไม่ใช่ benchmark:** สมมติทุก 128 weights ใช้ scale FP16 หนึ่งค่า ไม่มี zero-point และยังไม่นับส่วนอื่น

$$
\operatorname{bpp}_{\mathrm{effective}}
=2+\frac{16}{128}=2.125.
$$

สำหรับ weights ที่เข้าเงื่อนไขจำนวน 8 พันล้านตัว พื้นที่เชิงอุดมคติคือ

$$
\frac{8\times10^9\times2.125}{8}
=2{,}125{,}000{,}000\text{ bytes}
=2.125\text{ GB}.
$$

และอัตราส่วนเทียบ BF16 คือ $16/2.125\approx7.53$ เท่า ตัวเลขนี้ **ไม่ใช่ขนาดไฟล์ Llama-3.1-8B จริง** เพราะจำนวนพารามิเตอร์จริง ขอบเขตที่ quantize และ overhead อาจต่างจากสมมติฐาน

สิ่งที่ต้องนับเพิ่มเมื่อ deploy ได้แก่

- embeddings, output head และ layer ที่คงความละเอียดเดิม
- scales/zero-points ตาม format ที่ใช้จริง
- padding, tensor alignment, packing container และ metadata
- KV cache, activations และ workspace สำหรับ **runtime memory** ซึ่งไม่ใช่ส่วนเดียวกับ checkpoint bytes

ตัวอย่างกับดักจาก repository: GSQ บาง path เก็บ 2-bit codes ใน `uint4` container ของ compressed-tensors แล้วจึงใช้ Humming converter repack เป็น effective 2-bit ดังนั้นอ่านแค่จำนวนระดับของ codebook ยังยืนยันขนาดไฟล์ไม่ได้.[2]

## 7. ตัวอย่างครบ: Gumbel-Softmax บน linear layer จิ๋ว

### 7.1 โจทย์และ baseline

กำหนด weights หนึ่งแถวเป็น

```text
W = [-0.9, 0.35]
initial scale = 0.5
grid = [-2, -1, 0, 1]
```

input ที่สร้างขึ้นสำหรับสาธิตคือ

```text
X rows = [ [1.0, 1.0], [1.0, 0.9], [1.1, 1.0],
           [2.0, 2.1], [-1.0, -1.0] ]
target per row = dot(W, row)
```

การปัดใกล้ที่สุดด้วย scale ตั้งต้นให้ codes `[-2, 1]` และ weights `[-1.0, 0.5]` เช่น input `[1, 1]` มี target `-0.55` แต่ baseline ให้ `-0.5` ข้อมูลชุดนี้มี feature ที่สัมพันธ์กัน จึงเปิดโอกาสให้การเลือก weights ร่วมกันเปลี่ยนผลลัพธ์ได้

### 7.2 ดาวน์โหลดและรัน

[ดาวน์โหลด gsq_demo.py](/assets/examples/quantization/gsq_demo.py) — ใช้ **Python 3 standard library เท่านั้น**, ไม่ต้องใช้ GPU, PyTorch, model download หรือ API key

```bash
python3 gsq_demo.py
```

หากเปิดจาก repository นี้:

```bash
python3 assets/examples/quantization/gsq_demo.py
python3 -m unittest discover -s tests -p 'test_quantization_examples.py' -v
```

ตัวอย่างทำ 3000 steps, เฉลี่ย gradient จาก Gumbel samples แปดชุดต่อ step, ใช้ seed 7, ลด temperature จาก 1.0 สู่ 0.05 และเรียนรู้ logits กับ scale ร่วมกัน โดยเลือก checkpoint ด้วย **hard calibration MSE** ไม่ใช่ soft training loss

โครงสำคัญของ loss ในไฟล์คือ

```python
probs = [softmax([(l + n) / temperature for l, n in zip(lr, nr)])
         for lr, nr in zip(logits, noise)]
means = [sum(p * q for p, q in zip(row, GRID)) for row in probs]
weights = [scale * q for q in means]
```

ตอนประเมิน hard weights ใช้

```python
codes = [GRID[max(range(len(GRID)), key=lambda k: row[k])]
         for row in logits]
hard_weights = [q * scale for q in codes]
```

### 7.3 ผลที่ได้จากการรันจริง

ย่อเฉพาะค่าหลักจาก JSON ที่สคริปต์พิมพ์:

```text
seed       = 7
rtn_codes  = [-2, 1]
rtn_mse    = 0.00421
codes      = [-2, 0]
scale      = 0.2752165279662071
weights    = [-0.5504330559324142, 0.0]
hard_mse   = 0.0007347016581720856
```

Output MSE ลดลงประมาณ **82.55% ในข้อมูลสาธิตชุดนี้** ขณะที่ weight MSE กลับเพิ่มจาก **0.01625** เป็นประมาณ **0.12235** จึงเห็นชัดว่า “น้ำหนักใกล้เดิม” กับ “output ใกล้เดิมบนข้อมูลชุดนี้” เป็นคนละเป้าหมาย

**อย่าแปลผลเกินขอบเขต:** ตัวอย่างนี้มีเพียงสอง weights ใช้ synthetic calibration ชุดเดิมในการเลือก hard checkpoint และไม่ได้วัด held-out generalization การที่น้ำหนักเปลี่ยนมากอาจทำให้ผลบน input distribution อื่นแย่ลงได้ จึงไม่ใช่หลักฐานว่า LLM จะดีขึ้น 82.55%

### 7.4 ต่างจาก GSQ จริงอย่างไร

| ตัวอย่างนี้ | Pipeline ในงานวิจัย |
|---|---|
| เริ่มจาก RTN | หลัก ๆ เริ่มจาก GPTQ |
| SGD แบบสั้นเพื่ออ่าน gradient ได้ | ใช้ Lion และ training recipe เฉพาะ |
| หนึ่ง linear output / หนึ่ง scale | กลุ่มน้ำหนักและ block/expert จำนวนมาก |
| สร้างข้อมูลเอง ไม่มี held-out | ใช้ calibration และ benchmark datasets |
| คืน hard weights เป็นตัวเลข Python | ต้อง export/pack และทดสอบ runtime จริง |

ส่วนที่ตัวอย่างตั้งใจพิสูจน์คือกลไก differentiable discrete selection, joint scale learning และความจำเป็นของ hard evaluation **ไม่ใช่** ความถูกต้องของระบบ LLM deployment ทั้งชุด

## 8. ผลวิจัย: ดูทั้ง accuracy และ bpp ไม่ใช่แค่คำว่า 2-bit

ตารางต่อไปนี้คัดค่าจาก Table 1 ของ paper v2 คะแนนเป็นค่าเฉลี่ย zero-shot ของ ARC-C, ARC-E, HellaSwag, PIQA และ Winogrande **ยิ่งสูงยิ่งดี** แต่ละแถวต้องอ่านคู่กับอัตราเก็บข้อมูลของตัวเอง.[1]

| วิธี | รายงาน bpp: 8B / 70B | Llama-3.1-8B-Instruct | Llama-3.1-70B-Instruct |
|---|---|---:|---:|
| FP16/BF16 | 16 / 16 | 73.71 | 78.99 |
| GPTQ | 2.25 / 2.25 | 37.53 | 57.38 |
| EfficientQAT | 2.25 / 2.25 | 63.79 | 71.43 |
| QTIP | 2.00 / 2.00 | 69.88 | 77.25 |
| PV-Tuning | 2.27 / 2.07 | 69.83 | 76.27 |
| GSQ | 2.13 / 2.13 | 68.55 | 75.57 |

GSQ สูงกว่า EfficientQAT **4.76 และ 4.14 percentage points** ในการเปรียบเทียบนี้ แต่ยังต่ำกว่า full precision และ QTIP ทั้งสองขนาด จึงควรกล่าวว่า **ลดช่องว่างระหว่าง scalar quantization กับวิธีที่ซับซ้อนกว่า** ไม่ใช่ “2 บิตไม่สูญเสียความแม่นยำ” หรือ “ชนะทุกวิธีที่ขนาดเท่ากัน”.[1]

ข้อจำกัดในการอ่านผล:

1. ทั้งตาราง **ไม่ได้มี footprint เท่ากันทุกแถว**
2. สำหรับ 8B มี down projection ของ block ที่สองที่ผู้วิจัยคง full precision เพราะไม่เสถียรเมื่อบีบอัดมาก
3. ผล 2-bit Llama ของ GSQ มี scale-only fine-tuning เพิ่มหลัง blockwise optimization
4. Calibration/training budget ของวิธีต่าง ๆ ไม่จำเป็นต้องเท่ากัน จึงไม่ใช่ pure optimizer-only ablation.[1]

สำหรับ Kimi-K2.5 paper quantize เฉพาะ non-shared experts และไม่ใช่ทุกองค์ประกอบของโมเดล คะแนน GPQA Diamond ใน Table 3 ลดจาก **89.29** เป็น **76.57** แม้บางงานคณิตศาสตร์หรือโค้ดจะดีขึ้น จึงไม่ควรใช้คำว่า “ใกล้ lossless ทุกความสามารถ” และควรทดสอบตามงานใช้งานจริง.[1]

## 9. ใช้จริงต้องตรวจอะไรบ้าง

### 9.1 Compatibility ไม่ได้เกิดจากชื่อ algorithm อย่างเดียว

Paper v2 มีการ refine Qwen3-8B GGUF K-Quant โดยเริ่มจาก checkpoint ที่มีอยู่ แล้ว project กลับสู่ **format เดิม** ซึ่งช่วยเรื่องการใช้กับ local-deployment stacks แต่ไม่ได้แปลว่าการแปลง GSQ output ใด ๆ ไปเป็น GGUF เป็นคำสั่งเดียวที่ใช้ได้กับทุกรุ่น.[1][2]

ก่อนใช้ checkpoint ให้ตรวจ

- model architecture และ layer ที่รองรับ
- group size, bitwidth และ symmetric/asymmetric scheme
- metadata และ packing layout ตรงกับ loader หรือไม่
- kernel รองรับ mixed precision ที่เลือกจริงหรือไม่
- ต้อง repack หรือ dequantize กลับเป็น BF16 ก่อนคำนวณหรือไม่

Repository มีข้อจำกัดเฉพาะ serving backend/GPU และ tensor-parallel shape ดังนั้น “เป็น scalar format” เป็นข้อได้เปรียบในการ integrate ไม่ใช่คำรับประกันว่าเครื่องทุกชนิดจะได้ acceleration โดยไม่ปรับอะไร.[2]

### 9.2 แยกความเร็วสามชนิด

- **เวลาทำ quantization**: เวลา GPU ที่ใช้สร้าง checkpoint
- **ความเร็ว kernel**: เวลาของ low-bit matrix multiplication
- **ความเร็ว serving ทั้งระบบ**: latency, throughput, batching, context length และ memory behavior

Paper รายงานผล vLLM/Humming บน L40s เป็น TPS/GPU ที่ normalize ข้าม tensor-parallel configurations การนำ speedup นั้นไปอ้างว่าเครื่องเดี่ยวทุกเครื่องจะเร็วขึ้นเท่ากันจึงไม่ถูกต้อง.[1]

### 9.3 Checklist ก่อนย้ายงานจริง

- เก็บ full-precision baseline ภายใต้ evaluation protocol เดียวกัน
- เลือก calibration ที่เป็นตัวแทนภาษา โดเมน และความยาว context ที่ใช้จริง
- ตรวจ hard weights หลัง export ไม่อาศัย soft loss อย่างเดียว
- ประเมิน held-out perplexity และ task metrics ที่ต้องรักษา โดยแยกจาก calibration
- วัดขนาดไฟล์จริง, VRAM ที่ peak, TTFT, TPOT และ throughput
- ตรวจความถูกต้องก่อนและหลัง repack โดยเทียบ logits หรือ output reconstruction
- หากคุณภาพตก ให้ลองเพิ่ม bits เฉพาะส่วนที่ไว แทนการบังคับทั้งโมเดลใช้ bitwidth เดียว

ข้อสุดท้ายเชื่อมกับ RCO: GSQ ทำให้ candidate quantized weights มีคุณภาพขึ้น ส่วนการแบ่งงบระหว่าง candidate เหล่านั้นเป็นโจทย์ allocation อีกระดับหนึ่ง.[1][3]

## 10. คำถามที่พบบ่อย

**GSQ เป็น PTQ แล้วทำไมมีการเรียนรู้?**
PTQ หมายถึงแปลงโมเดลที่ pretrained แล้ว ไม่ได้ห้าม gradient-based calibration ผู้วิจัย optimize quantization assignments และ scales แทนการฝึกโมเดลใหม่ทั้งหมด.[1]

**ต้องสุ่ม Gumbel ตอนตอบคำถามผู้ใช้หรือไม่?**
ไม่ต้อง หลัง export ใช้ hard codes และ scales ไม่ใช้ auxiliary logits ใน inference ปกติ.[12]

**GSQ เป็น vector quantization หรือไม่?**
วิธีหลักของงานนี้เป็น scalar quantization แต่ปรับ assignments ร่วมกันผ่าน reconstruction objective การ optimize ร่วมกันไม่ได้ทำให้ format กลายเป็น vector codebook โดยอัตโนมัติ.[1]

**2-bit weights ทำให้ activation และ KV cache เป็น 2-bit ด้วยหรือไม่?**
ไม่ใช่ขอบเขตของ weight-only recipe ที่อธิบายในบทความ ต้องเลือกวิธีและ kernel สำหรับ activation/KV cache แยกต่างหาก.[1]

**ใช้ GSQ กับ RCO ได้เลยหรือไม่?**
ในเชิงสถาปัตยกรรมสามารถมอง GSQ เป็นวิธีสร้าง candidate weights และ RCO เป็นตัวค้น allocation ได้ แต่ released RCO pipeline ที่ตรวจใช้ฐาน GPTQ เป็นหลัก ต้องเชื่อม candidate store, scales และ exporter ให้ตรงกันก่อน ไม่ควรอ้างว่า workflow สองโครงการนี้เชื่อมกันครบเพียงเพราะใช้ Gumbel เหมือนกัน.[2][4]

## สรุป

GSQ แสดงให้เห็นว่า low-bit scalar quantization ยังพัฒนาได้มากด้วย **การ optimize การเลือกค่าที่จะเก็บ** ไม่จำเป็นต้องเปลี่ยนไปใช้ representation ที่ซับซ้อนเสมอไป อย่างไรก็ตาม คุณภาพที่ดีต้องอาศัย initialization, calibration, schedule และการตรวจ hard checkpoint; format ที่เล็กไม่ได้รับประกัน runtime ที่เร็วหรือความสามารถที่ไม่ลดลง.[1]

หากคำถามถัดไปคือ “ควรให้ layer ไหน 2 บิต และ layer ไหน 3–4 บิต ภายใต้งบไฟล์รวม?” ให้อ่าน [[RCO: Riemannian Constrained Optimization จัดสรรบิตภายใต้งบขนาดโมเดล]]

## Sources

[1] <https://arxiv.org/html/2604.18556v2>

[2] <https://github.com/IST-DASLab/GSQ>

[3] <https://arxiv.org/html/2605.00649v2>

[4] <https://github.com/IST-DASLab/RCO>

[12] <https://raw.githubusercontent.com/IST-DASLab/GSQ/03fc16484c369e3127225615d5e03e8d3a6043e3/src/quantization/gumbel_quantizer_2bit.py>

</div>
