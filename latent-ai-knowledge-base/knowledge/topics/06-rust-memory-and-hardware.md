# หัวข้อ 06 — Rust, memory layout, SIMD และ CPU/GPU runtime

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

สังเคราะห์หลังสกัดโพสต์แต่ละอันครบ · วันที่ 2026-09-20 · [กลับสารบัญ](../README.md)

## โพสต์ที่นำมาประกอบ

| โพสต์ | สิ่งที่เพิ่มให้หัวข้อนี้ |
|---|---|
| [010](../010-rust-latent-space-game-world-recap.md) | แชร์ข้อมูลระหว่างเกม/runtime และงบการคำนวณ |
| [011](../011-historical-state-ternary-proof.md) | การแทนค่า ternary และขอบเขตของ hardware proof |
| [018](../018-tokenizer-throughput-frame-budget.md) | แยก tokenizer hot path จาก game tick |
| [021](../021-rust-bytemuck-bincode-layout.md) | memory casting, serialization, alignment และ endian |
| [026](../026-mux-ahla-tpass-lattice.md) | ลดงานก่อนลงมือเร่ง kernel |
| [027](../027-latent-first-deterministic.md) | determinism, allocation และความเหมาะสมของงาน |
| [038](../038-go-puct-rust-wasm-simd.md) | นำ kernel เดียวกันไปใช้ผ่าน WASM |
| [040](../040-kimi-mla-muon-rust-training.md) | แบ่งหน้าที่ฝึกและใช้งานระหว่างสองเครื่อง |
| [043](../043-rust-simd-on-gpu.md) | ความต่างของ SIMD กับ GPU SIMT |
| [044](../044-cpu-simd-gpu-crossover.md) | จุดที่ GPU เริ่มคุ้มต้นทุน |
| [048](../048-vllm-katgpt-rs-benchmarking.md) | คอขวด runtime และ cache ใน serving |
| [049](../049-apple-silicon-local-inference.md) | runtime เฉพาะโมเดลบน Apple Silicon |
| [052](../052-llama-cpp-vllm-bragging-gate.md) | เกณฑ์ยอมรับการปรับประสิทธิภาพ |

## บทเรียนร่วม

โพสต์กลุ่มนี้ชี้วิธีลดต้นทุนคนละชั้น: ลดงานที่ไม่จำเป็น ลดการย้ายข้อมูล เพิ่มความขนาน และจัด runtime ให้ตรงกับโมเดล การเขียนด้วย Rust เป็นเครื่องมือหนึ่งในการควบคุมรายละเอียดเหล่านี้ แต่ต้องระบุว่าการเปลี่ยนใดเป็นสาเหตุของผลที่วัดได้

## เรียงปัญหาก่อนเลือกเครื่องมือ

| ชั้น | คำถามที่ต้องตอบ | ตัวอย่างวิธีแก้ |
|---|---|---|
| Algorithm | คำนวณซ้ำหรือมองทุกคู่โดยไม่จำเป็นหรือไม่ | cache, spatial partition, prune |
| Data | ค่าที่ใช้ติดกันอยู่ใกล้กันใน memory หรือไม่ | จัด layout, ใช้ buffer ซ้ำ, ลด copy |
| Kernel | มี operation เดียวทำกับข้อมูลหลายตัวหรือไม่ | vectorize, SIMD, fuse operation |
| Scheduling | งานแต่ละครั้งใหญ่พอและรอกันตรงไหน | batch, overlap, ลด synchronization |
| Hardware | bottleneck คือ compute, bandwidth หรือ launch | เลือก CPU/GPU ตาม phase |

นี่เป็นกรอบสังเคราะห์เพื่อใช้อ่าน [026](../026-mux-ahla-tpass-lattice.md), [043](../043-rust-simd-on-gpu.md), [044](../044-cpu-simd-gpu-crossover.md) และ [049](../049-apple-silicon-local-inference.md) ร่วมกัน งานที่ตัดการคำนวณออกได้อาจประหยัดกว่าการทำงานเดิมให้เร็วขึ้น

## Zero-copy, serialization และ shared memory

Zero-copy บอกว่าบางขั้นไม่สร้างสำเนาข้อมูล ส่วน serialization บอกว่าแปลงข้อมูลตามรูปแบบข้อตกลง ทั้งสองคำจึงอยู่คนละแกน และ serializer บางแบบก็คืน reference ที่ยืมข้อมูลจาก buffer ได้

[021](../021-rust-bytemuck-bincode-layout.md) อธิบายว่าการ cast bytes ต้องตรวจ layout/alignment/bit pattern ต่างจากการ decode ตาม format ส่วน [010](../010-rust-latent-space-game-world-recap.md) เพิ่มปัญหาอายุข้อมูลและขอบเขต Rust/Unity/WASM การแชร์ memory ไม่ลบต้นทุนอ่านข้อมูล การแย่งใช้ หรือ cache miss

ข้อเสนอสำหรับแบบฝึก: แทน NPC เป็นข้อมูลหลายตัว แล้วเทียบการเก็บแต่ละตัวครบทุก field กับการเก็บ field เดียวของทุกตัวติดกัน เลือก workload ที่อ่านเฉพาะตำแหน่ง เพื่อดูว่า layout มีผลอย่างไร จากนั้นเปลี่ยน workload ให้ใช้ทุก field และดูว่าข้อได้เปรียบยังอยู่หรือไม่

