---
title : Sigmoid Function
notetype : feed
date : 22-04-2024
---

```
Sigmoid Function เป็นฟังก์ชันที่เป็น Curve รูปตัว S เห็นแล้วเข้าใจได้ง่าย และเนื่องจาก Output ของ Sigmoid Function มีค่าระหว่าง 0 – 1 จึงเหมาะที่จะถูกใช้ในงานที่ต้องการ Output เป็นความน่าจะเป็น (Probability) หรือใช้เป็น Output ว่า 1=Yes, 0=No

ข้อเสีย
- ถ้า Input น้อยกว่า -5 หรือมากกว่า 5 ความชัน Slope จะเข้าใกล้ 0 จน Gradient หายไปหมด ทำให้โมเดล Train ไม่ไปไหน เรียกว่า Vanishing Gradient
- Output ไม่ Balance มี Mean ไม่เท่ากับ 0 เพราะมีแต่ค่าเป็นบวก ทำให้ Optimize ยาก
- ใช้แล้วโมเดลมักจะ Converge ช้า

Cr.Surapong Kanoktipsatharporn
```

![Formula](/assets/img/Other/Sigmoid_Formula.png)
![Formula](/assets/img/Other/Sigmoid_Chart.webp)

Resource
- https://www.bualabs.com/archives/1261/what-is-activation-function-what-is-sigmoid-function-activation-function-ep-1/
