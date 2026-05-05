---
title: DDSketch
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, ddsketch, quantile, percentile, monitoring, latency, streaming, probabilistic, datadog]
status: published
---

# DDSketch: วัด p99 Latency แบบ Real-time ด้วย 5 KB

> **"API ของเรามี p99 latency เท่าไหร่? ต้องตอบได้ทันที โดยไม่เก็บ log ทุก request"** — DDSketch ตอบคำถามนี้ด้วย memory แค่ 5 KB โดยมี relative error ≤ 1%

DDSketch เป็น **quantile estimation** algorithm สำหรับหา percentile (p50, p90, p95, p99, p99.9) จาก data stream — คำนวณ latency, response time, และ distribution metrics แบบ real-time

**Inventors:** Charles Masson, Jee E. Rim, Homin K. Lee (Datadog, 2019)

---

## ปัญหาที่แก้

```
"p99 latency ของ API คือเท่าไหร่?"

Naive: เก็บทุก value → sort → pick percentile
  1M requests/sec × 8 bytes = 8 MB/sec = 691 GB/day ❌

ต้องการ:
  ✅ Fixed small memory (5 KB)
  ✅ Query any percentile at any time
  ✅ Merge across machines
  ✅ Handle skewed distributions (latency = long tail)
```

---

## หลักการ: Logarithmic Bucketing

DDSketch map values เป็น buckets โดยใช้ **logarithmic scaling** — แต่ละ bucket ครอบคลุม range เป็นสัดส่วนของ value:

```
Value 100 → bucket ครอบ [99, 101]    (±1%)
Value 1000 → bucket ครอบ [990, 1010]  (±1%)
Value 10000 → bucket ครอบ [9900, 10100] (±1%)

ทุก bucket มี relative error เท่ากัน → ±α%
```

---

## Algorithm Step-by-Step

### Parameter

```
α = relative accuracy (e.g., 0.01 = 1% error)

Guarantee: |estimate - true| / true ≤ α
```

### Step 1: Logarithmic Mapping

$$\text{bucket\_index}(v) = \left\lceil \frac{\ln(v)}{\ln(\gamma)} \right\rceil$$

$$\gamma = 1 + \frac{2\alpha}{1 - \alpha} \approx 1 + 2\alpha$$

```
α = 0.01 → γ ≈ 1.02
α = 0.001 → γ ≈ 1.002
```

### Step 2: สร้าง Histogram

```
Maintain: {bucket_index → count}

INSERT(value):
  if value > 0:
    idx = bucket_index(value)
    positive_histogram[idx] += 1
  elif value < 0:
    idx = bucket_index(-value)
    negative_histogram[idx] += 1
  else:
    zero_count += 1
```

### Step 3: Query Percentile

$$\text{target\_count} = q \times N$$

```
Walk buckets from smallest until cumulative ≥ target_count
Map bucket index back to value: v = γ^idx
```

### 🧮 ตัวอย่างการคำนวณ

```
α = 0.02 (2% error), γ ≈ 1.04

Latencies (ms): [5, 12, 15, 23, 45, 67, 89, 120, 350, 890]

Step 1: Map to buckets
  ln(5)/ln(1.04)   = 1.609/0.0392 = 41.1 → bucket 42
  ln(12)/ln(1.04)  = 2.485/0.0392 = 63.4 → bucket 64
  ln(15)/ln(1.04)  = 2.708/0.0392 = 69.1 → bucket 70
  ln(23)/ln(1.04)  = 3.135/0.0392 = 80.0 → bucket 80
  ln(45)/ln(1.04)  = 3.807/0.0392 = 97.1 → bucket 98
  ln(67)/ln(1.04)  = 4.204/0.0392 = 107.2 → bucket 108
  ln(89)/ln(1.04)  = 4.489/0.0392 = 114.5 → bucket 115
  ln(120)/ln(1.04) = 4.787/0.0392 = 122.1 → bucket 123
  ln(350)/ln(1.04) = 5.858/0.0392 = 149.4 → bucket 150
  ln(890)/ln(1.04) = 6.791/0.0392 = 173.2 → bucket 174

Histogram (simplified):
  42→1, 64→1, 70→1, 80→1, 98→1, 108→1, 115→1, 123→1, 150→1, 174→1

Step 2: Query p50 (5th value out of 10)
  Walk: bucket 42(1) → 64(2) → 70(3) → 80(4) → 98(5) ← target!
  
  p50 estimate = γ^98 = 1.04^98 ≈ 46.8 ms
  True p50 = 45 ms
  Error = |46.8 - 45| / 45 = 4% (slightly above α due to small sample)

Step 3: Query p99 (9.9th value)
  Walk all → 9th value at bucket 150
  
  p99 estimate = γ^150 = 1.04^150 ≈ 367 ms
  True p99 = 350 ms
  Error = |367 - 350| / 350 = 4.9% (again, small sample)
  
  With millions of values → error converges to ≤ α
```

---

## Space vs Accuracy

| α (relative error) | Max buckets | Memory | At p99 |
|---------------------|------------|--------|--------|
| 0.01 (1%) | ~600 | ~5 KB | ±1% |
| 0.005 (0.5%) | ~1,200 | ~10 KB | ±0.5% |
| 0.001 (0.1%) | ~6,000 | ~50 KB | ±0.1% |
| 0.0001 (0.01%) | ~60,000 | ~500 KB | ±0.01% |

