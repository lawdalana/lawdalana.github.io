---
title : Claude Code
notetype : feed
date : 19-07-2025
---

# [Claude Code](https://www.anthropic.com/claude-code)

- [Claude Code](#claude-code)
  - [❔คืออะไร (What is it)](#คืออะไร-what-is-it)
  - [UseCase ไหนบ้างที่ Claude code สามารถทำงานได้ดี](#usecase-ไหนบ้างที่-claude-code-สามารถทำงานได้ดี)
    - [🟡 Data Infrastructure](#-data-infrastructure)
    - [🟢 Claude Code (Product Dev)](#-claude-code-product-dev)
    - [🔵 Security Engineering](#-security-engineering)
    - [🟣 Inference](#-inference)
    - [🟠 Data Science \& ML Engineering](#-data-science--ml-engineering)
    - [🔴 API Knowledge](#-api-knowledge)
    - [🟤 Growth Marketing](#-growth-marketing)
    - [🟡 Product Design](#-product-design)
    - [🟢 RL Engineering](#-rl-engineering)
    - [🔵 Legal](#-legal)
    - [📌 ข้อคิดจากทีม Anthropic](#-ข้อคิดจากทีม-anthropic)
  - [ตัวอย่าง command](#ตัวอย่าง-command)


## ❔คืออะไร (What is it)
Claude Code คือ “agentic coding tool” (เครื่องมือช่วยเขียนโค้ดเชิงตัวแทน) แบบบรรทัดคำสั่ง (CLI) ที่ฝังโมเดล Claude (เช่น Opus / รุ่น Sonnet ล่าสุด) ลงในเทอร์มินัล ให้มัน เข้าใจโค้ดเบสทั้งโปรเจ็กต์, เลือกไฟล์ที่เกี่ยวข้องเอง, แก้ / สร้าง / refactor โค้ด, รันคำสั่ง shell และจัดการเวิร์กโฟลว์ Git ผ่านภาษามนุษย์ เพื่อเร่งความเร็วการพัฒนาแบบ end-to-end.

---
## [UseCase ไหนบ้างที่ Claude code สามารถทำงานได้ดี](https://www.facebook.com/share/p/16qvfvKsVW/)

### 🟡 Data Infrastructure
```
ใช้ทำ: อัปเดตเอกสาร, วิเคราะห์โค้ด, ทำให้ทีมอื่นเข้าใจโค้ดง่ายขึ้น
เทคนิคเด่น:
 • เขียน Claude.md แบบละเอียด จะช่วยให้ Claude ทำงานได้ดีขึ้น
 • แชร์ session การใช้งาน Claude ภายในทีม เพื่อสร้างแนวปฏิบัติร่วม
 • ใช้ Claude ช่วยจัดการสิทธิ์ผ่าน MCP servers ที่ปลอดภัยกว่า CLI เดิม
```

### 🟢 Claude Code (Product Dev)
```
ใช้ทำ: Prototype, สร้างฟีเจอร์ใหม่, สร้าง unit test
เทคนิคเด่น:
 • สร้าง loop อัตโนมัติให้ Claude ตรวจผลและทำซ้ำ
 • เขียน prompt แบบละเอียด เพื่อให้ Claude ทำงาน autonomously ได้
 • แยกการตั้งชื่อ task classification และระบบ supervision ออกให้ชัด
```

### 🔵 Security Engineering
```
ใช้ทำ: วิเคราะห์โค้ด infrastructure, สลับบริบท test/dev
เทคนิคเด่น:
 • ใช้ Claude กับ command line เพื่อรันงานซ้ำ ๆ
 • ให้ Claude จัดรูปแบบโค้ด (format as you go)
 • ช่วยเขียนเอกสาร DevSecOps ได้ไวขึ้น
```

### 🟣 Inference
```
ใช้ทำ: อธิบายโค้ด, เตรียม onboarding, แปลคำสั่งหลายภาษา
เทคนิคเด่น:
 • ใช้ Claude ตรวจว่า “รู้อะไรมากกว่า Google” ก่อนเริ่ม
 • เริ่มจากให้ Claude generate โค้ด → แล้วค่อย review
 • ใช้ Claude ทำ first draft ช่วยลดแรงกดดันจาก deadline
```

### 🟠 Data Science & ML Engineering
```
ใช้ทำ: เขียน dashboard JS/TS, วิเคราะห์ข้อมูลซ้ำ ๆ
เทคนิคเด่น:
 • ให้ Claude ช่วยจัดลำดับความสำคัญ → ลองถาม “ทำไมทำสิ่งนี้?”
 • ให้ Claude จดบันทึกแทนใน Notebooks
 • delegate task โดยไม่ต้องผ่านโค้ดหนัก
```

### 🔴 API Knowledge
```
ใช้ทำ: วางแผน API, ลดการ switch context
เทคนิคเด่น:
 • ใช้ Claude เป็น partner ในการ iterate prompt
 • ให้ Claude เริ่มจากข้อมูลให้น้อยที่สุดก่อน แล้วค่อยเติม
 • ใช้ Claude ช่วย build มั่นใจแม้ในโค้ดที่ไม่ถนัด
```

### 🟤 Growth Marketing
```
ใช้ทำ: สร้างโฆษณาอัตโนมัติ, วิเคราะห์ Meta Ads, เขียนคอนเทนต์
เทคนิคเด่น:
 • คัด task ซ้ำ → ให้ Claude ทำอัตโนมัติ
 • แยก workflow เป็น sub-agent แต่ละงาน เพื่อปรับแต่ง
 • brainstorm กับ Claude ก่อนเริ่มงานจริง ช่วยจัดลำดับความคิด
```

### 🟡 Product Design
```
ใช้ทำ: Rapid prototyping, แก้ไข state management
เทคนิคเด่น:
 • เตรียมไฟล์ memory สำหรับ Claude ใช้แทนดีไซน์
 • ใช้ Claude อ่านและสรุประบบ backend
 • วางภาพ UI ลงไป → Claude สร้าง prototype จากภาพได้เลย
```

### 🟢 RL Engineering
```
ใช้ทำ: Debug โค้ด, วิเคราะห์ stack, จัดการ Kubernetes
เทคนิคเด่น:
 • ปรับ prompt เพื่อหลีกเลี่ยงการเรียกเครื่องมือซ้ำ
 • สร้าง workflow ที่ rollback ได้
 • ให้ Claude ทำ first try ก่อน แล้วค่อย review เป็นรอบ ๆ
```

### 🔵 Legal
```
ใช้ทำ: เขียนสัญญา, วิเคราะห์ความเสี่ยง, สื่อสารกับครอบครัวผู้ใช้
เทคนิคเด่น:
 • วางแผนเอกสารใน Claude ก่อน แล้วค่อยจัดทำจริง
 • แสดงผลลัพธ์แบบ visual ให้เข้าใจง่าย
 • แชร์ prototype แม้เป็นไอเดียใหม่ (Claude รับมือได้)
```

### 📌 ข้อคิดจากทีม Anthropic
```
 • Claude ทำงานได้ดีมากเมื่อมีเอกสาร Claude.md ที่ละเอียด
 • ให้ Claude “ทำเองก่อน” แล้วเราค่อย review เป็นรอบ
 • เขียน prompt แบบแยกปัญหาใหญ่เป็นส่วนย่อย ทำให้ Claude ตอบแม่นขึ้น
 • ใช้ภาพ, code block และ memory file เพื่อช่วยให้ Claude เข้าใจ context ได้เร็ว
```

> ℹ️ **Reference**
> - [How Anthropic teams
use Claude Code](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
> - [UseCase ไหนบ้างที่ Claude code สามารถทำงานได้ดี](https://www.facebook.com/share/p/16qvfvKsVW/)
> - [Claude Code](https://www.anthropic.com/claude-code)

> ⚠️ **Warning**
>  
> Be careful when using **Claude Code**: data is retained for **2 years** by default, and can be stored for up to **7 years** if the appropriate flag is set.


---

## ตัวอย่าง command

| Command               | Description                                                                                                     |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| `/add-dir`            | Add a new working directory                                                                                     |
| `/bug`                | Submit feedback about Claude Code                                                                               |
| `/clear`              | Clear conversation history and free up context                                                                  |
| `/compact`            | Clear conversation history but keep a summary in context. Optional: `/compact [instructions for summarization]` |
| `/config`             | Open config panel                                                                                               |
| `/cost`               | Show the total cost and duration of the current session                                                         |
| `/doctor`             | Checks the health of your Claude Code installation                                                              |
| `/exit`               | Exit the REPL                                                                                                   |
| `/help`               | Show help and available commands                                                                                |
| `/ide`                | Manage IDE integrations and show status                                                                         |
| `/init`               | Initialize a new CLAUDE.md file with codebase documentation                                                     |
| `/install-github-app` | Set up Claude GitHub Actions for a repository                                                                   |
| `/login`              | Sign in with your Anthropic account                                                                             |
| `/logout`             | Sign out from your Anthropic account                                                                            |
| `/mcp`                | Manage MCP servers                                                                                              |
| `/memory`             | Edit Claude memory files                                                                                        |
| `/migrate-installer`  | Migrate from global npm installation to local installation                                                      |
| `/model`              | Set the AI model for Claude Code                                                                                |
| `/permissions`        | Manage allow & deny tool permission rules                                                                       |
| `/pr-comments`        | Get comments from a GitHub pull request                                                                         |
| `/release-notes`      | View release notes                                                                                              |
| `/resume`             | Resume a conversation                                                                                           |
| `/review`             | Review a pull request                                                                                           |
| `/status`             | Show Claude Code status including version, model, account, API connectivity, and tool statuses                  |
| `/upgrade`            | Upgrade to Max for higher rate limits and more Opus                                                             |
| `/vim`                | Toggle between Vim and Normal editing modes                                                                     |

---
