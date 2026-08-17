---
title: Probabilistic Data Structures
notetype: feed
date: 2026-08-16
last_modified: 2026-08-17
tags: [data-structures, probabilistic, bloom-filter, hyperloglog, count-min-sketch, minhash, space-saving, ddsketch, streaming, big-data]
status: published
---

# Probabilistic Data Structures: เลือก “คำตอบโดยประมาณ” ให้ตรงกับคำถาม

เมื่อข้อมูลไหลเข้ามาเป็นล้านหรือพันล้านรายการ ปัญหาไม่ได้อยู่ที่ `HashSet` หรือ `HashMap` ตอบผิด แต่เป็นเพราะการเก็บข้อมูลทุกชิ้นเพื่อให้ได้คำตอบแบบแม่นยำอาจใช้หน่วยความจำ เวลา และค่าใช้จ่ายสูงเกินความจำเป็น

**Probabilistic Data Structures** และ **Approximate Streaming Summaries** ใช้วิธีเก็บ “ร่องรอยสรุป” ขนาดเล็กแทนข้อมูลทั้งหมด แล้วตอบคำถามเฉพาะอย่างภายใต้ขอบเขตความผิดพลาดที่อธิบายได้ เช่น

- เคยเห็นค่านี้หรือยัง?
- มีค่าที่ไม่ซ้ำประมาณกี่ค่า?
- ค่านี้เกิดขึ้นประมาณกี่ครั้ง?
- ข้อมูลสองชุดคล้ายกันแค่ไหน?
- ค่าใดเกิดบ่อยที่สุด?
- ค่า p95 หรือ p99 อยู่ที่เท่าไร?

> จุดสำคัญไม่ใช่การบอกว่าโครงสร้างหนึ่ง “แม่น 99%” แต่ต้องบอกให้ครบว่า **อะไรอาจผิด ผิดไปทางไหน มากแค่ไหน และเกิดด้วยความน่าจะเป็นเท่าไร**

![ภาพรวมคำถาม 6 แบบและโครงสร้างข้อมูลที่เหมาะสม](/assets/img/DS/Probabilistic/probabilistic-six-families.svg)

*ภาพรวม: เริ่มจากคำถามที่ระบบต้องตอบ แล้วจึงเลือกโครงสร้างและรูปแบบความคลาดเคลื่อนที่ยอมรับได้*

---

## สรุปสั้น ๆ ของทั้ง 6 แบบ

| โครงสร้าง | คำถามที่ตอบ | คำอธิบายสั้น ๆ |
|---|---|---|
| [[Bloom Filter]] | “เคยมี `x` ไหม?” | เหมือนกระดานติ๊กช่อง ถ้าเจอช่องว่างแปลว่า **ไม่มีแน่ ๆ** แต่ถ้าทุกช่องถูกติ๊ก แปลว่า **อาจมี** และอาจต้องตรวจฐานข้อมูลจริงอีกครั้ง |
| [[HyperLogLog]] | “มีค่าที่ไม่ซ้ำกี่ค่า?” | ไม่เก็บรายชื่อทั้งหมด แต่ดูรูปแบบ hash ที่พบได้ยากเพื่อเดาว่ามีสมาชิกไม่ซ้ำไหลผ่านมามากแค่ไหน |
| [[Count-Min Sketch]] | “`x` เกิดกี่ครั้ง?” | ส่ง `x` ไปถาม counter หลายแถว แล้วเลือกคำตอบที่ต่ำที่สุด เพื่อลดผลจาก key อื่นที่ชนช่องเดียวกัน |
| [[MinHash]] | “ชุด A กับ B คล้ายกันแค่ไหน?” | ทำ “ลายนิ้วมือ” ขนาดเล็กให้แต่ละชุด ยิ่งลายนิ้วมือตรงกันหลายตำแหน่ง สองชุดก็ยิ่งคล้ายกัน |
| [[Space-Saving Algorithm]] | “ค่าไหนเกิดบ่อยที่สุด?” | เหมือนกระดานอันดับที่มีเพียง `k` ช่อง รายการที่มาบ่อยจะอยู่ต่อ ส่วนรายการที่พบน้อยจะถูกแทนที่ |
| [[DDSketch]] | “p50, p95, p99 เท่าไร?” | เหมือน histogram ที่ช่องกว้างขึ้นตามขนาดของค่า จึงสรุปได้ทั้ง latency หลักสิบและหลักพันในโครงสร้างเดียว |

### หมายเหตุเรื่องชื่อหมวด

ทั้งหกแบบเป็น “กล่องเครื่องมือสำหรับข้อมูลขนาดใหญ่” แต่ไม่ได้ใช้กลไกเดียวกันทั้งหมด

- Bloom Filter, HyperLogLog, Count-Min Sketch และ MinHash พึ่งพา hashing หรือ randomization โดยตรง
- Space-Saving แบบพื้นฐานและ DDSketch เป็น approximate streaming summaries ที่ทำงานแบบ deterministic ได้

ดังนั้นข้อความว่า “ทุกโครงสร้างใช้ hash เพื่อบีบข้อมูล” จึงไม่ถูกต้องเสมอไป สิ่งที่เหมือนกันจริง ๆ คือ **ยอมเก็บข้อมูลไม่ครบ เพื่อให้ตอบคำถามเฉพาะอย่างได้ด้วย state ที่เล็กลง**

---

## Approximate ไม่ได้แปลว่าเดาสุ่ม

โครงสร้างแบบ exact และ approximate ต่างกันที่ “ข้อมูลซึ่งเก็บไว้ตอบคำถาม”

| แนวทาง | สิ่งที่เก็บ | สิ่งที่ได้ | ต้นทุนหลัก |
|---|---|---|---|
| Exact | สมาชิกหรือ counter ครบทุก key | คำตอบแม่นยำและมักเรียกดูสมาชิกเดิมได้ | หน่วยความจำโตตามจำนวน key หรือจำนวนค่า |
| Approximate | bit, register, counter, signature หรือ bucket ที่สรุปข้อมูล | คำตอบเฉพาะประเภทพร้อม error contract | ต้องออกแบบพารามิเตอร์ ตรวจสอบ error และมี fallback เมื่อจำเป็น |

ตัวอย่างเช่น HyperLogLog อาจตอบว่า “มีผู้ใช้ไม่ซ้ำประมาณ 10.1 ล้านคน” แต่ไม่สามารถคืนรายชื่อผู้ใช้ทั้ง 10.1 ล้านคนนั้นได้ เพราะรายชื่อไม่ได้ถูกเก็บไว้ตั้งแต่แรก

---

## กลไกของทั้ง 6 แบบในภาพเดียว

![กลไกการบีบข้อมูลของ Bloom Filter, HyperLogLog, Count-Min Sketch, MinHash, Space-Saving และ DDSketch](/assets/img/DS/Probabilistic/probabilistic-six-mechanisms.svg)

*แต่ละโครงสร้างบีบข้อมูลคนละวิธี: bits, registers, counter matrix, signatures, candidate slots และ logarithmic buckets*

---

## 1. Bloom Filter — เช็กว่า “เคยมีไหม?”

