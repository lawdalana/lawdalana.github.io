---
title: "LMDB - Lightning Memory-Mapped Database"
notetype: feed
date: 2026-08-16
last_modified: 2026-08-17
tags: [database, lmdb, embedded-database, key-value-store, b-tree, mmap, mvcc, rocksdb, tuning, license]
status: published
---

# LMDB (Lightning Memory-Mapped Database)

LMDB คือ embedded transactional key-value database แบบเรียงลำดับ เขียนด้วย C และเป็นส่วนหนึ่งของโครงการ OpenLDAP จุดเด่นคือใช้ `mmap`, B+ tree, MVCC และ copy-on-write (COW) เพื่อให้หลาย read transactions อ่าน snapshot ที่คงที่ได้พร้อมกัน ขณะที่มี write transaction ทำงานได้ครั้งละหนึ่งตัว

## Mental model แบบสั้น

1. Environment ปกติมี `data.mdb` สำหรับข้อมูล และ `lock.mdb` สำหรับ coordination
2. ทุกการอ่าน/เขียนต้องอยู่ใน transaction
3. Reader อ่าน root ของ snapshot ตัวเอง แล้วเดิน B+ tree ผ่าน memory map
4. Writer ไม่แก้ active page เดิม แต่สร้าง page ชุดใหม่ด้วย COW
5. Commit เผยแพร่ root ใหม่ผ่าน meta page อีกฝั่ง ส่วน page เก่าจะ reuse ได้เมื่อไม่มี reader เก่าใช้อยู่

> LMDB ไม่มี server process, WAL หรือ background compaction thread แต่ความทนทานของ commit ยังขึ้นกับ sync flags, filesystem และ storage hardware

---

## สถาปัตยกรรมภาพรวม

![LMDB architecture: read path, write path, mmap, data.mdb และ lock.mdb](/assets/img/DS/LMDB/lmdb-architecture.svg)

*เส้นสีฟ้าแสดง read path ผ่าน snapshot และ memory map; เส้นสีส้มแสดง write path ที่ serialize writer, ทำ COW และ publish snapshot ใหม่ตอน commit*

Environment แบบ directory ปกติมีไฟล์หลัก 2 ไฟล์:

- `data.mdb` — meta pages, Main DB, named DBs, FreeDB และ overflow pages
- `lock.mdb` — shared synchronization state, writer lock และ reader slots; ไม่ใช่ user data

ถ้าเปิดด้วย `MDB_NOSUBDIR` จะระบุ path ของ data file โดยตรง และ LMDB จะใช้ lock file อีกชื่อหนึ่งที่เติม suffix ตาม API แทนรูปแบบ directory ข้างต้น

---

## 1. Memory mapping และ read path

LMDB map `data.mdb` เข้า virtual address space โดยค่าปกติเป็น read-only mapping; `MDB_WRITEMAP` จึงเป็นโหมด opt-in สำหรับ writable mapping

```c
int prot = PROT_READ;
if (flags & MDB_WRITEMAP) prot |= PROT_WRITE;
void *map = mmap(NULL, map_size, prot, MAP_SHARED, fd, 0);
```

สิ่งที่ควรเข้าใจ:

- การ map ไฟล์ใหญ่ **ไม่ได้หมายความว่าไฟล์ทั้งก้อนอยู่ใน RAM**
- OS โหลด page เมื่อถูกแตะผ่าน demand paging และบริหาร residency ด้วย page cache
- หลาย process ที่ map ไฟล์เดียวกันบนเครื่องเดียวกันใช้ physical page cache ร่วมกันได้
- ใน C API ค่า `MDB_val` ที่อ่านได้มักชี้เข้า mapped page โดยตรง จึงห้ามใช้ pointer ต่อหลัง transaction สิ้นสุดหรือหลัง operation ที่ทำให้ข้อมูลนั้นเปลี่ยน
- ขนาดสูงสุดที่ใช้งานจริงไม่ได้เป็นเลขตายตัว แต่ถูกจำกัดโดย map size, virtual address space, build/platform, filesystem และพื้นที่ disk

### Read workflow

![LMDB read workflow from transaction snapshot to B+ tree leaf and OS page fault handling](/assets/img/DS/LMDB/lmdb-read-path.svg)

Read transaction จับ snapshot transaction ID หนึ่งค่า จากนั้นใช้ root ที่อยู่ใน meta snapshot เดิมตลอดอายุ transaction ดังนั้น writer จะ commit root ใหม่ได้โดยไม่เปลี่ยนภาพที่ reader ตัวเดิมเห็น

- ถ้า page อยู่ใน RAM การเดิน tree คือ memory access
- ถ้า page ไม่ resident การแตะ mapped address จะเกิด page fault แล้ว OS โหลด page จาก storage
- การหา key ที่ไม่มีสิ้นสุดเมื่อค้นถึง leaf แล้วไม่พบ; ค่าใช้จ่ายจริงขึ้นกับ tree depth, cache state, key/value layout และ storage

