# 039 — ใช้ Weight เดิม แต่เปลี่ยนเกมด้วย Search

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 121-128  
รูปประกอบ: ![Tweet about RIIR Moka](../original/image-15.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์เล่าว่าเอา weight ของ Moka มา load เข้า Rust arena แล้วเติม PUCT + SIMD + KatGPT จนชนะ baseline greedy 98%, เร็วกว่า 12.2× และจบระบบประมาณ 273 KB ผู้เขียนย้ำว่าใช้ weight ของเขา ไม่ได้ train net ใหม่ และยังบอกตรง ๆ ว่ายังแพ้ระดับประมาณ 2 kyu หนัก ๆ

ต้นฉบับที่ภาพ quote คือ Moka: repo [`millionco/moka`](https://github.com/millionco/moka) อธิบายว่าเป็น Go-playing model สำหรับ 9×9 Go ขนาดเล็กพอใส่เว็บ, มี policy/value network 105,353 parameters, INT8 weights 114 KB, distilled จาก KataGo b6c96 และมี browser runtime ของตัวเอง นี่ทำให้โพสต์นี้เป็นตัวอย่างของ “เอา model เล็กที่มีอยู่แล้วมาใส่ search/runtime ใหม่” มากกว่า “ค้นพบวิธี train Go ใหม่”

## ความรู้ที่ค้นเพิ่ม

แยก architecture เป็น 4 ชั้นจะเข้าใจง่าย:

1. Weight ให้ policy prior ว่า move ไหนน่าสนใจ
2. Value ประเมินคร่าว ๆ ว่าตำแหน่งน่าชนะหรือแพ้
3. PUCT/MCTS ใช้งบ search ไปกับ branch ที่ทั้งดูดีและยังไม่ถูกลองพอ
4. SIMD ลดเวลาของ forward pass หรือ dot product บางส่วน

AlphaGo Zero ใช้แนวคิดคล้ายกันในระดับใหญ่กว่า: network คืน move probabilities กับ value แล้ว MCTS ใช้ network guide simulation; paper ระบุว่า search probabilities มักเลือก move แข็งกว่า raw network probabilities [AlphaGo Zero PDF](https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf). ต่างกันตรงโพสต์นี้ไม่ได้ train self-play loop แบบ AlphaGo Zero แต่เพิ่ม search เหนือ model เดิม

## ตัวอย่าง PUCT สั้น ๆ

สูตร intuition คือ `Q + exploration_bonus` โดย bonus มาจาก prior และความยังไม่แน่ใจ:

`Q(s,a) + c_puct * P(s,a) * sqrt(total_visits) / (1 + visits_of_a)`

ถ้า move หนึ่งมี `Q` ดีแต่ถูกลองเยอะ bonus จะลดลง ถ้าอีก move มี prior สูงแต่เพิ่งลองน้อย bonus จะดันให้ search ไปดูบ้าง นี่คือเหตุผลที่ PUCT อาจชนะ greedy: greedy เห็นแค่คำตอบชั้นเดียว แต่ PUCT ถามต่อว่า “ถ้าเดินตรงนี้แล้วอีก 3-5 ชั้นเกิดอะไรขึ้น”

## แบบฝึก

ทำ ablation table 4 แถว:

| ระบบ | search | SIMD | สิ่งที่อยากรู้ |
| --- | --- | --- | --- |
| greedy no SIMD | ไม่มี | ไม่มี | baseline policy เดิม |
| greedy SIMD | ไม่มี | มี | SIMD เร่ง forward แค่ไหน |
| PUCT no SIMD | มี | ไม่มี | search เพิ่ม win rate แค่ไหน |
| PUCT SIMD | มี | มี | search ดีขึ้นโดย latency ยังพอรับได้ไหม |

วัด `games won`, `ms/move`, `evals/move`, และ `binary/asset size` จะช่วยตอบว่า win rate เพิ่มจาก search หรือจาก model forward ที่ถูกลง

## ข้อควรระวัง

ตัวเลข 98% ต่อ greedy อ่านเป็น benchmark ภายใน ไม่ใช่ระดับความเก่งทั่วไปของ Go engine การบอกว่า “ไม่ต้อง train” หมายถึงไม่ train เพิ่มในระบบนี้ แต่ความรู้ยังมาจาก Moka/KataGo distillation อยู่ดี และถ้า policy/value มี blind spot, PUCT อาจสำรวจ blind spot นั้นซ้ำมากขึ้น

## แหล่งอ้างอิง

- [millionco/moka GitHub](https://github.com/millionco/moka)
- [AlphaGo Zero PDF](https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf)
- [Rust Portable SIMD](https://doc.rust-lang.org/std/simd/index.html)
- [V8 WebAssembly SIMD](https://v8.dev/features/simd)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งใหม่ 1 — KataGo paper (2019, [arXiv](https://arxiv.org/abs/1902.10565)).** โพสต์นี้พูดว่าเอา weight คนอื่นมา load แล้วเติม PUCT/SIMD แหล่ง KataGo ช่วยเติมบริบทว่า teacher lineage ของ Go network มักไม่ได้ให้เพียง policy move แต่มี value/score/ownership signals ที่ช่วยให้ search ตีความ board state ได้ลึกขึ้น วิธีทดลองใน paper เป็น self-play training และ auxiliary objectives; ผลอยู่ในขอบเขตการฝึก Go ไม่ใช่ข้อพิสูจน์ว่า binary 273 KB หรือ Rust runtime เร็วกว่าเสมอ

**แหล่งใหม่ 2 — AlphaZero “general reinforcement learning algorithm” (2017 preprint, [arXiv](https://arxiv.org/abs/1712.01815)).** คำถามคือ PUCT/search กับ weight เดิมต่างจากการฝึก network อย่างไร AlphaZero ใช้ self-play เพื่อฝึก network แล้วใช้ MCTS ใน loop เดียวกัน; ใช้ arXiv preprint เพื่อให้ตรวจเนื้อหาได้โดยไม่ติด publisher access ขณะที่โพสต์นี้ใช้ network เดิมแล้วเปลี่ยน decision layer ผลที่ควรสรุปจึงแคบกว่า: search อาจทำให้ model เดิมเล่นดีขึ้นเมื่อ prior/value พอใช้ แต่ไม่ได้เท่ากับสร้าง learner แบบ AlphaZero

**ตัวอย่างทดลอง:** ให้ board position เดียวกัน 100 ตำแหน่ง รัน greedy กับ PUCT โดยบันทึก top move, visit distribution, value estimate และ legal move pruning หาก PUCT ชนะ greedy ให้ตรวจว่าเพราะแก้ tactical blunder, เพราะเพิ่ม simulations, หรือเพราะ greedy baseline อ่อน

**ข้อจำกัด:** “ไม่ต้อง train ก็พอเล่นได้” เป็น lesson ที่ถูกในแง่ reuse weight แต่ถ้า distribution ต่างจาก teacher มาก เช่น board size/rules/komi/time control เปลี่ยน PUCT อาจขยาย bias ของ policy/value เดิม การ publish ควรแนบ arena protocol และ SGF/logs
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 038](038-go-puct-rust-wasm-simd.md) · [โพสต์ 040 →](040-kimi-mla-muon-rust-training.md)

หัวข้อที่เกี่ยวข้อง: [02 Latent reasoning, recursion และ search](topics/02-latent-reasoning-and-search.md) · [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