$$\text{Buckets} \approx \frac{\ln(\text{max\_value} / \text{min\_value})}{\ln(\gamma)} \approx \frac{\ln(\text{range})}{2\alpha}$$

```
Example (α=0.01, range 0.1ms to 60000ms):
  ~600 buckets × 8 bytes = ~5 KB
  Fixed regardless of how many values ingested!
```

---

## Relative vs Absolute Error

```
Absolute error: |estimate - true| ≤ ε
  p99 of 1000ms: [990, 1010] ✅
  p99 of 10ms:   [0, 20] ❌ useless!

Relative error: |estimate - true| / true ≤ α
  p99 of 1000ms: [990, 1010] ✅
  p99 of 10ms:   [9.9, 10.1] ✅ still accurate!
  
DDSketch = relative error → เหมาะสำหรับ latency ที่ span หลาย orders of magnitude
```

---

## Collapse: Memory Management

```
เมื่อ memory เกิน limit:
  Merge adjacent buckets: count[i] + count[i+1] → count[i]
  Effective α doubles (1% → 2%)

This provides bounded memory with graceful degradation:

  Before collapse: 600 buckets, α=0.01 (1%)
  After 1 collapse: 300 buckets, α=0.02 (2%)  
  After 2 collapses: 150 buckets, α=0.04 (4%)
  
  Memory never exceeds limit, accuracy degrades gracefully
```

---

## Merge

```
DDSketch₁ + DDSketch₂ = merged

Method: merge histograms (add counts for same bucket index)

Properties:
  ✅ Lossless merge (same α)
  ✅ No additional error
  ✅ Associative, commutative

Use case:
  Server 1: DDSketch of latencies → sketch1
  Server 2: DDSketch of latencies → sketch2
  Global p99 = query(merge(sketch1, sketch2))
```

---

## Comparison: DDSketch vs t-Digest

| Feature | DDSketch | t-Digest |
|---------|----------|----------|
| **Error type** | Relative (α) | Scaled (δ) |
| **Error guarantee** | ±α% everywhere | Better at tails |
| **Uniform accuracy** | ✅ Same across all quantiles | ❌ Better at extremes |
| **Merge** | ✅ Lossless (same α) | ⚠️ Slight loss possible |
| **Insert speed** | O(1) | O(log n) |
| **Memory bounded** | ✅ Collapse mechanism | ✅ δ controls centroids |
| **Negative values** | 3 sub-sketches | ✅ Native |
| **Invented by** | Datadog (2019) | Ted Dunning (2019) |
| **Used in** | Datadog monitoring | Elasticsearch, Spark |

```
Use DDSketch when:
  ✅ Need guaranteed relative error across ALL quantiles
  ✅ Latencies spanning orders of magnitude (1ms → 60s)
  ✅ Merging many sketches (lossless)
  ✅ Using Datadog

Use t-Digest when:
  ✅ Care most about tail accuracy (p99.9)
  ✅ Using Elasticsearch / Spark (built-in)
  ✅ Want better accuracy at extreme percentiles
```

---

## Code Examples

### Python

```python
from ddsketch import DDSketch

# 1% relative error → ~5 KB
sketch = DDSketch(0.01)

# Ingest latencies
for latency in latency_stream:
    sketch.insert(latency)  # in seconds

# Query any percentile
print(f"p50:   {sketch.quantile(0.50):.3f}s")
print(f"p90:   {sketch.quantile(0.90):.3f}s")
print(f"p95:   {sketch.quantile(0.95):.3f}s")
print(f"p99:   {sketch.quantile(0.99):.3f}s")
print(f"p99.9: {sketch.quantile(0.999):.3f}s")

# Statistics
print(f"min:   {sketch.min_value}")
print(f"max:   {sketch.max_value}")
print(f"count: {sketch.count}")

# Merge from another server
sketch.merge(sketch_from_server2)
```

### Rust

```rust
use ddsketch::DDSketch;

let mut sketch = DDSketch::new(0.01); // 1% relative error

for value in &latency_stream {
    sketch.insert(*value);
}

println!("p50: {:.3}", sketch.quantile(0.50).unwrap());
println!("p95: {:.3}", sketch.quantile(0.95).unwrap());
println!("p99: {:.3}", sketch.quantile(0.99).unwrap());
```

---

## Real-World Systems

| System | Algorithm | Use Case |
|--------|-----------|----------|
| **Datadog** | DDSketch | APM latency percentiles |
| **Elasticsearch** | t-Digest | `percentiles` aggregation |
| **Apache Spark** | t-Digest | `approx_percentile()` |
| **Kafka Streams** | t-Digest | Real-time percentile queries |
| **OpenTelemetry** | DDSketch | Trace metrics |

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | Streaming quantile estimation with relative error guarantee |
| **Error** | \|est - true\| / true ≤ α (tunable, typically 1%) |
| **Space** | ~5 KB (α=0.01) |
| **Insert** | O(1) |
| **Merge** | ✅ Lossless (same α) |
| **Best for** | Latency monitoring, APM, SLA tracking |

---

## References

- Masson, C., Rim, J., Lee, H. (2019). "DDSketch: A Fast and Fully-Mergeable Quantile Sketch with Near-Optimal Error" (Datadog)
- Dunning, T. & Ertl, O. (2019). "Computing Extremely Accurate Quantiles Using t-Digest"
- Datadog sketches-py: [github.com/DataDog/sketches-py](https://github.com/DataDog/sketches-py)
- Related: [[Probabilistic Data Structures]], [[HyperLogLog]], [[Count-Min Sketch]]
