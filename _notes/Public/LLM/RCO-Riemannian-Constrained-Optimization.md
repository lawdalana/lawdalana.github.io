---
title: "RCO: Riemannian Constrained Optimization จัดสรรบิตภายใต้งบขนาดโมเดล"
notetype: feed
date: 2026-10-28
last_modified: 2026-10-29
tags: [RCO, Riemannian-optimization, quantization, mixed-precision, LLM, model-compression, budget]
status: published
permalink: /notes/rco-riemannian-constrained-optimization
---

<link rel="stylesheet" href="/assets/css/quantization-articles.css">
<div class="quantization-article" markdown="1">

> **ขอบเขตและที่มา:** บทความนี้อธิบาย *Model Compression with Exact Budget Constraints via Riemannian Manifolds* โดย **Michael Helcig และ Dan Alistarh**, อ้างอิง **arXiv:2605.00649v2** และ official repository ที่ตรวจเมื่อ **28 ตุลาคม 2026** ผล LLM benchmarks เป็น **ผลที่ผู้วิจัยรายงาน** ส่วนตัวอย่างด้านล่างเป็น **การรันจริงของ geometry primitives และ budget-constrained DP บน CPU** ไม่ใช่การทำซ้ำ LLM search ทั้ง paper.[3][4]

## TL;DR

- **RCO เลือก compression option ให้แต่ละกลุ่มภายใต้งบรวม** เช่น layer นี้ 2-bit, อีก layer 4-bit หรือ expert นี้เก็บ/ตัด โดย optimize loss ที่ขึ้นกับการเลือกทุกส่วนร่วมกัน.[3]
- RCO ไม่ใช่ quantizer ที่แทน GPTQ หรือ GSQ แต่เป็น **วิธีค้น allocation** ใน released quantization pipeline ที่ตรวจ จะสร้างฐาน candidate weights ด้วย GPTQ แล้วค้นว่าจะหยิบ bitwidth ใดให้แต่ละ layer.[4]
- ใช้ softmax เปลี่ยน discrete options เป็นความน่าจะเป็น และมองเงื่อนไข expected cost เท่ากับงบเป็น **budget manifold** จากนั้นครอบ Adam ด้วย tangent projection, retraction และ momentum transport.[3]
- ฝั่ง forward ยังต้องมี **dynamic programming (DP)** เพื่อเลือก discrete assignment ที่ไม่เกินงบ ส่วน Gumbel-STE ให้ surrogate gradient สำหรับเรียนรู้ logits การใช้ argmax แยกทุก layer ไม่ได้แทนขั้นตอนนี้.[3]
- “Exact budget” ต้องแยกสามชั้น: **expected modeled cost**, **discrete modeled cost** และ **ขนาดไฟล์หลัง serialize จริง** ไม่ควรสัญญาว่าใส่งบ 1.5 GB แล้วจะได้ไฟล์ตรงทุกไบต์โดยไม่คิด overhead.[3][4]

**อ่านพื้นฐานการสร้างน้ำหนักแบบบิตต่ำ:** [[GSQ: Gumbel-Softmax Quantization บีบอัดน้ำหนัก LLM ให้แม่นยำในบิตต่ำ]]

## 1. ทำไมไม่ให้ทุก layer ใช้จำนวนบิตเท่ากัน

พิจารณาโมเดลที่ต้องลดขนาดให้พอดีกับพื้นที่เก็บข้อมูล หากบังคับทุกส่วนเป็น 2-bit ก็จัดการง่าย แต่บาง layer อาจไวต่อ quantization มาก ในขณะที่บางส่วนทนต่อการบีบอัดได้ดีกว่า การให้บิตเพิ่มกับส่วนแรกและลดกับส่วนหลังจึงอาจให้ trade-off ที่ดีกว่า.[3]

โจทย์ที่แท้จริงไม่ใช่เพียง “layer ไหนสำคัญ?” แต่เป็น

> เลือกความละเอียดของทุกส่วน **พร้อมกัน** อย่างไร ให้คุณภาพรวมดีที่สุดโดยไม่เกินงบ?

ถ้า loss แยกเป็นผลรวมอิสระของแต่ละ layer ได้จริง ก็ให้คะแนนราย layer แล้วใช้ knapsack/DP จัดงบได้ แต่ใน neural network layer ที่เปลี่ยนไปส่งต่อ input distribution ใหม่ให้ layer ถัดไป ความเสียหายรวมจึงไม่จำเป็นต้องเท่ากับผลรวมของการเปลี่ยนทีละ layer.[3]

### ตัวอย่างเชิงแนวคิด: sensitivity แบบแยกส่วนอาจหลอกเรา

สมมติการลดบิตของ A เพียงตัวเดียวทำให้ loss เพิ่ม 0.1 และของ B เพียงตัวเดียวเพิ่ม 0.1 แต่หากลดพร้อมกัน loss เพิ่ม 0.9 เพราะข้อผิดพลาดส่งเสริมกัน ตัวเลขสมมตินี้แสดงว่าการใช้ $0.1+0.1$ เป็นตัวแทน loss รวมอาจเลือก allocation ผิดได้

