# 054 — TypeSafe Jev เทียบ Local NPC Decision Loop

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 7-15  
รูปประกอบ: ![Jev vs local game arena](../original/image-1.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์เทียบ TypeSafe AI/Jev กับ `katgpt` สำหรับ game NPC โดยภาพ claim ว่า Jev มี latency 70-500 ms network round-trip ส่วน stack ภายในวัดได้ 0.9 µs/NPC และ 1000 NPC ต่อ tick ใน 0.90 ms ที่ 20Hz พร้อม failure mode เช่น `ABSTAIN -> SalienceTriGate -> System-2 escalation`

## ความรู้ที่ค้นเพิ่ม

บทความ official ของ TypeSafe AI แนะนำ Jev เป็น “System One Model” สำหรับ structured decisions ที่ software ใช้ได้โดยตรง ไม่ generate string แบบ LLM ปกติ TypeSafe claim ว่า Jev คืน typed probabilistic decisions, มี confidence, output structure ถูกกำหนดล่วงหน้า และ end-to-end response time 70-500 ms สำหรับบริการของเขา [TypeSafe AI blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev). เขายังบอกชัดว่า Jev ยอมเสียความสามารถ string generation เพื่อ structured outputs

สำหรับเกม real-time ความต่างสำคัญคือ time budget: 20Hz แปลว่าหนึ่ง tick มี 50 ms ถ้า decision ต้อง round-trip network 70 ms ก็ไม่ทันต่อ NPC ต่อ tick แบบ synchronous แต่ Jev อาจเหมาะกับ async decision, high-level planning, content moderation, routing หรือ smart if-statement ที่ไม่ต้องตอบทุก frame

## วิธีลองออกแบบ

แบ่ง NPC brain เป็น 3 ชั้น:

- Reflex: local deterministic/state machine ภายใน 1 ms
- Tactical: local model/search ทุก 5-10 ticks
- Strategic: remote AI หรือ Jev แบบ async เมื่อ latency ยอมรับได้

ถ้า remote answer มาช้า ให้ใช้ abstain/fallback ไม่หยุด simulation

## ข้อควรระวัง

Type-safe output ไม่ได้แปลว่า semantic decision ถูกเสมอ มันแปลว่า schema/type ไม่พัง เช่น enum อยู่ในค่าที่กำหนด แต่ confidence calibration, policy quality และ OOD behavior ยังต้องทดสอบด้วย eval ของเกมจริง ตัวเลข 0.9 µs/NPC เป็น claim ภายในของผู้เขียน ต้องมี reproducible benchmark ก่อนใช้เทียบสาธารณะ

## แหล่งอ้างอิง

- [TypeSafe AI: Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** Guo et al., [On Calibration of Modern Neural Networks (ICML 2017)](https://arxiv.org/abs/1706.04599), Geifman & El-Yaniv, [Selective Classification for Deep Neural Networks (2017)](https://arxiv.org/abs/1705.08500) และ Angelopoulos & Bates, [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification (2021/2022)](https://arxiv.org/abs/2107.07511). งาน calibration ชี้ว่าความน่าจะเป็นที่โมเดลรายงานอาจไม่ตรงกับโอกาสถูกจริง; selective classification ศึกษาการให้โมเดล abstain เพื่อแลก coverage กับ risk; conformal prediction ให้ชุด/ช่วงคำตอบที่มี coverage guarantee ตามระดับที่กำหนดภายใต้เงื่อนไข calibration data/exchangeability ไม่ใช่การรับรองว่าคำตอบเดี่ยว “ฉลาด” หรือเหมาะกับเกมเสมอ

**สิ่งที่ขยายจากโพสต์:** Jev/TypeSafe output ที่มี confidence และ structured decision ยังต้องมี calibration ก่อนใช้เป็น NPC policy. โพสต์มี failure mode `ABSTAIN -> SalienceTriGate -> System-2 escalation`; รอบ 2 เพิ่มว่าการ abstain ดีเมื่อ threshold ผูกกับ risk จริง ไม่ใช่แค่ confidence สูง/ต่ำตาม raw softmax. ถ้าใช้ conformal set กับ action เช่น `{Attack, Flee}` ความหมายคือ “ชุดนี้ควรครอบ label จริงตามสถิติบน distribution คล้าย calibration set” ไม่ใช่ “ทุก action ในชุดถูกต้องทาง gameplay”. เกม real-time ควรวัดทั้ง latency, coverage, set size, abstain rate และ decision risk

**ตัวอย่างทดลอง:** เก็บ state เกม 10,000 ตัวอย่าง แบ่ง in-distribution และ OOD เช่น enemy ใหม่, fog-of-war, stale target. ให้ระบบคืน action + confidence แล้วทำ reliability diagram/ECE แยกต่อ action class. ตั้ง threshold abstain ที่ลด error ใน OOD โดยยังรักษา coverage เช่น 95% ใน ID. สำหรับ Jev remote ให้เพิ่ม metric `deadline_miss_rate`; สำหรับ local NPC ให้เพิ่ม `tick_budget_used`

**ข้อจำกัด:** Calibration/selective classification papers ไม่ได้ประเมิน Jev หรือ katgpt โดยตรง แต่ให้เครื่องมือวัด claim “confidence/abstain” ให้เป็นวิทยาศาสตร์ขึ้น. Type-safe schema ทำให้ output parse ได้ แต่ semantic correctness และ calibration ต้องทดสอบกับ task distribution จริง
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 053](053-paper-flow-and-topic-selection.md) · [โพสต์ 055 →](055-typesafe-jev-diy.md)

หัวข้อที่เกี่ยวข้อง: [03 Neuro-symbolic, constraints, types และการตรวจคำตอบ](topics/03-neuro-symbolic-types-and-verification.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