> **จำประโยคเดียว:** Bloom Filter ใช้คัดคำตอบว่า “ไม่มีแน่ ๆ” ออกอย่างรวดเร็ว ส่วนคำตอบว่า “มี” แปลได้เพียง “อาจมี”

### นึกภาพแบบง่าย

ลองนึกถึงกระดานสวิตช์ที่เริ่มต้นเป็น `0` ทุกช่อง เมื่อเพิ่มข้อมูลหนึ่งชิ้น เราใช้ hash เลือกหลายช่องแล้วเปิดสวิตช์เหล่านั้นเป็น `1` โดย Bloom Filter ไม่ได้เก็บข้อมูลต้นฉบับไว้เลย

### ตอนเพิ่มข้อมูล

1. คำนวณตำแหน่ง `k` ตำแหน่งจาก item
2. ตั้ง bit ทุกตำแหน่งนั้นเป็น `1`

### ตอนค้นหา

- ถ้ามีอย่างน้อยหนึ่งตำแหน่งเป็น `0` → **ไม่มีแน่นอน**
- ถ้าทุกตำแหน่งเป็น `1` → **อาจมี** เพราะ bit เหล่านั้นอาจถูก item อื่นตั้งไว้

### ตัวอย่างทีละขั้น: bit array 10 ช่อง

เพื่อให้คำนวณตามได้ง่าย สมมติว่าใช้ hash 2 ตัว และได้ตำแหน่งดังนี้ (ตำแหน่งเหล่านี้เป็นค่าจำลองเพื่ออธิบายแนวคิด)

| ข้อมูล | `h1` | `h2` |
|---|---:|---:|
| `apple` | 1 | 4 |
| `banana` | 4 | 7 |

หลังเพิ่ม `apple` และ `banana` กระดานจะเป็น

```text
index: 0 1 2 3 4 5 6 7 8 9
bit:   0 1 0 0 1 0 0 1 0 0
```

ลองค้นหา 3 ค่า:

| ค่าที่ค้นหา | ตำแหน่งที่ตรวจ | ผล | เหตุผล |
|---|---|---|---|
| `apple` | 1, 4 | อาจมี | ทั้งสองช่องเป็น `1` และในตัวอย่างนี้มีอยู่จริง |
| `mango` | 2, 7 | ไม่มีแน่นอน | ช่อง 2 เป็น `0` จึงเป็นไปไม่ได้ว่าเคยเพิ่ม `mango` |
| `grape` | 1, 7 | อาจมี | ทั้งสองช่องเป็น `1` แม้ไม่เคยเพิ่ม `grape` นี่คือ **false positive** |

ตัวอย่างนี้แสดงว่าการชนกันของ bit ทำให้ Bloom Filter ไม่มีคำตอบแบบ “มีแน่นอน” แต่คำตอบแบบ “ไม่มีแน่นอน” มีประโยชน์มาก เพราะช่วยข้ามการอ่านฐานข้อมูลหรือไฟล์ที่ไม่จำเป็นได้

ตัวอย่างการใช้งานที่เหมาะ:

- เช็กว่า event ID อาจเคยถูกประมวลผลแล้วหรือยัง ก่อนอ่านฐานข้อมูลหลัก
- เช็กว่า SST file ของ RocksDB อาจมี key ที่ต้องการหรือไม่ เพื่อลด I/O ที่ไม่จำเป็น
- กรอง URL หรือ object ที่ “ไม่น่าจะอยู่ในชุด” ออกอย่างรวดเร็ว

สำหรับจำนวน item ที่คาดไว้ `n` และ false-positive rate เป้าหมาย `p` ขนาดโดยประมาณคือ

$$m = -\frac{n\ln p}{(\ln 2)^2}$$

และจำนวน hash ที่เหมาะสมคือ

$$k \approx \frac{m}{n}\ln 2$$

### ตัวอย่างคำนวณขนาดจริง

ต้องรองรับ `n = 1,000,000` รายการ และยอมให้ false positive ได้ `p = 1% = 0.01`

$$m = -\frac{1{,}000{,}000\ln(0.01)}{(\ln 2)^2} \approx 9{,}585{,}058\text{ bits}$$

แปลงหน่วยความจำ:

$$\frac{9{,}585{,}058}{8} \approx 1{,}198{,}132\text{ bytes} \approx 1.14\text{ MiB}$$

จำนวน hash ที่เหมาะสม:

$$k \approx \frac{9{,}585{,}058}{1{,}000{,}000}\ln 2 \approx 6.64$$

จึงปัดเป็น `k = 7` hash functions สรุปคือประมาณ `9.585` bits ต่อรายการ หรือ `1.14 MiB` สำหรับหนึ่งล้านรายการ ก่อนนับ metadata และ overhead ของ implementation

> ถ้าใส่ข้อมูลเกิน capacity ที่ใช้คำนวณไว้ false-positive rate จะสูงขึ้น และ Bloom Filter มาตรฐานไม่รองรับการลบโดยตรง

อ่านต่อ: [[Bloom Filter]]

---

## 2. HyperLogLog — นับจำนวนค่าที่ไม่ซ้ำ

> **จำประโยคเดียว:** HyperLogLog บอกได้ว่า “มีคนไม่ซ้ำประมาณกี่คน” แต่บอกไม่ได้ว่า “มีใครบ้าง”

### นึกภาพแบบง่าย

ค่า hash ที่ดีควรกระจายเหมือนการโยนเหรียญ การพบ hash ที่ขึ้นต้นด้วยศูนย์ติดกันยาว ๆ จึงเป็นเหตุการณ์หายาก เช่น โอกาสพบศูนย์นำหน้าอย่างน้อย 4 ตัวอยู่ที่ประมาณ `1/16` ถ้าเห็นรูปแบบหายากเช่นนี้หลายกลุ่ม ก็เป็นสัญญาณว่าน่าจะมีข้อมูลไม่ซ้ำไหลผ่านมาจำนวนมาก

HyperLogLog (HLL) แบ่ง hash ออกเป็นสองส่วน:

1. ส่วนแรกเลือก register
2. ส่วนที่เหลือให้ “คะแนนความหายาก” จากจำนวนศูนย์นำหน้า
3. แต่ละ register จำเฉพาะคะแนนสูงสุดที่เคยพบ ไม่ได้จำ user ID
4. ตอน query จึงรวมคะแนนจาก register ทั้งหมดเป็นค่าประมาณจำนวนสมาชิกไม่ซ้ำ

ข้อมูลซ้ำจะได้ hash เดิม เลือก register เดิม และได้คะแนนเดิม ค่าสูงสุดจึงไม่เปลี่ยนและไม่เพิ่มค่าประมาณ distinct count

### ตัวอย่างคำนวณขนาดเล็ก

สมมติ stream คือ

```text
u1, u2, u1, u3, u4, u5, u6, u7, u8
```

ค่าจริงมี 9 events แต่มีผู้ใช้ไม่ซ้ำ 8 คน เพราะ `u1` ซ้ำหนึ่งครั้ง สมมติว่าใช้ 8 registers และหลัง hash แล้วได้ state นี้:

```text
register: 0 1 2 3 4 5 6 7
value:    3 1 0 2 1 0 4 0
```

