---
title: "DDTree: Dynamic Draft Tree for Speculative Decoding"
notetype: feed
date: 2026-05-09
last_modified: 2026-09-16
tags: [llm, speculative-decoding, inference, tree-search, rust]
status: published
---

# DDTree (Dynamic Draft Tree)

> ใช้ Best-First Search สร้างต้นไม้ของ token ที่ draft model เสนอ แล้วให้ target model ตรวจสอบทั้งต้นไม้และเลือกเส้นทางที่ผ่านการตรวจสอบได้ยาวที่สุด เพื่อเร่ง LLM inference โดยรักษาคุณภาพคำตอบ

## ทำไมต้องเป็น Tree

Speculative decoding แบบ linear ให้ draft model ทำนาย token ต่อเนื่องกันเป็นเส้นทางเดียว

```
Prefix → [draft₁] → [draft₂] → [draft₃] → [draft₄] → [draft₅]
```

ถ้า token ตัวที่ 3 ไม่ผ่านการตรวจสอบ ก็ต้อง **ยกเลิก token 4, 5 ด้วย** ทำให้ draft อีก 2 tokens ใช้ต่อไม่ได้

**DDTree เพิ่มทางเลือก** ด้วยการสร้างต้นไม้ที่แตกแขนงเป็นหลายเส้นทาง:

```
                    Prefix
                   /   |   \
              draft₁  draft₁' draft₁"
              /  \      |       |
         draft₂ draft₂' draft₂"  ...
          /       |
       draft₃   draft₃'
```

ถ้าเส้นทาง `draft₁-draft₂-draft₃` ไม่ผ่าน ก็ยังมีเส้นทางอื่นให้ตรวจ เช่น `draft₁-draft₂'-draft₃'` หรือ `draft₁'-draft₂"` จึงเพิ่มโอกาสใช้ token ที่ draft ไว้

## มาจากไหน

แนวคิด tree-based speculative decoding มาจาก:

| Paper | Year | สิ่งที่ทำ |
|-------|------|----------|
| **SpecInfer** (CMU) | 2023 | Token tree + tree verification, เร่ง 2.6-3.5× |
| **EAGLE-2** | 2024 | Dynamic draft tree ที่ปรับตาม context, ใช้ draft model confidence |
| **DDTree** (project นี้) | — | Best-First Search + BinaryHeap, pure Rust |

## ทำงานยังไง (Step by Step)

### Phase 1: Build Tree

```
1. Draft model forward pass บน prefix
   → ได้ log-probabilities สำหรับทุก token ใน vocabulary

2. เลือก top-K tokens เป็น root children
   → ใส่เข้า BinaryHeap (priority = log-prob, สูง = ดีกว่า)

3. Loop: Pop top candidate → expand → push children
   while tree_nodes < BUDGET:
       node = heap.pop()           // ดึง candidate ที่ดีสุด
       children = expand(node)     // draft model ทำนายต่อ
       for child in children:
           heap.push(child)        // ใส่กลับเข้า heap

4. Output: tree ที่มี nodes ไม่เกิน BUDGET
```

### Phase 2: Verify Tree

```
5. Pack tree เป็น batch → run target model 1 ครั้ง
   (tree attention mask ทำให้ target model verify ทุก path พร้อมกัน)

6. ตรวจทุก node: accept/reject ตาม Leviathan criteria

7. หา accepted path ที่ยาวที่สุด → return tokens ตาม path นั้น
```

### Phase 3: Continue

```
8. เพิ่ม accepted tokens เข้า prefix → กลับไป Phase 1
```

## BinaryHeap ใน Rust

DDTree ใช้ `std::collections::BinaryHeap` ซึ่งเป็น max-heap โดยแต่ละ operation มีความซับซ้อนดังนี้:

| Operation | Complexity |
|-----------|-----------|
| `push` | O(log n) |
| `pop` | O(log n) |
| `peek` | O(1) |

```rust
use std::collections::BinaryHeap;
use std::cmp::Reverse;

// Max-heap: ค่ามาก = priority สูง = log-prob ดี
let mut heap: BinaryHeap<TreeNode> = BinaryHeap::new();

// Push root candidates
for (token_id, log_prob) in top_k_logits {
    heap.push(TreeNode { path: vec![token_id], score: log_prob });
}

// Expand tree
while heap.len() < budget {
    let best = heap.pop().unwrap();
    let logits = draft_model.forward(&best.path);
    for (token_id, log_prob) in logits.top_k() {
        let new_score = best.score + log_prob; // cumulative log-prob
        heap.push(TreeNode {
            path: [...best.path, token_id],
            score: new_score,
        });
    }
}
```

## Tree Budget

Budget คือจำนวน nodes สูงสุดใน tree ใช้จำกัดต้นทุนการคำนวณ

```
Budget น้อย (เช่น 8):
  → tree เล็ก → verify เร็ว
  → แต่ไม่ครอบคลุมทางเลือก → acceptance rate ต่ำกว่า

Budget มาก (เช่น 64):
  → tree ใหญ่ → verify ช้า
  → แต่มีทางเลือกเยอะ → โอกาสเจอ accepted path ยาวสูงกว่า
```

**Budget ที่เหมาะสม** ขึ้นกับ acceptance rate:

