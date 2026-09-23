# 025 — Self Healing จากกฎท้องถิ่นซ้ำ ๆ

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 302-308 · [ต้นฉบับ](../original/post.md) · ภาพ: ![NCA cells to pixels](../original/image-29.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์อ้าง `Neural Cellular Automata: From Cells to Pixels` แล้วต่อยอดเป็น proposal เรื่อง NPC self-healing เช่น NPC ที่เคยเจ็บปวดค่อย ๆ ฟื้น motivation เมื่อเวลาผ่านไป ภาพเป็นโพสต์ของผู้เขียน paper และระบุ arXiv `2506.22899` พร้อม demo/code

paper นี้นิยาม Neural Cellular Automata (NCA) เป็น dynamical systems ที่ cell เหมือนกันทั้งหมดใช้ learned local update rule ซ้ำ ๆ จน self-organize เป็น pattern ที่ซับซ้อน มี regeneration, robustness และ spontaneous dynamics ผู้เขียนเสนอให้ NCA วิวัฒน์บน coarse grid แล้วใช้ lightweight implicit decoder แปลง cell state กับ local coordinate เป็น appearance ทำให้ render high resolution ได้และยัง parallelizable ([arXiv:2506.22899](https://arxiv.org/abs/2506.22899)).

สิ่งที่เอามาใช้กับ NPC ได้คือหลัก “local update” ไม่จำเป็นต้องมีผู้กำกับกลาง ทุก tick ให้ affect state ของ NPC อัปเดตจากตัวเอง เพื่อนบ้าน เหตุการณ์ล่าสุด และ decay term เช่น sadness ค่อย ๆ ลดถ้ามี safe interaction แต่เพิ่มเมื่อถูกโจมตี แนวนี้ทำให้ emotional state มี inertia และ recovery เหมือนระบบ dynamical มากกว่า boolean flag

แบบฝึก: ให้ NPC มี vector `[valence, arousal, trust, hunger]` เขียน update rule เดียวกันทุก NPC เช่น `new_valence = 0.95*old + 0.05*neighbor_avg + event_delta` แล้วจำกัดค่าไว้ในช่วง -1 ถึง 1 จากนั้นจำลอง 100 ticks หลังเหตุการณ์ลบ ดูว่า NPC ฟื้นเมื่ออยู่ใกล้เพื่อนหรือมีอาหารพอไหม

ข้อจำกัด: NCA ใน paper เป็นงานภาพ/graphics ที่มีการ train local update rule การนำไปใช้กับจิตใจ NPC เป็น analogy ไม่ใช่ผลวิจัยว่า emotion healing จะ realistic โดยอัตโนมัติ ต้องทดสอบกับ gameplay และ narrative goals

คำถามฝึก: ถ้า healing เร็วเกินไปผู้เล่นจะรู้สึกว่า NPC ไม่มีความทรงจำไหม?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** Neural Cellular Automata สนับสนุน analogy เรื่อง self-healing ของ NPC ได้ถึงระดับไหน? แหล่งใหม่คือ Distill “Growing Neural Cellular Automata” ซึ่งฝึก update rule เดียวให้ cell grid เติบโต คงรูป และ regenerate หลังถูก damage [Distill 2020](https://distill.pub/2020/growing-ca/). ผู้เขียนอธิบายว่า cell state เป็นเวกเตอร์หลาย channel, แต่ละ cell ใช้ neighborhood เล็ก ๆ และ update rule เดียวกันซ้ำ ๆ ส่วน hidden channels ไม่มีความหมายกำหนดล่วงหน้า อีกแหล่งคือ Growing Isotropic Neural Cellular Automata ที่แก้ข้อจำกัด anisotropy เพื่อให้ rule ไม่ผูกกับทิศภายนอกมากเกินไป [arXiv:2205.01681](https://arxiv.org/abs/2205.01681).

**กลไกที่เกี่ยวกับโพสต์:** สิ่งที่ย้ายมาใช้กับ NPC ได้คือ pattern “local state + local perception + repeated update + damage/recovery training” ไม่ใช่ชีววิทยาหรืออารมณ์มนุษย์โดยตรง ถ้า NPC ถูกแฟนทิ้งแล้ว heal ได้ นั่นควรเป็น state dynamics เช่น trust ลด, motivation ลด, social support เพิ่มแล้วค่อยฟื้น ไม่ใช่ claim ว่า NCA พิสูจน์ emotional realism

**ผลเชิงปฏิบัติ:** ออกแบบ emotional NCA แบบเล็กได้โดยให้แต่ละ NPC มี vector `[sadness, trust, energy, social_signal]` และเพื่อนบ้านส่ง signal เฉพาะระยะใกล้ update rule อาจเป็น neural หรือ rule table ก็ได้ สิ่งที่ต้องวัดคือเวลาฟื้น, overshoot, relapse และผลต่อ action ไม่ใช่แค่ภาพ heatmap ดูมีชีวิต

**แบบฝึก:** จำลอง grid 20×20 ให้ node หนึ่งเสีย motivation แล้วให้เพื่อนบ้านช่วยเพิ่ม social signal ทีละ tick เปรียบเทียบ rule ที่ฟื้นเร็วแต่แพร่ panic กับ rule ที่ฟื้นช้ากว่าแต่ stable Caveat คือ NCA ใน Distill ผ่าน gradient training เพื่อ target pattern; ถ้า NPC rule เขียนมือ ต้องทดสอบ stability เอง และ local self-healing อาจสร้าง global side effect ที่ไม่คาดคิด
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 024](024-modelless-zombie-bandit.md) · [โพสต์ 026 →](026-mux-ahla-tpass-lattice.md)

หัวข้อที่เกี่ยวข้อง: [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md) · [05 Memory, adaptation และระบบที่ปรับปรุงตัวเอง](topics/05-memory-and-self-improvement.md)
<!-- POST_NAV_END -->
