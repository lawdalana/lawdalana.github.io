# NPC, world models, เศรษฐกิจเกม และการประสานฝูง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

## Core lesson

โลก NPC ที่ดูมีชีวิตไม่ได้เกิดจาก LLM อย่างเดียว มันเกิดจาก state, memory, reward, rule, coordination และเวลา tick ที่วัดได้ หัวข้อนี้รวมโพสต์ที่เอา latent/state abstraction ไปใช้กับเกม: สัตว์กลัวผู้ล่า, NPC คุยกัน, supply chain ทำให้ราคาขยับ, quest ถูกสร้างตามสถานการณ์, Go agent ใช้ search, และฝูงใช้ signal/coordination ลด compute.

แก่นที่ควรจำคือ “world model” มีหลายความหมาย: paper world model อาจเป็นโมเดลที่ฝึกทำนายอนาคต, เกมจำลองอาจมี explicit state/rules, KatGPT-style อาจใช้ latent/state vector กับ neuro-symbolic pruner. อย่าปน model-free RL กับ no-model/no-training: bandit ใน [024](../024-modelless-zombie-bandit.md) ยังมี policy/reward/update rule แม้ไม่มี neural world model pretrain.

## โพสต์ที่ประกอบหัวข้อนี้

| Post | ส่วนที่เติมเข้าหัวข้อนี้ |
|---|---|
| [003](../003-memory-salience-adaptive-policy.md) | memory/salience ทำให้ node/NPC เลือกพฤติกรรมจากประวัติ |
| [004](../004-nextlat-policy-cache.md) | cache decision pipeline เพื่อลดการคิดซ้ำในสถานการณ์คล้ายเดิม |
| [008](../008-correlated-equilibria-npc-coordination.md) | CCE/mean-field ช่วยคิด coordination ของประชากรจำนวนมาก |
| [010](../010-rust-latent-space-game-world-recap.md) | recap โลกเมือง, economy, day/night, GM tools, Rust/WASM/SIMD caveats |
| [019](../019-quest-generation-throughput.md) | quest grammar/KG/validator แยก throughput จาก LLM generation |
| [020](../020-latent-action-factorization.md) | แยก agent action effect จาก world dynamics/camera |
| [024](../024-modelless-zombie-bandit.md) | bandit simulator แสดง model-free learning ที่ยังมี reward/policy |
| [025](../025-neural-cellular-automata-self-healing.md) | local update rules สร้าง self-healing/emotional dynamics แบบ analogy |
| [028](../028-gcrl-lod-latent-intersection.md) | LOD hierarchy และ cognitive depth สำหรับ MMORPG agent |
| [034](../034-local-npc-scale-claims.md) | scale claims ต้องวัด tick, sync, correctness, replay |
| [037](../037-hello-neuro-symbolic-recap.md) | quest/NPC/latent-to-latent use cases และ Q&A |
| [038](../038-go-puct-rust-wasm-simd.md) | Go arena: model eval + PUCT search |
| [039](../039-katgpt-go-weight-puct-simd.md) | ใช้ weight เดิม แต่เปลี่ยน decision/search layer |

## กลไกที่เหมือนและต่างกัน

`003`, `004`, `019`, `024` ใช้ “หน่วยความจำ” คนละแบบ: salience score สำหรับ adaptive policy, cache สำหรับผล pipeline, KG/quest corpus สำหรับ generation, bandit history สำหรับ reward update. Cache ไม่ใช่ weight; memory ไม่ใช่ context window; context window ไม่ใช่ learned policy.

`008` และ `034` พูดถึงฝูง: mean-field/CCE เป็นกรอบเกมทฤษฎีสำหรับประชากรจำนวนมาก ส่วน claim NPC ล้านความคิดเป็น private benchmark ที่ต้องตรวจ tick/replay/sync. `038` และ `039` เป็นเกมกระดาน: PUCT search ใช้ model/value ไม่ใช่ emotional memory. `020` ช่วยกันความเข้าใจผิดว่า action latent ต้องแยก camera/background ออกจาก actor.

## Worked pipeline: เมืองเล็ก 20 Hz

ออกแบบเมือง 10 NPC:

1. world state: เวลา, อาหาร, ราคา, predator, ร้านค้า, wallet
2. per-NPC state: hunger, fear, trust, location, role
3. memory: เหตุการณ์ล่าสุด เช่น เห็นเหยี่ยว, ร้านปิด, node ล่ม
4. policy: bandit หรือ scorer เลือก `eat/rest/work/flee/trade`
5. coordination: ถ้า predator signal สูง ให้ส่ง summary ระดับ zone ไม่ใช่บอกทุก NPC ทีละคู่
6. verifier: action ต้องเดินถึงได้, item มีจริง, wallet ไม่ติดลบ
7. cache: สถานการณ์ซ้ำใช้ policy template แต่ตรวจ world version ก่อน

