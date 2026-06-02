---
title: "Glass/Silica Data Storage: เก็บข้อมูล 10,000+ ปีในแก้ว (Deep Research 2026)"
notetype: feed
date: 2026-06-01
last_modified: 2026-06-02
tags: [glass-storage, silica, project-silica, 5d-optical-storage, data-storage, femtosecond-laser, research, deep-research]
status: published
---

# Glass/Silica Data Storage: เก็บข้อมูล 10,000+ ปีในแก้ว

> Deep Research เรื่อง Glass/Silica Data Storage — เทคโนโลยีเก็บข้อมูลถาวรบนแก้วด้วย femtosecond laser สร้าง voxel ระดับนาโน อายุขัย 10,000+ ปี (Microsoft Project Silica) ถึง 10²⁰ ปี (5D Optical Storage) ไม่ต้องใช้ไฟเวลาไม่อ่าน (อัปเดต 2 มิ.ย. 2026, Nature 2026 + SPhotonix commercialization)

---

## มันคืออะไร?

**Glass/Silica Data Storage** คือการใช้ **femtosecond laser** (พัลส์สั้น ~10⁻¹⁵ วินาที) ยิงเข้าไปในแก้ว เพื่อสร้างโครงสร้างนาโนเรียกว่า **voxel** (volume pixel) — ข้อมูลถูกเข้ารหัสเป็นการเปลี่ยนแปลงสมบัติทางแสงของแก้ว ไม่ต้องใช้ไฟเก็บ **อยู่ได้ 10,000+ ปี**

ถ้า SSD เก็บด้วย electric charge, HDD เก็บด้วย magnetic field — Glass Storage เก็บด้วย **โครงสร้างทางกายภาพในแก้ว** ที่ไม่เสื่อม

### Voxel คืออะไร? (สรุปสั้น)

**Voxel = Volume Pixel** — ถ้า pixel คือจุด 2D บนหน้าจอ, voxel คือจุด 3D ในปริมาตร

- **1 voxel** = จุดข้อมูล 1 จุดในแก้ว (ขนาด ~2-5 µm — ใกล้เคียงแบคทีเรีย)
- ถูกสร้างด้วย **femtosecond laser pulse** → เปลี่ยนโครงสร้างระดับนาโนของแก้วตรงจุดนั้น → **ถาวร** ไม่สลาย
- Voxel ไม่ได้เก็บแค่ "มี/ไม่มี" (0/1) แต่เก็บ **สมบัติทางแสง** ได้หลายค่า → เก็บได้ 3-6.6 bits/voxel
- สมบัติที่ใช้: **polarization angle** (มุมแสง), **retardance** (ความหน่วงแสง), **refractive index** (ดัชนีหักเห)

| Level | ข้อมูลที่เก็บได้ | ใช้ใน |
|:------|:----------------|:-------|
| 2 levels (0/1) | 1 bit/voxel | Basic |
| 8 levels | 3 bits/voxel | Birefringent (Fused Silica) |
| 100 levels | ~6.6 bits/voxel | Project Silica Gen 2 (สูงสุด) |

> 📖 **อ่านเพิ่ม:** [[Voxel-and-Optical-Properties-Explained]] — อธิบาย voxel, polarization, retardance, refractive index แบบเข้าใจง่าย พร้อมภาพประกอบ

### ทำไมต้องสนใจ?

- ข้อมูลโลกปี 2025 มีมากกว่า **120+ zettabytes** และเพิ่มขึ้น ~20% ต่อปี
- Cloud archival storage ใช้ HDD/tape ที่ต้อง **copy ทุก 3-5 ปี** เพื่อป้องกันข้อมูลเสีย
- การ copy ข้อมูลซ้ำๆ ใช้ **พลังงานมหาศาล** — Project Silica ตั้งเป้าลด carbon footprint ของ archival storage อย่างมีนัยสำคัญ
- Glass storage เขียนครั้งเดียว → ไม่ต้อง copy อีกเลย → **ประหยัดพลังงาน + ลด e-waste**

---

## 2 สายหลัก

