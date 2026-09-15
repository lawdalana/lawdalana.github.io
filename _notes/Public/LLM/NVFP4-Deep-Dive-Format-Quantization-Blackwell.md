---
title: "NVFP4 ฉบับเจาะลึก: 4 บิตแบบ NVIDIA ทำงานอย่างไร เร็วแค่ไหน และควรใช้เมื่อใด"
notetype: feed
date: 2026-08-09
last_modified: 2026-09-16
tags: [NVFP4, FP4, quantization, NVIDIA, Blackwell, TensorRT-LLM, vLLM, LLM-inference, low-precision]
status: published
---

# NVFP4 ฉบับเจาะลึก

![ภาพประกอบการบีบอัด tensor เป็น NVFP4](/assets/img/Other/NVFP4/nvfp4-hero.avif)

*ภาพปกสร้างขึ้นใหม่สำหรับบทความนี้ ไม่ได้คัดลอกภาพประกอบหรือกราฟ benchmark ของ NVIDIA*

> **หมายเหตุบรรณาธิการ:** บทความนี้ค้นคว้าจาก [*Introducing NVFP4 for Efficient and Accurate Low-Precision Inference*](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) ของ NVIDIA แล้วตรวจสอบเทียบกับ OCP MX specification, CUDA/CUTLASS, Transformer Engine, Model Optimizer, TensorRT-LLM, vLLM, model cards และงานวิจัยที่ออกภายหลัง ข้อมูล software/hardware อ้างอิงสถานะ ณ **9 สิงหาคม 2026** ตัวเลขจาก NVIDIA จะระบุว่าเป็น **ผลที่ NVIDIA รายงาน** ส่วนข้ออนุมานจะระบุว่าเป็น **บทวิเคราะห์**

## TL;DR

1. **NVFP4 ไม่ใช่เพียง “float 4 บิต”** แต่กำหนดทั้งรูปแบบการแทนค่าและวิธี scale เป็นลำดับชั้น (hierarchical block scaling): ค่าแต่ละตัวใช้ **FP4 E2M1** ทุก 16 ค่าใช้ **FP8 E4M3 scale** ร่วมกัน และทั้ง tensor มี **FP32 global scale** อีกชั้น
2. E2M1 เก็บค่า raw ได้เพียง `{0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}` แต่ scale ทั้งสองชั้นทำให้ tensor จริงไม่ได้ถูกจำกัดอยู่ที่ช่วง ±6
3. สำหรับ tensor ขนาดใหญ่ รูปแบบนี้ใช้พื้นที่ประมาณ `4 + 8/16 = 4.5` บิตต่อ element และมี overhead อีก `32/N` บิตจาก global scale จึงได้อัตราส่วนเชิงอุดมคติราว **3.56× เทียบ BF16/FP16** หรือ **1.78× เทียบ FP8**
4. **ตัวเลข 3.56×/1.78× ไม่ใช่คำรับประกัน VRAM ทั้งระบบ** เพราะโมเดลยังมี layer ที่ไม่ quantize, KV cache, activation, workspace, padding, metadata และ allocator overhead
5. NVFP4 ต่างจาก **MXFP4** ตรงที่ใช้ block เล็กกว่า คือ 16 แทน 32 ค่า ใช้ E4M3 scale ที่มีความละเอียดในส่วนเศษแทน UE8M0 scale ที่เป็นกำลังของสอง และเพิ่ม FP32 tensor scale
6. การเร่ง FP4 ด้วย Tensor Core โดยตรงต้องใช้ **NVIDIA Blackwell** และ kernel ของ runtime ที่รองรับ การเปิด checkpoint บน Hopper/Ampere ด้วย fallback หรือ emulation ไม่ได้หมายความว่าจะได้ throughput แบบ W4A4 FP4
7. คำว่า NVFP4 checkpoint อาจหมายถึง **W4A4**, **W4A16**, mixed precision หรือเพิ่ม **NVFP4 KV cache** ก็ได้ ต้องอ่าน quantization metadata ไม่ใช่ดูชื่อไฟล์อย่างเดียว
8. NVFP4 เป็น **quantization ที่สูญเสียข้อมูลบางส่วน (lossy quantization)** ความแม่นยำขึ้นกับโมเดล layer ที่เลือก quantize, calibration, algorithm, dataset และ metric โมเดลใหญ่บางตัวทำ PTQ ได้ดี แต่โมเดลเล็กหรือโมเดลที่ความสามารถด้าน reasoning/RL ไวต่อการ quantize อาจต้องใช้ mixed precision, 4/6, AWQ, QAT หรือ QAD
9. NVIDIA รายงาน DeepSeek-R1-0528 NVFP4 ใกล้ FP8 ใน benchmark ที่เลือก แต่แต่ละ metric ขยับทั้งบวกและลบ จึงไม่ควรสรุปว่า quantization “ทำให้ฉลาดขึ้น”
10. ใช้ NVFP4 เมื่อมี Blackwell โดยมีการเก็บหรือรับส่ง model weights เป็นคอขวด runtime รองรับ recipe นั้นจริง และผลประเมินผ่าน SLO ทั้งด้านคุณภาพ latency, throughput และ memory หากเงื่อนไขใดไม่ครบ FP8, BF16 หรือ W4A16 อาจเป็นตัวเลือกที่เสี่ยงน้อยกว่า

---

## คำตอบเร็ว: NVFP4 ในหนึ่งตาราง

| คำถาม | คำตอบสั้น |
|---|---|
| NVFP4 คืออะไร? | FP4 E2M1 + E4M3 scale ต่อ 16 ค่า + FP32 scale ต่อ tensor |
| เป็น 4 บิตจริงไหม? | payload 4 บิต แต่ representation แบบ 1×16 ใช้ราว 4.5 บิต/ค่าเมื่อรวม block scale |
| เป็น IEEE 754 FP4 ไหม? | ไม่ใช่ IEEE interchange format; E2M1 เป็น finite low-precision type และ NVFP4 เพิ่ม scaling/layout |
| lossless ไหม? | ไม่ใช่ มี rounding, underflow-to-zero และ saturation/clipping ได้ |
| ต่างจาก FP4 ทั่วไปอย่างไร? | “FP4” บอก codebook อย่างเดียว ส่วน NVFP4 กำหนด block/global scaling เพิ่ม |
| ต่างจาก MXFP4 อย่างไร? | NVFP4: 16 + E4M3 + FP32 global; MXFP4: 32 + UE8M0 power-of-two |
| ต่างจาก INT4 อย่างไร? | codebook เป็น floating แทน integer; INT4 ยังมีหลายสูตร scale/zero-point/group size จึงเทียบจากชื่ออย่างเดียวไม่ได้ |
| ลด weight memory เท่าไร? | เชิงอุดมคติ ~3.56× จาก 16 บิต หรือ ~1.78× จาก 8 บิต; อัตราการลดจริงมักต่ำกว่า |
| ลด VRAM ทั้งระบบเท่ากันไหม? | ไม่ เพราะ KV cache, activation, workspace และ layer ที่คง precision เดิมยังอยู่ |
| เร็วขึ้นกี่เท่า? | ไม่มีค่าตายตัว; peak Tensor Core, kernel speed และ serving TPS/latency เป็นคนละตัวเลข |
| GPU ไหนได้ native acceleration? | Blackwell ตาม support matrix ของ runtime; product/SM และ mode ต้องตรวจเป็นรายกรณี |
| H100/A100 ใช้ได้ไหม? | อาจโหลดผ่าน fallback/emulation หรือ W4A16 backend บางชนิด แต่ไม่มี native Blackwell FP4 path |
| KV cache เป็น FP4 อัตโนมัติไหม? | ไม่ ต้องเลือก recipe และ attention kernel ที่รองรับแยกต่างหาก |
| ต้อง calibration ไหม? | ถ้า activation scale เป็น static ต้องใช้ข้อมูล calibration; dynamic W4A4 หรือ weight-only max บาง recipe อาจไม่ต้องเก็บ activation statistics |
| ใช้ train ได้ไหม? | ได้ผ่าน Transformer Engine บน Blackwell แต่เป็น native quantized-training recipe ที่ซับซ้อนกว่า PTQ |
| ecosystem มีอะไร? | Model Optimizer, TensorRT-LLM, Transformer Engine, CUDA/CUTLASS, vLLM, SGLang และ checkpoints ที่ export metadata มาแล้ว |

