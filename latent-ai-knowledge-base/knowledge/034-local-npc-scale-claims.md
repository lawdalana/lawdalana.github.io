# 034 — NPC ล้านความคิดต้องวัด sync, tick และ correctness

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 208-222 · [ต้นฉบับ](../original/post.md) · ภาพ: ![gigatoken screenshot](../original/image-19.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์อ้างว่า Rust + speculative + neuro-symbolic pruner + mux + HLA ฝั่ง deterministic ทำได้ระดับ 140M tokens/sec และระหว่าง live มี AI NPC 1,000 x 1,000 reasoning sync กัน 2 nodes ใช้ CPU 20%x2 ที่ 20Hz ภาพประกอบเป็น screenshot Gigatoken ที่อ้าง tokenizer เร็วกว่า HuggingFace/tiktoken มาก

ต้องแยกสองเรื่อง: ภาพ Gigatoken เป็น tokenizer benchmark จาก repo ภายนอก ซึ่งผู้พัฒนาระบุ benchmark หลาย CPU เช่น Apple M4 Max และ AMD EPYC พร้อม validation ว่า output match บางชุด ([GitHub: gigatoken](https://github.com/marcelroed/gigatoken)). แต่ tokenization throughput ไม่ได้ยืนยัน NPC reasoning throughput ของ KatGPT โดยตรง

สำหรับ simulation scale หน่วยวัดที่ต้องมีคือจำนวน agent, tick rate, จำนวน action ต่อ tick, network sync bytes, deterministic replay pass/fail, CPU model, core count, และ latency percentile ถ้าอ้าง 1,000x1,000 NPC ต้องชัดว่าเป็นหนึ่งล้าน agent จริง หรือเป็น 1,000 NPC sync กับ 1,000 reasoning contexts

แหล่งวิจัยช่วย framing คือ neuro-symbolic systems ที่รวม learning กับ symbolic reasoning เพื่อให้ตรวจสอบและอธิบายได้มากขึ้น ([arXiv:2012.05876](https://arxiv.org/abs/2012.05876)) และ Rust Book อธิบาย ownership/drop ที่ช่วยจัดการ memory โดยไม่ใช้ GC ซึ่งเกี่ยวข้องกับ latency predictability แต่ไม่ได้รับประกันว่า logic ถูกต้อง ([Rust Book](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)).

แบบฝึก: ทำ stress test NPC 10k ตัวก่อน วัด `tick_ms`, `p95`, `p99`, replay hash ต่อ tick, และจำนวน desync จาก seed เดิม ถ้า p99 เกิน 50ms ที่ 20Hz แปลว่ายังไม่ realtime แม้ average จะดูดี

ข้อจำกัด: ตัวเลขในโพสต์เป็น private benchmark ที่ตรวจซ้ำจาก repo นี้ไม่ได้ จึงควรใช้เป็นแรงบันดาลใจและ checklist สำหรับ benchmark

คำถามฝึก: คุณจะยอมลดความฉลาดต่อ NPC เท่าไรเพื่อให้ deterministic sync ผ่านทุก tick?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** claim NPC scale ควรเทียบกับงาน agent simulation แบบใด? แหล่งใหม่คือ Generative Agents ปี 2023 ซึ่งจำลองเมืองเล็ก 25 agents โดยใช้ memory, reflection, planning และ natural-language interaction [arXiv:2304.03442](https://arxiv.org/abs/2304.03442). อีกแหล่งคือ Generative Agent Simulations of 1,000 People ปี 2024 ซึ่งจำลองบุคคล 1,052 คนจาก qualitative interviews แล้ววัดความใกล้เคียงกับคำตอบจริงใน survey/experiment setting [arXiv:2411.10109](https://arxiv.org/abs/2411.10109).

**กลไกที่เกี่ยวกับโพสต์:** งานเหล่านี้ช่วยแยก “จำนวน agent” ออกจาก “ชนิด reasoning” และ “หน่วยเวลา” 25 agents แบบ LLM planning อาจหนักมากแต่ richer behavior ส่วน 1,000 agents ใน paper 2024 เป็น simulation/behavioral replication ไม่ใช่ realtime game tick 20Hz ทุกตัวชนกันหมด ดังนั้นโพสต์ที่บอก 1,000×1,000 reasoning NPCs ต้องอธิบายว่าเป็นจำนวน NPC, จำนวนคู่ปฏิสัมพันธ์, จำนวน decision หรือจำนวน sync events

**ผลเชิงปฏิบัติ:** Benchmark เกมควรรายงานอย่างน้อย: agents active, interactions evaluated, tick rate, p99 tick time, CPU utilization, sync topology, determinism/replay และ correctness metric เช่น collision/economy violations ถ้า reasoning ถูกลดเป็น local deterministic transition ก็เทียบกับ LLM generative agents ตรง ๆ ไม่ได้ แต่เป็น engineering trade-off ที่อาจเหมาะกับเกม realtime

**แบบฝึก:** จำลอง 1,000 NPC แล้ววัดสามโหมด: independent update O(N), neighbor grid O(N×k), all-pairs O(N²) พร้อมเปิด OBS หรือ workload อื่นเหมือนโพสต์ รายงาน p50/p99 และจำนวน violation Caveat คือ CPU 20% ระหว่าง live เป็น observation ที่น่าสนใจ แต่ยังไม่บอก quality, replay correctness หรือ worst-case spike
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 033](033-noob-learning-streams.md) · [โพสต์ 035 →](035-hope-rank-one-operators.md)

หัวข้อที่เกี่ยวข้อง: [04 NPC, world models, เศรษฐกิจเกม และการประสานฝูง](topics/04-npc-worlds-and-coordination.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
