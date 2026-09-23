# 021 — Zero Copy เร็วได้ แต่ layout ต้องจริง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 334-339 · [ต้นฉบับ](../original/post.md) · ภาพ: ![bytemuck bincode](../original/image-33.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์พูดถึงเบื้องหลังความเร็วด้วย Rust, Bytemuck และ Bincode พร้อมเตือน Python เรื่อง alignment และ little endian ภาพเทียบ Bytemuck ในบทบาท zero-copy memory casting กับ Bincode ในบทบาท binary serialization แต่คำอธิบายว่า Bincode ต้อง copy เสมอเป็นการย่อมากเกินไป สาระสำคัญคือ “เร็ว” มาจากการลดการแปลงข้อมูล แต่การลด copy ต้องแลกกับข้อกำหนดเรื่อง memory layout

เอกสาร bytemuck ระบุชัดว่า cast บางชนิดอาจ fail จาก alignment เช่น `cast_ref::<[u8; 4], u32>` ถ้า reference ไม่ align 4 และฟังก์ชันจำนวนมากถูก guard ด้วย trait `Pod` ([docs.rs/bytemuck](https://docs.rs/bytemuck/latest/bytemuck/)). หน้า `Pod` บอกว่าเป็น unsafe marker สำหรับ plain old data, ผลการ cast bytes ขึ้นกับ endian, type ต้องไม่มี padding/uninit bytes, field ต้องเป็น `Pod`, และควรเป็น `repr(C)` หรือ `repr(transparent)` ([Pod docs](https://docs.rs/bytemuck/latest/bytemuck/trait.Pod.html)).

ฝั่ง Bincode เป็น serialization ที่ encode/decode ตามรูปแบบกำหนดไว้ API รุ่น 2.0.1 มีทั้ง decode ปกติและ borrowed decode รวมถึงเขียนลง buffer ที่จองไว้แล้ว จึงไม่ควรสรุปว่าต้อง allocation หรือ copy ทุก field เสมอ ([เอกสาร bincode 2.0.1](https://docs.rs/bincode/2.0.1/bincode/)). ผู้ส่งกับผู้รับยังต้องตกลงชนิดข้อมูล ลำดับ field และ config ให้ตรงกัน และต้องออกแบบ version ของ schema เอง การมี serializer ไม่ได้ให้ schema evolution หรือความเข้ากันได้ข้ามภาษาโดยอัตโนมัติ

ตัวอย่างเรียนรู้: สร้าง struct `#[repr(C)] struct Vec2 { x: f32, y: f32 }` แล้วทดลอง `bytemuck::bytes_of(&v)` จากนั้นลองเพิ่ม `u8` คั่นกลางแล้ว derive `Pod` จะเห็นว่าปัญหา padding โผล่เร็วมาก ต่อด้วย encode struct เดียวกันด้วย bincode แล้วดูว่าไฟล์อ่านข้ามภาษา/ข้ามเครื่องง่ายกว่า raw memory dump อย่างไร

ข้อควรระวัง: Rust ownership ช่วยจัดการ memory โดยไม่ต้อง GC ตาม Rust Book แต่ไม่ได้ทำให้ unsafe cast ถูกต้องเอง กฎ ownership บอกเรื่อง owner/drop ส่วน bytemuck ต้องการ invariant อีกชุดเรื่อง bit pattern, alignment และ layout ([Rust Book: ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)).

คำถามฝึก: ข้อมูลชนิดไหนในเกมควรใช้ raw POD cast และชนิดไหนควร serialize แบบมี schema?


หมายเหตุเวอร์ชันที่ตรวจเมื่อ 2026-09-20: หน้า bincode latest/3.0.0 ประกาศยุติการดูแลและระบุว่ารุ่นดังกล่าวใส่ compile error เพื่อแจ้งสถานะ ตัวอย่างแนวคิดในบทนี้จึงอ้าง API รุ่น 2.0.1 ไม่ใช่คำแนะนำให้ติดตั้ง latest ([ประกาศจากแพ็กเกจ](https://docs.rs/crate/bincode/3.0.0)).

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** zero-copy ใน Rust ต้องอาศัยสัญญาอะไรนอกเหนือจาก ownership? แหล่งใหม่คือ Rustonomicon เรื่อง alternative representations และ Rust Reference เรื่อง type layout. Rustonomicon อธิบายว่า `repr(C)` ตั้งใจให้ order, size และ alignment ของ field เป็นแบบที่ C/C++ คาดหวัง และจำเป็นต่อการ reinterpret layout อย่างระมัดระวัง แต่ยังมีข้อยกเว้นเช่น ZST, DST pointer, enum และ interaction กับ layout แปลก ๆ [Rustonomicon reprs](https://doc.rust-lang.org/nomicon/other-reprs.html). Rust Reference เป็นแหล่งหลักสำหรับกติกา layout ที่ compiler รับประกัน [Rust Reference: type layout](https://doc.rust-lang.org/reference/type-layout.html).

**กลไกที่เกี่ยวกับโพสต์:** Bytemuck เร็วเพราะอ่าน bytes เป็นชนิดข้อมูลโดยไม่ decode format ทีละ field แต่ความเร็วนี้ซื้อด้วย invariant: alignment ถูก, ไม่มี padding/uninit ที่ถูกอ่านผิด, bit pattern ถูกต้อง และ endian ตรงกับที่ออกแบบไว้ Bincode อยู่คนละแกนเพราะ encode/decode ตาม format จึงช่วยพกข้อมูลข้าม process/version ได้ง่ายกว่า raw memory dump แม้จะมี overhead เพิ่ม

**ผลเชิงปฏิบัติ:** ถ้าจะส่ง latent/NPC state ระหว่าง Rust, WASM, Unity หรือไฟล์ binary ให้แยกชนิดข้อมูลเป็นสองกลุ่ม กลุ่ม hot path ภายใน process ใช้ POD layout แบบคุมเองได้ ส่วนข้อมูลข้าม version/network ใช้ serializer พร้อม schema/version การเขียนว่า “zero-copy” ใน benchmark ต้องระบุว่าข้าม boundary ไหน: slice ใน process, mmap file, network buffer หรือ FFI

**แบบฝึก:** สร้าง `#[repr(C)] Vec2 { x: f32, y: f32 }` แล้ววัด `bytemuck::cast_slice` เทียบกับ bincode decode จาก buffer เดิม จากนั้นเพิ่ม field `u8 flag` และเช็กขนาด/alignment ด้วย `std::mem::size_of/align_of` Caveat คือ `repr(C)` ไม่ได้ทำให้ type ทุกชนิด FFI-safe และ `repr(packed)` อาจลด padding แต่ทำให้ reference ไป field เกิดปัญหา alignment ได้
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 020](020-latent-action-factorization.md) · [โพสต์ 022 →](022-jacobian-space-not-consciousness.md)

หัวข้อที่เกี่ยวข้อง: [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