มี register ที่ยังเป็นศูนย์ `V = 3` ช่อง ในช่วงที่จำนวน distinct ยังไม่สูง implementation มักใช้ small-range correction ซึ่งมองจำนวน register ว่าง:

$$\hat n = m\ln\left(\frac{m}{V}\right)$$

แทนค่า `m = 8` และ `V = 3`:

$$\hat n = 8\ln\left(\frac{8}{3}\right) \approx 7.85$$

จึงตอบว่า **มีประมาณ 8 คนไม่ซ้ำ** ซึ่งใกล้กับค่าจริง 8 คน ตัวอย่างนี้ตั้งใจใช้ register น้อยเพื่อให้เห็นขั้นตอน; HLL จริงใช้ register มากกว่า รวมค่าด้วย harmonic mean และมีการแก้ bias ตามช่วงข้อมูล

สำหรับ HLL ดั้งเดิมที่มี `m` registers ค่าคลาดเคลื่อนมาตรฐานโดยคร่าวคือ

$$\text{RSE} \approx \frac{1.04}{\sqrt{m}}$$

ถ้า `m = 16,384` registers:

$$\text{RSE} \approx \frac{1.04}{\sqrt{16{,}384}} = \frac{1.04}{128} = 0.008125 = 0.8125\%$$

ถ้ามีค่าจริงราว 1,000,000 ค่า ขนาดของหนึ่ง standard error จึงอยู่ราว `1,000,000 × 0.008125 = 8,125` ค่า นี่เป็นการอธิบายการกระจายของ estimator ไม่ใช่ hard bound ว่าทุกคำตอบต้องอยู่ในช่วงนี้

**ตัวอย่างที่ควรใช้ HLL**

- unique users ต่อวัน
- distinct device IDs ต่อแคมเปญ
- distinct source IPs ต่อช่วงเวลา
- จำนวนสินค้าที่เคยถูกเปิดดู โดยไม่ต้องเก็บ ID ทั้งหมดในตัวนับ

**สิ่งที่ HLL ทำไม่ได้:** คืนรายชื่อ distinct values หรือเช็กว่า user คนหนึ่งอยู่ในชุดหรือไม่

Redis เป็นตัวอย่าง implementation ที่ระบุขนาดสูงสุดประมาณ `12 KB` และ standard error `0.81%` ตัวเลขนี้เป็นคุณสมบัติของ Redis HLL ไม่ใช่ค่าคงที่ของ HLL ทุกตัว

อ่านต่อ: [[HyperLogLog]]

---

## 3. Count-Min Sketch — ประมาณความถี่ของ key ที่ระบุ

> **จำประโยคเดียว:** ถ้ารู้ชื่อ key อยู่แล้วและอยากถามว่า “key นี้เกิดกี่ครั้ง?” ให้ใช้ Count-Min Sketch; ถ้ายังไม่รู้ว่าจะถาม key ไหน CMS เพียงตัวเดียวช่วยค้นหา Top-K ไม่ได้

### นึกภาพแบบง่าย

Count-Min Sketch (CMS) มี counter หลายแถว แต่ละแถวใช้ hash คนละตัวเพื่อส่ง key ไปยังหนึ่งช่อง เมื่อ `A` เข้ามาหนึ่งครั้ง เราจึงเพิ่ม counter ของ `A` หนึ่งช่องใน **ทุกแถว**

บางแถว `A` อาจชนกับ `B` ทำให้ counter สูงเกินจริง แต่โอกาสที่ `A` จะชนหนักเหมือนกันทุกแถวน้อยกว่า เราจึงอ่านทุกแถวแล้วเลือกค่าต่ำที่สุด

### Update `x`

เพิ่ม counter หนึ่งตำแหน่งในทุกแถว

### Query `x`

อ่าน counter ที่ตรงกับ `x` ทุกแถว แล้วคืนค่าต่ำสุด

$$\hat f(x) = \min_i \text{counter}[i, h_i(x)]$$

เหตุผลที่เลือกค่าต่ำสุดคือ collision ทำให้ counter เพิ่มขึ้น ไม่ได้ทำให้ลดลง ในโมเดลมาตรฐานที่ update ด้วยจำนวนไม่ติดลบ เราจึงได้

$$f(x) \le \hat f(x) \le f(x) + \varepsilon N$$

ด้วยความน่าจะเป็นอย่างน้อย `1 - δ` โดย `N` คือจำนวน update รวมทั้งหมด

### ตัวอย่างคำนวณทีละขั้น

สมมติ stream คือ

```text
A, A, B, A, C, B
```

ค่าจริงคือ `A=3`, `B=2`, `C=1` ใช้ CMS ขนาด 3 แถว × 5 ช่อง และสมมติ hash แต่ละแถวส่ง key ไปยังช่องดังนี้:

```text
A → (แถว 1 ช่อง 1, แถว 2 ช่อง 3, แถว 3 ช่อง 0)
B → (แถว 1 ช่อง 1, แถว 2 ช่อง 4, แถว 3 ช่อง 2)
C → (แถว 1 ช่อง 2, แถว 2 ช่อง 3, แถว 3 ช่อง 4)
```

หลังประมวลผลครบ ตาราง counter เป็น

| แถว | ช่อง 0 | ช่อง 1 | ช่อง 2 | ช่อง 3 | ช่อง 4 |
|---|---:|---:|---:|---:|---:|
| `h1` | 0 | 5 | 1 | 0 | 0 |
| `h2` | 0 | 0 | 0 | 4 | 2 |
| `h3` | 3 | 0 | 2 | 0 | 1 |

ลอง query `A`:

1. แถว 1 อ่านได้ `5` เพราะ `A` ชนกับ `B`
2. แถว 2 อ่านได้ `4` เพราะ `A` ชนกับ `C`
3. แถว 3 อ่านได้ `3` และไม่มี key อื่นชนช่องนี้
4. เลือกค่าต่ำสุด: `min(5, 4, 3) = 3`

ดังนั้น CMS ตอบ `A ≈ 3` ซึ่งตรงกับค่าจริงในตัวอย่างนี้ ส่วน `C` อ่านได้ `min(1, 4, 1) = 1` แนวคิดสำคัญคือ **ค่าต่ำสุดช่วยเลือกแถวที่ปนเปื้อนจาก collision น้อยที่สุด** ไม่ได้แปลว่าทุก query จะตรงค่าจริงเสมอไป

พารามิเตอร์ที่ใช้บ่อยคือ

$$w = \left\lceil \frac{e}{\varepsilon} \right\rceil, \qquad d = \left\lceil \ln\frac{1}{\delta} \right\rceil$$

### ตัวอย่างคำนวณขนาดจริง

ต้องการ additive error `ε = 0.1% = 0.001` และ failure probability `δ = 1% = 0.01`

$$w = \left\lceil\frac{e}{0.001}\right\rceil = 2{,}719$$

$$d = \left\lceil\ln\left(\frac{1}{0.01}\right)\right\rceil = \lceil\ln 100\rceil = 5$$

จึงมี counter ทั้งหมด `2,719 × 5 = 13,595` ช่อง ถ้า counter ละ 32 bits หรือ 4 bytes:

