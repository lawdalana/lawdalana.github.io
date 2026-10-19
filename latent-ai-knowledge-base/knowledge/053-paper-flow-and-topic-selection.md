# 053 — เมื่อ Paper ไหลเร็ว: เลือกอ่านให้เกิดระบบ

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 16-23  
รูปประกอบ: ![Paper list screenshot](../original/image-2.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์บอกว่าช่วงนี้ paper ไหลเร็วมากจนเลือกหัวข้อ talk ยาก ภาพเป็นรายชื่อ paper/notes หลายตัว เช่น `ASEntmax`, `Metabolic_Gate`, `Active_Inference`, `Flybody`, `CVRR_Latent_Necessity`, `FLYNN_Modality` และลิงก์ `katgpt-rs` ที่อธิบายตัวเองว่า neuro-symbolic micro-Transformer with speculative decoding, constraint pruning, recurrent attention และ adaptive test-time scaling

## ความรู้ที่ค้นเพิ่ม

บทเรียนไม่ใช่ paper ใด paper หนึ่ง แต่คือการจัดระบบอ่าน research ที่เร็วมาก ให้แบ่งทุก paper เป็น 4 ช่อง:

- Primitive: เทคนิคใหม่ เช่น optimizer, attention, search
- Evidence: benchmark/dataset ที่รองรับ
- Relevance: เกี่ยวกับ stack เราอย่างไร
- Repro cost: ต้องใช้ GPU/data/time เท่าไร

จากแหล่งที่ตรวจในชุดโพสต์นี้ มี paper ที่ควรใส่ใน primitive map เช่น AlphaGo Zero สำหรับ neural search [Nature](https://www.nature.com/articles/nature24270), FRM สำหรับ recurrent refinement [arXiv](https://arxiv.org/abs/2606.29150), vec2vec สำหรับ embedding privacy [arXiv](https://arxiv.org/html/2505.12540v2), และ PagedAttention สำหรับ serving memory management [arXiv](https://arxiv.org/abs/2309.06180)

## ตัวอย่างจากชื่อ Flybody ในภาพ

ภาพมีไฟล์ `553_Flybody_WPG_Residual...` ซึ่งชี้ไปทางงาน fruit fly แต่จากชื่อไฟล์อย่างเดียวห้ามสรุปว่าเป็น “สมองแมลงวันเล่นเกม” หรือ architecture แบบใดแบบหนึ่ง สิ่งที่ตรวจจากแหล่งหลักได้มีอย่างน้อยสามชั้นที่ต้องแยกกัน:

1. **body physics model:** repo [`TuragaLab/flybody`](https://github.com/TuragaLab/flybody) ระบุว่า `flybody` เป็นโมเดลร่างกายแมลงวันผลไม้แบบละเอียดสำหรับ MuJoCo และงาน reinforcement learning พัฒนาโดย Google DeepMind กับ HHMI Janelia; README ยังมีตัวอย่าง `walk_imitation()` และบอกว่า action เดินมี 59 มิติ
2. **learned controller:** flybody มี task เช่น walking, flight และ vision-guided flight พร้อม script ฝึก distributed RL/DMPO แต่นี่คือ policy/controller ที่ฝึกให้ควบคุมร่างกายใน simulation ไม่ใช่ connectome ทั้งสมองโดยอัตโนมัติ
3. **connectome/simulated brain:** FlyWire เป็นคนละทรัพยากร คือ wiring diagram ของสมอง/ระบบประสาทแมลงวัน ทีม Fly Connectomics ระบุว่าชุดข้อมูล FlyWire ถูกตีพิมพ์ใน Nature และเป็นแผนที่ connectome ของ fruit fly [Fly Connectomics](https://flyconnecto.me/). งานที่ใช้ connectome เป็น neural controller มีเช่น Fly-connectomic Graph Model ซึ่ง instantiate whole-brain connectome เป็น graph-structured controller สำหรับ simulated fly ผ่าน deep RL [arXiv:2602.17997](https://arxiv.org/abs/2602.17997)

ดังนั้นถ้าจะพูดใน talk ให้ใช้ประโยคปลอดภัยว่า “Flybody คือร่างกายและ physics environment; controller ต้องฝึกหรือออกแบบเพิ่ม; FlyWire/connectome คือแผนที่สายไฟสมองอีกชั้นหนึ่ง” ไม่ควรพูดว่าเปิด repo แล้วได้สมองแมลงวันที่เข้าใจเกมทันที

## วิธีลอง

ทำ reading queue ที่มีคะแนน 1-5:

| paper | primitive | relevance | repro cost | next action |
| --- | --- | --- | --- | --- |
| FRM | recurrent refinement | high | medium | toy Sudoku |
| vec2vec | embedding translation | high | medium | privacy threat model |
| PagedAttention | KV cache paging | medium | high | benchmark reading |
| Flybody | embodied physics + RL task env | medium | medium/high | run walking env, then inspect controller |

เลือก talk จากช่องที่ relevance สูงและ repro cost ต่ำก่อน จะได้ demo ได้จริง

แบบฝึกสั้นสำหรับ Flybody: ติดตั้ง core package แล้วรัน environment เดินด้วย random actions ก่อน เพื่อแยก “body sim ทำงาน” ออกจาก “controller เดินเก่ง” จากนั้นค่อยเปิด policy หรือ training script ถ้าต้องการพูดเรื่อง learning และถ้าจะโยง connectome ให้เพิ่มคอลัมน์แยกต่างหากว่าใช้ FlyWire/FlyGM หรือไม่

## ข้อควรระวัง

ชื่อ paper ในภาพบางส่วนเปิดไม่ครบหรือไม่ชัดพอจาก screenshot จึงไม่ควรสรุปผลวิจัยเฉพาะจากชื่อไฟล์ ต้องกลับไปอ่าน PDF/abstract ก่อนทุกครั้ง โดยเฉพาะ paper ที่ claim “super goat” หรือดูน่าตื่นเต้นมาก กรณี Flybody ยิ่งต้องระวัง เพราะ body physics, learned controller, connectome และ “simulated brain” เป็นคนละวัตถุวิจัย

## แหล่งอ้างอิง

- [katgpt-rs GitHub จากต้นฉบับ](https://github.com/katopz/katgpt-rs)
- [AlphaGo Zero](https://www.nature.com/articles/nature24270)
- [Flow Reasoning Models](https://arxiv.org/abs/2606.29150)
- [vec2vec](https://arxiv.org/html/2505.12540v2)
- [PagedAttention/vLLM](https://arxiv.org/abs/2309.06180)
- [TuragaLab/flybody](https://github.com/TuragaLab/flybody)
- [Fly Connectomics / FlyWire](https://flyconnecto.me/)
- [Whole-Brain Connectomic Graph Model](https://arxiv.org/abs/2602.17997)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** repo [arxiv-sanity-lite](https://github.com/karpathy/arxiv-sanity-lite) และ Shan Carter & Chris Olah, [Research Debt (Distill, 2017)](https://distill.pub/2017/research-debt/). arxiv-sanity-lite เป็นเครื่องมือจัด tag/recommend paper จาก abstracts ด้วย tf-idf/SVM ส่วน Research Debt อธิบายต้นทุนสะสมเมื่อ field มีแนวคิด/คำอธิบายที่คนตามไม่ทัน แม้ไม่ใช่ paper experimental แต่มาจากช่องทางหลักของผู้เขียนและช่วยตั้งกรอบอ่านงานเร็ว

**สิ่งที่ขยายจากโพสต์:** ภาพรายชื่อ paper ไหลเร็วมากควรจัดการด้วย workflow ไม่ใช่อ่านทุกอย่างเท่ากัน. เพิ่ม 3 กล่องต่อ paper: `claim`, `artifact`, `decision`. Claim คือผู้เขียน paper พูดอะไร; artifact คือมี code/data/benchmark หรือไม่; decision คือเราจะ demo, cite, ignore หรือ revisit. แบบนี้ลด research debt เพราะทุกชื่อใน list มีสถานะ ไม่เป็นกองลิงก์ที่ดูสำคัญเท่ากันหมด

**ตัวอย่างทดลองสำหรับ talk:** สร้าง reading board 20 paper จากภาพ/สัปดาห์นั้น ใช้ scoring 1–5: novelty, relevance to katgpt-rs, reproducibility, demo cost, risk of overclaim. เลือก 3 paper ที่คะแนน relevance สูงและ demo cost ต่ำไปทำ mini-repro 2 ชั่วโมง ส่วน paper ที่เป็น infrastructure เช่น Flybody/FlyWire ให้แยก “body sim”, “controller”, “connectome” เป็นคนละ card เพื่อไม่ conflation

**ข้อจำกัด:** arxiv-sanity-lite เป็นเครื่องมือช่วยกรอง ไม่ใช่ตัวตัดสินคุณภาพ paper. Research Debt เป็น essay ที่ใช้เป็นกรอบวิธีอ่าน ไม่ใช่หลักฐานว่า paper ใดถูก. สำหรับโพสต์นี้ข้อสรุปคือให้เก็บ provenance และสถานะความมั่นใจของแต่ละหัวข้อก่อนสังเคราะห์เป็น talk
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 052](052-llama-cpp-vllm-bragging-gate.md) · [โพสต์ 054 →](054-typesafe-jev-vs-local-npc.md)

หัวข้อที่เกี่ยวข้อง: [07 การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก](topics/07-training-and-model-architecture.md) · [10 วิธีอ่าน paper, สร้างการทดลอง และวางแผนเรียน](topics/10-research-methods-and-learning.md)
<!-- POST_NAV_END -->
