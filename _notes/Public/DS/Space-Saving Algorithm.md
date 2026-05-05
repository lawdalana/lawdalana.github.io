---
title: Space-Saving Algorithm
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, space-saving, heavy-hitters, top-k, streaming, probabilistic, frequency]
status: published
---

# Space-Saving Algorithm: หา Top-K ด้วยแค่ K Counters

> **"Stream มี 1 ล้าน distinct items แต่เราสนใจแค่ 10 อันดับแรก — ไม่ต้องนับทั้ง 1 ล้านตัว ใช้แค่ 10 counters!"**

Space-Saving Algorithm คือ heavy hitter detection algorithm ที่ **track top-K most frequent items** โดยใช้ memory เพียง O(k) — เล็กกว่า [[Count-Min Sketch]] 100-1000 เท่า เมื่อต้องการแค่ Top-K

**Inventors:** Ahmed Metwally, Divyakant Agrawal, Amr El Abbadi (2003)

---

## ปัญหาที่แก้

```
"Hashtag ไหน trend ที่สุดตอนนี้?" (Twitter/X)
"IP address ไหนส่ง traffic เยอะสุด?" (Network monitoring)
"Product ไหนขายดีสุดวันนี้?" (E-commerce)
"Search query ไหนถูกค้นหาเยอะสุด?" (Google Trends)

HashMap:    เก็บ count ของทุก item → O(n) memory
CMS:        เก็บ sketch → O(d×w) memory
Space-Saving: เก็บแค่ k counters → O(k) memory!
```

---

## Algorithm Step-by-Step

### Data Structure

```
k entries of (item, count), sorted by count ascending

เช่น k = 3:
  [(item=None, count=0), (item=None, count=0), (item=None, count=0)]
```

### INSERT(item)

```
if item มีอยู่แล้วใน counters:
    count[item] += 1
    re-sort if needed
    
else if counters ไม่เต็ม (< k entries):
    add (item, 1)
    
else:  // counters เต็ม และ item ใหม่
    find entry with MINIMUM count → (min_item, min_count)
    replace with (item, min_count + 1)
    // "สืบทอด" count เดิมเป็น guaranteed minimum
    
⚠️ Key insight: การ "inherit" min_count ทำให้ไม่ต้องเริ่มนับใหม่จาก 0
```

---

## 🧮 ตัวอย่างการคำนวณแบบละเอียด

```
k = 3, Stream: A, B, A, C, A, B, A, D, B, C, A

Initial: []

───────────────────────────────────────
Step 1: INSERT A → counters ไม่เต็ม
  → add (A, 1)
  Counters: [(A, 1)]

Step 2: INSERT B → counters ไม่เต็ม
  → add (B, 1)
  Counters: [(A, 1), (B, 1)]

Step 3: INSERT A → มีอยู่
  → count[A] += 1
  Counters: [(B, 1), (A, 2)]

Step 4: INSERT C → counters ไม่เต็ม
  → add (C, 1)
  Counters: [(B, 1), (C, 1), (A, 2)]

Step 5: INSERT A → มีอยู่
  → count[A] += 1
  Counters: [(B, 1), (C, 1), (A, 3)]

Step 6: INSERT B → มีอยู่
  → count[B] += 1
  Counters: [(C, 1), (B, 2), (A, 3)]

Step 7: INSERT A → มีอยู่
  → count[A] += 1
  Counters: [(C, 1), (B, 2), (A, 4)]

Step 8: INSERT D → counters เต็ม! MIN = C(1)
  → replace C(1) with D(1+1=2)
  Counters: [(B, 2), (D, 2), (A, 4)]
  
  ⚠️ D "สืบทอด" count 1 จาก C → overcount!
  True count of D = 1, but reported = 2

Step 9: INSERT B → มีอยู่
  → count[B] += 1
  Counters: [(D, 2), (B, 3), (A, 4)]

Step 10: INSERT C → counters เต็ม! MIN = D(2)
  → replace D(2) with C(2+1=3)
  Counters: [(B, 3), (C, 3), (A, 4)]
  
  ⚠️ C สืบทอด count 2 จาก D
  True count of C = 2, but reported = 3

Step 11: INSERT A → มีอยู่
  → count[A] += 1
  Counters: [(B, 3), (C, 3), (A, 5)]

───────────────────────────────────────
FINAL RESULTS:
  Reported: A=5, B=3, C=3
  True:     A=5, B=3, C=2, D=1

  A: reported=5, true=5 → exact ✅
  B: reported=3, true=3 → exact ✅
  C: reported=3, true=2 → overcount by 1 (≤ n/k = 11/3 ≈ 3.67) ✅
  D: not tracked (true=1, < n/k threshold) ✅
```