| | **Microsoft Project Silica** | **5D Optical Storage (Southampton → SPhotonix)** |
|--|--|--|
| เป้าหมาย | Cloud archival storage (Azure) | Ultra-long-term preservation + commercial data center |
| วัสดุ | Fused Silica / Borosilicate (Pyrex) | Fused Quartz |
| ขนาดแผ่น | 120 × 120 × 2 mm | Disc format |
| ความจุ | 2-5 TB/แผ่น (ขึ้นกับวัสดุ) | หลาย TB → **360 TB (ทฤษฎี)** |
| อายุขัย | 10,000+ ปี | **13B+ ปี** (ห้อง) / 13.8B ปี (190°C) |
| สถานะ | Research complete, Gen 2 demo | **มีบริการพาณิชย์แล้ว** — SPhotonix raise $4.5M |
| Paper | Nature (Feb 2026) | Optica Express (2013-2024) |
| Startup | Microsoft internal | SPhotonix (spinoff 2024, Southampton) |

---

## End-to-End Process: Project Silica

```
User Data → Compress → Encrypt → +FEC → Symbol Encode → Femtosecond Laser → Glass (เขียน)
Glass → Microscope → CNN Decode → FEC → Decrypt → Decompress → Data (อ่าน)
```

### ขั้นตอนเขียน (Write)

**1. Data Preparation**
- **Compression** — บีบอัดข้อมูล
- **Encryption** — เข้ารหัสลับ
- **FEC (Forward Error Correction)** — เพิ่ม redundant bits เพื่อกู้คืนเมื่อมี error

### FEC คืออะไร? (ทำไมต้องมี?)

FEC = **Forward Error Correction** — เป็นเทคนิคเพิ่มข้อมูลสำรอง (redundant bits) เข้าไปตอนเขียน เพื่อให้ **อ่านคืนได้ถูกต้องแม้บาง voxel เสีย**

**ปัญหา:** แก้วถาวร แต่ไม่ได้หมายความว่าทุก voxel จะอ่านได้สมบูรณ์ 100%:
- รอยขีดข่วนบนแก้ว → บาง voxel อาจเบลอ
- Read noise จากกล้อง → ภาพไม่ชัดเจน
- Cross-talk ระหว่าง voxel ข้างเคียง → สัญญาณรบกวน

**วิธีทำงานของ FEC:**

```
ข้อมูลเดิม:     [1] [0] [1] [1] [0] [1] [0] [0]
                  ↓ FEC encode (เพิ่ม parity bits)
เขียนลงแก้ว:    [1] [0] [1] [1] [0] [1] [0] [0] [P1] [P2] [P3]
                                                    ↑    ↑    ↑
                                              redundant bits
                  
อ่านกลับ (มี error): [1] [0] [?] [1] [0] [1] [0] [0] [P1] [P2] [P3]
                                    ↑
                              voxel นี้เสีย
                  
FEC decode: ใช้ P1 P2 P3 คำนวณ → ได้ [1] คืน → **ข้อมูลครบถ้วน**
```

**ประเภท FEC ที่ใช้:**

| ประเภท | ใช้ที่ไหน | ความสามารถ |
|:-------|:----------|:-----------|
| Reed-Solomon | CD/DVD/QR code | แก้ burst errors |
| LDPC (Low-Density Parity-Check) | Project Silica, 5G, Wi-Fi | แก้ random errors ได้ดีมาก |
| Polar Codes | 5G control channel | แก้ errors ในสภาพ noise สูง |

> Project Silica ใช้ **LDPC codes** — เป็น FEC รุ่นใหม่ที่ใช้ใน 5G และ deep space communication (NASA) ทน noise ได้ดีมาก
> 
> **Overhead:** FEC เพิ่มข้อมูล ~20-50% แต่แลกกับการกู้ errors ได้แม้ raw BER (Bit Error Rate) จะสูงถึง 10⁻³ → หลัง FEC decode ลดเหลือ **< 10⁻¹²** (แทบจะไม่มี error เลย)

**2. Symbol Encoding**
- Bits ถูกจัดกลุ่มเป็น **symbols** (1 symbol = 1 voxel)
- แต่ละ voxel เก็บได้ **มากกว่า 1 bit** (multi-level encoding — สูงสุด 100 levels)

**3. Laser Writing** 🔬