RCO จึงพยายามใช้ gradient จาก **joint model objective** เช่น calibration KL divergence แทนการตรึง independent sensitivity scores เป็นโจทย์สุดท้าย ขณะเดียวกันก็ต้องรักษางบที่เป็นเงื่อนไขแข็ง.[3]

## 2. เขียนโจทย์ให้ชัดก่อน: อะไรคือ group, option และ cost

ให้

- $N$ คือจำนวนกลุ่ม เช่น linear layers หรือ MoE experts
- $K$ คือจำนวนตัวเลือกต่อกลุ่ม
- $w_i>0$ คือน้ำหนักเชิงต้นทุนของกลุ่มที่ $i$ เช่นจำนวนพารามิเตอร์
- $c_k$ คือต้นทุนต่อหนึ่งหน่วยของ option ที่ $k$ เช่น bits/parameter
- $z_{ik}\in\lbrace 0,1\rbrace$ บอกว่ากลุ่ม $i$ เลือก option $k$ หรือไม่
- $B$ คืองบรวมใน **หน่วยเดียวกับ cost**.[3]

โจทย์ discrete เขียนได้เป็น

$$
\min_z\mathcal L(z)
\quad\text{subject to}\quad
\sum_iw_i\sum_kz_{ik}c_k\le B,
\qquad \sum_kz_{ik}=1.
$$

ตัวอย่าง หากมีสาม layers ขนาด 1, 2 และ 1 ล้านพารามิเตอร์ แล้วเลือก `[4, 2, 2]` bits ตามลำดับ จำนวน payload bits คือ

$$
1\mathrm M\times4+2\mathrm M\times2+1\mathrm M\times2
=10\mathrm M\text{ bits}.
$$

ค่าเฉลี่ยที่ถูกต้องจึงเป็น

$$
\bar b=\frac{10\mathrm M}{4\mathrm M}=2.5\text{ bits/parameter}.
$$

**อย่าเฉลี่ยตามจำนวน layer แบบไม่ถ่วงน้ำหนัก** เพราะ layer ขนาดสองล้านพารามิเตอร์มีผลต่อพื้นที่มากกว่า layer ขนาดหนึ่งล้านพารามิเตอร์

## 3. เปลี่ยน discrete choices เป็น budget manifold

### 3.1 Softmax relaxation

ให้แต่ละ group มี learnable logits $\alpha_i\in\mathbb R^K$ และ

$$
p_{ik}=\operatorname{softmax}(\alpha_i)_k.
$$

Expected modeled cost เป็น

$$
C(\alpha)=\sum_iw_i\sum_kp_{ik}c_k.
$$

จากนั้น optimize บนผิว

$$
\mathcal M=\{\alpha\in\mathbb R^{NK}:C(\alpha)=B\}.
$$

เมื่อ costs ไม่เท่ากันทั้งหมดและงบอยู่ภายในช่วงที่เป็นไปได้ ผิวนี้เป็น smooth manifold ขนาด $NK-1$ ใน full logit space โครงสร้าง simplex ถูกบรรจุอยู่ใน softmax อยู่แล้ว ไม่ต้องเพิ่มข้อจำกัด sum-to-one แยกอีกชุด.[3]

### 3.2 คำว่า Riemannian หมายถึงอะไรในงานนี้

นึกถึงการเดินบนผิวที่โค้ง: เราอยากเดินลงตาม loss แต่ห้ามเดินออกนอกผิวงบ บนแต่ละจุดจะมี tangent space สำหรับทิศทางที่ไม่เปลี่ยน cost ในอันดับแรก และ normal ที่ตั้งฉากกับผิวนั้น.[3]

Paper ใช้ **Euclidean ambient metric ใน logit space** จึงคำนวณ projection ได้ง่าย ไม่ได้หมายความว่าใช้ Fisher information หรือ natural gradient โดยอัตโนมัติ และ “Riemannian” ไม่ใช่ชื่อ kernel สำหรับคูณเมทริกซ์บิตต่ำ.[3]

## 4. สาม operation ที่ครอบ Adam

<figure class="quantization-figure">
  <a href="/assets/img/LLM/GSQ-RCO/rco-budget-manifold.svg" target="_blank" rel="noopener noreferrer" aria-label="ขยายภาพ projection retraction และ momentum transport ของ RCO ในแท็บใหม่">
    <img src="/assets/img/LLM/GSQ-RCO/rco-budget-manifold.svg" alt="ภาพแนวคิด budget manifold แยก tangent projection การคืนจุดด้วย retraction และการจัด momentum ให้ตรง tangent space ใหม่" width="800" height="1060" loading="lazy" decoding="async">
  </a>
  <figcaption><strong>สามหน้าที่ที่ไม่เหมือนกัน:</strong> 1 ตัดส่วน normal ออกจาก gradient, 2 คืนจุดหลัง update ให้ expected cost กลับสู่งบ, 3 จัด first moment ให้ตรง tangent space ใหม่ ลูกศร retraction แสดงการเลื่อนตาม cost direction ไม่จำเป็นต้องตั้งฉากกับผิว ภาพนี้เป็น schematic สองมิติ ไม่ใช่ logit geometry หรือกราฟ convergence จริง และยังต้องมี constrained DP สำหรับ hard choices — แตะภาพเพื่อขยาย</figcaption>
