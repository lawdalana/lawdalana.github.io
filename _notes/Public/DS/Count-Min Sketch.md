---
title: Count-Min Sketch
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, count-min-sketch, frequency, streaming, probabilistic, heavy-hitters, redis]
status: published
---

# Count-Min Sketch: นับ Frequency ทุก Item ใน Stream ด้วย Memory นิดเดียว

> **"Stream มี 10 ล้าน distinct items แต่อยากรู้ว่าแต่ละอันปรากฏกี่ครั้ง — โดยไม่เก็บทั้ง 10 ล้านตัว"** — Count-Min Sketch ตอบคำถามนี้ด้วยแค่ 5 KB

Count-Min Sketch (CMS) เป็น frequency estimation structure ที่ **overestimate เท่านั้น** (never undercount) — เหมาะสำหรับ heavy hitter detection, ad impression counting, network monitoring

**Inventors:** Graham Cormode & S. Muthukrishnan (2005)

---

## ปัญหาที่แก้

```
"มี IP address ไหนส่ง traffic เยอะผิดปกติ?" (DDoS detection)
"Hashtag ไหน trend ที่สุดวันนี้?" (Social media)
"Ad campaign นี้ถูกแสดงกี่ครั้ง?" (Ad tech)

HashMap:     เก็บทุก (item, count) → 10M items × 24 bytes = 240 MB
CMS:         ~5 KB สำหรับ 1% error (48,000x smaller!)
```

---

## โครงสร้าง

```
CMS = d × w array of counters (ทั้งหมดเริ่มต้น = 0)
+ d hash functions อิสระต่อกัน

     w=0   w=1   w=2   w=3  ...  w=271
d=0 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₀
d=1 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₁
d=2 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₂
d=3 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₃
d=4 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₄
d=5 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₅
d=6 [  0  ] [  0  ] [  0  ] [  0  ] ... [  0  ]  ← h₆

Parameters:
  d = depth = ⌈ln(1/δ)⌉        → controls failure probability
  w = width = ⌈e/ε⌉           → controls error magnitude
```

---

## Algorithm

### INSERT(item)

```
for i in 0..d:
    CMS[i][hᵢ(item)] += 1
    
O(d) — d hash computations + d counter increments
```

### QUERY(item) → estimated frequency

```
return min(CMS[0][h₀(item)], CMS[1][h₁(item)], ..., CMS[d-1][h_{d-1}(item)])

O(d) — d hash computations + d counter reads
```

**ทำไมใช้ MIN?** — collisions เพิ่มค่า counter → MIN = closest to true value

---

## 🧮 ตัวอย่างการคำนวณแบบละเอียด

```
Setup: d=3, w=5, hash functions h₀, h₁, h₂

Initial state (all zeros):
     w=0  w=1  w=2  w=3  w=4
d=0 [  0 ] [  0 ] [  0 ] [  0 ] [  0 ]
d=1 [  0 ] [  0 ] [  0 ] [  0 ] [  0 ]
d=2 [  0 ] [  0 ] [  0 ] [  0 ] [  0 ]

───────────────────────────────────────────
INSERT "apple" 3 times:

Hash values: h₀("apple")=1, h₁("apple")=3, h₂("apple")=0

After 3 inserts:
     w=0  w=1  w=2  w=3  w=4
d=0 [  0 ] [  3 ] [  0 ] [  0 ] [  0 ]   ← h₀→pos 1
d=1 [  0 ] [  0 ] [  0 ] [  3 ] [  0 ]   ← h₁→pos 3
d=2 [  3 ] [  0 ] [  0 ] [  0 ] [  0 ]   ← h₂→pos 0

───────────────────────────────────────────
INSERT "banana" 2 times:

Hash values: h₀("banana")=3, h₁("banana")=1, h₂("banana")=0

⚠️ COLLISION: h₂("banana")=0 = h₂("apple")=0!
⚠️ COLLISION: h₀("banana")=3 = h₁("apple")=3 (cross-row, ok)

After 2 inserts:
     w=0  w=1  w=2  w=3  w=4
d=0 [  0 ] [  3 ] [  0 ] [  2 ] [  0 ]   ← h₀: apple@1, banana@3
d=1 [  0 ] [  2 ] [  0 ] [  3 ] [  0 ]   ← h₁: apple@3, banana@1
d=2 [  5 ] [  0 ] [  0 ] [  0 ] [  0 ]   ← h₂: apple+banana BOTH @0!

───────────────────────────────────────────
QUERY "apple":
  CMS[0][h₀("apple")] = CMS[0][1] = 3
  CMS[1][h₁("apple")] = CMS[1][3] = 3
  CMS[2][h₂("apple")] = CMS[2][0] = 5  ← overcount! (collision with banana)
  
  estimate = min(3, 3, 5) = 3 ✅ EXACT! (3 inserts of "apple")

QUERY "banana":
  CMS[0][h₀("banana")] = CMS[0][3] = 2
  CMS[1][h₁("banana")] = CMS[1][1] = 2
  CMS[2][h₂("banana")] = CMS[2][0] = 5  ← overcount!
  
  estimate = min(2, 2, 5) = 2 ✅ EXACT! (2 inserts of "banana")

QUERY "cherry" (never inserted):
  CMS[0][h₀("cherry")] = CMS[0][2] = 0
  → min = 0 ✅ CORRECT (no false positives for zero)
```

---

## Error Guarantee

$$f_x \leq \hat{g}(x) \leq f_x + \varepsilon N$$

with probability $\geq 1 - \delta$

| Symbol | ความหมาย |
|--------|----------|
| $f_x$ | true frequency ของ item x |
| $\hat{g}(x)$ | CMS estimate |
| $N$ | total count ของทุก items |
| $\varepsilon$ | error tolerance (determines width $w$) |
| $\delta$ | failure probability (determines depth $d$) |

