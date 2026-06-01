---
title: "Glass/Silica Data Storage: เก็บข้อมูล 10,000+ ปีในแก้ว (Deep Research 2026)"
notetype: feed
date: 2026-06-01
last_modified: 2026-06-01
tags: [glass-storage, silica, project-silica, 5d-optical-storage, data-storage, femtosecond-laser, research, deep-research]
status: published
---

# Glass/Silica Data Storage: เก็บข้อมูล 10,000+ ปีในแก้ว

> Deep Research เรื่อง Glass/Silica Data Storage — เทคโนโลยีเก็บข้อมูลถาวรบนแก้วด้วย femtosecond laser สร้าง voxel ระดับนาโน อายุขัย 10,000+ ปี (Microsoft Project Silica) ถึง 10²⁰ ปี (5D Optical Storage) ไม่ต้องใช้ไฟเวลาไม่อ่าน (อัปเดต 1 มิ.ย. 2026, Nature 2026 + multiple sources)

---

## มันคืออะไร?

**Glass/Silica Data Storage** คือการใช้ **femtosecond laser** (พัลส์สั้น ~10⁻¹⁵ วินาที) ยิงเข้าไปในแก้ว เพื่อสร้างโครงสร้างนาโนเรียกว่า **voxel** (volume pixel) — ข้อมูลถูกเข้ารหัสเป็นการเปลี่ยนแปลงสมบัติทางแสงของแก้ว ไม่ต้องใช้ไฟเก็บ **อยู่ได้ 10,000+ ปี**

ถ้า SSD เก็บด้วย electric charge, HDD เก็บด้วย magnetic field — Glass Storage เก็บด้วย **โครงสร้างทางกายภาพในแก้ว** ที่ไม่เสื่อม

---

## 2 สายหลัก

| | **Microsoft Project Silica** | **5D Optical Storage (Southampton)** |
|--|--|--|
| เป้าหมาย | Cloud archival storage | Ultra-long-term preservation |
| วัสดุ | Fused Silica / Borosilicate | Fused Quartz |
| ความจุ | 2-5 TB/แผ่น | หลาย TB → 360 TB (ทฤษฎี) |
| อายุขัย | 10,000+ ปี | 10²⁰ ปี (ห้อง) / 13.8B ปี (190°C) |
| สถานะ | Research complete, ยังไม่พาณิชย์ | มีบริการพาณิชย์แล้ว |
| Paper | Nature (Feb 2026) | Optica Express (2013-2024) |

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

**2. Symbol Encoding**
- Bits ถูกจัดกลุ่มเป็น **symbols** (1 symbol = 1 voxel)
- แต่ละ voxel เก็บได้ **มากกว่า 1 bit** (multi-level encoding)

**3. Laser Writing** 🔬
- ใช้ **femtosecond laser** (~100 fs/pulse)
- **Pseudo-single-pulse method:**
  - **Seed pulse** → เริ่มสร้าง nanovoid (รูนาโน)
  - **Data pulse** → ยืด nanovoid เป็น voxel สุดท้าย
- เขียนเป็นชั้นๆ (layer by layer) จากล่างขึ้นบน
- ความถี่เลเซอร์: **10 MHz**
- **Multi-beam:** 4 beams = 65.9 Mbit/s, 16 beams = ~263.6 Mbit/s

**4. ประเภท Voxel 2 แบบ**

| | Birefringent Voxels | Phase Voxels |
|--|--|--|
| กลไก | Anisotropic change (ขึ้นกับทิศทางวัด) | Isotropic refractive index change |
| วัสดุ | Fused Silica **เท่านั้น** | แก้วใส่ทุกชนิด (รวม Borosilicate) |
| ความจุ/voxel | สูง (8 polarization levels) | ต่ำกว่า |
| พัลส์ | 2 (seed + data) | 1 |
| ต้นทุน | แพง | ถูกกว่า |

### ขั้นตอนอ่าน (Read)

**1. Microscope Scanning** 🔭
- ใช้ **automated wide-field polarization microscope** (กล้องเดียวใน Gen 2)
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

- Femtosecond laser สร้าง **nanogratings** ที่ self-assemble ในแก้ว
- Features เล็กเพียง **20 nm** — เล็กที่สุดที่สร้างด้วยแสง
- Nanogratings สร้าง **birefringence** — เปลี่ยนวิธีเดินของแสง
- เหมือนแว่นกันแดด polarized: แต่ละโครงสร้างเปลี่ยนแสงต่างกัน → อ่านแยกได้

### การอ่าน 5D
- ส่องแสงผ่านแก้ว
- วิเคราะห์ birefringence: orientation + retardance
- ถอดรหัส 5 มิติ → digital data

---

## เปรียบเทียบสื่อเก็บข้อมูล

| สื่อ | มิติ | ความจุ | อายุขัย | ต้องใช้ไฟ? |
|:----|:-----|:-------|:--------|:----------|
| CD | 2D | ~700 MB | 10-50 ปี | ไม่ (แต่ผิวเสื่อม) |
| DVD | 3D | ~17 GB | 10-50 ปี | ไม่ |
| Blu-ray | 3D | ~128 GB | 10-50 ปี | ไม่ |
| HDD | Magnetic | 20+ TB | 3-5 ปี | **ใช้** |
| SSD/Flash | Semiconductor | ตามรุ่น | ~10 ปี | **ใช้** |
| LTO-10 Tape | Magnetic | 36 TB | 15-30 ปี | ไม่ (ต้องดูแล) |
| DNA Storage | Molecular | 455 EB/g | 500-10,000+ ปี | ไม่ |
| **Project Silica** | **3D + optical** | **2-5 TB** | **10,000+ ปี** | **ไม่** |
| **5D Glass** | **5D** | **360 TB (ทฤษฎี)** | **10²⁰ ปี** | **ไม่** |

