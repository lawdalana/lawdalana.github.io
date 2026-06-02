---
title: "Voxel และสมบัติทางแสง: อธิบายให้เข้าใจง่าย"
notetype: feed
date: 2026-06-02
last_modified: 2026-06-02
tags: [glass-storage, voxel, optical-properties, polarization, retardance, refractive-index, femtosecond-laser, tutorial]
status: published
---

# Voxel และสมบัติทางแสง: อธิบายให้เข้าใจง่าย

> เจาะลึกเรื่อง **voxel** และ **สมบัติทางแสง** ที่ทำให้ Glass/Silica Data Storage เก็บข้อมูลได้หลาย bits ต่อ voxel — polarization, retardance, refractive index — อธิบายด้วยภาษาธรรมดา + ภาพประกอบ
>
> 📖 อ่านคู่กับ: [[Glass-Silica-Data-Storage-2026]]

---

## Voxel คืออะไร?

**Voxel = Volume Pixel** — ถ้า pixel คือจุด 2D บนหน้าจอ, voxel คือจุด 3D ในปริมาตร

```
Pixel (2D):          Voxel (3D):
┌───┬───┬───┐       ┌───┐
│ ■ │ □ │ ■ │       │ ■ │  ← ชั้น 1 (z=0)
├───┼───┼───┤       ├───┤
│ □ │ ■ │ □ │       │ □ │  ← ชั้น 2 (z=1)
└───┴───┴───┘       └───┘
 แบน 2 มิติ          ลึก 3 มิติ
```

### ใน Glass Storage

- **1 voxel** = จุดข้อมูล 1 จุดในแก้ว (ขนาด ~2-5 µm)
- Voxel ถูกสร้างด้วย **femtosecond laser pulse** ที่ยิงเข้าไปในแก้ว
- เลเซอร์เปลี่ยนโครงสร้างระดับนาโนของแก้วตรงจุดนั้น → สร้าง **nanovoid** (รูเล็กๆ) หรือ **nanograting** (แผ่นบางๆ เรียงกัน)
- การเปลี่ยนแปลงนี้ **ถาวร** — ไม่สลาย ไม่เสื่อม ไม่ต้องใช้ไฟรักษา

### แต่ละ voxel เก็บได้มากกว่า 1 bit

| Level | ข้อมูลที่เก็บได้ | ใช้ใน |
|:------|:----------------|:-------|
| 2 levels (0/1) | 1 bit/voxel | Basic |
| 8 levels | 3 bits/voxel | Project Silica (birefringent) |
| 100 levels | ~6.6 bits/voxel | Project Silica Gen 2 (สูงสุด) |

### ขนาดของ voxel เทียบกับสิ่งอื่น

| อะไร | ขนาด |
|:-----|:-----|
| เส้นผม | ~70 µm |
| เม็ดทราย | ~60-2000 µm |
| เซลล์เม็ดเลือดแดง | ~7 µm |
| **Voxel (Glass Storage)** | **~2-5 µm** |
| Bacteria | ~1-5 µm |
| Nanograting features (5D) | **~20 nm** |

→ ขนาด voxel ใกล้เคียงแบคทีเรีย — ต้องใช้กล้องจุลทรรศน์อ่าน

---

## ทำไม Voxel เก็บได้หลาย Level?

Voxel ไม่ได้เก็บแค่ "มี/ไม่มี" (เหมือน CD ที่มีแค่ pit/land) แต่เก็บ **สมบัติทางแสง** ได้หลายค่า — แต่ละค่าสามารถแบ่งเป็น multiple levels ได้:

```
CD/DVD (เก็บ 1 bit/จุด):
  pit  = 0      land = 1
  (มี/ไม่มี เท่านั้น)

Glass Storage (เก็บหลาย bit/voxel):
  voxel 1: polarization=45°,  retardance=λ/4  → symbol "5"
  voxel 2: polarization=135°, retardance=λ/2  → symbol "11"
  voxel 3: refractive index change=0.005      → symbol "3"
  ...
  แต่ละสมบัติ = แกนที่เก็บข้อมูลได้ 1 แกน
```

---

## สมบัติทางแสงทั้ง 3 แบบ

### 1. มุม Polarization (Slow Axis Orientation) 🔄

**แสงคืออะไร?** แสงเป็นคลื่นแม่เหล็กไฟฟ้า — สั่นได้หลายทิศทาง

```
แสงปกติ (สั่นทุกทิศ):        Polarized (สั่นทิศเดียว):
    ↗ ↑ ↖                        ↑ ↑ ↑
  ← ● →                          ● → →
    ↘ ↓ ↙                        
                                 
เหมือนเชือกที่สั่นไปมา          เหมือนเชือกที่สั่นขึ้น-ลงอย่างเดียว
```

