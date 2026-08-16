---
title: Probabilistic Data Structures
notetype: feed
date: 2026-08-16
last_modified: 2026-08-16
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
| [[Bloom Filter]] | “เคยมี `x` ไหม?” | เช็กสมาชิกด้วย bit array ถ้าตอบว่า **ไม่มี** เชื่อได้ แต่ถ้าตอบว่า **อาจมี** ต้องยอมรับ false positive หรือไปตรวจแหล่งข้อมูลจริงต่อ |
| [[HyperLogLog]] | “มีค่าที่ไม่ซ้ำกี่ค่า?” | ประเมินจำนวน distinct values จากรูปแบบของค่า hash โดยไม่เก็บสมาชิกทั้งหมด เหมาะกับ daily active users หรือ distinct IPs |
| [[Count-Min Sketch]] | “`x` เกิดกี่ครั้ง?” | ใช้ตาราง counter หลายแถวเพื่อประมาณความถี่ของ key ที่ระบุ การชนกันของ hash ทำให้ค่าประมาณแบบมาตรฐานสูงกว่าค่าจริงได้ |
| [[MinHash]] | “ชุด A กับ B คล้ายกันแค่ไหน?” | ย่อแต่ละชุดเป็น signature แล้วใช้สัดส่วนตำแหน่งที่ตรงกันเพื่อประมาณ Jaccard similarity |
| [[Space-Saving Algorithm]] | “ค่าไหนเกิดบ่อยที่สุด?” | เก็บผู้สมัคร heavy hitters จำนวนจำกัด เมื่อเต็มจะถอดรายการที่มี counter ต่ำสุดออก จึงเหมาะกับ Top-K ใน stream |
| [[DDSketch]] | “p50, p95, p99 เท่าไร?” | จัดค่าลง bucket แบบ logarithmic เพื่อประมาณ quantile โดยควบคุมความคลาดเคลื่อนเชิงสัมพัทธ์ของค่าที่ตอบ |

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

Bloom Filter ประกอบด้วย bit array ขนาด `m` และตำแหน่ง hash จำนวน `k` ตำแหน่งต่อ item

### ตอนเพิ่มข้อมูล

1. คำนวณตำแหน่ง `k` ตำแหน่งจาก item
2. ตั้ง bit ทุกตำแหน่งนั้นเป็น `1`

### ตอนค้นหา

- ถ้ามีอย่างน้อยหนึ่งตำแหน่งเป็น `0` → **ไม่มีแน่นอน**
- ถ้าทุกตำแหน่งเป็น `1` → **อาจมี** เพราะ bit เหล่านั้นอาจถูก item อื่นตั้งไว้

ตัวอย่างการใช้งานที่เหมาะ:

- เช็กว่า event ID อาจเคยถูกประมวลผลแล้วหรือยัง ก่อนอ่านฐานข้อมูลหลัก
- เช็กว่า SST file ของ RocksDB อาจมี key ที่ต้องการหรือไม่ เพื่อลด I/O ที่ไม่จำเป็น
- กรอง URL หรือ object ที่ “ไม่น่าจะอยู่ในชุด” ออกอย่างรวดเร็ว

สำหรับจำนวน item ที่คาดไว้ `n` และ false-positive rate เป้าหมาย `p` ขนาดโดยประมาณคือ

$$m = -\frac{n\ln p}{(\ln 2)^2}$$

และจำนวน hash ที่เหมาะสมคือ

$$k \approx \frac{m}{n}\ln 2$$

**ตัวอย่าง:** ต้องรองรับ 1,000,000 รายการที่ `p = 1%`

- ต้องใช้ประมาณ `9.585` bits ต่อรายการ
- bit array มีขนาดประมาณ `1.14 MiB` ก่อนนับ metadata และ overhead ของ implementation
- ค่า `k` ที่เหมาะสมประมาณ `7`

> ถ้าใส่ข้อมูลเกิน capacity ที่ใช้คำนวณไว้ false-positive rate จะสูงขึ้น และ Bloom Filter มาตรฐานไม่รองรับการลบโดยตรง

อ่านต่อ: [[Bloom Filter]]

---

## 2. HyperLogLog — นับจำนวนค่าที่ไม่ซ้ำ

HyperLogLog (HLL) แบ่งค่า hash ออกเป็นสองส่วน:

1. ส่วนแรกเลือก register
2. ส่วนที่เหลือวัดรูปแบบหายาก เช่น จำนวนศูนย์นำหน้า
3. register เก็บค่าสูงสุดที่เคยพบ
4. ตอน query จะรวม register ทั้งหมดเป็นค่าประมาณ cardinality