> ใน Python binding (`py-lmdb`) `txn.get()` คืน `bytes` โดยปกติ จึงไม่ควรเรียกว่า zero-copy เสมอไป ต้องเปิด transaction ด้วย `buffers=True` หากต้องการ buffer ที่อ้าง mapped memory และต้องเลิกใช้ buffer ก่อน transaction สิ้นสุดหรือถูกแก้ไข

---

## 2. โครงสร้างไฟล์ (On-Disk Layout)

![LMDB on-disk layout: meta pages และ mixed page pool](/assets/img/DS/LMDB/lmdb-on-disk-layout.svg)

จุดสำคัญคือมีเพียง page 0 และ page 1 ที่เป็นตำแหน่งคงที่สำหรับ meta pages ส่วน page ตั้งแต่หมายเลข 2 เป็นต้นไปเป็น **mixed page pool** ไม่ได้แบ่ง Main DB, FreeDB หรือ overflow เป็นช่วงต่อกันแบบตายตัว

| ส่วน | หน้าที่ |
|---|---|
| **Meta page 0/1** | เก็บ format, page/map size, last page, transaction ID และ descriptor ของ Main DB กับ FreeDB; commit สลับใช้สองหน้า |
| **Branch page** | เก็บ separator keys และ child page numbers ของ B+ tree |
| **Leaf page** | เก็บ records; key/value เล็กอยู่ใน leaf ได้ |
| **Overflow page(s)** | เก็บ value ที่ไม่พอดีกับ leaf โดยใช้ page run ต่อเนื่อง |
| **FreeDB** | B+ tree ภายในที่ map transaction ID ไปยังรายการ page IDs สำหรับ free-space management |
| **Named DB** | B+ tree เพิ่มเติมใน environment เดียวกัน; descriptor ถูกเก็บเป็น record ใน Main DB |

Page size ถูกบันทึกใน metadata และมักเท่ากับ virtual-memory page size ของระบบ เช่น 4 KiB แต่ไม่ควร hard-code สมมติฐานนี้ในการอ่าน file format เอง

ตอนเปิด environment LMDB ตรวจ meta pages แล้วเลือก snapshot ที่ valid และใหม่กว่า การมี meta สองหน้าช่วยให้ commit รุ่นใหม่ไม่ต้อง overwrite meta snapshot เดียวที่ reader/การ recovery ต้องพึ่งอยู่

---

## 3. Transaction lifecycle และ concurrency

![LMDB transaction lifecycle for read-only and write transactions](/assets/img/DS/LMDB/lmdb-transaction-lifecycle.svg)

กฎสำคัญ:

- **ทุก operation อยู่ใน transaction** — รวมถึง read และ cursor scan
- มี read transactions พร้อมกันได้หลายตัว ภายใต้จำนวน reader slots ที่กำหนด
- มี active write transaction ได้ครั้งละหนึ่งตัวต่อ environment; writer อื่นรอ writer lock
- Reader ใช้ snapshot คงที่และไม่ถือ page-level read locks ระหว่าง traversal
- Writer กับ readers มักเดินพร้อมกันได้ เพราะ writer สร้าง page รุ่นใหม่แทนการแก้ page ที่ reader กำลังอ้าง
- Cursor และ mapped value มี lifetime ผูกกับ transaction
- เพื่อความปลอดภัยและ portability อย่าใช้ transaction/cursor ตัวเดียวพร้อมกันจากหลาย threads; write transaction ต้องอยู่กับ thread ที่สร้างมัน

ควรทำ read transaction ให้สั้น โดยเฉพาะ service ที่ทำงานนาน เพราะ reader ที่ค้างจะตรึง snapshot เก่าและชะลอการ reuse pages

---

## 4. B+ tree และ Copy-on-Write commit

LMDB เก็บ records ตามลำดับ key ใน B+ tree:

- branch nodes ชี้ไป child pages
- leaf nodes เก็บ records หรือ reference ไป overflow pages
- cursor ใช้โครงสร้างเรียงลำดับนี้ทำ range scan และ prefix scan ได้มีประสิทธิภาพ
- tree depth ขึ้นกับจำนวน records, ขนาด key/value, page size และ fill pattern จึงไม่ควรสรุปเป็นจำนวน page reads คงที่

### COW write workflow

![LMDB copy-on-write commit workflow](/assets/img/DS/LMDB/lmdb-cow-commit.svg)

เมื่อแก้ key หนึ่งตัว writer โดยสรุปจะ:

1. ล็อก writer และเริ่มจาก latest committed snapshot
2. เลือก page IDs ที่ปลอดภัยต่อการ reuse หรือขยาย file หากไม่มีพอ
3. copy และแก้ leaf เป้าหมาย; split หาก page ไม่พอ
4. copy parent path ที่ต้องเปลี่ยนไปจนถึง root
5. เขียน dirty pages และ flush ตาม durability mode
6. publish root/transaction ID ชุดใหม่ลง alternate meta page
7. ปล่อย writer lock; reader ใหม่เห็น snapshot ใหม่ ส่วน reader เก่ายังเห็น tree เดิม