**Polarization คือ** "ทิศทางที่แสงสั่น" — แสงสามารถสั่นขึ้น-ลง, ซ้าย-ขวา, หรือทแยงมุมก็ได้

**เก็บข้อมูลยังไง:**
- Femtosecond laser สร้าง **nanograting** ในแก้ว — แผ่นบางๆ เรียงกันเป็นระเบียบ
- Nanograting หมุน **ทิศสั่นของแสง** ที่ผ่านมัน → แต่ละมุม = ค่าต่างกัน
- สมมติวัดได้ 8 มุม (0°, 45°, 90°, ..., 315°) → **3 bits/voxel**
- วัดได้ 100 มุม → **~6.6 bits/voxel**

```
เลเซอร์ยิงด้วย polarization ต่างกัน:

เลเซอร์ polarized แนวตั้ง ↕     เลเซอร์ polarized แนวนอน ↔
       ↓                                ↓
  ═══╪═══╪═══                    ││││││││││││
  nanograting แนวนอน              nanograting แนวตั้ง
  → เก็บ "0"                       → เก็บ "1"
  
อ่าน: ส่องแสงผ่าน → วัดมุม polarization ที่ออกมา → รู้ค่าข้อมูล
```

> **เปรียบเทียบ:** เหมือนแว่นกันแดด polarized — หมุนแว่นแต่ละมุมจะเห็นแสงต่างกัน → voxel แต่ละอัน "หมุน" แสงต่างมุมกัน → อ่านแยกได้

**ใช้ใน:** Birefringent Voxels → Fused Silica (Project Silica)

---

### 2. Retardance (ความแรงของการหน่วงแสง) 📏

**Retardance คือ** แสงส่องผ่าน voxel → ถูก **หน่วง/ชะลอ** ไม่เท่ากันในแต่ละทิศ

```
แสงเข้า →  [voxel]  → แสงออก
  ↑                    ↑ ↑
  1 ความยาวคลื่น      ทิศ A: ผ่านเร็ว (ไม่หน่วง)
                       ทิศ B: ผ่านช้า (หน่วง λ/4, λ/2, λ...)
                       
  ความต่าง = retardance → วัดได้เป็นตัวเลข
```

**ทำไมถึงหน่วงไม่เท่ากัน?**
- Nanograting สร้างโครงสร้างที่มีทิศทาง (anisotropic) — เหมือนไม้ไผ่เรียงกัน
- แสงสั่น **ขนาน** กับแนว nanograting → ผ่านช้า (ถูกหน่วง)
- แสงสั่น **ตั้งฉาก** กับแนว nanograting → ผ่านเร็ว (ไม่ถูกหน่วง)
- ความต่างของ "ช้า vs เร็ว" = **retardance** → วัดได้เป็นตัวเลข

```
Nanograting หนาแน่น (retardance สูง):     Nanograting เบาบาง (retardance ต่ำ):
  ═══╪═══╪═══╪═══╪═══                       ═══╪═══╪═══
  หน่วงมาก → เก็บ "level 7"                 หน่วงน้อย → เก็บ "level 2"
  
ควบคุมด้วย: พลังงานเลเซอร์ → nanograting หนาแน่นมาก/น้อย → retardance สูง/ต่ำ
```

**เก็บข้อมูลยังไง:**
- เลเซอร์ควบคุม **intensity (พลังงานพัลส์)** → ควบคุมความหนาแน่นของ nanograting → ควบคุม retardance
- Retardance แต่ละระดับ = ข้อมูล 1 level
- ยิ่ง resolution ของการวัดสูง → แบ่ง level ได้มาก → เก็บ bits ได้มาก

> **เปรียบเทียบ:** เหมือนกระจกบานเดียวกัน แต่บางจุดหนากว่า → แสงผ่านช้ากว่า → วัดความหนาได้ = อ่านข้อมูลได้

**ใช้ใน:** Birefringent Voxels → Fused Silica (Project Silica) + 5D Memory Crystal (SPhotonix)

> **ความสัมพันธ์กับ Birefringence:** Retardance เกิดจาก **birefringence** — สมบัติของวัสดุที่มี refractive index ต่างกันตามทิศทาง ทำให้แสงเดินด้วยความเร็วต่างกันในแต่ละทิศ → ผลคือ retardance

---

### 3. Refractive Index Change (การเปลี่ยนดัชนีหักเห) 🔀

**Refractive Index (n) คือ** ตัวเลขบอกว่า **แสงเดินช้าลงแค่ไหน** เมื่อผ่านวัสดุ

```
อากาศ (n=1.0):     แก้ว (n=1.5):
แสง →  ████████     แสง →  ████████
       เร็ว (300K km/s)    ช้าลง 33% (200K km/s)
```