ใช้ **femtosecond laser** — พัลส์แสงสั้นมาก (~100 femtoseconds = 10⁻¹³ วินาที) — สั้นกว่าการกะพริบตา **1 ล้านล้านเท่า**

**เลเซอร์ modulate (ปรับ) ยังไงเพื่อเขียนข้อมูล?**

เลเซอร์ไม่ได้ยิงแค่ "เปิด/ปิด" — แต่ปรับพารามิเตอร์ 2 ตัวเพื่อสร้าง voxel ที่ต่างกัน:

| พารามิเตอร์ | หมายถึง | เปลี่ยนยังไง | ผลลัพธ์ |
|:-----------|:--------|:-------------|:--------|
| **Energy (พลังงานพัลส์)** | แรงของแสง | ปรับความแรงของพัลส์ | ควบคุมขนาด + รูปร่าง nanovoid |
| **Polarization (ทิศทางสั่น)** | ทิศทางที่แสงสั่น | หมุนทิศทาง polarization | ควบคุม orientation ของ nanograting |

**การ modulate ทำงานจริง:**

```
Birefringent Voxels (Fused Silica):
                                      
  Seed pulse (พลังงานต่ำ)     Data pulse (พลังงานสูง + polarization)
       ↓                            ↓
  ┌─────────┐              ┌──────────────────┐
  │ สร้าง    │      →      │ ยืด + กำหนด       │
  │ nanovoid│              │ ทิศทาง voxel      │
  │ เริ่มต้น  │              │ → ข้อมูลถูกเขียน    │
  └─────────┘              └──────────────────┘
  
  เปลี่ยน polarization → เปลี่ยนมุม nanograting → เก็บค่าต่างกัน
  8 มุม = 3 bits/voxel (หรือมากกว่า)

Phase Voxels (Borosilicate):
                                   
  Data pulse (single pulse)
       ↓
  ┌──────────────────┐
  │ เปลี่ยน refractive │
  │ index ของแก้ว     │ → ข้อมูลถูกเขียน
  │ ตรงจุดนั้นโดยตรง    │
  └──────────────────┘
  
  เปลี่ยนพลังงานพัลส์ → เปลี่ยนระดับ phase shift → เก็บค่าต่างกัน
```

**ทำไมต้อง femtosecond (ไม่ใช่ ms, µs, หรือ ns)?**

| เวลาพัลส์ | เกิดอะไรขึ้น | ใช้ได้ไหม |
|:---------|:------------|:---------|
| millisecond (10⁻³ s) | แก้วร้อน → ระเบิด/แตก | ❌ ทำลายแก้ว |
| microsecond (10⁻⁶ s) | ร้อนเกิน → melt พื้นที่ใหญ่ | ❌ ไม่แม่นยำ |
| nanosecond (10⁻⁹ s) | ดีขึ้น แต่ยังมี heat diffusion | ⚠️ พอใช้ แต่ไม่แม่น |
| **femtosecond (10⁻¹⁵ s)** | **พลังงานสูงมาก ส่งในเวลาสั้นมาก → ไม่มีเวลากระจายความร้อน** | **✅ แม่นยำระดับนาโน** |

> **Non-thermal ablation:** Femtosecond laser ส่งพลังงานทั้งหมดก่อนที่ความร้อนจะกระจาย → ตัดวัสดุโดยไม่ทำให้รอบข้างร้อน → เหมือน "ตัดน้ำแข็งด้วยเลเซอร์โดยที่น้ำแข็งไม่ละลาย"

**เขียนหลายชั้นยังไง?**
- เลเซอร์โฟกัสได้ **ตามความลึก (z-axis)** — เปลี่ยนระยะโฟกัส = เขียนชั้นต่างกัน
- เขียนเป็นชั้นๆ (layer by layer) จากล่างขึ้นบน — สูงสุด **100 layers** ใน 2mm แก้ว
- ระยะห่างระหว่างชั้น: ~20 µm
- ความถี่เลเซอร์: **10 MHz** (10 ล้านพัลส์/วินาที)
- **Multi-beam parallel writing:** ใช้หลาย beams พร้อมกัน → 4 beams = 65.9 Mbit/s, 16 beams = ~263.6 Mbit/s