LMDB จึงไม่ต้อง append WAL แล้ว replay ตอนเปิดฐานข้อมูล อย่างไรก็ตามคำว่า “crash-proof” จะถูกต้องก็ต่อเมื่อมองร่วมกับ default sync behavior, filesystem ordering และ storage ที่ทำตาม flush/barrier อย่างถูกต้อง การใช้ unsafe flags เปลี่ยน guarantee นี้โดยตรง

---

## 5. MVCC และการนำ page กลับมาใช้

![LMDB MVCC timeline and safe page reuse workflow](/assets/img/DS/LMDB/lmdb-mvcc-page-reuse.svg)

ตัวอย่างในภาพ:

- Reader A เริ่มที่ transaction 42 และยังอ้าง page `P5`
- Writer 43 สร้าง `P9` แทน `P5` แล้ว commit
- Reader ใหม่เห็น transaction 43 แต่ Reader A ยังอ่าน `P5` ได้
- Writer ตรวจ oldest active reader จาก reader table; ตราบใดที่ transaction 42 ยัง active จะนำ `P5` กลับมาใช้ไม่ได้
- เมื่อ Reader A จบ มันเพียงปล่อย reader slot — **reader ไม่ได้เขียน FreeDB เอง**
- write transaction ถัดไปจึงประเมินว่า page ปลอดภัย แล้วบันทึก/เลือก page IDs ผ่าน FreeDB เพื่อนำกลับมาใช้

ผลคือ readers ไม่ต้อง block writer บน data pages แต่ long-lived reader สามารถทำให้ file โต เพราะ writer ต้องเก็บ page versions เก่าไว้

---

## 6. FreeDB, file growth และ compact copy

FreeDB เป็น logical B+ tree อยู่ใน `data.mdb` เช่นเดียวกับ Main DB โดย records ใช้ transaction ID เป็น key และรายการ page IDs เป็น value เพื่อบอกว่า pages ชุดใดถูกปลดจาก snapshot รุ่นนั้น

พื้นที่ใน LMDB มีพฤติกรรมดังนี้:

1. COW ทำให้ page รุ่นเก่าหลุดจาก tree ใหม่
2. Writer เทียบอายุ page กับ oldest active reader
3. Page ที่ปลอดภัยถูกจัดการผ่าน FreeDB และเลือก reuse ก่อนขยาย high-water mark เมื่อทำได้
4. ถ้าพื้นที่ reusable ยังใช้ไม่ได้หรือไม่พอ file จะโต
5. การลบ records ไม่ทำให้ `data.mdb` หดทันที; พื้นที่กลายเป็น reusable ภายใน file

ดังนั้นคำว่า “ไม่ต้อง compaction” หมายถึง LMDB ไม่ต้องมี background compaction เพื่อให้ read path ทำงาน แต่ถ้าต้องการไฟล์ที่เล็กลง สามารถสร้าง **compact copy** ด้วย:

```bash
mdb_copy -c /path/to/source-env /path/to/compact-copy
```

`-c` คัดลอกเฉพาะ pages ของ current snapshot และละ pages ที่ free/unused ออก ควรเผื่อ disk สำหรับทั้งต้นฉบับและสำเนา และระวังว่าการ copy ขณะมี writer อาจยืดอายุ snapshot ทำให้ต้นฉบับโตชั่วคราว

สำหรับ backup ให้ใช้ `mdb_copy` หรือ environment-copy API ของ LMDB แทนการคัดลอกไฟล์แบบไม่ประสานขณะที่มี write activity

---

## 7. Durability modes: เร็วขึ้นแลกกับอะไร

ไม่มีตัวเลข throughput สากลสำหรับแต่ละ flag เพราะผลต่างขึ้นกับ transaction batching, filesystem, drive cache และ latency ของ sync แต่ guarantee ต่างกันชัดเจน:

| Mode / flag | พฤติกรรมโดยสรุป | ความเสี่ยงเมื่อเครื่อง/OS ล้ม |
|---|---|---|
| **Default** | sync data และ metadata ตาม commit protocol | ให้ full durability เมื่อ filesystem/hardware ทำตาม sync semantics |
| `MDB_NOMETASYNC` | flush data แต่ไม่ force meta page ทุก commit | database integrity ยังเป็นเป้าหมาย แต่ commit ล่าสุดอาจหาย |
| `MDB_NOSYNC` | ไม่ force dirty buffers ตอน commit | recent transactions อาจหาย; ความเสียหายขึ้นกับ filesystem และ flags อื่น |
| `MDB_WRITEMAP` | ใช้ writable mmap; ไม่ใช่ durability mode ด้วยตัวเอง | stray pointer สามารถทำลาย DB; ห้ามผสม process ที่เปิดแบบ writemap/ไม่ writemap |
| `MDB_MAPASYNC` | asynchronous map flush และใช้ร่วมกับ `MDB_WRITEMAP` | transaction ล่าสุดอาจหาย และมี corruption risk ตามที่ API เตือน |

