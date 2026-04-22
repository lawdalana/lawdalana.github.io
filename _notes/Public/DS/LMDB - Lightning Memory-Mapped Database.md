---
title : LMDB - Lightning Memory-Mapped Database
notetype : feed
date : 22-04-2026
last_modified : 22-04-2026
tags : [database, lmdb, embedded-database, key-value-store, b-tree, mmap, mvcc, rocksdb, tuning, license]
status : published
---

# LMDB (Lightning Memory-Mapped Database)

LMDB คือ embedded transactional key-value database เขียนด้วย C โดย Howard Chu ในปี 2011 พัฒนาเพื่อใช้ใน [[OpenLDAP]] เพื่อทดแทน Berkeley DB

**License:** OpenLDAP Public License (BSD-style) — ไม่มีปัญหา license เหมือน Berkeley DB ที่ Oracle เปลี่ยนเป็น AGPL ในปี 2013

---

## สถาปัตยกรรมภาพรวม

```
┌─────────────────────────────────────────────┐
│              Application                      │
├─────────────────────────────────────────────┤
│          LMDB Library (C API)                │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ B+ Tree      │  │ Free Page Tracker    │  │
│  │ (data)       │  │ (B+ tree of freed    │  │
│  │              │  │  pages)              │  │
│  └──────┬───────┘  └──────────┬───────────┘  │
│         │   Copy-on-Write     │              │
├─────────┴────────────────────┴───────────────┤
│          Memory Map (mmap)                    │
│   ┌─────────────────────────────────────┐    │
│   │  Single File: data.mdb              │    │
│   │  [Meta0][Meta1][Data Pages...]       │    │
│   └─────────────────────────────────────┘    │
├──────────────────────────────────────────────┤
│          OS Page Cache (auto-managed)         │
├──────────────────────────────────────────────┤
│          Disk / SSD                           │
└──────────────────────────────────────────────┘
```

ไฟล์บน disk มีแค่ 2 ไฟล์:
- `data.mdb` — ไฟล์เดียวเก็บทุกอย่าง (metadata + B+ tree data + free pages)
- `lock.mdb` — shared memory สำหรับ reader slots + writer mutex

---

## 1. Memory Mapping (mmap) — พื้นฐานทั้งหมด

LMDB เริ่มต้นด้วยการ `mmap()` ไฟล์ data.mdb เข้า virtual memory:

```c
void *map = mmap(NULL, map_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
```

**สิ่งที่เกิดขึ้น:**
- OS สร้าง virtual memory mapping ของไฟล์ทั้งก้อน
- **ไม่ได้ load ทั้งไฟล์เข้า RAM** — load เฉพาะ pages ที่ access (lazy/on-demand)
- Access ข้อมูล = access memory pointer ตรง → **ไม่มี memcpy, ไม่มี malloc**

**ทำไมเร็ว:**
- OS page cache เป็น cache manager (ไม่ต้องเขียนเอง)
- Hot pages อยู่ใน RAM, cold pages อยู่ใน disk → OS จัดการเอง
- Multiple processes mmap ไฟล์เดียวกัน → **แชร์ page cache เดียวกัน**
- 64-bit: รองรับ DB ขนาดสูงสุด **128 TB** (48-bit address space)

---

## 2. โครงสร้างไฟล์ (On-Disk Layout)

```
┌──────────┬──────────┬──────────┬──────────┬─────────┐
│ Meta pg0 │ Meta pg1 │ Free DB  │ Main DB  │ ...     │
│ (4KB)    │ (4KB)    │ (B+tree) │ (B+tree) │ Free    │
│          │          │          │          │ Pages   │
└──────────┴──────────┴──────────┴──────────┴─────────┘
```

| Section | หน้าที่ |
|---|---|
| **Meta pg0/pg1** | สลับกันเก็บ root pointer + transaction ID (atomic commit) |
| **Free DB** | B+ tree เก็บรายการ pages ที่ว่าง (ถูกลบ/เก่า) |
| **Main DB** | B+ tree หลักเก็บ key-value pairs ของ user |

Meta pages สลับกัน (ping-pong) → commit = write meta page เดียว = atomic operation

---

## 3. B+ Tree — โครงสร้างข้อมูลหลัก

```
                    [Root Node]
                   /           \
          [Branch Node]    [Branch Node]
          /    |    \        /    |    \
      [Leaf] [Leaf] [Leaf] [Leaf] [Leaf] [Leaf]
       K1V1   K2V2   K3V3   K4V4   K5V5   K6V6
```