$$13{,}595 \times 4 = 54{,}380\text{ bytes} \approx 53.1\text{ KiB}$$

ถ้า stream มี update รวม `N = 1,000,000` ครั้ง ขอบเขต additive error คือ

$$\varepsilon N = 0.001 \times 1{,}000{,}000 = 1{,}000$$

กล่าวคือ ภายใต้โมเดลมาตรฐาน ค่าประมาณไม่ต่ำกว่าค่าจริง และมีโอกาสอย่างน้อย `99%` ที่จะไม่เกิน `ค่าจริง + 1,000` ตาม guarantee นี้

ข้อควรระวังสำคัญคือ error `εN` คิดจาก **จำนวน update รวม** ไม่ใช่จากจำนวนครั้งของ item นั้น จึงอาจใหญ่เกินไปสำหรับ item ที่เกิดน้อย

> CMS ตอบ `count(x)` ได้เมื่อเรามี `x` อยู่แล้ว แต่ตัว sketch ไม่ได้เก็บรายการ key ให้ enumerate ดังนั้น CMS เพียงตัวเดียวหา Top-K จาก key ที่ไม่รู้จักทั้งหมดไม่ได้ ต้องมี candidate set หรืออัลกอริทึม heavy-hitter อีกชั้นหนึ่ง

อ่านต่อ: [[Count-Min Sketch]]

---

## 4. MinHash — ประมาณความคล้ายของสองชุด

> **จำประโยคเดียว:** MinHash เปลี่ยนชุดขนาดใหญ่ให้เป็นลายนิ้วมือสั้น ๆ แล้วนับว่าลายนิ้วมือของสองชุดตรงกันกี่ตำแหน่ง

### เริ่มจาก Jaccard similarity

ถ้าใช้ Jaccard similarity แบบ exact:

$$J(A,B) = \frac{|A\cap B|}{|A\cup B|}$$

เราต้องมีสมาชิกของทั้งสองชุดเพื่อหา intersection และ union ส่วน MinHash จะใช้ hash หลายชุด แต่ละ hash เก็บเพียง **ค่าต่ำสุด** ที่พบในเซต จึงได้ signature จำนวน `k` ตำแหน่งแทนข้อมูลทั้งหมด

เหตุผลที่วิธีนี้ใช้ได้คือ เมื่อใช้ hash family ที่มีคุณสมบัติเหมาะสม แล้วพิจารณาสมาชิกที่มี hash ต่ำที่สุดใน `A ∪ B` ถ้าสมาชิกตัวนั้นอยู่ใน `A ∩ B` ทั้งสองชุดจะเห็นค่าต่ำสุดเดียวกัน โอกาสที่ signature หนึ่งตำแหน่งจะตรงกันจึงเท่ากับ Jaccard similarity

$$\hat J(A,B) = \frac{\text{จำนวนตำแหน่ง signature ที่ตรงกัน}}{k}$$

### ตัวอย่างคำนวณทีละขั้น

ใช้เซตขนาดเล็กเพื่อให้คำนวณด้วยมือได้:

```text
A = {1, 2, 3, 5}
B = {1, 2, 4, 5}
```

สมาชิกที่ซ้ำกันคือ `{1, 2, 5}` มี 3 ตัว และ union คือ `{1, 2, 3, 4, 5}` มี 5 ตัว ดังนั้น

$$J(A,B) = \frac{3}{5} = 0.60$$

ต่อไปลองสร้าง MinHash signature 4 ตำแหน่งด้วย hash แบบง่าย modulo 7:

| Hash | `min hash(A)` | `min hash(B)` | ตรงกันไหม |
|---|---:|---:|---|
| `h1(x) = x mod 7` | 1 | 1 | ตรง |
| `h2(x) = (x + 1) mod 7` | 2 | 2 | ตรง |
| `h3(x) = (2x + 3) mod 7` | 0 | 0 | ตรง |
| `h4(x) = (x + 3) mod 7` | 1 | 0 | ไม่ตรง |

จึงได้

```text
signature(A) = [1, 2, 0, 1]
signature(B) = [1, 2, 0, 0]
```

ตรงกัน 3 จาก 4 ตำแหน่ง:

$$\hat J(A,B) = \frac{3}{4} = 0.75$$

ค่าจริงคือ `0.60` แต่ตัวอย่างประมาณได้ `0.75` เพราะใช้ signature เพียง 4 ตำแหน่ง จึงผันผวนมาก ตัวอย่าง modulo 7 นี้มีไว้สาธิตการคำนวณเท่านั้น ระบบจริงควรใช้ hash family ที่เหมาะสมและ signature ที่ยาวกว่า

ถ้าใช้ `k = 256` และ similarity จริง `J = 0.60` ส่วนเบี่ยงเบนมาตรฐานโดยประมาณคือ

$$\sigma \approx \sqrt{\frac{J(1-J)}{k}}$$

$$\sigma \approx \sqrt{\frac{0.60(1-0.60)}{256}} \approx 0.0306$$

หรือประมาณ `3.06` percentage points ยิ่งเพิ่ม `k` ค่าประมาณยิ่งนิ่งขึ้น แต่ signature ก็ใช้พื้นที่และเวลาเปรียบเทียบมากขึ้น

ก่อนใช้ MinHash ต้องนิยามให้ชัดว่า “หนึ่งสมาชิกของชุด” คืออะไร เช่น

- คำแต่ละคำ
- word shingles ขนาด 3 หรือ 5 คำ
- product IDs ที่ผู้ใช้เคยดู
- DNA k-mers

หาก tokenization ต่างกัน ความหมายของ similarity ก็เปลี่ยน แม้ MinHash configuration จะเหมือนเดิม

อ่านต่อ: [[MinHash]]

---

## 5. Space-Saving — หา heavy hitters ด้วยจำนวนช่องจำกัด

> **จำประโยคเดียว:** Space-Saving เป็นกระดานอันดับที่มีที่นั่งจำกัด รายการที่มาบ่อยจะรักษาที่นั่งไว้ได้ ส่วนรายการที่พบน้อยอาจถูกผู้มาใหม่แทนที่

Space-Saving เก็บรายการ `(item, estimated_count, error)` ไว้เพียง `k` ช่อง จึงไม่ต้องสร้าง counter ให้ทุก item ที่เคยผ่านเข้ามา

เมื่อ item ใหม่เข้ามา:

1. ถ้ามี item อยู่แล้ว → เพิ่ม counter
2. ถ้ายังมีช่องว่าง → เพิ่ม item ด้วย count เท่ากับ 1
3. ถ้าเต็ม → แทน item ที่มี count ต่ำสุดด้วย item ใหม่ และตั้ง count ใหม่เป็น `minimum + 1`

การ “รับช่วง” count ต่ำสุดทำให้ count ของ item ใหม่เริ่มสูงกว่าจำนวนครั้งที่เห็นจริง แต่เราจะบันทึก error เดิมไว้ด้วย วิธีนี้เปิดโอกาสให้ item ที่เพิ่งเริ่มมาแรงเข้าสู่กระดานได้ แทนที่จะถูกกันออกตลอดไป

