---
title : Transformer
notetype : feed
date : 19-04-2024
---

Original Source
- https://jalammar.github.io/illustrated-transformer/

# Transformer
- แบ่งออกเป็น 2 ส่วนหลังๆ คือ Encoders, Decoders
![Transformer](/assets/img/transformer/transformer_0.png)
![Endcoder_Decoder](/assets/img/transformer/transformer_1.png)

## Encoders
- ประกอบไปด้วย Self-Attention layer และ Feed Forward Nueral Network
- ขั้นตอนคือ เราจะแปลง Word to Vector (Embedding) 
- หลังจากได้ embedding แล้วเราจะ + Position Encoding เข้าไปด้วย
- ก่อนที่จะเป็น Input ของ Self-Attention layer
- ผลลัพธ์จาก Self-Attention layer เป็น input ของ Feed Forward Nueral Network
- หลังจากนั้นก็จะได้ผลลัพธ์ของ Encoder ตัวแรก
![Endcoder_Position](/assets/img/transformer/transformer_11.png)
![Endcoder](/assets/img/transformer/transformer_2.png)

## Position Encoding
- ปกติ Postion Embedding จะถูกสร้างขึ้นมาเพื่อนำมาบวกกับ Embedding ตัวหลักเพื่อบ่งบอก คำแต่ละตำแหน่ง
![Position Encoding](/assets/img/transformer/transformer_12.png)
-โดยปกติจะถูกสร้างจาก Function Sin หรือ Cos แต่ Paper ปัจจุบันเอา สัญญาณมาแทรกระหว่างกัน
![Position Encoding](/assets/img/transformer/transformer_13.png)

## Self-Attention 
- ขั้นแรกเราจะสร้าง Vector ขึ้นมา 3 ตัวคือ Queries, Keys, Values ทั้งสามค่าได้มาจากการ multiply กับ embedding จาก weight ใน neural network ซึ่งในที่นี้คือ Wq, Wk, Wv
- ต่อมาเราจะคิด score ของแต่ละคำที่เอาค่า Q ไป dot product กับทุกๆ K เช่น Q1.K1, Q1.K2, Q1.Kn
- หารด้วย square root ของขนาด embeding K (ตาม paper ปกติขนาด k คือ 64)
- จากในตัวอย่าง Score 112/8 = 14, 96/12 = 12
- และนำ score ที่ได้มาเข้า [[Softmax Functon]]
- และนำ Soft Max score มาคูณกับ V1, V2, Vn เพื่อที่จะให้ความสำคัญของแต่ละอันต่างกันไป
- หลังจากนั้นนำค่าที่คูณแล้วมา Sum กัน จะได้ผลลัพธ์ Z1
![Example](/assets/img/transformer/transformer_3.png)
- แต่แทนที่เราจะทำการคำนวนทีละอัน  เราสามารถ คำนวณพร้อมกันแบบ Matrix ได้เลย
![Example_Matrix1](/assets/img/transformer/transformer_6.png)
![Example_Matrix2](/assets/img/transformer/transformer_7.png)

## multi-headed-Attention 
- เป็นการรัน Self-Attention หลายๆ Node พร้อมกัน เช่น
![Example_Multi1](/assets/img/transformer/transformer_8.png)
- หลังจากรันแล้วเราจะได้คำตอบของทุกตัว ในที่นี้จะมีคำตอบ 7 ตัว
- เราจะนำคำตอบทั้งหมดมา concate กันและคูณด้วย W0 เผื่อหา final answer
![Example_Multi2](/assets/img/transformer/transformer_9.png)
![Example_Multi3](/assets/img/transformer/transformer_10.png)


## Decoders

