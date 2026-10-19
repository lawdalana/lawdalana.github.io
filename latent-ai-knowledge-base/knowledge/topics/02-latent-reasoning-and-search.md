# Latent reasoning, recursion และ search

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

## Core lesson

หัวข้อนี้รวมวิธี “คิดเพิ่ม” ที่ไม่จำเป็นต้องเขียน chain-of-thought เป็นข้อความทุกก้าว แต่กลไกแต่ละแบบไม่เหมือนกัน บางแบบคือ recurrent latent state, บางแบบคือ search tree, บางแบบคือ flow refinement, บางแบบคือ symbolic pruning. สิ่งสำคัญคือแยกว่า compute เพิ่มตรงไหนและ verifier อยู่ตรงไหน

อย่าสับสนสามคู่: **latent recursion** วน hidden state ไม่ใช่ PUCT search, **Flow Reasoning Model** ต้องฝึก flow/recurrent reasoner ไม่ใช่แค่ metaphor ว่าไหลใน latent, และ **ฝึก layer เดียว** ไม่เท่ากับ inference ใช้ layer เดียว. หัวข้อนี้ไม่ได้อยู่เพื่อบอกว่าแบบใดชนะเสมอ แต่อยู่เพื่อเลือกกลไกให้ตรงโจทย์.

## โพสต์ที่ประกอบหัวข้อนี้

| Post | ส่วนที่เติมเข้าหัวข้อนี้ |
|---|---|
| [012](../012-latent-recursive-reasoning.md) | hidden-state loop และ recurrent depth เพิ่ม compute โดยไม่พิมพ์ทุกขั้น |
| [017](../017-lattice-deduction-soundness.md) | lattice/pruning แยก soundness, completeness, abstention |
| [026](../026-mux-ahla-tpass-lattice.md) | MUX/AHLA/T-PASS/LATTICE เป็นภาษาของ packed input, summary, loop, logical cage |
| [030](../030-latent-thought-flows.md) | latent flow เป็นการเดินใน state/geometry ก่อน decode |
| [031](../031-primitive-first-vs-compose-first.md) | primitive ทางคณิตศาสตร์ช่วยเรียน แต่ต้องแยก paper กับ implementation |
| [036](../036-output-entropy-distillation.md) | visual latent optimization ทำให้ distribution มั่นใจขึ้น แต่ไม่รับประกันถูก |
| [038](../038-go-puct-rust-wasm-simd.md) | PUCT/MCTS ใช้ policy prior + value ใน search ไม่ใช่ recurrence |
| [039](../039-katgpt-go-weight-puct-simd.md) | ใช้ weight เดิมแต่เปลี่ยน decision layer ด้วย PUCT/SIMD |
| [050](../050-flow-reasoning-models.md) | FRM ใช้ flow/recurrent refinement และ stability selection |

## กลไกที่เหมือนและต่างกัน

`012`, `030`, และ `050` ดูเหมือน “วนคิดใน latent” แต่ต่างกันมาก. `012` คือ hidden state ถูกป้อนกลับผ่าน block หรือ recurrent depth. `030` เป็น metaphor/แนวคิด latent traversal ว่าก่อน decode เราเดินใน geometry ได้. `050` เป็น paper Flow Reasoning Models ที่มี training และ inference recipe ของตัวเอง ใช้ self-conditioning, re-noise และ dynamic stability กับ structured tasks.

`038` และ `039` คือ search แบบเกม: PUCT/MCTS ไม่ได้ refine hidden state โดยตรง แต่ขยาย tree ของ action/state แล้วใช้ policy/value network เป็น prior และ leaf eval ตามแนว AlphaGo Zero. `017` และ `026` เพิ่มด้าน verifier/pruner: lattice ตัด candidate โดยกฎ, LATTICE ในโพสต์ KatGPT เป็น logical cage ที่ต้องพิสูจน์ว่ากฎครบและไม่ตัดคำตอบถูก.

`036` เป็น multimodal latent optimization: entropy ลดลงแปลว่ามั่นใจขึ้น แต่ถ้า reward หรือ grounding ผิด ความมั่นใจอาจผิดกว่าเดิม.

## Worked pipeline: solver สำหรับ puzzle เล็ก

ลองทำ Sudoku 4x4:

1. encode board เป็น candidate set ต่อช่อง
2. lattice prune ด้วยกฎแถว/คอลัมน์/กล่อง
3. ถ้ายังไม่จบ ใช้ search เลือกช่องที่ candidate น้อยสุด
4. เพิ่ม latent recursion เพื่อให้ scorer ประเมินทางเลือกซ้ำ 2–4 รอบ
5. เพิ่ม flow-style refinement: เติม noise เล็กน้อยให้ candidate board แล้ว repair ซ้ำ
6. verifier ตรวจคำตอบเต็ม ถ้าผ่าน commit ถ้าไม่ผ่าน abstain หรือย้อน search

