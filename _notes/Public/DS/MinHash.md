---
title: MinHash
notetype: feed
date: 2026-05-05
last_modified: 2026-05-05
tags: [data-structures, minhash, similarity, jaccard, lsh, locality-sensitive-hashing, document-dedup, probabilistic]
status: published
---

# MinHash: เปรียบเทียบความคล้ายของชุดข้อมูลด้วย 2 KB

> **"มีเอกสาร 1 ล้านฉบับ — จะรู้ได้ยังไงว่าฉบับไหนคล้ายกัน โดยไม่ต้องเปรียบเทียบทุกคู่ (500 พันล้านคู่)?"** — MinHash ลดปัญหานี้เหลือเปรียบเทียบแค่ signature ขนาด 2 KB ต่อชุด

MinHash เป็น **Locality-Sensitive Hashing (LSH)** technique สำหรับประเมิน **Jaccard Similarity** ระหว่างชุดข้อมูล — ใช้ใน document deduplication, recommendation systems, DNA sequence comparison, และ web-scale similarity search

**Inventor:** Andrei Broder (1997) — สร้างเพื่อใช้ใน AltaVista search engine สำหรับ deduplicate web pages

---

## Jaccard Similarity: พื้นฐาน

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

```
ตัวอย่าง:
  A = {the, quick, brown, fox, jumps}
  B = {the, quick, brown, cat, jumps}
  
  A ∩ B = {the, quick, brown, jumps}       → 4 words
  A ∪ B = {the, quick, brown, fox, cat, jumps} → 6 words
  
  J(A, B) = 4/6 = 0.667 (66.7% similar)
  
  J = 1.0 → identical
  J = 0.0 → completely different
```

**ปัญหา:** คำนวณ Jaccard แบบ exact ต้องเก็บทุก element ในทั้งสองชุด → O(|A| + |B|) ต่อการเปรียบเทียบ 1 คู่

---

## MinHash Insight

**Key Property:**

$$P(\min h(A) = \min h(B)) = J(A, B)$$

> "probability ที่ hash ต่ำสุดของ A และ B จะเท่ากัน = Jaccard similarity ของ A และ B"

### ทำไม?

```
h เป็น random permutation ของ universe U

min h(A) = min h(B) ⟺ element ที่ hash ต่ำสุด อยู่ใน A ∩ B

P(min hash value is in intersection) = |A ∩ B| / |A ∪ B| = J(A, B)
```

---

## Algorithm Step-by-Step

### Step 1: เลือก k hash functions

```
h₁, h₂, ..., hₖ  (k = 128 or 256, typically)

ใช้ double hashing trick สร้างจาก 2 functions:
  hᵢ(x) = h₁(x) + i × h₂(x)  (mod large prime)
```

### Step 2: สร้าง Signature ของแต่ละ set

```
สำหรับ set S:

sig(S) = [min(h₁(S)), min(h₂(S)), ..., min(hₖ(S))]

= [min{h₁(x) : x ∈ S},
   min{h₂(x) : x ∈ S},
   ...,
   min{hₖ(x) : x ∈ S}]
```

### Step 3: Estimate Jaccard

$$\hat{J}(A, B) = \frac{|\{i : \text{sig}(A)[i] = \text{sig}(B)[i]\}|}{k}$$

---

## 🧮 ตัวอย่างการคำนวณแบบละเอียด

```
Set A = {1, 3, 5, 7}
Set B = {3, 5, 7, 9}

True Jaccard: |A ∩ B| / |A ∪ B| = |{3,5,7}| / |{1,3,5,7,9}| = 3/5 = 0.6

Hash functions (k=5):

For each element, compute h₁..h₅:
┌───────┬─────┬─────┬─────┬─────┬─────┐
│ item  │ h₁  │ h₂  │ h₃  │ h₄  │ h₅  │
├───────┼─────┼─────┼─────┼─────┼─────┤
│   1   │  3  │  7  │  2  │  5  │  1  │
│   3   │  1  │  4  │  8  │  2  │  6  │
│   5   │  6  │  2  │  1  │  8  │  3  │
│   7   │  4  │  9  │  5  │  3  │  7  │
│   9   │  2  │  5  │  3  │  1  │  4  │
└───────┴─────┴─────┴─────┴─────┴─────┘

Signature of A = {1, 3, 5, 7}:
  sig(A)[1] = min(h₁(1), h₁(3), h₁(5), h₁(7)) = min(3,1,6,4) = 1
  sig(A)[2] = min(h₂(1), h₂(3), h₂(5), h₂(7)) = min(7,4,2,9) = 2
  sig(A)[3] = min(h₃(1), h₃(3), h₃(5), h₃(7)) = min(2,8,1,5) = 1
  sig(A)[4] = min(h₄(1), h₄(3), h₄(5), h₄(7)) = min(5,2,8,3) = 2
  sig(A)[5] = min(h₅(1), h₅(3), h₅(5), h₅(7)) = min(1,6,3,7) = 1
  
  sig(A) = [1, 2, 1, 2, 1]

Signature of B = {3, 5, 7, 9}:
  sig(B)[1] = min(h₁(3), h₁(5), h₁(7), h₁(9)) = min(1,6,4,2) = 1
  sig(B)[2] = min(h₂(3), h₂(5), h₂(7), h₂(9)) = min(4,2,9,5) = 2
  sig(B)[3] = min(h₃(3), h₃(5), h₃(7), h₃(9)) = min(8,1,5,3) = 1
  sig(B)[4] = min(h₄(3), h₄(5), h₄(7), h₄(9)) = min(2,8,3,1) = 1
  sig(B)[5] = min(h₅(3), h₅(5), h₅(7), h₅(9)) = min(6,3,7,4) = 3
  
  sig(B) = [1, 2, 1, 1, 3]

Compare signatures:
  Position 1: 1 == 1 → ✅ match
  Position 2: 2 == 2 → ✅ match
  Position 3: 1 == 1 → ✅ match
  Position 4: 2 ≠ 1 → ❌ no match
  Position 5: 1 ≠ 3 → ❌ no match

Matches: 3/5 = 0.6 ✅ EXACT! (lucky with small k)

With k=200: estimate ≈ 0.58-0.62 (close to true 0.6)
Standard Error = 1/√k = 1/√200 ≈ 7%
```