## ตัวอย่างคำนวณจุดคุ้ม GPU

สมมติ CPU ทำได้ 20 elements/µs, GPU ทำได้ 200 elements/µs แต่มีต้นทุนรวมตอนเริ่ม 30 µs:

~~~text
T_CPU = N/20
T_GPU = 30 + N/200
จุดที่เท่ากัน: N/20 = 30 + N/200 → N ≈ 667
~~~

ตัวเลขนี้สร้างขึ้นเพื่อสอน cost model เมื่อเพิ่มต้นทุนส่งข้อมูล หรือเก็บข้อมูลบน GPU ไว้อยู่แล้ว จุดคุ้มย่อมเปลี่ยน จึงไม่ย้ายเลข 128k จาก [044](../044-cpu-simd-gpu-crossover.md) มาใช้เป็นค่าคงที่กับทุกงาน

SIMD ของ CPU กับ SIMT ของ GPU ยังมีการจัด thread, register และการแยกเส้นทางควบคุมต่างกัน การใช้ชนิดข้อมูลชื่อเดียวไม่ทำให้ compiler ส่งไป GPU อัตโนมัติ ดูหลักฐานและข้อจำกัดใน [043](../043-rust-simd-on-gpu.md)

## จากการเร่งจุดเล็กไปสู่ทั้งระบบ

[049](../049-apple-silicon-local-inference.md) เป็นตัวอย่างการ specialize runtime ตามโมเดลและ phase ส่วน [040](../040-kimi-mla-muon-rust-training.md) เป็นการแบ่งบทบาทเครื่อง การเปลี่ยนสองเรื่องนี้พร้อมกันต้องวัดเวลาส่ง checkpoint และคุณภาพด้วย จึงจะทราบว่าเวลาที่ประหยัดใน kernel ถูกใช้ไปที่อื่นหรือไม่

ลำดับเรียนที่แนะนำ: 021 → 043 → 044 → 049 → 052 จากนั้นใช้ [หัวข้อ benchmark](08-performance-and-benchmarks.md) กำหนดเกณฑ์ยอมรับผลก่อนปรับครั้งต่อไป ขนาดโมเดลเล็กลง จำนวน allocation ลด และเวลาใช้งานลด เป็นผลที่อาจเกิดแยกกันได้

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

รอบ 2 ทำให้หัวข้อนี้คมขึ้นตรงคำว่า “เร็วเพราะ hardware” ต้องแตกเป็นสามต้นทุน: layout ใน memory, การ dispatch งาน, และ model execution จริง เอกสาร [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html) ระบุว่า CUDA เป็นทั้ง platform และ programming model สำหรับเขียนโค้ดที่รันบน GPU และมีหัวข้อ SIMT kernels, asynchronous execution, unified memory และ compiler/runtime โดยตรง ส่วน [WebGPU specification](https://www.w3.org/TR/webgpu/) ช่วยย้ำว่า GPU path ผ่าน device/queue/command/synchronization ไม่ใช่ function call ฟรี ๆ

เมื่อนำกลับมาอ่านโพสต์ [021](../021-rust-bytemuck-bincode-layout.md), [043](../043-rust-simd-on-gpu.md), [044](../044-cpu-simd-gpu-crossover.md) และ [049](../049-apple-silicon-local-inference.md) จะเห็นความสัมพันธ์ชัด: การ cast ข้อมูลโดยไม่คัดลอกต้องรักษาเงื่อนไข layout/alignment/endian; ส่วน borrowed deserialization มีสัญญาข้อมูลอีกแบบ; CPU SIMD ช่วยงาน data-parallel ที่อยู่ใกล้ cache; GPU/SIMT คุ้มเมื่องานใหญ่พอและ memory access เหมาะ; Apple/Metal/MLX เป็น runtime เฉพาะ ecosystem ไม่ใช่หลักฐานว่า local ชนะ cloud ทุกกรณี

ตัวอย่างที่ควรลองคือ benchmark เดียวกัน 4 path: scalar Rust, CPU SIMD, GPU kernel และ runtime เฉพาะเครื่อง วัด `copy_us`, `dispatch_us`, `kernel_us`, `total_us`, `GB/s`, `p95`. ถ้า GPU ชนะเฉพาะ kernel แต่แพ้ total แปลว่าผู้ใช้ยังไม่ได้กำไรจริง ถ้า zero-copy เร็วกว่า serializer ต้องระบุว่าอยู่ใน process เดียวหรือข้าม file/network boundary

ข้อจำกัดของหลักฐาน: CUDA/WebGPU docs อธิบาย behavior ของ platform ไม่ได้ยืนยันตัวเลขในโพสต์ใด ๆ; Rust/SIMD, WASM หรือ GPU ไม่ได้ให้ speedup อัตโนมัติ ต้องจับคู่ workload, compiler flag, data layout และ validation ของผลลัพธ์ทุกครั้ง
<!-- RESEARCH_REVIEW_2_END -->