- **Branch nodes:** เก็บ keys + pointers to child pages
- **Leaf nodes:** เก็บ keys + values (actual data)
- **Page size** = OS page size (typically 4096 bytes)
- **Branching factor** ~100-256 children/node → tree ไม่ลึก
- **1M keys → tree depth ~3** → worst case 3 page reads

### Read: O(log N) page accesses

```
1. เริ่มที่ root page → mmap pointer ตรง
2. Binary search keys ใน branch node → หา child pointer
3. Follow pointer → page number → pointer arithmetic
4. ซ้ำจนถึง leaf → binary search key → return VALUE POINTER
5. Hot pages = pure memory access, cold pages = 1 page fault
```

---

## 4. Copy-on-Write (COW) — หัวใจของ LMDB

**กฎเหล็ก: ไม่เขียนทับข้อมูลเดิมเด็ดขาด**

### เพิ่มข้อมูลใหม่ step-by-step:

```
ก่อน write:
  B+ Tree: [...A(10)...B(20)...C(30)...]  ← Leaf page P5

ต้องการ insert: key=25, value="hello"

Step 1: COW — copy leaf page
  P5 (ORIGINAL)  → P5' (COPY)
  (readers ยังอ่านตัวเดิม)   (writer แก้ตัวใหม่)

Step 2: Insert into copy
  P5': A(10) B(20) [25="hello"] C(30)

Step 3: ถ้า page เต็ม → SPLIT เป็น 2 pages
  P5': A(10) B(20)
  P6': 25(hello) C(30)
  + Parent (COW'd): [...ptr P5', ptr P6']

Step 4: COW every page จาก leaf → root
  (tree depth 3-4 → copy 3-4 pages)

Step 5: Commit = atomic swap meta pointer
  Meta0 → Meta1 (สลับกัน)
```

### ผลของ COW:
- ✅ **Crash-proof:** disk structure ถูกต้องเสมอ (ไม่เขียนทับ)
- ✅ **No WAL:** ไม่ต้องเขียนข้อมูล 2 รอบ
- ✅ **Instant recovery:** เปิดไฟล์ = ใช้ได้เลย ไม่ต้อง replay
- ✅ **MVCC:** readers เห็น version เก่าได้ ไม่ lock กัน

---

## 5. MVCC (Multiversion Concurrency Control)

```
Timeline:
  T=0: Reader A starts → sees txn 5
  T=1: Writer starts txn 6
  T=2: Writer modifies P5 → COW → P5' (new copy)
       Reader A ยังเห็น P5 (old version)
  T=3: Writer commits txn 6
       New readers เห็น txn 6
       Reader A ยังเห็น P5
  T=4: Reader B starts → sees txn 6
  T=5: Reader A finishes
       P5 → "free" → added to Free Page Tree
  T=6: Writer txn 7 → reuse P5 from free tree
```

**Reader tracking:** shared memory array in `lock.mdb`
```
Slot 0: [thread_id, current_txn_id]
Slot 1: [thread_id, current_txn_id]
...
```
Writer scan: "oldest txn any reader is using?" → ไม่ free pages ที่ยังถูกใช้

**ผล:**
- Readers **scale linearly** — เพิ่ม thread = เพิ่ม throughput ตรง
- Readers **never block writers**, writers **never block readers**
- ⚠️ **Long-lived readers ทำให้ DB โต** — pages เก่าไม่ได้ free จนกว่า reader จะปิด

---

## 6. Free Page Management — ไม่ต้อง Compaction

```
Free Page Tree (B+ tree พิเศษ):
  Key:   txn_id + page_number
  Value: number of contiguous free pages

Flow:
  1. Page ถูกแทนที่ (COW) → page เก่าไม่ถูกเขียนทับ
  2. Reader ตัวสุดท้ายที่ใช้ page เก่า ปิด txn → page "free"
  3. Free page → ใส่ Free Page Tree
  4. Write txn ใหม่ → ดึงจาก Free Page Tree ก่อน
  5. Free pages หมด → ขยาย mmap file (grow)

ผล: DB size ไม่โตไม่หยุด (reuses pages), ไม่ต้อง compaction
```

---

## 7. Cache Miss — LMDB จัดการอย่างไร

### LMDB: OS จัดการหมด (no separate cache)

| Scenario | สิ่งที่เกิดขึ้น | เวลา |
|---|---|---|
| Page ใน RAM | Direct pointer access | ~50-100ns |
| Page ไม่ใน RAM | OS page fault → disk read | ~0.1ms (SSD) |
| Key ไม่มี | Binary search leaf → not found | ~50-100ns (if cached) |