</figure>

### 4.1 Tangent projection: ตัดทิศที่เปลี่ยนงบออกจาก gradient

เขียน expected cost ของ group $i$ เป็น

$$
\mu_i=\sum_kp_{ik}c_k.
$$

อนุพันธ์ของงบคือ

$$
n_{ik}=\frac{\partial C}{\partial\alpha_{ik}}
=w_ip_{ik}(c_k-\mu_i).
$$

เวกเตอร์ $n=\nabla C$ เป็น normal ของ budget manifold ถ้า gradient จาก loss คือ $g$ ให้ project เป็น

$$
g_T=g-\frac{\langle g,n\rangle}{\|n\|^2}n.
$$

จึงมี $\langle g_T,n\rangle=0$ ในเลขคณิตอุดมคติ เป็นการเก็บส่วนที่ไม่เปลี่ยนงบในอันดับแรกไว้ ไม่ใช่การลบ gradient ของ layer ที่มีความสำคัญน้อยแบบ heuristic.[3]

**จุดสำคัญ:** projection นี้อยู่ก่อน Adam เพื่อไม่ให้ first moment สะสมทิศทาง normal โดยเปล่าประโยชน์ แต่ finite Adam step ยังออกนอก manifold ได้จากความโค้งและ per-coordinate scaling จึงยังต้องทำขั้นถัดไป.[3]

### 4.2 Retraction: กลับมาที่ผิวงบหลัง update

หลัง Adam ได้ logits ชั่วคราว $\alpha'$ ให้เลื่อนทุกแถวตาม cost vector เดียวกัน

$$
\alpha''_{ik}=\alpha'_{ik}+t c_k.
$$

แล้วหา scalar $t$ ที่ทำให้

