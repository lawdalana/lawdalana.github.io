---
title: HyperLogLog
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, hyperloglog, cardinality, counting, streaming, probabilistic, redis]
status: published
---

# HyperLogLog: นับพันล้าน Unique ด้วย 12 KB

> **"ใช้ memory แค่ 12 KB เพื่อนับ unique items พันล้านตัว โดย error แค่ 0.8%"** — นี่คือ data structure ที่อยู่เบื้องหลัง `APPROX_COUNT_DISTINCT` ใน BigQuery, Spark, Redis

HyperLogLog (HLL) เป็น cardinality estimation algorithm ที่ตอบคำถาม *"มี unique items กี่ตัว?"* — เหมาะสำหรับ use cases เช่น "วันนี้มี unique visitors กี่คน?", "มี distinct IPs กี่อันใน log?"

**History:** Probabilistic Counting (1985) → LogLog (2004) → **HyperLogLog** (2007) → **HLL++** (Google, 2013)

---

## หลักการ: หา Leftmost 1-bit

ถ้า hash output มี leading zeros มาก → เราเห็น "rare" value → มี unique items เยอะ

```
Intuition: โยนเหรียญ
  ได้ "หัว" 1 ครั้งติด = common (prob 1/2)
  ได้ "หัว" 7 ครั้งติด = rare (prob 1/128)
  
  ถ้าเคยเห็น "หัว 7 ครั้งติด" → โยนมาประมาณ 128 ครั้งแล้ว
  
  Hash = "โยนเหรียญ" แบบ deterministic
  Leading zeros = จำนวน "หัว" ติดต่อกัน
```

---

## Algorithm Step-by-Step

### ขั้นตอนที่ 1: เตรียม Registers

```
m = 2^p registers (p = precision parameter)
ทุก register เริ่มต้น = 0

ตัวอย่าง p = 4 → m = 16 registers:
  M = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

### ขั้นตอนที่ 2: Insert แต่ละ element

```
สำหรับทุก element x ใน stream:

1. hash = H(x)                    → เช่น 64-bit MurmurHash3
2. j = first p bits of hash        → register index (0..m-1)
3. w = remaining bits              → (64-p) bits
4. ρ(w) = position of leftmost 1   → 1-indexed
5. M[j] = max(M[j], ρ(w))         → เก็บค่าสูงสุด
```

**ตัวอย่าง:**

```
INSERT("user_12345"):
  hash = 0b 0001 01101001... (64 bits)
  
  p = 4:
  j = 0001 = register index 1
  w = 01101001...
  ρ(w) = position of leftmost 1 = 2 (bit ที่ 2 นับจากซ้าย)
  
  M[1] = max(M[1], 2) = max(0, 2) = 2

INSERT("user_67890"):
  hash = 0b 0001 00000111...
  
  j = 0001 = register index 1 (register เดียวกัน!)
  w = 00000111...
  ρ(w) = 6 (leading zeros 5 ตัว → bit ที่ 6)
  
  M[1] = max(M[1], 6) = max(2, 6) = 6  ← update เป็นค่าที่สูงกว่า

หลังจาก insert หลายพันตัว:
  M = [3, 6, 2, 8, 1, 5, 7, 4, 3, 9, 2, 5, 6, 4, 3, 7]
```

### ขั้นตอนที่ 3: Query — คำนวณ Cardinality

$$Z = \left(\sum_{j=1}^{m} 2^{-M[j]}\right)^{-1}$$

$$E = \alpha_m \times m^2 \times Z$$

$$\alpha_m = \frac{0.7213}{1 + \frac{1.079}{m}}$$

### 🧮 ตัวอย่างการคำนวณ

```
p = 4, m = 16 registers
M = [3, 6, 2, 8, 1, 5, 7, 4, 3, 9, 2, 5, 6, 4, 3, 7]

Step 1: คำนวณ Z
  Z = (2^(-3) + 2^(-6) + 2^(-2) + 2^(-8) + 2^(-1) + 2^(-5) + 
       2^(-7) + 2^(-4) + 2^(-3) + 2^(-9) + 2^(-2) + 2^(-5) + 
       2^(-6) + 2^(-4) + 2^(-3) + 2^(-7))^(-1)
  
  = (0.125 + 0.016 + 0.250 + 0.004 + 0.500 + 0.031 + 
     0.008 + 0.063 + 0.125 + 0.002 + 0.250 + 0.031 + 
     0.016 + 0.063 + 0.125 + 0.008)^(-1)
  
  = (1.617)^(-1) = 0.618

Step 2: คำนวณ α_m
  α₁₆ = 0.7213 / (1 + 1.079/16) = 0.7213 / 1.0674 = 0.676

Step 3: คำนวณ E
  E = 0.676 × 16² × 0.618
  E = 0.676 × 256 × 0.618
  E ≈ 106.9
  
  → Estimated unique count ≈ 107
