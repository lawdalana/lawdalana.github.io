# 048 — อยากไป vLLM แต่กลับมา Improve Runtime เอง

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 48-54  
รูปประกอบ: ![katgpt-rs vLLM win chart](../original/image-7.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์บอกว่าอยากไปงาน vLLM แต่ตั๋วเต็ม เลยเอาเวลาไป improve `katgpt-rs` แทน ภาพประกอบเป็น win chart ที่ claim ว่า `katgpt-rs` ชนะ vLLM ในบาง row เช่น decode @20K, cached TTFT และ acceptance แต่ระบุเองว่าเป็น row ที่ corrected แล้ว

## ความรู้ที่ค้นเพิ่ม

vLLM เป็น serving engine ที่ดังจาก PagedAttention งานต้นฉบับบอกว่าปัญหาสำคัญของ LLM serving คือ KV cache ใหญ่และ dynamic ทำให้ memory waste สูง PagedAttention จัดการ KV cache แบบ page เพื่อลด waste และเพิ่ม batch size โดย paper รายงาน throughput ดีขึ้น 2-4x เมื่อเทียบกับ FasterTransformer/Orca ใน workload ที่ประเมิน [PagedAttention/vLLM paper](https://arxiv.org/abs/2309.06180). เอกสาร benchmark ของ vLLM ยังเตือนว่าการรัน benchmark ซ้ำกับ server เดิมอาจ reuse prefix cache และ inflate throughput ได้ [vLLM Benchmark CLI](https://docs.vllm.ai/en/latest/benchmarking/cli/)

ดังนั้นเวลาเทียบ runtime ต้องระบุ cache state, prompt length, output length, concurrency, batch policy, quantization, GPU, driver และ sampling config ไม่เช่นนั้นตัวเลข TTFT/tok/s จะเล่าเรื่องคนละเรื่อง

## วิธีลองวัด

ทำ benchmark sheet แยก:

- TTFT: วินาทีต่อ first token, lower is better
- Decode throughput: tokens/s หลัง prefill
- Goodput: tokens/s ที่ผ่าน SLO latency
- Acceptance: tokens accepted ต่อ verify step ถ้าใช้ speculative decoding

ทุก row ต้องมี command, commit, model checksum, warmup และ raw logs

## ข้อควรระวัง

ภาพเป็น claim ภายในของผู้เขียน ไม่ใช่ผลรับรองจาก vLLM การชนะบาง row ไม่ได้แปลว่าระบบดีกว่าทั่วไป vLLM ถูกออกแบบเพื่อ serving workloads กว้างและ high concurrency ส่วน runtime เฉพาะทางอาจชนะ workload เฉพาะได้มาก ถ้ารู้ model/shape ล่วงหน้า

## แหล่งอ้างอิง

- [Efficient Memory Management for LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [vLLM documentation](https://docs.vllm.ai/en/latest/benchmarking/cli/)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** [MLPerf Inference reference implementation](https://github.com/mlcommons/inference) และ repo [llmperf](https://github.com/ray-project/llmperf). MLPerf Inference repo เป็น reference implementation และกติกา benchmark suite สำหรับวัด inference อย่างเป็นระบบ ส่วน llmperf เป็น harness เปิดสำหรับวัด LLM API/server latency-throughput จึงช่วยเติมด้าน “matched benchmark” ให้ claim เร็วกว่า vLLM/llama.cpp ในโพสต์

**สิ่งที่ขยายจากโพสต์:** การ improve `katgpt-rs` หลังตั๋ว vLLM เต็มเป็นเรื่อง engineering ที่ดี แต่ claim ว่าเร็วกว่า runtime อื่นต้องเทียบงานเดียวกัน: model/quantization เดียวกัน, prompt length/output length เดียวกัน, batch/concurrency เดียวกัน, hardware/driver/compiler เดียวกัน, และ metric เดียวกัน. สำหรับ LLM serving ต้องแยก throughput token/s, TTFT, TPOT, p95 latency, memory footprint และ quality/tolerance

**ตัวอย่างทดลอง:** สร้าง benchmark card หนึ่งใบต่อ row: `model_sha`, `weights_format`, `ctx_len`, `prompt_tokens`, `output_tokens`, `batch`, `concurrency`, `sampling`, `hardware`, `commit`, `command`, `raw_log`. รัน katgpt-rs, vLLM และ llama.cpp อย่างน้อย 7 repeats แล้วรายงาน median + interquartile range. ถ้า workload ต่างกัน เช่น speculative decoding เปิดเฉพาะฝั่งหนึ่ง ต้องแยกเป็นคนละ experiment

**ข้อจำกัด:** MLPerf/llmperf ไม่ได้พิสูจน์ตัวเลขในภาพ และ benchmark harness เองก็ต้อง configure ให้ถูก. รอบ 2 จึงเพิ่มเกณฑ์ว่า “เร็วกว่า” ต้องมี row-level evidence และ raw log ไม่ใช่ใช้ชื่อ vLLM เป็นตัวแทนของทุก deployment
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 047](047-latent-first-neuron-db.md) · [โพสต์ 049 →](049-apple-silicon-local-inference.md)

หัวข้อที่เกี่ยวข้อง: [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
