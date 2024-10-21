---
title : Speculative Sampling / Decoding
notetype : feed
date : 19-10-2024
---

## Summary
![Speculative_Decoding_timeline](/assets/img/Other/llm/Speculative_Decoding_timeline.avif)
- Speculative Decoding เป็นวิธีในการช่วยให้ LLM Model Inference ได้เร็วขึ้น 2x - 3x
- โดยใช้ Model ขนาดเล็กmujใช้ **Tokenizer** ตัวเดียวกันในการเทรนเพื่อมาช่วย Predict
![Speculative_Sampling_SpS_How_to_work](/assets/img/Other/llm/Speculative_Sampling_SpS_How_to_work.avif)
- Model ตัวใหญ่ = **Target model** / Model ตัวเล็ก = **Draft model**
- `Draft model ต้องมีปริมาณ parameter น้อยกว่า Target model โดยปกติน้อยกว่า 10 - 50 เท่า`
- ปกติ Model จะ Predict คำถัดไปแล้วทำซ้ำไปเรื่อยๆทำให้ช้า
- Draft model จะช่วย predict ไปก่อน 1 - 10 token ล่วงหน้า (เล็กกว่าเร็วกว่า เพราะบางคำเป็นคนที่ Predict ได้ง่ายๆเช่น of, the)
- Target model จะตรวจผลลัพธ์ของ Draft model
- โดยจะเช็คค่า prob ผ่านสมการ ถ้า Accept ก็จะเช็คตัวถัดไป แต่ถ้า Reject ก็จะหยุดและแก้ token ตัวนั้น
- หลังจากนั้นก็จะวน Process แบบนี้ไปเรื่อยๆ
![Speculative_Sampling_SpS_Algorithm](/assets/img/Other/llm/Speculative_Sampling_SpS_Algorithm.avif)
- ทำให้ Target model ที่กิน resource มากกว่าจะไม่ต้องรันหลายรอบมากเกินไปทำให้ inference ได้เร็วขึ้น 1.5x - 3x
![Speculative_Decoding_Example](/assets/img/Other/llm/Speculative_Decoding_Example.avif)

## Claude Summary
#### English
```
Speculative Sampling (SpS) is a novel technique for accelerating large language model (LLM) inference without compromising output quality. The method uses a smaller, faster "draft" model to predict multiple tokens in parallel, which are then validated by the larger "target" model. This process leverages the fact that for LLMs, scoring multiple tokens at once takes about the same time as scoring a single token, due to hardware utilization efficiencies.

The key to SpS is its modified rejection sampling scheme, which ensures the output maintains the target model's distribution. When the target model rejects a draft token, the process stops, resamples that token, and continues from there. This approach significantly speeds up text generation, achieving 2-25x faster inference in tests with a 70 billion parameter model, while preserving output quality across various tasks.
```
#### Thai
```
การสุ่มตัวอย่างเชิงคาดการณ์ (Speculative Sampling หรือ SpS) เป็นเทคนิคใหม่ที่ช่วยเร่งความเร็วในการอนุมานของโมเดลภาษาขนาดใหญ่ (LLM) โดยไม่ส่งผลกระทบต่อคุณภาพของผลลัพธ์ วิธีนี้ใช้โมเดล "ร่าง" ที่เล็กกว่าและเร็วกว่าในการทำนายโทเค็นหลายตัวพร้อมกัน จากนั้นจึงตรวจสอบโดยโมเดล "เป้าหมาย" ที่ใหญ่กว่า กระบวนการนี้ใช้ประโยชน์จากข้อเท็จจริงที่ว่าสำหรับ LLM การให้คะแนนโทเค็นหลายตัวพร้อมกันใช้เวลาประมาณเท่ากับการให้คะแนนโทเค็นเดียว เนื่องจากประสิทธิภาพการใช้งานฮาร์ดแวร์

กุญแจสำคัญของ SpS คือการใช้วิธีการสุ่มตัวอย่างแบบปฏิเสธที่ดัดแปลง ซึ่งทำให้มั่นใจได้ว่าผลลัพธ์ยังคงรักษาการกระจายตัวของโมเดลเป้าหมาย เมื่อโมเดลเป้าหมายปฏิเสธโทเค็นร่าง กระบวนการจะหยุด สุ่มตัวอย่างโทเค็นนั้นใหม่ และดำเนินการต่อจากจุดนั้น วิธีการนี้ช่วยเพิ่มความเร็วในการสร้างข้อความอย่างมีนัยสำคัญ โดยทำให้การอนุมานเร็วขึ้น 2-25 เท่าในการทดสอบกับโมเดลขนาด 70 พันล้านพารามิเตอร์ ในขณะที่ยังคงรักษาคุณภาพของผลลัพธ์ในงานต่างๆ
```

## Related Work
- Quantisation to int8, int4
- Distillation 
- [Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150)
- [Aggressive decoding](https://arxiv.org/abs/2205.10350)
- [Blockwise parallel decoding](https://arxiv.org/abs/1811.03115)


## Resource
- [Speculative Decoding — Make LLM Inference Faster](https://medium.com/ai-science/speculative-decoding-make-llm-inference-faster-c004501af120)
- [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)
- [Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318)
- [Serving AI models faster with speculative decoding](https://research.ibm.com/blog/speculative-decoding)
- [Speculative Decoding for LLMs](https://github.com/hemingkx/SpeculativeDecodingPapers?tab=readme-ov-file#speculative-decoding-for-llms)