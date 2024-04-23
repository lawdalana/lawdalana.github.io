---
title : Mean Reciprocal Rank(MRR)
notetype : feed
date : 22-04-2024
---

- เป็น Evaluate Metrix ตัวนึงที่ใช้ว่าตำแหน่งของ Actual กับ Predict ตรงกันแค่ไหน

Query 	|Proposed Results 	|Correct response 	|Rank 	|Reciprocal rank
--- | --- | ---| ---| ---
cat 	|catten, cati, cats| 	cats| 	3| 	1/3
torus 	|torii, tori, toruses| 	tori| 	2 |	1/2
virus 	|viruses, virii, viri| 	viruses| 	1 |	1 

MRR = (1/3 + 1/2 + 1) / 3 = 11/18 = ~0.61

![Formula](/assets/img/Other/MRR.jpeg)

---
Resource
- https://en.wikipedia.org/wiki/Mean_reciprocal_rank