pipeline นี้ช่วยแยกบทบาท: pruner กันผิดกฎ, search สำรวจทางเลือก, recurrence ใช้ compute เพิ่มกับ state เดิม, flow refinement ทดสอบ stability, verifier เป็นด่านสุดท้าย. ถ้าวัด performance ให้รายงาน coverage ด้วย ไม่ใช่แค่ accuracy เฉพาะข้อที่ตอบ.

## Caveats

PUCT ชนะ greedy ใน Go arena ของ [038](../038-go-puct-rust-wasm-simd.md) เป็น claim เฉพาะ workload และ weight ที่ใช้ ไม่ได้แปลว่า search จะชนะทุก policy. FRM ใน [050](../050-flow-reasoning-models.md) เป็นงาน structured reasoning ที่ฝึกมา ไม่ใช่เพียงคำว่า “flow” ในภาพ. T-PASS/AHLA/LATTICE ใน [026](../026-mux-ahla-tpass-lattice.md) มีคำอธิบายใน `katgpt-rs` README แต่ benchmark และ correctness ต้องตรวจจาก code/bench. Latent recursion ลด token ที่แสดงออกได้ แต่จำนวนรอบคำนวณยังเพิ่มตาม K.

## ลำดับเรียนที่แนะนำ

เริ่มจาก [012](../012-latent-recursive-reasoning.md) เพื่อเข้าใจ loop ใน hidden state แล้วอ่าน [017](../017-lattice-deduction-soundness.md) เพื่อแยก soundness/completeness. ต่อด้วย [038](../038-go-puct-rust-wasm-simd.md) และ [039](../039-katgpt-go-weight-puct-simd.md) เพื่อเห็น search ในเกม จากนั้นอ่าน [050](../050-flow-reasoning-models.md) กับ [036](../036-output-entropy-distillation.md) เพื่อดู refinement/stability. ปิดด้วย [026](../026-mux-ahla-tpass-lattice.md), [030](../030-latent-thought-flows.md), [031](../031-primitive-first-vs-compose-first.md) เพื่อจัดศัพท์และ primitive ให้ไม่ปนกัน.

แหล่งหลัก: [AlphaGo Zero](https://www.nature.com/articles/nature24270), [Flow Reasoning Models](https://arxiv.org/abs/2606.29150), [Coconut](https://arxiv.org/abs/2412.06769), [Lattice Deduction Transformers](https://arxiv.org/abs/2605.08605).

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 เพิ่มภาษากลางสำหรับ “คิดนานขึ้น” ว่าต้องตอบสามคำถาม: ใช้ state เดิมวนซ้ำกี่รอบ, มีเงื่อนไขหยุดอย่างไร, และ verifier อยู่ตรงไหน งาน [Adaptive Computation Time](https://arxiv.org/abs/1603.08983) ให้ RNN เรียนจำนวน step ก่อน emit output โดยมีต้นทุนเวลาแฝง ส่วน [Universal Transformers](https://arxiv.org/abs/1807.03819) ผสม self-attention กับ recurrent processing และใช้แนวคิด dynamic halting ต่อ position แหล่งนี้ช่วยเชื่อม [โพสต์012](../012-latent-recursive-reasoning.md), [โพสต์030](../030-latent-thought-flows.md) และ [โพสต์050](../050-flow-reasoning-models.md): recurrent compute กับการเพิ่ม autoregressive tokens เป็นคนละแกนที่ใช้ร่วมกันได้ และจำนวนพารามิเตอร์คงที่ไม่ได้แปลว่า latency คงที่

ความต่างที่ต้องคงไว้คือ search tree, latent loop และ symbolic pruning แก้คนละปัญหา [โพสต์038](../038-go-puct-rust-wasm-simd.md) กับ [โพสต์039](../039-katgpt-go-weight-puct-simd.md) ซื้อคุณภาพด้วย simulations/action branches; [โพสต์017](../017-lattice-deduction-soundness.md) และ [โพสต์026](../026-mux-ahla-tpass-lattice.md) จำกัดทางเลือกด้วย constraints/abstain ภายใต้สมมติฐานของ verifier; [โพสต์036](../036-output-entropy-distillation.md) ซื้อความมั่นใจของ distribution แต่ยังต้องเช็ก correctness แยก

ตัวอย่างทดลองใหม่: ทำ maze 20×20 ที่มีทางลวง วัด 4 ระบบด้วย wall-clock budget เท่ากัน: greedy one-shot, latent loop K=1/2/4/8 พร้อม early stop เมื่อ verifier ผ่าน, PUCT/search, และ lattice rule ที่ตัด path ชนกำแพง รายงาน solve rate, invalid path, median latency, node expansions และจำนวน step ที่ใช้จริง ถ้า K=8 ดีขึ้นแต่ทุกโจทย์ง่ายหยุดที่ K=2 ได้ บทเรียนคือ halting สำคัญพอ ๆ กับ recurrence ถ้า state นิ่งแต่ path ผิด ต้องเขียนว่า stability ไม่ใช่ proof
<!-- RESEARCH_REVIEW_2_END -->