**4. ประเภท Voxel 2 แบบ**

| | Birefringent Voxels | Phase Voxels |
|--|--|--|
| กลไก | Anisotropic change (ขึ้นกับทิศทางวัด) | Isotropic refractive index change |
| วัสดุ | Fused Silica **เท่านั้น** | แก้วใส่ทุกชนิด (รวม Borosilicate/Pyrex) |
| ความจุ/voxel | สูง (8 polarization levels → สูงสุด 100 levels) | ต่ำกว่า |
| พัลส์ | 2 (seed + data) | 1 |
| ต้นทุน | แพงกว่า | **ถูกกว่า** (Pyrex = ราคาถูกกว่า fused silica หลายเท่า) |
| หมายเหตุ | Phase voxels เป็นนวัตกรรมใหม่ของ Gen 2 — ทำให้ใช้แก้วที่ถูกกว่าได้ |

> **ทำไม Borosilicate (Pyrex) ถึงสำคัญ?** Fused silica แพงมาก แต่ Pyrex เป็นแก้วที่ผลิตได้ง่าย ราคาถูก และมีอยู่ทั่วไป — Microsoft เลือกใช้ phase voxels กับ Pyrex แม้ความจุจะต่ำกว่า (2 TB vs 5 TB) แต่ต้นทุนต่อ TB ถูกกว่ามาก

### ขั้นตอนอ่าน (Read)

**1. Microscope Scanning** 🔭
- Gen 2: ใช้ **กล้องเดียว** (wide-field polarization microscope) — ก่อนหน้าต้องใช้ 3 ตัว
- Auto: fiducial alignment + focus + z-stack capture
- จับภาพ voxel ทีละชั้น

**2. CNN Decoding** 🧠
- ภาพส่งเข้า **Convolutional Neural Network (CNN)**
- CNN แก้:
  - Read noise
  - Inter-voxel cross-talk
  - 3D inter-symbol interference
- แปลง pixel pattern → symbol → bit stream

**3. Error Correction + Decryption**
- **FEC decode** — ตรวจ + แก้ errors
- **Decrypt** → **Decompress** → ได้ข้อมูลคืน

---

## End-to-End Process: 5D Optical Storage

### "5 Dimensions" คืออะไร?

| มิติ | พารามิเตอร์ | วิธีควบคุม |
|:----|:-----------|:----------|
| 1st | X (แนวนอน) | ตำแหน่งเลเซอร์ |
| 2nd | Y (แนวตั้ง) | ตำแหน่งเลเซอร์ |
| 3rd | Z (ความลึก) | โฟกัสเลเซอร์ |
| **4th** | **Slow axis orientation** | **Polarization** เลเซอร์ |
| **5th** | **Retardance strength** | **Intensity** เลเซอร์ |

### กลไก Nanograting

- Femtosecond laser สร้าง **nanogratings** ที่ self-assemble ในแก้ว (เรียกว่า **FemtoEtch™** โดย SPhotonix)
- Features เล็กเพียง **20 nm** — เล็กที่สุดที่สร้างด้วยแสง
- Nanogratings สร้าง **birefringence** — เปลี่ยนวิธีเดินของแสง
- เหมือนแว่นกันแดด polarized: แต่ละโครงสร้างเปลี่ยนแสงต่างกัน → อ่านแยกได้

### การอ่าน 5D
- ส่องแสงผ่านแก้ว
- วิเคราะห์ birefringence: orientation + retardance
- ถอดรหัส 5 มิติ → digital data

---

## เปรียบเทียบสื่อเก็บข้อมูล

