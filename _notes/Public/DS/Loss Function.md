---
title: Loss Function
notetype: feed
date: 2024-04-22
last_modified: 2024-04-22
tags: [machine-learning, loss-function, deep-learning, optimization]
status: published
---

# Loss Function

> **"หัวใจหลักของการฝึกฝนโมเดล — ตัวชี้วัดว่าโมเดลทำผลงานได้ดีแค่ไหน และควรปรับตัวอย่างไร"**

---

## ❔ คืออะไร (What is it)
**Loss Function** (ฟังก์ชันสูญเสีย) หรือ Cost Function/Objective Function คือสมการคณิตศาสตร์ที่ใช้ประเมินความแตกต่างระหว่าง **"ค่าที่โมเดลทำนายได้"** กับ **"ค่าจริง (Ground Truth)"** ในระหว่างการเทรน Machine Learning หรือ Deep Learning โมเดลจะใช้ค่านี้ร่วมกับ Optimizer (เช่น SGD, Adam) ในการปรับ Parameters เพื่อลดค่า Loss ให้เหลือน้อยที่สุด.

---

## 📈 Regression Loss Functions (สำหรับการทำนายตัวเลขต่อเนื่อง)

### 🟡 Mean Squared Error (MSE) Loss
```text
ใช้ทำ: งาน Regression ทั่วไป เช่น ทำนายราคาบ้าน, ทำนายยอดขาย
จุดเด่น / เทคนิค:
 • คำนวณจาก "ค่าเฉลี่ยของกำลังสองของความคลาดเคลื่อน" (Average of squared differences)
 • ลงโทษ (Penalize) ความผิดพลาดที่มีขนาดใหญ่ (Outliers) อย่างรุนแรง
 • เป็น Default เบื้องต้นของงาน Regression ส่วนใหญ่
```

### 🟢 Mean Squared Logarithmic Error (MSLE) Loss
```text
ใช้ทำ: งานที่มี Target Value มีช่วงกว้างมาก หรือไม่ต้องการให้ Outlier มากระทบโมเดลหนักเกินไป
จุดเด่น / เทคนิค:
 • คำนวณ MSE บนค่า Logarithm ของค่าที่ทำนายและค่าจริง
 • ลงโทษความผิดพลาดเชิงสัดส่วน (Percentage/Ratio error) มากกว่าผลต่างแบบสัมบูรณ์
 • โฟกัสที่การทายค่าน้อยกว่าความเป็นจริง (Underestimate) มากกว่าทายเกิน (Overestimate)
```

### 🔵 Mean Absolute Error (MAE) Loss
```text
ใช้ทำ: งานที่ข้อมูลมี Outliers เยอะ และต้องการให้โมเดลทนทานต่อ Outlier (Robustness)
จุดเด่น / เทคนิค:
 • คำนวณจาก "ค่าเฉลี่ยของค่าสัมบูรณ์ของความคลาดเคลื่อน"
 • มุมมองความผิดพลาดเป็นเส้นตรง (Linear penalty) ทนทานต่อ Outlier ดีเยี่ยม
 • แปลความหมายง่าย เพราะผลลัพธ์มีหน่วยเดียวกับข้อมูลจริงโดยตรง
```

---

## 📊 Classification Loss Functions (สำหรับการจัดกลุ่ม/แยกประเภท)

### 🟣 Sigmoid Loss Function
```text
ใช้ทำ: มักใช้คู่กับงาน Binary Classification หรือ Multi-label Classification
จุดเด่น / เทคนิค:
 • แปลง Output ให้อยู่ในสเกล 0-1 (แทนค่าความน่าจะเป็น) แต่ละคลาสแยกกันอิสระ
 • บาง Framework จะควบรวม Sigmoid เข้ากับ Crossentropy เลยเพื่อความเสถียร (Numerical stability)
```

### 🟠 Binary Crossentropy (BCE) Loss
```text
ใช้ทำ: งานจัดกลุ่มแบบ 2 คลาส (เช่น แมว vs หมา, สแปม vs อีเมลปกติ)
จุดเด่น / เทคนิค:
 • ใช้ Log function ประเมินว่าค่าความน่าจะเป็นที่ทำนายเข้าใกล้ Label จริงแค่ไหน
 • โมเดลจะถูกลงโทษหนักมากถ้า "มั่นใจแบบผิดๆ"
 • อาศัย Output ที่ถูกผ่าน Sigmoid function มาแล้ว
```

### 🔴 Categorical Crossentropy (CCE) Loss
```text
ใช้ทำ: งานจัดกลุ่มแบบหลายคลาส (Multi-class Classification) ที่ผลลัพธ์เป็นได้แค่ 1 คลาส
จุดเด่น / เทคนิค:
 • คาดหวังให้ Target Labels อยู่ในรูปแบบ "One-hot encoding" (เช่น [0, 1, 0])
 • ทำงานสอดคล้องกับ Softmax Activation อย่างสมบูรณ์แบบ
 • สนใจคำนวณ Loss เฉพาะสัดส่วนในคลาสที่ถูกต้องเท่านั้น
```

### 🟤 Sparse Categorical Crossentropy (SCCE) Loss
```text
ใช้ทำ: คล้าย CCE (Multi-class) แต่ปรับวิธีการรับ Label ขาเข้า
จุดเด่น / เทคนิค:
 • รับ Target Labels เป็น Integer โดยตรง (เช่น 0, 1, 2, 3...) แทนที่จะเป็น One-hot vector
 • ประหยัดหน่วยความจำ (Memory efficient) มหาศาลเมื่อใช้กับ Dataset ที่มีคลาสจำนวนมาก
 • ผลลัพธ์ทางคณิตศาสตร์เหมือน CCE ทุกประการ
```

---

> 💡 **Tip**: การเลือก Loss Function ให้ตรงกับชนิดของข้อมูลเป็นเรื่องสำคัญมาก หากเลือกใช้ MSE กับงาน Classification โมเดลอาจลู่เข้าได้ช้าหรือล้มเหลวเลย เพราะ Landscape ของฟังก์ชันไม่ได้ถูกออกแบบมาให้เป็นส่วนเว้าโค้งพอเหมาะสำหรับการแก้ปัญหานั้น!