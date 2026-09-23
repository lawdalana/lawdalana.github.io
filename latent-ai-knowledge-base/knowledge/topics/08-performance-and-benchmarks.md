# หัวข้อ 08 — อ่านและออกแบบ benchmark ให้เปรียบเทียบได้

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

สังเคราะห์หลังสกัดโพสต์แต่ละอันครบ · วันที่ 2026-09-20 · [กลับสารบัญ](../README.md)

## โพสต์ที่นำมาประกอบ

| โพสต์ | สิ่งที่เพิ่มให้หัวข้อนี้ |
|---|---|
| [008](../008-correlated-equilibria-npc-coordination.md) | ลดความละเอียดของปัญหาต้องวัดคุณภาพที่เสียไป |
| [015](../015-latent-bandwidth-bits.md) | จำนวนบิตไม่ใช่ความเร็วหรือความแม่นยำ |
| [017](../017-lattice-deduction-soundness.md) | accuracy, coverage และ abstention |
| [018](../018-tokenizer-throughput-frame-budget.md) | tokenization กับ game frame budget |
| [019](../019-quest-generation-throughput.md) | สร้างเควสต์กับการสร้างภาษาใช้หน่วยต่างกัน |
| [021](../021-rust-bytemuck-bincode-layout.md) | นับต้นทุนแปลง/คัดลอกข้อมูลให้ครบ |
| [023](../023-single-layer-rl-and-mapping.md) | จำนวน layer ที่ฝึกไม่ใช่จำนวน layer ที่รัน |
| [026](../026-mux-ahla-tpass-lattice.md) | นิยาม N ก่อนอ้าง O(N) |
| [027](../027-latent-first-deterministic.md) | deterministic ไม่ได้แปลว่าเร็วหรือถูกเสมอ |
| [034](../034-local-npc-scale-claims.md) | จำนวน NPC และจำนวนปฏิสัมพันธ์ต้องแยกกัน |
| [038](../038-go-puct-rust-wasm-simd.md) | แยกผล Rust/SIMD ออกจากผล search |
| [039](../039-katgpt-go-weight-puct-simd.md) | win rate ต้องระบุคู่แข่งและงบค้นหา |
| [040](../040-kimi-mla-muon-rust-training.md) | ฝึก, fine-tune และ inference เป็นคนละ phase |
| [041](../041-one-layer-lora-overhead.md) | overhead และ Amdahl limit |
| [042](../042-latent-rag-cargo-heal.md) | หน่วย latency และขอบเขตงาน cargo heal |
| [043](../043-rust-simd-on-gpu.md) | SIMD lane กับ GPU warp เทียบตรง ๆ ไม่ได้ |
| [044](../044-cpu-simd-gpu-crossover.md) | CPU/GPU crossover ตาม workload |
| [048](../048-vllm-katgpt-rs-benchmarking.md) | TTFT, cache และ serving concurrency |
| [049](../049-apple-silicon-local-inference.md) | prefill กับ decode ของโมเดล/เครื่องที่กำหนด |
| [052](../052-llama-cpp-vllm-bragging-gate.md) | bragging gate และการตรวจ regression |
| [054](../054-typesafe-jev-vs-local-npc.md) | network round-trip กับ local decision |

## บทเรียนร่วม

ตัวเลขจะเปรียบเทียบกันได้เมื่อใช้โจทย์ ความหมายของผลลัพธ์ และขอบเขตการจับเวลาตรงกัน โพสต์ในกลุ่มนี้มีทั้ง tokenizer, quest generator, game decision, model kernel และบริการผ่านเครือข่าย จึงควรเริ่มจากระบุชนิดงานก่อนคำนวณ speedup

## หน่วยไหนตอบคำถามอะไร

| ตัววัด | ใช้ตอบคำถาม | สิ่งที่ต้องเขียนกำกับ |
|---|---|---|
| bytes/s และ tokenizer tokens/s | แปลงข้อความได้เร็วเพียงใด | corpus, vocabulary, กฎตัดคำ |
| generated tokens/s | สร้างข้อความใหม่ได้เร็วเพียงใด | model, quantization, prompt/output length |
| decisions/s | เลือก action ได้กี่ครั้ง | state, กฎ, search budget, cache |
| TTFT | รอนานเท่าไรก่อนผลแรก | queue, prefill, network, prefix cache |
| tick p99 | รอบเกมที่ช้ามากใช้เวลาเท่าไร | จำนวน entity, sync, physics, rendering |
| success และ coverage | แก้โจทย์ถูกและยอมตอบมากเพียงใด | test set, abstention, timeout |

รายละเอียดรายกรณีอยู่ใน [018](../018-tokenizer-throughput-frame-budget.md), [019](../019-quest-generation-throughput.md), [048](../048-vllm-katgpt-rs-benchmarking.md) และ [054](../054-typesafe-jev-vs-local-npc.md)

## แยกสาเหตุของความเร็ว

กรณี Go ใน [038](../038-go-puct-rust-wasm-simd.md) เปลี่ยนทั้ง implementation และวิธี search ถ้าต้องการทราบว่าอะไรช่วย ให้ทำตารางสองแกน: JS/Rust กับ greedy/PUCT แล้วใช้ weights, board และงบคำนวณเดียวกัน

กรณี [008](../008-correlated-equilibria-npc-coordination.md) เปลี่ยนปัญหาต่อเนื่องเป็นตารางจำกัด ต้องวัดคุณภาพหลังลดความละเอียด กรณี [023](../023-single-layer-rl-and-mapping.md) ลด layer ที่ฝึก ต้องจับ training time แยกจาก inference time การสรุปว่าเร็วเพราะภาษาหรือ latent จากการเปลี่ยนหลายอย่างพร้อมกันยังแยกเหตุไม่ได้

