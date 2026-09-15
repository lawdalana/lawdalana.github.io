---
title : Claude Code
notetype : feed
date : 19-07-2025
last_modified: 2026-09-16
---

# [Claude Code](https://www.anthropic.com/claude-code)

- [Claude Code](#claude-code)
  - [❔คืออะไร (What is it)](#คืออะไร-what-is-it)
  - [งานที่ Claude Code ช่วยได้ดี](#usecase-ไหนบ้างที่-claude-code-สามารถทำงานได้ดี)
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
Claude Code เป็นเครื่องมือเขียนโค้ดที่ทำงานเป็น agent ผ่านบรรทัดคำสั่ง (CLI) โดยใช้โมเดล Claude เช่น Opus หรือ Sonnet ช่วยอ่านโค้ดในโปรเจกต์ เลือกไฟล์ที่เกี่ยวข้อง สร้าง แก้ไข หรือ refactor โค้ด รันคำสั่ง shell และจัดการงาน Git ตามคำสั่งภาษาปกติ

---
<a id="usecase-ไหนบ้างที่-claude-code-สามารถทำงานได้ดี"></a>

## [งานที่ Claude Code ช่วยได้ดี](https://www.facebook.com/share/p/16qvfvKsVW/)

### 🟡 Data Infrastructure
```
ใช้ทำ: อัปเดตเอกสาร, วิเคราะห์โค้ด, ทำให้ทีมอื่นเข้าใจโค้ดง่ายขึ้น
เทคนิคเด่น:
 • เขียน CLAUDE.md ให้มีบริบทและข้อกำหนดที่ชัดเจน เพื่อช่วยให้ Claude ทำงานได้ตรงโจทย์
 • แชร์ session การใช้งาน Claude ภายในทีม เพื่อสร้างแนวปฏิบัติร่วม
 • ใช้ MCP servers เชื่อมต่อเครื่องมือที่ Claude ต้องใช้ พร้อมกำหนดสิทธิ์ให้เหมาะสม
```

### 🟢 Claude Code (Product Dev)
```
ใช้ทำ: สร้าง prototype ฟีเจอร์ใหม่ และ unit tests
เทคนิคเด่น:
 • สร้าง loop อัตโนมัติให้ Claude ตรวจผลและทำซ้ำ
 • เขียน prompt ให้ละเอียด เพื่อให้ Claude ทำงานต่อได้ด้วยตัวเอง
 • แบ่งประเภทงานและกำหนดวิธีติดตามการทำงานให้ชัดเจน
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
ใช้ทำ: อธิบายโค้ด เตรียมเอกสารให้ผู้เริ่มใช้งาน และแปลคำสั่งหลายภาษา
เทคนิคเด่น:
 • ใช้ Claude ตรวจว่า “รู้อะไรมากกว่า Google” ก่อนเริ่ม
 • ให้ Claude สร้างโค้ดร่าง แล้วตรวจทานก่อนนำไปใช้
 • ใช้ Claude ช่วยทำฉบับร่าง เพื่อให้มีเวลาตรวจและแก้ไขก่อนกำหนดส่ง
```

### 🟠 Data Science & ML Engineering
```
ใช้ทำ: เขียน dashboard JS/TS, วิเคราะห์ข้อมูลซ้ำ ๆ
เทคนิคเด่น:
 • ให้ Claude ช่วยจัดลำดับความสำคัญ → ลองถาม “ทำไมทำสิ่งนี้?”
 • ให้ Claude จดบันทึกแทนใน Notebooks
 • มอบหมายงานให้ Claude ช่วย โดยลดส่วนที่ต้องเขียนโค้ดเอง
```

### 🔴 API Knowledge
```
ใช้ทำ: วางแผน API และลดการสลับไปมาระหว่างเครื่องมือหรือเอกสาร
เทคนิคเด่น:
 • ใช้ Claude ช่วยปรับ prompt เป็นรอบ ๆ
 • ให้ Claude เริ่มจากข้อมูลให้น้อยที่สุดก่อน แล้วค่อยเติม
 • ใช้ Claude ช่วยทำความเข้าใจและพัฒนาโค้ดในส่วนที่ยังไม่คุ้นเคย
```

### 🟤 Growth Marketing
```
ใช้ทำ: สร้างโฆษณาอัตโนมัติ, วิเคราะห์ Meta Ads, เขียนคอนเทนต์
เทคนิคเด่น:
 • เลือกงานที่ต้องทำซ้ำ แล้วให้ Claude ช่วยทำโดยอัตโนมัติ
 • แยก workflow เป็น sub-agent แต่ละงาน เพื่อปรับแต่ง
 • ระดมความคิดกับ Claude ก่อนเริ่มงาน เพื่อช่วยจัดลำดับสิ่งที่ต้องทำ
```

### 🟡 Product Design
```
ใช้ทำ: Rapid prototyping, แก้ไข state management
เทคนิคเด่น:
 • เตรียมไฟล์ memory ที่บันทึกบริบทและข้อกำหนดของงานออกแบบให้ Claude
 • ใช้ Claude อ่านและสรุประบบ backend
 • วางภาพ UI ลงไป → Claude สร้าง prototype จากภาพได้เลย
```

### 🟢 RL Engineering
```
ใช้ทำ: Debug โค้ด, วิเคราะห์ stack, จัดการ Kubernetes
เทคนิคเด่น:
 • ปรับ prompt เพื่อหลีกเลี่ยงการเรียกเครื่องมือซ้ำ
 • สร้าง workflow ที่ rollback ได้
 • ให้ Claude ลองทำรอบแรก แล้วค่อยตรวจทานและปรับแก้เป็นรอบ ๆ
```

### 🔵 Legal
```
ใช้ทำ: เขียนสัญญา, วิเคราะห์ความเสี่ยง, สื่อสารกับครอบครัวผู้ใช้
เทคนิคเด่น:
 • วางแผนเอกสารใน Claude ก่อน แล้วค่อยจัดทำจริง
 • ใช้ภาพหรือแผนภาพช่วยอธิบายผลลัพธ์
 • ใช้ prototype ช่วยสื่อสารแนวคิดใหม่
```

### 📌 ข้อคิดจากทีม Anthropic
```
 • เอกสาร CLAUDE.md ที่ละเอียดช่วยให้ Claude มีบริบทในการทำงาน
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
> ระยะเวลาที่ **Claude Code** เก็บข้อมูลขึ้นอยู่กับประเภทบัญชีและการตั้งค่าความเป็นส่วนตัว ส่วนข้อมูลที่ส่งเป็น feedback อาจมีเงื่อนไขต่างจากบทสนทนาทั่วไป ดูรายละเอียดใน [นโยบายการใช้และเก็บข้อมูลของ Claude Code](https://code.claude.com/docs/en/data-usage)


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
| `/doctor`             | Check the health of your Claude Code installation                                                               |
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
| `/upgrade`            | Upgrade to Max for higher rate limits and more access to Opus                                                   |
| `/vim`                | Toggle between Vim and Normal editing modes                                                                     |

---
