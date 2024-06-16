---
title : WIP - Transformer
notetype : feed
date : 19-04-2024
---

Source
- https://jalammar.github.io/illustrated-transformer/
- https://www.youtube.com/watch?v=zxQyTK8quyY&ab_channel=StatQuestwithJoshStarmer
- https://towardsdatascience.com/transformers-explained-visually-part-2-how-it-works-step-by-step-b49fa4a64f34
- https://towardsdatascience.com/transformers-explained-visually-part-3-multi-head-attention-deep-dive-1c1ff1024853

# Transformer
- แบ่งออกเป็น 2 ส่วนหลังๆ คือ Encoders, Decoders
![Transformer](/assets/img/transformer/transformer_0.avif)
![Endcoder_Decoder](/assets/img/transformer/transformer_1.avif)

## Encoders
- ประกอบไปด้วย Self-Attention layer และ Feed Forward Nueral Network
- ขั้นตอนคือ เราจะแปลง Word to Vector (Embedding) 
- หลังจากได้ embedding แล้วเราจะ + Position Encoding เข้าไปด้วย
- ก่อนที่จะเป็น Input ของ Self-Attention layer
- ผลลัพธ์จาก Self-Attention layer จะถูกนำมาบวกกับ input อีกครั้งและทำการ Normalize (Residual Network)
- ผลลัพธ์จาก Normalize layer จะเป็น input ของ Feed Forward Nueral Network
- และเช่นเดียวกับ layer ก่อนหน้า ผลลัพธ์ของ Feed Forward Nueral Network ก็จะต้องเอามา + input และทำ normalize
- หลังจากนั้นก็จะได้ผลลัพธ์ของ Encoder ตัวแรก
![Endcoder_Position](/assets/img/transformer/transformer_11.avif)
![Endcoder](/assets/img/transformer/transformer_2.avif)

## Position Encoding
- ปกติ Postion Embedding จะถูกสร้างขึ้นมาเพื่อนำมาบวกกับ Embedding ตัวหลักเพื่อบ่งบอก คำแต่ละตำแหน่ง
![Position Encoding](/assets/img/transformer/transformer_12.avif)
- โดยปกติจะถูกสร้างจาก Function Sin หรือ Cos แต่ Paper ปัจจุบันเอา สัญญาณมาแทรกระหว่างกัน
![Position Encoding](/assets/img/transformer/transformer_13.avif)

## Self-Attention 
- ขั้นแรกเราจะสร้าง Vector ขึ้นมา 3 ตัวคือ Queries, Keys, Values ทั้งสามค่าได้มาจากการ multiply กับ embedding จาก weight ใน neural network ซึ่งในที่นี้คือ Wq, Wk, Wv (Q = Embedding x Wq, K = Embedding x Wk, V = Embedding x Wv)
- ไม่ว่าเราจะ set ให้ input ยาวแค่ไหนก็ตาม เรายังใช้ Wa, Wk, Wv เหมือนกันหมด ยกเว้น multi-head ตัวอื่นๆ
- ต่อมาเราจะคิด score ของแต่ละคำที่เอาค่า Q ไป dot product กับทุกๆ K เช่น Q1.K1, Q1.K2, Q1.Kn
- หารด้วย square root ของขนาด embeding K (ตาม paper ปกติขนาด k คือ 64)
- จากในตัวอย่าง Score 112/8 = 14, 96/12 = 12
- และนำ score ที่ได้มาเข้า [[Softmax Functon]]
- และนำ Soft Max score มาคูณกับ V1, V2, Vn เพื่อที่จะให้ความสำคัญของแต่ละอันต่างกันไป
- หลังจากนั้นนำค่าที่คูณแล้วมา Sum กัน จะได้ผลลัพธ์ Z1
![Example](/assets/img/transformer/transformer_3.avif)
- แต่แทนที่เราจะทำการคำนวนทีละอัน  เราสามารถ คำนวณพร้อมกันแบบ Matrix ได้เลย
![Example_Matrix1](/assets/img/transformer/transformer_6.avif)
![Example_Matrix2](/assets/img/transformer/transformer_7.avif)

## multi-headed-Attention 
- เป็นการรัน Self-Attention หลายๆ Node พร้อมกัน เช่น
![Example_Multi1](/assets/img/transformer/transformer_8.avif)
- หลังจากรันแล้วเราจะได้คำตอบของทุกตัว ในที่นี้จะมีคำตอบ 7 ตัว
- เราจะนำคำตอบทั้งหมดมา concate กันและคูณด้วย W0 เผื่อหา final answer
![Example_Multi2](/assets/img/transformer/transformer_9.avif)
![Example_Multi3](/assets/img/transformer/transformer_10.avif)


## Decoders
- ผลลัพธ์จาก Encoder จะเป็น input และเป็น Residual ของ Decoder ทุก Node
- 
![Decoder](/assets/img/transformer/transformer_14.avif)
