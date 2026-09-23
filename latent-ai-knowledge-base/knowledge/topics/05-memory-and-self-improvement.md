# Memory, adaptation และระบบที่ปรับปรุงตัวเอง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

## Core lesson

ระบบที่ “ปรับตัวเอง” ไม่ได้มีรูปแบบเดียว บางครั้งคือ retry/backoff จำ node ที่ล่ม, บางครั้งคือ cache ผลตัดสินใจ, บางครั้งคือ trajectory ที่ prompt เดิมกลับมาใช้ได้ง่ายขึ้น, บางครั้งคือ evaluator พัฒนาร่วมกับ agent, บางครั้งคือ corpus code healer โตจาก miss cases. หัวข้อนี้สอนให้แยก **memory**, **context**, **weights**, **cache**, **proof/log**, และ **corpus** ออกจากกันก่อนพูดว่า self-improvement.

ถ้าระบบดีขึ้น ต้องถามเสมอว่าอะไรเปลี่ยน: parameter เปลี่ยนไหม, corpus เพิ่มไหม, prompt/context เปลี่ยนไหม, cache hit มากขึ้นไหม, evaluator อ่อนลงหรือไม่, world state เปลี่ยนหรือไม่.

## โพสต์ที่ประกอบหัวข้อนี้

| Post | ส่วนที่เติมเข้าหัวข้อนี้ |
|---|---|
| [003](../003-memory-salience-adaptive-policy.md) | memory salience ใช้ประวัติ/อารมณ์เทียมปรับ policy |
| [004](../004-nextlat-policy-cache.md) | policy cache จำผล pipeline แทนการคิดซ้ำ |
| [009](../009-trajectory-acquisition-stabilization.md) | TAS เป็นกรอบ/infographic เรื่อง trajectory ที่เข้าถึงง่ายขึ้น ยังไม่ใช่หลักฐานเชิงทดลอง |
| [011](../011-historical-state-ternary-proof.md) | historical reconstruction ต้องระบุ event/snapshot/proof ที่พิสูจน์อะไร |
| [013](../013-meta-sibr-context-routing.md) | SIBR/META-SIBR แยกโหมด context routing แต่ยังเป็น hypothesis/ภาพช่วยคิด |
| [014](../014-red-queen-agents-evaluators.md) | agent และ evaluator co-evolve ได้ แต่ต้องตรึง version/anchor |
| [016](../016-semantic-landscape-knowledge-access.md) | represented, accessible, stable knowledge ช่วยแยกมีข้อมูลกับเรียกใช้ได้ |
| [025](../025-neural-cellular-automata-self-healing.md) | self-healing แบบ local update เป็น analogy จาก NCA ไป emotional state |
| [047](../047-latent-first-neuron-db.md) | neuron-db/corpus healer โตจาก rules, domains, misses และ validators |

## กลไกที่เหมือนและต่างกัน

`003` เป็น short-term adaptive policy: score เปลี่ยนตามเหตุการณ์. `004` เป็น memoization: ผลเก่าถูกเรียกซ้ำเมื่อ key เหมือนพอ. `009` และ `016` เป็น access phenomenon: trajectory หรือ semantic path อาจเปิดง่ายขึ้นจาก prompt/context แต่ไม่ได้แปลว่า weights เปลี่ยน. `011` เป็น audit/proof: reconstruct state ต้องมี event log และ invariant. `014` เป็น meta-learning/evaluation loop: evaluator เปลี่ยนได้แต่ต้องมี anchor. `047` เป็น corpus growth: ระบบ healer ดีขึ้นเพราะ rule/corpus เพิ่ม ไม่จำเป็นต้องเป็น model weight learning.

`025` เป็น local dynamics: state ของ cell/NPC ฟื้นจาก update rule ซ้ำ ๆ ซึ่งเป็น analogy จาก Neural Cellular Automata ไม่ใช่หลักฐานว่า emotion simulation realistic. `013` เป็น routing: หลายบทบาท/บริบท active พร้อมกันได้ แต่ภาพ activation ไม่ใช่ measurement ของสมองหรือโมเดลจริง.

## Worked pipeline: self-improving code healer แบบตรวจได้

1. รับ diagnostic เช่น clippy/perf/security
2. route domain: lint, rust_perf, kernel_opt, sec
3. retrieve rule/corpus ที่เกี่ยวข้อง
4. propose patch
5. validate ด้วย parser/typecheck/test/bench ตามความเสี่ยง
6. ถ้าพลาด บันทึก miss case พร้อมเหตุผล
7. เพิ่ม rule หรือ negative example เข้าคลัง
8. version ทุกอย่าง: `rule_version`, `validator_version`, `corpus_version`