### เทียบกับ RocksDB (LSM tree):

```
RocksDB read "user:456":
  1. Check memtable           → miss
  2. Check immutable memtable → miss
  3. Check L0 files (4-8)     → miss, miss, miss
  4. Check L1 files           → miss
  5. Check L2 files           → found! (or truly not exist)
  Total: potentially 5+ I/O operations

LMDB read "user:456":
  1. B+ tree traversal (3-4 pages)
  2. Binary search leaf → found or not found
  Total: 1 path = 3-4 page accesses
```

**LMDB หา key ที่ไม่มี เร็วพอๆ กับหา key ที่มี** (ถ้า pages cached) เพราะเป็น single tree traversal เทียบกับ LSM ที่ต้อง check หลาย level

---

## 8. ทำไม LMDB Write ช้ากว่า RocksDB

### Write Path เปรียบเทียบ

```
═══ LMDB ═══
mdb_put(txn, key, value):
  1. COW leaf page (memcpy 4KB)
  2. Insert key-value (memmove + binary search)
  3. If full → SPLIT (copy + redistribute + update parent)
  4. COW every page from leaf to root (3-4 pages)
  5. Atomic meta page write (commit)
  Total: ~3-5μs per write

═══ RocksDB ═══
db.Put(key, value):
  1. Append to WAL (sequential write, optional fsync)
  2. Insert into memtable (skiplist, in-memory)
  3. Return ✅
  Total: ~0.5-1μs per write
  (Background compaction happens later)
```

### 4 เหตุผลที่ LMDB write ช้ากว่า:

**1. COW Overhead** — copy 3-4 pages (12-16KB) ทุก write
**2. Immediate tree update** — update B+ tree ทันที ไม่ defer
**3. Single writer** — 1 thread write เท่านั้น, serialized
**4. Page splits** — page เต็ม → split cascade (expensive, random)

### แต่ RocksDB ไม่ได้เร็วกว่า "ฟรี"

| Hidden Cost | LMDB | RocksDB |
|---|---|---|
| Compaction | **ไม่มี** | Background I/O heavy |
| Write stalls | **ไม่มี** | 100ms - 10s pauses |
| Write amplification | **1-2x** | **10-30x** (SSD wear) |
| Tuning | 3 params | 50+ params |

> LMDB = "จ่ายตอน write" → ไม่มี hidden cost
> RocksDB = "จ่ายตอน write น้อย แต่ชดเชยด้วย compaction ทีหลัง"

---

## 9. Performance Summary

### Benchmark (approximate, in-memory, 16B key / 100B value)

```
            Random Read    Random Write    Batch Write
LMDB:       ~4,500,000/s   ~  800,000/s    ~2,200,000/s (append)
RocksDB:    ~1,800,000/s   ~2,500,000/s    ~2,500,000/s
LevelDB:    ~  450,000/s   ~  600,000/s    ~1,000,000/s
SQLite:     ~1,200,000/s   ~  400,000/s    ~  800,000/s
```

### LMDB เร็วสุดใน:
- Random reads (~2.5x faster than RocksDB)
- Batch writes with MDB_APPEND
- Multi-process read scaling (linear)

### RocksDB เร็วสุดใน:
- Random writes (~3x faster than LMDB)
- Multi-writer throughput

---

## 10. เปรียบเทียบ LMDB vs RocksDB

| | LMDB | RocksDB |
|---|---|---|
| **Data Structure** | B+ Tree (COW) | LSM Tree |
| **Read Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Write Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Write Amplification** | 1-2x | 10-30x |
| **Compaction** | ไม่ต้อง | ต้อง (causes stalls) |
| **Crash Recovery** | Instant (0ms) | WAL replay (ms-min) |
| **Concurrency** | MVCC, lock-free reads | Snapshots + compaction |
| **Writers** | Single | Multiple |
| **Memory** | OS-managed (mmap) | Manual block cache |
| **Tuning** | 3 parameters | 50+ parameters |
| **Max DB Size** | 128 TB | No limit |
| **Multi-process** | ✅ แชร์ mmap | ❌ Single process |
| **License** | OpenLDAP (BSD) | Apache 2.0 / GPLv2 |

---

## 11. เลือกอะไรเมื่อไหร่

