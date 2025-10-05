---
title: (RAG-MCP) Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation
notetype: feed
date: 2025-10-04
last_modified: 2025-10-04
tags: [llm, mcp, ai, tools, rag]
status: published
---

# [Source: RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation](https://arxiv.org/abs/2505.03275)

## TLDR;
- ใช้ semantic retrieval เพื่อคัดเลือก MCP/เครื่องมือที่เกี่ยวข้องก่อนส่งให้ LLM ลด prompt bloat และความซับซ้อนในการตัดสินใจ
- ลดโทเคนในพรอมป์ได้มาก (เกิน 50%) และเพิ่มความแม่นยำการเลือกเครื่องมือกว่า 3 เท่า (43.13% เทียบกับ 13.62% เบสไลน์)
- ทำให้การเชื่อมต่อเครื่องมือจำนวนมากกับ LLM ทำได้ แม่นยำและขยายเพิ่มได้

## 1.Introduction
- Problem
  - LLM จำกัดด้วยความรู้ในพารามิเตอร์และความยาวบริบท จึงพึ่งพา ฟังก์ชัน/เครื่องมือภายนอก (web search, DB, calculator ฯลฯ)
  - แม้แนวทางอย่าง ReAct, Toolformer, Gorilla จะช่วยใช้เครื่องมือดีขึ้น แต่เมื่อจำนวนเครื่องมือเพิ่มมาก ๆ จะเกิด
    - Prompt bloat: ต้องใส่คำอธิบายเครื่องมือจำนวนมากในคอนเท็กซ์
    - Decision overhead: ตัวแบบเลือกเครื่องมือถูกยากขึ้นและเสี่ยง hallucinate API
- Hypothesis
  - แยกขั้น “ค้นหาเครื่องมือ” ออกจากการสร้างข้อความ โดยใช้การดึงคืนความหมาย (RAG) เลือกเฉพาะเครื่องมือที่น่าจะเกี่ยวข้องที่สุดมาให้ LLM

![Tools_w_wo_MCP](/assets/img/Other/LLM/RAG-MCP.avif)

### Contributions
- สถาปัตยกรรม RAG-MCP: ผสาน retrieval กับการเรียกใช้ฟังก์ชันในบริบท MCP
- Semantic tool retrieval: ทำดัชนีคำอธิบาย/สคีมาของเครื่องมือ แล้ว match กับโจทย์ผู้ใช้เพื่อคัด top-k ลดปริมาณคอนเท็กซ์และภาระการตัดสินใจ
- ผลลัพธ์ดีกว่าเบสไลน์: รักษาความแม่นยำการเลือกเครื่องมือแม้จำนวนเครื่องมือเพิ่มขึ้น และลดความผิดพลาด เช่น เลือกเครื่องมือผิด/พารามิเตอร์ผิด

## 2.Methodology
ศึกษาว่าจำนวนของเซิร์ฟเวอร์ MCP ที่มีอยู่ส่งผลต่อความสามารถของโมเดลภาษาขนาดใหญ่ (LLM) ในการเลือกและเรียกใช้เครื่องมือที่ถูกต้อง (“prompt bloat”) อย่างไร

### Prompt Bloat & MCP Stress Test
#### How
- ดัดแปลงการ Stress Test จากหลังการ Needle-in-a-Haystack (NIAH - งมเข็มในมหาสมุทร): ทดสอบความสามารถ “ดึงของถูก” ออกจากกองข้อมูลยาว ๆ โดย สุ่มเลือก 1 MCP ที่ถูก + N−1 ตัวลวง (N 1 - 11100) แล้วให้โมเดลเลือก-เรียกใช้ WebSearch MCP ที่ถูกต้อง วัดทั้งการเลือกให้ถูกและการทำงานสำเร็จจริง (search/ตอบกลับ)
- MCP Server ที่ใช้มาจากของที่เป็น public 4400+ Server เพื่อให้สถานการณ์ “เครื่องมือเยอะจริง” ใกล้ความเป็นจริงของ MCP ecosystem