---

## 1. ก่อนอื่นต้องแยก “format” ออกจาก “recipe”

คำว่า NVFP4 ถูกใช้ครอบคลุมหลายชั้น ถ้าไม่แยกชั้นให้ชัด การเปรียบเทียบจะผิดตั้งแต่ต้น

1. **FP4 E2M1 codebook** — บอกว่า 4 บิตตีความเป็นตัวเลขอะไรได้บ้าง
2. **NVFP4 block scaling** — กำหนด E4M3 scale ต่อ micro-block 16 ค่า
3. **Global scaling** — FP32 scale ระดับ tensor เพื่อให้ block scales อยู่ในช่วง E4M3
4. **Quantization algorithm** — AbsMax, 4/6, AWQ, MSE sweep, GPTQ, QAT/QAD ฯลฯ
5. **Tensor layout** — แบ่ง block ตามแกนใด, padding อย่างไร, scale ถูก swizzle/transposed แบบไหน
6. **Compute recipe** — W4A4, W4A16, KV precision, accumulator/output precision และ layer exceptions
7. **Kernel/runtime** — TensorRT-LLM, CUTLASS, vLLM, SGLang หรือ Transformer Engine
8. **Hardware** — Tensor Core generation, compute capability, memory system และ interconnect

ดังนั้น ประโยคว่า “โมเดลนี้เป็น NVFP4” ยังบอกไม่ได้ว่า activation และ KV cache เป็น 4 บิตหรือไม่ ยกเว้น layer ใดไว้ ใช้ native kernel หรือ fallback และผล benchmark จะเร็วขึ้นเท่าไร

> **บทวิเคราะห์:** ให้มอง NVFP4 เป็น **ข้อตกลงเรื่องการแทนค่าและการคำนวณระหว่าง checkpoint, quantization metadata, kernel และ hardware** มากกว่าจะเป็นเพียงนามสกุลไฟล์หรือชื่อ dtype

---

## 2. E2M1: 4 บิตเก็บค่าอะไรได้บ้าง

FP4 ที่ NVFP4 ใช้มีโครงสร้าง

```text
S | EE | M
1   2    1  bits
```

- `S` คือ sign
- `EE` คือ exponent 2 บิต
- `M` คือ mantissa 1 บิต

ค่าขนาด (magnitude) ที่แทนได้มีเพียง

| บิต magnitude | ค่า |
|---|---:|
| `000` | 0 |
| `001` | 0.5 |
| `010` | 1 |
| `011` | 1.5 |
| `100` | 2 |
| `101` | 3 |
| `110` | 4 |
| `111` | 6 |

ใส่ sign แล้วได้ `{±0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}` หรือ 16 bit patterns โดย `+0` และ `−0` มีค่าเชิงตัวเลขเป็นศูนย์เหมือนกัน

### สิ่งที่ E2M1 ไม่มี

- ไม่มีความละเอียดพอเก็บค่าจริงทุกค่า เช่น 1.1 ต้องปัดไปยังค่าที่ใกล้ที่สุดในชุดค่าที่รองรับ
- ไม่มี raw magnitude เกิน 6
- finite E2M1 type นี้ไม่ได้กัน encoding ไว้ให้ NaN/Infinity เหมือน floating-point ขนาดใหญ่
- ระยะห่างระหว่างค่ากว้างขึ้นเมื่อ magnitude สูงขึ้น

แต่ประโยค “ช่วง NVFP4 คือ −6 ถึง 6” ยังอธิบายไม่ครบ เพราะ ±6 เป็นช่วงของ **payload ก่อนคูณ scale** ค่าที่ได้หลังถอดรหัสกลับอาจใหญ่หรือเล็กกว่านั้นมาก

---

## 3. หัวใจของ NVFP4: two-level microscaling

