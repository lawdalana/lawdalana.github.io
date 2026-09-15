---
title: RAG (Retrieval-Augmented Generation)
notetype: feed
date: 2025-02-08
last_modified: 2026-09-16
tags: [llm, rag, ai, retrieval, generation]
status: published
---

## From GPT-4o 

RAG หรือ Retrieval-Augmented Generation เป็นเทคนิคที่นำการค้นคืนข้อมูล (retrieval) มาใช้ร่วมกับการสร้างข้อความ (generation) เพื่อช่วยให้ Large Language Models (LLMs) ตอบคำถามโดยอ้างอิงข้อมูลที่เกี่ยวข้อง

### หลักการทำงานของ RAG
โดยทั่วไป LLM ตอบคำถามจากสิ่งที่เรียนรู้ระหว่างการฝึก ซึ่งอาจล้าสมัยหรือไม่ครอบคลุมเรื่องที่ถาม RAG เพิ่มขั้นตอนค้นคืนข้อมูลจากแหล่งภายนอก เพื่อนำมาใช้ประกอบการสร้างคำตอบ

1. Retrieval (การดึงข้อมูล)
    - เมื่อมีคำถาม ระบบจะค้นข้อมูลที่เกี่ยวข้องจากเอกสารหรือฐานข้อมูล โดยอาจใช้เครื่องมือค้นหาเวกเตอร์ เช่น FAISS หรือ Pinecone
2. Augmentation (การเสริมข้อมูล)
    - ระบบนำข้อมูลที่ค้นได้มาใส่ใน prompt เพื่อให้ LLM ใช้ประกอบคำตอบ
3. Generation (การสร้างคำตอบ)
    - LLM ใช้ข้อมูลที่เพิ่มเข้ามาสร้างคำตอบที่ตรงกับคำถามและมีข้อมูลอ้างอิง

### ข้อดีของ RAG
- ✅ ช่วยลดการสร้างข้อมูลที่ไม่ถูกต้อง (Hallucination) โดยให้โมเดลใช้ข้อมูลที่ค้นคืนมาประกอบคำตอบ
- ✅ เพิ่มข้อมูลใหม่ได้โดยไม่ต้องฝึกโมเดลใหม่ ด้วยการอัปเดตแหล่งข้อมูลที่ใช้ค้นคืน
- ✅ ปรับแต่งเฉพาะทางได้ง่าย – เหมาะกับงานที่ต้องการความแม่นยำสูง เช่น AI สำหรับวิจัย, กฎหมาย, การแพทย์

### ตัวอย่างการใช้งาน RAG
- Chatbot ที่ใช้ข้อมูลจากฐานข้อมูลบริษัทประกอบคำตอบ
- ระบบค้นหาข้อมูลเอกสารภายในองค์กร เช่น การค้นหากฎระเบียบหรือคู่มือใช้งาน
- AI ช่วยสรุปข่าวสารหรือข้อมูลวิชาการ โดยดึงข้อมูลจากแหล่งที่เชื่อถือได้

### เครื่องมือยอดนิยมที่ใช้ทำ RAG
- ฐานข้อมูลและไลบรารีค้นหาเวกเตอร์: FAISS, Pinecone, Weaviate, ChromaDB
- LLM Frameworks: LangChain, LlamaIndex
- Embedding Models: OpenAI Embeddings, BERT, SentenceTransformers

![RAG LLM Integration](/assets/img/Other/LLM/rag_llm_integration.avif) 

## Useful link
- https://humanloop.com/blog/optimizing-llms