แนวคิดคือ ถ้าเราเคยเห็นรูปแบบ hash ที่เกิดได้ยากมาก ก็น่าจะมี distinct values ไหลผ่านมามากพอสมควรแล้ว

สำหรับ HLL ดั้งเดิมที่มี `m` registers ค่าคลาดเคลื่อนมาตรฐานโดยคร่าวคือ

$$\text{RSE} \approx \frac{1.04}{\sqrt{m}}$$

ถ้า `m = 16,384` registers จะได้ RSE ประมาณ `0.8125%` แต่รายละเอียดของ memory, sparse encoding และ bias correction ขึ้นอยู่กับ implementation

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

Count-Min Sketch (CMS) เป็นตาราง counter ขนาด `d × w` โดยแต่ละแถวใช้ hash คนละตัว

### Update `x`

เพิ่ม counter หนึ่งตำแหน่งในทุกแถว

### Query `x`

อ่าน counter ที่ตรงกับ `x` ทุกแถว แล้วคืนค่าต่ำสุด

$$\hat f(x) = \min_i \text{counter}[i, h_i(x)]$$

เหตุผลที่เลือกค่าต่ำสุดคือ collision ทำให้ counter เพิ่มขึ้น ไม่ได้ทำให้ลดลง ในโมเดลมาตรฐานที่ update ด้วยจำนวนไม่ติดลบ เราจึงได้

$$f(x) \le \hat f(x) \le f(x) + \varepsilon N$$

ด้วยความน่าจะเป็นอย่างน้อย `1 - δ` โดย `N` คือจำนวน update รวมทั้งหมด

พารามิเตอร์ที่ใช้บ่อยคือ

$$w = \left\lceil \frac{e}{\varepsilon} \right\rceil, \qquad d = \left\lceil \ln\frac{1}{\delta} \right\rceil$$

**ตัวอย่าง:** ต้องการ additive error ไม่เกิน `0.1%` ของจำนวน update รวม และ failure probability `1%`

- `w = 2,719`
- `d = 5`
- ถ้า counter ละ 32 bits ตัว matrix ใช้ประมาณ `53.1 KiB` ก่อน overhead

ข้อควรระวังสำคัญคือ error `εN` คิดจาก **จำนวน update รวม** ไม่ใช่จากจำนวนครั้งของ item นั้น จึงอาจใหญ่เกินไปสำหรับ item ที่เกิดน้อย

> CMS ตอบ `count(x)` ได้เมื่อเรามี `x` อยู่แล้ว แต่ตัว sketch ไม่ได้เก็บรายการ key ให้ enumerate ดังนั้น CMS เพียงตัวเดียวหา Top-K จาก key ที่ไม่รู้จักทั้งหมดไม่ได้ ต้องมี candidate set หรืออัลกอริทึม heavy-hitter อีกชั้นหนึ่ง

อ่านต่อ: [[Count-Min Sketch]]

---

## 4. MinHash — ประมาณความคล้ายของสองชุด

ถ้าใช้ Jaccard similarity แบบ exact:

$$J(A,B) = \frac{|A\cap B|}{|A\cup B|}$$

เราต้องมีสมาชิกของทั้งสองชุดเพื่อหา intersection และ union ส่วน MinHash จะเก็บ signature จำนวน `k` ตำแหน่งแทน แล้วประมาณ similarity จากสัดส่วนตำแหน่งที่ตรงกัน

$$\hat J(A,B) = \frac{\text{จำนวนตำแหน่ง signature ที่ตรงกัน}}{k}$$

**ตัวอย่าง**

```text
A = {search, cart, payment, coupon, delivery}
B = {search, cart, payment, review, delivery}

intersection = 4 รายการ
union        = 6 รายการ
J(A, B)      = 4/6 = 0.667
```

ถ้าใช้ signature `k = 256` ที่ค่า similarity จริงประมาณ `0.667` ส่วนเบี่ยงเบนมาตรฐานของ estimator จะอยู่ราว `0.0295` หรือประมาณ `2.95` percentage points

$$\sigma \approx \sqrt{\frac{J(1-J)}{k}}$$

ก่อนใช้ MinHash ต้องนิยามให้ชัดว่า “หนึ่งสมาชิกของชุด” คืออะไร เช่น

- คำแต่ละคำ
- word shingles ขนาด 3 หรือ 5 คำ
- product IDs ที่ผู้ใช้เคยดู
- DNA k-mers

หาก tokenization ต่างกัน ความหมายของ similarity ก็เปลี่ยน แม้ MinHash configuration จะเหมือนเดิม

อ่านต่อ: [[MinHash]]

---

## 5. Space-Saving — หา heavy hitters ด้วยจำนวนช่องจำกัด

