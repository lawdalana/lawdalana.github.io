---
title: Bloom Filter
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, bloom-filter, probabilistic, membership, hash, AMQ, streaming]
status: published
---

# Bloom Filter: กระเป๋าเล็กๆ ที่จำว่าอะไรเคยผ่านมา

> **"ใช้ memory แค่ 9.6 bits ต่อ item ในการบอกว่า 'เคยเห็นของชิ้นนี้ไหม?' — ตอบ 'ไม่เคย' ได้ถูก 100% แต่ตอบ 'เคย' อาจผิด 1%"**

Bloom Filter เป็น **Approximate Membership Query (AMQ)** structure ที่เก่าแก่และใช้กันแพร่หลายที่สุด — ตีพิมพ์ปี 1970 โดย Burton Howard Bloom แต่ยังเป็น default ใน RocksDB, Cassandra, Chrome จนถึงทุกวันนี้

---

## ปัญหาที่แก้

```
"URL นี้เป็น malicious site ไหม?"
  เก็บทุก URL ใน HashSet: 10M URLs × ~60 bytes = 600 MB
  Bloom Filter: 10M × 9.6 bits = 12 MB (เล็กกว่า 50 เท่า!)
  
"SSTable นี้มี key ที่เราต้องการไหม?" (RocksDB)
  ถ้าไม่มี → ไม่ต้องอ่าน disk → ประหยัด I/O มหาศาล
```

---

## หลักการทำงาน

### โครงสร้าง

```
Bloom Filter = bit array ขนาด m bits + hash functions k ตัว

เริ่มต้น: ทุก bit = 0
  
  bit:  [0][0][0][0][0][0][0][0][0][0][0][0][0][0][0][0]
  index: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
  
Hash functions: h₁, h₂, h₃ (k=3)
```

### Insert: เพิ่ม item เข้าระบบ

```
INSERT("apple"):
  h₁("apple") = 3   → set bit[3] = 1
  h₂("apple") = 7   → set bit[7] = 1
  h₃("apple") = 14  → set bit[14] = 1
  
  bit:  [0][0][0][1][0][0][0][1][0][0][0][0][0][0][1][0]
                ↑           ↑                    ↑

INSERT("banana"):
  h₁("banana") = 7   → set bit[7] = 1 (เป็น 1 อยู่แล้ว)
  h₂("banana") = 11  → set bit[11] = 1
  h₃("banana") = 3   → set bit[3] = 1 (เป็น 1 อยู่แล้ว)
  
  bit:  [0][0][0][1][0][0][0][1][0][0][0][1][0][0][1][0]
```

### Query: เช็คว่ามีไหม

```
QUERY("apple"):
  h₁("apple") = 3   → bit[3] = 1 ✅
  h₂("apple") = 7   → bit[7] = 1 ✅
  h₃("apple") = 14  → bit[14] = 1 ✅
  → ทุก bit เป็น 1 → "อาจจะมี" (Probably Yes) ✅

QUERY("cherry"):
  h₁("cherry") = 2   → bit[2] = 0 ❌
  → มี bit ที่เป็น 0 → "แน่นอนว่าไม่มี" (Definitely No) ✅

QUERY("durian"):  ← FALSE POSITIVE!
  h₁("durian") = 3   → bit[3] = 1 ✅ (ถูก "apple" set ไว้)
  h₂("durian") = 7   → bit[7] = 1 ✅ (ถูก "apple"/"banana" set ไว้)
  h₃("durian") = 11  → bit[11] = 1 ✅ (ถูก "banana" set ไว้)
  → ทุก bit เป็น 1 → "อาจจะมี" แต่จริงๆ ไม่เคย insert!
  → False Positive! (ประมาณ 1% ถ้า config ดี)
```

---

## สมการคำนวณ False Positive Rate

$$FPR \approx \left(1 - e^{-kn/m}\right)^k$$

| Symbol | ความหมาย |
|--------|----------|
| $m$ | จำนวน bits |
| $n$ | จำนวน items ที่ insert |
| $k$ | จำนวน hash functions |

### การหาค่า k ที่เหมาะสม

เพื่อให้ FPR ต่ำสุด ค่า $k$ ที่เหมาะสมคือ:

$$k_{optimal} = \frac{m}{n} \ln 2 \approx 0.693 \times \frac{m}{n}$$

### 🧮 ตัวอย่างการคำนวณ

**ต้องการ:** เก็บ 10 ล้าน URLs, FPR ≤ 1%

**Step 1: คำนวณจำนวน bits ที่ต้องการ**

$$m = -\frac{n \ln(p)}{(\ln 2)^2}$$

