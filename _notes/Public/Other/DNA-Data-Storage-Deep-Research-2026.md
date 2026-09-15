---
title: "DNA Data Storage: เก็บข้อมูลทั้งโลกในถ้วยชา (Deep Research 2026)"
notetype: feed
date: 2026-05-16
last_modified: 2026-09-16
tags: [dna-storage, biotechnology, data-storage, molecular-computing, research, deep-research]
status: published
---

# DNA Data Storage: เก็บข้อมูลทั้งโลกในถ้วยชา

> เจาะลึก DNA Data Storage หรือการเก็บข้อมูลดิจิทัลในโมเลกุล DNA ซึ่งมีความหนาแน่นตามทฤษฎี 455 exabytes/gram เก็บได้นานหลายพันปี และไม่ต้องใช้ไฟเลี้ยงเพื่อคงข้อมูลไว้ ช่วงปี 2025-2026 เริ่มมีผลิตภัณฑ์เชิงพาณิชย์แล้ว (อัปเดต 16 พ.ค. 2026, 25+ sources)

---

## มันคืออะไร?

**DNA Data Storage** คือการเข้ารหัสข้อมูลดิจิทัล (binary 0,1) เป็นลำดับ nucleotide (A,T,G,C) ในโมเลกุล DNA สังเคราะห์ โดยนำหลักการที่ธรรมชาติใช้เก็บข้อมูลพันธุกรรมมาประยุกต์เก็บข้อมูลดิจิทัล

เปรียบเทียบง่าย ๆ คือ SSD เก็บข้อมูลด้วยประจุไฟฟ้าในซิลิคอน ส่วน DNA storage เก็บข้อมูลในโมเลกุลชีวภาพ โดยมีความหนาแน่นตามทฤษฎี **455 exabytes ต่อ 1 gram** จึงมีคำเปรียบเทียบว่าเก็บข้อมูลทั้งโลกได้ในถ้วยชา

---

## End-to-End Process

```
Digital Data → Encoding → DNA Synthesis → Storage → Sequencing → Decoding → Digital Data
(01101...)    (A=00,     (สร้าง DNA       (เก็บใน     (อ่าน DNA    (แปลงกลับ    (ไฟล์เดิม)
               C=01,      จริงๆ)            สภาพแวดล้อม  sequence)    binary)
               G=10,                        ที่เหมาะสม)
               T=11)
```

### 1. Encoding (เข้ารหัส)

แปลง binary → DNA sequence (A,T,G,C) พร้อม error correction codes (Reed-Solomon) และ index/address sequences (barcode) เพื่อให้รู้ลำดับ ต้องหลีกเลี่ยง homopolymers (AAAA, TTTT) เพราะทำให้ sequencing ผิดพลาด

### 2. DNA Synthesis (เขียน)

- **Chemical synthesis:** สร้าง DNA strand ทีละ nucleotide — แพง ช้า แต่แม่นยำ
- **Enzymatic synthesis:** ใช้ enzyme สร้าง DNA — ถูกกว่า เร็วขึ้น (ทิศทางใหม่)
- **Catalog's combinatorial approach:** ไม่ต้องเขียนทีละ base → ใช้ pre-made DNA blocks ประกอบ → เร็ว + ถูกลง

### 3. Storage (เก็บ)

เก็บ DNA ในสภาพแวดล้อมที่เหมาะสม เช่น อุณหภูมิต่ำและแห้ง โดย **ตัวสื่อไม่ต้องใช้ไฟเลี้ยงเพื่อคงข้อมูลไว้** (zero energy at rest) เทคนิคใหม่มีทั้งการเก็บด้วย liquid crystal (Science Advances 2025) ที่ใช้ cationic surfactants เพื่อให้นำ DNA กลับมาอ่านได้โดยไม่ทำลาย และการสร้างผลึกอนินทรีย์ห่อหุ้ม ซึ่งยืดอายุการเก็บได้ 10x ที่ -20°C

### 4. Sequencing (อ่าน)

- **Next-Generation Sequencing (NGS):** แม่นยำ แต่ช้า
- **Nanopore sequencing:** อ่าน strand ยาวได้ (Oxford Nanopore)
- **Cas9-guided random access:** เลือกอ่านเฉพาะไฟล์ที่ต้องการ (Nature Comms 2025)

### 5. Decoding (ถอดรหัส)

แปลง DNA sequence กลับเป็น binary → error correction → reconstruct original file

---

## Density (ความหนาแน่น)

