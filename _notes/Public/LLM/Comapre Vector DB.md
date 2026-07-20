---
title: "Vector Database Performance 2026: ตัวไหนเร็วที่สุด?"
notetype: feed
date: 2024-05-29
last_modified: 2026-07-20
tags: [vector-database, vector-search, benchmark, RAG, HNSW]
status: published
---

ถ้าถามว่า **Vector Database ตัวไหนเร็วที่สุด** คำตอบที่ถูกต้องคือ “เร็วที่สุดภายใต้ workload ไหน” เพราะผู้ชนะเปลี่ยนทันทีเมื่อสลับจาก read-heavy ไปเป็น streaming ingestion, เพิ่ม metadata filter, บังคับ recall ให้สูงขึ้น หรือเปลี่ยนจากเครื่องเดียวไปเป็น distributed cluster

จากข้อมูลที่ตรวจเมื่อ **2026-07-20** คำตอบแบบใช้งานได้คือ:

- **Zilliz Cloud** นำด้าน QPS และ p99 latency ใน VDBBench แบบ read-heavy ที่ normalize งบไว้ที่ 1,000 ดอลลาร์ต่อเดือน
- **Milvus** เป็นตัวเลือก self-hosted ที่เด่นด้าน throughput และการใช้ core จำนวนมาก
- **Qdrant** เด่นเมื่อมี concurrent ingestion และ payload filtering โดยเฉพาะเมื่อบังคับ recall สูง
- **pgvector** ยังสมเหตุผลมากถ้าข้อมูลหลักอยู่ใน PostgreSQL และ workload ไม่ได้ต้องการ scale-out แบบ vector-native
- ไม่มีผล benchmark ชุดเดียวที่พิสูจน์ว่า database หนึ่งชนะทุกสถานการณ์

<!--more-->

## ทำไม QPS สูงสุดยังไม่แปลว่า “ดีที่สุด”

Vector search เป็น approximate nearest-neighbor search จึงแลกความเร็วกับความแม่นยำ ถ้า database A ทำได้ 10,000 QPS ที่ recall 0.80 ส่วน database B ทำได้ 2,000 QPS ที่ recall 0.98 การเรียก A ว่าเร็วกว่าโดยไม่บอก recall แทบไม่มีประโยชน์

ลำดับการอ่าน benchmark ที่ปลอดภัยกว่าคือ:

1. กำหนด **recall threshold** ก่อน เช่น Recall@10 ≥ 0.95
2. เทียบ **p99 latency** ไม่ใช่ดูเฉพาะค่าเฉลี่ย
3. เทียบ **QPS ที่ concurrency เดียวกัน**
4. ใส่ write rate, filter selectivity และ update/delete เข้าไปใน workload
5. normalize ด้วย hardware หรือค่าใช้จ่าย
6. ดูเวลา build index, memory, disk amplification และ recovery เพิ่มเติม

กล่าวง่าย ๆ คือ **Recall เป็น gate ส่วน latency, throughput และ cost เป็นตัวตัดสินหลังจากผ่าน gate แล้ว**

## ผล read-heavy ล่าสุดจาก VDBBench