$$m = -\frac{10{,}000{,}000 \times \ln(0.01)}{(0.693)^2} = \frac{10{,}000{,}000 \times 4.605}{0.480} \approx 95{,}940{,}000 \text{ bits}$$

$$\approx 11.4 \text{ MB}$$

**Step 2: หา k ที่เหมาะสม**

$$k = \frac{m}{n} \ln 2 = \frac{95{,}940{,}000}{10{,}000{,}000} \times 0.693 \approx 6.64 \approx 7 \text{ hash functions}$$

**Step 3: Verify FPR**

$$FPR = \left(1 - e^{-7 \times 10{,}000{,}000 / 95{,}940{,}000}\right)^7 = (1 - e^{-0.729})^7$$

$$= (1 - 0.482)^7 = (0.518)^7 \approx 0.0083 = 0.83\%$$

**สรุป:** 10M items, 1% FPR → **11.4 MB, 7 hash functions** ✅

---

## Space vs Accuracy Table

| Items (n) | FPR (p) | Bits/Item | Total Space | Hash Functions (k) |
|-----------|---------|-----------|-------------|-------------------|
| 1M | 10% | 4.8 | 600 KB | 3 |
| 1M | 1% | 9.6 | 1.2 MB | 7 |
| 1M | 0.1% | 14.4 | 1.8 MB | 10 |
| 1M | 0.01% | 19.2 | 2.4 MB | 14 |
| 10M | 1% | 9.6 | 12 MB | 7 |
| 100M | 1% | 9.6 | 120 MB | 7 |
| 1B | 1% | 9.6 | 1.2 GB | 7 |

> **Key insight:** bits/item ขึ้นอยู่กับ FPR ที่ต้องการ ไม่ขึ้นกับจำนวน items — 1M items ใช้ 9.6 bits/item เท่ากับ 1B items

---

## ข้อจำกัด

### ❌ ลบไม่ได้

```
Insert: "apple" → set bits {3, 7, 14}
Insert: "banana" → set bits {3, 7, 11}  (overlap!)

ถ้าลบ "apple" โดย clear bits {3, 7, 14}:
  → bit[3] ถูก "banana" ใช้ด้วย → "banana" จะหาย!
  → bit[7] ถูก "banana" ใช้ด้วย → "banana" จะหาย!
  
วิธีแก้: ใช้ Counting Bloom Filter (แต่ละ bit เป็น counter 4 bits แทน)
```

### ❌ นับไม่ได้

Bloom Filter บอกแค่ "มี/ไม่มี" — ไม่รู้ว่ามากี่ครั้ง ถ้าต้องนับ → ใช้ [[Count-Min Sketch]]

### ❌ ดึงข้อมูลกลับไม่ได้

ไม่สามารถ list ทุก item ที่ insert แล้วได้ — รู้แค่ query ทีละตัว

---

## การเลือก Hash Function

```
คุณภาพ hash → ผลกระทบโดยตรงต่อ FPR

✅ ดี:
  MurmurHash3 — เร็ว, distribution ดี (default ในส่วนใหญ่)
  xxHash — เร็วมาก, SIMD-friendly
  SipHash — cryptographically strong, ป้องกัน hash flooding

❌ หลีกเลี่ยง:
  CRC32 — distribution ไม่ดีพอ
  MD5/SHA — ช้าเกินไป (overkill)
  
Trick: ใช้ hash 2 ตัวสร้าง k ตัว:
  hᵢ(x) = h₁(x) + i × h₂(x)  (Kirsch-Mitzenmacher trick)
```

---

## Variants

| Variant | ข้อจำกัดที่แก้ | วิธี | Space |
|---------|---------------|------|-------|
| **Counting Bloom Filter** | ลบได้ | counter 4 bits แทน 1 bit | 4-5x |
| **Blocked Bloom Filter** | Cache-friendly | แบ่งเป็น blocks 64-512 bits | ~10% more |
| **Scalable Bloom Filter** | เติบโตได้ | เพิ่ม filter ใหม่เมื่อเต็ม | grows |
| **Stable Bloom Filter** | ลบข้อมูลเก่าได้ | random decay counters | fixed |

### Counting Bloom Filter: ลบได้!

```
แทน bit array → ใช้ counter array (4 bits each)

Insert "apple":  counter[3]++, counter[7]++, counter[14]++
Insert "banana": counter[3]++, counter[7]++, counter[11]++

Delete "apple":  counter[3]--, counter[7]--, counter[14]--
  → "banana" ยังเหลือ counter[3]=1, counter[7]=1 ✅

Trade-off: 4x more memory (4 bits per counter vs 1 bit)
Risk: counter overflow (4 bits max = 15)
```

---

## Code Examples

### Python