แนวทางใช้งาน:

- ใช้ default ก่อน แล้ว benchmark ด้วย durability requirement จริง
- ใช้ unsafe flags เฉพาะข้อมูลที่ rebuild ได้หรือยอมรับการสูญเสียหลัง crash ได้
- อย่าเรียก `MDB_WRITEMAP` ว่าเร็วกว่าเสมอ; header ของ LMDB ระบุว่า DB ที่ใหญ่กว่า RAM อาจช้าลง และ mode นี้ลดการป้องกัน wild writes
- `MDB_NOLOCK` ไม่ได้แปลว่า “single process แล้วปลอดภัยอัตโนมัติ” ผู้เรียกต้องจัด single-writer และ reader safety เองทั้งหมด

---

## 8. Performance และ Transactions / sec

ตัวเลข throughput เคยถูกเอาออกตอนปรับบทความรอบก่อน เพราะตารางเดิมไม่ได้ระบุ source, hardware, transaction size และ durability mode ทำให้ดูเหมือนเป็นค่าที่ LMDB ทำได้เสมอ รอบนี้นำกลับมาโดยใช้ผลทดสอบที่ตรวจสอบย้อนกลับได้ พร้อมแยก `ops/sec`, `entries/sec` และ `transactions/sec` ให้ชัดเจน

ประสิทธิภาพของ storage engine เปลี่ยนมากตาม workload จึงไม่ควรใช้ตัวเลขจากเครื่องอื่นเป็นคำตอบสุดท้าย จุดแข็งเชิงสถาปัตยกรรมของ LMDB คือ read path สั้น, ไม่มี cache copy ชั้นที่สอง, ordered scan และไม่มี background compaction มาแย่ง I/O ส่วนข้อจำกัดหลักคือ writer serialization, COW/page splits, commit sync และ file growth เมื่อ readers ค้าง

### Historical benchmark ที่ตรวจสอบที่มาได้