[VDBBench live leaderboard](https://zilliz.com/vector-database-benchmark-tool) แสดงผลบน Cohere 768-dimensional embeddings ทั้ง 1M และ 10M vectors ภายใต้หัวข้อ “Vector Search Latency and QPS at $1,000 Monthly Cost” ตารางด้านล่างเลือกจุดที่เร็วที่สุดของแต่ละ configuration หลังบังคับ **recall ≥ 0.95** จากข้อมูลที่หน้าเว็บเปิดเผย ณ วันที่ตรวจ

| System / configuration | 1M QPS | 1M p99 | Recall | 10M QPS | 10M p99 | Recall |
|---|---:|---:|---:|---:|---:|---:|
| ZillizCloud-8cu-perf | 12,837.53 | 2.1 ms | 0.9588 | 6,793.84 | 2.2 ms | 0.9522 |
| Milvus-16c64g-sq4u-fp16-force_merge | 7,704.36 | 2.7 ms | 0.9541 | 2,762.41 | 3.1 ms | 0.9556 |
| Milvus-16c64g-sq8-force_merge | 4,006.40 | 3.2 ms | 0.9609 | 1,833.26 | 3.9 ms | 0.9510 |
| OpenSearch-16c128g-force_merge | 2,590.38 | 8.6 ms | 0.9679 | 1,388.55 | 12.5 ms | 0.9597 |
| ElasticCloud-8c60g-force_merge | 1,482.38 | 12.1 ms | 0.9546 | — | — | — |
| QdrantCloud-16c64g | 1,111.36 | 7.0 ms | 0.9550 | 323.40 | 9.8 ms | 0.9507 |

ใน leaderboard นี้ **Zilliz Cloud เป็นผู้ชนะ read-heavy ที่ชัดเจน** ส่วน Milvus เป็น self-hosted configuration ที่เร็วที่สุดในรายการ แต่ต้องระวังรายละเอียดก่อนนำตัวเลขไปใช้ตัดสินใจ:

- Milvus ใช้ scalar quantization, FP16 และ `force_merge`; นี่ไม่ใช่ default configuration ธรรมดา
- ระบบใช้ขนาด instance และ architecture ต่างกัน จึงควรอ่านผลนี้เป็น **cost-normalized comparison** ไม่ใช่ hardware-identical comparison
- Pinecone และ Turbopuffer ไม่มีจุดที่ผ่าน recall 0.95 ในข้อมูลที่หน้า leaderboard แสดง ณ วันที่ตรวจ การใส่เครื่องหมาย “—” จึงไม่ได้แปลว่าผลิตภัณฑ์ทำ recall ระดับนี้ไม่ได้ในทุก configuration
- Weaviate ไม่อยู่ในชุด live results นี้ การไม่ปรากฏชื่อไม่ใช่หลักฐานว่าแพ้
- เจ้าของโครงการ [VectorDBBench](https://github.com/zilliztech/VectorDBBench) คือ Zilliz และหน้าโครงการระบุ vendor sponsors ชัดเจน ผลจึงมีประโยชน์ แต่ไม่ควรเป็นหลักฐานเพียงชิ้นเดียว

## เมื่อมี ingestion พร้อมกับ search ผู้ชนะเปลี่ยน

VDBBench ยังมี streaming test บน Cohere 10M ตารางนี้ใช้ QPS ที่หน้าเว็บรายงานและคำนวณ **retention = QPS ที่ 1,000 rows/s ÷ static QPS**

| System | Static QPS | QPS @ 500 rows/s | QPS @ 1,000 rows/s | Retention @ 1,000 | Recall |
|---|---:|---:|---:|---:|---:|
| Zilliz Cloud | 7,385.0 | 2,119.0 | 1,860.0 | 25.2% | 0.9384 |
| Milvus | 2,747.0 | 306.0 | 156.0 | 5.7% | 0.9204 |
| Pinecone | 1,131.0 | 367.4 | 369.7 | 32.7% | 0.9024 |
| Turbopuffer | 649.9 | 536.0 | 442.6 | 68.1% | 0.8352 |
| Qdrant Cloud | 446.9 | 393.8 | 347.6 | 77.8% | 0.9357 |

มีสองมุมที่ต้องอ่านพร้อมกัน:

- **Absolute throughput:** Zilliz Cloud ยังสูงสุดที่ 1,860 QPS
- **Performance retention:** Qdrant รักษา throughput ได้ 77.8% และมี recall ใกล้กับ Zilliz มากที่สุดในกลุ่มที่เลือกมา

ดังนั้นระบบ RAG ที่มี document ingestion ต่อเนื่องอาจเลือกต่างจากระบบ catalog ที่ rebuild index เป็นรอบ ๆ และอ่านเกือบอย่างเดียว อย่าใช้ static QPS ไปทำนาย mixed read/write workload

## Metadata filtering: QPS ต้องอ่านคู่กับ recall

ที่ `filterRatio = 0.9` บน Cohere 1M ผลจาก leaderboard เดียวกันเป็นดังนี้:

| System | QPS | p99 latency | Recall |
|---|---:|---:|---:|
| Zilliz Cloud | 5,506.18 | 5.5 ms | 0.9193 |
| OpenSearch force-merge | 2,685.67 | 7.6 ms | 0.4914 |
| Qdrant Cloud + payload index | 1,059.34 | 7.8 ms | 0.9856 |
| Pinecone | 492.49 | 29.6 ms | 0.9269 |
| Elastic Cloud | 437.87 | 27.1 ms | 0.9364 |
| Turbopuffer | 260.40 | 48.3 ms | 0.9828 |

ถ้า requirement คือ recall ≥ 0.98, Qdrant เป็นตัวที่เร็วที่สุดในตารางนี้ แต่ถ้ารับ recall ประมาณ 0.92 ได้ Zilliz ให้ QPS สูงกว่ามาก ส่วน OpenSearch ดูเร็วเป็นอันดับสองเมื่อมอง QPS อย่างเดียว แต่ recall 0.4914 ทำให้ผลนั้นใช้แทน high-accuracy retrieval ไม่ได้

นี่คือเหตุผลที่ benchmark table ซึ่งไม่มี recall column อาจพาเลือกผิดระบบได้ง่าย

## หลักฐานจากงานวิจัยอิสระให้ภาพที่ต่างออกไป

งาน preprint เดือนมิถุนายน 2026 เรื่อง [When More Cores Hurts: The Vector Database Scaling Paradox in HPC](https://arxiv.org/html/2606.08950) ทดสอบ Milvus, Qdrant และ Weaviate บน production supercomputers สูงสุด 256 workers / 64 nodes และ datasets ระดับ 1M–10M vectors ผลสำคัญคือ:

- Qdrant ทำ single-worker ingestion ได้สูงสุด 37,218 vectors/s และ multiworker ingestion สูงสุด 489,213 vectors/s ในชุดทดสอบนั้น
- ที่ 10M vectors Milvus ให้ Recall@10 สูงสุดทั้ง Yandex-T2I และ Pes2o-VE: 0.876 และ 0.982 เทียบกับ Qdrant ที่ 0.837 และ 0.970 และ Weaviate ที่ 0.738 และ 0.918
- ใน mixed read/write test throughput ของ Milvus ลดลงเฉลี่ย 23.44% น้อยกว่า Weaviate ที่ 38.37% และ Qdrant ที่ 50.57%
- การเพิ่ม core หรือ node ให้มากขึ้นให้ diminishing returns และบางกรณี query performance ลดลงได้ถึง 30.67%

ข้อค้นพบเรื่อง mixed workload ดูต่างจาก VDBBench ซึ่ง Qdrant รักษา streaming QPS ได้ดีที่สุด แต่ไม่ได้แปลว่างานใดงานหนึ่งผิด ทั้งสองชุดใช้ hardware, storage, embedding geometry, segmentation, concurrency และนิยาม workload ต่างกัน นี่กลับเป็นหลักฐานที่ดีว่า **database ranking ไม่สามารถย้ายข้าม workload ได้ตรง ๆ**

อีกงานหนึ่งคือ [Benchmarking Open Source Vector Databases](https://doi.org/10.54116/jbdai.v4i1.80) ที่เผยแพร่ในปี 2026 และใช้การทดลองซ้ำ 10 ครั้งต่อ configuration พบว่า Chroma ทำ latency 7.7–8.4 ms และได้สูงสุด 141 QPS ที่ medium scale ขณะที่ pgvector + HNSW ทำ latency ต่ำกว่า 10 ms และมากกว่า 100 QPS ที่ 50k vectors ผลนี้ไม่ได้พิสูจน์ว่า pgvector จะชนะที่ 10M หรือ 100M vectors แต่ยืนยันว่าใน workload ขนาดเล็กถึงกลาง การย้ายออกจาก PostgreSQL อาจเพิ่ม operational complexity โดยไม่ได้เพิ่มคุณค่ามากพอ

## Index ที่เร็วที่สุดไม่เท่ากับ database ที่ดีที่สุด

[VIBE](https://arxiv.org/html/2505.17810) แยก benchmark ชั้น ANN index ออกจาก database layer โดยทดสอบ 12 modern embedding datasets ที่ recall 95% ผลคือ SymphonyQG นำ 5 datasets, Glass นำ 4, NGT-QG นำ 2 และ LoRANN นำ 1 ไม่มี algorithm เดียวชนะทั้งหมด และ graph-based methods ที่ค้นหาเร็วมีต้นทุน build index สูงกว่า

Vector database จริงยังเพิ่มสิ่งที่ index benchmark ไม่ได้วัด เช่น:

- durability, replication และ recovery
- metadata filtering และ hybrid retrieval
- concurrent insert/update/delete
- compaction, segment merge และ write amplification
- multi-tenancy, backup และ observability
- network serialization และ client-side concurrency

FAISS หรือ ANN library อาจชนะด้าน raw latency บนเครื่องเดียว แต่ไม่ใช่สิ่งทดแทน database ที่ต้องให้ durability และ online updates โดยอัตโนมัติ

## เลือกตัวไหนตาม workload

### 1. Managed, read-heavy และต้องการ QPS สูงสุด

เริ่ม POC ด้วย **Zilliz Cloud** เพราะนำ VDBBench ปัจจุบันทั้ง 1M และ 10M ที่ recall ≥ 0.95 แต่ต้องทดสอบ pricing tier, network latency และ filter distribution ของ production จริง

### 2. Self-hosted, read-heavy และ scale ใหญ่

เริ่มด้วย **Milvus** โดยเฉพาะเมื่อทีมจัดการ distributed components และ tuning เรื่อง quantization/compaction ได้ ผล VDBBench และงาน HPC สนับสนุนทั้ง throughput, recall และการใช้ core จำนวนมาก แต่ default setup ไม่ควรถูกคาดหวังว่าจะได้ตัวเลขเท่ากับ tuned `force_merge` configuration

### 3. Streaming ingestion และ payload filtering

ให้ **Qdrant** เป็น candidate แรก ๆ เพราะรักษา QPS ระหว่าง ingestion ได้ดีและมี filtered recall สูงใน VDBBench อีกทั้งงาน HPC พบ ingestion throughput ที่เด่น อย่างไรก็ตามผล mixed workload ระหว่างสองงานวิจัยไม่ตรงกัน จึงต้อง replay write rate และ filter ของระบบจริง

### 4. ข้อมูลหลักอยู่ใน PostgreSQL

ทดลอง **pgvector** ก่อน ถ้า workload ยังอยู่ระดับที่ vertical scaling รับไหว ต้องการ transaction/join/backup ชุดเดียว และทีมไม่อยากดูแล datastore เพิ่ม งานปี 2026 แสดงว่ามันแข่งขันได้ดีที่ 50k vectors แต่ควร benchmark ใหม่เมื่อ corpus โตถึงหลักล้านหรือ filter มีความซับซ้อนสูง

### 5. Hybrid text + vector search สำคัญกว่า ANN ล้วน

**OpenSearch หรือ Elastic** อาจเป็นคำตอบที่ดีกว่าเมื่อ BM25, full-text filters, aggregations และ existing operations มีน้ำหนักสูง แม้ pure-vector QPS จะไม่ชนะ เพราะ end-to-end relevance และจำนวนระบบที่ต้องดูแลมีผลต่อ performance จริงของผลิตภัณฑ์

### 6. ต้องการ managed developer experience หรือ ecosystem เฉพาะ

**Pinecone และ Weaviate** ยังควรอยู่ใน shortlist ถ้า operational simplicity, SDK, multi-tenancy หรือ integration สำคัญกว่า leaderboard ตำแหน่งแรก การไม่มีจุดที่ผ่าน threshold ใน leaderboard หนึ่งชุดไม่ใช่เหตุผลเพียงพอที่จะตัดผลิตภัณฑ์ออก

## Benchmark contract ที่ควรเขียนก่อนเริ่ม POC

ก่อนยิง load test ควรตกลง contract ให้ชัดอย่างน้อยดังนี้:

| Dimension | สิ่งที่ต้องล็อก |
|---|---|
| Corpus | จำนวน vectors, dimensions, distance metric และ distribution ของ embedding จริง |
| Accuracy | Recall@K ขั้นต่ำและวิธีสร้าง exact ground truth |
| Read workload | Top-K, concurrency, query distribution, warm/cold cache และ duration |
| Filter workload | field cardinality, selectivity, nested conditions และ tenant distribution |
| Write workload | rows/s, batch size, update/delete ratio และ freshness SLA |
| Latency | p50, p95, p99 และ timeout rate แยก client/server |
| Cost | compute, memory, disk, network, replicas และ operational labor |
| Lifecycle | ingest time, index build, compaction, backup/restore และ failure recovery |

ควรรันหลายรอบ รายงาน median พร้อม variance และแยก cold-start ออกจาก steady state แต่อย่าลบ outlier ที่ผู้ใช้ production จะเจอจริง โดยเฉพาะ p99 ระหว่าง compaction หรือ concurrent writes

## สรุป

ถ้าต้องเลือกจากหลักฐานปัจจุบันแบบสั้นที่สุด:

- **Zilliz Cloud:** read-heavy QPS สูงสุดใน live VDBBench
- **Milvus:** self-hosted throughput และ large-scale tuning
- **Qdrant:** ingestion resilience และ high-recall filtering
- **pgvector:** operational simplicity เมื่อ PostgreSQL ยังพอ
- **OpenSearch/Elastic:** hybrid retrieval และ existing search stack

แต่คำตอบสุดท้ายไม่ควรมาจาก logo หรือ QPS ตัวเดียว ให้กำหนด recall และ p99 SLO ก่อน แล้ว replay corpus, filters และ write rate ของ production บนงบเท่ากัน Database ที่ผ่าน SLO ด้วยต้นทุนรวมต่ำที่สุดต่างหากคือ “best performance” สำหรับระบบนั้น

## Sources

- [VDBBench Leaderboard](https://zilliz.com/vector-database-benchmark-tool) — live benchmark ของ vector databases หลายระบบ; ใช้สำหรับตัวเลข read-heavy, streaming และ filtering ในบทความนี้ ตรวจเมื่อ 2026-07-20
- [VectorDBBench on GitHub](https://github.com/zilliztech/VectorDBBench) — source code, methodology, supported systems และ sponsor disclosure ของ benchmark suite
- [When More Cores Hurts: The Vector Database Scaling Paradox in HPC](https://arxiv.org/html/2606.08950) — preprint ปี 2026 ที่ทดสอบ Milvus, Qdrant และ Weaviate สูงสุด 64 compute nodes
- [Benchmarking Open Source Vector Databases](https://doi.org/10.54116/jbdai.v4i1.80) — งาน peer-reviewed ปี 2026 ครอบคลุม latency, throughput, ingestion stability และ cold-start behavior
- [VIBE: Vector Index Benchmark for Embeddings](https://arxiv.org/html/2505.17810) — benchmark ชั้น ANN algorithm บน modern text และ image embeddings
- [Qdrant Vector Search Benchmarks](https://qdrant.tech/benchmarks/) — vendor-authored benchmark พร้อม methodology และ raw result links; หน้าเว็บระบุข้อจำกัดเรื่อง bias ไว้โดยตรง
- [ANN-Benchmarks](https://github.com/erikbern/ann-benchmarks) — historical ANN benchmark; repository ระบุว่าไม่ได้ actively maintained และแนะนำ VIBE สำหรับ modern embeddings