| Metric | ค่า | เปรียบเทียบ |
|:-------|:----|:------------|
| **DNA Theoretical max** | **455 EB/gram** | ข้อมูลทั้งโลกในถ้วยชา |
| **DNA Experimental best** | ~432.2 EB/gram | ใช้ yeast cells |
| **DNA Practical current** | ~43 EB/gram | 2025 experiments |
| SSD | ~1 TB/gram | DNA = 43 ล้านเท่า |
| HDD | ~0.003 TB/gram | DNA = 14 พันล้านเท่า |
| LTO-10 Tape | ~0.06 TB/cm³ | DNA = 1000x denser |

## Longevity (อายุการเก็บ)

| Medium | อายุ | เงื่อนไข |
|:-------|:-----|:---------|
| **DNA** | **500-10,000+ ปี** | สภาพเหมาะสม |
| HDD | 3-5 ปี | ต้อง spin |
| SSD | 5-10 ปี | charge decay |
| Tape (LTO) | 15-30 ปี | controlled env |
| Optical (CD/DVD) | 5-10 ปี | degradation |

## Energy

| Medium | Power at rest |
|:-------|:-------------|
| **DNA** | **Zero** |
| HDD array | Watts/TB |
| Tape library | ต่ำแต่ต้อง climate control |
| SSD | Nonzero |

---

## Cost (ภาพปัจจุบัน)

