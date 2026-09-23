# 036 — Unsilencing Visual Latents และ Entropy ที่ลดลง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 196-201 · [ต้นฉบับ](../original/post.md) · ภาพ: ![unsilencing visual latents](../original/image-17.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์พูดถึงโลก latent และ “Stage II monotone output-entropy” จากภาพ/paper ที่ผู้เขียนกำลัง POC ภาพที่แนบเป็น Figure 4 ของ paper `Visual Latents Know More Than They Say: Unsilencing Latent Reasoning in MLLMs` ภาพสรุปสองขั้น: Stage I ทำ query-guided contrastive latent-visual alignment หา positive/negative patches เพื่อ warm-up visual latents; Stage II ทำ latent-to-answer reinforcement ด้วย reward ที่ผลัก output token distributions ให้ concentrated มากขึ้นระหว่าง latent span

arXiv abstract ของ paper นี้บอกว่าปัญหาคือ visual latents ใน MLLM อาจ enriched ทาง semantic ระหว่าง training แต่ contribution ต่อ final answer ถูก suppress เพราะ autoregressive objective ชอบ shortcut จาก direct visual input มากกว่า latent reasoning ผู้เขียนจึง optimize latent reasoning ที่ inference time โดย freeze backbone parameters และรายงานการทดลองบน 8 benchmarks กับ 4 model backbones ([arXiv:2605.02735](https://arxiv.org/abs/2605.02735)).

รายละเอียดจากวิธีการช่วยแยกอีกสองแกน: paper ใช้การรบกวน latent และ NES gradient estimator ใน Stage II แม้ตรึงน้ำหนัก backbone ไว้ และระบุว่า reward ระหว่างรอบ optimization อาจไม่เพิ่มแบบ monotonic จึงเก็บ latent ที่ได้คะแนนดีที่สุดไว้ คำว่า “monotone output-entropy” ในโพสต์ไม่ควรถูกขยายเป็นหลักประกันว่าทุกรอบปรับปรุงต้องดีขึ้น ([วิธีการและสมการ 6](https://arxiv.org/html/2605.02735v1)).

คำว่า output entropy โดยทั่วไปหมายถึงความกระจายของ probability distribution ถ้า entropy ต่ำลง โมเดลมั่นใจในตัวเลือกน้อยตัวมากขึ้น “confidence-progression reward” ใน paper จึงเกี่ยวกับการทำให้ distribution ตาม latent span progressively concentrated แต่ต้องระวัง: distribution ที่มั่นใจขึ้นอาจมั่นใจผิด ถ้า reward หรือ visual grounding ผิด

แบบฝึก: เอาภาพหนึ่งใบกับคำถาม “คนทำอะไรบนบันได” ใช้ VLM หรือ feature extractor หา patch ที่เกี่ยวข้องกับคน/บันได แล้วเทียบคำตอบก่อนและหลัง masking patch ที่ไม่เกี่ยวข้อง ถ้าคำตอบเปลี่ยนมาก แปลว่า latent grounding ยังเปราะ จากนั้นสร้าง distribution คำตอบ 4 ตัวเลือก เช่น `[0.25,0.25,0.25,0.25]`, `[0.55,0.2,0.15,0.1]`, `[0.9,0.04,0.03,0.03]` แล้วคำนวณ entropy เพื่อเห็นว่าความมั่นใจเพิ่มไม่เท่ากับความถูกต้องเสมอ

ข้อจำกัด: paper เป็น inference-time optimization สำหรับ multimodal latent reasoning ไม่ใช่สูตรทั่วไปว่า entropy ต้องลดแล้วคำตอบถูกขึ้นทุกงาน และคำว่า “monotone output-entropy” เป็นคำสรุปในโพสต์/ภาพมากกว่าชื่อ theorem ที่ตรวจจาก abstract ได้โดยตรง

คำถามฝึก: คุณจะจับคู่ entropy กับ verifier อะไรเพื่อแยก “มั่นใจถูก” จาก “มั่นใจผิด”?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** “visual latents know more” ควรผูกกับ representation vision พื้นฐานอย่างไร? แหล่งใหม่คือ CLIP ซึ่งเรียน image-text representation จากคู่ภาพ/ข้อความจำนวนมากและใช้ natural language เป็นตัวอ้างอิง concept สำหรับ zero-shot transfer [CLIP](https://arxiv.org/abs/2103.00020). อีกแหล่งคือ DINOv2 ซึ่งสร้าง all-purpose visual features ด้วย self-supervised training และ distillation [DINOv2](https://arxiv.org/abs/2304.07193). สองงานนี้ช่วยวางพื้นว่าภาพสามารถมี latent/feature ที่มี semantic content ก่อนถึง decoder คำตอบ

**กลไกที่เกี่ยวกับโพสต์:** Paper Unsilencing Visual Latents อ้างว่าระหว่าง training visual latents อาจ enriched แต่ contribution ต่อคำตอบถูก suppress โดย autoregressive objective จึง optimize latent reasoning ตอน inference โดย freeze backbone แยก Stage I alignment กับ Stage II confidence-progression reward ประเด็นสำคัญคือ “no parameter update” ไม่ได้แปลว่าไม่มี optimization; ยังมี gradient/การปรับ latent ตอน inference

**ผลเชิงปฏิบัติ:** ถ้าจะ POC ในระบบตัวเอง ให้แยกสามค่า: semantic alignment ของ visual patch, entropy/confidence ของ output distribution และ correctness จาก label/verifier Entropy ลดลงแค่บอกว่า distribution กระจุกขึ้น ถ้า grounding ผิดก็เป็นความมั่นใจผิดได้

**แบบฝึก:** ใช้ภาพหนึ่งใบ สร้างคำถามแบบ multiple choice แล้วบันทึก probability ก่อน/หลัง latent optimization หรือ patch masking คำนวณ entropy และ accuracy แยกกัน ถ้า entropy ลดแต่คำตอบผิด ให้เขียน failure case ว่า reward ดัน shortcut Caveat คือ CLIP/DINOv2 เป็น representation foundation ไม่ใช่ proof ว่าทุก MLLM มี latent reasoning ที่ถูกซ่อนอยู่
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 035](035-hope-rank-one-operators.md) · [โพสต์ 037 →](037-hello-neuro-symbolic-recap.md)

หัวข้อที่เกี่ยวข้อง: [02 Latent reasoning, recursion และ search](topics/02-latent-reasoning-and-search.md) · [07 การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก](topics/07-training-and-model-architecture.md)
<!-- POST_NAV_END -->