### ใช้ LMDB เมื่อ:
- ✅ Read-heavy workloads (reads >> writes)
- ✅ ต้องการ predictable latency (no stalls)
- ✅ SSD lifespan สำคัญ (low write amplification)
- ✅ Instant crash recovery
- ✅ Multi-process shared access
- ✅ ไม่อยาก tune 50 parameters
- ✅ Embedded systems, constrained resources

### ใช้ RocksDB เมื่อ:
- ✅ Write-heavy workloads (writes >> reads)
- ✅ ต้องการ multi-writer
- ✅ ข้อมูลเยอะมาก (>128TB)
- ✅ ต้องการ column families, merge operators, TTL
- ✅ ใช้เป็น storage engine ใน DBMS (MySQL, MongoDB, [[TiDB]])

### พิจารณา libmdbx (LMDB successor):
- Better write performance + concurrent writers
- ใช้ใน Ethereum (Erigon, Reth), blockchain nodes
- Trade-off: ecosystem เล็กกว่า LMDB

---

## 12. โปรเจกต์ที่ใช้ LMDB

| Project | Use Case |
|---|---|
| OpenLDAP | Original purpose, directory service |
| Monero | Blockchain storage |
| Meilisearch | Search engine |
| Samba AD | Active Directory DC |
| Postfix | Mail lookup tables |
| PowerDNS / Knot DNS | DNS server |
| Shopify | SkyDB system |
| Nano | Cryptocurrency |
| Sun Grid Engine | Job scheduling |

---

## 13. Python Usage

```python
import lmdb

# Open — map_size = max DB size
env = lmdb.open('mydb', map_size=1 << 30)  # 1 GB

# Write
with env.begin(write=True) as txn:
    txn.put(b'user:1', b'{"name":"Alice"}')
    txn.put(b'user:2', b'{"name":"Bob"}')

# Read (zero-copy)
with env.begin() as txn:
    val = txn.get(b'user:1')  # pointer to mmap, no copy!
    print(val)  # b'{"name":"Alice"}'

# Range scan
with env.begin() as txn:
    cursor = txn.cursor()
    for key, value in cursor:
        print(key, value)

# Fast append (keys must be pre-sorted!)
with env.begin(write=True) as txn:
    for i in range(100_000):
        txn.put(f'key:{i:06d}'.encode(), b'data', append=True)

# Delete
with env.begin(write=True) as txn:
    txn.delete(b'user:2')

# Multiple databases
with env.begin(write=True) as txn:
    db_index = env.open_db(b'index', txn=txn)
    txn.put(b'reverse_key', b'value', db=db_index)
```

---


## 14. Parameter Tuning

LMDB มี parameter แค่ **3 ตัวหลัก** — เทียบกับ RocksDB ที่มี 50+

### map_size — สำคัญที่สุด

```python
env = lmdb.open('mydb', map_size=1 << 40)  # 1 TB
```

| | รายละเอียด |
|---|---|
| **คืออะไร** | ขนาด virtual memory ที่ mmap จองไว้ (upper bound ของ DB) |
| **ไม่ได้ใช้ RAM จริง** | เป็น virtual address space เท่านั้น |
| **เต็มแล้ว** | `mdb_map_full` error → ต้อง close + resize + reopen |
| **แนะนำ** | ตั้งใหญ่กว่าที่คิดไว้ เช่น `1 << 40` (1 TB) |

```
Development:   1 << 30   (1 GB)
Production:    1 << 40   (1 TB)
Large system:  1 << 43   (8 TB)
```

### max_readers — จำนวน concurrent readers

```python
env = lmdb.open('mydb', max_readers=126)  # default
```

- จำนวน concurrent read transactions สูงสุด (thread-level)
- LMDB ใช้ shared memory array (`lock.mdb`) เก็บ reader slots
- Default = 126, แต่ละ slot เล็กมาก → ตั้งเยอะไม่เสียอะไร

```
Single process:   16-32
Multi-process:    128 (default)
High concurrency: 256-1024
```

### max_dbs — จำนวน named databases

```python
env = lmdb.open('mydb', max_dbs=5)  # default = 1
```

- Default = 1 (main DB only) — ต้องตั้งเพิ่มถ้าใช้ `open_db()`
- **ตั้งตอนสร้างเท่านั้น** — เปลี่ยนทีหลังไม่ได้

```python
env = lmdb.open('mydb', max_dbs=10)
users_db = env.open_db(b'users')
index_db = env.open_db(b'index')
```

### Environment Flags