- อากาศ n=1.0 → แสงเดินเต็มความเร็ว (300,000 km/s)
- แก้ว n=1.5 → แสงช้าลง 33%
- เพชร n=2.4 → แสงช้าลง 58% → เหตุผลที่เพชร "เป็นประกาย"

**เก็บข้อมูลยังไง:**

```
แก้วเดิม:  n = 1.500 ทุกจุด (ไม่มีข้อมูล)

หลังเลเซอร์ยิง:
แสง →  [n=1.501] [n=1.505] [n=1.510] [n=1.515]
         level 1    level 2    level 3    level 4
         
เปลี่ยนพลังงานพัลส์ → เปลี่ยน n มาก/น้อย → แต่ละระดับ = ข้อมูล 1 level
```

- Femtosecond laser pulse เปลี่ยน **ความหนาแน่นของแก้ว** ตรงจุด voxel แบบ **isotropic** (เท่ากันทุกทิศ — ไม่มีทิศทาง)
- เปลี่ยนพลังงานพัลส์ → เปลี่ยน refractive index มาก/น้อย → แต่ละระดับ = ข้อมูล 1 level
- อ่านโดยส่องแสงผ่าน + วัด **phase shift** (การเปลี่ยนเฟสของคลื่นแสง)

> **เปรียบเทียบ:** เหมือนแก้วใสที่บางจุด "หนากว่า/บางกว่า" มองไม่เห็นด้วยตาเปล่า แต่ส่องแสงผ่านแล้ววัดการเบี่ยงเบนได้

**ใช้ใน:** Phase Voxels → Borosilicate/Pyrex (Project Silica Gen 2)

> **Phase Voxels vs Birefringent Voxels:** Phase voxels เปลี่ยน refractive index แบบเท่ากันทุกทิศ (isotropic) → เก็บ levels ได้น้อยกว่า แต่ทำงานกับแก้วที่ถูกกว่า (Pyrex) ได้

---

## สรุป: เปรียบเทียบทั้ง 3 สมบัติ

| สมบัติ | วัดอะไร | ควบคุมยังไง | ใช้ใน voxel ประเภทไหน | เก็บ bits ได้มากไหม |
|:------|:--------|:-----------|:---------------------|:-------------------|
| **Polarization angle** | มุมที่แสงถูกหมุน | ทิศทาง polarization ของเลเซอร์ | Birefringent (Fused Silica) | สูง |
| **Retardance** | แสงถูกหน่วงแค่ไหน | พลังงานเลเซอร์ → ความหนาแน่น nanograting | Birefringent (Fused Silica) | สูง |
| **Refractive index** | แสงเดินช้าลงแค่ไหน | พลังงานเลเซอร์ → ความหนาแน่นแก้วตรงจุด | Phase (Borosilicate) | ปานกลาง |

**Birefringent Voxels** ใช้ polarization + retardance → เก็บได้หลาย bits (สูงสุด ~6.6 bits/voxel) แต่ต้องใช้ Fused Silica แพง

**Phase Voxels** ใช้ refractive index change → เก็บได้น้อยกว่า แต่ใช้กับ Borosilicate (Pyrex) ที่ถูกกว่ามาก → **trade-off ระหว่าง cost vs capacity**

---

## เหมือนอะไรในชีวิตจริง?

ลองจินตนาการว่า voxel = กระเป๋าเก็บข้อมูล:

```
CD/DVD (1 bit/จุด):
┌──────────┐
│ มี/ไม่มี  │  ← กระเป๋าเล็ก เก็บได้แค่ "ใช่/ไม่ใช่"
└──────────┘

Birefringent Voxel (3-6.6 bits/voxel):
┌──────────┐
│ มุมหมุน  │  ← กระเป๋าใหญ่ เก็บได้หลายมิติ:
│ หน่วงแสง │     มุมหมุน (polarization) และ ความหนา (retardance)
└──────────┘

Phase Voxel (ปานกลาง):
┌──────────┐
│ ความหนา  │  ← กระเป๋ากลาง เก็บได้ 1 มิติ:
│ แก้ว     │     ความหนาแน่น (refractive index) แต่ทำง่ายกว่า
└──────────┘
```

---

## อ่านเพิ่ม

- [[Glass-Silica-Data-Storage-2026]] — Deep Research เต็มเรื่อง Glass/Silica Data Storage
- [[DNA-Data-Storage-Deep-Research-2026]] — เปรียบเทียบกับ DNA Storage

---

## Sources

- Nature: "Laser writing in glass for dense, fast and efficient archival data storage" (Feb 2026)
- Microsoft Research Blog: "Project Silica's advances in glass storage technology" (Feb 2026)
- 5D Memory Crystal / SPhotonix: 5dmemorycrystal.com/technology
- Wikipedia: 5D optical data storage
