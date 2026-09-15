---
title: Introduction to the Model Context Protocol (MCP)
notetype: feed
date: 2025-10-04
last_modified: 2026-09-16
tags: [llm, mcp, ai, tools]
status: published
---

# [Source: Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](https://arxiv.org/abs/2503.23278)

MCP คือโปรโตคอลมาตรฐานที่ให้แอป AI เชื่อมต่อกับเครื่องมือและแหล่งข้อมูลภายนอกผ่านวิธีการเดียวกัน ช่วยลดปัญหาข้อมูลแยกอยู่ในหลายระบบและลดงานเขียนตัวเชื่อมต่อเฉพาะทาง

## Timeline (ChatGPT - Tools)
- พ.ย. 2022 — เปิดตัว ChatGPT (จุดเริ่ม “ยุคแชตบอต”)
- มี.ค. 2023 — ChatGPT Plugins (เริ่ม “ต่อเครื่องมือ/เว็บ”)
- ก.ค. 2023 — Code Interpreter (ต่อมาเรียก Advanced Data Analysis)
- ก.ค. 2023 — **[Function Calling (ทางการสำหรับ Dev)](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api)**
- ก.ย. 2023 — ChatGPT “กลับมาท่องเว็บได้” (Browse) อย่างเป็นทางการ
- พ.ย. 2023 — DevDay: GPT-4 Turbo, Assistants API & “Agent-like experiences”
- พ.ย. 2023 — “GPTs” (ChatGPT Apps/Custom GPT) เปิดให้ผู้ใช้สร้างผู้ช่วยเฉพาะงาน
- ม.ค. 2024 — GPT Store (คลังแอป GPT สาธารณะ)
- พ.ค. 2024 — GPT-4o (Omni) รองรับการทำงานแบบ real-time และข้อมูลหลายรูปแบบ
- ก.ค. 2024 — SearchGPT ต้นแบบการค้นหาข้อมูลผ่านบทสนทนา
- ก.ย. 2024 — รุ่น reasoning ตระกูล o1 (“คิดก่อนตอบ”)
- พ.ย. 2024 — **[Anthropic เปิดตัว MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro)**
- มี.ค. 2025 — Responses API & Agents SDK (ยุคเอเจนต์สำหรับนักพัฒนา)

## 1.Introduction
- AI agent ใช้เครื่องมือภายนอกมากขึ้นตั้งแต่ปี 2023
- หลังจาก OpenAI เปิดตัว function calling Anthropic ก็เปิดตัว MCP ในปี 2024
- MCP ช่วยให้ AI ค้นหาและเรียกใช้เครื่องมือผ่านอินเทอร์เฟซมาตรฐาน
- งานวิจัยนี้วิเคราะห์ MCP ทั้งด้านสถาปัตยกรรม ระบบนิเวศ และความปลอดภัย

---

## 2.Background and Motivation
![Tools_w_wo_MCP](/assets/img/Other/LLM/Tools_w_wo_MCP.avif)
- AI Tooling
  - ก่อนมี MCP นักพัฒนาต้องเขียนโค้ดเชื่อมต่อ API แต่ละตัวเอง ทำให้ระบบซับซ้อนและดูแลยาก
  - อินเทอร์เฟซแบบปลั๊กอิน เช่น ChatGPT Plugins ช่วยแก้ปัญหาบางส่วน แต่ยังมีข้อจำกัด
  - Frameworks อย่าง LangChain ช่วยรวมเครื่องมือ แต่ยังไม่เป็นมาตรฐาน
  - MCP ให้วิธีมาตรฐานสำหรับเชื่อมแอป AI กับเครื่องมือภายนอก

- Motivation
  - MCP ช่วยลดภาระของนักพัฒนาและเพิ่มความยืดหยุ่นของ agent แต่ยังต้องศึกษาปัญหาด้านความปลอดภัย การค้นพบเครื่องมือ และการกำกับดูแล

---

## 3.MCP Architecture

![MCP Architecture](/assets/img/Other/LLM/MCP_Architecture.avif)


- Core Components
  - MCP Host: แอป AI เช่น Cursor, Claude Desktop
  - MCP Client: ตัวกลางสื่อสารระหว่าง host และ server
  - MCP Server: เปิดให้เข้าถึงเครื่องมือ แหล่งข้อมูล และ prompt templates

![MCP_Workflow](/assets/img/Other/LLM/MCP_Workflow.avif)

![MCP Lifecycle](/assets/img/Other/LLM/MCP_Life_cycle.avif)

---

## 4.Security and Privacy Analysis

### MCP Server Lifecycle

![MCP Server Lifecycle](/assets/img/Other/LLM/MCP_Server_LF.avif)

- Creation Phase
  - Name Collision: เซิร์ฟเวอร์ปลอมใช้ชื่อใกล้เคียงกับของจริง
  - Installer Spoofing: ตัวติดตั้งถูกดัดแปลงให้มี backdoor
  - Code Injection: ฝังโค้ดอันตรายในซอร์สโค้ด