นี่คือ self-improvement แบบไม่ต้องอ้างว่าระบบ “เข้าใจมากขึ้น” ในเชิงลึกลับ สิ่งที่ดีขึ้นคือ coverage ของ corpus, precision/recall ของ rule, และเวลาต่อ fix. หาก validator เปลี่ยน ต้องเทียบกับ anchor เหมือน [014](../014-red-queen-agents-evaluators.md).

## Caveats

อย่าปน cache กับ memory: cache ใช้ซ้ำเมื่อ key valid; memory อาจเปลี่ยนนโยบายแม้ state ไม่เหมือนเดิม. อย่าปน context กับ weights: prompt ที่ดีขึ้นอาจดึงความรู้เดิมได้โดยไม่ update model. อย่าปน evaluator improvement กับ agent improvement: คะแนนสูงขึ้นอาจเพราะผู้ตรวจเปลี่ยน. HRIS TAS/SIBR ใน [009](../009-trajectory-acquisition-stabilization.md) และ [013](../013-meta-sibr-context-routing.md) ควรอ่านเป็น owner-defined hypothesis/infographic ยังไม่ใช่ proven physical map. Ternary proof ใน [011](../011-historical-state-ternary-proof.md) ต้องระบุ property ที่พิสูจน์ ไม่ใช่แค่ใช้ ternary แล้วกลายเป็น proof.

## ลำดับเรียนที่แนะนำ

เริ่มจาก [003](../003-memory-salience-adaptive-policy.md) เพื่อเห็น adaptive policy ง่าย ๆ ต่อด้วย [004](../004-nextlat-policy-cache.md) เพื่อเข้าใจ cache. อ่าน [016](../016-semantic-landscape-knowledge-access.md), [009](../009-trajectory-acquisition-stabilization.md), [013](../013-meta-sibr-context-routing.md) เพื่อแยก access/context/routing. จากนั้นอ่าน [011](../011-historical-state-ternary-proof.md) และ [014](../014-red-queen-agents-evaluators.md) เพื่อเรียนเรื่อง proof/version/evaluator. ปิดด้วย [025](../025-neural-cellular-automata-self-healing.md) และ [047](../047-latent-first-neuron-db.md) เพื่อดู local self-healing กับ corpus-based improvement.

แหล่งหลัก: [AWS Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/), [Microsoft Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), [Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294), [Clippy docs](https://doc.rust-lang.org/clippy/).

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 จัด memory เป็นสามแกนที่ไม่ควรปนกัน: priority ว่าควรหยิบมาทบทวนหรือ retrieve บ่อยแค่ไหน, confidence ว่าเชื่อข้อเท็จจริงแค่ไหน, และ freshness ว่ายังทันโลกปัจจุบันหรือไม่ งาน [Prioritized Experience Replay](https://arxiv.org/abs/1511.05952) ใช้ priority เพื่อ replay transition สำคัญบ่อยขึ้นใน DQN แต่ต้องมี stochastic prioritization/importance sampling เพราะความถี่ในการหยิบไม่เท่ากับความจริงของโลก งาน [In-context Learning and Induction Heads](https://arxiv.org/abs/2209.11895) และ [Lost in the Middle](https://arxiv.org/abs/2307.03172) ช่วยแยกว่า context ที่มีข้อมูลอยู่กับ context ที่โมเดลดึงมาใช้ได้จริงเป็นคนละเรื่อง

เมื่อเชื่อม [โพสต์003](../003-memory-salience-adaptive-policy.md), [โพสต์004](../004-nextlat-policy-cache.md), [โพสต์009](../009-trajectory-acquisition-stabilization.md), [โพสต์011](../011-historical-state-ternary-proof.md), [โพสต์013](../013-meta-sibr-context-routing.md), [โพสต์014](../014-red-queen-agents-evaluators.md), [โพสต์016](../016-semantic-landscape-knowledge-access.md), [โพสต์025](../025-neural-cellular-automata-self-healing.md) และ [โพสต์047](../047-latent-first-neuron-db.md) จะเห็นว่า “ระบบดีขึ้น” อาจเกิดจาก cache hit, corpus เพิ่ม, evaluator เปลี่ยน, context route ดีขึ้น หรือ world state เปลี่ยน ไม่จำเป็นต้องเป็น weight learning

แบบฝึก: ทำ memory table ของ NPC/code-healer มี `fact`, `priority`, `confidence`, `fresh_until`, `evidence`, `validator`, `version` เหตุการณ์ “ยามเห็นซอมบี้ที่ประตูเหนือ” ควร priority สูงทันที แต่ confidence ขึ้นกับ sensor/พยาน และ freshness หมดเมื่อยามลาดตระเวนใหม่ ถ้าแก้ bug แล้ว rule เข้า corpus ให้ผูก validator และ regression case ไม่ใช่เพิ่ม embedding เฉย ๆ การประเมิน self-improvement จึงต้องรายงาน before/after บนชุดตรึง, evaluator version และจำนวน retrieval ที่ใช้จริง
<!-- RESEARCH_REVIEW_2_END -->