---

## Accuracy vs Space

$$\text{Standard Error} = \frac{1}{\sqrt{k}}$$

| k (hash functions) | Signature Size | Standard Error |
|---------------------|---------------|----------------|
| 64 | 512 B | 12.5% |
| 128 | 1 KB | 8.8% |
| **256** | **2 KB** | **6.3%** |
| 512 | 4 KB | 4.4% |
| 1024 | 8 KB | 3.1% |

---

## LSH Forest: Scaling to Billions

```
ปัญหา: เปรียบเทียบ 1M documents ทั้งหมด = C(1M,2) = 500 พันล้านคู่

LSH Forest Solution:
  1. สร้าง MinHash signature ของทุก document
  2. สร้าง prefix tree (trie) บน signatures
  3. Query: traverse tree → ได้แค่ candidates ที่คล้าย
  4. Verify candidates แบบ exact

Complexity: O(n × k × log n) แทน O(n²)

Python library: datasketch.MinHashLSHForest
```

---

## Variants

### One-Permutation MinHash (OPH)
```
ใช้ hash function แค่ 1 ตัว + partition เป็น k bins
เร็วกว่า standard MinHash 5-10x
Li, Owen, Zhang (2012)
```

### b-bit MinHash
```
เก็บแค่ b bits แรกของแต่ละ hash (b=1 คือ default)
ลด space 8x, เพิ่ม variance เล็กน้อย
Li & König (2010)
```

### BagMinHash
```
สำหรับ weighted sets (elements มี weight)
จัดการ bag/multiset similarity
Ertl (2020)
```

---

## SimHash: Alternative สำหรับ Cosine Similarity

| | MinHash | SimHash |
|---|---------|---------|
| **Similarity** | Jaccard | Cosine |
| **Signature** | k × 64 bits | 64-128 bits |
| **Compare** | O(k) | O(1) (XOR + popcount) |
| **Best for** | Set overlap | Document fingerprint |
| **Used by** | AltaVista, recommendation | **Google web dedup** |

```
SimHash algorithm:
  1. Hash each token → vector of +1/-1
  2. Sum all vectors element-wise
  3. Take sign → fingerprint (64-128 bits)
  4. Compare: similarity ≈ 1 - hamming_distance/bits
```

---

## Code Examples

### Python (datasketch)

```python
from datasketch import MinHash, MinHashLSH

# Build MinHash for document A
mha = MinHash(num_perm=128)  # k=128 permutations
for word in doc_a.split():
    mha.update(word.encode('utf8'))

# Build MinHash for document B
mhb = MinHash(num_perm=128)
for word in doc_b.split():
    mhb.update(word.encode('utf8'))

# Estimate Jaccard similarity
print(f"Jaccard: {mha.jaccard(mhb):.3f}")

# LSH for finding similar documents at scale
lsh = MinHashLSH(threshold=0.5, num_perm=128)
lsh.insert("doc_a", mha)
lsh.insert("doc_b", mhb)

# Query: find all docs > 50% similar
result = lsh.query(mhc)  # → ["doc_a", "doc_b"]
```

### DNA Sequence Similarity (Mash)

```bash
# Mash uses MinHash for genome comparison
mash sketch genome1.fna genome2.fna
mash dist genome1.fna.msh genome2.fna.msh
# → distance: 0.034  (96.6% similar!)
```

---

## Real-World Applications

| Application | ใช้อย่างไร |
|-------------|----------|
| **Document deduplication** | เปรียบเทียบ MinHash signatures → dedup 95%+ |
| **Recommendation** | "Users who bought A also bought B" = similar user sets |
| **Genome comparison** | Mash tool — compare entire genomes in seconds |
| **Image dedup** | MinHash on perceptual hash features |
| **Database query optimization** | Estimate join selectivity |
| **Web crawl dedup** | AltaVista → Google (now SimHash) |

---

## Summary

| Aspect | Detail |
|--------|--------|
| **What** | ประเมิน Jaccard similarity ระหว่างชุดข้อมูล |
| **Space** | k × 8 bytes per set (2 KB for k=256) |
| **Error** | ~$1/\sqrt{k}$ (6.3% for k=256) |
| **Compare** | O(k) per pair |
| **Scale** | LSH Forest → O(n log n) instead of O(n²) |
| **Merge** | ❌ (unlike HLL) |

---

## References

- Broder, A. (1997). "On the Resemblance and Containment of Documents"
- Li, P. & König, A. (2010). "b-Bit Minwise Hashing"
- datasketch library: [ekzhu.com/datasketch](https://ekzhu.com/datasketch/)
- Mash: [genomebiology.biomedcentral.com](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-0997-x)
- Related: [[Probabilistic Data Structures]], [[HyperLogLog]], [[Space-Saving Algorithm]]