- Operation Phase
  - Tool Name Conflict: เครื่องมือชื่อซ้ำกันอาจทำให้เรียกใช้ผิดตัว
  - Slash Command Overlap: คำสั่งของเครื่องมือต่างตัวใช้ชื่อซ้ำกัน
  - Sandbox Escape: เครื่องมือหลุดจากสภาพแวดล้อมที่จำกัดสิทธิ์และเข้าถึงระบบหลัก

- Update Phase
  - Privilege Persistence: สิทธิ์ผู้ใช้ไม่ถูกรีเซ็ตหลังอัปเดต
  - Redeploy Vulnerable Versions: ติดตั้งเวอร์ชันเก่าที่มีช่องโหว่
  - Configuration Drift: ค่าตั้งค่าเปลี่ยนไปจากมาตรฐานที่กำหนด

### [MCP-Client and MCP-Server] Name Collision Issue (ชื่อซ้ำ)
- Problem
  - ผู้โจมตีตั้งชื่อ MCP server ให้เหมือนหรือคล้ายของจริง เช่น mcp-github เลียนแบบ github-mcp เพื่อหลอกให้ผู้ใช้หรือ agent ติดตั้งผิดตัว โดยอาศัยการเลือกจากชื่อและคำอธิบาย
- Impact
  - ข้อมูลอ่อนไหวอาจถูกดักอ่านหรือแก้ไข ผู้โจมตีอาจสั่งงานแทนผู้ใช้ และทำให้ขั้นตอนการทำงานผิดไปจากที่ตั้งใจ
- Solution
  - กำหนด allowlist และตรึงแหล่งแพ็กเกจหรือผู้เผยแพร่ที่เชื่อถือได้ ก่อนอนุญาตให้ agent ใช้งาน
  - แสดงผู้เผยแพร่และ fingerprint ให้ชัดเจนในหน้าจอไคลเอนต์ พร้อมเตือนเมื่อชื่อคล้ายเซิร์ฟเวอร์ที่รู้จัก
  - ระยะยาว: กำหนดนโยบาย namespace ใช้ลายเซ็นดิจิทัลยืนยันตัวตนเซิร์ฟเวอร์ และสร้างระบบประเมินความน่าเชื่อถือสำหรับการลงทะเบียนและค้นหา

### [MCP-Server] Installer Spoofing 
- Problem
  - การตั้งค่า MCP server ด้วยตนเองมีหลายขั้นตอน จึงมีเครื่องมือติดตั้งอัตโนมัติจากชุมชน เช่น Smithery-CLI, mcp-get และ mcp-installer เครื่องมือเหล่านี้เพิ่มความเสี่ยงจากห่วงโซ่อุปทานซอฟต์แวร์ หากแพ็กเกจถูกดัดแปลงหรือฝังโค้ดอันตราย
  - ผู้โจมตีอาจแนบมัลแวร์หรือ backdoor เปลี่ยนค่าตั้งค่า หรือฝังกลไกให้กลับมาเข้าถึงระบบได้หลังติดตั้ง โดยผู้ใช้อาจไม่ได้ตรวจซอร์สโค้ดของตัวติดตั้ง
- Impact
  - ผู้โจมตีอาจได้สิทธิ์ในเครื่อง เปลี่ยนค่าตั้งค่า ส่งข้อมูลออกนอกระบบ หรือติดตั้งเซิร์ฟเวอร์ที่ดัดแปลงไว้เพื่อรอรับคำสั่ง
- Solution
  - ติดตั้งจากแหล่งที่ตรวจสอบได้ และตรวจ checksum หรือลายเซ็นทุกครั้ง
  - ตรึงเวอร์ชัน (pin) และรันตัวติดตั้งกับเซิร์ฟเวอร์ใน sandbox/container ที่ไม่ใช้สิทธิ์ root โดยปฏิเสธการเข้าถึงไฟล์และเครือข่ายไว้ก่อน แล้วอนุญาตเฉพาะที่จำเป็น
  - ตรวจ SBOM และ dependencies พร้อมเปิด audit log สำหรับการเปลี่ยนค่าตั้งค่าและการใช้เครือข่าย
  - ระยะยาว: พัฒนามาตรฐานการติดตั้ง การตรวจสอบแพ็กเกจ และระบบประเมินความน่าเชื่อถือของตัวติดตั้งอัตโนมัติ

### [MCP-Server] Sandbox Escape
- Problem
  - แม้จะรันเครื่องมือ MCP ใน sandbox เพื่อจำกัดการเข้าถึงระบบหลัก ผู้โจมตีก็อาจใช้ช่องโหว่ของ sandbox/container runtime, system calls, ไลบรารีภายนอก หรือ side-channel เพื่อออกไปยังโฮสต์และยกระดับสิทธิ์
  - งานวิจัยระบุภัยนี้ไว้ในช่วงการทำงาน (operation phase) ของวงจรชีวิต MCP server