### ตัวอย่างคำนวณทีละขั้น

กำหนดให้มีเพียง `k = 3` ช่อง และรับ stream นี้:

```text
A, B, A, C, A, B, D, A
```

| ลำดับ | item เข้า | สิ่งที่ทำ | 3 ช่องหลังจบขั้นตอน |
|---:|---|---|---|
| 1 | A | มีช่องว่าง จึงเพิ่ม A | `A:1` |
| 2 | B | มีช่องว่าง จึงเพิ่ม B | `A:1, B:1` |
| 3 | A | A มีอยู่แล้ว จึงบวก 1 | `A:2, B:1` |
| 4 | C | ยังเหลือช่อง จึงเพิ่ม C | `A:2, B:1, C:1` |
| 5 | A | บวก counter ของ A | `A:3, B:1, C:1` |
| 6 | B | บวก counter ของ B | `A:3, B:2, C:1` |
| 7 | D | เต็มแล้ว; C ต่ำสุดที่ 1 จึงแทนด้วย D และตั้ง `1+1` | `A:3, B:2, D:2` โดย D มี error 1 |
| 8 | A | บวก counter ของ A | `A:4, B:2, D:2` |

นับแบบ exact จะได้ `A=4`, `B=2`, `C=1`, `D=1` ส่วน Space-Saving เก็บ `A=4`, `B=2`, `D=2`:

- A และ B ยังอยู่ เพราะเข้ามาบ่อย
- C หายจากกระดาน เพราะถูกแทนออก
- D เคยเข้ามาจริงเพียง 1 ครั้ง แต่รับช่วง count ต่ำสุดมา จึงมีค่าประมาณ 2 และ error 1
- จาก `(estimate=2, error=1)` เรารู้ว่าค่าจริงของ D ตอนนั้นอยู่ในช่วง `2-1` ถึง `2` หรือ `[1,2]`

ในตัวอย่างนี้มี events รวม `N = 8` และ `k = 3` ดังนั้น threshold พื้นฐานคือ

$$\frac{N}{k} = \frac{8}{3} \approx 2.67$$

item ที่มีความถี่มากกว่า `N/k` จะต้องอยู่ใน summary ตาม guarantee ของ Space-Saving; A มีความถี่ 4 จึงผ่านเกณฑ์นี้ ส่วน B มีความถี่ 2 จึงอาจอยู่หรือหลุดก็ได้ แม้ในตัวอย่างนี้ยังอยู่

สิ่งที่ควรจำ:

- ใช้ memory `O(k)` โดยไม่โตตามจำนวน distinct items
- รับประกัน heavy hitters ตาม threshold ที่สัมพันธ์กับ `N/k` ได้ แต่ **Top-K ใกล้จุดตัดอาจเรียงไม่ตรงแบบ exact**
- count ของ item ที่ถูกแทนเข้ามาอาจเป็น overestimate
- Space-Saving พื้นฐานไม่ควรถูกมองว่า merge ได้ด้วยการบวกตารางแบบตรง ๆ

> Redis `TOPK` ใช้ **HeavyKeeper** ไม่ใช่ Space-Saving ทั้งสองแก้โจทย์ heavy hitters เหมือนกัน แต่กลไกและ error behavior ต่างกัน

อ่านต่อ: [[Space-Saving Algorithm]]

---

## 6. DDSketch — ประมาณ percentile ด้วย relative error

> **จำประโยคเดียว:** DDSketch เป็น histogram ที่ bucket ค่อย ๆ กว้างขึ้นตามขนาดของค่า จึงยอมคลาดเป็น “เปอร์เซ็นต์” ใกล้เคียงกันทั้งค่าหลักสิบและหลักพัน

### ทำไมไม่ใช้ bucket กว้างเท่ากัน?

ถ้า bucket กว้าง 10 ms ความคลาดเคลื่อน 10 ms ถือว่าใหญ่มากเมื่อ latency อยู่แถว 20 ms แต่เล็กมากเมื่อ latency อยู่แถว 5,000 ms DDSketch จึงใช้ bucket แบบ logarithmic: ค่ายิ่งใหญ่ ช่วงของ bucket ยิ่งกว้าง แต่สัดส่วนความคลาดเคลื่อนยังใกล้เดิม

เมื่อกำหนด relative accuracy เป็น `α` ค่า bucket base ที่ใช้ในแนวคิดมาตรฐานคือ

$$\gamma = \frac{1+\alpha}{1-\alpha}$$

สำหรับ ideal logarithmic mapping ของค่าบวก `v` เราสามารถเขียนขั้นตอนหลักได้เป็น

$$k(v) = \left\lceil\log_{\gamma}(v)\right\rceil$$

เมื่อ query ระบบจะเดิน cumulative count จนถึงอันดับที่ต้องการ แล้วคืนค่าตัวแทนของ bucket เช่น

$$\tilde v(k) = \frac{2\gamma^k}{\gamma+1}$$

ด้วยการวางขอบเขตเช่นนี้ ค่าตัวแทนจะคลาดจากค่าบวกใน bucket ไม่เกินสัดส่วน `α` ตาม ideal mapping ส่วน implementation จริงอาจใช้ log approximation, storage policy และการจัดการศูนย์หรือค่าติดลบเพิ่มเติม

### ตัวอย่างคำนวณทีละขั้น

เพื่อให้เห็น bucket ชัด กำหนด relative accuracy ค่อนข้างหยาบที่ `α = 10% = 0.10`

$$\gamma = \frac{1+0.10}{1-0.10} = \frac{1.10}{0.90} \approx 1.2222$$

ใช้ข้อมูล latency 7 ค่า:

```text
10, 11, 12, 20, 21, 22, 100 ms
```

เมื่อนำแต่ละค่าไปคำนวณ `k(v) = ceil(logγ(v))` จะได้

| bucket `k` | ค่าที่ตกใน bucket | count | cumulative count | ค่าตัวแทน `ṽ(k)` |
|---:|---|---:|---:|---:|
| 12 | 10, 11 | 2 | 2 | 10.00 ms |
| 13 | 12 | 1 | 3 | 12.22 ms |
| 15 | 20 | 1 | 4 | 18.26 ms |
| 16 | 21, 22 | 2 | 6 | 22.32 ms |
| 23 | 100 | 1 | 7 | 90.93 ms |

**หา p50**

1. มีข้อมูล `n = 7` ค่า
2. nearest-rank ของ p50 คือ `ceil(0.50 × 7) = 4`
3. cumulative count ถึงอันดับ 4 ที่ bucket 15
4. DDSketch จึงตอบค่าตัวแทนประมาณ `18.26 ms`
5. ค่า exact อันดับ 4 คือ `20 ms`; relative error คือ `|18.26-20|/20 ≈ 8.7%` ซึ่งยังอยู่ใน `α = 10%`

**หา p90**

1. nearest-rank คือ `ceil(0.90 × 7) = 7`
2. อันดับ 7 อยู่ที่ bucket 23
3. DDSketch ตอบประมาณ `90.93 ms`
4. ค่า exact คือ `100 ms`; relative error คือ `|90.93-100|/100 ≈ 9.1%`