---

## Error Guarantee

$$f_x \leq \hat{f}_x \leq f_x + \frac{n}{k}$$

| Symbol | ความหมาย |
|--------|----------|
| $f_x$ | true frequency ของ item x |
| $\hat{f}_x$ | Space-Saving estimate |
| $n$ | total items processed |
| $k$ | number of counters |

### 🧮 การคำนวณ Error Bound

```
ตัวอย่าง: n = 10,000,000 items, k = 100

Max overcount for any item: n/k = 10,000,000/100 = 100,000

ถ้า item มี true count = 500,000:
  Reported: 500,000 ≤ x ≤ 600,000
  Error: ≤ 20% of true count

ถ้า item มี true count = 5,000,000 (50% of total):
  Reported: 5,000,000 ≤ x ≤ 5,100,000
  Error: ≤ 2% of true count

⚠️ Overcount เป็นสัดส่วนของ TOTAL (n/k), ไม่ใช่ของ item
   → Heavy items มี error % ต่ำกว่า light items
```

### เลือก k ยังไง?

```
ถ้าอยากจับทุก item ที่ frequency ≥ θ × n:
  ต้องการ k ≥ 1/θ

ตัวอย่าง:
  "จับทุก item ที่ ≥ 1% of total" → k ≥ 100
  "จับทุก item ที่ ≥ 0.1% of total" → k ≥ 1000
  "Top 10" → k = 10-50 (buffer ไว้บ้าง)
```

---

## Data Structure Implementation

### Stream-Summary (Optimal)

```
Linked list of "buckets" sorted by count, each bucket has a list of items:

Bucket(1) → [C] ───────────────────────┐
    ↓                                   │
Bucket(2) → [B] ─→ [D]                │  ← items with same count
    ↓                                   │  share a bucket
Bucket(3) → [B]                        │
    ↓                                   │
Bucket(5) → [A] ───────────────────────┘

Operations:
  Find min:    O(1) — head of list
  Increment:   O(1) — move item to next bucket
  Insert new:  O(1) — replace min + move to bucket(count+1)
```

### Min-Heap (Simple)

```
Min-heap of (count, item):
  Insert: O(log k)
  Query top-K: O(k log k)
  Simple to implement but slightly slower
```

---

## HeavyKeepers: Space-Saving + Decay

HeavyKeepers (2020) เพิ่ม **exponential decay** ให้ counters:

```
เพิ่ม periodic decay:
  for all counters: count *= λ  (λ < 1, e.g., 0.99)
  remove entries with count < threshold

Benefits:
  ✅ Recent heavy hitters มี priority สูงกว่า
  ✅ Old heavy hitters จางไปเอง
  ✅ เหมาะสำหรับ time-varying distributions

Use cases:
  - Network traffic: "IP ไหนส่งเยอะตอนนี้?" (not last hour)
  - DDoS detection: detect spikes in real-time
  - Trending topics: "hashtag ไหน trend NOW?"
```

---

## Code Examples

### Python