- Impact
  - โค้ดอันตรายอาจทำงานบนโฮสต์และเข้าถึงข้อมูลนอก sandbox รวมถึงทำให้ผู้โจมตียึดเครื่องหรือคลัสเตอร์ที่ agent ใช้งาน
- Solution
  - ใช้ runtime ที่แยกสภาพแวดล้อมเข้มงวด เช่น gVisor/Firecracker ร่วมกับ seccomp/AppArmor/SELinux ลด Linux capabilities และใช้ rootless containers
  - กำหนดระบบไฟล์ให้อ่านอย่างเดียวและไม่ผูกโฟลเดอร์จากโฮสต์เข้ามาโดยปริยาย ส่วนเครือข่ายให้ปฏิเสธไว้ก่อนแล้วอนุญาตเฉพาะปลายทางใน allowlist
  - ใช้โทเคนอายุสั้น หมุนเวียนคีย์ อัปเดตแพตช์ runtime และไลบรารีสม่ำเสมอ พร้อมซ้อมรับมือ sandbox escape ตามกรณีที่งานวิจัยยกมา

---

## 5.Application and MCP Server

### Application

| Category                         | Company/Product               | Key Features or Use Cases                                                          |
| -------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| **AI Models and Frameworks**     | Anthropic (Claude)            | Full MCP support in the desktop version, enabling interaction with external tools. |
|                                  | OpenAI                        | MCP support in Agent SDK and API for seamless integration.                         |
|                                  | Baidu Maps                    | API integration using MCP to access geolocation services.                          |
|                                  | Blender MCP                   | Enables Blender and Unity 3D model generation via natural language commands.       |
| **Developer Tools**              | Replit                        | AI-assisted development environment with MCP tool integration.                     |
|                                  | Microsoft Copilot Studio      | Extends Copilot Studio with MCP-based tool integration.                            |
|                                  | Sourcegraph Cody              | Implements MCP through OpenCTX for resource integration.                           |
|                                  | Codeium                       | Adds MCP support for coding assistants to facilitate cross-system tasks.           |
|                                  | Cursor                        | MCP tool integration in Cursor Composer for seamless code execution.               |
|                                  | Cline                         | VS Code coding agent that manages MCP tools and servers.                           |
| **IDEs/Editors**                 | Zed                           | Provides slash commands and tool integration based on MCP.                         |
|                                  | JetBrains                     | Integrates MCP for IDE-based AI tooling.                                           |
|                                  | Windsurf Editor               | AI-assisted IDE with MCP tool interaction.                                         |
|                                  | TheiaAI/TheiaIDE              | Enables MCP server interaction for AI-powered tools.                               |
|                                  | Emacs MCP                     | Enhances AI functionality in Emacs by supporting MCP tool invocation.              |
|                                  | OpenSumi                      | Supports MCP tools in IDEs and enables seamless AI tool integration.               |
| **Cloud Platforms and Services** | Cloudflare                    | Provides remote MCP server hosting and OAuth integration.                          |
|                                  | Block (Square)                | Uses MCP to enhance data processing efficiency for financial platforms.            |
|                                  | Stripe                        | Exposes payment APIs via MCP for seamless AI integration.                          |
| **Web Automation and Data**      | Apify MCP Tester              | Connects to any MCP server using SSE for API testing.                              |
|                                  | LibreChat                     | Extends the current tool ecosystem through MCP integration.                        |
|                                  | Goose                         | Allows building AI agents with integrated MCP server functionality.                |



### MCP Server

| Collection | Author | Mode | # Servers | URL |
|---|---|---|---:|---|
| MCP.so | mcp.so | Website | 4774 | mcp.so |
| Glama | glama.ai | Website | 3356 | glama.ai |
| PulseMCP | Antanavicius et al. | Website | 3164 | pulsemcp.com |
| Smithery | Henry Mao | Website | 2942 | smithery.ai |
| Dockmaster | mcp-dockmaster | Desktop App | 517 | mcp-dockmaster.com |
| **Official Collection** | **Anthropic** | **GitHub Repo** | **320** | **modelcontextprotocol/servers** |
| AiMCP | Hekmon | Website | 313 | aimcp.info |
| MCP.run | mcp.run | Website | 114 | mcp.run |
| Awesome MCP Servers | Stephen Akinyemi | GitHub Repo | 88 | appcypher/mcp-servers |
| mcp-get registry | Michael Latman | Website | 59 | mcp-get.com |
| Awesome MCP Servers | wong2 | Website | 34 | mcpservers.org |
| OpenTools | opentoolsteam | Website | 25 | opentools.com |
| Toolbase | gching | Desktop App | 20 | gettoolbase.ai |
| make inference | mkinf | Website | 20 | mkinf.io |
| Awesome Crypto MCP Servers | Luke Fan | GitHub Repo | 13 | badkk/crypto-mcp-servers |



## Useful link
- [Function Call OpenAI](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api)
- [Anthropic MCP Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Anthropic MCP Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