#### Matrix
- Choose the right Tool = 1
- Wrong Tools = 0

---

### RAG-MCP
#### How
- ต่อเนืองจาก Prompt Bloat & MCP Stress Test
- สำหรับแต่ละค่า N โมเดลต้องทำ 20 งาน web-search และในแต่ละงานต้อง (a) เลือก MCP ที่ถูก, (b) ออก query/คำตอบให้ถูกฟอร์แมต, (c) ส่งผลลัพธ์สุดท้ายกลับมา
- ทดสอบ 3 วิธีเทียบกัน: Blank Conditioning, Actual Match, และ RAG-MCP (retriever จัดอันดับเชิงความหมายแล้วฉีดแค่สคีมาของตัวที่ดีที่สุดเข้าไป)

#### Matrix
- Accuracy = สัดส่วนรอบที่เลือก MCP ตัวจริงถูกต้อง
- Avg Prompt Tokens = จำนวนโทเคนในพรอมป์เฉลี่ย (รวมเมทาดาตา/สคีมาเครื่องมือที่ใส่เข้าไป)
- Avg Completion Tokens = โทเคนคำตอบเฉลี่ยที่โมเดลสร้างออกมา
- Latency = เวลาที่ใช้ในการตอบ
- Llama-based judge = ให้ Llama-based verifier (“Llama as Judge”) ตรวจเทียบผลลัพธ์สุดท้ายกับ ground truth เพื่อความเป็นระบบอัตโนมัติของการตัดสินถูก/ผิด

#### Baselines
- Blank Conditioning: ยัดสคีมาของ MCP ทั้ง N ตัวให้โมเดลเลือกเอง
- Actual Match: กรองคีย์เวิร์ดหยาบ ๆ ก่อน แล้วค่อยให้โมเดลเลือก
- RAG-MCP: จัดอันดับเชิงความหมายบนดัชนีเวกเตอร์ แล้ว ฉีดสคีมาของตัวที่ดีที่สุดแค่ตัวเดียว เข้าไปในพรอมป์เพื่อใช้งานจริง

![Tools_w_wo_MCP](/assets/img/Other/LLM/Three-Step-Pipeline-Diagram.avif)


## 3.Experiment Result
### 3.1 Experiment Choose the right tool
![Tools_w_wo_MCP](/assets/img/Other/LLM/RAG_MCP_result.avif)

- แกน X (MCP Number): จำนวนเครื่องมือ (N) ที่ใส่เข้าไปในรอบทดสอบนั้น ๆ แต่ละคอลัมน์คือคนละค่า N ไล่ตั้งแต่หลักหน่วยไปจนถึง หลักหมื่น (≈1 → 11,100)
- แกน Y (Key MCP Position): ตำแหน่งของ “เครื่องมือที่ถูกต้อง” ภายในลิสต์ผู้สมัครของรอบนั้น
- สี: อ้างอิงสเกลด้านขวา
  - เหลือง = 1.0 = สำเร็จ (เลือก/เรียกใช้เครื่องมือที่ถูกต้องได้)
  - ม่วง = 0.0 = ล้มเหลว (เลือกผิดหรือไม่สำเร็จ)


### 3.2 Experiment Choose the right tools

![Tools_w_wo_MCP](/assets/img/Other/LLM/RAG_MCP_result_2.avif)


## 4.Conclusion
- ยืนยันรูปแบบเสื่อมตามสเกล และแสดงโซนที่ยังสำเร็จได้แม้เครื่องมือมาก (รูปตาราง เหลือง ม่วง)
- Tools น้อยกว่า <=30 ความสำเร็จสูงมาก
- ถ้า Tools มากกว่า 100 แทบจะตอบไม่ได้
- เหตุผลที่ RAG-MCP เหนือกว่า
  - Focused context filtering
  - Prompt efficiency
  - Balanced generation โทเคนคำตอบมากขึ้นเล็กน้อยแลกกับการตรวจสอบ/ให้เหตุผลที่ดีขึ้น