| สื่อ | มิติ | ความจุ | อายุขัย | ต้องใช้ไฟ? | ต้นทุน/GB (ประมาณ) |
|:----|:-----|:-------|:--------|:----------|:-------------------|
| CD | 2D | ~700 MB | 10-50 ปี | ไม่ (แต่ผิวเสื่อม) | ~$0.01 |
| DVD | 3D | ~17 GB | 10-50 ปี | ไม่ | ~$0.005 |
| Blu-ray | 3D | ~128 GB | 10-50 ปี | ไม่ | ~$0.02 |
| HDD | Magnetic | 20+ TB | 3-5 ปี | **ใช้** | ~$0.015 |
| SSD/Flash | Semiconductor | ตามรุ่น | ~10 ปี | **ใช้** | ~$0.05 |
| LTO-10 Tape | Magnetic | 36 TB | 15-30 ปี | ไม่ (ต้องดูแล) | ~$0.005 |
| DNA Storage | Molecular | 455 EB/g | 500-10,000+ ปี | ไม่ | **~$1,000+** (ยังแพง) |
| **Project Silica** | **3D + optical** | **2-5 TB** | **10,000+ ปี** | **ไม่** | ยังไม่พาณิชย์ (แต่วัสดุถูก) |
| **5D Glass** | **5D** | **360 TB (ทฤษฎี)** | **13B+ ปี** | **ไม่** | พาณิชย์แล้ว (ราคา premium) |

> **ความสำคัญ:** ต้นทุนหลักของ tape/HDD archival ไม่ใช่แค่อุปกรณ์ แต่คือ **"copy cost"** — ต้องย้ายข้อมูลทุก 3-5 ปี ใช้ไฟ + แรงงาน + เครื่องใหม่ → Glass storage ตัดต้นทุนนี้ออกทั้งหมด

---

## วิธีทดสอบ (Testing)

### 1. Accelerated Aging Test (Arrhenius Equation)

{% raw %}
$$k = A \times e^{-E_a / RT}$$
{% endraw %}

- อบแก้วที่ **200-400°C** → วัดอัตราเสื่อมของ voxels
- Extrapolate กลับที่ 25°C → อายุขัย **> 10,000 ปี**
- Project Silica: ทดสอบจริง ยืนยัน > 10,000 ปีที่อุณหภูมิห้อง
- 5D Memory Crystal: ทนอุณหภูมิสูงถึง **1,000°C** โดยไม่เสียข้อมูล

### 2. Environmental Testing

- จุ่มน้ำ / ฉีดฝุ่น / แช่เย็นจัด
- คลื่นแม่เหล็กไฟฟ้า (EMI)
- แรงกระแทกโดยตรงถึง **½ ตัน** (5D glass)
- ทนอุณหภูมิสูงถึง **1,000°C**
- ทนรังสี cosmic (ทดสอบบน Falcon Heavy)

### 3. Read/Write Verification

- เขียน known pattern → อ่านกลับ → เทียบ BER (Bit Error Rate)
- ทดสอบว่า FEC แก้ errors ได้จริง
- Gen 2: CNN decoder ลด raw error rate จาก ~10⁻³ → **near-zero** หลัง FEC

### 4. Cross-talk & Inter-symbol Interference

- เขียน voxels หนาแน่น → วัด interference ระหว่าง voxel ข้างเคียง
- ทดสอบ CNN แก้ 3D inter-symbol interference ได้จริง
- 100 layers ใน 2mm → voxel spacing ~20µm → cross-talk เป็น challenge หลัก

---

## สเปค Project Silica Gen 2

| เมตริก | Fused Silica | Borosilicate (Pyrex) |
|:-------|:------------|:-------------|
| ขนาดแผ่น | 120 × 120 × 2 mm | 120 × 120 × 2 mm |
| ความจุ | **4.84 TB** | **2.02 TB** |
| ความเร็วเขียน (1 beam) | 25.6 Mbit/s | 25.6 Mbit/s |
| ความเร็วเขียน (4 beams) | — | 65.9 Mbit/s |
| ความเร็วเขียน (16 beams) | ~263.6 Mbit/s | ~263.6 Mbit/s |
| Voxel type | Birefringent (สูงกว่า) | Phase (ต่ำกว่า) |
| ราคาวัสดุ | แพงกว่า | **ถูกกว่า** (Pyrex = cheap) |
| อายุขัย | 10,000+ ปี | 10,000+ ปี |
| ข้อดี | ความจุสูงกว่า 2.4x | ถูกกว่า เขียนได้หลาย beam |

> เทียบกับ **LTO-10 Tape:** 400 MB/s (uncompressed) → 1,000 MB/s (compressed) — เร็วกว่า 12-30x
>
> **แต่** tape ต้อง copy ใหม่ทุก 5-10 ปี → total cost of ownership (TCO) ของ glass อาจถูกกว่าในระยะยาว