---

## วิธีทดสอบ (Testing)

### 1. Accelerated Aging Test (Arrhenius Equation)

$$k = A \times e^{-E_a / RT}$$

- อบแก้วที่ **200-400°C** → วัดอัตราเสื่อมของ voxels
- Extrapolate กลับที่ 25°C → อายุขัย **> 10,000 ปี**
- Project Silica: ทดสอบจริง ยืนยัน > 10,000 ปีที่อุณหภูมิห้อง

### 2. Environmental Testing

- จุ่มน้ำ / ฉีดฝุ่น / แช่เย็นจัด
- คลื่นแม่เหล็กไฟฟ้า (EMI)
- แรงกระแทกโดยตรงถึง **½ ตัน** (5D glass)
- ทนอุณหภูมิสูงถึง **1,000°C**

### 3. Read/Write Verification

- เขียน known pattern → อ่านกลับ → เทียบ BER (Bit Error Rate)
- ทดสอบว่า FEC แก้ errors ได้จริง

### 4. Cross-talk & Inter-symbol Interference

- เขียน voxels หนาแน่น → วัด interference ระหว่าง voxel ข้างเคียง
- ทดสอบ CNN แก้ 3D inter-symbol interference ได้จริง

---

## สเปค Project Silica Gen 2

| เมตริก | Fused Silica | Borosilicate |
|:-------|:------------|:-------------|
| ขนาดแผ่น | 120 × 120 × 2 mm | 120 × 120 × 2 mm |
| ความจุ | **4.84 TB** | **2.02 TB** |
| ความเร็วเขียน (1 beam) | 25.6 Mbit/s | 25.6 Mbit/s |
| ความเร็วเขียน (4 beams) | — | 65.9 Mbit/s |
| ความเร็วเขียน (16 beams) | ~263.6 Mbit/s | ~263.6 Mbit/s |
| ราคาวัสดุ | แพงกว่า | **ถูกกว่า** |
| อายุขัย | 10,000+ ปี | 10,000+ ปี |

> เทียบกับ **LTO-10 Tape:** 400 MB/s (uncompressed) → 1,000 MB/s (compressed) — เร็วกว่า 12-30x

---

## การใช้งานจริง

- **2018** — Arch Mission Foundation ส่ง 5D crystal (Isaac Asimov Foundation Trilogy) ขึ้น SpaceX Falcon Heavy → โคจรรอบดวงอาทิตย์ 30 ล้านปี
- **2024** — University of Southampton เก็บ **human genome ฉบับสมบูรณ์** บน 5D memory crystal
- **2026** — Microsoft ตีพิมพ์ paper Nature ยืนยัน Gen 2 system ทั้ง fused silica + borosilicate

---

## ข้อจำกัด

| ปัญหา | รายละเอียด |
|:------|:----------|
| **WORM** | Write Once Read Many — เขียนครั้งเดียว ไม่ลบ/แก้ไขได้ |
| **เขียนช้า** | ~25.6 Mbit/s/beam vs LTO-10: 8,000 Mbit/s |
| **อุปกรณ์แพง** | Femtosecond laser + polarization microscope |
| **ยังไม่พาณิชย์** (Silica) | Microsoft บอก "research phase complete" แต่ไม่มีแผนขาย |
| **ความจุต่ำกว่า HDD** | 5 TB/แผ่น 120mm² vs HDD 20+ TB 3.5" |

### เหมาะสำหรับ ✅
- Archival storage (เก็บถาวรระดับชาติ)
- Cold storage (ข้อมูลที่ไม่ค่อยเข้าถึง)
- ข้อมูลประวัติศาสตร์ / วัฒนธรรม
- Space archival (ทนสภาพอวกาศ)

### ไม่เหมาะ ❌
- Hot data / ข้อมูลที่แก้ไขบ่อย
- ใช้แทน HDD/SSD ปกติ
- Real-time access

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
9. ซ้อนเป็นชั้นๆ (layer by layer, ล่างขึ้นบน)
10. เขียนจนเต็มความหนาแก้ว ✅
```

### Read Flow (Project Silica)

```
1. วางแผ่นแก้วใน automated microscope
2. Auto: fiducial alignment + focus + z-stack
3. จับภาพ voxel ทีละชั้น (wide-field imaging)
4. ส่งภาพเข้า CNN:
   ├─ แยก signal จาก noise
   ├─ แก้ inter-voxel cross-talk
   └─ แก้ 3D inter-symbol interference
5. CNN → symbols → bits
6. FEC decode → ตรวจ + แก้ errors
7. Decrypt → Decompress
8. ได้ข้อมูลผู้ใช้คืน ✅
```

---

## Sources

- Microsoft Research Blog (Feb 2026)
- Nature Paper: "Laser writing in glass for dense, fast and efficient archival data storage" (Feb 2026)
- Ars Technica: "Microsoft's new 10,000-year data storage medium: glass" (Feb 2026)
- Tom's Hardware: "Project Silica write-once storage" (Feb 2026)
- Blocks & Files: "Project Silica finds cheaper glass, boosts write speeds" (Feb 2026)
- 5D Memory Crystal: 5dmemorycrystal.com/faq
- Arch Mission Foundation: archmission.org/5d-optical-memory
- University of Southampton: "Human genome stored on everlasting memory crystal" (Sep 2024)
- ACM: "Project Silica: Towards Sustainable Cloud Archival Storage"
- [[DNA-Data-Storage-Deep-Research-2026]] — เปรียบเทียบกับ DNA storage
