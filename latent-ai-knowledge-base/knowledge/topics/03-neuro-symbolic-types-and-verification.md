# Neuro-symbolic, constraints, types และการตรวจคำตอบ

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

## Core lesson

Neuro-symbolic ไม่ได้แปลว่าเอา neural network ไปแทนกฎทั้งหมด และ type-safe ไม่ได้แปลว่าตัดสินใจถูกทั้งหมด แก่นของหัวข้อนี้คือการแบ่งงานระหว่าง “ตัวเสนอ” กับ “ตัวตรวจ”: neural/latent scorer เสนอทางเลือก, symbolic/type/grammar/verifier กรองทางเลือกที่ผิด, แล้วระบบตัดสินใจว่าจะ commit, abstain หรือ escalate.

คำว่าไม่มี if/else ในโพสต์หลายอันควรอ่านว่า “ไม่แตกกรณีด้วย imperative if/else กระจัดกระจาย” มากกว่า “ไม่มีกฎ” เพราะกฎยังอยู่ใน lattice, grammar, state machine, type schema หรือ validator.

## โพสต์ที่ประกอบหัวข้อนี้

| Post | ส่วนที่เติมเข้าหัวข้อนี้ |
|---|---|
| [005](../005-category-laws-functional-attention.md) | category laws และ chain rule เป็นตัวอย่างกฎที่ code/test ตรวจได้ |
| [017](../017-lattice-deduction-soundness.md) | lattice deduction แยก correct answer, abstain, coverage |
| [027](../027-latent-first-deterministic.md) | deterministic ช่วย replay/debug แต่ไม่เท่ากับถูกเสมอ |
| [028](../028-gcrl-lod-latent-intersection.md) | LOD/GCRL และ MUX/T-PASS/Lattice วางระดับ state และ reasoning |
| [029](../029-rust-ep5-neuro-symbolic-study-guide.md) | วิธีเรียน session neuro-symbolic และแยกคำ public/project-specific |
| [032](../032-condition-and-reasoning-together.md) | condition กับ reasoning อยู่ใน loop เดียวกันผ่าน constraints/masks/verifier |
| [037](../037-hello-neuro-symbolic-recap.md) | recap ใหญ่ของ propose-and-prune, quest, Sudoku, HLA, Q&A |
| [045](../045-ruliology-program-games.md) | FSM/game theory/ruliology แสดงว่า reasoning บางแบบเป็น program/state transition |
| [054](../054-typesafe-jev-vs-local-npc.md) | Jev ให้ typed probabilistic decisions แต่ latency/schema/semantic correctness ต้องแยก |
| [055](../055-typesafe-jev-diy.md) | architecture และ byte-level grammar → exact function call เป็นเส้นทางสู่ output ที่ตรวจได้ |

## กลไกที่เหมือนและต่างกัน

`005` เป็น verification แบบกฎคณิตศาสตร์เล็ก ๆ เช่น functor law, monoid law, chain rule. `017` เป็น verification แบบลด candidate และแยกคำว่า sound กับ complete. `054` และ `055` เป็น verification ที่ output schema/type: enum ถูก, JSON/function call ถูก, confidence มีรูปแบบอ่านได้. แต่ schema ถูกไม่ได้แปลว่า action ถูกกับโลกจริง.

`027`, `028`, `032`, `037`, `045` พูดเรื่องระบบตัดสินใจ: deterministic replay, LOD state, condition-in-reasoning, finite-state/game programs. เหมือนกันตรงเอากฎเข้ามาใน loop; ต่างกันตรงระดับ abstraction. FSM เหมาะกับ state จำกัด, lattice เหมาะกับ candidate sets, grammar/type เหมาะกับ output shape, verifier เหมาะกับ invariant ของโลก.

## Worked example: quest generator ที่ไม่แตก if/else

โจทย์: สร้าง quest ให้ NPC แต่ต้องไม่ขัดโลกเกม

1. neural/latent proposer เสนอ quest เช่น “ช่วยชาวนาเอานมไปคาเฟ่”
2. symbolic facts มี triples: `(farmer owns cow)`, `(cafe needs milk)`, `(cow alive)`
3. type schema บังคับ output: `{giver, target, item, reward, fail_condition}`
4. verifier ตรวจว่า item มีจริง, giver รู้ข้อมูล, reward มีใน economy, timeline ไม่ขัด
5. ถ้าผ่าน commit; ถ้าไม่ผ่านให้ rewrite; ถ้าไม่มั่นใจ abstain/escalate

ระบบนี้ยังมีกฎเต็มไปหมด แต่กฎอยู่เป็น data/schema/verifier แทน if/else ร้อยบรรทัด. ถ้าต้อง realtime NPC ให้มีชั้น reflex local ก่อน เช่น [054](../054-typesafe-jev-vs-local-npc.md) แนะนำแยก reflex/tactical/strategic.

