# 024 — Modelless Simulator ยังมีนโยบายและรางวัล

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 309-318 · [ต้นฉบับ](../original/post.md) · ภาพ: ![zombie sim](../original/image-30.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์เล่า Zombie Escaping Simulator ที่มี NPC หลายบุคลิก เช่น panic, sociable, explorer และ balanced ภาพแสดง grid, zombie target lines, NPC escape vectors, KG stream และ affect sliders ผู้เขียนบอกว่า modelless ไม่มีการ train model ล่วงหน้า แต่ encoder ทำมือแปลงกระดานเป็น 10 มิติ แล้วใช้ bandit strategy เรียนจาก reward เช่น รอด +1, โดนกัด -2, ตาย -50

คำว่า modelless ในที่นี้ควรตีความว่า “ไม่มี neural world model ที่ pretrain” ไม่ใช่ไม่มีโมเดลทางคณิตศาสตร์เลย เพราะยังมี state representation, policy, reward function, และ update rule Bandit เป็นกรอบเรียนรู้แบบเลือก action จากผลตอบแทน โดยไม่ต้องสร้างโมเดล dynamics เต็มของโลก

paper UCB1 ของ Auer, Cesa-Bianchi และ Fischer อธิบาย multi-armed bandit ว่าเป็นปัญหา exploration vs exploitation และเสนอ policy ที่มี finite-time logarithmic regret ภายใต้ reward bounded support ([PDF: Finite-time Analysis of the Multiarmed Bandit Problem](https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf)). ใน simulator นี้ bandit อาจใช้เลือก action/strategy เช่น หนีไปทางไหน เก็บเสบียงไหม หรือเข้าหาฝูงไหม

ตัวอย่างทำเอง: state 10 มิติอาจเป็น `dist_zombie`, `dist_food`, `ally_count_nearby`, `hp`, `hunger`, `panic`, `courage`, `sociability`, `safe_cells`, `tick`. ให้ action 4 ทิศ + stay แล้วเริ่มด้วย epsilon-greedy หรือ UCB บันทึก reward ต่อ NPC personality สิ่งสำคัญคือไม่ต้องเขียน if/else ทุกเคส แต่ยังต้องนิยาม reward และ feature ให้ดี

ข้อจำกัด: ไม่มี if/else ไม่ได้แปลว่าไม่มีเงื่อนไข เงื่อนไขถูกย้ายไปอยู่ใน feature, reward, distance metric หรือ policy update แทน ถ้า reward ผิด NPC จะเรียนพฤติกรรมผิดอย่างมั่นใจ

คำถามฝึก: บุคลิก “ขี้กลัว” ควรเปลี่ยน feature, reward หรือ action selection temperature?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** โพสต์บอก modelless/no train แต่มี bandit learn 1500–3000 epoch ควรเรียกอย่างไรให้ถูก? แหล่งใหม่คือหนังสือ Reinforcement Learning: An Introduction ของ Sutton และ Barto ซึ่งเป็นแหล่งหลักของนิยาม RL, value, policy, reward และ model-free/model-based [Sutton & Barto book](https://incompleteideas.net/book/the-book-2nd.html). อีกแหล่งคือ Auer, Cesa-Bianchi และ Fischer (2002) เรื่อง finite-time analysis ของ multi-armed bandit ซึ่งแสดงปัญหา exploration/exploitation และอัลกอริทึม UCB1 [Finite-time Analysis of the Multiarmed Bandit Problem](https://cesa-bianchi.di.unimi.it/Pubblicazioni/ml-02.pdf).

**กลไกที่เกี่ยวกับโพสต์:** model-free ไม่ได้แปลว่าไม่มี state, ไม่มี policy หรือไม่เรียนเลย แปลว่า agent ไม่เรียน explicit model ของ transition/reward เพื่อวางแผนล่วงหน้า แต่ยัง update estimate ของ action value จาก reward ได้ ใน zombie simulator ที่มี +1 ต่อ tick, -2 เมื่อโดนกัด, -50 เมื่อตาย ระบบกำลังเรียนผ่าน reward signal แม้ encoder 10 มิติจะทำมือและไม่มี neural world model pretrain

**ผลเชิงปฏิบัติ:** คำว่า “ไม่มี if/else” ควรอ่านว่าไม่แตกกฎพฤติกรรมด้วย branch มือจำนวนมาก แต่ยังมี reward shaping, state encoding, action set และ update rule ถ้า reward ผิด agent จะหนีเก่งตาม reward ผิด เช่นยืนใกล้อาหารแต่ไม่ช่วยคนอื่นเพราะ survival reward ให้คะแนนแบบนั้น

**แบบฝึก:** ทำ bandit สำหรับ `flee/group/supply/rest` โดยเก็บค่าเฉลี่ย reward ต่อ action แล้วเพิ่ม epsilon-greedy หรือ UCB เปรียบเทียบ survivor ticks กับ hunger deaths รายงาน learning curve หลัง 500, 1500, 3000 episode Caveat คือ bandit มอง action แยกแบบตื้น ถ้า state สำคัญมากต้องใช้ contextual bandit หรือ RL เต็มรูปแบบ และ deterministic simulator ไม่ทำให้ policy ถูกกับโลกจริงโดยอัตโนมัติ
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 023](023-single-layer-rl-and-mapping.md) · [โพสต์ 025 →](025-neural-cellular-automata-self-healing.md)

หัวข้อที่เกี่ยวข้อง: [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md)
<!-- POST_NAV_END -->