```python
import heapq

class SpaceSaving:
    def __init__(self, k):
        self.k = k
        self.counters = {}  # item → count
        self.heap = []       # min-heap of (count, item)
    
    def insert(self, item):
        if item in self.counters:
            self.counters[item] += 1
            heapq.heappush(self.heap, (self.counters[item], item))
        
        elif len(self.counters) < self.k:
            self.counters[item] = 1
            heapq.heappush(self.heap, (1, item))
        
        else:
            # Find actual minimum (skip stale entries)
            while self.heap:
                min_count, min_item = self.heap[0]
                if (min_item in self.counters and 
                    self.counters[min_item] == min_count):
                    break
                heapq.heappop(self.heap)
            
            min_count, min_item = heapq.heappop(self.heap)
            del self.counters[min_item]
            
            new_count = min_count + 1
            self.counters[item] = new_count
            heapq.heappush(self.heap, (new_count, item))
    
    def top_k(self):
        return sorted(self.counters.items(), key=lambda x: -x[1])

# Usage
ss = SpaceSaving(k=10)
for item in stream:
    ss.insert(item)

for item, count in ss.top_k():
    print(f"{item}: ~{count}")
```

### Redis TOPK

```bash
# Create top-k filter (k=10, width=50, depth=4, decay=0.9)
TOPK.RESERVE trending 10 50 4 0.9

# Add items
TOPK.ADD trending "python" "rust" "python" "go" "rust" "python"
TOPK.ADD trending "python" "go" "rust" "python"

# Get top-K
TOPK.LIST trending
# → 1) "python"  2) "rust"  3) "go"

# Check if item is in top-K
TOPK.QUERY trending "python"   # → 1
TOPK.QUERY trending "java"     # → 0
```

---

## เปรียบเทียบ Heavy Hitter Methods

| Method | Space | Insert | Error | All freqs | Top-K | Merge |
|--------|-------|--------|-------|-----------|-------|-------|
| HashMap | O(n) | O(1) | 0% | ✅ | ✅ | ❌ |
| **Space-Saving** | **O(k)** | **O(log k)** | **≤ n/k** | ❌ | **✅** | **❌** |
| HeavyKeepers | O(k) | O(log k) | ≤ n/k + decay | ❌ | ✅ | ❌ |
| [[Count-Min Sketch]] | O(d×w) | O(d) | ≤ εN | ✅ | indirect | ✅ |
| Misra-Gries | O(k) | O(k) | ≤ n/k | ❌ | ✅ | ❌ |

> **ถ้าต้องการแค่ Top-K → Space-Saving เลือดเย็นที่สุด (O(k) space)**
> **ถ้าต้องการทุก frequency → [[Count-Min Sketch]]**
> **ถ้าต้องการทั้งสองอย่าง → ใช้ทั้งคู่**

---

## Real-World Uses

| System | Algorithm | Purpose |
|--------|-----------|---------|
| **Redis** | Space-Saving (TOPK) | Trending topics, popular items |
| **Network monitoring** | HeavyKeepers | DDoS detection, traffic analysis |
| **E-commerce** | Space-Saving | Best sellers, popular products |
| **Social media** | Space-Saving + Decay | Trending hashtags |
| **CDN** | Space-Saving | Hot content detection |

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | หา Top-K most frequent items ใน stream |
| **Space** | O(k) — เพียง k counters |
| **Error** | Overestimate ≤ n/k |
| **Insert** | O(log k) |
| **Delete** | ❌ (HeavyKeepers = partial via decay) |
| **Merge** | ❌ (unlike CMS) |
| **Best for** | Top-K only, O(k) memory |

---

## References

- Metwally, A., Agrawal, D., El Abbadi, A. (2003). "Efficient Computation of Frequent and Top-k Elements in Data Streams"
- Chen, L. et al. (2020). "HeavyKeepers: An Efficient Algorithm for Heavy-Hitter Detection"
- Redis TOPK: [redis.io/commands/topk.reserve](https://redis.io/commands/topk.reserve)
- Related: [[Probabilistic Data Structures]], [[Count-Min Sketch]]
