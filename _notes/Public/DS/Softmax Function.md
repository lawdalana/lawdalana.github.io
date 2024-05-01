---
title : Softmax Functon
notetype : feed
date : 19-04-2024
---

```
Softmax Function หรือ SoftArgMax Function หรือ Normalized Exponential Function คือ ฟังก์ชันที่รับ Input เป็น Vector ของ Logit จำนวนจริง แล้ว Normalize ออกมาเป็นความน่าจะเป็น Probability ที่ผลรวมเท่ากับ 1

หรือเข้าใจง่าย ๆ ว่า Softmax รับตัวเลขเข้าไป แล้วแปลงออกมาเป็น Probability เรามาดูตัวอย่างกันจะเข้าใจง่ายขึ้น

ข้อเสีย
- เหมาะกับการใช้งานที่คาดหวัง Output ที่ถูกต้องอันเดียวเท่านั้น (ใกล้เคียง Max Function)
- เนื่องจาก ตัวหารต้อง Sum รวมทั้งหมดทุก Item ทุกครั้ง จึงทำให้มีปัญหาเรื่อง Performance ถ้ามีจำนวน Item มาก ๆ เช่น Output เป็น 1 ใน 500,000 คำใน Dictionary ในงาน NLP

Cr.Surapong Kanoktipsatharporn
```

![Formula](/assets/img/transformer/transformer_4.avif)
![Example](/assets/img/transformer/transformer_5.avif)

Resource
- https://www.bualabs.com/archives/1819/what-is-softmax-function-how-to-use-softmax-function-benefit-of-softmax/
- https://medium.com/super-ai-engineer/softmax-function-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3-eae1f1bbef63