ตัวอย่างนี้จงใจใช้ `α = 10%` เพื่อให้เห็นการรวม bucket ชัดเจน งาน monitoring จริงมักเลือกค่าที่ละเอียดกว่า เช่น 1–2% ตาม error budget และต้นทุนหน่วยความจำ

เหมาะกับข้อมูลที่กระจายหลาย order of magnitude เช่น

- API latency ตั้งแต่ไม่กี่ millisecond ถึงหลายวินาที
- payload sizes
- transaction values
- queue wait times

อีกตัวอย่างหนึ่ง ถ้ามี latency 20 ค่าเรียงจากน้อยไปมาก:

```text
42, 45, 48, 50, 51, 54, 55, 58, 61, 64,
68, 73, 81, 90, 95, 110, 124, 160, 210, 860 ms
```

ถ้าใช้ nearest-rank แบบ exact จะได้ `p50=64 ms`, `p95=210 ms`, `p99=860 ms` ส่วน DDSketch จะคืนค่าจาก bucket ใกล้ค่าดังกล่าวภายใต้ relative-value error ที่ตั้งไว้

### สมการหาจำนวน buckets

สำหรับค่าบวกในช่วงที่ต้องการรองรับตั้งแต่ `v_min` ถึง `v_max` ให้หาหมายเลข bucket ของปลายช่วงก่อน:

$$k_{\min} = \left\lceil\log_{\gamma}(v_{\min})\right\rceil, \qquad
k_{\max} = \left\lceil\log_{\gamma}(v_{\max})\right\rceil$$

จำนวนตำแหน่ง bucket ที่ครอบคลุมช่วงทั้งหมดแบบนับหัวและท้ายจึงเป็น

$$B = k_{\max} - k_{\min} + 1$$

หรือเขียนแทน `k` ลงไปได้โดยตรง:

$$B =
\left\lceil\frac{\ln(v_{\max})}{\ln(\gamma)}\right\rceil
- \left\lceil\frac{\ln(v_{\min})}{\ln(\gamma)}\right\rceil
+ 1$$

ถ้าต้องการกะขนาดอย่างรวดเร็ว ให้ดู dynamic range `R = v_max/v_min`:

$$B \;\text{โตประมาณ}\;
\frac{\ln(R)}{\ln(\gamma)}
= \frac{\ln(v_{\max}/v_{\min})}{\ln(\gamma)}$$

และเมื่อ `α` มีค่าน้อย จะมี `ln(γ) ≈ 2α` จึงเห็น trade-off ได้ง่ายขึ้นว่า

$$B \approx \frac{\ln(v_{\max}/v_{\min})}{2\alpha}$$

**ลองกับตัวอย่างด้านบน:** `α = 0.10`, `γ ≈ 1.2222`, `v_min = 10` และ `v_max = 100`

$$k_{\min} = \left\lceil\frac{\ln 10}{\ln 1.2222}\right\rceil = 12$$

$$k_{\max} = \left\lceil\frac{\ln 100}{\ln 1.2222}\right\rceil = 23$$

$$B = 23 - 12 + 1 = 12\text{ bucket positions}$$

ตารางตัวอย่างมี bucket ที่ count ไม่เป็นศูนย์เพียง 5 ช่อง แต่ช่วงตั้งแต่ index 12 ถึง 23 มีทั้งหมด 12 ตำแหน่ง ความต่างนี้สำคัญเพราะ sparse store อาจเก็บเฉพาะช่องที่มีข้อมูล ขณะที่ dense store อาจจองพื้นที่ตาม index span

สำหรับค่าติดลบ DDSketch แยกเก็บ bucket ตามขนาดสัมบูรณ์อีกฝั่งหนึ่ง ส่วนค่าที่ใกล้ศูนย์เก็บใน `zero_count` ดังนั้นหากข้อมูลมีทั้งสองเครื่องหมาย ต้องคำนวณช่วง bucket ของฝั่งบวกและลบแยกกัน

หน่วยความจำของ DDSketch ไม่ใช่ตัวเลขคงที่ เพราะขึ้นกับ

- ค่า `α`
- ช่วงค่าต่ำสุดถึงสูงสุดที่พบ
- รูปแบบการเก็บ bucket
- นโยบาย collapse เมื่อจำกัดจำนวน bins

Datadog ยกตัวอย่าง configuration เฉพาะที่ relative accuracy `2%` สำหรับช่วง `1 ms` ถึง `1 minute` ซึ่งใช้ประมาณ 275 buckets หรือประมาณ `2 KB` เมื่อ counter ละ 64 bits ตัวเลขนี้เป็นตัวอย่างตามช่วง, การปัดขอบเขต และ implementation ไม่ใช่ขนาดสากลของ DDSketch

อ่านต่อ: [[DDSketch]]

---

## Error ของแต่ละแบบหน้าตาไม่เหมือนกัน

![รูปแบบความคลาดเคลื่อนของโครงสร้างข้อมูลโดยประมาณ](/assets/img/DS/Probabilistic/probabilistic-error-models.svg)

*อย่าใช้คำว่า “accuracy 99%” เพียงลำพัง เพราะ false-positive rate, estimator variance, additive error และ relative-value error เป็นคนละหน่วยกัน*

| โครงสร้าง | สิ่งที่อาจคลาดเคลื่อน | ทิศทางหรือหน่วยของ error |
|---|---|---|
| Bloom Filter | ตอบว่า “อาจมี” ทั้งที่ไม่มี | false-positive probability; ปกติไม่มี false negative ภายใต้การ insert อย่างถูกต้องและไม่ลบ bit แบบผิดวิธี |
| HyperLogLog | จำนวน distinct สูงหรือต่ำกว่าค่าจริง | การกระจายของ estimator; ลดลงเมื่อเพิ่ม registers |
| Count-Min Sketch | `count(x)` สูงกว่าค่าจริง | one-sided additive error `εN` ในโมเดล update ไม่ติดลบ |
| MinHash | Jaccard estimate สูงหรือต่ำกว่าค่าจริง | sampling variance ซึ่งขึ้นกับ `J` และ signature length `k` |
| Space-Saving | candidate/count ใกล้ cutoff ไม่ตรง exact | bounded candidate summary และ count overestimate จากการแทนช่อง |
| DDSketch | ค่าของ quantile คลาดจากค่าจริง | relative-value error `α`; ไม่ใช่คำรับประกัน rank error แบบเดียวกับทุก quantile sketch |

---

## ตัวอย่างเดียว ใช้ครบทั้ง 6 แบบ

สมมติระบบ e-commerce รับ event ต่อเนื่อง และอยากสร้าง dashboard แบบ near real-time

**ข้อมูลอ้างอิงขนาดเล็กสำหรับทดสอบ**

```text
product stream: A, A, B, A, C, B, A, D, B, A, C, A
user stream:    u1, u2, u1, u3, u4, u2, u5, u1, u6, u5, u7, u1
```

ค่าจริงที่ใช้เป็น ground truth คือสินค้า `A=6, B=3, C=2, D=1` และมีผู้ใช้ไม่ซ้ำ `7` คน

