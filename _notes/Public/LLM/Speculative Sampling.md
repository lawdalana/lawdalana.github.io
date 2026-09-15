---
title : Speculative Sampling
notetype : feed
date : 23-10-2024
last_modified: 2026-09-16
---

## Summary
![Speculative_Decoding_timeline](/assets/img/Other/LLM/Speculative_Decoding_timeline.avif)
- Speculative Decoding ช่วยให้ LLM สร้างข้อความได้เร็วขึ้น 2x - 3x
- ใช้โมเดลขนาดเล็กที่มี **Tokenizer** เดียวกันช่วยทำนายโทเคนล่วงหน้า
![Speculative_Sampling_SpS_How_to_work](/assets/img/Other/LLM/Speculative_Sampling_SpS_How_to_work.avif)
- โมเดลใหญ่เรียกว่า **Target model** ส่วนโมเดลเล็กเรียกว่า **Draft model**
- `Draft model ต้องมีปริมาณ parameter น้อยกว่า Target model โดยปกติน้อยกว่า 10 - 50 เท่า`
- โดยปกติโมเดลจะทำนายโทเคนถัดไปทีละตัว แล้วทำซ้ำจนได้คำตอบ จึงใช้เวลาหลายรอบ
- Draft model ทำนายล่วงหน้า 1 - 10 token ได้เร็วกว่า เพราะมีขนาดเล็กและบางคำทำนายได้ง่าย เช่น of, the
    - เลือก draft model ได้หลายแนวทาง เช่น เพิ่ม multi-head attention ใน target model ระหว่างฝึก ทำ sequence-level distillation ฝึก draft model ด้วยข้อมูลนำเข้าเดียวกัน หรือเลือกโมเดลขนาดเล็กในตระกูลเดียวกัน
- Target model ตรวจสอบโทเคนที่ Draft model เสนอ
- ตรวจค่าความน่าจะเป็นตามสมการ ถ้ายอมรับ (Accept) จะตรวจโทเคนถัดไป หากปฏิเสธ (Reject) จะหยุดและสุ่มโทเคนใหม่ที่ตำแหน่งนั้น
- จากนั้นทำกระบวนการนี้ซ้ำต่อไป
![Speculative_Sampling_SpS_Algorithm](/assets/img/Other/LLM/Speculative_Sampling_SpS_Algorithm.avif)
    - [ทำไมต้องสุ่ม r ~U[0, 1]](https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm) ([[Metropolis algorithm]])
- Target model ซึ่งใช้ทรัพยากรมากกว่าจึงทำงานน้อยรอบลง ช่วยให้ inference เร็วขึ้น 1.5x - 3x
![Speculative_Decoding_Example](/assets/img/Other/LLM/Speculative_Decoding_Example.avif)

---

### Result

Sampling Method|Benchmark|Result|Mean Token Time|Speed Up
:---:|:---:|:---:|:---:|:---:
ArS (Nucleus)|XSum (ROUGE-2)|0.112|14.1ms/Token |1x
SpS (Nucleus)|XSum (ROUGE-2)|0.114|7.52ms/Token |1.92x
ArS (Nucleus)|XSum (ROUGE-2)|0.157|14.1ms/Token |1x
SpS (Nucleus)|XSum (ROUGE-2)|0.156|7.00ms/Token |2.01x
ArS (Nucleus)|HumanEval (100 Shot)|45.1% |14.1ms/Token |1x
SpS (Nucleus)|HumanEval (100 Shot)|47.0%|5.73ms/Token |2.46x

![Speculative_Decoding_wall_time](/assets/img/Other/LLM/Speculative_Decoding_wall_time.avif)

## Claude Summary
#### English
```
Speculative Sampling (SpS) speeds up large language model (LLM) inference by letting a smaller, faster "draft" model propose several tokens ahead. The larger "target" model then checks those tokens in parallel. Scoring several tokens in one pass can use the hardware more efficiently than running a separate pass for each token.

A modified rejection-sampling step preserves the target model's output distribution. When a draft token is rejected, the algorithm resamples that position from an adjusted distribution and continues generating. In tests with a 70 billion parameter model, the method produced text 2-2.5x faster while preserving the target distribution.
```
#### Thai
```
Speculative Sampling (SpS) ช่วยเร่งการสร้างข้อความของ LLM โดยให้ draft model ที่เล็กกว่าและเร็วกว่าเสนอโทเคนล่วงหน้าหลายตัว จากนั้น target model จะตรวจสอบโทเคนเหล่านั้นพร้อมกัน การให้คะแนนหลายโทเคนในรอบเดียวช่วยใช้ฮาร์ดแวร์ได้คุ้มกว่าการประมวลผลแยกทีละโทเคน

ขั้นตอน rejection sampling ที่ปรับให้เหมาะกับวิธีนี้ช่วยรักษาการแจกแจงผลลัพธ์ของ target model เมื่อปฏิเสธโทเคนที่ draft เสนอ ระบบจะสุ่มโทเคนใหม่จากการแจกแจงที่ปรับแล้ว และสร้างข้อความต่อไป ในการทดลองกับโมเดลขนาด 70 พันล้านพารามิเตอร์ วิธีนี้สร้างข้อความได้เร็วขึ้น 2-2.5 เท่าโดยรักษาการแจกแจงผลลัพธ์เดิม
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