ที่ 20 Hz หนึ่ง tick มี 50 ms หาก physics 15 ms, sync 10 ms, rendering/game IO 10 ms เหลือ 15 ms ให้ NPC. อย่าเอา tokenizer throughput หรือ quest throughput มาแทนเวลาทั้ง tick.

## Caveats

คำว่า no if/else ในเกมต้องตีความว่า condition ถูกย้ายเป็น score, rule, validator, หรือ state transition. “Modelless” ใน [024](../024-modelless-zombie-bandit.md) ไม่ใช่ไม่มีโมเดลใด ๆ แต่ไม่มี neural world model pretrain. Cache ใน [004](../004-nextlat-policy-cache.md) ลด compute ได้เฉพาะเมื่อ key ยัง valid; ถ้าโลกเปลี่ยน cache จะพาผิด. ตัวเลข scale/latency จาก [034](../034-local-npc-scale-claims.md), [038](../038-go-puct-rust-wasm-simd.md), [039](../039-katgpt-go-weight-puct-simd.md) ต้อง reproduce ด้วย workload เดียวกัน.

## ลำดับเรียนที่แนะนำ

เริ่มจาก [010](../010-rust-latent-space-game-world-recap.md) เพื่อเห็นภาพเมืองเต็ม แล้วอ่าน [024](../024-modelless-zombie-bandit.md) เพื่อเข้าใจ reward/policy ต่อด้วย [003](../003-memory-salience-adaptive-policy.md) และ [004](../004-nextlat-policy-cache.md) เพื่อแยก memory/cache. อ่าน [008](../008-correlated-equilibria-npc-coordination.md) กับ [028](../028-gcrl-lod-latent-intersection.md) เพื่อ scale เป็นฝูง. จากนั้นอ่าน [019](../019-quest-generation-throughput.md), [037](../037-hello-neuro-symbolic-recap.md), [038](../038-go-puct-rust-wasm-simd.md), [039](../039-katgpt-go-weight-puct-simd.md) เพื่อดู generation และ game search.

แหล่งหลัก: [Boids](https://www.red3d.com/cwr/boids/index.html), [Mean Field Games CCE](https://arxiv.org/abs/2606.20062), [Latent Actions](https://arxiv.org/abs/2606.30544), [AlphaGo Zero](https://www.nature.com/articles/nature24270).

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 เพิ่มแกน “social generalization” ให้ชัด: NPC scale ไม่ใช่แค่จำนวนตัวละคร แต่คือการทำให้พฤติกรรมยังสมเหตุสมผลเมื่อจำนวน agent, density, information flow และ reward coupling เปลี่ยน งาน [Mean Field Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1802.05438) ประมาณปฏิสัมพันธ์จำนวนมากด้วยผลเฉลี่ยของประชากร/เพื่อนบ้าน เพื่อลดความซับซ้อนของ multi-agent RL ส่วน [Generative Agents](https://arxiv.org/abs/2304.03442) สร้างเมืองเล็ก 25 agents ด้วย memory, reflection และ planning ผ่านภาษา แหล่งทั้งสองชี้คนละขั้ว: mean-field ลดรายละเอียดเพื่อ scale; generative agents เพิ่มรายละเอียดเพื่อ believability จึงห้ามเทียบ “จำนวน NPC” ตรง ๆ โดยไม่ดู tick, memory, social events และ latency

ในหัวข้อนี้ [โพสต์003](../003-memory-salience-adaptive-policy.md), [โพสต์004](../004-nextlat-policy-cache.md), [โพสต์008](../008-correlated-equilibria-npc-coordination.md) และ [โพสต์010](../010-rust-latent-space-game-world-recap.md) ควรถูกผูกด้วยคำถามว่า “สรุปข้อมูลระดับใดพอสำหรับการตัดสินใจ” memory/salience ทำให้แต่ละ NPC มีประวัติ, cache ลดการคิดซ้ำ, mean-field ช่วยสรุปปฏิสัมพันธ์ ส่วน regret ใช้ประเมินการเสียโอกาสจากกลยุทธ์ที่เลือก, economy/world state ทำให้การกระทำมีผลย้อนกลับ ขณะที่ [โพสต์019](../019-quest-generation-throughput.md), [โพสต์024](../024-modelless-zombie-bandit.md), [โพสต์034](../034-local-npc-scale-claims.md) เตือนว่าระบบเกมต้องวัด violation ไม่ใช่แค่ throughput

ตัวอย่างทดลอง: เมือง 100 NPC แบ่ง 5 zone เทียบ 3 summary คือ global mean, zone mean, และ neighbor-k รายงาน collision, market shortage, rumor spread time, p95 tick และจำนวน social inconsistency เช่น NPC ใช้ private fact ที่ไม่เคยสังเกตหรือถูกสื่อสารตามกฎ simulation ถ้า global mean เร็วแต่พลาดคอขวดที่ประตูแคบ แปลว่าต้องเพิ่ม locality; ถ้า full memory believability สูงแต่เกิน frame budget ให้เลือก reflection เฉพาะ event สำคัญ ไม่ใช่ทุก tick
<!-- RESEARCH_REVIEW_2_END -->
