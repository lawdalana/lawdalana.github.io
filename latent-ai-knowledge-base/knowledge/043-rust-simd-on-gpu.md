# 043 — Rust SIMD บน GPU: ไอเดีย Lane เดียวกัน คนละเครื่อง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 89-94  
รูปประกอบ: ![Rust SIMD on GPU concept](../original/image-11.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์สั้นมาก: “Rust SIMD on GPU” แล้วแนบภาพที่เทียบ CPU กับ GPU โดยใช้ชนิด `Simd<i16, 32>` เหมือนกัน ภาพเสนอ mental model ว่า CPU thread มี SIMD lanes ส่วน GPU warp มี 32 lanes และในทั้งสองกรณี `core::simd` ขับ lane เหล่านั้นได้

## ความรู้ที่ค้นเพิ่ม

SIMD คือ Single Instruction, Multiple Data: instruction เดียวทำ operation เดียวกับข้อมูลหลายตัวพร้อมกัน V8 อธิบาย WebAssembly SIMD ว่าเป็นชุด operation แบบ portable สำหรับ data parallelism และจำกัดที่ fixed-width 128-bit เพื่อให้ข้าม platform ได้ [V8 WASM SIMD](https://v8.dev/features/simd). Rust `std::simd` ให้ abstraction แบบ portable แต่ยังเป็น nightly-only experimental API และไม่ผูกกับ hardware เฉพาะ [Rust `std::simd`](https://doc.rust-lang.org/std/simd/index.html).

ส่วน GPU ใช้ SIMT มากกว่า SIMD ในเชิง programming model: threads ใน warp ทำ instruction เดียวกัน แต่แต่ละ lane มี register/state ของตัวเอง CUDA docs ระบุว่า control flow ที่ทำให้ threads ใน warp แยกทางกันจะเพิ่มจำนวน instruction ที่ต้อง execute [CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html). นี่คือเหตุผลที่ภาพ “SIMD on GPU” น่าสนใจแต่ต้องระวังความหมาย

การเขียนชนิด `core::simd` ไม่ได้ส่งงานไป GPU โดยอัตโนมัติ ยังต้องมี compiler/backend และ runtime ที่รองรับ target นั้น เอกสาร portable SIMD ของ Rust เพียงอย่างเดียวจึงไม่ยืนยัน mapping CPU-thread/GPU-warp ที่ภาพเสนอ

## วิธีลองคิด

ลองเขียน vector add ขนาด 32 lanes ในสามแบบ: scalar loop, CPU SIMD, และ GPU kernel แล้ววัดสองกรณี:

- งานเล็กมาก เช่น 32 หรือ 320 elements
- งานใหญ่ เช่น 3.2 ล้าน elements

คุณจะเห็นว่าความขนานไม่ได้ฟรี เพราะ GPU ต้องจ่าย launch overhead และ memory transfer ส่วน CPU SIMD ทำงานเล็กใกล้ข้อมูลได้ดี

## ข้อควรระวัง

อย่าตีความว่า `Simd<i16, 32>` บน CPU และ warp 32 lane บน GPU มี semantics/performance เหมือนกันทุกเรื่อง CPU SIMD lanes อยู่ใน vector register เดียว ส่วน GPU warp scheduling, memory coalescing, divergence และ occupancy เป็นปัจจัยแยกต่างหาก

## แหล่งอ้างอิง

- [Rust `std::simd`](https://doc.rust-lang.org/std/simd/index.html)
- [V8 WebAssembly SIMD](https://v8.dev/features/simd)
- [CUDA Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** [CUDA Programming Guide (อัปเดต 2026)](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html) และ repo [Rust-GPU/rust-gpu](https://github.com/Rust-GPU/rust-gpu). NVIDIA อธิบาย CUDA เป็น programming model สำหรับรันโค้ดบน GPU และมีหัวข้อ writing SIMT kernels, asynchronous execution, unified memory, compiler และ execution model โดยตรง ส่วน Rust-GPU ระบุเป้าหมายเป็นการทำให้ Rust เป็นภาษาและ ecosystem สำหรับ GPU shaders ไม่ใช่การทำให้ `std::simd` ของ CPU กลายเป็น GPU warp อัตโนมัติ

**สิ่งที่ขยาย/แก้ความเข้าใจจากโพสต์:** ภาพในโพสต์ดีในฐานะ intuition ว่า “lane” ของ CPU SIMD กับ lane ใน warp ดูคล้ายกัน แต่หลักฐานที่ตรวจเพิ่มทำให้ต้องแยก 3 ชั้น: 1) Rust portable SIMD เป็น abstraction สำหรับ data parallel CPU path, 2) CUDA/SIMT คือ model ของ threads จำนวนมากที่รันบน GPU และมี divergence/scheduling/memory coalescing, 3) Rust-GPU เป็น compiler/toolchain สำหรับ shader target. ดังนั้นประโยค “Rust SIMD on GPU” ควรอ่านเป็นแนววิจัย/DSL ที่อยากให้โค้ด Rust map ไป GPU ได้ ไม่ใช่ claim ว่า `Simd<i16, 32>` ใน Rust ปัจจุบันมี semantics เท่ากับ warp 32 lane บนทุก GPU

**ตัวอย่างทดลองที่มีความหมาย:** เขียน vector add เดียวกัน 4 path: scalar Rust, `std::simd`/nightly CPU, Rust-GPU shader หรือ CUDA kernel, และ WebGPU/compute shader ถ้ามี runtime ที่สะดวก ใช้ input 1k, 32k, 1M, 64M elements แล้วรายงานแยก `compile_mode`, `copy_host_device_us`, `dispatch_us`, `kernel_us`, `total_us`, `throughput_GBps`. ถ้า GPU ชนะเฉพาะ `kernel_us` แต่แพ้ `total_us` แปลว่า product path ยังไม่ชนะจริง

**ข้อจำกัด:** CUDA docs เป็น NVIDIA-specific และ Rust-GPU ยังเป็น ecosystem เฉพาะ shader; ไม่ใช่หลักฐานว่า Rust portable SIMD จะครอบคลุม GPU ทุก vendor. การใช้ชนิด lane เท่ากันช่วยอ่านโค้ดง่ายขึ้นได้ แต่ correctness และ performance ยังขึ้นกับ backend, memory layout, alignment, branch divergence และการ batch งานให้มากพอ
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 042](042-latent-rag-cargo-heal.md) · [โพสต์ 044 →](044-cpu-simd-gpu-crossover.md)

หัวข้อที่เกี่ยวข้อง: [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