ตารางต่อไปนี้มาจาก [Symas Database Microbenchmarks (กันยายน 2012)](http://www.lmdb.tech/bench/microbench/) จึงควรอ่านเป็น **ข้อมูลย้อนหลังเพื่ออธิบายพฤติกรรม** ไม่ใช่คำรับรอง performance บนเครื่องปัจจุบัน เงื่อนไข baseline คือ:

- Dell Precision M4400, Core 2 Extreme Q9300 2.53 GHz, RAM 8 GB และ Ubuntu 12.04/kernel 3.5
- key 16 bytes, value 100 bytes และรายงานค่ามัธยฐานจาก 3 รอบ
- รันบน `tmpfs` เพื่อลดผลของ storage I/O
- write แบบ asynchronous; ฝั่ง LMDB ใช้ `MDB_NOSYNC` และ benchmark รุ่นนี้เปิด `MDB_WRITEMAP`

| Workload | LMDB | RocksDB | LevelDB | SQLite3 | หน่วยที่ source รายงาน |
|---|---:|---:|---:|---:|---|
| Sequential read | 14,705,882 | —¹ | 4,587,156 | 313,283 | ops/sec |
| Random read | 751,315 | —¹ | 174,246 | 82,994 | ops/sec |
| Sequential write | 461,255 | —¹ | 498,753 | 56,693 | ops/sec |
| Random write | 240,154 | —¹ | 317,662 | 42,199 | ops/sec |
| Batch sequential write | 2,481,390 | —¹ | 677,048 | 109,302 | entries/sec |
| Batch random write | 294,898 | —¹ | 432,152 | 58,432 | entries/sec |

> ¹ รายงานปี 2012 ไม่ได้ทดสอบ RocksDB จึงไม่ควรนำตัวเลขจาก benchmark คนละปีและคนละ workload มาเสียบในช่องเดียวกัน ตารางถัดไปเป็นการเปรียบเทียบ LMDB กับ RocksDB ที่รันอยู่ใน test เดียวกัน

### LMDB vs RocksDB ใน benchmark เดียวกัน (2014)

[Symas In-Memory Microbenchmark (มิถุนายน 2014)](http://www.lmdb.tech/bench/inmem/) มี RocksDB อยู่ในการทดสอบเดียวกับ LMDB โดยใช้ key 16 bytes, value 100 bytes, ปิด compression, สุ่มอ่านและ update records เดิม พร้อม reader หลาย threads และ writer หนึ่งตัว ข้อมูลอยู่บน `tmpfs` และมีขนาดพอดีกับ RAM

| Concurrent workload | LMDB | RocksDB | หน่วยที่ source รายงาน |
|---|---:|---:|---|
| 20M records, 4 reader threads | **1,449,709** | **91,544** | reads/sec รวมทุก readers |
| 20M records, 1 writer | **10,224** | **10,233** | writes/sec — จำกัดเพดานไว้ที่ 10,240 |
| 100M records, 16 reader threads | **2,486,800** | **129,397** | reads/sec รวมทุก readers |
| 100M records, 1 writer | **10,230** | **10,232** | writes/sec — จำกัดเพดานไว้ที่ 10,240 |

ข้อควรระวังในการอ่านตาราง RocksDB:

- writer ถูก rate-limit ไว้ไม่เกินประมาณ 10,240 writes/sec ดังนั้นแถว write บอกเพียงว่าแต่ละ engine รักษาอัตราที่กำหนดไว้ได้หรือไม่ **ไม่ได้วัด write throughput สูงสุด**
- `writes/sec` ในรายงานนี้ไม่ควรถูกเรียกเป็น durable `transactions/sec` ข้าม engine เพราะ transaction boundary, WAL/sync และ durability configuration ไม่ได้มีความหมายเหมือนกัน
- นี่คือ historical benchmark ที่ Symas เผยแพร่ในปี 2014 ด้วย LMDB/RocksDB เวอร์ชันและ hardware ในยุคนั้น ไม่ใช่ผลรับประกันของเวอร์ชันปัจจุบัน

### แปลงเป็น Transactions / sec อย่างถูกต้อง

[source code ของ benchmark ฝั่ง LMDB](http://www.lmdb.tech/bench/microbench/db_bench_mdb.cc) ทำให้ตีความตัวเลขได้ดังนี้:

- **Read:** benchmark เปิด read transaction หนึ่งตัวแล้วอ่านหลาย records ดังนั้น `read ops/sec` ในตาราง **ไม่ใช่** `read transactions/sec`
- **Single write:** เปิดและ commit write transaction ใหม่ทุก 1 record ดังนั้น `write ops/sec` เท่ากับ `write transactions/sec` สำหรับ test นี้
- **Batch write:** หนึ่ง transaction มี 1,000 records ดังนั้นต้องหาร `entries/sec` ด้วย 1,000

| LMDB workload | Records / transaction | Throughput ที่รายงาน | Transactions / sec |
|---|---:|---:|---:|
| Sequential write, async `MDB_NOSYNC` | 1 | 461,255 ops/sec | **461,255 tx/sec** |
| Random write, async `MDB_NOSYNC` | 1 | 240,154 ops/sec | **240,154 tx/sec** |
| Batch sequential write, async `MDB_NOSYNC` | 1,000 | 2,481,390 entries/sec | **2,481.390 tx/sec** |
| Batch random write, async `MDB_NOSYNC` | 1,000 | 294,898 entries/sec | **294.898 tx/sec** |

ตัวอย่างการคำนวณ batch:

```text
Sequential: 2,481,390 entries/sec ÷ 1,000 entries/transaction
          = 2,481.390 transactions/sec

Random:      294,898 entries/sec ÷ 1,000 entries/transaction
          =   294.898 transactions/sec
```

จะเห็นว่า `entries/sec` สูงขึ้นจากการ batch แต่ `transactions/sec` ไม่ได้สูงตาม เพราะหนึ่ง transaction ทำงานมากขึ้น ตัวเลขสองหน่วยนี้ตอบคนละคำถาม

### Durable commit rate บน SSD ใน benchmark เดียวกัน

เมื่อทดสอบ single-record transactions บน Crucial M4 SSD 512 GB กับ reiserfs โดยเปิด synchronous durability ผลของ LMDB เป็นดังนี้ ตัวเลขนี้ใช้หนึ่ง record ต่อหนึ่ง transaction จึงอ่าน `ops/sec` เป็น `transactions/sec` ได้สำหรับ test นี้:

| Mode | Sequential write | Random write |
|---|---:|---:|
| Default full sync | **149 tx/sec** | **148 tx/sec** |
| `MDB_NOMETASYNC` | **328 tx/sec** | **322 tx/sec** |

ความต่างจากตัวเลข `MDB_NOSYNC` บน `tmpfs` แสดงให้เห็นว่า latency ของ durable sync และ storage มีผลต่อ commit rate มากเพียงใด และเป็นเหตุผลว่าทำไมตัวเลข Transaction / Sec ที่ไม่ระบุ durability mode จึงเทียบกันไม่ได้

> ตัวเลขทั้งหมดข้างบนเป็น historical microbenchmark จากปี 2012 บน software/hardware รุ่นเก่า ไม่ควรใช้ capacity planning โดยตรง ให้ใช้เพื่อเข้าใจหน่วยและ trade-off แล้ว benchmark ซ้ำบน workload, transaction size, filesystem, storage และ flags ที่จะใช้จริง

### Benchmark workflow ที่เทียบได้จริง

1. กำหนด key/value size และ distribution ให้เหมือน production
2. ทดสอบ dataset ทั้งที่เล็กกว่าและใหญ่กว่า RAM
3. ระบุ read/write/scan ratio และ hit/miss ratio
4. ใช้ transaction batch size และ sync flags เดียวกับ production
5. แยก warm-cache, cold-cache และ restart tests
6. วัด throughput พร้อม p50/p95/p99/p99.9 latency
7. วัด disk bytes written, file growth และเวลาที่ reader อยู่ใน transaction
8. ทดสอบ crash/restart บน filesystem และ storage รุ่นเดียวกับที่จะ deploy

`MDB_APPEND`/`append=True` ช่วยกรณี ingest ที่ keys เรียงถูกต้องอยู่แล้ว แต่ถ้าส่ง key ผิดลำดับ operation จะไม่ทำงานตามเงื่อนไขของ append optimization

---

## 9. LMDB vs RocksDB: คนละ trade-off

![LMDB B+ tree workflow compared with RocksDB LSM workflow](/assets/img/DS/LMDB/lmdb-vs-rocksdb-workflow.svg)

RocksDB เป็น LSM engine: write โดยทั่วไปเข้า WAL และ memtable ก่อน จากนั้น flush เป็น SST files และมี background compaction ส่วน read ตรวจ memory structures, cache/index/filter และ SST levels ที่เกี่ยวข้อง การใช้ Bloom filters และ block cache ทำให้ไม่ควรเหมารวมว่า read miss ต้องอ่านทุก level หรือทำ I/O จำนวนตายตัว

| มิติ | LMDB | RocksDB |
|---|---|---|
| โครงสร้างหลัก | Copy-on-write B+ tree | LSM tree + SST files |
| Write concurrency | หนึ่ง active write transaction | รองรับ concurrent client writes และ batching ภายใน engine |
| Read cache | OS page cache ผ่าน mmap | block cache ที่กำหนดได้; อาจใช้ OS cache ร่วมด้วย |
| Background work | ไม่มี flush/compaction workers ของ engine | flush และ compaction เป็นงานหลักของระบบ |
| Read snapshot | MVCC root snapshot | sequence-number snapshot |
| Recovery | เลือก valid committed meta snapshot; ไม่มี WAL replay | อาจ replay WAL และใช้ manifest/version metadata |
| Space reclaim | FreeDB reuse; file ไม่หดเอง | compaction ทิ้ง obsolete entries/files |
| Ordered scan | B+ tree ตาม key order | merged iteration จาก memtables/SST levels |
| Multi-process | ออกแบบให้หลาย process เปิด local environment ร่วมกัน | primary open ปกติมี lock; มี read-only/secondary modes เฉพาะ |
| Feature surface | API เล็กและตรงไปตรงมา | column families, merge operators, filters และ tuning จำนวนมาก |

ไม่มีผู้ชนะสากล: LMDB มักเหมาะเมื่อ read/scan และ simplicity สำคัญ ส่วน RocksDB มักเหมาะเมื่อ write ingestion, feature set และการกระจายงานเบื้องหลังสำคัญ ต้อง benchmark บน workload จริงเสมอ

---

## 10. เลือก LMDB เมื่อไร

### เหมาะเมื่อ

- embedded/local key-value store ที่ต้องการ ACID transactions
- read-heavy หรือ ordered range scans
- หลาย process ต้องแชร์ฐานข้อมูลบนเครื่องเดียวกัน
- ต้องการ snapshot reads และ operational surface ที่เล็ก
- รับข้อจำกัด one-active-writer ได้
- ต้องการหลีกเลี่ยง background compaction และ WAL recovery

### ควรพิจารณาทางเลือกเมื่อ

- ต้องการ write transactions หลายตัวทำงานพร้อมกันจริง ๆ
- workload มี sustained write rate ที่ writer เดียวรับไม่ไหว
- ต้องการ remote/distributed database, replication หรือ network API ในตัว
- ต้องการ column families/merge/TTL และ ecosystem ของ LSM engine
- ไม่สามารถกำหนด map-size headroom หรือเฝ้าระวัง long readers/disk growth ได้

`libmdbx` เป็น descendant/fork ที่มี API และ engineering choices ต่างจาก LMDB แต่ **ยัง serialize writers ด้วย writer mutex** ไม่ใช่คำตอบแบบ multi-writer โดยอัตโนมัติ ควรประเมิน compatibility, format, license และ benchmark แยกต่างหาก

---

## 11. Python usage ที่ถูกต้อง

```python
from pathlib import Path
import lmdb

path = Path("mydb")
path.mkdir(exist_ok=True)

# map_size คือเพดาน virtual mapping; เลือกตาม workload/platform และ monitor การใช้งาน
# max_dbs ต้องเผื่อ named databases และให้ opener ตัวแรกกำหนดอย่างสอดคล้องกัน
env = lmdb.open(path.as_posix(), map_size=8 * 1024**3, max_dbs=4)

# เปิด named DB handle ครั้งเดียวแล้ว reuse
with env.begin(write=True) as txn:
    users = env.open_db(b"users", txn=txn, create=True)

# Write transaction: context manager commit เมื่อออกโดยไม่มี exception
with env.begin(write=True, db=users) as txn:
    txn.put(b"user:0001", b'{"name":"Alice"}')
    txn.put(b"user:0002", b'{"name":"Bob"}')

# Default read คืน bytes (copy semantics ของ Python binding)
with env.begin(db=users) as txn:
    value = txn.get(b"user:0001")
    if value is not None:
        print(value.decode("utf-8"))

# Zero-copy-style buffer: ใช้ให้เสร็จภายใน transaction นี้เท่านั้น
with env.begin(db=users, buffers=True) as txn:
    value_buffer = txn.get(b"user:0001")
    if value_buffer is not None:
        consume_now = bytes(value_buffer)  # copy หากต้องเก็บหลัง transaction จบ

# Ordered range scan
with env.begin(db=users) as txn:
    cursor = txn.cursor()
    if cursor.set_range(b"user:0001"):
        for key, value in cursor:
            if not key.startswith(b"user:"):
                break
            print(key, value)

# Append optimization: keys ต้องมาแบบ strict sorted order ตาม comparator
with env.begin(write=True, db=users) as txn:
    for i in range(3, 1000):
        key = f"user:{i:04d}".encode()
        txn.put(key, b"{}", append=True)

env.close()
```

ข้อควรระวังของ binding:

- อย่าเก็บ buffer, cursor หรือ transaction ข้าม lifetime ที่ API อนุญาต
- ปิด write transaction ด้วย context manager หรือ `commit()`/`abort()` ให้แน่นอน
- เมื่อเจอ `lmdb.MapFullError` ให้หยุด writes และทำ coordinated resize; `Environment.set_mapsize()` ต้องไม่มี active transactions ใน process และการ resize หลาย process ต้องออกแบบ coordination เอง
- อย่าเปิด environment เดียวกันซ้ำหลาย handle ใน process เดียวโดยไม่มีเหตุผล; share environment handle ตามรูปแบบที่ binding รองรับ

---

## 12. Configuration ที่ควรตัดสินใจจาก workload

### `map_size`

- เป็นเพดาน virtual address mapping และขนาดสูงสุดที่ environment โตได้ใน configuration นั้น
- ไม่ได้จอง RAM ทั้งก้อน แต่ address-space limit ยังสำคัญ โดยเฉพาะ 32-bit
- อย่าใช้ค่า 1 TB/8 TB เป็นสูตรสากล; เผื่อ headroom จาก live data, COW churn, long readers, backup และ growth rate
- monitor `last_pgno`, filesystem free space และ `MapFullError`
- วางขั้นตอน resize ให้ทุก process เห็น map size ที่สอดคล้องกัน

### `max_readers`

- กำหนดจำนวน reader slots ใน lock table ไม่ใช่จำนวน keys หรือ requests
- opener ตัวแรกของ environment เป็นผู้กำหนดขนาด reader table ที่ใช้งานร่วมกัน
- นับ peak concurrent read transactions จริง รวมทุก threads/processes แล้วเผื่อ margin
- ตรวจและเก็บ stale slots ด้วย `mdb_reader_check()` หรือเครื่องมือ binding ที่เทียบเท่า

### `max_dbs`

- ต้องตั้งมากกว่า 0 เมื่อใช้ named DBs และเผื่อจำนวน handles ที่ต้องเปิด
- opener ตัวแรกต้องกำหนดค่าให้เหมาะสม; process อื่นควรใช้ configuration ที่เข้ากัน
- named DBs แชร์ transaction, map size และไฟล์ `data.mdb` เดียวกัน ไม่ใช่ isolation boundary แบบแยกไฟล์

### Transaction sizing

- batch หลาย writes ใน transaction เดียวช่วย amortize commit/sync cost
- transaction ใหญ่มากใช้ dirty pages และทำให้ writer lock ถูกถือนาน
- เลือก batch จาก p99 latency, memory, crash-loss boundary และ throughput ที่วัดจริง

### Flags อื่น

- `MDB_RDONLY` ไม่เขียน data pages แต่โดยปกติยังใช้/แก้ lock file เพื่อ reader tracking; กรณี filesystem เป็น read-only มีพฤติกรรม no-lock ตามเงื่อนไขที่ API ระบุ
- `MDB_NORDAHEAD` อาจช่วย random-read workload เมื่อ DB ใหญ่กว่า RAM แต่ควร benchmark
- `MDB_NOSUBDIR` เปลี่ยน path layout ไม่ได้เปลี่ยน storage semantics
- `MDB_NOLOCK` ใช้ได้เฉพาะเมื่อ application ทำ locking/reader safety ที่ LMDB ต้องการครบเอง

---

## 13. Operations checklist

### ก่อน production

- [ ] ใช้ local filesystem ที่ mmap และ locking semantics เชื่อถือได้; หลีกเลี่ยง network filesystem
- [ ] ทดสอบ crash/power-loss ด้วย sync flags จริง
- [ ] ตั้ง alert ทั้ง map utilization และ disk free space
- [ ] กำหนด max readers/max DBs ให้ opener ทุก process สอดคล้องกัน
- [ ] จำกัดอายุ read transaction ใน request/worker paths
- [ ] แยก metric ระหว่าง active readers, stale readers และ writer wait time

### ระหว่าง operation

```bash
# ดูสถิติ environment / DB
mdb_stat -ea /path/to/env

# แสดง reader table
mdb_stat -r /path/to/env

# สร้าง consistent compact copy
mdb_copy -c /path/to/env /path/to/backup-env
```

- ทำ backup restore drill ไม่ใช่แค่ตรวจว่าคำสั่ง copy สำเร็จ
- หาก file โตผิดปกติ ให้หา long-lived/stale reader ก่อนสรุปว่า leak
- compact copy เป็น operation แยก ไม่ใช่งาน maintenance ที่ต้องรันตาม schedule เสมอ
- อย่าแก้/ตัด `data.mdb` ด้วย filesystem tools เพื่อหวังลดขนาด

---

## 14. License — OpenLDAP Public License 2.8

LMDB แจกภายใต้ OpenLDAP Public License 2.8 ซึ่งเป็น permissive license โดยเงื่อนไขหลักในข้อความ license คือ:

- source redistribution ต้องคง copyright notices, เงื่อนไข และ disclaimer
- binary redistribution ต้องทำซ้ำ notices/เงื่อนไข/disclaimer ใน documentation หรือ materials ที่ให้มาด้วย
- ต้องแจกสำเนา license แบบ verbatim
- ห้ามใช้ชื่อผู้เขียนหรือ copyright holders เพื่อ endorse/promote derived products โดยไม่มี written permission

โดยทั่วไป license นี้รองรับ commercial และ closed-source redistribution เมื่อปฏิบัติตามเงื่อนไขข้างต้น แต่ข้อความนี้เป็นสรุปทางเทคนิค **ไม่ใช่คำแนะนำทางกฎหมาย** ควรให้ทีมกฎหมายตรวจ license text ฉบับจริงสำหรับการแจกจ่ายผลิตภัณฑ์

---

## 15. Caveats ที่จำให้ขึ้นใจ

- one active writer เป็น invariant หลัก ไม่ใช่ tuning bug
- long-lived readers ทำให้ page reuse ช้าและ file โต
- delete ทำให้พื้นที่ reusable แต่ไม่ทำให้ไฟล์หดอัตโนมัติ
- mapped pointers/buffers มี transaction lifetime
- map size และ disk free space เป็นคนละ limit และต้อง monitor ทั้งคู่
- unsafe sync flags เปลี่ยน durability guarantee
- `MDB_WRITEMAP` เพิ่ม blast radius ของ memory corruption
- อย่าใช้บน network filesystem โดยสมมติว่า mmap/locking เหมือน local disk
- อย่าสมมติว่า file copy portable ข้ามทุก architecture, endianness, page-size และ build option; ตรวจ compatibility ก่อน และใช้ logical export/import เมื่อ environment ไม่ compatible

---

## References

- [Symas LMDB benchmark index](http://www.lmdb.tech/bench/)
- [Symas Database Microbenchmarks (2012)](http://www.lmdb.tech/bench/microbench/)
- [LMDB benchmark source (`db_bench_mdb.cc`)](http://www.lmdb.tech/bench/microbench/db_bench_mdb.cc)
- [Symas In-Memory Microbenchmark with RocksDB (2014)](http://www.lmdb.tech/bench/inmem/)
- [Official LMDB API header (`lmdb.h`)](https://raw.githubusercontent.com/LMDB/lmdb/mdb.master/libraries/liblmdb/lmdb.h)
- [Official LMDB implementation (`mdb.c`)](https://raw.githubusercontent.com/LMDB/lmdb/mdb.master/libraries/liblmdb/mdb.c)
- [Official LMDB introduction](https://raw.githubusercontent.com/LMDB/lmdb/mdb.master/libraries/liblmdb/intro.doc)
- [OpenLDAP Public License 2.8](https://raw.githubusercontent.com/LMDB/lmdb/mdb.master/libraries/liblmdb/LICENSE)
- [LMDB `mdb_copy(1)` manual](https://raw.githubusercontent.com/LMDB/lmdb/mdb.master/libraries/liblmdb/mdb_copy.1)
- [py-lmdb documentation](https://lmdb.readthedocs.io/en/release/)
- [RocksDB overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)
- [RocksDB write stalls](https://github.com/facebook/rocksdb/wiki/Write-Stalls)
- [RocksDB block cache](https://github.com/facebook/rocksdb/wiki/Block-Cache)
- [libmdbx README](https://github.com/erthink/libmdbx)
- Related: [[RocksDB]], [[LevelDB]], [[Berkeley DB]]