---

## SPhotonix & 5D Memory Crystal: พาณิชย์แล้ว

SPhotonix เป็น **spinoff จาก University of Southampton** (ก่อตั้ง 2024) โดย Prof. Peter Kazansky — ผู้บุกเบิก 5D optical storage มากว่า 30 ปี

### เหตุการณ์สำคัญ

| ปี | เหตุการณ์ |
|:---|:---------|
| **2013** | สาธิต 5D optical storage ครั้งแรก (300 KB text file) |
| **2016** | เก็บ Universal Declaration of Human Rights, Bible, Magna Carta ลง 5D crystal |
| **2018** | Arch Mission Foundation ส่ง 5D crystal (Isaac Asimov Foundation Trilogy) ขึ้น SpaceX Falcon Heavy → โคจรรอบดวงอาทิตย์ **30 ล้านปี** |
| **2024** | เก็บ **human genome ฉบับสมบูรณ์** บน 5D memory crystal → CNN "blueprint to restore humanity" |
| **2024** | SPhotonix ก่อตั้ง, **raise $4.5M pre-seed** (Creator Fund + XTX Ventures) |
| **2024** | Boucheron luxury ring: แหวนเพชรฝัง 5D memory crystal (Quatre 5D Memory ring) |
| **2024** | GOG: เก็บ video game icon ลง 5D crystal "forever" |
| **2025-2026** | **Pilot 5D storage ใน data centers** — SPhotonix เตรียมทดสอบกับ enterprise clients |
| **2026** | Plans for **space data centres** — 5D crystal ทนสภาพอวกาศ |

### บริการ SPhotonix ปัจจุบัน

- **5D Memory Crystal™** — custom preservation service สำหรับ luxury, cultural heritage, DNA
- Swiss-made crystal — ผลิตในโรงงานมาตรฐานสวิส
- รับ order สำหรับ:
  - DNA/personal genome preservation
  - Cultural artifacts (หนังสือ, ศิลปะ, ประวัติศาสตร์)
  - Luxury brands (เช่น Boucheron)
  - Corporate archival

---

## Sustainability: ทำไม Glass Storage ถึงสำคัญสำหรับโลก

### ปัญหา Archival Storage ปัจจุบัน

```
HDD/Tape Archival Lifecycle (วนซ้ำทุก 3-5 ปี):
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Write Data │ →  │  Copy/Refresh │ →  │  Verify Data │
│  to Media   │    │  to New Media │    │  Integrity   │
└─────────────┘    └──────────────┘    └──────────────┘
       ↑                                    │
       └──────── ทุก 3-5 ป์ ───────────────┘
```

- ทุกรอบใช้ **ไฟฟ้า + แรงงาน + อุปกรณ์ใหม่** + สร้าง e-waste
- Data center ใช้พลังงาน **1-2% ของไฟฟ้าโลก** (และเพิ่มขึ้นเรื่อยๆ)
- Archival data = **60-80%** ของข้อมูลทั้งหมดใน cloud แต่แทบไม่ถูกเข้าถึง

### Glass Storage Solution

```
Glass Archival Lifecycle (เขียนครั้งเดียว):
┌─────────────┐
│  Write Data │
│  to Glass   │ →  ไม่ต้องทำอะไรอีกเลย 10,000+ ปี
└─────────────┘
```

- **ไม่ต้อง copy** — ข้อมูลอยู่ในแก้วถาวร
- **ไม่ต้องใช้ไฟ** — ไม่มี moving parts, ไม่มี charge ที่รั่ว
- **ไม่มี e-waste** — แก้วไม่เป็นพิษ, รีไซเคิลได้
- **TCO ต่ำกว่า** — แม้ต้นทุนเขียนจะแพงกว่า แต่ไม่ต้องดูแล

> Microsoft ประเมินว่า archival storage ด้วย glass สามารถลด **total energy consumption** ได้หลายสิบเท่าเมื่อเทียบกับ HDD-based archival ในระยะเวลา 10+ ปี

---

## Roadmap & อนาคต

### Project Silica (Microsoft)