## ตัวอย่างตัวเลขที่ชวนตีความผิด

- ระบบตอบถูก 20/20 ครั้งที่ยอมตอบ แต่ abstain อีก 80 ข้อ: ความแม่นเฉพาะคำตอบ 100% ขณะที่ coverage 20% ตาม [017](../017-lattice-deduction-soundness.md)
- 1,000 NPC × 0.9 µs = 0.9 ms เป็นการคูณต้นทุนสมมติของ decision เท่านั้น ยังไม่รวมส่วนอื่นของ tick ตาม [054](../054-typesafe-jev-vs-local-npc.md)
- 20 Hz ให้เวลา 50 ms ต่อ tick ส่วน 1,000 × 1,000 อาจหมายถึงหนึ่งล้านคู่ปฏิสัมพันธ์ ไม่ใช่หลักฐานว่ามีหนึ่งล้าน NPC ทำ reasoning ครบวงรอบ ตาม [034](../034-local-npc-scale-claims.md)
- 40,960 บิตเป็นขนาด representation ในตัวอย่าง ไม่ใช่ FLOPs, ความแม่น หรือ tokens/sec ตาม [015](../015-latent-bandwidth-bits.md)

Amdahl ให้ตัวอย่างคำนวณที่ใช้ได้ทั่วไป: หากเร่งส่วนที่กินเวลา 20% ได้ 32 เท่า อัตราเร็วรวมคือ 1/(0.8+0.2/32) ≈ 1.24 เท่า ไม่ใช่ 32 เท่า ต้อง profile ก่อนเลือกส่วนที่จะเร่ง

## แม่แบบ benchmark สำหรับลองเอง

~~~text
โจทย์และ input ที่ทำซ้ำได้:
expected output / เกณฑ์คุณภาพ:
model หรือ policy version:
hardware, runtime, build options:
ขอบเขตที่จับเวลา:
cache: cold / warm / hit rate:
concurrency และ batch:
เวลา p50/p95/p99 และ throughput:
ความถูกต้อง, abstention, timeout:
จำนวนรอบ, ความแปรปรวน, raw logs:
~~~

ให้ correctness gate ผ่านก่อน performance gate แล้วเทียบงานครบเส้นทางกับ kernel แยกกัน เกณฑ์ “ชนะ 1.1 เท่า” ใน [052](../052-llama-cpp-vllm-bragging-gate.md) จะมีความหมายก็ต่อเมื่อมากกว่าความผันผวนและไม่ทำคุณภาพตก การเลือกเฉพาะแถวที่ชนะจะตอบไม่ได้ว่าผู้ใช้งานจริงได้รับประโยชน์หรือไม่

## วิธีอ่านชุดนี้

เริ่ม 018 → 017 → 041 → 044 → 052 แล้วกลับไปดูตัวเลขที่สนใจ ค่าของ KatGPT ในภาพเก็บไว้ในฐานะผลที่ผู้เขียนรายงาน ส่วนตัวอย่างคำนวณในเอกสารนี้เป็นตัวอย่างสอน ไม่ได้รัน benchmark ระบบ KatGPT เพื่อรับรองตัวเลขเหล่านั้น

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 เพิ่มวัฒนธรรม benchmark จากแหล่งที่กำหนด workload ชัดเจนขึ้น Repo [MLPerf Inference](https://github.com/mlcommons/inference) ระบุว่าเป็น benchmark suite สำหรับวัดว่าระบบรันโมเดลได้เร็วเพียงใดในหลาย deployment scenarios และมี reference implementations/rules ส่วน [llmperf](https://github.com/ray-project/llmperf) เป็น harness สำหรับ validate และ benchmark LLMs. แหล่งเหล่านี้ไม่ได้รับรองตัวเลข KatGPT แต่ช่วยนิยามว่า claim เร็วกว่า runtime อื่นต้องมี scenario และ artifact ที่ replay ได้

เมื่อนำไปอ่าน [018](../018-tokenizer-throughput-frame-budget.md), [019](../019-quest-generation-throughput.md), [038](../038-go-puct-rust-wasm-simd.md), [048](../048-vllm-katgpt-rs-benchmarking.md), [052](../052-llama-cpp-vllm-bragging-gate.md) และ [054](../054-typesafe-jev-vs-local-npc.md) จะเห็นว่าหน่วยวัดคนละโลก: tokenizer tokens/s, internal quest transitions/s, generated tokens/s, Go moves/simulations, TTFT/TPOT, network round-trip และ NPC decision/tick ห้ามเอา speedup ข้ามหน่วยมาบวกกัน

ตัวอย่าง actionable คือสร้าง `bench_card.yaml` ต่อหนึ่ง claim: `task`, `model/weights_sha`, `runtime_commit`, `hardware`, `prompt_tokens`, `output_tokens`, `batch`, `concurrency`, `warmup`, `repeats`, `metrics`, `correctness_or_tolerance`, `raw_log`. Gate ให้ผ่านเมื่อ median speedup เกิน threshold และ lower confidence bound ยังชนะ พร้อม output ไม่เปลี่ยนเกิน tolerance. สำหรับเกมให้เพิ่ม `tick_budget`, `active_agents`, `interactions`, `p99_tick_ms`

ข้อจำกัด: MLPerf/llmperf เป็นกรอบ ไม่ใช่ oracle ว่า benchmark local ถูกเสมอ; benchmark ที่ดีต้องเปิด workload เดียวกัน และ speedup เล็กเช่น 1.01x อาจเป็น noise ถ้าไม่มี repeats/statistics
<!-- RESEARCH_REVIEW_2_END -->
