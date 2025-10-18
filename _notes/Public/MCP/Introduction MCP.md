---
title: Introduction Model Context Protocal (MCP)
notetype: feed
date: 2025-10-04
last_modified: 2025-10-04
tags: [llm, mcp, ai, tools]
status: published
---

# [Source: Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](https://arxiv.org/abs/2503.23278)

MCP คืออะไร: โปรโตคอลมาตรฐานที่ทำให้ AI คุยกับ “เครื่องมือ-ข้อมูลภายนอก” ได้แบบเป็นระบบเดียวกัน ลด data silos และเพิ่มการทำงานข้ามระบบอย่างไร้รอยต่อ. เป็นมาตรฐานใหม่ที่ทำให้ AI สามารถสื่อสารกับเครื่องมือและแหล่งข้อมูลภายนอกได้อย่างราบรื่น

## Timeline (ChatGPT - Tools)
- พ.ย. 2022 — เปิดตัว ChatGPT (จุดเริ่ม “ยุคแชตบอต”)
- มี.ค. 2023 — ChatGPT Plugins (เริ่ม “ต่อเครื่องมือ/เว็บ”)
- ก.ค. 2023 — Code Interpreter (ต่อมาเรียก Advanced Data Analysis)
- *ก.ค. 2023 — **[Function Calling (ทางการสำหรับ Dev)](https://help.openai.com/en/articles/8555517-function-calling-in-the-openai-api)**
- ก.ย. 2023 — ChatGPT “กลับมาท่องเว็บได้” (Browse) อย่างเป็นทางการ
- พ.ย. 2023 — DevDay: GPT-4 Turbo, Assistants API & “Agent-like experiences”
- พ.ย. 2023 — “GPTs” (ChatGPT Apps/Custom GPT) ให้ใครๆ สร้างแอปย่อยได้
- ม.ค. 2024 — GPT Store (คลังแอป GPT สาธารณะ)
- พ.ค. 2024 — GPT-4o (Omni) โหมดเรียลไทม์/มัลติโมดัลเต็มรูป
- ก.ค. 2024 — SearchGPT (ต้นแบบ “ChatGPT ที่ค้นหาได้แบบ Search เต็มตัว”)
- ก.ย. 2024 — รุ่น reasoning ตระกูล o1 (“คิดก่อนตอบ”)
- *พ.ย. 2024 — **[Anthropic เปิดตัว MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro)**
- มี.ค. 2025 — Responses API & Agents SDK (ยุคเอเจนต์สำหรับนักพัฒนา)

## 1.Introduction
- พัฒนาการของ AI agent ที่ใช้เครื่องมือภายนอกเพิ่มขึ้นอย่างมากตั้งแต่ปี 2023
- OpenAI เปิดตัว function calling → Anthropic พัฒนาเป็น MCP ในปี 2024
- MCP ช่วยให้ AI ค้นหาและใช้เครื่องมือได้อย่างอิสระ ไม่ต้องกำหนดล่วงหน้า
- งานวิจัยเป็นการวิเคราะห์เชิงลึกครั้งแรกของ MCP ทั้งสถาปัตยกรรม ระบบนิเวศ และความปลอดภัย

---

## 2.Background and Motivation
![Tools_w_wo_MCP](/assets/img/Other/LLM/Tools_w_wo_MCP.avif)
- AI Tooling
  - ก่อนมี MCP นักพัฒนาต้องเขียน API เชื่อมต่อเอง (manual API wiring) → ซับซ้อนและเปราะบาง
  - Plugin interfaces เช่น ChatGPT Plugins แก้บางส่วนแต่ยังจำกัด
  - Frameworks อย่าง LangChain ช่วยรวมเครื่องมือ แต่ยังไม่เป็นมาตรฐาน
  - MCP ทำให้ AI เชื่อมต่อและประมวลผลกับเครื่องมือภายนอกได้แบบรวมศูนย์

- Motivation
  - MCP ช่วยลดภาระของนักพัฒนาและเพิ่มความยืดหยุ่นของ agent แต่ยังมีช่องว่างด้าน security, discoverability และ governance → ต้องมีงานวิจัยต่อเนื่อง

---

## 3.MCP Architecture

![MCP Architecture](/assets/img/Other/LLM/MCP_Architecture.avif)


- Core Components
  - MCP Host: แอป AI เช่น Cursor, Claude Desktop
  - MCP Client: ตัวกลางสื่อสารระหว่าง host และ server
  - MCP Server: จัดการการเข้าถึงเครื่องมือ, แหล่งข้อมูล, และ prompt templates

![MCP_Workflow](/assets/img/Other/LLM/MCP_Workflow.avif)

![MCP Lifecycle](/assets/img/Other/LLM/MCP_Life_cycle.avif)

---

## 4.Security and Privacy Analysis

### MCP Server Lifecycle

![MCP Server Lifecycle](/assets/img/Other/LLM/MCP_Server_LF.avif)

- Creation Phase
  - Name Collision: เซิร์ฟเวอร์ปลอมชื่อใกล้เคียงของจริง
  - Installer Spoofing: ตัวติดตั้งถูกแก้ไขให้มี backdoor
  - Code Injection: ฝังโค้ดอันตรายลงใน source

- Operation Phase
  - Tool Name Conflict: เครื่องมือชื่อเหมือนกัน → เรียกใช้ผิด
  - Slash Command Overlap: คำสั่งซ้ำกันระหว่าง tools
  - Sandbox Escape: เครื่องมือออกจากสภาพแวดล้อมจำกัดและเข้าควบคุมระบบหลัก

- Update Phase
  - Privilege Persistence: สิทธิ์ผู้ใช้ไม่ถูกรีเซ็ตหลังอัปเดต
  - Redeploy Vulnerable Versions: ติดตั้งเวอร์ชันเก่าที่มีช่องโหว่
  - Configuration Drift: ค่าการตั้งค่าเบี่ยงเบนจากมาตรฐาน

### [MCP-Client and MCP-Server] Name Collision Issue (ชื่อซ้ำ)
- Problem
  - ผู้โจมตีจงใจจดทะเบียน MCP server ที่ชื่อ “เหมือนหรือคล้าย” ของจริง (เช่น mcp-github เลียนแบบ github-mcp) เพื่อให้ผู้ใช้/เอเจนต์ติดตั้งผิดตัว เพราะไคลเอนต์ MCP อาศัย “ชื่อและคำอธิบาย” เป็นหลักตอนเลือกเซิร์ฟเวอร์
- Impact
  - ข้อมูลอ่อนไหวถูกดัก/แก้ไข, คำสั่งสำคัญถูกสั่งโดยผู้โจมตี, เวิร์กโฟลว์ล้มเหลวหรือถูกบิดเบือน
- Solution
  - ใช้ allowlist/pinning ของ “ผู้พัฒนา/ผู้จัดการแพ็กเกจที่เชื่อถือได้” ก่อนอนุญาตให้เอเจนต์ใช้
  - UI ฝั่งไคลเอนต์โชว์ publisher + fingerprint ชัดเจน และเตือนเมื่อชื่อคล้ายของดัง
  - ระยะยาว: จัดทำ namespace policy + เซ็นชื่อคริปโต ให้ยืนยันตัวตนเซิร์ฟเวอร์ และ ระบบความน่าเชื่อถือ (reputation) สำหรับการลงทะเบียน/ค้นพบเซิร์ฟเวอร์

### [MCP-Server] Installer Spoofing 
- Problem
  - เพราะการตั้งค่าเซิร์ฟเวอร์ MCP โดยมือค่อนข้างยาก จึงเกิด auto-installer ชุมชน (เช่น Smithery-CLI, mcp-get, mcp-installer) เพื่อกดครั้งเดียวจบ—แต่ช่องทางนี้เปิด “ผิวโจมตีซัพพลายเชน” เพิ่ม หากแพ็กเกจถูกดัดแปลง/ฉีดโค้ด
  - ผู้โจมตีแนบมัลแวร์/แบ็กดอร์, ตั้งค่าผิดเจตนา, หรือแอบเปิด persistence ระหว่างติดตั้ง โดยผู้ใช้มักไม่ตรวจซอร์สโค้ดของ one-click installer
- Impact
  - สิทธิ์ในเครื่องถูกยึด, config ถูกแก้, outbound แปลก ๆ, ติดตั้งเซิร์ฟเวอร์ที่ถูก “ปรุงแต่ง” รอรับคำสั่ง
- Solution
  - ติดตั้งจากแหล่งที่ตรวจสอบได้เท่านั้น + ตรวจเช็กซัม/ลายเซ็น ทุกครั้ง
  - ล็อกเวอร์ชัน (pin) และรัน installer/เซิร์ฟเวอร์ใน sandbox/container แบบ non-root, จำกัดสิทธิ์ไฟล์/เครือข่ายเริ่มต้นเป็น deny by default
  - ใช้ SBOM/Dependency audit; เปิด audit log สำหรับไฟล์คอนฟิกและเครือข่าย
  - ระยะยาว: สร้าง framework ติดตั้งอย่างเป็นมาตรฐาน + ตรวจความถูกต้องแพ็กเกจ และ ระบบ reputation สำหรับ auto-installers

### [MCP-Server] Sandbox Escape
- Problem
  - แม้ MCP จะบังคับรัน “เครื่องมือ” ใน sandbox เพื่อจำกัดการเข้าถึงระบบหลัก แต่ผู้โจมตีอาจใช้ช่องโหว่ของ sandbox/container runtime, system calls, lib ภายนอก หรือ side-channel เพื่อ “หนีออก” ไปสู่โฮสต์ แล้วยกระดับสิทธิ์/รันโค้ดอิสระ
  - เป็นภัยหลักของ ช่วงปฏิบัติการ (operation phase) ของ MCP server ซึ่งงานระบุไว้ตรง ๆ ในไดอะแกรมและคำอธิบายวงจรชีวิต
- Impact
  - โค้ดอันตรายรันบนโฮสต์, ข้อมูลหลุดจากโฟลเดอร์นอก sandbox, เอเจนต์ถูกยึดคลัสเตอร์/เครื่อง
- Solution
  - เลือก runtime แยกสิทธิ์เข้ม (เช่น gVisor/Firecracker) + เปิด seccomp/AppArmor/SELinux, drop Linux capabilities, rootless containers
  - ไฟล์ระบบ read-only + no host bind-mounts โดยปริยาย; network ของเครื่องมือ deny by default แล้วค่อย allowlist เป็นรายปลายทาง
  - หมุนคีย์/โทเคนแบบสั้นอายุ, อัปแพตช์ runtime/ไลบรารีสม่ำเสมอ, ทำ chaos/sandbox-escape drills ตามรายการโจมตีตัวอย่างในงาน

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
- [Antropic MCP Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Antropic MCP Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)