| Phase | เป้าหมาย | สถานะ |
|:------|:---------|:------|
| Gen 1 | Proof of concept (fused silica, 3 cameras) | ✅ สำเร็จ |
| Gen 2 | Borosilicate support, 1 camera, multi-beam | ✅ สำเร็จ (Nature 2026) |
| Gen 3 (เป้า) | Scale write speed, reduce cost, integrate with Azure | 🔬 In progress |
| Commercial | Azure archival tier ด้วย glass | 📋 ยังไม่มี timeline ชัดเจน |

### 5D Memory Crystal (SPhotonix)

| Phase | เป้าหมาย | สถานะ |
|:------|:---------|:------|
| Lab demo | พิสูจน์ 5D storage ได้ | ✅ สำเร็จ (2013) |
| Custom service | Luxury + cultural preservation | ✅ ขายอยู่ |
| Data center pilot | Cold storage สำหรับ enterprise | 🔬 1-2 ปีข้างหน้า |
| Space data center | 5D crystal ในอวกาศ | 📋 Long-term vision |

---

## เทียบกับ DNA Storage

| | **Glass/Silica** | **DNA Storage** |
|--|--|--|
| ความจุ | 5 TB/แผ่น → 360 TB (ทฤษฎี) | **455 EB/g** (ทฤษฎี — ชนะขาด) |
| อายุขัย | 10,000+ → 13B+ ปี | 500-10,000+ ปี (ขึ้น storage condition) |
| Write speed | ~25 Mbit/s/beam (เร็วกว่า) | **~1 Kbit/s** (ช้ากว่า 25,000x) |
| Read speed | Seconds → minutes | Hours → days |
| ต้นทุน write | ยังไม่พาณิชย์ (แต่วัสดุถูก) | **~$1,000+/GB** (แพงมาก) |
| ความเสถียร | ทนทุกสภาพ (น้ำ, ไฟ, รังสี) | ต้องควบคุม temp/humidity |
| Maturity | ใกล้พาณิชย์ (5D) / ยังวิจัย (Silica) | ยังวิจัย แต่ progress เร็ว |

> **สรุป:** DNA ชนะเรื่องความหนาแน่น แต่ Glass ชนะเรื่อง speed + stability + cost → **ทั้งสองอาจเติมเต็มกัน** ไม่ใช่แข่งกัน

---

## การใช้งานจริง

### ที่ผ่านมา

- **2016** — เก็บ Universal Declaration of Human Rights, Bible ลง 5D crystal
- **2018** — Arch Mission Foundation ส่ง 5D crystal (Isaac Asimov Foundation Trilogy) ขึ้น SpaceX Falcon Heavy → โคจรรอบดวงอาทิตย์ 30 ล้านปี
- **2024** — University of Southampton เก็บ **human genome ฉบับสมบูรณ์** บน 5D memory crystal → "เผยพันธุกรรมมนุษย์ไว้เป็นล้านปี"
- **2024** — Boucheron แหวน Quatre 5D Memory ring — ฝัง 5D crystal ในแหวนเพชร
- **2024** — GOG เก็บ video game icon ลง 5D crystal "forever"

### ที่จะเกิดขึ้น

- **Azure cloud archival** — Microsoft วางแผนใช้ Project Silica เป็น cold storage tier (ไม่มี timeline ชัดเจน)
- **Enterprise data center pilot** — SPhotonix เตรียมทดสอบกับ data centers ใน 1-2 ปีข้างหน้า
- **Space archival** — ทนรังสี + ทนอุณหภูมิ → เหมาะสำหรับ deep space preservation
- **National archives** — ห้องสมุดแห่งชาติ, พิพิธภัณฑ์ ที่ต้องเก็บข้อมูลถาวร

---

## ข้อจำกัด

