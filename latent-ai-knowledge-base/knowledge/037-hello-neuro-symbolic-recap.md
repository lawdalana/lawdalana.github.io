# 037 — Hello Neuro Symbolic: จากกฎ if/else สู่ระบบ propose-and-prune

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 139-195 · [ต้นฉบับ](../original/post.md) · วันที่ค้นคว้า: 2026-09-20

โพสต์นี้เป็น recap ยาวจาก session “Hello Neuro Symbolic (Rust ep5)” แกนใหญ่คือใช้ latent space + neuro-symbolic reasoning เพื่อสร้าง NPC/quest โดยลด if-else ที่แตกเคสไม่จบ ผู้บันทึกอธิบาย manifold/latent space เป็นโลก representation ที่กำหนดมิติได้, symbolic เป็นสัญลักษณ์/กฎ เช่น หมากรุก, และ neural เป็นการฟังความสัมพันธ์ในพื้นที่ต่อเนื่อง

เมื่อเทียบกับวรรณกรรม neuro-symbolic, แนวคิดหลักตรงกับการรวม neural network-based learning กับ symbolic knowledge representation และ logical reasoning เพื่อให้ได้ทั้งความยืดหยุ่นและการตรวจสอบได้ ([arXiv:2012.05876](https://arxiv.org/abs/2012.05876)). ส่วน Transformer ดั้งเดิมใช้ attention เป็นแกนและเด่นเรื่อง parallelization เมื่อเทียบกับ recurrent/convolutional sequence models ([Google Research](https://research.google/pubs/attention-is-all-you-need/)). โพสต์เสนอว่า KatGPT ใช้ “ทางด่วน” รอบ transformer บางส่วนเพื่อทำ latent-to-latent และ symbolic pruning แต่ claim เฉพาะ implementation ต้องตรวจจาก code/benchmark แยก

หัวข้อย่อยจากต้นฉบับควรแยกก่อนสังเคราะห์:

- Manifold & latent space: latent space ถูกอธิบายเป็นโลกจำลอง/geometry ที่ project state เข้าไปค้นหาคำตอบได้ ต่างจากโลก explicit ที่ต้องเก็บรายละเอียดทุกอย่าง ผู้พูดใช้เกมเป็นภาพจำ: มี state ของตัวเรา เพื่อนบ้าน และ action ที่เกิดจากการ observe state
- Symbolic: กฎและสัญลักษณ์ เช่น หมากรุกหรือ state machine ให้โครงที่ตรวจได้ ข้อสำคัญคือ “ไม่มี if/else” ไม่ได้แปลว่าไม่มีกฎ แต่กฎถูกย้ายไปอยู่ใน symbolic constraints, verifier หรือ pruner
- Neural/NN: neural side ถูกเล่าเป็นการ listening ความสัมพันธ์ในพื้นที่ต่อเนื่อง เช่น ความกลัวของกระต่ายต่อหมาป่า หรือ economic relationship ในเกม ไม่ใช่ condition boolean ทีละบรรทัด
- Transformer/LLM: recap พูดถึง tokenization, self-attention, RLHF, RAG และ cost ของการคิดผ่านข้อความ ความหมายเชิงเรียนรู้คือ LLM ดีที่ language interface แต่แพงและ sequential เมื่อทุกอย่างต้อง decode เป็น token
- Speculative/DFlash/DDTree: จุดนี้มี public research รองรับบางส่วน ไม่ใช่คำภายในทั้งหมด DFlash เป็น speculative decoding framework ที่ใช้ lightweight block diffusion model เพื่อ draft token block แบบขนานแล้วให้ target model verify ([arXiv:2602.06036](https://arxiv.org/abs/2602.06036)). DDTree หรือ Diffusion Draft Tree สร้าง draft tree จาก per-position distributions ของ block diffusion drafter และ verify efficiently ด้วย ancestor-only attention mask ([arXiv:2604.12989](https://arxiv.org/abs/2604.12989)). ส่วนที่เป็น KatGPT-specific คือการเอา DFlash/DDTree ไปผูกกับ constraint pruning, LATTICE, game/quest state หรือ Rust runtime
- Test-time training / T-PASS: recap เปรียบกับเอาโพยเข้าสอบ เรียน/ปรับหน้างานใน latent หรือ runtime แทน retrain model ใหญ่ทั้งหมด ต้องแยกจาก TTT ใน paper ทั่วไป เพราะ implementation KatGPT ยังเป็น claim ภายใน
- Deep manifold / Jacobian / J-Space: เนื้อหาพูดถึงการอ่าน trajectory ผ่าน layer, Jacobian field และ vocabulary directions จุดที่ควรจำคือ Jacobian วัด sensitivity/local causal operator ไม่ใช่หลักฐาน consciousness โดยตรง
- Topology/HLA/AHLA: ตอนท้ายพูดถึง topology, hypersphere/manifold และ HLA ที่รวมข้อมูล higher-order เหมือน function ใน Google Sheets รวมถึงโลกเกมหลายระดับ เช่น global octree, region/zone, near cell, self-cell จาก README ของ `katgpt-rs`, `HLA/AHLA` ถูกวางเป็น Higher-order Linear Attention / O(1) prefix stats และ `LT2 Looped` เป็น weight-shared T-pass loop แบบ hybrid SDPA+AHLA ([katgpt-rs README](https://raw.githubusercontent.com/katopz/katgpt-rs/develop/README.md)). ผมยังไม่พบ public paper ที่ตรงชื่อ AHLA โดยตรง จึงควรแยก method name ใน repo ออกจากหลักฐาน benchmark
- Use cases: quest generation, NPC dialogue เปลี่ยนตาม state, Sudoku solver, customer service emotion classification, local privacy และ latency เป็นกรณีใช้งานที่ต้นฉบับยกขึ้นมา
- Q&A: คำถามสำคัญคือเอา model มาเล่นใน latent อย่างไร ต้นฉบับตอบด้วยแนวคิด mapping layer/ห้องเกมที่ให้ model interact กับ latent state โดยไม่ต้องแปลงกลับเป็น text ทุกก้าว

ภาพรวมเทคนิคจาก recap สามารถจัดเป็น pipeline: observe game state -> encode เป็น latent/state vector -> propose หลาย action/path -> ใช้ symbolic rules prune ทางผิด -> score/rerank -> commit action/quest -> log trajectory เพื่อ replay/debug วิธีนี้ไม่ใช่ “ไม่มี condition” แบบไร้กฎ แต่เปลี่ยน condition จาก if/else กระจัดกระจายเป็น rule/constraint ที่อยู่ใน pruner และ verifier

ตัวอย่าง quest: แทนที่จะเขียน `if npc_has_item && player_level > 5 && dragon_alive...` หลายร้อยบรรทัด ให้ state มี entity/relation เช่น `(dragon threatens city)`, `(npc fears dragon)`, `(player can fight)` แล้ว generator เสนอ quest หลายแบบ pruner ตรวจว่ารางวัลมีจริง, NPC รู้ข้อมูลนั้นจริง, และ quest ไม่ขัด timeline

ตัวอย่าง Sudoku ใน recap ช่วยแยก neural กับ symbolic ชัดขึ้น: neural/latent scorer อาจเสนอ candidate หรือ heuristic path แต่ symbolic rule ตรวจ row/column/box ว่าถูกหรือไม่ ถ้า rule ชัด การ prune ทำให้ search ไม่ต้องเสียเวลาในทางที่ผิด นี่คือแก่น neuro-symbolic ที่จับต้องได้กว่า claim เรื่องความเร็ว

ข้อจำกัด: บันทึกมีคำจำนวนมากที่สถานะไม่เท่ากัน: DFlash/DDTree เป็นชื่อ public speculative decoding papers, AHLA/HLA/T-PASS/LATTICE มีคำอธิบายใน `katgpt-rs` README แต่ benchmark/implementation details ยังต้องตรวจจาก code/bench, ส่วน J-Lane และ META-SIBR ยังเป็น vocabulary-to-verify จากโพสต์นี้ อีกทั้ง model-less ไม่ได้หมายถึงไร้ state/reward/rules และ “หลักล้าน tokens/sec” ต้องแยก token ของ language generation ออกจาก state/action transitions

คำถามฝึก: ในระบบ quest ของคุณ กฎไหนควรเป็น symbolic hard constraint และส่วนไหนควรปล่อยให้ neural/latent scorer เลือกอย่างนุ่มนวล?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** Neuro-symbolic ใน recap ควรแยก “neural proposer” กับ “symbolic verifier” อย่างไร? แหล่งใหม่คือ Neural Logic Machines ซึ่งรวม neural networks กับ logic-style reasoning over objects/properties/relations และรายงาน generalization จากงานขนาดเล็กไปงาน relational ขนาดใหญ่ใน setting ของ paper [Neural Logic Machines](https://arxiv.org/abs/1904.11694). อีกแหล่งคือ Logic Tensor Networks ซึ่งใช้ many-valued differentiable first-order logic เพื่อผสม learning กับ reasoning/query answering [Logic Tensor Networks](https://arxiv.org/abs/2012.13635).

**กลไกที่เกี่ยวกับโพสต์:** Recap บอกว่าไม่มี if-else condition และ quest generation ง่ายขึ้น ควรแปลว่า condition ถูกย้ายเป็น representation, constraint, grammar, score หรือ verifier ไม่ใช่หายไป Neuro-symbolic มีหลายแบบ: symbolic rules อาจสร้าง differentiable loss, neural model อาจเสนอ candidate แล้ว symbolic checker ตัดทิ้ง, หรือ logic อาจอยู่ใน architecture เลย แต่ละแบบมีหลักฐานคนละชนิด

**ผลเชิงปฏิบัติ:** สำหรับ quest/NPC pipeline ให้ใช้ pattern `propose → constrain → verify → commit/abstain` เช่น proposer สร้าง quest candidate, KG บอก entity relation, type schema บังคับ field, economy/timeline verifier ตรวจ invariant แล้วถ้าขัดแย้งให้ rewrite หรือ abstain สิ่งนี้ช่วยลด if/else กระจัดกระจายแต่ยังต้องมี rule data และ test set

**แบบฝึก:** สร้าง quest 20 ตัวจาก state เดียว แล้วให้ verifier ตรวจ 5 invariant: item exists, giver knows target, reward affordable, timeline possible, no duplicate active quest รายงาน accept/reject และเหตุผล Caveat คือ NLM/LTN เป็นงานวิจัยเฉพาะ ไม่ได้ยืนยันว่า KatGPT implementation ใช้กลไกเดียวกัน และ symbolic verifier รับประกันเฉพาะกฎที่เราเขียนไว้เท่านั้น
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 036](036-output-entropy-distillation.md) · [โพสต์ 038 →](038-go-puct-rust-wasm-simd.md)

หัวข้อที่เกี่ยวข้อง: [03 Neuro-symbolic, constraints, types และการตรวจคำตอบ](topics/03-neuro-symbolic-types-and-verification.md) · [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md)
<!-- POST_NAV_END -->