| Flag | ทำอะไร | ใช้เมื่อ |
|---|---|---|
| `MDB_WRITEMAP` | เขียนตรงผ่าน mmap (เร็วขึ้น) | มั่นใจ app ไม่มี bug |
| `MDB_MAPASYNC` | Flush async | Balance ระหว่าง speed + safety |
| `MDB_NOMETASYNC` | ไม่ fsync meta page | Write speed > crash safety |
| `MDB_NOSYNC` | ไม่ fsync เลย | Batch loading, rebuildable data |
| `MDB_NOLOCK` | ไม่ใช้ locking | Single-process only |
| `MDB_RDONLY` | Read-only mode | Read replicas |

### Sync Flags มีผลมากต่อ write throughput

```
Default (safest):     fsync ทุก commit    → ~5,000 writes/s (SSD)
MDB_NOMETASYNC:       skip meta fsync      → ~50,000 writes/s
MDB_NOSYNC+MAPASYNC:  no fsync at all      → ~200,000+ writes/s
```

### Transaction Flags

| Flag | ทำอะไร |
|---|---|
| `MDB_NOOVERWRITE` | Put ไม่เขียนทับ key เดิม |
| `MDB_APPEND` | Append mode (keys ต้อง sorted) — เร็วมาก |
| `MDB_APPENDDUP` | Append สำหรับ duplicate keys |

### 99% use cases

```python
env = lmdb.open('mydb', map_size=1 << 40, max_dbs=5)
```

---

## 15. License — OpenLDAP Public License (BSD-style)

### ✅ ทำได้

- **ใช้เชิงพาณิชย์** — ฝังใน product ขายได้
- **ใช้ใน closed-source product** — ไม่ต้องเปิด code
- **SaaS** — ใช้เป็น backend โดยไม่ต้องเปิด source
- **แก้ไข source code** — modify + redistribute ได้
- **Embed ใน hardware** — IoT, embedded devices
- **Sub-license** — ให้สิทธิ์คนอื่นต่อได้

### ⚠️ เงื่อนไข

- รักษา copyright notice + license text
- ถ้าแจก source → แสดงว่าใช้ LMDB (attribution)
- ไม่ใช้ชื่อ "OpenLDAP" โปรโมท product โดยไม่ได้รับอนุญาต

### ❌ ทำไม่ได้

- ลบ/แก้ copyright notice
- บอกว่า author รับรอง product ของคุณ

### เทียบกับ license อื่น

| | LMDB (OpenLDAP) | Berkeley DB (AGPL) | RocksDB (Apache 2.0) |
|---|---|---|---|
| Commercial use | ✅ | ⚠️ ต้องเปิด source | ✅ |
| Closed source | ✅ | ❌ | ✅ |
| SaaS โดยไม่เปิด code | ✅ | ❌ | ✅ |
| ต้องเปิด code ตัวเอง | ❌ | ✅ (AGPL) | ❌ |
| Patent grant | ❌ | ❌ | ✅ |

> ใจเย็นมาก ใช้ได้แทบทุกที่ ไม่มี trap เหมือน AGPL ของ Berkeley DB

---

## 16. Caveats & Best Practices

- **ตั้ง `map_size` ให้พอ** — ถ้าเต็มจะเขียนไม่ได้ (ต้อง resize = close + reopen)
- **หลีกเลี่ยง long-lived read transactions** — pages เก่าไม่ free → DB โต
- **เช็ค stale readers:** `mdb_reader_check()` หรือ `mdb_stat -r`
- **File format architecture-dependent** — ย้าย 32↔64 bit ต้อง export/import
- **อย่าใช้บน remote filesystem** — mmap + flock ไม่ reliable
- **Single writer** — ถ้าต้องการ multi-writer ใช้ libmdbx แทน

---

## References

- [LMDB Official](http://www.lmdb.tech/)
- [LMDB Source (mdb.c)](https://github.com/openldap/openldap/blob/master/libraries/liblmdb/mdb.c)
- [py-lmdb Docs](https://lmdb.readthedocs.io/)
- Howard Chu, "MDB: A Memory-Mapped Database and Backend for OpenLDAP" (2011)
- Symas Corp, [Database Microbenchmarks](http://www.lmdb.tech/bench/microbench/) (2012)
- Wikipedia: [LMDB](https://en.wikipedia.org/wiki/Lightning_Memory-Mapped_Database), [RocksDB](https://en.wikipedia.org/wiki/RocksDB)
- libmdbx: [github.com/erthink/libmdbx](https://github.com/erthink/libmdbx)
- Related: [[RocksDB]], [[LevelDB]], [[Berkeley DB]]
