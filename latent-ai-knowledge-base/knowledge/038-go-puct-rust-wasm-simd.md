# 038 — Go Arena: PUCT, Rust, WASM และ SIMD

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 129-138  
รูปประกอบ: ![Go arena diagram](../original/image-16.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์นี้บอกว่า port ระบบเล่น Go เป็น Rust → WASM + SIMD แล้ว benchmark ภายในเร็วกว่า JavaScript ใน V8 12.2× และเมื่อเพิ่ม PUCT search ก็ชนะ greedy policy 98% โดยใช้ weight เดิม ไม่ใช่ train net ใหม่ ภาพแยก pipeline เป็น `MokaWeights`, `encode_features`, `forward_with_scratch SIMD kernel` แล้วส่งต่อให้ player หลายแบบ เช่น greedy, alpha-beta negamax และ `GoPuctMokaPlayer`.

ต้นทางของ weight ที่ภาพอ้างถึงคือ Moka ของ Aiden Bai/Million: repo [`millionco/moka`](https://github.com/millionco/moka) ระบุว่า Moka v1 เป็น policy/value network สำหรับ Go 9×9 ขนาด 105,353 parameters, INT8 weights 114 KB, run ใน browser และ distilled จาก KataGo b6c96 โดยใช้ teacher games กับ positions จาก rollout ของ Moka เอง จุดนี้สำคัญเพราะ claim ของโพสต์คือ “เปลี่ยน runtime/search รอบ ๆ model” ไม่ใช่ “สร้าง model Go ใหม่จากศูนย์”

## PUCT คืออะไรแบบจับต้องได้

ใน AlphaGo Zero, neural network คืนสองอย่าง: policy prior `P(s,a)` ว่า move ไหนน่าลอง และ value `V(s)` ว่าตำแหน่งนี้น่าชนะไหม จากนั้น MCTS เลือก edge ที่มี `Q(s,a) + U(s,a)` สูง โดย `Q` คือค่าเฉลี่ยจาก simulation เดิม และ `U` เป็น bonus จาก prior กับจำนวนครั้งที่ยังไม่ค่อยได้ลอง [AlphaGo Zero PDF](https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf). สูตรที่ใช้กันบ่อยในสาย AlphaZero เขียนได้ประมาณนี้:

`score(s,a) = Q(s,a) + c_puct * P(s,a) * sqrt(sum_b N(s,b)) / (1 + N(s,a))`

ตัวอย่างเล็ก ๆ: สมมติที่ตำแหน่งหนึ่ง search ไปแล้วรวม 100 ครั้ง, `c_puct = 1`

- move A: `Q=0.60`, `P=0.20`, `N=20` → score ≈ `0.60 + 0.20*10/21 = 0.695`
- move B: `Q=0.50`, `P=0.50`, `N=5` → score ≈ `0.50 + 0.50*10/6 = 1.333`

แม้ A มีค่าเฉลี่ยดีกว่า แต่ B ยังมี prior สูงและถูกลองน้อย จึงควรถูกสำรวจเพิ่ม นี่ต่างจาก greedy ที่เลือก move ที่ policy สูงสุดทันทีแล้วจบ

## ความรู้ที่ค้นเพิ่ม

Moka upstream บอกว่า browser path ของ Moka เล็กกว่า teacher KataGo path มาก และ inference วัดใน Chromium บน Apple Silicon โดยรวม worker messaging ด้วย [Moka README](https://github.com/millionco/moka). ฝั่งโพสต์ของผู้เขียนเพิ่ม Rust/WASM/SIMD และ PUCT เอง ตัวเลข 12.2×, 0.39 ms/pass, 8.7× kernel speedup และ 98% จึงเป็นผลจาก arena ภายในของผู้เขียน ไม่ใช่ผล upstream Moka

เอกสาร Rust ระบุว่า `std::simd` ยังเป็น nightly experimental API และ portable SIMD ไม่ได้รับประกันว่า operation หนึ่งจะกลายเป็น instruction เดียวเสมอ [Rust `std::simd`](https://doc.rust-lang.org/std/simd/index.html). ส่วน V8 อธิบาย WebAssembly SIMD เป็น 128-bit portable operations สำหรับงาน parallel data [V8 WASM SIMD](https://v8.dev/features/simd). ดังนั้นแก่นบทเรียนคือใช้ SIMD ลดต้นทุน model evaluation แล้วให้ PUCT ใช้ evaluation budget ให้คุ้มขึ้น

## แบบฝึก

ทำ tic-tac-toe หรือ Go 5×5 แบบ toy แล้วสร้าง model ปลอมที่คืน `(policy, value)` จาก heuristic จากนั้นเทียบ greedy กับ PUCT ที่ 25/50/100 simulations วัด `win rate`, `ms/move`, `model evals/move` และ `nodes expanded` จะเห็นว่า search ช่วยได้แม้ model เดิม แต่ latency โตตามจำนวน simulation

## ข้อควรระวัง

PUCT ไม่ได้ทำให้ model ถูกเสมอ ถ้า prior/value เพี้ยนมาก search อาจขยายความผิดได้ และ win rate 98% ต่อ greedy ไม่ได้แปลว่าแข็งระดับมนุษย์หรือ KataGo ต้องเทียบหลายคู่แข่ง กติกา seed time control และ hardware เดียวกัน

## แหล่งอ้างอิง

- [millionco/moka GitHub](https://github.com/millionco/moka)
- [AlphaGo Zero PDF](https://discovery.ucl.ac.uk/id/eprint/10045895/1/agz_unformatted_nature.pdf)
- [Rust `std::simd`](https://doc.rust-lang.org/std/simd/index.html)
- [V8 WebAssembly SIMD](https://v8.dev/features/simd)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งใหม่ 1 — “Accelerating Self-Play Learning in Go” (2019, KataGo, [arXiv](https://arxiv.org/abs/1902.10565)).** คำถามคือ model Go ขนาดเล็กใน Moka/KataGo lineage ได้ประโยชน์จากอะไรนอกจาก network policy/value ธรรมดา วิธีของ KataGo เพิ่ม auxiliary targets และวิธีฝึกที่ใช้โครงสร้างเกม Go เช่น ownership/score เพื่อเร่ง self-play learning ผลใน scope ของ paper คือเรียน Go ได้ sample-efficient กว่า baseline self-play ในงานของผู้เขียน ไม่ใช่การรับรอง runtime Rust/WASM ของโพสต์นี้โดยตรง การต่อยอดกับโพสต์คือช่วยอธิบายว่าทำไม “weight เดิม” อาจมี signal มากพอให้ PUCT ใช้ต่อได้ เพราะ policy/value network ไม่ใช่แค่ heuristic ดิบ แต่ถูกฝึกให้ encode เกม Go หลายมิติ

**แหล่งใหม่ 2 — “Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model” (2020, MuZero, [Nature](https://www.nature.com/articles/s41586-020-03051-4)).** คำถามคือ search ต้องรู้ rules/model ของโลกแค่ไหน MuZero แสดงแนวทางเรียน representation, dynamics และ prediction แล้วใช้ MCTS วางแผนโดยไม่ต้องรู้กฎเกมแบบ explicit ในทุก environment วิธีนี้ต่างจากโพสต์ Go arena ที่มี rules ของ Go ชัดและใช้ policy/value จาก Moka แต่เหมือนกันตรง “network ให้ prior/value, search เลือก action”

**ความหมายเชิงปฏิบัติ:** ถ้าจะ reproduce โพสต์นี้ ให้แยก benchmark 3 ชั้น: `forward_with_scratch` ต่อ position, PUCT simulations ต่อ move, และ win rate ต่อ opponent ที่กำหนด ตัวอย่างทดลองคือรัน greedy, PUCT 16 sims, PUCT 64 sims บน weight เดียวกัน แล้ววัดทั้ง `ms/move` และ `winrate` อย่าเอา 12.2× kernel speedup ไปสรุปว่า game strength เพิ่ม 12.2×

**ข้อจำกัด:** KataGo/MuZero เป็น paper training/planning ไม่ใช่หลักฐานของ claim 0.39 ms/pass หรือ 98% ใน arena ภายใน ต้องมี commit, compiler flags, browser/wasm runtime, seed และ opponent list จึงตรวจได้ครบ
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 037](037-hello-neuro-symbolic-recap.md) · [โพสต์ 039 →](039-katgpt-go-weight-puct-simd.md)

หัวข้อที่เกี่ยวข้อง: [02 Latent reasoning, recursion และ search](topics/02-latent-reasoning-and-search.md) · [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md) · [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