| Acceptance Rate | Best Budget | เหตุผล |
|----------------|-------------|--------|
| สูง (>90%) | เล็ก (4-8) | draft แม่นอยู่แล้ว ไม่ต้องมีทางเลือกเยอะ |
| กลาง (70-90%) | กลาง (16-32) | บาง token ไม่ผ่านการตรวจสอบ จึงควรมีทางเลือกสำรอง |
| ต่ำ (<70%) | ใหญ่ (32-64) | draft ไม่แม่น → ต้องมีทางเลือกเยอะ |

## DDTree vs DFlash vs Linear Speculative

| Aspect | Linear Speculative | DFlash | DDTree |
|--------|-------------------|--------|--------|
| **โครงสร้าง** | เส้นตรง (1 path) | Flat (L independent) | Tree (multiple paths) |
| **Draft cost** | L × forward_pass | 1 × forward_pass | ~log(B) × forward_pass |
| **Verify cost** | O(L) | O(L) | O(tree_nodes) |
| **Diversity** | ต่ำ (1 path) | กลาง (independent) | สูง (branching) |
| **เมื่อไรดีสุด** | Draft แม่นมาก | Draft แม่น + ต้องการ speed | Draft ไม่แม่น / context ซับซ้อน |

## Workflow แบบเต็ม

```
┌──────────────┐
│   Input Text  │
│   "The cat"   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Phase 1: Build Tree                 │
│                                       │
│  Draft model forward pass on prefix  │
│       ↓                               │
│  Top-3 tokens: "sat"(0.4) "was"(0.3) "is"(0.2) │
│       ↓                               │
│  BinaryHeap:                          │
│    [score=-0.92] "sat"               │
│    [score=-1.20] "was"               │
│    [score=-1.61] "is"                │
│       ↓                               │
│  Expand "sat" → "on"(0.5) "down"(0.3)│
│  Expand "was" → "sit"(0.4) "not"(0.3)│
│       ↓                               │
│  Tree (budget=8):                     │
│          "The cat"                    │
│         /    |    \                   │
│      "sat" "was"  "is"               │
│      / \     |                        │
│   "on""down""sit"                     │
│    |                                 │
│  "the"                               │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Phase 2: Verify with Target Model   │
│                                       │
│  Pack tree → single batched forward  │
│  Target model checks EVERY path:     │
│                                       │
│  "sat" → ✅ (p/q = 1.2 > 1)         │
│  "sat"→"on" → ✅ (p/q = 0.95)       │
│  "sat"→"on"→"the" → ✅ (p/q = 1.1)  │
│  "sat"→"down" → ❌ (p/q = 0.3)      │
│  "was" → ❌ (p/q = 0.4)              │
│  "is" → ❌ (p/q = 0.2)               │
│                                       │
│  Longest accepted path: sat→on→the   │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Result: "The cat sat on the"         │
│  (3 tokens from 1 target verification)│
│                                       │
│  Without DDTree: 3 separate steps     │
│  With DDTree:    1 verify + 8 draft   │
│  → ~2-3× faster                      │
└──────────────────────────────────────┘
```

## Performance (จาก SpecInfer / EAGLE-2 benchmarks)

| Model | Method | Speedup | Notes |
|-------|--------|---------|-------|
| LLaMA-2-70B | Linear speculative | 2.0-2.5× | Baseline tree |
| LLaMA-2-70B | SpecInfer (tree) | 2.6-3.5× | ดีกว่า linear |
| Vicuna-33B | EAGLE-2 (dynamic tree) | 3.0-4.0× | Context-aware |
| Small model (draft=4d) | DDTree | ~2-3× | Project-specific |

## Limitations

1. **Memory:** ต้องเก็บทุกเส้นทางใน tree จึงใช้หน่วยความจำมากกว่าแบบ linear
2. **Tree attention mask:** Target model ต้องรองรับ tree-structured attention ทำให้ implementation ซับซ้อนขึ้น
3. **Budget tuning:** ต้องหา budget ที่เหมาะสม ถ้ามากเกินไปจะตรวจสอบช้า แต่ถ้าน้อยเกินไปก็อาจพลาดเส้นทางที่ผ่านการตรวจสอบ
4. **Draft model quality:** หาก draft model ทำนายได้ไม่ดี การเพิ่มขนาด tree ก็อาจไม่ช่วย

## Papers ที่เกี่ยวข้อง

- **SpecInfer** — [arXiv:2305.09781](https://arxiv.org/abs/2305.09781): Tree-based speculative inference and verification
- **EAGLE-2** — [arXiv:2406.16858](https://arxiv.org/abs/2406.16858): Dynamic draft trees with context-awareness
- **Leviathan et al.** — [arXiv:2211.17192](https://arxiv.org/abs/2211.17192): Original speculative decoding with rejection sampling
- **Blockwise Parallel Decoding** — [arXiv:1811.03115](https://arxiv.org/abs/1811.03115): Parallel decoding precursor

---

*DDTree นำ Best-First Search มาใช้กับ speculative decoding เพื่อสร้างทางเลือกหลายเส้นทาง แล้วให้ target model ตรวจสอบและเลือกเส้นทางที่ผ่านเกณฑ์*
