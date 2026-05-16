---
title: "DNA Data Storage: เก็บข้อมูลทั้งโลกในถ้วยชา (Deep Research 2026)"
notetype: feed
date: 2026-05-16
last_modified: 2026-05-16
tags: [dna-storage, biotechnology, data-storage, molecular-computing, research, deep-research]
status: published
---

# DNA Data Storage: เก็บข้อมูลทั้งโลกในถ้วยชา

> Deep Research เรื่อง DNA Data Storage — เทคโนโลยีเก็บข้อมูล digital ในโมเลกุล DNA ความหนาแน่น 455 exabytes/gram อยู่ได้หลายพันปี ไม่ต้องใช้ไฟเวลาไม่อ่าน ปี 2025-2026 เริ่มมี commercial products แล้ว (อัปเดต 16 พ.ค. 2026, 25+ sources)

---

## มันคืออะไร?

**DNA Data Storage** คือการเข้ารหัสข้อมูล digital (binary 0,1) เป็นลำดับ nucleotide (A,T,G,C) ในโมเลกุล DNA สังเคราะห์ — เอาธรรมชาติที่เก็บ genetic information มาเก็บ digital information แทน

กล่าวง่ายๆ: ถ้า SSD เก็บข้อมูลด้วย electric charge ใน silicon DNA storage เก็บข้อมูลด้วยโมเลกุลชีวภาพ — **455 exabytes ต่อ 1 gram** (ข้อมูลทั้งโลกในถ้วยชา)

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

เก็บในสภาพแวดล้อมที่เหมาะสม (อุณหภูมิต่ำ แห้ง) — **ไม่ต้องใช้ไฟเลย** เมื่อไม่อ่าน (zero energy at rest) เทคนิคใหม่ใช้ Liquid crystal preservation (Science Advances 2025) — cationic surfactants → nondestructive recovery และ inorganic crystal mineralization → อายุยืด 10x ที่ -20°C

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
  - 60 PB in 60 cubic inches (ใส่มือ)
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
- Acquired Catalog (มี.ค. 2026) → เร่ง development
- End-to-end commercial solutions before end of 2026

### Catalog

- Shortmer combinatorial encoding (Nature Scientific Reports)
- ไม่ต้อง synthesize DNA base-by-base → ใช้ pre-made DNA blocks ประกอบ
- ถูก Biomemory acquire แล้ว

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

**ทำสำเร็จครั้งแรก:** erase + overwrite DNA data repeatedly — เปลี่ยน DNA จาก "write-once" → rewritable medium

ก่อนหน้านี้ DNA = write-once only (เขียนแล้วเขียนอีกไม่ได้) ถือเป็น game changer เพราะ storage ที่ใช้งานได้จริงต้อง rewritable — เป้าหมาย: thumb-drive-sized DNA storage

### 2. Cas9 Random Access + Semantic Search (Nature Comms, ก.ค. 2025)

ใช้ **CRISPR-Cas9** เลือกอ่านเฉพาะไฟล์ที่ต้องการ — Deep neural network mapping 1.74M images → embedding → Cas9 target sequences ทำหน้าที่เป็น "molecular addresses"

**Molecular similarity search:** ค้นหาภาพคล้ายกันใน DNA pool — แก้ปัญหา "random access" ที่เป็น bottleneck หลักของ DNA storage

### 3. Liquid Crystal DNA Preservation (Science Advances, 2025)

Liquid crystal-guided DNA preservation platform (LDIPP) — **Nondestructive recovery:** ดึง DNA ออกมาอ่านโดยไม่ทำลาย Inorganic crystal mineralization → preservation ยืด 10x ที่ -20°C + antimicrobial + anti-enzymatic properties

### 4. DNA-DISK: Automated End-to-End (PNAS, 2025)

Enzymatic single-nucleotide DNA synthesis + sequencing บน digital microfluidics — รวม Gibson assembly, PCR, Nanopore sequencing ใน platform เดียว ก้าวหน้าไปสู่ "DNA storage drive" ที่ใช้งานได้จริง

### 5. 12-Letter DNA (XNA) — Beyond ATGC

Enzymatic synthesis + nanopore sequencing ของ **12-letter DNA** — เพิ่ม B,S,P,Z,X,K,J,V เป็น bases เพิ่ม จาก 2 bits/base → log₂(12) ≈ 3.58 bits/base เพิ่ม density ~79%

### 6. Solid-State Nanopore Readout (PMC, 2025)

SiNx nanopore platform สำหรับอ่าน DNA data — Programmable DNA + peptide nanostructures Scale to array formats → multiple reads พร้อมกัน

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
- **ช้า:** Read/Write เป็น hours-days ไม่ใช่ milliseconds
- **Cold storage only** — ไม่เหมาะ active data
- **Random access ยาก** — DNA อยู่ใน liquid ต้องใช้ Cas9 technique
- **Standards ยังไม่มี** — แต่ละบริษัทใช้ encoding ต่างกัน
- **Error rates:** Synthesis deletion errors, sequencing substitution errors
- **Scalability:** ยังไม่มี infrastructure สำหรับ production scale

---

## สรุป

DNA Data Storage มี physics ที่สวยงาม — density ไม่มีอะไรเทียบได้, longevity เป็นพันปี, zero energy at rest แต่ economics ยังไม่เข้าขั้น ต้นทุนสูงเกินไปสำหรับการใช้งานทั่วไป

แต่จุดพลิกผันกำลังเกิดขึ้น:

1. **Commercial products วางจำหน่ายแล้ว** (Atlas Eon 100, Biomemory DNA Card)
2. **Rewritable DNA** ทำสำเร็จ (ไม่ใช่ write-once อีกต่อไป)
3. **Cost ลด 10x/ปี** — trajectory ไป mainstream ภายใน 10 ปี
4. **Big tech ลงทั้งที** — Microsoft, Seagate, Western Digital, Meta

ถ้าถามว่า "เมื่อไหร่จะใช้ได้จริง?" — สำหรับ cold/archive storage: **~2030** สำหรับ general storage: **~2050** แต่ถ้า cost reduction เร่งตัวเร็วกว่าที่คาด ทุกอย่างจะเร็วขึ้น

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