Space-Saving เก็บรายการ `(item, estimated_count, error)` ไว้เพียง `k` ช่อง

เมื่อ item ใหม่เข้ามา:

1. ถ้ามี item อยู่แล้ว → เพิ่ม counter
2. ถ้ายังมีช่องว่าง → เพิ่ม item ด้วย count เท่ากับ 1
3. ถ้าเต็ม → แทน item ที่มี count ต่ำสุดด้วย item ใหม่ และตั้ง count ใหม่เป็น `minimum + 1`

การ “รับช่วง” count ต่ำสุดทำให้ item ใหม่ถูกประเมินสูงกว่าค่าจริงได้ แต่ช่วยให้ heavy hitter ซึ่งเริ่มมาแรงในภายหลังมีโอกาสเข้าสู่รายการ

ตัวอย่าง stream สินค้า:

```text
A, A, B, A, C, B, A, D, B, A, C, A
```

ค่าจริงคือ `A=6, B=3, C=2, D=1` ถ้ามีเพียง 3 ช่อง รายการที่ความถี่ต่ำจะถูกสลับออกระหว่างทาง ขณะที่ A และ B มีแนวโน้มอยู่ต่อเนื่องเพราะ count สูง

สิ่งที่ควรจำ:

- ใช้ memory `O(k)` โดยไม่โตตามจำนวน distinct items
- รับประกัน heavy hitters ตาม threshold ที่สัมพันธ์กับ `N/k` ได้ แต่ **Top-K ใกล้จุดตัดอาจเรียงไม่ตรงแบบ exact**
- count ของ item ที่ถูกแทนเข้ามาอาจเป็น overestimate
- Space-Saving พื้นฐานไม่ควรถูกมองว่า merge ได้ด้วยการบวกตารางแบบตรง ๆ

> Redis `TOPK` ใช้ **HeavyKeeper** ไม่ใช่ Space-Saving ทั้งสองแก้โจทย์ heavy hitters เหมือนกัน แต่กลไกและ error behavior ต่างกัน

อ่านต่อ: [[Space-Saving Algorithm]]

---

## 6. DDSketch — ประมาณ percentile ด้วย relative error

DDSketch ใช้ bucket ที่เว้นระยะแบบ logarithmic แทน bucket ความกว้างคงที่ จึงรักษาสัดส่วนความคลาดเคลื่อนใกล้เคียงกันได้ทั้งค่าขนาดเล็กและขนาดใหญ่

เมื่อกำหนด relative accuracy เป็น `α` ค่า bucket base ที่ใช้ในแนวคิดมาตรฐานคือ

$$\gamma = \frac{1+\alpha}{1-\alpha}$$

แล้ว map ค่าบวก `v` ไปยัง bucket จาก logarithm ของ `v` เมื่อ query quantile ระบบจะเดิน cumulative count จนถึงอันดับที่ต้องการ แล้ว map bucket กลับเป็นค่าประมาณ

เหมาะกับข้อมูลที่กระจายหลาย order of magnitude เช่น

- API latency ตั้งแต่ไม่กี่ millisecond ถึงหลายวินาที
- payload sizes
- transaction values
- queue wait times

ตัวอย่าง latency 20 ค่าเรียงจากน้อยไปมาก:

```text
42, 45, 48, 50, 51, 54, 55, 58, 61, 64,
68, 73, 81, 90, 95, 110, 124, 160, 210, 860 ms
```

ถ้าใช้ nearest-rank แบบ exact จะได้ `p50=64 ms`, `p95=210 ms`, `p99=860 ms` ส่วน DDSketch จะคืนค่าจาก bucket ใกล้ค่าดังกล่าวภายใต้ relative-value error ที่ตั้งไว้

หน่วยความจำของ DDSketch ไม่ใช่ตัวเลขคงที่ เพราะขึ้นกับ

- ค่า `α`
- ช่วงค่าต่ำสุดถึงสูงสุดที่พบ
- รูปแบบการเก็บ bucket
- นโยบาย collapse เมื่อจำกัดจำนวน bins

Datadog ยกตัวอย่าง configuration เฉพาะที่ relative accuracy `2%` สำหรับช่วง `1 ms` ถึง `1 minute` ซึ่งใช้ 275 buckets หรือประมาณ `2 KB` เมื่อ counter ละ 64 bits ตัวเลขนี้เป็นตัวอย่างตามช่วงและ implementation ไม่ใช่ขนาดสากลของ DDSketch

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
| session สองชุดมีพฤติกรรมคล้ายกันไหม? | MinHash | จากชุดตัวอย่างก่อนหน้า Jaccard จริงคือ `0.667`; signature จะให้ค่าประมาณใกล้เคียง |
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
