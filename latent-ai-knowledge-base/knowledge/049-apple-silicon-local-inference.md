# 049 — Local Inference Stack บน Apple Silicon

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 42-47  
รูปประกอบ: ![Two local inference stacks](../original/image-6.png)  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์มีแค่ภาพกับลิงก์ Perplexity เรื่อง optimizing on-device inference for Apple Silicon ภาพเทียบสองแนวทาง: MLX-LM/MLX เป็น general-purpose array runtime ที่ model developer ประกอบ graph จาก operation กลาง ๆ ส่วน Lily เป็น Rust runtime/process เดียวที่ออกแบบรอบ model และ chip เดียว มี execution path เฉพาะสำหรับ prefill/decode เช่น routed MoE, DeltaNet scan, grouped Q4 GEMM, folded GQA และ GPU token loop

## ความรู้ที่ค้นเพิ่มจากบทความต้นฉบับ

บทความ Perplexity เปิดผ่านเครื่องมือเว็บโดยตรงไม่ได้ในรอบตรวจนี้ แต่ตรวจเนื้อหาจากสำเนาข้อความของ URL ต้นทางผ่าน text proxy ร่วมกับ repo ของผู้พัฒนา บทความบอกว่า Lily เป็น lightweight local inference engine สำหรับ Apple Silicon และ Qwen3.6-35B-A3B โดยมี optimization แยก prefill กับ decode และมี standalone demo ที่ repo [`perplexityai/pplx-garden/tree/main/lily`](https://github.com/perplexityai/pplx-garden/tree/main/lily)

รายละเอียดสำคัญคือ Lily ไม่เอา PyTorch หรือ MLX ไว้ใน execution path: Rust runtime โหลด checkpoint, จัดการ session state/generation loop, expose OpenAI-compatible chat completions API และใช้ custom Metal kernels สำหรับ Qwen-specific operations ส่วน MLX-LM อธิบาย computation เป็น MLX array operations ที่ reusable กว่า บทความรายงาน benchmark Qwen3.6-35B-A3B บน MacBook Pro M5 Max 40-core GPU, unified memory 128 GB: เฉลี่ย prefill 1.23× MLX-LM และ decode 1.35× MLX-LM; ที่ 4K prompt/context Lily ได้ 5,749.9 prefill tok/s และ 186.6 decode tok/s เทียบกับ MLX-LM 4,737.5 และ 140.9 tok/s [บทความและตาราง benchmark ของ Perplexity](https://www.perplexity.ai/hub/blog/optimizing-on-device-inference-for-apple-silicon)

## หลักฐานฝั่ง Apple/MLX

Apple WWDC25 อธิบายว่า MLX เป็น open-source library ที่ optimize สำหรับ Apple Silicon ใช้ Metal สำหรับ GPU acceleration และ unified memory เพื่อให้ CPU/GPU ทำงานร่วมกันง่ายขึ้น [Apple Developer](https://developer.apple.com/videos/play/wwdc2025/298/). Repo [`mlx-lm`](https://github.com/ml-explore/mlx-lm) ระบุว่าเป็น Python package สำหรับ text generation และ fine-tuning LLM บน Apple Silicon พร้อม MLX, รองรับ quantization, LoRA/full fine-tuning และ Hugging Face Hub integration

ดังนั้นภาพนี้ไม่ได้บอกว่า MLX “แย่” แต่บอก trade-off: runtime ทั่วไปพา model หลายแบบไปได้เร็วและยืดหยุ่น ส่วน runtime เฉพาะ model/chip มีโอกาส fuse งาน ตัด intermediate และวาง schedule ได้คมกว่า แต่จ่ายด้วย maintenance cost

## แบบฝึก

เลือก model หนึ่งตัวแล้วแยกเวลาเป็น `tokenize`, `prefill`, `decode/token`, `KV cache update`, `sampling`, `API serialization` จากนั้นถามแต่ละส่วนว่า shape คงที่พอทำ specialized kernel หรือไม่ ถ้าไม่คงที่ runtime generic อาจคุ้มกว่า ถ้าคงที่และกินเวลามาก นั่นคือ candidate สำหรับ Lily-style execution path

## ข้อควรระวัง

ตัวเลขของ Perplexity เป็น benchmark ของ Qwen3.6-35B-A3B Q4, batch 1, M5 Max ตามบทความ ไม่ควรย้ายไปสรุปว่า Rust/Metal เฉพาะทางจะชนะ MLX ทุก model หรือทุก Mac และความต่าง floating-point order ทำให้ต้องตรวจ numerical consistency เสมอ บทความเองรายงาน teacher-forced comparison เพื่อดูความต่างนี้

## แหล่งอ้างอิง

- [Perplexity blog URL จากต้นฉบับ](https://www.perplexity.ai/hub/blog/optimizing-on-device-inference-for-apple-silicon)
- [Perplexity Lily demo](https://github.com/perplexityai/pplx-garden/tree/main/lily)
- [MLX-LM GitHub](https://github.com/ml-explore/mlx-lm)
- [Apple Developer: Explore large language models on Apple silicon with MLX](https://developer.apple.com/videos/play/wwdc2025/298/)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** [Lily README ใน repo Perplexity](https://github.com/perplexityai/pplx-garden/tree/main/lily), รายงาน benchmark [2026-09-02: Lily vs MLX 0.32.2](https://github.com/perplexityai/pplx-garden/blob/main/lily/docs/2026-09-02-performance-mlx-0.32.2.md), [MLX documentation](https://ml-explore.github.io/mlx/build/html/index.html) และ [Metal Performance Shaders Graph](https://developer.apple.com/documentation/metalperformanceshadersgraph). README ระบุว่า Lily เป็น Metal inference server สำหรับ checkpoint เดียว `Qwen3.6-35B-A3B` แบบ MLX affine 4-bit, greedy decode, API ผิว OpenAI-compatible เฉพาะ subset และไม่รองรับ dense/GGUF/AWQ/GPTQ/int8/fp8 จึงเป็นหลักฐานว่า claim นี้แคบมากตั้งแต่ design

**สิ่งที่ขยายจากโพสต์:** รายงาน 2026-09-02 เทียบ Lily กับ MLX 0.32.2 บน Qwen3.6-35B-A3B, batch 1, synthetic deterministic prompt, greedy argmax, fresh process, warmup และวัด timed regions ภายใน process ไม่รวม model loading/tokenization/HTTP/detokenization. ตารางนั้นไม่ได้บอกว่า Lily “รัน graph เดียวกับ MLX เร็วกว่า” เพราะงานต่อ token ไม่เหมือนกัน: MLX-LM คืน full-vocabulary logprob แต่ Lily API minimal ทำ greedy selection. ดังนั้นตัวเลข speedup ควรอ่านเป็น production-engine throughput สำหรับ model/checkpoint/hardware/contract นี้ ไม่ใช่ข้อสรุปว่า Rust+Metal หรือ local Apple Silicon ชนะ MLX/cloud ทุกงาน

**ตัวอย่างทดลอง:** วัด local inference บน M3/M4 ด้วย prompt เดียวกัน 3 ขนาด: 256, 2k, 16k tokens และ output 128 tokens. แยก `prefill_tokens_s`, `decode_tokens_s`, `peak_memory`, `power/thermal note`, และคุณภาพคำตอบจากชุดคำถามเดิม. เทียบ MLX-LM, llama.cpp Metal, และ runtime ภายในโดย pin model/quantization เดียวกัน ถ้า runtime หนึ่งรองรับ quantization คนละแบบ ให้เขียนแยก ไม่รวมใน speedup เดียว

**ข้อจำกัด:** เอกสาร MLX/MPSGraph ไม่ได้ยืนยันตัวเลข benchmark ของ Perplexity หรือผู้เขียนโพสต์. มันยืนยันว่ามี stack สำหรับ local ML บน Apple ecosystem เท่านั้น. ข้อสรุปที่ปลอดภัยคือ local-first น่าสนใจเมื่อ latency/privacy/offline สำคัญ แต่ต้องวัดกับ workload และเครื่องจริง
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 048](048-vllm-katgpt-rs-benchmarking.md) · [โพสต์ 050 →](050-flow-reasoning-models.md)

หัวข้อที่เกี่ยวข้อง: [06 Rust, memory layout, SIMD และ CPU/GPU runtime](topics/06-rust-memory-and-hardware.md) · [07 การฝึกโมเดล, attention และสถาปัตยกรรมขนาดเล็ก](topics/07-training-and-model-architecture.md) · [08 อ่านและออกแบบ benchmark ให้เปรียบเทียบได้](topics/08-performance-and-benchmarks.md)
<!-- POST_NAV_END -->
