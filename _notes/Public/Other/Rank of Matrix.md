---
title : Rank of Matrix
notetype : feed
date : 15-06-2024
---

# Rank of Matrix

- [คำจำกัดความมีได้หลายแบบ](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29#Alternative_definitions)
- column rank of A = dimension of the column space of A
- row rank of A = dimension of the row space of A
- ผลลัพธ์พื้นฐานของ linear algebra คือ `column rank` **=** `row rank`

## 2 Type of Matrix 

### Full rank
- ค่าของ Rank = ค่ามากสุดที่เป็นไปได้ของ Maxtrix size
- Matrix A(m,n) -> rank(A) = min(m, n)

![Full rank](/assets/img/Other/rank_of_matrix.avif)

### Rank-deficient
- ค่าของ Rank = ค่าน้อยกว่าค่ามากสุดที่เป็นไปได้ของ Maxtrix size
- Matrix A(m,n) -> rank(A) < min(m, n)

![Rank-deficient](/assets/img/Other/rank_of_matrix_2.avif)

## การหาค่าของ Rank
### ตัวอย่างการหาค่า Rank แบบคำนวนง่ายๆ (ให้เข้าใจหลักการ & Column อย่างเดียว)
![Full rank](/assets/img/Other/rank_of_matrix.avif)
- จากรูปด้านบนที่ Rank = 3 เพราะ
    - Rank = 0
    - Rank+1 ดูจาก column แรก = 1 1 3 ไม่ซ้ำกับใคร
    - Rank+1 ดูจาก column ที่สอง = 2 1 0 ไม่ซ้ำกับใคร และไม่ใช่ column แรก *2 *3 /2 /3 ...
    - Rank+1 ดูจาก column สาม = 3 0 4 ไม่ซ้ำกับใคร และไม่ใช่ column แรก *2 *3 /2 /3 ... และ ไม่ใช่ผมรวม ผลลบของ column ที่ 1 กับ 2
    - Rank = 3 ทั้งสาม column เป็น [linearly independent](https://en.wikipedia.org/wiki/Linear_dependence) กัน
    
![Rank-deficient](/assets/img/Other/rank_of_matrix_2.avif)
- จากรูปด้านบนที่ Rank = 3 เพราะ
    - Rank = 0
    - Rank+1 ดูจาก column แรก = 1 2 ไม่ซ้ำกับใคร
    - Rank+0 ดูจาก column ที่สอง = 2 4 เป็น 2 เท่าของ column แรก 
    - Rank+0 ดูจาก column สาม = 3 6 เป็น 3 เท่าของ column แรก หรือ column 1 + 2
    - Rank = 1

จากทั้งสองตัวอย่างเราคำนวณแบบ Row ได้เหมือนกัน

### การหาค่า Rank แบบ `Row echelon forms`
เป็นวิธีการคำนวนหา Rank แบบง่าย

![Row echelon forms](/assets/img/Other/rank_of_matrix_3.avif)


### การหาค่า Rank กรณีที่เป็น floating point 
- เนื่องจากค่าเป็น floating point ที่คำนวนอยู่บน computer ทำให้ basic Gaussian elimination (LU decomposition) ไม่สามารถเชื่อถือได้
- rank-revealing decomposition จะถูกนำมาใช้แทน เช่น [singular value decomposition - SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition)
- และยังมีทางอื่นที่ใช้การคำนวนน้อยกว่าเช่น [QR decomposition](https://en.wikipedia.org/wiki/QR_decomposition) with pivoting (rank-revealing QR factorization)


## Reference
- [Comprehensive Guide to Adapters, LoRA, QLoRA, LongLoRA with implementation](https://medium.com/@raniahossam/comprehensive-guide-to-adapters-lora-qlora-longlora-with-implementation-de003be30352)
- [Rank (linear algebra)](https://en.wikipedia.org/wiki/Rank_%28linear_algebra%29)