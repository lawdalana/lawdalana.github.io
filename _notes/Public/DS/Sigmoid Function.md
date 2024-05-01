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

---

# Sigmoid Loss Function
Tenforflow function
- tf.nn.sigmoid_cross_entropy_with_logits
- tf.nn.weighted_cross_entropy_with_logits
- tf.losses.sigmoid_cross_entropy

Sigmoid loss function is for binary classification. But tensorflow functions are more general and allow to do multi-label classification, when the classes are independent. In other words, `tf.nn.sigmoid_cross_entropy_with_logits` solves N binary classifications at once.

The labels must be one-hot encoded or can contain soft class probabilities.

tf.losses.sigmoid_cross_entropy in addition allows to set the in-batch weights, i.e. make some examples more important than others. tf.nn.weighted_cross_entropy_with_logits allows to set class weights (remember, the classification is binary), i.e. make positive errors larger than negative errors. This is useful when the training data is unbalanced.

Resource
- https://www.bualabs.com/archives/1261/what-is-activation-function-what-is-sigmoid-function-activation-function-ep-1/
- https://stackoverflow.com/questions/47034888/how-to-choose-cross-entropy-loss-in-tensorflow

