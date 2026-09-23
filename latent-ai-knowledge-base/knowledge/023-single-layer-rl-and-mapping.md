# 023 — Layer เดียวอาจพอ แต่ต้องดูงานที่วัด

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 319-327 · [ต้นฉบับ](../original/post.md) · ภาพ: ![single layer RL](../original/image-31.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์ถามจาก paper `Is One Layer Enough? Training A Single Transformer Layer Can Match Full-Parameter RL Training` แล้วโยงไปเรื่องให้ LLM “เข้าไปเล่นเกมใน latent space” โดยไม่ต้อง encode/decode ไปมา ประเด็นหลักคือ adaptation ของโมเดลอาจไม่ได้กระจายเท่ากันทุก layer บาง layer สำคัญกับ RL post-training มากกว่า layer อื่น

arXiv abstract ของ paper นี้รายงานว่า training transformer layer เดียวสามารถ recover gains จาก full-parameter RL ได้มาก และบางกรณีเหนือกว่า โดยนิยาม layer contribution เพื่อวัดส่วนของ improvement ที่ layer นั้นกู้คืนได้ งานทดลองครอบคลุม 7 models, 3 RL algorithms และหลาย domain โดยพบ high-contribution layers กระจุกแถวกลางของ transformer stack ([arXiv:2607.01232](https://arxiv.org/abs/2607.01232)). นี่เป็น claim ของผู้เขียน paper ใน setting ของเขา ไม่ได้บอกว่าโมเดลทุกตัวควรเหลือ layer เดียว

จุดที่ต้องแยกให้ชัดคือ paper นี้พูดเรื่อง “ฝึก/ปรับพารามิเตอร์เพียงหนึ่ง layer ระหว่าง RL post-training” แต่ inference ยังใช้โมเดลลึกทั้งตัวเพื่อ forward ตามปกติ ไม่ใช่ “ตัดโมเดลเหลือหนึ่ง layer ตอนรันจริง” ดังนั้นถ้า KatGPT หรือระบบอื่นพูดว่าใช้ 1 layer/looped layer ตอน inference นั่นเป็นคนละ claim ต้องวัด latency/quality/acceptance แยก ไม่ควรเอาผล paper นี้ไปยืนยันโดยตรง

แนวคิดที่เอาไปเรียนต่อคือ “representation bridge” ถ้าจะให้ latent ของภาษาไปคุยกับ latent ของเกม ต้องมี mapping ที่รักษาความสัมพันธ์สำคัญ เช่น entity, goal, action, constraint มากกว่าการแปลงทุกอย่างกลับเป็น text ภาษาคณิตศาสตร์อาจนึกถึง projection หรือ functor แบบหลวม ๆ แต่ใน implementation ต้องนิยาม input/output และ loss/validator ให้ชัด

แบบฝึก: ทำเกมเล็กที่ state เป็น vector `[hp, hunger, threat_distance, food_distance]` แล้วสร้าง mapping จากคำสั่งภาษา “หาอาหารแต่หลบศัตรู” เป็น goal vector จากนั้นให้ policy ใน latent space เลือก action โดยไม่ generate text ระหว่างทาง วัดผลด้วย survival time และ rule violation

ข้อจำกัด: การฝึก layer เดียวเป็นผลเชิง empirical ของ RL post-training ไม่ใช่หลักฐานว่า reasoning ทั้งหมดอยู่ layer เดียว และ “latent to latent” ลด overhead ได้เฉพาะเมื่อ mapping ถูกต้องพอ

คำถามฝึก: ถ้าคุณเลือกได้แค่หนึ่ง layer ให้ปรับ คุณจะเลือกจาก intuition หรือจาก ablation?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** “ฝึก layer เดียว” อยู่ตรงไหนในครอบครัว parameter-efficient adaptation? แหล่งใหม่คือ LoRA: Low-Rank Adaptation of Large Language Models ซึ่ง freeze น้ำหนักเดิมและเพิ่ม trainable low-rank matrices ใน layer ของ Transformer แทน full fine-tuning [arXiv:2106.09685](https://arxiv.org/abs/2106.09685), [OpenReview LoRA](https://openreview.net/forum?id=nZeVKeeFYf9). LoRA สนับสนุนบทเรียนว่า “จำนวนพารามิเตอร์ที่ฝึก” กับ “จำนวนพารามิเตอร์ที่ใช้ตอน inference” เป็นคนละตัวเลข

**กลไกที่เกี่ยวกับโพสต์:** paper one-layer RL ที่โพสต์อ้างพูดเรื่องการเลือก layer สำคัญสำหรับ RL post-training ส่วน LoRA พูดเรื่องเพิ่ม adapter rank ต่ำในหลาย layer หรือบาง layer ทั้งคู่เป็น adaptation ไม่ใช่การพิสูจน์ว่า inference ใช้ Transformer layer เดียวแล้วพอ ถ้า backbone ยัง forward ครบทุก layer latency หลักยังอยู่กับ backbone แม้ gradient/update จะน้อยลงมาก

**ผลเชิงปฏิบัติ:** การให้ LLM “เข้าไปเล่นเกมใน latent space” ต้องมี bridge ระหว่าง state/action/constraint ของเกมกับ representation ของ model จะใช้ projection, adapter, action decoder หรือ functor-like mapping ก็ต้องระบุ loss และ validator ไม่ควรอ้างผล one-layer RL ไปยืนยัน zero-copy latent-to-latent runtime โดยตรง

**แบบฝึก:** ทำ ablation 3 แบบกับ policy เล็ก: full fine-tune, LoRA/adaptor เฉพาะชั้นกลาง, และ train classifier head อย่างเดียว วัด training step time, VRAM, inference latency และ success rate แยกกัน ถ้า adapter ชนะ training cost แต่ latency เท่าเดิม ให้เขียนผลแบบนั้น Caveat คือ layer contribution ขึ้นกับ model, task, RL algorithm และ distribution shift; layer ที่สำคัญใน paper หนึ่งไม่จำเป็นต้องสำคัญในเกมของเรา
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 022](022-jacobian-space-not-consciousness.md) · [โพสต์ 024 →](024-modelless-zombie-bandit.md)

หัวข้อที่เกี่ยวข้อง: [07 การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก](topics/07-training-and-model-architecture.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