```

---

## HyperLogLog++ (Google's Improvement)

Google ปรับปรุง HLL ใน paper "HyperLogLog in Practice" (Heule et al., 2013) — version นี้ใช้ใน Redis, BigQuery, Spark

### สิ่งที่ปรับปรุง

| Feature | HLL (Original) | HLL++ (Google) |
|---------|---------------|----------------|
| Hash size | 32-bit | **64-bit** |
| Small set optimization | ❌ | ✅ **Sparse encoding** |
| Bias correction | Simple threshold | **Empirical lookup table** |
| Register width | 5 bits | **6 bits** (supports $2^{64}$ cardinality) |

### Sparse vs Dense Representation

```
Cardinality < ~25,000:
  → Sparse mode: เก็บแค่ (register_index, value) ที่ไม่ใช่ 0
  → 100 unique items → ~300 bytes (40x smaller than dense!)

Cardinality > ~25,000:
  → Dense mode: full register array = 2^p × 6 bits
  → p=14: 16,384 × 6 bits = 12,288 bytes

Auto-switch: เมื่อ sparse ใหญ่กว่า dense → convert อัตโนมัติ
```

---

## Space vs Accuracy

| Precision (p) | Registers (m) | Memory (dense) | Std Error |
|---------------|--------------|----------------|-----------|
| 10 | 1,024 | 768 B | 3.25% |
| 12 | 4,096 | 3 KB | 1.63% |
| **14** | **16,384** | **12 KB** | **0.81%** |
| 16 | 65,536 | 49 KB | 0.41% |
| 18 | 262,144 | 196 KB | 0.20% |

$$\text{Std Error} = \frac{1.04}{\sqrt{m}}$$

> **Key insight:** เพิ่ม precision 1 → memory x2, error / √2

---

## Merge Operation (Union)

HLL สามารถ merge ข้าม machines ได้ — **lossless**:

```
Server A counts users 9am-12pm → HLL_A
Server B counts users 12pm-3pm → HLL_B

Merged: M_merged[j] = max(HLL_A[j], HLL_B[j])  for all j

Properties:
  ✅ Lossless (no additional error)
  ✅ Associative: (A ∪ B) ∪ C = A ∪ (B ∪ C)
  ✅ Commutative: A ∪ B = B ∪ A
  ✅ Can merge at any time

Total unique users 9am-3pm = query(merge(HLL_A, HLL_B))
```

---

## Code Examples

### Redis

```bash
# Add elements
PFADD visitors:2024-05-05 "user1" "user2" "user3"
PFADD visitors:2024-05-05 "user2" "user4"  # duplicate user2 ignored

# Count unique
PFCOUNT visitors:2024-05-05  # → 4

# Merge across days
PFMERGE visitors:week visitors:05-04 visitors:05-05
PFCOUNT visitors:week  # → unique across both days

# Memory: ~12 KB per key, regardless of cardinality!
```

### Python

```python
from hyperloglog import HyperLogLog

# 1% error rate → ~12 KB
hll = HyperLogLog(0.01)

for user_id in user_stream:
    hll.add(user_id)

print(f"Unique users: {len(hll)}")  # approximate count

# Merge
hll_merged = HyperLogLog(0.01)
hll_merged.merge(hll_server_a)
hll_merged.merge(hll_server_b)
```

### BigQuery

```sql
-- Uses HLL++ internally
SELECT 
  APPROX_COUNT_DISTINCT(user_id) as unique_users
FROM events
WHERE date = '2024-05-05';
```

---

## เปรียบเทียบกับวิธีอื่น

| Method | Space | Error | Merge | Max Cardinality |
|--------|-------|-------|-------|----------------|
| HashSet (exact) | O(n) | 0% | ✅ | unlimited |
| Linear Counting | O(m) bits | depends | ✅ | ≤ m |
| **HyperLogLog** | **O(m)** | **0.81%** | **✅** | **$2^{64}$** |
| HLL++ | O(m) | 0.81% | ✅ | $2^{64}$ |

---

## When to Use

```
✅ ใช้ HLL เมื่อ:
  - ต้องนับ unique items ใน massive stream
  - Memory จำกัด (12 KB vs 16 GB)
  - ต้อง merge ข้าม machines
  - ~1% error ยอมรับได้

❌ ไม่ใช้ HLL เมื่อ:
  - ต้องการ exact count → HashSet
  - ต้องการ intersection → [[MinHash]] (better)
  - ข้อมูลน้อย (< 1000) → Linear Counting
```

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | นับจำนวน unique items ใน stream |
| **Space** | 12 KB (p=14) สำหรับ billions of items |
| **Error** | ~0.81% (p=14), tunable |
| **Insert** | O(1) |
| **Merge** | ✅ Lossless union |
| **Delete** | ❌ |
| **Best version** | HLL++ (Google) with sparse encoding |

---

## References

- Flajolet, P. et al. (2007). "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm"
- Heule, S. et al. (2013). "HyperLogLog in Practice: Algorithmic Engineering of a State of The Art Cardinality Estimation Algorithm" (Google)
- Redis HLL: [redis.io/commands/pfadd](https://redis.io/commands/pfadd)
- Related: [[Probabilistic Data Structures]], [[Count-Min Sketch]], [[MinHash]]