$$
C(\alpha'+t\tilde c)=B,
$$

โดย $\tilde c$ คือ cost vector ที่ broadcast ไปยังทุก group เหตุผลที่ใช้ binary search ได้คือ

$$
\frac{d}{dt}C(\alpha'+t\tilde c)
=\sum_iw_i\operatorname{Var}_{p_i(t)}[c]>0.
$$

เมื่อเพิ่ม $t$ option ที่แพงกว่าจะมี relative logit สูงขึ้น expected cost จึงเพิ่มแบบ monotone ทำให้คืนจุดกลับสู่ budget surface ได้โดยไม่ต้องแก้ nonlinear system ขนาดใหญ่.[3]

**Exact ในทางปฏิบัติยังมี tolerance:** โค้ด `retraction()` ที่ pin ตรวจมี `tol` และ `max_iter`; default `tol` ของฟังก์ชันนี้เป็น `0.05` ในหน่วย cost ที่ caller ส่งมา ดังนั้นควรดูการ normalize cost และ tolerance ของ run จริง ไม่เหมารวมว่าทุก call มี residual ระดับ machine epsilon ตัวอย่างในบทความตั้ง tolerance ของตัวเองให้เข้มกว่า.[13]

### 4.3 Vector transport: พา momentum ไปยัง tangent space ใหม่

หลัง retraction ตำแหน่งใหม่มี normal $n'$ ซึ่งต่างจากเดิม หากเก็บ momentum $m$ เดิมไว้ตรง ๆ มันอาจมีส่วนที่ชี้ออกนอกผิว จึงทำ

$$
m\leftarrow m-\frac{\langle m,n'\rangle}{\|n'\|^2}n'.
$$

Paper transport เฉพาะ **first moment** ของ Adam ส่วน second moment เป็นค่าประมาณขนาดรายพิกัด ไม่ใช่เวกเตอร์ทิศทางที่ต้องอยู่ใน tangent space จึงไม่ถูก project แบบเดียวกัน.[3][13]

## 5. อยู่บน expected budget แล้ว ทำไมยังต้อง DP?

นี่คือจุดที่สรุปสั้น ๆ มักทำให้เข้าใจผิด

สมมติ group ทุกกลุ่มมี probability ที่ทำให้ **expected** cost เท่ากับงบ แต่ตอนเลือก option จริงด้วย argmax แยกแต่ละกลุ่ม อาจเลือก expensive option พร้อมกันจนเกินงบ การรักษา $C(\alpha)=B$ จึงไม่ได้รับประกัน hard assignment ที่เกิดจาก independent rounding.[3]

### 5.1 Forward ใช้ budget-constrained knapsack

RCO สุ่ม Gumbel noise และสร้าง perturbed logits

$$
\hat\alpha_{ik}=(\alpha_{ik}+G_{ik})/\tau.
$$

จากนั้นหา

$$
z^*=\operatorname{argmax}_z\sum_{i,k}z_{ik}\hat\alpha_{ik}
$$

ภายใต้เงื่อนไขเลือกหนึ่ง option ต่อ group และ

$$
\sum_iw_i\sum_kz_{ik}c_k\le B.
$$

นี่คือ multiple-choice knapsack ซึ่ง DP แก้ให้ได้ discrete assignment ที่ feasible ใน modeled cost ส่วน objective ที่ DP maximize เป็น **คะแนน logits แบบบวกกันได้** ไม่ใช่กำลังแก้ joint LLM loss ทั้งระบบได้อย่าง exact ด้วย DP.[3]

### 5.2 Backward ใช้ Gumbel-STE

ให้ $\hat p=\operatorname{softmax}(\hat\alpha)$ และเขียนตัวแทนที่ใช้สำหรับ gradient เป็น

$$
z_{\mathrm{STE}}
=\operatorname{stopgrad}(z^*-\hat p)+\hat p.
$$

Forward เห็นค่า hard assignment $z^*$ จริง แต่ backward เดินผ่าน $\hat p$ ที่สร้างจาก **perturbed logits ชุดเดียวกัน** แล้ว project gradient กลับสู่ tangent space ก่อนส่งให้ Adam วิธีนี้ให้ gradient estimator ที่มี bias; projection ไม่ได้ทำให้ gradient ของ loss กลายเป็น unbiased เพียงแต่ตัดส่วน normal ที่จะรบกวน constraint handling ออก.[3]

**หมายเหตุจากสมการ:** ถ้า $\tau$ เป็น scalar บวกตัวเดียวสำหรับทุกคะแนน การหาร perturbed logits ทั้งหมดด้วยมันจะไม่เปลี่ยน argmax ของโจทย์ DP สำหรับ noise ชุดนั้นเอง ผลของ temperature ต่อ softmax surrogate/gradient ต้องแยกจากการสุ่ม Gumbel ใหม่ ไม่ควรอธิบายว่าเพียงเปลี่ยนตัวหารนี้แล้ว hard assignment ของ sample เดิมต้องเปลี่ยนเสมอ

### 5.3 หลังฝึกยังต้องแก้ constrained assignment

Paper ดึง allocation สุดท้ายด้วย DP บน $\log p$ แบบไม่มี noise และไม่มี temperature ไม่ใช่ argmax แยก layer แล้วหวังว่างบจะพอดี.[3]

```text
initialize logits → retract to expected budget
for each optimization step:
  sample Gumbel noise
  solve constrained DP on perturbed logits → hard choices
  evaluate actual model calibration loss using chosen candidates
  backpropagate through matched softmax surrogate (STE)
  average gradients across samples when configured
  project gradient onto tangent space
  Adam update
  retract logits back to expected budget
  transport Adam first moment to new tangent space
final constrained DP on log probabilities
materialize selected weights → pack → check actual bytes and quality
```

## 6. “Exact” สามชั้น และสิ่งที่ไม่ได้รับประกัน

| ชั้น | สิ่งที่ควบคุม | สิ่งที่ต้องระวัง |
|---|---|---|
| Continuous | $C(\alpha)=B$ ภายใน numerical tolerance | นี่คือ expected cost ใน relaxation |
| Discrete | $C(z)\le B$ ใน DP cost model | อาจใช้ไม่เต็มงบ และขึ้นกับ integer cost units |
| Serialized file | bytes ของ checkpoint ที่เขียนจริง | ต้องรวม packing, scales, untouched tensors, metadata และวัดหลัง export |

สองชั้นแรกเป็นส่วนของ algorithm; ชั้นสุดท้ายต้องใช้ cost accounting กับ exporter ที่สอดคล้องกันด้วย ไม่ใช่คำรับประกันที่ได้จากชื่อ RCO เพียงอย่างเดียว.[3][4]

นอกจากนี้

- **ไม่รับประกัน global optimum ของ LLM loss:** complete pipeline มี STE bias และ optimizer heuristic; paper แยกข้อพิสูจน์ด้าน geometry ออกจากผล convergence เชิงประจักษ์.[3]
- **ไม่รับประกัน inference latency ตามงบบิต:** latency เป็น nonlinear hardware-dependent cost และไม่รับ monotone-retraction property นี้ไปโดยอัตโนมัติ.[3]
- **ไม่ควรบังคับ equality ทุกกรณี:** หากคำตอบที่ดีที่สุดใช้ต้นทุนต่ำกว่างบ การบังคับใช้ให้เต็มอาจทำให้เลือก option ที่แย่ลง paper จึงมี inequality extension โดยใช้ slack variable.[3]
- **DP ยังมีต้นทุน:** complexity ที่ paper ระบุคือ $O(NKB')$ โดย $B'$ เป็นงบใน integer cost units ต้องจัดการหน่วย/การหารด้วยตัวประกอบร่วม ไม่ใช่สร้างตารางยาวเท่าจำนวนบิตทุกบิตในไฟล์หลาย GB แบบตรง ๆ.[3]

## 7. ตัวอย่างที่ 1: งบไฟล์ 1.5 GB ต้องแปลงเป็นงบบิตอย่างไร

**สมมติฐานสาธิต:** มี weights ที่จะ quantize 4 พันล้านตัว, ใช้ group size 128, มี FP16 scale หนึ่งค่าต่อ group, ไม่มี zero-point, และกัน fixed overhead/ส่วนที่ไม่ quantize รวม 100,000,000 bytes ตัวเลขใช้ **GB ฐานสิบ** และสมมติว่า pack payload ได้ตรงบิต โดยยังไม่เพิ่ม row padding

ตั้งงบไฟล์รวม

```text
file budget       = 1,500,000,000 bytes
fixed bytes       =   100,000,000 bytes
scale bytes       =    62,500,000 bytes
payload remaining = 1,337,500,000 bytes
```

เพราะ

$$
\text{scale bytes}
=\frac{4\times10^9}{128}\times2
=62{,}500{,}000.
$$

งบเฉลี่ยสำหรับ **payload codes เท่านั้น** คือ

$$
\bar b_{\mathrm{payload}}
=\frac{1{,}337{,}500{,}000\times8}{4\times10^9}
=2.675.
$$

หากเลือกได้เฉพาะ 2 กับ 3 บิต และ overhead ของทั้งสองแบบตรงตามสมมติฐาน ให้ $f$ เป็นสัดส่วน **ตามจำนวนพารามิเตอร์** ที่ใช้ 3-bit จะได้

$$
2(1-f)+3f=2.675
\quad\Rightarrow\quad f=0.675.
$$

จึงมีงบให้ 3-bit ได้ 67.5% ของ quantized parameters ไม่ใช่ 67.5% ของจำนวน layers แต่การเลือกว่าพารามิเตอร์ส่วนใดควรได้บิตเพิ่มเป็นงานของ allocation search และอาจทำสัดส่วนนี้ไม่ได้พอดีถ้าต้องเลือกทีละ layer ขนาดใหญ่

**ข้อจำกัดของตัวอย่าง:** ของจริงต้องคำนวณจำนวน groups ตาม row/tensor boundaries, zero-point storage, kernel packing, alignment และ metadata ให้ครบ หากต้นทุนเฉพาะ option ต่างกันตาม layer อาจต้องใช้ per-group option costs/generalized cost model ไม่ใช่ยัดทุกอย่างลง $w_i c_k$ โดยไม่ตรวจว่าแยกตัวประกอบได้จริง

ถ้าไฟล์เกินหลัง export อย่าแก้ด้วยการอ้างว่า expected budget ผ่านแล้ว ให้ปรับ cost model หรือ safety reserve แล้วค้นใหม่

## 8. ตัวอย่างที่ 2: geometry และ DP ที่รันได้จริงโดยไม่ใช้ GPU

[ดาวน์โหลด rco_demo.py](/assets/examples/quantization/rco_demo.py) — ใช้ **Python 3 standard library เท่านั้น** ไม่มีโมเดลหรือข้อมูลภายนอก

```bash
python3 rco_demo.py
```

หรือรันจาก repository:

```bash
python3 assets/examples/quantization/rco_demo.py
python3 -m unittest discover -s tests -p 'test_quantization_examples.py' -v
```

### 8.1 Retraction ให้ expected cost กลับมาที่งบ

กำหนดขนาดกลุ่ม `[1, 2, 1]` หน่วย, options `[2, 3, 4]` และ logits เป็นศูนย์ทั้งหมด probabilities จึงเท่ากัน และ expected cost ตั้งต้นเท่ากับ 12 ต้องการงบ continuous 10.5

โค้ดสั้นนี้รันได้เมื่ออยู่โฟลเดอร์เดียวกับไฟล์ดาวน์โหลด:

```python
from rco_demo import expected_cost, retract

alpha = [[0.0, 0.0, 0.0] for _ in range(3)]
sizes = [1, 2, 1]
costs = [2, 3, 4]
adjusted = retract(alpha, sizes, costs, budget=10.5)
print(expected_cost(adjusted, sizes, costs))
```

ผลรันสาธิต:

```text
continuous_cost_before = 12.0
continuous_cost_after  = 10.500000000004606
tangent_dot_normal     = -1.214306433183765e-16
```

Residual ของ dot product ใกล้ศูนย์เป็น floating-point roundoff ไม่ใช่ค่าศูนย์แบบ symbolic และ budget 10.5 ในส่วนนี้เป็น **ตัวอย่าง continuous แยกต่างหาก** จากงบ discrete 10 ในหัวข้อถัดไป

### 8.2 Independent argmax ใช้เกินงบได้อย่างไร

ใช้คะแนนสมมติสำหรับตัวเลือก `[2, 3, 4]` ดังนี้:

| กลุ่ม | ขนาด | คะแนน 2-bit | คะแนน 3-bit | คะแนน 4-bit |
|---|---:|---:|---:|---:|
| A | 1 | 0 | 1 | 5 |
| B | 2 | 0 | 1 | 4 |
| C | 1 | 0 | 0 | 0 |

งบ discrete เป็น 10 หน่วย ถ้าเลือกคะแนนสูงสุดแยกทุกแถวจะได้ `[4, 4, 2]` ใช้ต้นทุน **14** เกินงบ แต่ constrained DP ให้ `[4, 2, 2]` ใช้ต้นทุน **10** และคะแนนรวม **5**

<figure class="quantization-figure">
  <a href="/assets/img/LLM/GSQ-RCO/rco-bit-allocation.svg" target="_blank" rel="noopener noreferrer" aria-label="ขยายภาพเปรียบเทียบ independent argmax กับ constrained DP ในแท็บใหม่">
    <img src="/assets/img/LLM/GSQ-RCO/rco-bit-allocation.svg" alt="ขนาดกลุ่ม A B C เท่ากับ 1 2 และ 1 ล้านพารามิเตอร์ การเลือกบิตแบบ argmax ใช้งบ 14 ล้านบิต ส่วน DP ใช้ 10 ล้านบิต" width="800" height="1000" loading="lazy" decoding="async">
  </a>
  <figcaption><strong>บิตเท่ากันไม่ได้แปลว่าต้นทุนเท่ากัน:</strong> B มีพารามิเตอร์สองเท่าของ A จึงมีต้นทุนสองเท่าเมื่อใช้ precision เดียวกัน แถบทั้งสองชุดใช้สเกลเดียวกัน และคำนวณจาก toy DP จริง: argmax ใช้ 14 ล้าน payload bits แต่ DP เลือกให้เหลือ 10 ล้าน bits ตัวเลขนี้ยังไม่รวม scales หรือ overhead และไม่ใช่การเปรียบเทียบ accuracy ของ LLM — แตะภาพเพื่อขยาย</figcaption>
</figure>

```text
argmax_bits          = [4, 4, 2]
argmax_cost          = 14
dp_bits              = [4, 2, 2]
dp_cost              = 10
dp_score             = 5
payload_average_bits = 2.5
```

เราเทียบ DP ใน test กับการ enumerate ทุก combination ของตัวอย่างนี้แล้ว ได้คะแนน optimum ตรงกัน แต่จำไว้ว่า **คะแนนในตารางเป็น additive fixture ไม่ใช่ loss จาก LLM** ใน RCO จริง logits ถูกปรับด้วย joint model loss ก่อนให้ DP ตัดสินใจ

### 8.3 ขนาดไฟล์จำลองต้องรวม scale และขอบเขตกลุ่ม

ถ้าแปลงขนาด `[1, 2, 1]` เป็น `[1M, 2M, 1M]` parameters, เก็บตามบิต `[4, 2, 2]`, มี FP16 scale ต่อ 128 weights และ fixed overhead 100,000 bytes ตัวอย่างคืน

```text
payload bytes      = 1,250,000
scale groups       = 31,251
scale bytes        = 62,502
fixed bytes        = 100,000
modeled_file_bytes = 1,412,502
```

<figure class="quantization-figure">
  <a href="/assets/img/LLM/GSQ-RCO/rco-file-budget.svg" target="_blank" rel="noopener noreferrer" aria-label="ขยายภาพแยก payload scales และ overhead ของขนาดไฟล์ในแท็บใหม่">
    <img src="/assets/img/LLM/GSQ-RCO/rco-file-budget.svg" alt="งบไฟล์จำลองรวม 1,412,502 bytes แยกเป็น packed codes 1,250,000 scales 62,502 และ fixed overhead 100,000 bytes" width="800" height="950" loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Payload ไม่ใช่ขนาดไฟล์ทั้งหมด:</strong> สำหรับ toy ขนาด 4 ล้านพารามิเตอร์นี้ ต้องบวก FP16 scales ของ 31,251 groups และ fixed overhead ด้วย แถบแบ่งตามสัดส่วน bytes จริงของโมเดลต้นทุนอย่างง่ายนี้ ไม่ใช่ผล serialize GGUF/safetensors และยังไม่ได้รวม zero-points หรือ row padding — แตะภาพเพื่อขยาย</figcaption>
</figure>

จำนวน groups ใช้ $\lceil n_i/128\rceil$ **แยกต่อ tensor ใน fixture** จึงไม่ได้เท่ากับการรวมพารามิเตอร์แล้วหาร 128 เสมอไป ฟังก์ชัน `modeled_bytes()` เป็น calculator แบบง่าย ไม่ใช่ GGUF/safetensors serializer; row boundaries และ padding จริงยังต้องเพิ่มเอง

### 8.4 สิ่งที่ไฟล์นี้ทำและไม่ทำ

ทำจริง:

- stable softmax, expected cost และ analytical budget normal
- tangent projection, monotone bisection retraction และ projection สำหรับ transport
- exact multiple-choice DP ใน positive integer cost units
- simplified file-size accounting
- tests เทียบ budget derivative กับ finite differences และ DP กับ exhaustive enumeration

**ไม่ได้ทำ:** รัน model calibration, autograd ของ LLM, Adam search loop หรือ Gumbel-STE training ดังนั้นไฟล์นี้สอน operation หลักและตรวจข้อจำกัดเชิงตัวเลขได้ แต่ไม่ได้เป็นคำสั่งสร้าง compressed Qwen checkpoint สำเร็จรูป

## 9. Pipeline สำหรับโมเดลจริง: database → search → materialize

Official repository แบ่งงานออกเป็นขั้นตอนชัดเจน.[4]

### 9.1 เตรียม candidate database

สร้างน้ำหนักที่ quantize ไว้หลาย bitwidth ต่อ layer โดยมีทั้ง dequantized tensors สำหรับ search และ qparams sidecars สำหรับ export จริง Sidecars ต้องมี integer codes, scales, zeros และ metadata ให้ตรงกับ bitwidth/grouping ที่เลือก ไม่เช่นนั้นอาจค้น assignment ได้แต่สร้าง packed checkpoint ไม่ครบ.[4][15]

### 9.2 ค้น allocation

ตัวอย่างคำสั่งจาก wrapper ที่ตรวจ ณ commit ที่ pin ไว้ มีรูปแบบดังนี้ **เป็นคำสั่งอ้างอิงสำหรับเครื่องที่ติดตั้งโครงการและเตรียม candidate database แล้ว ไม่ได้รัน LLM search นี้บนเครื่องเขียนบทความ**.[14]

```bash
bash scripts/run_search_quant.sh \
  Qwen/Qwen3-8B \
  ./qwen3_8b_db \
  2.5 \
  200 \
  4
```

ความหมายของ argument ตามลำดับคือ model, layer database, target average bits, จำนวน steps และจำนวน Gumbel samples ต่อ step ต้องตรวจ calibration domain, memory requirements, dependencies และ output path ของ run ที่ใช้จริงด้วย.[14]

### 9.3 Materialize แบบ packed ไม่ใช่ fake-quant

**กับดักสำคัญ:** `run_build_checkpoint.py quant` ตั้ง default เป็น `fake-quant` ซึ่งใส่ dequantized weights กลับลง tensor BF16 แม้ค่าจะอยู่บน quantization grid แล้ว แต่ไม่มีประโยชน์ด้านขนาดไฟล์แบบ packed ต้องเลือก `--format compressed-tensors` หากต้องการ packed checkpoint และมี qparams sidecars ครบ.[15]

รูปแบบคำสั่งอ้างอิงที่ตรวจจาก parser:

```bash
python3 run_build_checkpoint.py quant \
  --model Qwen/Qwen3-8B \
  --config ./assignment.json \
  --layer-dir ./qwen3_8b_db \
  --output ./qwen3_8b_mixed_packed \
  --group-size 128 \
  --format compressed-tensors
```

`assignment.json` ในตัวอย่างเป็น path สมมติให้แทนด้วยผล search จริง ต้องตั้ง symmetric/asymmetric metadata ให้ตรงกับ database ที่สร้าง ไม่ใช่ใส่ `--symmetric` เพิ่มเพียงเพราะอยากลด overhead และต้องตรวจว่า runtime รองรับ bitwidth ที่เลือกครบจริง.[15]

หลัง export ให้ตรวจทั้ง

1. ขนาดไฟล์ของ checkpoint ที่นิยามไว้ในงบ รวมไฟล์ประกอบตาม scope
2. การโหลดสำเร็จและไม่มี tensor/quantization metadata ที่ขาด
3. คุณภาพบน held-out data หลัง **packed** round-trip
4. runtime memory และ latency บนเครื่องเป้าหมาย

สำหรับ MoE pruning ก็มีความต่างเดียวกัน: mode ที่ zero weights ยังเก็บ tensor shape เดิม ส่วน mode ที่ remove expert จริงจึงลด storage และอาจต้องมี loader รองรับจำนวน experts ที่ต่างกันแต่ละ layer.[4]

## 10. ผลที่ paper รายงาน: เปรียบเทียบอะไร และเร็วตรงไหน

การทดลอง mixed-precision บน Qwen3-8B ใน paper v2 เลือก 2–8 bits ให้ **252 linear layers**, ใช้ GPTQ candidate database และ calibration KL divergence จาก FineWeb-Edu 256 sequences ความยาว 2048 ส่วน evaluation ใช้ held-out FineWeb-Edu และ C4 โดย perplexity **ยิ่งต่ำยิ่งดี**.[3]

ตัวอย่างที่ target 2.5 average bits จาก Table 2:

| วิธี/setting | FineWeb-Edu PPL | C4 PPL | เวลาในตาราง |
|---|---:|---:|---|
| RCO, $g=4,T=200$ | 15.78 | 24.73 | 62 นาที |
| RCO, $g=32,T=50$ | 15.43 | 24.00 | 117 นาที |
| RCO, $g=16,T=200$ | 15.45 | 23.79 | 215 นาที |
| EvoPress, 100 generations | 15.64 | 24.63 | 11–14 ชั่วโมง |
| HIGGS | 20.08 | 31.15 | ประมาณ 2 ชั่วโมง |

ในตาราง $g$ คือจำนวน Gumbel samples และ $T$ คือจำนวน optimization steps ผลเหล่านี้สะท้อน trade-off ระหว่าง sample count, compute และ quality ไม่ใช่ว่าเพิ่ม steps หรือ samples แล้วทุก metric จะดีขึ้นแบบ monotone.[3]

Paper ระบุว่า EvoPress บน Qwen3-8B เป็นการ reproduce ของผู้เขียนภายใต้ matched protocol ไม่ใช่หยิบตัวเลขดั้งเดิมต่าง setup มาเทียบ และคำว่าเร็วกว่าคือ **เวลาค้น allocation ตามการทดลอง** ไม่ใช่ inference TPS ของโมเดลที่ deploy แล้ว.[3]

นอกจาก dense quantization ยังมี MoE expert pruning และ MoE mixed precision แสดงว่าแนวคิดครอบคลุม discrete resource allocation มากกว่า bitwidth อย่างเดียว แต่ตัวเลขจาก task หนึ่งไม่ใช่คำรับประกันของอีก task.[3]

## 11. ใช้ GSQ กับ RCO ร่วมกัน: แยกหน้าที่ให้ถูก

อ่านภาพรวมเชิงระบบได้ดังนี้:

```text
quantization candidate generator
  GPTQ / GSQ / another validated quantizer
               ↓
per-group candidates + correct modeled costs
               ↓
allocation search such as RCO
               ↓
chosen bitwidth / option for every group
               ↓
compatible packing + quality / byte / runtime checks
```

GSQ เรียนรู้ว่า **ภายใน grid นี้** ควรแทนน้ำหนักแต่ละตัวอย่างไร ส่วน RCO เรียนรู้ว่า **แต่ละ group ควรเลือก grid/bitwidth ไหน** จึงเป็นคนละระดับและใช้แนวคิดร่วมกันได้ แต่ official RCO quantization pipeline ที่ตรวจสร้าง database ด้วย GPTQ; บทความนี้ **ไม่ได้ทดสอบ full GSQ→RCO integration**.[1][4]

ก่อนเชื่อมจริงต้องแก้และตรวจ

- candidate weights และ scale/zero-point semantics ตรงกับ store/loader
- group size, signed code convention และ packing ตรงกัน
- per-option cost รวม overhead ที่เกี่ยวข้อง
- การเลือก candidate ผ่าน STE ไม่ทำให้ gradient path ขาด
- หลังค้น allocation แล้ว exporter เก็บ bitwidth ที่ได้จริง ไม่ขยายกลับ BF16 โดยไม่ตั้งใจ

การที่ทั้งสองวิธีใช้ Gumbel-related relaxation ไม่ได้ทำให้ file format หรือ API เข้ากันเอง

## 12. ควรใช้เมื่อไร และควรระวังอะไร

**เหมาะเมื่อ** ต้องการ mixed compression ภายใต้งบชัดเจน มี candidate options ให้เลือก มี calibration ที่เชื่อถือได้ และยอมรับค่าใช้จ่ายในการ search เพื่อแลกกับ quality/size trade-off ที่ดีขึ้น.[3][4]

**อาจไม่คุ้มเมื่อ** uniform precision ที่ runtime รองรับให้คุณภาพและขนาดพออยู่แล้ว, งบ search จำกัดมาก, ไม่มีข้อมูล calibration ที่เป็นตัวแทน หรือ hardware ไม่รองรับ heterogeneous bitwidth อย่างมีประสิทธิภาพ ข้อนี้เป็นข้อพิจารณาด้านระบบ ไม่ใช่ benchmark ใหม่ของ paper

ข้อควรระวังหลัก:

1. **Calibration overfitting:** ต้องมี held-out quality checks ตามภาษาและงานจริง
2. **Budget units:** bits, bytes, decimal GB และ GiB ไม่ใช่หน่วยเดียวกัน
3. **Discrete reachability:** บาง budget แทนไม่ได้พอดีเมื่อเลือกทีละ layer
4. **Expected ≠ hard:** continuous equality ไม่แทน constrained extraction
5. **Fake ≠ packed:** ค่าบน integer grid ที่อยู่ใน BF16 tensor ยังใช้พื้นที่ BF16
6. **Storage ≠ VRAM ≠ latency:** ต้องวัดแต่ละอย่างแยกกัน
7. **Exact constraint ≠ exact optimum:** feasibility ไม่ได้พิสูจน์ความแม่นยำสูงสุดทั่วทั้ง search space

## สรุป

RCO ทำให้โจทย์ “แบ่งงบให้ทุกส่วนอย่างไร” กลายเป็นการ optimize บน budget surface ที่มี geometry คำนวณได้ง่าย: **project gradient → Adam → retract → transport momentum** และใช้ **constrained DP** ควบคุม discrete forward choices อีกชั้น.[3]

จุดที่นำไปใช้ได้ทันทีจากบทความนี้คือวินัยในการแยก **คุณภาพของ candidate**, **การแบ่งงบ**, **ต้นทุนที่จำลอง** และ **ไฟล์ที่เก็บจริง** หากแยกครบ จะเลือก precision ได้อย่างมีเหตุผลมากกว่าดูเพียงชื่อ “2-bit model” หรือคำว่า “exact budget”

อ่านควบคู่: [[GSQ: Gumbel-Softmax Quantization บีบอัดน้ำหนัก LLM ให้แม่นยำในบิตต่ำ]]

## Sources

[1] <https://arxiv.org/html/2604.18556v2>

[3] <https://arxiv.org/html/2605.00649v2>

[4] <https://github.com/IST-DASLab/RCO>

[13] <https://raw.githubusercontent.com/IST-DASLab/RCO/9a1e09c07d468109cbe60a1b87d5036034a79d10/src/manifold.py>

[14] <https://raw.githubusercontent.com/IST-DASLab/RCO/9a1e09c07d468109cbe60a1b87d5036034a79d10/scripts/run_search_quant.sh>

[15] <https://github.com/IST-DASLab/RCO/blob/9a1e09c07d468109cbe60a1b87d5036034a79d10/run_build_checkpoint.py>

</div>
