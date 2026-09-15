---
title: DDSketch
notetype: feed
date: 2026-05-05
last_modified: 2026-09-16
tags: [data-structures, ddsketch, quantile, percentile, monitoring, latency, streaming, probabilistic, datadog]
status: published
---

# DDSketch: วัด p99 Latency แบบ Real-time ด้วย 5 KB

> **"API ของเรามี p99 latency เท่าไร? ต้องตอบได้ทันที โดยไม่เก็บ log ของทุก request"** DDSketch ช่วยประมาณค่านี้ได้ด้วยหน่วยความจำเพียง 5 KB โดยมี relative error ≤ 1%

DDSketch เป็นอัลกอริทึม **ประมาณค่า quantile** สำหรับหา percentile (p50, p90, p95, p99, p99.9) จาก data stream ใช้ติดตามการกระจายของ latency, response time และตัวชี้วัดอื่นแบบ real-time

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

DDSketch จัดค่าลง buckets ด้วย **logarithmic scaling** โดยช่วงค่าที่แต่ละ bucket ครอบคลุมจะกว้างขึ้นตามขนาดของค่า:

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

ตัวอย่างนี้ใช้การเลือกอันดับแบบ nearest-rank:

$$\text{target\_count} = \left\lceil q \times N \right\rceil$$

```
Walk buckets from smallest until cumulative ≥ target_count
Map bucket index back to its representative: v = 2 × γ^idx / (γ + 1)
```

### 🧮 ตัวอย่างการคำนวณ

```
α = 0.02 (2% error), γ = (1 + α) / (1 - α) ≈ 1.040816
ln(γ) ≈ 0.040005

Latencies (ms): [5, 12, 15, 23, 45, 67, 89, 120, 350, 890]

Step 1: Map to buckets
  ln(5)/ln(γ)   ≈ 40.2306  → bucket 41
  ln(12)/ln(γ)  ≈ 62.1144  → bucket 63
  ln(15)/ln(γ)  ≈ 67.6922  → bucket 68
  ln(23)/ln(γ)  ≈ 78.3769  → bucket 79
  ln(45)/ln(γ)  ≈ 95.1539  → bucket 96
  ln(67)/ln(γ)  ≈ 105.1033 → bucket 106
  ln(89)/ln(γ)  ≈ 112.2009 → bucket 113
  ln(120)/ln(γ) ≈ 119.6713 → bucket 120
  ln(350)/ln(γ) ≈ 146.4288 → bucket 147
  ln(890)/ln(γ) ≈ 169.7579 → bucket 170

Histogram (simplified):
  41→1, 63→1, 68→1, 79→1, 96→1, 106→1, 113→1, 120→1, 147→1, 170→1

Step 2: Query p50 (nearest-rank = ceil(0.50 × 10) = 5)
  Walk: bucket 41(1) → 63(2) → 68(3) → 79(4) → 96(5) ← target!
  
  p50 estimate = 2 × γ^96 / (γ + 1) ≈ 45.6183 ms
  True p50 = 45 ms
  Relative error = |45.6183 - 45| / 45 ≈ 1.374% ≤ 2%

Step 3: Query p99 (nearest-rank = ceil(0.99 × 10) = 10)
  Walk all → 10th value at bucket 170
  
  p99 estimate = 2 × γ^170 / (γ + 1) ≈ 880.6887 ms
  True p99 = 890 ms
  Relative error = |880.6887 - 890| / 890 ≈ 1.046% ≤ 2%
  
  The ideal mapping keeps relative error ≤ α for these positive values.
  A small sample does not invalidate this bound.
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