| คำถามในระบบ | โครงสร้าง | ตัวอย่างผลลัพธ์และวิธีใช้ |
|---|---|---|
| event `evt-99` เคยประมวลผลหรือยัง? | Bloom Filter | ถ้าได้ “ไม่มี” ให้ประมวลผลต่อได้ ถ้าได้ “อาจมี” ให้ตรวจ event store อีกครั้งเพื่อเลี่ยงการทิ้ง event จาก false positive |
| วันนี้มีผู้ใช้ไม่ซ้ำกี่คน? | HyperLogLog | ควรได้ค่าประมาณใกล้ `7`; ใน production ขนาดใหญ่ยอมรับค่าคลาดตาม precision ที่กำหนด |
| สินค้า A ถูกเปิดกี่ครั้ง? | Count-Min Sketch | ค่าจริงคือ `6`; sketch อาจตอบ `6` หรือสูงกว่าเล็กน้อยจาก collision |
| session สองชุดมีพฤติกรรมคล้ายกันไหม? | MinHash | จากตัวอย่างก่อนหน้า Jaccard จริงคือ `0.60`; signature สั้น 4 ตำแหน่งประมาณได้ `0.75` และจะนิ่งขึ้นเมื่อเพิ่มจำนวนตำแหน่ง |
| สินค้าใดกำลังเป็น heavy hitters? | Space-Saving | ใช้ช่องจำนวนจำกัดติดตาม A, B และผู้สมัครใกล้ลำดับถัดไป โดยไม่เก็บ count ของทุกสินค้า |
| latency p95/p99 เท่าไร? | DDSketch | สำหรับชุดตัวอย่าง exact คือ `210/860 ms`; sketch ตอบค่าจาก logarithmic buckets ภายใน relative error ที่ตั้งไว้ |

> ค่าจริงในตารางมีไว้สำหรับอธิบายและตรวจสอบ การทำงานใน production ต้องเปรียบเทียบ sketch กับ exact sample เป็นระยะ ไม่ควรสมมติว่าค่าประมาณจะตรงทุกครั้ง

---

## ตารางเปรียบเทียบแบบไม่ซ่อนเงื่อนไข

| โครงสร้าง | State หลัก | ปุ่มปรับ accuracy | การรวมข้อมูลจากหลายเครื่อง |
|---|---|---|---|
| Bloom Filter | `m` bits, `k` positions | capacity `n`, FPR `p` | OR ได้เฉพาะ layout/hash/config ที่เข้ากัน และต้องประเมิน capacity/FPR หลังรวม |
| HyperLogLog | `m` registers | precision/register count | ใช้ max ต่อ register เมื่อ precision, hash และรูปแบบ state เข้ากัน |
| Count-Min Sketch | `d × w` counters | `ε`, `δ`, counter width | บวก counter ตำแหน่งเดียวกัน เมื่อ dimensions และ hash/seed ตรงกัน |
| MinHash | signature ยาว `k` | signature length, hash family | signature ของ union ใช้ minimum ต่อช่องได้เมื่อ hash family เดียวกัน; การ compare ไม่ใช่การ merge |
| Space-Saving | `k` candidate entries | จำนวนช่อง `k` | แบบพื้นฐานไม่ใช่ element-wise merge; ต้องใช้อัลกอริทึมหรือ implementation ที่นิยาม merge โดยเฉพาะ |
| DDSketch | logarithmic buckets | `α`, range/store/collapse policy | บวก bucket counts ได้เมื่อ mapping, accuracy และ storage semantics เข้ากัน |

**คำว่า mergeable จึงไม่ใช่เพียง ✅ หรือ ❌** แต่เป็นสัญญาว่า state จากทุก shard ใช้ precision, dimensions, hash seed, bucket mapping และเวอร์ชันที่เข้ากัน

---

## เลือกตัวไหนดี?

![Workflow เลือก Probabilistic Data Structure จากชนิดของคำถาม](/assets/img/DS/Probabilistic/probabilistic-decision-workflow.svg)

*Workflow ที่ปลอดภัย: เริ่มจากชนิดของคำตอบ ตรวจ error contract ตรวจ merge compatibility แล้ว validate กับข้อมูล exact*

สรุปเป็นคำถามสั้น ๆ:

1. ต้องการตอบแบบ membership หรือไม่? → Bloom Filter
2. ต้องการเพียงจำนวน unique โดยไม่ต้องรู้ว่าเป็นใครบ้าง? → HyperLogLog
3. มี key แล้วและอยากรู้ frequency ของ key นั้น? → Count-Min Sketch
4. ต้องการ similarity ระหว่างสองชุด? → MinHash
5. ต้องการ candidate Top-K จาก stream? → Space-Saving หรือ heavy-hitter algorithm ที่เหมาะกับ workload
6. ต้องการ percentile ของ distribution? → DDSketch หรือ quantile sketch ที่ตรงกับ error contract
7. ต้องการคำตอบ exact, ต้องลบ/แก้ย้อนหลัง, หรือต้อง audit รายการได้หรือไม่? → ใช้ exact state หรือทำระบบ hybrid ที่ sketch เป็นด่านแรกและมี source of truth สำหรับยืนยัน

---

## Workflow ออกแบบก่อนขึ้น production

### 1. เขียน query contract ให้ชัด

อย่าเริ่มจาก “อยากใช้ HLL” ให้เริ่มจาก “ต้องการจำนวน unique ต่อ tenant ต่อ 5 นาที และยอมคลาดได้เท่าไร”

### 2. ระบุ failure ที่ยอมรับได้

ตัวอย่าง:

- Bloom false positive 1% ยอมรับได้ เพราะมี database ตรวจซ้ำ
- CMS overcount ไม่เกิน 0.1% ของ traffic รวม
- p99 latency ยอมคลาดเชิงสัมพัทธ์ไม่เกิน 1%
- รายการ Top-K ใกล้อันดับ 10 ต้องมี candidate buffer แล้วค่อยนับ exact

### 3. ประเมิน workload

เก็บค่าประมาณของ capacity, total updates, distinct count, value range, skew, retry rate และจำนวน shards เพราะค่าเหล่านี้มีผลต่อ sizing และ error จริง

### 4. เลือก parameters จากสูตร ไม่ใช่จากตัวเลขจำ

ขนาด `12 KB`, `5 KB` หรือ `1%` ที่เห็นในตัวอย่างอาจเป็นของ implementation และ configuration หนึ่งเท่านั้น

### 5. กำหนด config identity

บันทึก version, precision, dimensions, hash algorithm, seed, bucket mapping และ window ไว้พร้อม state เพื่อป้องกันการ merge sketch ที่เข้ากันไม่ได้

### 6. สร้าง exact sample เป็น control group

เก็บข้อมูล exact สำหรับบาง tenant, บาง shard หรือบางช่วงเวลา แล้ววัด observed error อย่างต่อเนื่อง

### 7. วาง fallback

คำตอบที่มีผลต่อ billing, security, access control หรือการลบข้อมูลมักไม่ควรพึ่ง sketch เพียงชั้นเดียว ให้ใช้ sketch เป็น pre-filter แล้วตรวจ source of truth

### 8. เฝ้าระวัง saturation และ drift

