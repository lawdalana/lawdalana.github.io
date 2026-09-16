---
title: "Agent Harness Engineering"
notetype: feed
date: 2026-09-16
last_modified: 2026-09-16
tags: [AI, AI-agents, agentic-engineering, harness-engineering, context-engineering]
status: published
---

# Agent Harness Engineering: ระบบรอบโมเดล

> สรุปและเรียบเรียงภาษาไทยจาก [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) โดย Addy Osmani — 19 เมษายน 2026

![ภาพปก Agent Harness Engineering](/assets/img/LLM/Agentic-Engineering/agent-harness.jpg)

*ภาพปก: [Addy Osmani](https://addyosmani.com/assets/images/agent-harness.jpg)*

## TL;DR

**Harness** คือระบบรอบโมเดล เช่น instructions, tools, context, sandbox และวงจรตรวจงาน ผู้เขียนเสนอให้ปรับระบบนี้จากข้อผิดพลาดจริง

## ออกแบบตามหน้าที่

| หน้าที่ | ส่วนของ harness |
|---|---|
| เก็บงานและย้อนกลับ | Filesystem และ Git |
| ลงมือทำอย่างจำกัดขอบเขต | Tools และ sandbox |
| ตรวจความถูกต้อง | Tests และ hooks |
| ทำงานข้าม session | แผนและบันทึกสถานะ |

![โมเดลกลางระบบบริบท เครื่องมือ การควบคุม และการตรวจสอบ](/assets/img/LLM/Agentic-Engineering/harness-anatomy.jpeg)

*แผนภาพ: [ต้นฉบับของ Addy Osmani](https://addyosmani.com/assets/images/harness-anatomy.jpeg)*

## เรียนรู้จากความผิดพลาด

**Hooks บังคับขั้นตอน** และส่งผลทดสอบที่ล้มเหลวกลับให้แก้ ส่วน `AGENTS.md` เก็บกติกาสั้น ๆ ที่มีเหตุผลรองรับ

## จัดการ context

สรุปบริบทเก่า เก็บ log ยาวในไฟล์ และโหลด skills เมื่อจำเป็น เมื่อโมเดลเปลี่ยน ควรทบทวนส่วนของ harness ที่หมดประโยชน์ด้วย

## Related Notes

- [[The New Software Lifecycle]]
- [[The Factory Model]]
- [[Agentic Code Review]]
- [[The Orchestration Tax]]

## Reference

- [Addy Osmani — Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — อ่านเมื่อ 16 กันยายน 2026