### 🧮 การเลือก Parameters

```
ต้องการ: ε = 0.001 (0.1% of total), δ = 0.01 (1% failure prob)

Width:  w = ⌈e/ε⌉ = ⌈2.718/0.001⌉ = 2,719
Depth:  d = ⌈ln(1/δ)⌉ = ⌈ln(100)⌉ = ⌈4.605⌉ = 5

Memory: d × w × 4 bytes (32-bit counters)
       = 5 × 2,719 × 4 = 54,380 bytes ≈ 54 KB

Max overcount: ε × N = 0.001 × N
  ถ้า N = 1,000,000 total → overcount ≤ 1,000
```

### Practical Configurations

| Use Case | ε | δ | d | w | Memory | Max Overcount (N=1M) |
|----------|---|---|---|---|--------|---------------------|
| Rough | 0.01 | 0.01 | 5 | 272 | 5.4 KB | ±10,000 |
| Moderate | 0.001 | 0.01 | 5 | 2,719 | 54 KB | ±1,000 |
| High accuracy | 0.0001 | 0.001 | 7 | 27,183 | 760 KB | ±100 |
| Very high | 0.00001 | 0.0001 | 10 | 271,829 | 10.9 MB | ±10 |

---

## Conservative Update (Optimization)

Standard update increments ALL d positions. Conservative update กรองเฉพาะ positions ที่ ≤ current minimum:

```
Standard:
  for i in 0..d: CMS[i][hᵢ(x)] += 1

Conservative:
  estimate = min(CMS[i][hᵢ(x)] for i in 0..d)
  for i in 0..d:
      if CMS[i][hᵢ(x)] == estimate:
          CMS[i][hᵢ(x)] += 1
          
Benefit: ลด overcounting ได้มาก โดยเฉพาะกับ heavy items
```

---

## Heavy Hitter Detection

CMS เหมาะมากสำหรับหา items ที่ปรากฏบ่อยที่สุด (heavy hitters):

```
Threshold θ: หาทุก item ที่ frequency ≥ θ × N

Example: θ = 0.01 → หาทุก item ที่ ≥ 1% of total

Method:
  1. สร้าง candidate set (จาก data stream)
  2. สำหรับทุก candidate: query CMS
  3. ถ้า estimate ≥ θ × N → heavy hitter
  
หรือใช้ Space-Saving Algorithm (ดู [[Space-Saving Algorithm]]) สำหรับ top-K โดยเฉพาะ
```

---

## Merge

```
CMS₁ + CMS₂ = CMS_merged (ต้องใช้ dimensions เดียวกัน)

Method: CMS_merged[i][j] = CMS₁[i][j] + CMS₂[i][j]

Properties:
  ✅ Simple element-wise addition
  ✅ No additional error
  ✅ Associative, commutative
```

---

## Code Examples

### Redis

```bash
# Create sketch
CMS.INITBYPROB mysketch 0.001 0.01   # ε=0.001, δ=0.01

# Increment counts
CMS.INCRBY mysketch apple 5 banana 3 cherry 1

# Query frequency
CMS.QUERY mysketch apple    # → 5 (or slightly more)

# Merge two sketches
CMS.MERGE combined 2 sketch1 sketch2
```

### Python

```python
from datasketches import CountMinSketch

# ε=0.001, δ=0.01 → ~54 KB
cms = CountMinSketch(0.001, 0.01)

for item in stream:
    cms.update(item)

# Query
print(f"apple count: {cms.get_estimate('apple')}")      # estimate (over)
print(f"upper bound: {cms.get_upper_bound('apple')}")    # guaranteed upper
```

### Rust

```rust
use cmsketch::CountMinSketch;

let mut cms = CountMinSketch::new(0.001, 0.01);

for item in &stream {
    cms.insert(item);
}

println!("apple: ~{}", cms.count("apple"));  // always >= true count
```

---

## เปรียบเทียบกับทางเลือกอื่น

| Method | Space | Error | All frequencies | Top-K | Merge |
|--------|-------|-------|----------------|-------|-------|
| HashMap (exact) | O(n) | 0% | ✅ | ✅ | ❌ |
| **Count-Min Sketch** | **O(1/ε × log(1/δ))** | **≤ εN over** | **✅** | **indirect** | **✅** |
| Count Sketch | O(1/ε² × log(1/δ)) | unbiased | ✅ | ✅ | ✅ |
| [[Space-Saving Algorithm]] | O(k) | ≤ n/k | ❌ (top-K only) | ✅ | ❌ |

> **ถ้าต้องการแค่ Top-K → [[Space-Saving Algorithm]] ประหยัดกว่า 100-1000 เท่า**
> **ถ้าต้องการ frequency ของทุก item → CMS คือตัวเลือกเดียวที่ใช้ได้**

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | นับ frequency ของ items ใน stream |
| **Error** | Overestimate only: ≤ $f_x + \varepsilon N$ |
| **Space** | $O(1/\varepsilon \times \log(1/\delta))$ — 5 KB to 20 MB |
| **Speed** | O(d) insert + query |
| **Merge** | ✅ Simple addition |
| **Best optimization** | Conservative update |
| **Where used** | Redis, network monitoring, ad tech, NLP |

---

## References

- Cormode, G. & Muthukrishnan, S. (2005). "An Improved Data Stream Summary: The Count-Min Sketch and Its Applications"
- Redis CMS: [redis.io/commands/cms.incrby](https://redis.io/commands/cms.incrby)
- Apache DataSketches: [datasketches.apache.org](https://datasketches.apache.org/)
- Related: [[Probabilistic Data Structures]], [[Space-Saving Algorithm]], [[Bloom Filter]]