> "Storing one megabyte in DNA costs more than **a million times** as much as putting it on an SSD, and more than **2.5 million times** the cost of magnetic tape"
> — [Blocks & Files, ม.ค. 2026](https://blocksandfiles.com/data-protection/2026/01/16/dna-data-storage-when-the-physics-work-but-the-economics-dont/4090361)

| Item | Cost |
|:-----|:-----|
| Biomemory DNA Card | **$1,000/KB** (1 kilobyte!) |
| ต้นทุนเขียน 1 MB (2018) | $3,500 |
| ต้นทุนอ่าน 1 MB (2018) | $1,000 |
| SSD | ~$0.05/GB |
| LTO Tape | ~$0.005/GB |

### แต่ cost กำลังลดลงเร็วมาก

- Cost ลด **10x** ใน 1 ปี (2024-2025)
- Retrieval เร็วขึ้น **3,200x**
- Wyss Institute: automated microfluidic chips → 1 GB/day, throughput โต 50%/year

---

## บริษัทและ Products หลัก

### Atlas Data Storage (จาก Twist Bioscience)

- **Spun off:** พ.ค. 2025, **$155M seed funding**
- **Product: Atlas Eon 100**
  - First scalable DNA storage service
  - **36-60 petabytes per cassette**
  - 60 PB ในปริมาตร 60 ลูกบาศก์นิ้ว (ขนาดถือด้วยมือได้)
  - 1000x denser than LTO-10 tape
  - EMP-resistant, millennia-stable
  - Zero energy post-write
- เป้า: 13TB in a single drop of water by 2026
- Backed by: Seagate, Western Digital

### Biomemory (ฝรั่งเศส)

- **Product: DNA Card** — first commercially available DNA storage device
  - เก็บ 1 KB → $1,100
  - Data retention: 50, 100, หรือ 150 ปี
  - Biomemory Prime: targeted 2026 release
- เข้าซื้อ Catalog (มี.ค. 2026) เพื่อเร่งการพัฒนา
- End-to-end commercial solutions before end of 2026

### Catalog

- Shortmer combinatorial encoding (Nature Scientific Reports)
- ไม่ต้อง synthesize DNA base-by-base → ใช้ pre-made DNA blocks ประกอบ
- ถูก Biomemory เข้าซื้อแล้ว

### Iridia

- Founded 2016
- DNA polymer synthesis + electronic nano-switches + semiconductor fabrication
- Highly parallel nanomodule array → ความหนาแน่นสูงมาก
- Backed by Seagate, Western Digital

### DNA Data Storage Alliance (SNIA)

- Microsoft + Illumina + Twist + อื่นๆ
- 52-page Technology Review v1.0 (มิ.ย. 2025)
- กำหนด standards + roadmap

---

## Research Breakthroughs 2025-2026

### 1. Rewritable DNA Hard Drive (University of Missouri, 2026)

**ทำสำเร็จครั้งแรก:** ลบและเขียนข้อมูล DNA ทับได้หลายครั้ง จึงเปลี่ยนจากสื่อที่เขียนครั้งเดียวไปเป็นสื่อที่เขียนซ้ำได้

ก่อนหน้านี้ DNA storage เน้นการเขียนข้อมูลครั้งเดียว ความสามารถในการเขียนซ้ำจึงช่วยขยายรูปแบบการใช้งาน โดยมีเป้าหมายพัฒนาอุปกรณ์ให้มีขนาดใกล้เคียงแฟลชไดรฟ์

### 2. Cas9 Random Access + Semantic Search (Nature Comms, ก.ค. 2025)

ใช้ **CRISPR-Cas9** เลือกอ่านเฉพาะไฟล์ที่ต้องการ — Deep neural network mapping 1.74M images → embedding → Cas9 target sequences ทำหน้าที่เป็น "molecular addresses"

**Molecular similarity search:** ค้นหาภาพคล้ายกันใน DNA pool — แก้ปัญหา "random access" ที่เป็น bottleneck หลักของ DNA storage

### 3. Liquid Crystal DNA Preservation (Science Advances, 2025)

Liquid crystal-guided DNA preservation platform (LDIPP) ช่วยให้ **นำ DNA กลับมาอ่านได้โดยไม่ทำลาย** ส่วนการเก็บด้วยผลึกอนินทรีย์ช่วยยืดอายุ 10x ที่ -20°C พร้อมป้องกันการย่อยสลายจากจุลินทรีย์และเอนไซม์

### 4. DNA-DISK: Automated End-to-End (PNAS, 2025)

รวมการสังเคราะห์ DNA ทีละ nucleotide ด้วยเอนไซม์และการอ่านลำดับ DNA บนระบบ digital microfluidics โดยใช้ Gibson assembly, PCR และ Nanopore sequencing ในแพลตฟอร์มเดียว เป็นแนวทางพัฒนาอุปกรณ์เก็บข้อมูล DNA ที่ทำงานครบวงจร

### 5. 12-Letter DNA (XNA) — Beyond ATGC

Enzymatic synthesis + nanopore sequencing ของ **12-letter DNA** — เพิ่ม B,S,P,Z,X,K,J,V เป็น bases เพิ่ม จาก 2 bits/base → log₂(12) ≈ 3.58 bits/base เพิ่ม density ~79%

### 6. Solid-State Nanopore Readout (PMC, 2025)

ใช้แพลตฟอร์ม SiNx nanopore อ่านข้อมูล DNA ร่วมกับ programmable DNA และโครงสร้างนาโนจากเปปไทด์ โดยพัฒนาเป็น array เพื่ออ่านหลายชุดพร้อมกัน

---

## Market Forecast

| Source | 2025 | 2031 | 2035 | CAGR |
|:-------|:-----|:-----|:-----|:-----|
| Global Market Insights | - | $6.3B | **$80.2B** | 88% |
| Research Nester | $385M | - | **$51.6B** | 63.2% |

**Use case หลัก:** Cold/archive storage (ข้อมูลที่ไม่ต้อง access บ่อย) — ข้อมูลทางการแพทย์, scientific data, digital media archives, historical preservation, enterprise compliance

---

## Roadmap & Timeline

| ปี | Milestone |
|:---|:----------|
| 2012 | Harvard: 700 TB in 1 gram DNA (Church et al.) |
| 2016 | Iridia founded |
| 2019 | English Wikipedia (16 GB) encoded in DNA |
| 2021 | Catalog raises $35M Series B |
| 2023 | DNA Data Storage Alliance formed (SNIA) |
| 2025 พ.ค. | Atlas Data Storage spun off ($155M) |
| 2025 มิ.ย. | SNIA 52-page Technology Review v1.0 |
| 2025 ก.ค. | Cas9 random access + semantic search (Nature) |
| 2025 ธ.ค. | Atlas Eon 100 launched (36-60 PB/cassette) |
| 2025 | Biomemory DNA Card ($1,000/KB) |
| 2026 | Rewritable DNA hard drive (U. Missouri) |
| 2026 | Atlas: 13TB in a drop |
| 2026 | Biomemory end-to-end commercial solution |
| ~2030 | Mainstream archival adoption |
| ~2050 | Mainstream general storage |

---

## ข้อจำกัด

- **แพงมาก:** 1MB in DNA = 1 ล้านเท่า SSD — ยังห่างกันมหาศาล
- **ช้า:** การอ่านและเขียนใช้เวลาหลายชั่วโมงถึงหลายวัน แทนที่จะเป็นมิลลิวินาที
- **เหมาะกับ cold storage** — ไม่เหมาะกับข้อมูลที่ต้องเรียกใช้บ่อย
- **Random access ยาก** — DNA อยู่ใน liquid ต้องใช้ Cas9 technique
- **Standards ยังไม่มี** — แต่ละบริษัทใช้ encoding ต่างกัน
- **Error rates:** Synthesis deletion errors, sequencing substitution errors
- **Scalability:** ยังไม่มี infrastructure สำหรับ production scale

---

## สรุป

DNA Data Storage เด่นเรื่องความหนาแน่นสูง อายุการเก็บนับพันปี และการคงข้อมูลไว้โดยไม่ต้องใช้ไฟเลี้ยง แต่ต้นทุนยังสูงเกินไปสำหรับการใช้งานทั่วไป

พัฒนาการที่น่าติดตามมีดังนี้:

1. **Commercial products วางจำหน่ายแล้ว** (Atlas Eon 100, Biomemory DNA Card)
2. **Rewritable DNA** ทำสำเร็จ (ไม่ใช่ write-once อีกต่อไป)
3. **ต้นทุนลด 10x/ปี** — เป็นแนวโน้มที่อาจนำไปสู่การใช้งานแพร่หลายภายใน 10 ปี
4. **บริษัทเทคโนโลยีรายใหญ่เข้ามาลงทุน** — Microsoft, Seagate, Western Digital, Meta

บทความนี้คาดว่าการใช้งานจะเริ่มแพร่หลายในกลุ่ม cold/archive storage ราว **~2030** และในงานเก็บข้อมูลทั่วไปช่วง **~2050** กรอบเวลานี้ยังขึ้นอยู่กับการลดต้นทุน ซึ่งอาจเร็วหรือช้ากว่าที่คาด

---

## Sources

1. [SNIA DNA Data Storage Technology Review v1.0 (2025)](https://www.snia.org/sites/default/files/DNA/SNIA-DNA-Data-Storage-Technology-Review-v1.0.pdf)
2. [Nature Comms: Cas9 Random Access (2025)](https://www.nature.com/articles/s41467-025-61264-5)
3. [Science Advances: Liquid Crystal DNA Preservation](https://www.science.org/doi/10.1126/sciadv.adu3957)
4. [PNAS: DNA-DISK Automated Storage](https://www.pnas.org/doi/10.1073/pnas.2410164121)
5. [ACS Nano: Emerging Approaches to DNA Storage](https://pubs.acs.org/doi/10.1021/acsnano.2c06748)
6. [Forbes: Atlas Eon 100](https://www.forbes.com/sites/tomcoughlin/2025/12/06/atlas-data-storage-announces-eon-100-synthetic-dna-storage/)
7. [Blocks & Files: Economics Analysis](https://blocksandfiles.com/data-protection/2026/01/16/dna-data-storage-when-the-physics-work-but-the-economics-dont/4090361)
8. [Tom's Hardware: Rewritable DNA HDD](https://www.tomshardware.com/pc-components/storage/new-dna-hdd-can-be-erased-and-overwritten-repeatedly-university-of-missouri-researchers-aiming-for-next-gen-thumb-drive-sized-storage)
9. [Tom's Hardware: Atlas 60PB](https://www.tomshardware.com/pc-components/storage/worlds-first-scalable-dna-data-storage-offering-announced-offering-a-staggering-60pb-in-60-cubic-inches-enough-to-hold-660-000-4k-movies-atlas-data-storage-claims-its-solution-is-1000x-denser-than-lto-10-tape)
10. [Tom's Hardware: Biomemory DNA Card](https://www.tomshardware.com/pc-components/storage/new-memory-card-uses-dna-to-store-your-data-biomemorys-card-costs-dollar1100-to-store-one-kilobyte-of-data)
11. [Scientific American: DNA Ultimate Storage](https://www.scientificamerican.com/article/dna-the-ultimate-data-storage-solution/)
12. [Extremetech: 455 EB/gram](https://www.extremetech.com/extreme/218241-at-up-to-455-exabytes-on-a-single-gram-dna-storage-could-create-mankinds-permanent-record)
13. [Nature: DNA Origami Storage](https://www.nature.com/articles/s41467-025-66274-x)
14. [Scientific Reports: Combinatorial Encoding](https://www.nature.com/articles/s41598-024-58386-z)
15. [Linknovate: Top DNA Storage Startups 2026](https://blog.linknovate.com/top-dna-data-storage-startups-in-2026-the-future-of-digital-memory/)
16. [Global Market Insights: Market Forecast](https://www.gminsights.com/industry-analysis/dna-data-storage-market)
17. [U. Missouri: Rewritable DNA Drive](https://showme.missouri.edu/2026/mizzou-researchers-developing-a-rewritable-dna-hard-drive/)
18. [PMC: 12-Letter XNA](https://pmc.ncbi.nlm.nih.gov/articles/PMC10603101/)