สำหรับ element ลำดับ `i` เอกสาร [Transformer Engine](https://raw.githubusercontent.com/NVIDIA/TransformerEngine/main/docs/features/low_precision_training/nvfp4/nvfp4.rst) อธิบายการถอดรหัสได้เป็น

```text
x̂ᵢ = qᵢ × s⌊i/16⌋ × S
```

โดย

- `qᵢ` เป็น FP4 E2M1 4 บิต
- `s⌊i/16⌋` เป็น FP8 E4M3 scale ที่แชร์กัน 16 ค่า
- `S` เป็น FP32 global scale ของ tensor

เอกสารระดับ algorithm มักเรียก block scale ว่า E4M3 ส่วน CUTLASS เรียก low-level scale type ว่า `float_ue4m3_t` เพราะ scale factor ไม่ติดลบ ทั้งสองกรณีหมายถึง scale 8 บิตแบบมี fractional mantissa และต้องไม่สับสนกับ `UE8M0` power-of-two scale ของ MXFP4

![โครงสร้าง E2M1 และ two-level scaling ของ NVFP4](/assets/img/Other/NVFP4/nvfp4-format.svg)

*แผนภาพต้นฉบับโดย lawdalana แสดง block แบบ 1×16; training recipe อาจใช้ 16×16 scale สำหรับ weights ตามที่อธิบายในหัวข้อ training*

### ตัวอย่างสูตร AbsMax

สูตรอ้างอิงแบบง่ายกำหนด

```text
S   = amax_tensor / (448 × 6)
s_b = round_E4M3(amax_block / (S × 6))
q_i = round_E2M1(x_i / (S × s_b))
```

- `448` คือค่ามากสุดของ FP8 E4M3 ที่ใช้เป็น scale
- `6` คือค่ามากสุดของ E2M1
- implementation จริงยังต้องจัดการ zero block, epsilon, clipping, rounding, axis และ layout

### ทำไมต้องมี global FP32 scale

E4M3 แทนค่าในส่วนเศษได้ละเอียดกว่า UE8M0 แต่มีช่วง exponent แคบกว่า การ normalize tensor ด้วย `S` ก่อนทำให้ block scales อยู่ในช่วงที่ E4M3 แทนได้ จากนั้น `s_b` จึงปรับ dynamic range ของแต่ละ block อีกครั้ง

ลำดับการปรับ scale คือ

```text
ช่วงทั้ง tensor  ──FP32 global scale──►  ช่วงที่ E4M3 รับได้
ช่วงภายใน block ──E4M3 block scale───►  ช่วง E2M1 ±6
ค่าราย element  ──E2M1 rounding──────►  payload 4 บิต
```

### ทำไม block 16 ช่วย accuracy

ถ้า 32 ค่าที่มีการกระจายต่างกันมากต้องใช้ scale เดียวกัน ค่า outlier เพียงตัวเดียวอาจทำให้ค่าขนาดเล็กจำนวนมากถูกปรับจนเข้าใกล้ศูนย์ เมื่อแบ่งเป็นกลุ่มละ 16 ค่า scale จะปรับตามช่วงค่าภายในกลุ่มได้ละเอียดขึ้น แต่ต้องเก็บ scale metadata มากขึ้น

นี่คือข้อแลกเปลี่ยนหลักของ microscaling: **block เล็กลง → รักษาค่าภายในกลุ่มได้แม่นยำขึ้น แต่มี overhead และความซับซ้อนเพิ่มขึ้น**

---

## 4. แล้วทำไมเรียก 4 บิต ทั้งที่จริงราว 4.5 บิต

สำหรับ block 16 ค่าแบบมาตรฐาน

```text
payload       = 16 × 4 bits = 64 bits
E4M3 scale    = 1 × 8 bits  =  8 bits
รวมต่อ block                 = 72 bits
72 / 16                      = 4.5 bits/value
```

ถ้า tensor มี `N` ค่าและ global scale หนึ่งตัว

```text
effective_bits = 4 + 8/16 + 32/N
               = 4.5 + 32/N
```

สำหรับ tensor ใหญ่ `32/N` เล็กมากจึงมักพูดสั้น ๆ ว่า 4.5 บิต/ค่า แต่ tensor เล็กจะเห็น overhead ชัด เช่น `N=16` จะเป็น 6.5 บิต/ค่าเมื่อคิด global scale ด้วย

### อัตราส่วนเชิงอุดมคติ

| ต้นทาง | สูตร | อัตราส่วน ideal |
|---|---:|---:|
| FP16/BF16 16 บิต | `16 / 4.5` | 3.56× |
| FP8 8 บิต | `8 / 4.5` | 1.78× |

นี่คือที่มาของคำกล่าว **“ประมาณ 3.5× เทียบ 16 บิต”** และ **“ประมาณ 1.8× เทียบ FP8”** ในบทความ NVIDIA

### ประมาณ weight payload แบบไม่รวม runtime

ตารางต่อไปนี้ใช้ GB ฐานสิบและสมมติว่าพารามิเตอร์ทุกตัวอยู่ใน precision เดียวกัน

| Parameters | BF16 | FP8 | NVFP4 ที่ 4.5 บิต/ค่า |
|---:|---:|---:|---:|
| 8B | 16 GB | 8 GB | 4.5 GB |
| 70B | 140 GB | 70 GB | 39.375 GB |
| 405B | 810 GB | 405 GB | 227.813 GB |
| 671B | 1,342 GB | 671 GB | 377.438 GB |

> **บทวิเคราะห์:** ตารางนี้ใช้ประเมินพื้นที่ที่ต้องการคร่าว ๆ เท่านั้น ไม่ควรใช้ตัดสินว่าโมเดล “ใส่ใน GPU ได้พอดี” เพราะ checkpoint จริงมี tensor ที่ไม่ quantize, padding/sharding, tokenizer/config และตอนรันยังมี KV cache, activation, CUDA graph, communication buffer และ workspace

---

## 5. NVFP4 ต่างจาก FP8, MXFP4, INT4 และ NF4 อย่างไร

| Format/recipe | Payload | Scale ที่พบบ่อย | Effective bits โดยประมาณ | จุดเด่น | ข้อควรระวัง |
|---|---|---|---:|---|---|
| BF16 | 1-8-7 | ไม่มี microscale | 16 | range ใกล้ FP32, stable | memory/bandwidth สูง |
| FP8 E4M3 | 1-4-3 | per-tensor/channel/token แล้วแต่ recipe | ≥8 | precision สูงกว่า FP4, ecosystem กว้าง | compression ต่ำกว่า NVFP4 |
| Generic FP4 E2M1 | 1-2-1 | ไม่ได้ระบุ | ≥4 | payload เล็ก | คำว่า FP4 อย่างเดียวไม่บอก scale/layout |
| **NVFP4 1D** | E2M1 | E4M3/16 + FP32/tensor | `4.5 + 32/N` | local scale ละเอียด, native Blackwell | NVIDIA-specific recipe/backend coupling |
| MXFP4 | E2M1 | UE8M0/32 | 4.25 | OCP-defined microscaling | scale เป็น power of two และ block ใหญ่กว่า |
| INT4 | integer 4 บิต | symmetric/affine, group/channel/tensor | `4 + overhead` | kernels และ PTQ methods หลากหลาย | ไม่มี recipe เดียว; zero-point/scale ต่างกันมาก |
| NF4 | non-uniform 4-bit codebook | block scale + optional double quant | >4 | เหมาะกับ weight storage/QLoRA | ไม่ใช่ native NVFP4 W4A4 GEMM |

### NVFP4 vs MXFP4

ทั้งคู่ใช้ E2M1 payload แต่ [OCP Microscaling Formats MX v1.0](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf) ([microscaling paper สำรอง](https://arxiv.org/abs/2310.10537)) กำหนด MXFP4 เป็น

- 32 elements ต่อ block
- shared `UE8M0` scale 8 บิต
- scale เป็น power of two จึงคูณได้ง่าย แต่ไม่มี fractional mantissa

NVFP4 เปลี่ยนเป็น

- 16 elements ต่อ block
- shared `E4M3` scale 8 บิต ซึ่งปรับได้ระหว่าง power-of-two steps
- FP32 scale ระดับ tensor เพื่อชดเชย exponent range ของ E4M3

จึงใช้พื้นที่รวม metadata มากกว่าเล็กน้อย คือ 4.5 เทียบ 4.25 บิต/ค่าในกรณี 1D เพื่อแลกกับการรักษาค่าได้แม่นยำขึ้นหลัง quantize

งาน [*Pretraining Large Language Models with NVFP4*](https://arxiv.org/abs/2509.25149) ของ NVIDIA รายงานในการทดลอง 8B/1T tokens ว่า MXFP4 ต้องใช้ token เพิ่ม 36% จึงได้ loss เท่ากับ NVFP4 ในการทดลองนั้น ผลนี้จำกัดอยู่ที่ architecture/recipe/dataset ที่ทดลอง ไม่ใช่กฎว่า NVFP4 ดีกว่า MXFP4 ในทุก workload

### NVFP4 vs INT4

การบอกว่า “FP4 ดีกว่า INT4” โดยไม่มีรายละเอียดไม่สมบูรณ์ เพราะ INT4 อาจเป็น

- symmetric signed INT4 + scale
- affine INT4 + zero point
- groupwise 32/64/128
- per-channel weight-only W4A16
- W4A8 หรือ W4A4 ด้วย activation recipe คนละแบบ

E2M1 มีระยะห่างระหว่างค่าไม่สม่ำเสมอ และมี dynamic range แบบ floating point ที่กว้างกว่า codebook ของจำนวนเต็มที่มีระยะห่างคงที่ แต่ INT4 ที่ใช้ group size เล็ก ปรับ clipping ให้เหมาะสม หรือใช้ AWQ/GPTQ ก็อาจรักษาความแม่นยำได้ดีมาก การเปรียบเทียบที่ยุติธรรมต้องกำหนด **effective bits, quantized coverage, calibration, kernel, hardware และ benchmark** ให้ตรงกัน

### NVFP4 vs NF4

NF4 ของ QLoRA ออกแบบ codebook ให้เข้ากับ weight distribution และมัก dequantize กลับเป็น BF16/FP16 ระหว่างคำนวณ จุดประสงค์หลักคือประหยัด weight/optimizer memory ระหว่าง parameter-efficient fine-tuning ส่วน NVFP4 ออกแบบร่วมกับ block-scaled Tensor Core execution ดังนั้นคำว่า “4-bit model” ใน bitsandbytes ไม่ได้แปลว่าได้ native NVFP4 throughput

ดูแนวคิด double quantization เพิ่มเติมได้ที่ [[QLoRA]]

---

## 6. Hardware support: โหลดได้ ไม่ได้แปลว่าเร่งด้วย FP4

### Native path

**[เอกสาร NVIDIA]** [TensorRT-LLM quantization support](https://nvidia.github.io/TensorRT-LLM/features/quantization.html) ระบุ NVFP4 บน Blackwell classes เช่น SM100 และ SM120 ตาม feature/backend ขณะที่ [Transformer Engine](https://raw.githubusercontent.com/NVIDIA/TransformerEngine/main/docs/features/low_precision_training/nvfp4/nvfp4.rst) ระบุ NVFP4 training สำหรับ compute capability 10.0 และ 10.3 และ inference API บน SM100+

- Data-center Blackwell ใช้ native FP4 block-scaled Tensor Core instructions
- Blackwell GeForce/RTX-class support ต้องดู runtime และ kernel matrix เพราะ feature coverage อาจไม่เหมือน data-center GPU
- Blackwell รุ่นต่างกันมี peak rates และ memory topology ไม่เท่ากัน

### Older GPU path

A100/Ampere และ H100/Hopper ไม่มี Blackwell FP4 Tensor Core path ดังนั้น framework มีทางเลือกสามแบบ

1. ปฏิเสธ checkpoint/mode
2. emulation/dequantize ไป precision ที่สูงกว่า
3. ใช้ fallback เช่น NVFP4 weight storage แต่คำนวณแบบ **W4A16** ผ่าน Marlin-compatible kernel

vLLM แยก backend ใน code ระหว่าง native CUTLASS/FlashInfer, Marlin fallback และ emulation อย่างชัดเจน การที่ `from_pretrained()` สำเร็จจึงไม่พอ ต้องดู log ว่าเลือก kernel ใด

### CPU หรือ GPU ค่ายอื่น

CPU หรือ GPU ค่ายอื่นอาจอ่าน แปลง หรือจำลอง checkpoint และ metadata ได้ แต่ไม่ได้หมายความว่าจะคำนวณด้วย NVIDIA FP4 Tensor Core โดยตรง จึงย้ายไปใช้ข้ามระบบได้จำกัดกว่ารูปแบบหรือ open kernel ที่มี backend รองรับหลายผู้ผลิต

### Shape และ layout constraints

native kernels มักมีข้อกำหนดด้าน

- `M/N/K` alignment
- block dimension ต้องหารด้วย 16
- scale tensor swizzle/transposition
- padding เช่น scale dimensions ไปยัง multiple เฉพาะ
- tensor-parallel sharding และ MoE expert layout
- supported output/accumulator dtype

Padding ทำให้ checkpoint และ VRAM ที่ใช้จริงมีขนาดมากกว่าที่คำนวณจากสูตรเชิงอุดมคติ โดยเฉพาะ tensor ขนาดเล็กหรือ shape ที่ไม่ตรงกับข้อกำหนดของ kernel

---

## 7. Memory, bandwidth และ throughput: อะไรลดจริง อะไรไม่ลดเอง

### 7.1 Weight capacity

ส่วนที่ได้ประโยชน์โดยตรงที่สุดคือ quantized weights และ scales ทำให้ใช้ GPU น้อยลงเพื่อเก็บโมเดลขนาดใหญ่ หรือเหลือพื้นที่สำหรับ batch/KV cache มากขึ้น แต่ประโยชน์จริงขึ้นกับสัดส่วน layer ที่ quantize

ตัวอย่าง model card ของ NVIDIA

- [Llama-3.1-405B-Instruct-NVFP4](https://huggingface.co/nvidia/Llama-3.1-405B-Instruct-NVFP4) ระบุว่า quantize weights/activations เฉพาะ linear operators ใน Transformer blocks และรายงาน disk/GPU memory ลดประมาณ **3.5× จาก BF16**
- [DeepSeek-R1-0528-NVFP4](https://huggingface.co/nvidia/DeepSeek-R1-0528-NVFP4) เริ่มจาก FP8 และรายงาน actual reduction ประมาณ **1.6×** ไม่ใช่ 1.78× ideal

ความต่างนี้แสดงให้เห็นว่าชื่อ “FP4” ไม่ได้หมายความว่าข้อมูลทุกส่วนในระบบจะใช้พื้นที่ลดลงครึ่งหนึ่ง

### 7.2 Memory bandwidth

เมื่อ GEMM อ่าน weight payload 4 บิตแทน 8/16 บิต ปริมาณข้อมูลจาก HBM ลดลง และ decode ที่ต้อง stream weights ซ้ำอาจได้ประโยชน์มาก แต่ traffic ยังรวม

- E4M3 scales
- unquantized tensors
- activation reads/writes
- KV cache reads/writes
- all-reduce/all-to-all ใน multi-GPU/MoE
- dequantization/fusion overhead

หาก bottleneck อยู่ที่ KV cache หรือ network การลด weight bits อาจไม่เปลี่ยน latency มากเท่าที่คาด

### 7.3 Compute throughput

**[ผล peak ที่ NVIDIA รายงาน]** Table 1 ของงาน pretraining ระบุ FP4 Tensor Core math rate เทียบ BF16 เป็น 4× บน GB200 และ 6× บน GB300 หรือประมาณ 2×/3× เทียบ FP8 ตามลำดับ

ตัวเลขนี้คือ **peak arithmetic rate ของ supported GEMM** ไม่ใช่ tokens/s ทั้ง service เพราะ end-to-end ยังมี attention, normalization, routing, sampling, communication และ CPU/network overhead

### 7.4 Prefill กับ decode ได้ประโยชน์ไม่เหมือนกัน

- **Prefill:** GEMM ใหญ่และ parallelism สูง มัก compute-sensitive จึงขึ้นกับ Tensor Core utilization และ shape
- **Decode:** batch/sequence-dependent และมัก weight-/memory-bandwidth-sensitive จึงอาจได้ประโยชน์จาก weight compression แต่ long context ทำให้ KV/attention traffic เด่นขึ้น

ต้องวัดอย่างน้อย

| มิติ | Metric |
|---|---|
| ผู้ใช้รอคำแรก | TTFT |
| ความลื่นระหว่าง token | ITL หรือ TPOT |
| capacity ทั้งระบบ | output TPS และ RPS |
| memory | peak/steady VRAM แยก weights, KV, workspace |
| คุณภาพ | task score, perplexity, pass rate, human/product metric |
| ต้นทุน | power, GPU count, cost/request หรือ cost/token |

อ่านนิยาม metric เพิ่มได้ใน [LLM Inference Benchmarking: Fundamental Concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/)

### 7.5 KV cache ไม่ได้เล็กลงอัตโนมัติ

W4A4 ของ linear GEMM ไม่ได้กำหนด KV cache precision ปัจจุบัน Model Optimizer มี recipe `NVFP4_KV_CFG` และ `NVFP4_AFFINE_KV_CFG` แต่ต้องมี attention kernel/runtime รองรับ การ quantize KV เพิ่มอาจลด long-context memory มาก แต่เพิ่มอีกหนึ่งแหล่ง quantization error

> **บทวิเคราะห์:** สำหรับ reasoning workload ที่ output ยาว ให้ทดสอบ W4A4 และ KV precision แยกเป็นคนละ experiment มิฉะนั้นจะไม่รู้ว่า quality drop หรือ speedup มาจากส่วนใด

---

## 8. Accuracy: “ใกล้เคียง” ต้องอ่านพร้อมเงื่อนไข

### ทำไม NVFP4 มีโอกาสแม่นกว่า MXFP4/naive FP4

1. block 16 ลด range variation ภายในกลุ่ม
2. E4M3 scale มี mantissa จึงไม่ต้องปัด scale เป็น power of two เท่านั้น
3. FP32 global scale รักษาช่วงรวมของ tensor
4. mixed precision สามารถเว้น sensitive layers
5. calibration/recovery algorithm เลือก scale หรือ layer coverage ให้เข้ากับโมเดล

แต่ทั้งหมดยังไม่กำจัด rounding, zeroing และ saturation

### DeepSeek-R1-0528: ผลที่ NVIDIA รายงาน

model card ระบุ TensorRT-LLM บน B200 และเปรียบเทียบดังนี้

| Benchmark | FP8 reference | NVFP4 | Δ NVFP4 − FP8 |
|---|---:|---:|---:|
| MMLU Pro | 85.0 | 84.2 | −0.8 |
| GPQA Diamond | 81.0 | 80.0 | −1.0 |
| LiveCodeBench | 77.0 | 76.3 | −0.7 |
| SciCode | 40.0 | 40.1 | +0.1 |
| MATH-500 | 98.0 | 98.1 | +0.1 |
| AIME 2024 | 89.0 | 91.3 | +2.3 |

ข้อสรุปที่หลักฐานรองรับคือ **checkpoint นี้รักษาคะแนนไว้ใกล้ FP8 ในการประเมินที่รายงาน** ยังสรุปไม่ได้ว่า “NVFP4 เพิ่ม reasoning 2.3 คะแนน” เพราะชุดทดสอบที่มีจำนวนตัวอย่างจำกัด วิธีเขียน prompt, sampling, evaluation harness และความผันผวนในการวัดอาจทำให้บาง metric สูงขึ้นได้

### Llama-3.1-405B: ผลที่ NVIDIA รายงาน

| Benchmark | BF16 | NVFP4 | Δ |
|---|---:|---:|---:|
| MMLU | 87.3 | 87.2 | −0.1 |
| GSM8K-CoT | 96.8 | 96.1 | −0.7 |
| ARC Challenge | 96.9 | 96.6 | −0.3 |
| IFEval | 88.6 | 89.5 | +0.9 |

คะแนนที่สูงขึ้นใน metric หนึ่งไม่ได้พิสูจน์ว่า quantization ไม่มีผลหรือช่วยได้ในทุกงาน

### โมเดลใหญ่กับโมเดลเล็ก

งาน [QAD ของ NVIDIA](https://arxiv.org/abs/2601.20088) รายงานว่าโมเดลขนาดใหญ่หลายตัวทนต่อความคลาดเคลื่อนจาก NVFP4 PTQ ได้ดีกว่าโมเดลขนาดเล็กหรือโมเดลที่ไวต่อการ quantize ตัวอย่างเช่น Llama Nemotron Super V1 มีคะแนน AIME25 ลดจาก BF16 46.0 เป็น PTQ 32.3 ก่อนใช้ QAD กู้กลับเป็น 45.6 จึงเห็นได้ว่าคุณภาพที่ “ใกล้ lossless” ไม่ได้เกิดขึ้นโดยอัตโนมัติจากการใช้รูปแบบนี้

### Algorithm หลัง AbsMax

- **4/6:** ทดลอง scale ที่ map block max ไป 4 หรือ 6 แล้วเลือก error ต่ำกว่า งาน [4/6](https://arxiv.org/abs/2512.02010) รายงาน improvement โดยไม่เปลี่ยน runtime representation
- **AWQ/GPTQ:** ใช้ activation/sensitivity หรือ reconstruction objective แต่ technique ที่เคยดีบน INT4 ไม่ได้ดีบน NVFP4 เสมอ
- **MSE/FP8 scale sweep:** เลือก E4M3 scale candidate ที่ลด reconstruction error
- **AutoQuantize:** เลือก precision/เว้น quantization ราย layer ภายใต้ effective-bit constraint
- **QAT:** fine-tune ผ่าน fake-quantized forward
- **QAD:** match distribution ของ high-precision teacher ด้วย KL divergence

งาน [ScaleSweep](https://arxiv.org/abs/2606.07618) รายงานการกู้ประสิทธิภาพกลับมาได้ประมาณ 93–95% ในหลายกรณีที่ลด precision ของ weights, activations, KV และ query states อย่างมาก ผลนี้แสดงว่าการ quantize ให้ครอบคลุมส่วนต่าง ๆ มากขึ้นมีต้นทุนด้านคุณภาพที่ต้องพิจารณา

---

## 9. PTQ ทำงานอย่างไร

### Workflow ที่ควรใช้

1. **กำหนด baseline** — ใช้ checkpoint, tokenizer, prompt template และ evaluation harness ชุดเดิมตลอดการเปรียบเทียบ
2. **เลือก target recipe** — W4A4, W4A16, mixed, KV FP8/NVFP4 หรือ selective layers
3. **ตรวจว่ารันได้จริงก่อน quantize** — GPU, runtime, architecture และ shape ต้องรองรับ
4. **เตรียม calibration set** — เป็นตัวแทน distribution จริง ไม่ใช่เพียงข้อความทั่วไปถ้า production เป็น code/math/ภาษาไทย
5. **รัน calibration/algorithm** — max, 4/6, AWQ, MSE, GPTQ หรือ AutoQuantize
6. **export metadata ครบ** — scale dtype, block size, axis, excluded layers และ checkpoint format
7. **offline evaluation** — benchmark หลาย domain + regression prompts + perplexity/logit divergence
8. **performance benchmark** — hardware/runtime เดียวกัน, ISL/OSL/concurrency เดียวกัน
9. **canary/A-B** — ตรวจ product KPI, tail latency, refusal/safety และ rare failures
10. **เก็บ BF16/FP8 ไว้สำหรับย้อนกลับ** — อย่าแทนที่ baseline จนกว่าจะตรวจสอบใน production เสร็จ

NVIDIA PTQ tutorial ยก **128–512 samples** เป็นจำนวนตัวอย่างเริ่มต้นที่ใช้กันบ่อย แต่ไม่ได้รับประกันว่าจะเพียงพอสำหรับทุก domain

### ตัวอย่าง API ระดับแนวคิด

```python
import modelopt.torch.quantization as mtq

# forward_loop ต้องรัน representative calibration data ผ่าน model
model = mtq.quantize(
    model,
    mtq.NVFP4_DEFAULT_CFG,
    forward_loop=forward_loop,
)
```

จากนั้น export เป็น quantized Hugging Face checkpoint ด้วย Model Optimizer API แล้วเปิดด้วย runtime ที่รองรับ metadata นั้น ตัวอย่างนี้แสดงเพียงลำดับการทำงาน โดยไม่ได้ระบุ version หรือ environment ที่แน่นอน ให้ยึด [Model Optimizer guide](https://nvidia.github.io/Model-Optimizer/guides/1_quantization.html) ปัจจุบันเป็นหลัก

### W4A4 กับ W4A16 เลือกอะไร

| Mode | Weight | Activation | เหมาะเมื่อ | Trade-off |
|---|---|---|---|---|
| W4A4 | NVFP4 | NVFP4 | native Blackwell + ต้องการ compute/bandwidth สูงสุด | activation sensitivity และ backend constraints สูง |
| W4A16 | NVFP4 | BF16/FP16 | weight capacity เป็นปัญหา หรือต้อง fallback | compute/activation bandwidth ไม่ลดเท่า W4A4 |
| mixed | หลาย precision | หลาย precision | มี sensitive layers/ops | tuning และ metadata ซับซ้อนขึ้น |
| W4A4 + KV FP4 | NVFP4 | NVFP4 + KV NVFP4 | long context และ kernel พร้อม | quality risk เพิ่มอีกชั้น |

---

## 10. QAT, QAD และ native NVFP4 training ไม่ใช่สิ่งเดียวกัน

### Quantization-Aware Training — QAT

QAT ทำ fake quantization ใน forward เพื่อให้ weights ปรับตัวเข้ากับชุดค่าที่ quantization รองรับ ขณะที่ gradient/optimizer ยังใช้ precision สูง จุดประสงค์คือกู้ความแม่นยำตอน inference ของโมเดลที่ผ่าน pretraining แล้ว

ข้อจำกัดคือ ถ้าโมเดลผ่าน SFT, RL และ model merge มาหลายขั้น การ fine-tune ด้วย task loss อีกครั้งอาจเปลี่ยนพฤติกรรมที่ได้จาก post-training เดิม

### Quantization-Aware Distillation — QAD

QAD ใช้โมเดล precision สูงเป็น teacher และฝึกให้ KL divergence ระหว่างการแจกแจงผลลัพธ์ของ teacher กับ student ต่ำที่สุด แทนการเรียนจาก label อย่างเดียว รายงาน NVIDIA ปี 2026 พบว่า QAD ให้ผลเสถียรกว่า QAT ในโมเดลหลายตัวที่ผ่าน RL/SFT มาเป็นหลัก

ต้นทุนที่เพิ่มคือ

- ต้องเก็บ/รัน teacher
- มี training compute และ data pipeline
- ผลที่ใกล้ BF16 ในงานวิจัยไม่ได้รับประกันว่าจะได้เหมือนกันใน architecture/domain อื่น

### Native quantized pretraining

นี่คือการเร่ง training ตั้งแต่ต้น โดย quantize operands ของ

- forward GEMM — Fprop
- data-gradient GEMM — Dgrad
- weight-gradient GEMM — Wgrad

แต่ยังคง master weights, optimizer states และ accumulation บางส่วนใน FP32/BF16

งานของ NVIDIA ฝึก hybrid Mamba–Transformer 12B บน 10T tokens และรายงาน MMLU-Pro 62.58% เทียบกับ FP8 ที่ 62.62% โดยประเมินผลใน BF16 อย่างไรก็ตาม งานวิจัยระบุชัดว่าเน้นวิธีการคำนวณเชิงตัวเลขมากกว่าประสิทธิภาพของ runtime หรือระบบ

### Recipe ที่ทำให้ training อยู่รอด

Transformer Engine ใช้เทคนิคเพิ่มจาก format พื้นฐาน

1. **selective high precision:** paper ใช้ราว 16% ของ linear layers เป็น BF16 ใน run หลัก และเก็บ embedding, attention components, normalization, nonlinearity, output head ฯลฯ ที่ precision สูง
2. **2D weight scaling:** weights แชร์ scale ต่อ tile 16×16 เพื่อให้ quantized representation สอดคล้องกันตอน transpose ระหว่าง forward/backward แล้ว replicate scale เป็น 1×16 blocks ตอนส่ง Tensor Core เชิงตรรกะ payload + scale เท่ากับ `4 + 8/256 = 4.03125` บิต/weight ก่อน global scale, padding และการ replicate/materialize ตาม layout
3. **Random Hadamard Transform:** กระจาย outlier สำหรับ inputs ของ Wgrad
4. **stochastic rounding เฉพาะ gradients:** ลด bias; weights/activations ใช้ round-to-nearest-even

> **จุดสำคัญ:** เทคนิคเหล่านี้เป็น **training recipe** ไม่ใช่เงื่อนไขบังคับของ PTQ inference ทั่วไป และ 2D weight scaling มีต้นทุนการเก็บ metadata และจัด layout ต่างจากสูตร 4.5 บิตของ block 1×16

---

## 11. Software ecosystem ณ สิงหาคม 2026

| ชั้น | บทบาท | สิ่งที่ต้องตรวจ |
|---|---|---|
| CUDA math types | E2M1 representation/conversion | CUDA/toolkit และ target architecture |
| CUTLASS | block-scaled GEMM kernels/templates | SM, tile shape, scale layout, epilogue |
| Transformer Engine | NVFP4 training/inference recipe | SM100/103 training support, PyTorch/JAX, recipe flags |
| Model Optimizer | PTQ, QAT/QAD helpers, export, AutoQuantize | architecture support, recipe, calibration, export format |
| TensorRT-LLM | production inference/native kernels | hardware matrix, backend, MoE/attention/parallelism |
| vLLM | serving + native/fallback NVFP4 backends | CUTLASS/FlashInfer/Marlin/emulation ที่ถูกเลือกจริง |
| SGLang | serving/online quantization paths | architecture/kernel/version-specific support |
| Hugging Face checkpoints | distribution ของ quantized weights/metadata | model card, license, source precision, quant config |

Model Optimizer ปัจจุบันมี config นอกเหนือจาก `NVFP4_DEFAULT_CFG` เช่น W4A16, KV NVFP4, affine KV, 4/6, AWQ, MSE scale sweep และ mixed MHA recipes ดังนั้น บทความหรือ benchmark ที่เขียนเพียง “NVFP4” โดยไม่ระบุ config จึงนำไปทำซ้ำได้ยาก

NVIDIA มี [Inference Optimized Checkpoints collection](https://huggingface.co/collections/nvidia/model-optimizer-66aa84f7966b3150262481a4) ครอบคลุม Llama, DeepSeek, Qwen, Nemotron, VLM และ diffusion models แต่ทุก model card มี license, runtime และ hardware requirement ของตนเอง

---

## 12. วิธีตรวจ checkpoint ว่าเป็น NVFP4 แบบไหน

ก่อน deploy ให้เปิด quantization config และตอบคำถามเหล่านี้

```text
[ ] weights เป็น NVFP4 ทุก linear หรือเฉพาะ MLP/experts?
[ ] activations เป็น NVFP4 dynamic หรือ static?
[ ] เป็น W4A4, W4A16 หรือ W4A8?
[ ] block size = 16 และ scale dtype = E4M3 จริงหรือไม่?
[ ] มี FP32/global scale ต่อ tensor อย่างไร?
[ ] KV cache precision คือ BF16, FP8 หรือ NVFP4?
[ ] lm_head, embedding, attention, router และ norm ถูกยกเว้นหรือไม่?
[ ] checkpoint ใช้ ModelOpt, compressed-tensors หรือ schema ใด?
[ ] runtime version รองรับ schema/architecture นี้หรือไม่?
[ ] backend เลือก native FP4 kernel หรือ fallback?
```

ชื่อ repository ที่ลงท้าย `-FP4` อาจ redirect ไปยัง `-NVFP4` หรือระบุชื่อนี้ในคำอธิบาย แต่ metadata ภายในเป็นหลักฐานที่สำคัญกว่าชื่อ

---

## 13. Benchmark อย่างไรไม่ให้หลอกตัวเอง

### Quality gate

- ใช้ baseline checkpoint และ tokenizer เดียวกัน
- fix prompt template, few-shot examples, seed และ sampling
- วัด task ที่ production ใช้จริง รวมภาษาไทย/long-context/tool calling ถ้าเกี่ยวข้อง
- รายงาน confidence interval หรือหลาย run สำหรับ benchmark ที่ variance สูง
- ตรวจ logits/perplexity ควบคู่กับ exact-match เพราะ aggregate score อาจซ่อน regression
- ทำ layer/recipe ablation: W4 only → W4A4 → KV quantization
- ตรวจ safety/refusal และ structured-output validity แยกจาก academic accuracy

### Performance gate

- hardware SKU, clocks/power mode, GPU count และ topology เดียวกัน
- runtime/kernel version เดียวกัน
- tensor/pipeline/expert parallel config เดียวกัน
- ISL, OSL, batch, concurrency และ scheduler เดียวกัน
- warmup, CUDA graph และ prefix cache policy เดียวกัน
- รายงานทั้ง median และ p95/p99 TTFT/ITL
- แยก prefill/decode และ online/offline throughput
- บันทึก backend log เพื่อยืนยันว่า native FP4 ถูกใช้

### Memory gate

แยกอย่างน้อย

```text
weights + scales
KV cache
activations
CUDA graph / workspace
communication buffers
allocator fragmentation
host/offload memory
```

ถ้ารายงานเพียง peak VRAM ตัวเดียว จะอธิบายไม่ได้ว่าประโยชน์มาจาก weight compression, batch ที่เพิ่ม หรือ KV precision

---

## 14. ข้อจำกัดและความเสี่ยงที่ควรรู้

1. **Accuracy ไม่แน่นอน:** distribution และ sensitive layer ต่างกันระหว่างโมเดล
2. **Hardware coupling:** native benefit ผูกกับ Blackwell และ runtime kernel ที่รองรับ
3. **Recipe fragmentation:** NVFP4 ชื่อเดียวครอบคลุม W4A4/W4A16/KV/mixed หลายแบบ
4. **Padding/layout overhead:** 4.5 บิตเป็นค่าที่ได้เมื่อ tensor มีขนาดใหญ่มาก ไม่ใช่พื้นที่ที่ทุก tensor ใช้จริง
5. **Unquantized islands:** attention, norm, embedding, router, head หรือท้าย network อาจยัง precision สูง
6. **KV-cache bottleneck:** weight-only quantization ไม่แก้ long-context memory ทั้งหมด
7. **Fallback ambiguity:** framework อาจรันได้แต่ไม่ใช่ native W4A4
8. **Calibration bias:** calibration data ที่ไม่ตรง production ทำให้ activation range ผิด
9. **Rare capability loss:** คะแนน benchmark รวมอาจใกล้เดิม แต่การใช้ tool กรณีโค้ดที่พบไม่บ่อย หรือความสามารถหลายภาษาอาจลดลง
10. **Quantization cost:** AWQ/GPTQ/AutoQuantize/QAT/QAD ใช้เวลาและ compute ไม่เท่ากัน
11. **Version churn:** checkpoint schema, kernels และ support matrix เปลี่ยนเร็ว
12. **Peak vs product:** Tensor Core peak, kernel microbenchmark และ serving throughput เทียบกันตรง ๆ ไม่ได้
13. **Energy attribution:** คำกล่าวเรื่องประสิทธิภาพพลังงานของ Blackwell มักรวม GPU, memory, interconnect, rack/system และ software ไม่ใช่ผลของ NVFP4 เพียงตัวเดียว
14. **Vendor-specific semantics:** MXFP4 มี OCP specification ส่วน NVFP4 เป็น NVIDIA-oriented format/recipe แม้ software หลายโครงการรองรับ

---

## 15. ควรใช้ NVFP4 เมื่อใด

### เหมาะมากเมื่อ

- มี Blackwell ที่ runtime รองรับ native NVFP4
- ต้องการลดจำนวน GPU ที่ใช้เก็บ model weights หรือเพิ่มพื้นที่ให้ batch/KV cache
- decode/serving เป็น memory-bandwidth-sensitive
- มี representative calibration/evaluation data
- ยอมใช้ mixed precision หรือวิธีกู้คุณภาพ หากบาง layer ไวต่อการ quantize
- ทีมวัดคุณภาพและ SLO ซ้ำภายใต้เงื่อนไขเดิมได้

### พิจารณา W4A16 เมื่อ

- ต้องการลด weight memory เป็นหลัก
- activation quantization ทำ accuracy ตก
- hardware/backend ยังไม่มี native W4A4 ที่เหมาะ
- การย้ายไปใช้ข้ามระบบสำคัญกว่าประสิทธิภาพสูงสุดบน Blackwell

### เลือก FP8/BF16 ก่อนเมื่อ

- accuracy margin แคบมากหรือเป็น safety-critical
- deployment อยู่บน Hopper/Ampere เป็นหลัก
- model/operator coverage ของ FP4 ต่ำ
- ไม่มีงบสำหรับ calibration/training
- workload เล็กจน conversion/launch overhead กลบประโยชน์
- ต้องข้าม vendor/runtime หลายแบบ

### Decision tree แบบสั้น

```text
มี native Blackwell backend สำหรับ architecture นี้ไหม?
├─ ไม่มี → FP8/BF16 หรือ W4A16 fallback แล้ว benchmark
└─ มี
   ├─ weight/VRAM/bandwidth เป็นคอขวดไหม?
   │  └─ ไม่ใช่ → NVFP4 อาจไม่คุ้ม complexity
   └─ ใช่
      ├─ PTQ ผ่าน quality gate ไหม?
      │  ├─ ผ่าน → benchmark W4A4 และ deploy canary
      │  └─ ไม่ผ่าน → mixed / 4-6 / AWQ / AutoQuantize / QAD
      └─ long context เป็นคอขวดไหม?
         └─ ใช่ → ทดลอง KV precision แยก ไม่เปิดพร้อมกันแบบ blind
```

---

## 16. FAQ — คำถามที่มักถูกถาม

### NV ใน NVFP4 ย่อมาจาก NVIDIA ใช่ไหม

ชื่อสื่อถึงรูปแบบของ NVIDIA อย่างชัดเจน แต่เอกสารหลักที่ตรวจไม่ได้ให้นิยามทางการว่าอักษร `NV` ย่อมาจากคำใด จึงควรใช้ชื่อ “NVFP4” ตามเอกสาร

### NVFP4 คือ dtype 4 บิตตัวเดียวหรือไม่

คำอธิบายนั้นยังไม่ครบ Payload เป็น E2M1 4 บิต แต่รูปแบบการแทนค่ายังใช้ E4M3/16 และ FP32/tensor scales รวมทั้ง layout/metadata

### เก็บค่าเกิน 6 ได้ไหม

ได้หลัง reconstruction เพราะ `q` ถูกคูณด้วย block/global scales ค่า ±6 เป็นเพียง raw E2M1 maximum

### มี NaN และ Infinity ไหม

finite E2M1 payload ใช้ bit patterns กับ signed finite values/zero ไม่มี NaN/Infinity encoding แบบ FP16/FP32 Pipeline จึงต้องจัดการ non-finite values ก่อน quantization

### NVFP4 เป็น lossless หรือไม่

ไม่ใช่ ค่าเดิมถูกปัดเข้าสู่ E2M1 grid และอาจ underflow เป็น zero หรือ clip/saturate ได้

### ทำไม AIME ของ DeepSeek สูงกว่า FP8

ผลหนึ่ง metric ที่สูงขึ้นอาจเกิดจาก evaluation variance, prompt/sampling และ finite test set ไม่ใช่หลักฐานว่า quantization เพิ่ม reasoning โดยธรรมชาติ

### ลด VRAM 3.5× แน่นอนไหม

อัตราการลดพื้นที่เฉพาะ weight payload จาก 16 บิตเข้าใกล้ 3.56× ได้ในกรณีเชิงอุดมคติ Model card บางตัวรายงานผลจริงราว 3.5× แต่อัตราการลด VRAM ทั้งระบบขณะให้บริการอาจต่ำกว่านั้นมาก

### จาก FP8 ต้องลดได้ 1.8× เสมอไหม

ไม่เสมอไป 1.78× เป็นอัตราส่วนเชิงอุดมคติของรูปแบบการแทนค่า ส่วน DeepSeek model card รายงานอัตราการลดพื้นที่ disk/GPU memory จริงราว 1.6×

### ทำให้ latency เร็ว 2× ไหม

ไม่อัตโนมัติ Peak FP4 math อาจสูงกว่า FP8 2–3× บน Blackwell รุ่นที่ paper ระบุ แต่ end-to-end latency มี non-GEMM และ memory/network bottlenecks

### H100 รัน NVFP4 ได้ไหม

framework บางตัวอาจ fallback/dequantize หรือใช้ W4A16 kernel แต่ H100 ไม่มี native Blackwell FP4 Tensor Core path จึงอย่าอ้างผลแบบ native W4A4

### RTX 50-series ใช้ได้ไหม

TensorRT-LLM ระบุ SM120 support บางส่วน แต่ architecture, operator, mode และ runtime version ต้องอยู่ใน support matrix เดียวกัน ควรตรวจ log/kernel จริง

### KV cache เป็น NVFP4 ด้วยหรือไม่

ไม่ได้เป็นเช่นนั้นโดยค่าเริ่มต้น ต้องเลือก KV recipe และ kernel ที่รองรับ และพิจารณาความเสี่ยงด้านคุณภาพแยกจาก weights/activations

### จำเป็นต้องมี calibration data หรือไม่

ถ้า activation quantization เป็น static ต้องใช้ representative data เพื่อหา scale; dynamic W4A4 บาง recipe หรือ weight-only max อาจไม่ต้องเก็บ activation statistics แต่ยังต้องทำ evaluation

### Quantize layer ทั้งหมดดีที่สุดไหม

ไม่เสมอ งาน training และ QAD แสดงว่าการเก็บ sensitive layers/attention บางส่วนที่ BF16/FP8 ช่วย convergence/accuracy ได้

### ใช้ LoRA หรือ QLoRA กับ NVFP4 ได้ไหม

ทำได้ในบาง toolchain แต่ต้องแยก “base-weight storage”, “compute dtype” และ “adapter training recipe” QLoRA/NF4 ไม่ได้กลายเป็น native NVFP4 เอง และ support เป็น version-specific

### PTQ, QAT, QAD และ NVFP4 training เลือกอะไร

- PTQ: เร็ว/ถูกที่สุด เริ่มที่นี่
- QAT: fine-tune quantized forward ด้วย task loss
- QAD: ใช้ teacher ช่วย preserve output distribution เมื่อ PTQ/QAT ไม่พอ
- native training: ใช้ตั้งแต่ pretraining เพื่อเร่ง Fprop/Dgrad/Wgrad และซับซ้อนที่สุด

### NVFP4 เป็น open standard หรือไม่

E2M1/MX microscaling มีฐานจาก OCP แต่ two-level NVFP4 recipe เป็น NVIDIA-specific; มีเอกสารและ open-source implementations หลายส่วนแต่ไม่ควรเรียกว่า OCP MXFP4

### checkpoint NVFP4 ใช้ข้าม TensorRT-LLM, vLLM และ SGLang ได้เลยไหม

ไม่เสมอไป ต้องตรงกันทั้ง schema, architecture, scale layout, quantized coverage และ runtime version บาง engine รองรับเพียงบางส่วนหรือต้องแปลง metadata ก่อน

### ควรเริ่ม benchmark จากอะไร

เริ่ม 4 จุด: BF16/FP8 baseline, NVFP4 W4A16, NVFP4 W4A4 และ W4A4 + KV precision ที่ต้องการ โดยเปลี่ยนทีละตัวแปร

### สรุปว่า NVFP4 คุ้มไหม

คุ้มเมื่อมี native Blackwell path และ NVFP4 ช่วยลดคอขวดของ workload นั้นได้ แต่ยังใช้แทนรูปแบบเดิมทันทีในทุกระบบไม่ได้ ต้องพิสูจน์ความคุ้มค่าด้วย **throughput และต้นทุนที่วัดภายใต้เกณฑ์คุณภาพเดียวกัน** ในระบบจริง

---

## 17. แยกข้อเท็จจริงจากข้อวิเคราะห์

### ข้อเท็จจริงจาก NVIDIA/เอกสารทางการ

- E2M1 + E4M3 scale/16 + FP32 tensor scale
- raw E2M1 maximum ±6 และ E4M3 maximum 448
- theoretical storage ราว 4.5 บิต/ค่าใน layout 1×16
- TensorRT-LLM/Transformer Engine/Model Optimizer มี NVFP4 support ตาม matrices ของแต่ละโครงการ
- DeepSeek และ Llama model cards รายงาน benchmark/memory ภายใต้ setup ของตน
- training paper รายงาน 12B/10T tokens ใกล้ FP8 เมื่อใช้ recipe และ high-precision exceptions

### ผลจากงานวิจัยที่ออกภายหลัง

- 4/6, scale sweep, QAD และ sensitivity-aware methods ช่วยลด error ในบาง setup
- PTQ อาจทำให้คุณภาพลดลงมากในโมเดลขนาดเล็ก โมเดลที่ไวต่อการ quantize หรือโมเดลที่ผ่าน post-training ซับซ้อน
- technique จาก INT4 เช่น rotation ไม่ได้รับประกันว่าจะช่วย NVFP4

### บทวิเคราะห์ของผู้เรียบเรียง

- ควรมอง NVFP4 เป็นข้อตกลงเรื่องการแทนค่าและการคำนวณที่ทุกส่วนในระบบต้องรองรับตรงกัน
- ไม่ควรใช้อัตราส่วนบิตเชิงอุดมคติแทนผลการวัด VRAM ทั้งระบบหรือ latency
- W4A4 และ KV quantization ควร rollout แยกกัน
- การตัดสินใจควรใช้ quality-adjusted cost/throughput ไม่ใช่ peak TOPS หรือ benchmark เดี่ยว

---

## Sources และอ่านต่อ

### NVIDIA และเอกสาร implementation

1. [Introducing NVFP4 for Efficient and Accurate Low-Precision Inference](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) — แหล่งหลักด้าน inference, format และ DeepSeek-R1
2. [NVFP4 Trains with Precision of 16-Bit and Speed and Efficiency of 4-Bit](https://developer.nvidia.com/blog/nvfp4-trains-with-precision-of-16-bit-and-speed-and-efficiency-of-4-bit/) — ภาพรวม training recipe
3. [CUDA FP4 E2M1 type](https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/struct____nv__fp4__e2m1.html) — low-level type
4. [CUTLASS Blackwell functionality](https://docs.nvidia.com/cutlass/latest/media/docs/cpp/blackwell_functionality.html) — block-scaled Tensor Core kernels
5. [Transformer Engine NVFP4 documentation](https://raw.githubusercontent.com/NVIDIA/TransformerEngine/main/docs/features/low_precision_training/nvfp4/nvfp4.rst) — สูตร scale, 2D scaling, stochastic rounding และ RHT
6. [Model Optimizer quantization guide](https://nvidia.github.io/Model-Optimizer/guides/1_quantization.html) และ [support matrix](https://nvidia.github.io/Model-Optimizer/guides/0_support_matrix.html)
7. [TensorRT-LLM quantization support](https://nvidia.github.io/TensorRT-LLM/features/quantization.html)
8. [vLLM ModelOpt/NVFP4 documentation](https://docs.vllm.ai/en/latest/features/quantization/modelopt/)
9. [NVIDIA inference-optimized checkpoints](https://huggingface.co/collections/nvidia/model-optimizer-66aa84f7966b3150262481a4)

### Specification และงานวิจัย

10. [OCP Microscaling Formats MX v1.0](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf) — official PDF; หาก WAF ปฏิเสธ automated access ให้อ่าน [Microscaling Data Formats for Deep Learning](https://arxiv.org/abs/2310.10537) เป็นแหล่งสำรอง
11. [Pretraining Large Language Models with NVFP4](https://arxiv.org/abs/2509.25149)
12. [4/6: NVFP4 Quantization with Optimal Scaling](https://arxiv.org/abs/2512.02010)
13. [Quantization-Aware Distillation for NVFP4 Inference Accuracy Recovery](https://arxiv.org/abs/2601.20088)
14. [Sensitivity Matters: Toward Accurate and Efficient NVFP4 Quantization](https://arxiv.org/abs/2603.08747)
15. [ScaleSweep: Accurate NVFP4 Post-Training Quantization via Block Scale Initialization](https://arxiv.org/abs/2606.07618)

## Related notes

- [[QLoRA]] — NF4, double quantization และ parameter-efficient fine-tuning
- [[TurboQuant]] — quantization ของ KV cache และ vector/attention path

## Tags: #NVFP4 #FP4 #quantization #NVIDIA #Blackwell #TensorRT-LLM #vLLM #LLM-inference