```python
import mmh3  # MurmurHash3
import math

class BloomFilter:
    def __init__(self, expected_items, fpr):
        self.m = self._optimal_m(expected_items, fpr)
        self.k = self._optimal_k(self.m, expected_items)
        self.bit_array = bytearray(math.ceil(self.m / 8))
    
    def _optimal_m(self, n, p):
        """คำนวณจำนวน bits ที่เหมาะสม"""
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    def _optimal_k(self, m, n):
        """คำนวณจำนวน hash functions ที่เหมาะสม"""
        return int(m / n * math.log(2))
    
    def _hashes(self, item):
        """สร้าง k hash values ด้วย double hashing"""
        h1 = mmh3.hash(str(item), 0) % self.m
        h2 = mmh3.hash(str(item), 42) % self.m
        for i in range(self.k):
            yield (h1 + i * h2) % self.m
    
    def add(self, item):
        for pos in self._hashes(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)
    
    def contains(self, item):
        for pos in self._hashes(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                return False  # แน่นอนว่าไม่มี
        return True  # อาจจะมี

# Usage
bf = BloomFilter(expected_items=10_000_000, fpr=0.01)
bf.add("https://malicious-site.com")
print(bf.contains("https://malicious-site.com"))  # True
print(bf.contains("https://safe-site.com"))        # False (definitely)
```

### Rust

```rust
use fastbloom::BloomFilter;

let mut filter = BloomFilter::with_size(10_000_000)
    .expected_false_positives(0.01);

filter.insert("malicious-url-1");
filter.insert("malicious-url-2");

assert!(filter.contains("malicious-url-1"));  // probably true
assert!(!filter.contains("safe-url"));         // definitely false (if true, it's FP)
```

---

## Real-World Applications

### Chrome Safe Browsing

```
Problem: เช็ค URL ว่าเป็น malicious ไหม โดยไม่ส่งทุก URL ไป server

Solution:
  1. Google สร้าง Bloom Filter ของ malicious URLs (~12 MB)
  2. Chrome download filter มาเก็บไว้ local
  3. เวลา user เข้าเว็บ → check local Bloom Filter ก่อน
  4. ถ้า "ไม่มี" → safe, ไม่ต้องยิง server
  5. ถ้า "อาจจะมี" → ยิง server verify (ส่วนใหญ่เป็น FP)
  
Result: 99% of checks ไม่ต้องยิง server
```

### RocksDB / Cassandra (SSTable Lookup)

```
Problem: มี 100+ SSTable files, จะรู้ได้ยังไงว่า key อยู่ไฟล์ไหน?

Solution:
  1. แต่ละ SSTable มี Bloom Filter ของ keys ในนั้น
  2. Read request → check Bloom Filters ทุกไฟล์
  3. "ไม่มี" → skip ไฟล์นั้น (save disk I/O)
  4. "อาจจะมี" → อ่านจริง
  
Result: ลด disk I/O 90%+ ใน read-heavy workloads
```

---

## เปรียบเทียบกับ AMQ Filter อื่น

| Filter | Space (1% FPR) | Delete | Build | Lookup | Cache-friendly |
|--------|---------------|--------|-------|--------|---------------|
| **Bloom** | 9.6 bits/elem | ❌ | O(n) | O(k) | ❌ |
| Blocked Bloom | 10.6 bits/elem | ❌ | O(n) | O(k) | ✅ |
| Cuckoo Filter | 8-10 bits/elem | ✅ | O(n) | O(1) | ✅ |
| Binary Fuse | 7.5 bits/elem | ❌ | O(n) | O(1) | ✅ |
| Ribbon Filter | 7.0 bits/elem | ❌ | O(n) | O(1) | ✅ |

> Bloom Filter = ง่ายที่สุด, เข้าใจง่ายที่สุด, debug ง่ายที่สุด — แต่ไม่ใช่เลือดเย็น/เร็วที่สุด

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | ทดสอบว่า "item เคยเห็นมาก่อนไหม?" |
| **Space** | ~9.6 bits/item (FPR 1%) |
| **Speed** | O(k) insert + query |
| **False Negative** | ❌ ไม่มี (100% recall) |
| **False Positive** | ⚠️ ~1% (tunable) |
| **Delete** | ❌ (ใช้ Counting BF แทน) |
| **Where used** | RocksDB, Cassandra, Chrome, CDNs |

---

## References

- Bloom, B.H. (1970). "Space/Time Trade-offs in Hash Coding with Allowable Errors"
- Kirsch, A. & Mitzenmacher, M. (2006). "Less Hashing, Same Performance: Hashing with Two Functions"
- Wikipedia: [Bloom Filter](https://en.wikipedia.org/wiki/Bloom_filter)
- Related: [[Probabilistic Data Structures]], [[Count-Min Sketch]], [[HyperLogLog]]