## Caveats

Deterministic ไม่เท่ากับ correct; deterministic bug ก็ replay ได้สวยมาก. Type-safe ไม่เท่ากับ semantically safe; enum `Attack` อาจถูก schema แต่ผิดสถานการณ์. Neuro-symbolic ไม่ควรเอาไปอ้างว่าไม่ต้อง train เสมอ; บางงาน train neural scorer แล้วใช้ symbolic verifier. DFlash/DDTree เป็น public speculative decoding papers แต่การผูกกับ LATTICE/quest engine เป็น project-specific. Jev official blog ให้ latency/service claims ของเขา ส่วน KatGPT latency ในโพสต์เป็น private benchmark ต้อง reproduce.

## ลำดับเรียนที่แนะนำ

อ่าน [005](../005-category-laws-functional-attention.md) เพื่อเข้าใจ “กฎที่ test ได้” แล้วไป [017](../017-lattice-deduction-soundness.md) เพื่อแยก soundness/coverage. ต่อด้วย [032](../032-condition-and-reasoning-together.md) และ [037](../037-hello-neuro-symbolic-recap.md) เพื่อเห็น pipeline propose-and-prune. อ่าน [045](../045-ruliology-program-games.md) เพื่อเข้าใจว่า FSM/game theory ก็เป็น reasoning ได้ จากนั้นอ่าน [054](../054-typesafe-jev-vs-local-npc.md) และ [055](../055-typesafe-jev-diy.md) เพื่อทำ typed decisions อย่างมี eval.

แหล่งหลัก: [Neurosymbolic AI: The 3rd Wave](https://arxiv.org/abs/2012.05876), [Lattice Deduction Transformers](https://arxiv.org/abs/2605.08605), [TypeSafe AI Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [Wolfram Ruliology of Competition](https://writings.stephenwolfram.com/2026/06/games-between-programs-the-ruliology-of-competition/).

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 เติมแกน “constraints ไม่ใช่ confidence” และ “coverage ไม่ใช่ correctness” งาน [A Gentle Introduction to Conformal Prediction](https://arxiv.org/abs/2107.07511) อธิบายการสร้าง prediction set/interval ที่มี coverage guarantee ตามระดับที่กำหนดภายใต้ exchangeability/calibration ที่เหมาะสม; coverage เป็นสถิติระยะยาว ไม่ใช่คำรับรองรายเคส ขณะที่ [OpenAI Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs) เป็นเอกสารบริการที่อธิบายการผูก output กับ JSON Schema แต่ยังมี edge cases เช่น refusal หรือ max tokens ดังนั้น [โพสต์054](../054-typesafe-jev-vs-local-npc.md) และ [โพสต์055](../055-typesafe-jev-diy.md) ควรเสริมกันแบบนี้: schema ทำให้ parse/route ได้, calibration ทำให้ตัวเลข confidence พอเชื่อได้ขึ้น, conformal set ให้ coverage เชิงสถิติในเงื่อนไขที่ตั้งไว้, verifier ตรวจ invariant ของโลกจริง

เมื่อย้อนกลับไป [โพสต์017](../017-lattice-deduction-soundness.md), [โพสต์027](../027-latent-first-deterministic.md), [โพสต์032](../032-condition-and-reasoning-together.md) และ [โพสต์037](../037-hello-neuro-symbolic-recap.md) จะเห็น pattern เดียวกันคือ propose → constrain → verify → commit/abstain แต่ตัว constraint มีหลายชนิด: functor/type law ใน [โพสต์005](../005-category-laws-functional-attention.md), lattice candidate set, grammar/schema, FSM/ruliology ใน [โพสต์045](../045-ruliology-program-games.md), และ simulator invariant แต่ละชนิดรับประกันแค่พื้นที่ที่มันครอบ ไม่รับประกันความฉลาดทั่วไป

แบบฝึก: ทำ `NpcDecision` ที่คืน conformal set ของ action แทน action เดี่ยว เช่น `{Flee, CallGuard}` โดยต้องมี label/annotation ว่า action ใดถูกใน state นั้นก่อนจึงพูดเรื่อง coverage ได้ จากนั้นให้ verifier เช็ก mana, distance, line-of-sight และ quest state ถ้า world pruner ตัดสมาชิกบางตัวออก coverage guarantee เดิมอาจไม่คงอยู่ เพราะ distribution/conditioning เปลี่ยน ต้อง recalibrate หรือรายงาน coverage หลัง prune ถ้า set ใหญ่เกินจน NPC ลังเล ให้รายงาน set size/abstain rate ไม่ใช้ invalid JSON rate เป็น proxy ของ semantic correctness
<!-- RESEARCH_REVIEW_2_END -->