แจ้งเตือนเมื่อ Bloom เกิน capacity, counter ใกล้ overflow, value range ของ DDSketch กว้างขึ้น, distribution เปลี่ยน หรือ error จาก exact sample เกิน budget

---

## ตัวอย่างการต่อเข้ากับระบบ

### Redis: membership, distinct count และ point frequency

```text
# Bloom Filter: FPR 1%, capacity 1,000,000
BF.RESERVE seen-events 0.01 1000000
BF.ADD seen-events evt:123
BF.EXISTS seen-events evt:123

# HyperLogLog: daily active users
PFADD dau:2026-08-16 user:42 user:99
PFCOUNT dau:2026-08-16

# Count-Min Sketch: product frequency
CMS.INITBYPROB product-freq 0.001 0.01
CMS.INCRBY product-freq sku:A 1
CMS.QUERY product-freq sku:A
```

ข้อควรระวัง:

- Redis HLL ที่ระบุ `12 KB / 0.81%` เป็น implementation-specific
- `CMS.INITBYPROB` ใช้ error และ probability เพื่อกำหนด dimensions
- Redis `TOPK` ใช้ HeavyKeeper จึงไม่ควรใช้ผลลัพธ์หรือ guarantee ของ Space-Saving ไปอธิบายแทน

### BigQuery: approximate aggregation

```sql
SELECT
  APPROX_COUNT_DISTINCT(user_id) AS approx_unique_users,
  APPROX_TOP_COUNT(product_id, 10) AS approx_top_products,
  APPROX_QUANTILES(latency_ms, 100)[OFFSET(95)] AS approx_p95_ms
FROM `project.dataset.events`
WHERE event_date = DATE '2026-08-16';
```

BigQuery ระบุว่า approximate aggregate functions แลก statistical uncertainty กับการใช้ memory และเวลาที่รองรับข้อมูลขนาดใหญ่ ฟังก์ชัน convenience กลุ่มนี้ไม่ได้เปิด precision parameter ให้กำหนดเอง และไม่ควรสรุปว่าแต่ละฟังก์ชันใช้ implementation ภายในชนิดใด หากเอกสารไม่ได้ระบุไว้

---

## ข้อผิดพลาดที่พบบ่อย

1. **ใช้ sketch ผิดคำถาม** — HLL นับ unique ได้ แต่เช็ก membership หรือคืนรายชื่อไม่ได้
2. **เรียกทุกอย่างว่า accuracy 99%** — แต่ละโครงสร้างมีหน่วย error คนละแบบ
3. **ใช้ CMS หา Top-K โดยไม่มี candidate set** — matrix ไม่ได้เก็บ key ให้ enumerate
4. **merge state คนละ config** — ผลลัพธ์อาจผิดโดยไม่มี error ชัดเจน
5. **ใส่ Bloom เกิน capacity** — FPR จริงสูงกว่าเป้าหมาย
6. **นับ retry ซ้ำ** — sketch ไม่รู้เองว่า event เดิมถูกส่งซ้ำ ต้องออกแบบ idempotency/window ให้ชัด
7. **ใช้ percentile จาก sample เล็กเกินไป** — ต่อให้ sketch แม่น ค่า p99 ของหน้าต่างเล็กก็ผันผวนได้มาก
8. **ใช้ hash ที่อ่อนแอกับ input จากผู้ไม่หวังดี** — adversarial collisions อาจทำลาย accuracy หรือ performance
9. **เชื่อค่าประมาณกับงานที่ต้อง audit** — billing, quota enforcement และ security decision ควรมี exact verification
10. **ไม่ทดสอบกับ distribution จริง** — สูตรเป็นจุดเริ่มต้น แต่ skew, range และ cardinality จริงเป็นตัวตัดสินผลใน production

---

## ระบบที่ใช้แนวคิดเหล่านี้จริง

| ระบบ | โครงสร้างหรือ API | ใช้ทำอะไร |
|---|---|---|
| Redis | Bloom Filter, HyperLogLog, Count-Min Sketch, Top-K | membership, cardinality, frequency และ heavy hitters; Top-K ใช้ HeavyKeeper |
| RocksDB | Bloom Filter / Ribbon Filter ต่อ SST | ตัดไฟล์หรือ data blocks ที่ไม่น่ามี key ออกจาก read path |
| BigQuery | `APPROX_COUNT_DISTINCT`, `APPROX_QUANTILES`, `APPROX_TOP_COUNT`, `APPROX_TOP_SUM` | approximate aggregation ที่ scale กับข้อมูลขนาดใหญ่ |
| Datadog | DDSketch | รวม distribution จากหลายแหล่งและคำนวณ percentile ของ monitoring data |
| Apache DataSketches | HLL, frequency, quantiles, Theta, KLL และอื่น ๆ | ไลบรารี sketch สำหรับงาน distinct, frequency, sampling และ quantiles |

---

## สรุป

Probabilistic Data Structures ไม่ได้มีไว้แทน exact data structures ทุกกรณี แต่มีไว้เมื่อระบบต้องตอบ **คำถามเฉพาะอย่างด้วย state ที่เล็ก คงที่ หรือ merge กระจายได้**

วิธีเลือกที่ถูกต้องคือ

1. เริ่มจากคำถาม
2. เลือก error contract ที่ธุรกิจยอมรับ
3. คำนวณ parameters จาก workload
4. กำหนด merge compatibility
5. วัดเทียบกับ exact sample
6. มี source of truth สำหรับกรณีที่คำตอบผิดไม่ได้

ถ้าทำครบ การประมาณไม่ใช่การเดา แต่เป็นการแลกทรัพยากรกับความคลาดเคลื่อนอย่างมีขอบเขตและตรวจสอบได้

---

## Deep Dives

- [[Bloom Filter]] — Approximate membership: “มีไหม?”
- [[HyperLogLog]] — Cardinality estimation: “มีกี่ค่าที่ไม่ซ้ำ?”
- [[Count-Min Sketch]] — Point frequency: “ค่านี้เกิดกี่ครั้ง?”
- [[MinHash]] — Jaccard similarity: “สองชุดคล้ายกันแค่ไหน?”
- [[Space-Saving Algorithm]] — Heavy hitters: “ค่าไหนเกิดบ่อย?”
- [[DDSketch]] — Quantile estimation: “p95/p99 เท่าไร?”

## แหล่งอ้างอิง

- [Redis: Probabilistic data structures](https://redis.io/docs/latest/develop/data-types/probabilistic/)
- [Redis: Bloom filter](https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/)
- [Redis: HyperLogLog](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/)
- [Redis: Count-Min Sketch](https://redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/)
- [Redis: Top-K / HeavyKeeper](https://redis.io/docs/latest/develop/data-types/probabilistic/top-k/)
- [RocksDB: Bloom Filter](https://github.com/facebook/rocksdb/wiki/RocksDB-Bloom-Filter)
- [BigQuery: Approximate aggregate functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions)
- [Datadog: Computing accurate percentiles with DDSketch](https://www.datadoghq.com/blog/engineering/computing-accurate-percentiles-with-ddsketch/)
- [DataDog sketches-py](https://github.com/DataDog/sketches-py)
- [Apache DataSketches](https://datasketches.apache.org/docs/)
