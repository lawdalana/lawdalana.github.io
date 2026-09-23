# 026 — จาก O(N²) สู่ O(N) ต้องบอกว่าลดตรงไหน

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 288-301 · [ต้นฉบับ](../original/post.md) · ภาพ: ![optimization hub](../original/image-28.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์สรุปส่วนประกอบ KatGPT ว่า MUX รวม signal, AHLA map summary, T-PASS วน reasoning, LATTICE เป็น neuro-symbolic rules/pruner แล้วอ้างว่าจาก O(N²) เหลือ O(N), zero-allocation, pure Rust ภาพใช้ analogy เป็น optimization hub แยก spatial packing, temporal compression, recursive depth และ logical cage โดยภาพกำหนดบทบาทเฉพาะไว้ชัด: MUX = spatial packing รวม dialogue/game logic/entity memory เป็น super-stream, AHLA = temporal compression อัปเดต compact summary ledger แทน history ก้อนใหญ่, T-PASS = recursive depth ใช้ block เดียววนหลายรอบเพื่อจำลองความลึก, LATTICE = logical cage ที่ปล่อย valid step และ prune contradiction ทันที

แหล่งภายนอกช่วยวางกรอบได้: Transformer ดั้งเดิมเสนอ architecture ที่ parallelizable กว่า recurrent/convolutional model ([Google Research: Attention Is All You Need](https://research.google/pubs/attention-is-all-you-need/)) แต่ standard self-attention มีต้นทุน O(n²) ตาม sequence length; Linformer เสนอ approximation เพื่อลด self-attention จาก O(n²) เป็น O(n) ใน time/space สำหรับกลไกของมันเอง ([arXiv:2006.04768](https://arxiv.org/abs/2006.04768)). นี่สนับสนุนว่า “ลด quadratic attention” เป็นแนววิจัยจริง แต่ไม่ได้ยืนยัน implementation KatGPT

สำหรับชื่อ project-specific ผมเปิด README ของ `katgpt-rs` แล้วพบว่า repo อธิบาย `HLA/AHLA` ว่าเป็น “Higher-order Linear Attention — O(1) prefix stats” และ `LT2 Looped` ว่าเป็น weight-shared T-pass loop แบบ hybrid SDPA+AHLA ส่วน decode layer มี `DDTree` เป็น best-first tree from marginal log-probs และ `LeviathanVerifier` สำหรับ p/q rejection sampling ([katgpt-rs README](https://raw.githubusercontent.com/katopz/katgpt-rs/develop/README.md)). นี่ช่วยยืนยันว่าคำเหล่านี้มีสถานะเป็น feature ใน repo แต่ยังไม่เท่ากับ peer-reviewed evidence สำหรับ benchmark เฉพาะ

วิธีอ่านคำเหล่านี้: MUX คือการทำให้ input หลายชนิดเข้า stream เดียวเพื่อประมวลผลแบบ packed; AHLA/HLA คือชั้น summary ที่ต้องพิสูจน์ว่ายังเก็บข้อมูลพอ ไม่ใช่แค่บีบจนหาย; T-PASS คือ recurrent/reused computation ซึ่งประหยัด memory กว่า stack ลึกได้แต่เพิ่มจำนวนรอบ; LATTICE คือ hard constraints ที่ prune ทางผิดก่อนเสียเวลาต่อ ถ้าจะพิสูจน์ O(N) ต้องระบุ N คือ token, entity, edge, หรือ timestep และพิสูจน์ว่าแต่ละ step แตะข้อมูลกี่ครั้ง

แบบฝึก: สร้าง planner ที่มี entity 10,000 ตัว วิธี naive ให้ทุกตัวดูทุกตัวคือ O(N²) ลอง group ตาม zone แล้วให้ entity ดูเฉพาะ zone summary + neighbors จะเข้าใกล้ O(N) มากขึ้น วัดทั้งเวลารันและความผิดพลาดของ decision

ข้อจำกัด: Big-O ไม่บอก constant factor, memory locality, branch prediction, lock contention หรือ validation cost และ deterministic pruner ไม่รับประกัน correctness ถ้ากฎไม่ครบ

คำถามฝึก: ในระบบของคุณ quadratic เกิดจาก attention, collision, pathfinding หรือ rule checking?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** จาก O(N²) เป็น O(N) ควรพิสูจน์ที่ algorithm หรือที่ runtime memory movement? แหล่งใหม่คือ FlashAttention ซึ่งชี้ว่าการทำ attention ให้เร็วขึ้นไม่ได้มีแค่ลด FLOPs แต่ต้องลด reads/writes ระหว่าง HBM กับ SRAM ด้วย IO-aware tiling [FlashAttention](https://arxiv.org/abs/2205.14135). อีกแหล่งคือ Performer ซึ่งลด self-attention แบบ softmax ด้วย FAVOR+ random feature approximation เพื่อทำ linear attention [Performer](https://arxiv.org/abs/2009.14794).

**กลไกที่เกี่ยวกับโพสต์:** MUX/AHLA/T-PASS/LATTICE เป็นคำใน stack ของผู้เขียนและ README ของ `katgpt-rs`; การบอกว่า O(N²) เหลือ O(N) ต้องระบุว่า N คืออะไร เช่น token, entity, edge, candidate หรือ timestep ถ้า MUX pack signal แล้ว AHLA เก็บ prefix stats อาจลดการมองทุกคู่ แต่ถ้า LATTICE validator ต้องตรวจ constraint คู่จำนวนมาก ต้นทุนอาจกลับเป็น quadratic ในจำนวน relation ได้

**ผลเชิงปฏิบัติ:** ให้แยก claim เป็นสามชั้น: ลดความซับซ้อนเชิงคณิตศาสตร์, ลด memory traffic, และลด allocation/branch ใน implementation Rust ทั้งสามช่วย performance คนละทาง และอาจไม่เกิดพร้อมกัน การมี zero-allocation ไม่ได้พิสูจน์ O(N); การมี O(N) algorithm ไม่ได้แปลว่าเร็วถ้า memory access กระโดดหรือ constant ใหญ่

**แบบฝึก:** ทำ planner entity N ตัวสามเวอร์ชัน: pairwise all-to-all, zone summary, และ zone summary + lattice prune วัดเวลา, cache misses ถ้ามี, และ violation rate เพิ่ม N เป็น 1k/10k/100k แล้ว plot log-log Caveat คือ approximation แบบ linear attention หรือ summary อาจเสีย information จึงต้องวัดคุณภาพ decision ด้วย ไม่ใช่เวลาอย่างเดียว
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 025](025-neural-cellular-automata-self-healing.md) · [โพสต์ 027 →](027-latent-first-deterministic.md)

หัวข้อที่เกี่ยวข้อง: [02 Latent reasoning, recursion และ search](topics/02-latent-reasoning-and-search.md) · [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [07 การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก](topics/07-training-and-model-architecture.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
