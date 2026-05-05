---
title: Probabilistic Data Structures
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, probabilistic, bloom-filter, hyperloglog, count-min-sketch, minhash, ddsketch, streaming, big-data]
status: published
---

# Probabilistic Data Structures: คำตอบขนาด 12 KB สำหรับคำถามพันล้าน

> **"ถ้าคุณมี RAM 16 GB และต้องนับ unique users พันล้านคน คุณจะทำยังไง?"** — คำตอบคือไม่ต้องเก็บทั้งหมด แต่ใช้ Probabilistic Data Structures ที่แลก accuracy บางส่วนเพื่อ **space savings ถึง 1,000,000 เท่า**

---

## ทำไมต้องรู้?

Traditional data structures (HashMap, TreeSet, SortedList) ให้คำตอบ **แม่น 100%** แต่กิน memory มหาศาลเมื่อข้อมูลเยอะ:

```
"มี unique visitors กี่คนวันนี้?"
  HashSet:        เก็บทุก IP → 1 billion IPs × 16 bytes = 16 GB
  HyperLogLog:    ~0.8% error → 12 KB  (เล็กกว่า 1,333,333 เท่า!)
  
"item นี้ปรากฏกี่ครั้งใน stream?"
  HashMap:        เก็บทุก (key, count) → 10M items × 24 bytes = 240 MB
  Count-Min Sketch: 1% error → 5 KB (เล็กกว่า 50,000 เท่า!)
```

Real-world systems ทุกวันนี้ใช้ probabilistic structures: **Google, Meta, Redis, BigQuery, Spark, Datadog, Elasticsearch**

---

## 6 ตระกูลหลัก

```
┌──────────────────────────────────────────────────────────┐
│          PROBABILISTIC DATA STRUCTURES                    │
├──────────────┬───────────────────────────────────────────┤
│ คำถาม        │ Structure                                │
├──────────────┼───────────────────────────────────────────┤
│ "มีไหม?"     │ [[Bloom Filter]], Cuckoo, Xor, Ribbon    │
│ "กี่ตัว?"     │ [[HyperLogLog]], Linear Counting         │
│ "กี่ครั้ง?"   │ [[Count-Min Sketch]], Count Sketch       │
│ "คล้ายไหม?"  │ [[MinHash]], SimHash, TLSH               │
│ "เยอะสุด?"   │ [[Space-Saving Algorithm]], HeavyKeepers │
│ "percentile?"│ [[DDSketch]], t-Digest                    │
└──────────────┴───────────────────────────────────────────┘
```

---

## หลักการร่วม

ทุก structure มีกลไกเดียวกัน: **ใช้ hash function เพื่อ map ข้อมูลลงพื้นที่จำกัด**

```
Exact Data Structure:
  Input → Store everything → Query → Exact answer (100%)
  
Probabilistic Data Structure:
  Input → Hash → Compact representation → Query → Approximate answer (95-99.9%)
  
สิ่งที่แลก:
  ✅ Space:    12 KB แทน 16 GB
  ✅ Speed:    O(1) แทน O(n)
  ✅ Mergeable: รวมจากหลายเครื่องได้
  ❌ Accuracy:  ~0.5-5% error (tunable)
```

---

## เปรียบเทียบทั้ง 6 ตระกูล

| Structure | คำถาม | Space | Error | Merge | Speed | ใช้ที่ไหน |
|-----------|--------|-------|-------|-------|-------|----------|
| [[Bloom Filter]] | มีไหม? | ~10 bits/elem | 1% FPR | ❌ | O(k) | RocksDB, Chrome, CDN |
| [[HyperLogLog]] | กี่ตัว? | 12-16 KB | 0.8% | ✅ | O(1) | Redis, BigQuery, Spark |
| [[Count-Min Sketch]] | กี่ครั้ง? | 5 KB - 20 MB | ≤ εN over | ✅ | O(d) | Redis, network monitoring |
| [[MinHash]] | คล้ายไหม? | 2-8 KB/set | 3-6% | ✅ | O(k) | Recommendation, DNA |
| [[Space-Saving Algorithm]] | เยอะสุด? | O(k) | ≤ n/k over | ❌ | O(log k) | Redis TOPK, trending |
| [[DDSketch]] | percentile? | 5-50 KB | 0.1-1% rel. | ✅ | O(1) | Datadog, Elasticsearch |

---

## เลือกอะไรเมื่อไหร่?

```
"Is X in the set?"
  → [[Bloom Filter]] (simplest) / Binary Fuse (fastest) / Ribbon (smallest)

"How many unique items?"
  → [[HyperLogLog]] (12 KB, <1% error, mergeable)

"How many times did X appear?"
  → [[Count-Min Sketch]] (overestimate only, small)

"Are these two sets similar?"
  → [[MinHash]] (Jaccard similarity)
  → SimHash (cosine similarity, faster compare)

"What are the most frequent items?"
  → [[Space-Saving Algorithm]] (O(k) space, top-K only)

"What is the p99 latency?"
  → [[DDSketch]] (relative error guarantee) / t-Digest (tail accuracy)

"ทุกอย่างพร้อมกัน?"
  → Redis (มี built-in: Bloom, Cuckoo, HLL, CMS, Top-K)
  → Apache DataSketches (Java library จาก Yahoo)
```

---

## Systems ที่ใช้จริง

| System | Structures | Purpose |
|--------|-----------|---------|
| **Redis** | Bloom, Cuckoo, CMS, Top-K, HLL | `BF.ADD`, `PFADD`, `CMS.INCRBY`, `TOPK.ADD` |
| **RocksDB** | Ribbon / Bloom | SSTable key lookup optimization |
| **BigQuery** | HLL | `APPROX_COUNT_DISTINCT` |
| **Spark** | HLL | `approx_count_distinct()` |
| **Datadog** | DDSketch | Real-time percentile monitoring |
| **Elasticsearch** | t-Digest, HLL | Percentile aggregation, unique count |
| **Google** | SimHash | Web page deduplication |
| **Chrome** | Bloom Filter | Malicious URL checking (local) |
| **Twitter/X** | HLL, MinHash | Unique users, similar audiences |

---

## Key Resources

- **Apache DataSketches:** [datasketches.apache.org](https://datasketches.apache.org/)
- **Redis Probabilistic:** [redis.io/docs/data-types/probabilistic](https://redis.io/docs/data-types/probabilistic/)
- **Book:** "Probabilistic Data Structures and Algorithms for Big Data" — Andrii Gakhov
- **Key Papers:**
  - Bloom (1970), Flajolet et al. HLL (2007), Cormode & Muthukrishnan CMS (2005)
  - Broder MinHash (1997), Masson et al. DDSketch (2019), Metwally Space-Saving (2003)

---

## Deep Dives (แต่ละตัว)

- [[Bloom Filter]] — "มีไหม?" Membership testing
- [[HyperLogLog]] — "กี่ตัว?" Cardinality estimation
- [[Count-Min Sketch]] — "กี่ครั้ง?" Frequency estimation
- [[MinHash]] — "คล้ายไหม?" Similarity estimation
- [[Space-Saving Algorithm]] — "เยอะสุด?" Top-K heavy hitters
- [[DDSketch]] — "percentile?" Quantile estimation
