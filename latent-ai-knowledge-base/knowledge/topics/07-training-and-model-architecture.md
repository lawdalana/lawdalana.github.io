# 07 — การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

วันที่สังเคราะห์: 2026-09-20  
หัวข้อนี้แยกคำถามสามชั้น: จะฝึกอะไร, จะใช้ compute ตอน inference อย่างไร, และ architecture เก็บข้อมูลรูปแบบไหนไว้ใน state ภายใน งาน single-layer RL บอกว่าใน setting หนึ่ง การปรับพารามิเตอร์แค่หนึ่ง layer ระหว่าง RL post-training อาจกู้คืน gain จาก full-parameter RL ได้มาก ([post 023](../023-single-layer-rl-and-mapping.md), [arXiv:2607.01232](https://arxiv.org/abs/2607.01232)) แต่ข้อสรุปนี้คนละเรื่องกับการรัน inference ด้วย layer เดียว หรือการวน block เดิมหลายรอบแบบ recurrent depth ([post 012](../012-latent-recursive-reasoning.md), [Scaling up Test-Time Compute](https://arxiv.org/abs/2502.05171)).

## โพสต์ที่นำมาประกอบ

| โพสต์ | บทบาทเฉพาะในหัวข้อนี้ |
| --- | --- |
| [001](../001-topological-neural-operators.md) | เลือก data topology ก่อนเลือก operator |
| [004](../004-nextlat-policy-cache.md) | next-latent และ policy cache สำหรับ reuse decision |
| [005](../005-category-laws-functional-attention.md) | ใช้กฎเป็น validator ของ transformation |
| [012](../012-latent-recursive-reasoning.md) | hidden-state loop: params คงที่ได้ แต่ compute เพิ่ม |
| [023](../023-single-layer-rl-and-mapping.md) | แยก train-one-layer ออกจาก inference-one-layer |
| [026](../026-mux-ahla-tpass-lattice.md) | MUX/AHLA/T-PASS/LATTICE ลด compute คนละจุด |
| [030](../030-latent-thought-flows.md) | เดิน reasoning ใน latent state ก่อน decode เป็นภาษา |
| [031](../031-primitive-first-vs-compose-first.md) | เรียน primitive แบบใช้งาน ไม่จมสมการ |
| [035](../035-hope-rank-one-operators.md) | HOPE มอง neuron เป็น operator สำหรับ compression |
| [036](../036-output-entropy-distillation.md) | inference-time latent optimization และ entropy caveat |
| [040](../040-kimi-mla-muon-rust-training.md) | Kimi K3 เป็นตัวอย่าง architecture+optimizer สเกลใหญ่ |
| [041](../041-one-layer-lora-overhead.md) | runtime overhead ทำให้ลด layer ไม่เท่ากับลด latency |
| [049](../049-apple-silicon-local-inference.md) | generic runtime เทียบ specialized runtime |
| [053](../053-paper-flow-and-topic-selection.md) | วิธีจัด research queue: primitive, evidence, relevance, repro cost |
| [055](../055-typesafe-jev-diy.md) | typed decision architecture: GQA/RoPE/FFN/grammar |

## ความต่างที่ต้องรักษา

กลไกที่ต้องแยกให้ชัด: หนึ่งคือ **train-one-layer vs inference-one-layer**: paper ใน [023](../023-single-layer-rl-and-mapping.md) ปรับพารามิเตอร์ชั้นเดียวระหว่าง RL แต่ forward ยังใช้โมเดลเต็ม การตัด inference เหลือชั้นเดียวเป็น claim ใหม่ที่ต้อง benchmark เอง สองคือ **ตรึงน้ำหนัก backbone vs ไม่มี optimization**: [036](../036-output-entropy-distillation.md) อ้างงานที่ freeze backbone แล้ว optimize latent ตอน inference ([arXiv:2605.02735](https://arxiv.org/abs/2605.02735)); นั่นไม่ใช่ “ไม่มีการเรียนรู้ใด ๆ” เพราะยังมีการปรับ latent และใช้ backbone ที่เคยฝึกมาแล้ว การไม่เปลี่ยนน้ำหนักไม่ได้บอกว่าไม่ใช้ gradient ในตัวแปรอื่น สามคือ **พารามิเตอร์คงที่ vs compute คงที่**: recurrent loop ใน [012](../012-latent-recursive-reasoning.md) ใช้ block เดิมซ้ำได้ แต่เวลาโดยประมาณยังเป็น `K × เวลาต่อรอบ` สี่คือ **representation compression vs correctness**: HOPE ใน [035](../035-hope-rank-one-operators.md) และ NextLat ใน [004](../004-nextlat-policy-cache.md) ช่วยคิดเรื่องย่อ state/subspace แต่ต้อง validate downstream task ห้าคือ **generic runtime vs specialized runtime**: MLX-LM รองรับงานกว้าง ส่วน Lily เฉพาะ Qwen3.6-35B-A3B บน Apple Silicon รายงาน prefill/decode เร็วกว่าใน benchmark ของตน ([049](../049-apple-silicon-local-inference.md), [Perplexity blog](https://www.perplexity.ai/hub/blog/optimizing-on-device-inference-for-apple-silicon)).

## ตัวอย่างและการทดลอง

ตัวอย่างทำงาน: สร้าง NPC decision model ที่รับ state `[hp, hunger, enemy_dist, food_dist]` แล้วออก enum `Attack | Flee | Eat | Patrol | Abstain` เริ่มจาก rule-based, เพิ่ม classifier, แล้วเพิ่ม recurrent pass 1, 2, 4 รอบ ถ้าดีขึ้น ให้ถามว่าเพราะ compute เพิ่มหรือ architecture ดีขึ้น ถ้าจะใส่ GQA/RoPE/FFN ตาม [055](../055-typesafe-jev-diy.md), GQA ลดภาระ KV cache โดยแชร์ key/value บางส่วน ([GQA](https://arxiv.org/abs/2305.13245)), RoPE ใส่ตำแหน่งด้วยการหมุนเวกเตอร์ ([RoFormer](https://arxiv.org/abs/2104.09864)), และ FFN เป็นชั้นแปลง feature ต่อ token ใน Transformer ([Attention Is All You Need](https://arxiv.org/abs/1706.03762)).

แบบฝึก: สำหรับแต่ละ paper ให้กรอก `primitive`, `หลักฐาน`, `เกี่ยวกับ stack เราอย่างไร`, `repro cost` ตาม [053](../053-paper-flow-and-topic-selection.md). ถ้าเจอคำว่า “one layer”, “no training”, “latent”, “O(N)” ให้บังคับเขียนนิยามก่อน เช่น layer ที่ train หรือ layer ที่ run, ไม่เปลี่ยนน้ำหนัก backbone หรือไม่มีการปรับตัวแปรใดเลย, latent ที่มาจาก model ไหน, และ N หมายถึง token/entity/timestep อะไร

ข้อจำกัดคือ benchmark มักขึ้นกับ task, hardware, runtime, batch, quantization และ validator มากกว่าชื่อเทคนิค Rust/Metal/MLA/Muon/GQA ไม่ได้ทำให้ระบบถูกหรือเร็วอัตโนมัติ และ entropy ที่ลดลงไม่ได้แปลว่าคำตอบถูกขึ้นเสมอ ทุก claim ควรมี ablation, seed, workload, latency percentile, quality metric และ failure examples

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 เพิ่มแกนสำคัญคือ “น้ำหนักแช่แข็ง” ไม่เท่ากับ “ไม่มี optimization” และ “ฝึกพารามิเตอร์น้อย” ไม่เท่ากับ “inference ใช้ชั้นน้อย” งาน [LoRA](https://arxiv.org/abs/2106.09685) freeze pretrained weights แล้ว inject trainable low-rank matrices เพื่อลด trainable parameters และ memory ของการปรับงาน downstream ส่วน [ZeRO](https://arxiv.org/abs/1910.02054) แก้ bottleneck การฝึกขนาดใหญ่ด้วยการ partition optimizer states, gradients และ parameters ข้ามอุปกรณ์ ทั้งสองงานเกี่ยวกับ training/fine-tuning memory ไม่ใช่หลักฐานว่า runtime ตอบหนึ่ง token เร็วขึ้นเสมอ

เมื่อเชื่อมโพสต์ [023](../023-single-layer-rl-and-mapping.md), [030](../030-latent-thought-flows.md), [036](../036-output-entropy-distillation.md), [040](../040-kimi-mla-muon-rust-training.md) และ [041](../041-one-layer-lora-overhead.md) จะได้คำอธิบายที่แยกชนิดงานชัดขึ้น: one-layer RL คือเลือกอัปเดตบาง layer ระหว่าง RL post-training; LoRA คือ adapter/low-rank update; latent inference-time optimization อาจ freeze backbone แต่ยัง optimize latent หรือทำ recurrent compute; T-PASS/reused block อาจลด parameter footprint แต่เพิ่มจำนวนรอบ K ตอน inference

ตัวอย่างทดลองสำหรับ topic นี้คือทำตาราง 5 แถว: full fine-tune, LoRA, train-head-only, latent optimization with frozen weights, และ recurrent/test-time loop. คอลัมน์ต้องมี `trainable_params`, `frozen_params`, `optimizer_state_GB`, `inference_layers_executed`, `test_time_steps`, `latency_ms`, `quality_metric`. ตารางนี้ป้องกันการพูดว่า “ไม่ train” ทั้งที่มี optimization หรือพูดว่า “layer เดียว” ทั้งที่ forward ยังผ่าน backbone เต็ม

ข้อจำกัด: LoRA/ZeRO เป็นหลักฐานเชิงวิธีใน setting ของ paper ไม่ได้ยืนยัน architecture ภายใน KatGPT หรือ Kimi/KatGPT split โดยตรง และการลด entropy/confidence loss ต้องวัด correctness แยก เพราะ confidence สูงอาจผิดได้
<!-- RESEARCH_REVIEW_2_END -->