| ปัญหา | รายละเอียด |
|:------|:----------|
| **WORM** | Write Once Read Many — เขียนครั้งเดียว ไม่ลบ/แก้ไขได้ |
| **เขียนช้า** | ~25.6 Mbit/s/beam vs LTO-10: 8,000 Mbit/s — ช้ากว่า ~300x |
| **อ่านช้า** | ต้องสแกนด้วย microscope + CNN → เป็นนาที ไม่ใช่มิลลิวินาที |
| **อุปกรณ์แพง** | Femtosecond laser (write) + polarization microscope (read) |
| **ยังไม่พาณิชย์** (Silica) | Microsoft บอก "research phase complete" แต่ไม่มีแผนขาย |
| **ความจุต่ำกว่า HDD** | 5 TB/แผ่น 120mm² vs HDD 20+ TB 3.5" |
| **ไม่มี random access** | ต้องอ่านตามลำดับ layer → ไม่เหมาะสำหรับ random I/O |

### เหมาะสำหรับ ✅
- Archival storage (เก็บถาวรระดับชาติ)
- Cold storage (ข้อมูลที่ไม่ค่อยเข้าถึง)
- ข้อมูลประวัติศาสตร์ / วัฒนธรรม
- Space archival (ทนสภาพอวกาศ)
- Compliance/regulatory data (ต้องเก็บ 7-10+ ปี)
- Backup ระดับ "last resort"

### ไม่เหมาะ ❌
- Hot data / ข้อมูลที่แก้ไขบ่อย
- ใช้แทน HDD/SSD ปกติ
- Real-time access / random I/O
- ข้อมูลที่ต้อง update บ่อย

---

## สรุป Flow แบบเต็ม

### Write Flow (Project Silica)

```
1. รับข้อมูลผู้ใช้
2. บีบอัด (Compression)
3. เข้ารหัสลับ (Encryption)
4. เพิ่ม FEC bits (Forward Error Correction)
5. แปลง bits → symbols (หลาย bit ต่อ 1 symbol)
6. Modulate เลเซอร์ (energy + polarization)
7. Femtosecond laser ยิง:
   ├─ Seed pulse → สร้าง nanovoid เริ่มต้น
   └─ Data pulse → ยืดเป็น voxel สุดท้าย
8. เลื่อน beam/แก้ว → voxel ถัดไป
9. ซ้อนเป็นชั้นๆ (100 layers, ล่างขึ้นบน)
10. เขียนจนเต็มความหนาแก้ว ✅
```

### Read Flow (Project Silica)

```
1. วางแผ่นแก้วใน automated microscope (กล้องเดียว Gen 2)
2. Auto: fiducial alignment + focus + z-stack
3. จับภาพ voxel ทีละชั้น (wide-field imaging)
4. ส่งภาพเข้า CNN:
   ├─ แยก signal จาก noise
   ├─ แก้ inter-voxel cross-talk
   └─ แก้ 3D inter-symbol interference (100 layers)
5. CNN → symbols → bits
6. FEC decode → ตรวจ + แก้ errors
7. Decrypt → Decompress
8. ได้ข้อมูลผู้ใช้คืน ✅
```

---

## Sources

- Microsoft Research Blog: "Project Silica's advances in glass storage technology" (Feb 2026)
- Nature: "Laser writing in glass for dense, fast and efficient archival data storage" (Feb 2026)
- Nature Sustainability: "Sustainable glass-based data storage" (2026)
- Ars Technica: "Microsoft's new 10,000-year data storage medium: glass" (Feb 2026)
- Tom's Hardware: "Project Silica write-once storage" (Feb 2026)
- Blocks & Files: "Project Silica finds cheaper glass, boosts write speeds but trims capacity" (Feb 2026)
- The Register: "Microsoft's latest storage tech encodes data into Pyrex" (Feb 2026)
- IEEE Spectrum: "Laser-Written Glass Could Store Data for Millennia" (2026)
- C&EN: "Glass data storage solution could last millennia" (Feb 2026)
- StorageNewsletter: "Project Silica's Advances in Glass Data Storage Technology" (Feb 2026)
- ACM: "Project Silica: Towards Sustainable Cloud Archival Storage in Glass" (2024)
- 5D Memory Crystal / SPhotonix: 5dmemorycrystal.com
- University of Southampton: "Human genome stored on everlasting memory crystal" (Sep 2024)
- CNN: "Scientists store entire human genome on memory crystal" (Sep 2024)
- Arch Mission Foundation: archmission.org/5d-optical-memory
- [[DNA-Data-Storage-Deep-Research-2026]] — เปรียบเทียบกับ DNA storage
