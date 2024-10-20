---
title : Speculative Decoding
notetype : feed
date : 19-10-2024
---

## TLDR
- Speculative Decoding เป็นวิธีในการช่วยให้ LLM Model Inference ได้เร็วขึ้น 2x - 3x
- โดยใช้ Model ขนาดเล็กmujใช้ **Tokenizer** ตัวเดียวกันในการเทรนเพื่อมาช่วย Predict
- Model ตัวใหญ่ = **Target model** / Model ตัวเล็ก = **Draft model**
- `Draft model ต้องมีปริมาณ parameter น้อยกว่า Target model โดยปกติน้อยกว่า 10 - 30 เท่า`
- ปกติ Model จะ Predict คำถัดไปแล้วทำซ้ำไปเรื่อยๆทำให้ช้า
- Draft model จะช่วย predict ไปก่อน 1 - 10 token ล่วงหน้า (เล็กกว่าเร็วกว่า เพราะบางคำเป็นคนที่ Predict ได้ง่ายๆเช่น of, the)
- Target model จะตรวจผลลัพธ์และแก้ตัวที่ผิดให้
- นั้นทำให้ Target model ที่กิน resource มากกว่าจะไม่ต้องรันหลายรอบมากเกินไปทำให้ inference ได้เร็วขึ้น



## Resource
- [Speculative Decoding — Make LLM Inference Faster](https://medium.com/ai-science/speculative-decoding-make-llm-inference-faster-c004501af120)
- [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192)
- [Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318)
- [Serving AI models faster with speculative decoding](https://research.ibm.com/blog/speculative-decoding)
- [Speculative Decoding for LLMs](https://github.com/hemingkx/SpeculativeDecodingPapers?tab=readme-ov-file#speculative-decoding-for-llms)