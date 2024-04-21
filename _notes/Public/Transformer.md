---
title : Transformer
notetype : feed
date : 19-04-2024
---

Good Resource
- https://jalammar.github.io/illustrated-transformer/

# Transformer
- แบ่งออกเป็น 2 ส่วนหลังๆ คือ Encoders, Decoders
- ![Transformer](/assets/img/transformer/transformer_0.png)
- ![Endcoder_Decoder](/assets/img/transformer/transformer_1.png)

## Encoders
- ประกอบไปด้วย Self-Attention layer และ Feed Forward Nueral Network
- ขั้นตอนคือ เราจะแปลง Word to Vector (Embedding) ก่อนที่จะโยนเข้ามาในส่วนที่เป็น Self-Attention layer
- ผลลัพธ์จาก Self-Attention layer เป็น input ของ Feed Forward Nueral Network
- หลังจากนั้นก็จะได้ผลลัพธ์ของ Encoder ตัวแรก
- ![Endcoder](/assets/img/transformer/transformer_2.png)

## Self-Attention 
- ขั้นแรกเราจะสร้าง Vector ขึ้นมา 3 ตัวคือ Queries, Keys, Values ทั้งสามค่าได้มาจากการ multiply กับ embedding จาก weight ใน neural network ซึ่งในที่นี้คือ Wq, Wk, Wv
- ต่อมาเราจะคิด score ของแต่ละคำที่เอาค่า Q ไป dot product กับทุกๆ K เช่น Q1.K1, Q1.K2, Q1.Kn
- หารด้วย square root ของขนาด embeding K (ตาม paper ปกติขนาด k คือ 64)
- จากในตัวอย่าง Score 112/8 = 14, 96/12 = 12
- 
- ![Endcoder](/assets/img/transformer/transformer_3.png)

## Decoders

