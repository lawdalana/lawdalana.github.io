---
title: "Agent Harness Engineering"
notetype: feed
date: 2026-09-16
last_modified: 2026-09-17
tags: [AI, AI-agents, agentic-engineering, harness-engineering, context-engineering]
status: published
---

# Agent Harness Engineering: วิศวกรรมระบบรอบโมเดล

> ฉบับแปลภาษาไทยจาก [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) โดย Addy Osmani — 19 เมษายน 2026

![ภาพปก Agent Harness Engineering](/assets/img/LLM/Agentic-Engineering/agent-harness.jpg)

*ภาพปก: [Addy Osmani](https://addyosmani.com/assets/images/agent-harness.jpg)*

*Coding agent คือโมเดลบวกกับทุกสิ่งที่เราสร้างล้อมรอบมัน Harness engineering มองโครงสร้างรองรับเหล่านี้เป็น artifact ทางวิศวกรรมจริง ๆ และปรับมันให้รัดกุมขึ้นทุกครั้งที่ agent พลาด*

กล่าวแบบคร่าว ๆ คือ ทุกครั้งที่พบว่า agent ทำผิด เราควรใช้เวลาออกแบบวิธีแก้ที่ทำให้มันไม่ทำผิดแบบเดิมอีก

ตลอดสองปีที่ผ่านมา เราถกเถียงกันเรื่องโมเดลเป็นหลัก: ตัวไหนฉลาดที่สุด ตัวไหนเขียน React ได้สะอาดที่สุด ตัวไหน hallucinate น้อยที่สุด บทสนทนานี้มีประโยชน์ แต่ยังขาดอีกครึ่งหนึ่งของระบบ โมเดลเป็นเพียง input หนึ่งของ agent ที่กำลังทำงาน ส่วนที่เหลือคือ **harness**: prompts, tools, นโยบาย context, hooks, sandboxes, subagents, feedback loops และ recovery paths ที่ห่อหุ้มโมเดลไว้เพื่อให้มันทำงานจนเสร็จได้จริง

**โมเดลระดับพอใช้ที่มี harness ยอดเยี่ยม เอาชนะโมเดลยอดเยี่ยมที่มี harness แย่ได้** ผมเห็นเรื่องนี้เกิดขึ้นซ้ำแล้วซ้ำเล่าในงานของตัวเอง และงานวิศวกรรมที่น่าสนใจก็ย้ายจากการเลือกโมเดลไปอยู่ที่การออกแบบโครงสร้างรองรับรอบโมเดลมากขึ้น

ศาสตร์นี้มีชื่อแล้ว Viv Trivedy เป็นผู้บัญญัติคำว่า *harness engineering* และโพสต์ [“Anatomy of an Agent Harness”](https://x.com/Vtrivedy10/status/2031408954517971368) ของเขาอธิบายได้ชัดที่สุดว่า harness คืออะไรและแต่ละส่วนมีไว้ทำไม [Dex Horthy](https://x.com/dexhorthy/status/1985699548153467120) ติดตามรูปแบบนี้มาตลอดช่วงที่มันกำลังก่อตัว [HumanLayer](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) มองความล้มเหลวของ agent ส่วนใหญ่ว่าเป็น “skill issue” ซึ่งเกิดจาก configuration มากกว่าน้ำหนักของโมเดล [ทีมวิศวกรรมของ Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) เผยแพร่คำอธิบายสาธารณะที่ดีที่สุดชิ้นหนึ่งเกี่ยวกับการออกแบบ harness สำหรับงานระยะยาว และ [Birgitta Böckeler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) ก็อธิบายมุมมองของผู้ใช้งานได้ดี

บทความนี้พยายามนำแนวคิดเหล่านั้นมาร้อยเข้าด้วยกัน

---

## Harness คืออะไรกันแน่?

ประโยคเดียวของ Viv อธิบายแก่นสำคัญได้เกือบทั้งหมด:

> Agent = Model + Harness หากคุณไม่ใช่โมเดล คุณก็คือส่วนหนึ่งของ harness

Harness คือโค้ด configuration และ execution logic ทุกส่วนที่ไม่ใช่ตัวโมเดล โมเดลดิบ ๆ ยังไม่ใช่ agent มันจะกลายเป็น agent เมื่อ harness มอบ state, การเรียกใช้เครื่องมือ, feedback loops และข้อจำกัดที่บังคับใช้ได้ให้มัน

ในทางปฏิบัติ harness ประกอบด้วย:

- System prompts, `CLAUDE.md`, `AGENTS.md`, skill files และ prompts ของ subagents
- Tools, skills, MCP servers และคำอธิบายของสิ่งเหล่านี้
- Infrastructure ที่ให้มาพร้อมระบบ เช่น filesystem, sandbox และ browser
- Orchestration logic เช่น การสร้าง subagent, handoff และ model routing
- Hooks และ middleware สำหรับ deterministic execution เช่น compaction, continuation และ lint checks
- Observability เช่น logs, traces และการวัดต้นทุนกับ latency

[Simon Willison](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) ย่อส่วน loop ให้เหลือแก่นว่า agent คือระบบที่ *“เรียกใช้เครื่องมือเป็นวงรอบเพื่อบรรลุเป้าหมาย”* ทักษะสำคัญจึงอยู่ที่การออกแบบทั้ง tools และ loop

หากฟังดูเหมือนมีพื้นผิวให้ดูแลมาก นั่นก็เพราะมันมากจริง ๆ และพื้นผิวเหล่านี้เป็นความรับผิดชอบของเรา ไม่ใช่ของผู้ให้บริการโมเดล Claude Code, Cursor, Codex, Aider และ Cline ล้วนเป็น harness **แม้โมเดลข้างใต้บางครั้งจะเป็นตัวเดียวกัน แต่พฤติกรรมที่เราได้รับถูกกำหนดอย่างมากโดยสิ่งที่ harness ทำ**

```text
coding agent = AI model(s) + harness
```

สมการนี้ซึ่ง Viv เสนอและ HumanLayer นำไปขยาย คือบริเวณที่งานจริงอยู่ การถกเถียงเรื่องฝั่งซ้ายเสียงดัง แต่ leverage ส่วนใหญ่อยู่ฝั่งขวา

![โมเดลกลางระบบบริบท เครื่องมือ การควบคุม และการตรวจสอบ](/assets/img/LLM/Agentic-Engineering/harness-anatomy.jpeg)

*แผนภาพ: [ต้นฉบับของ Addy Osmani](https://addyosmani.com/assets/images/harness-anatomy.jpeg)*

---

## เปลี่ยนกรอบคิดจาก “โมเดลมีปัญหา” เป็น “ระบบมี skill issue”

มีรูปแบบหนึ่งที่ผมเห็นวิศวกรทำซ้ำกันบ่อย: agent ทำเรื่องไม่ฉลาด วิศวกรโทษโมเดล แล้วจัดปัญหานั้นไว้ในหมวด “รอรุ่นถัดไป”

แนวคิดแบบ harness engineering ไม่ยอมรับค่าเริ่มต้นนี้ เพราะความล้มเหลวมักอ่านออกและแก้ได้ เช่น

- Agent ไม่รู้ convention บางอย่าง → เพิ่มไว้ใน `AGENTS.md`
- Agent รันคำสั่งทำลายข้อมูล → เพิ่ม hook เพื่อบล็อก
- Agent หลงทางระหว่างงาน 40 ขั้นตอน → แยกเป็น planner และ executor
- Agent ประกาศว่า “เสร็จแล้ว” ทั้งที่โค้ดยังเสีย → ส่งผล typecheck กลับเข้า loop เพื่อสร้าง backpressure

HumanLayer สรุปว่า *“นี่ไม่ใช่ปัญหาของโมเดล แต่เป็นปัญหา configuration”* Harness engineering คือผลลัพธ์ของการเอาประโยคนี้มาปฏิบัติจริง

มีข้อมูลหนึ่งที่ปรากฏทั้งในงานของ Viv และ HumanLayer บน Terminal Bench 2.0: Claude Opus 4.6 ที่รันใน Claude Code ได้คะแนนต่ำกว่าการรันโมเดลเดียวกันใน custom harness อย่างมาก ทีมของ Viv ขยับ coding agent จากนอก Top 30 ขึ้นสู่ Top 5 ด้วยการเปลี่ยนเฉพาะ harness โมเดลมักถูก post-train ให้ทำงานคู่กับ harness ที่ใช้ตอนฝึก การย้ายไปยัง harness ที่มี tools เหมาะกับ codebase มากกว่า prompt กระชับกว่า และ backpressure คมกว่า อาจปลดล็อกความสามารถที่ harness เดิมใช้ไม่เต็มที่

นี่ตรงข้ามกับเรื่องเล่าแบบ “รอ GPT-6 ก็พอ” **ช่องว่างระหว่างสิ่งที่โมเดลปัจจุบันทำได้กับสิ่งที่เราเห็นมันทำ ส่วนใหญ่คือช่องว่างของ harness**

---

## Ratchet: ทุกความผิดพลาดต้องกลายเป็นกฎ

นิสัยสำคัญที่สุดของ harness engineering คือมองความผิดพลาดของ agent เป็น signal ถาวร ไม่ใช่เรื่องขำครั้งเดียวหรือ “รอบที่แย่” ซึ่งแก้ด้วยการกด retry

ถ้า agent ส่ง PR ที่ comment test ทิ้งไว้ และผมพลาด merge เข้าไป นั่นคือ input สำหรับปรับระบบ:

- `AGENTS.md` รุ่นถัดไปจะระบุว่า “ห้าม comment tests; ให้ลบหรือแก้ให้ถูกต้อง”
- pre-commit hook รุ่นถัดไปจะค้นหา `.skip(` และ `xit(` ใน diff
- reviewer subagent รุ่นถัดไปจะถือ commented-out tests เป็น blocker

เราเพิ่มข้อจำกัดเมื่อเห็นความล้มเหลวจริง และถอดออกเมื่อโมเดลที่เก่งขึ้นทำให้มันไม่จำเป็น **ทุกบรรทัดใน `AGENTS.md` ที่ดีควรย้อนกลับไปหาสิ่งเฉพาะที่เคยผิดพลาดได้**

นี่คือเหตุผลที่ harness engineering เป็นวินัยมากกว่า framework Harness ที่ถูกต้องสำหรับ codebase ของเราถูกหล่อขึ้นจากประวัติความล้มเหลวของเราเอง จึงดาวน์โหลดสำเร็จรูปมาใช้ไม่ได้

---

## ออกแบบย้อนกลับจากพฤติกรรมที่ต้องการ

กรอบคิดของ Viv ที่ผมใช้บ่อยที่สุดตอนออกแบบ harness คือ เริ่มจากพฤติกรรมที่ต้องการแล้วค่อยหาองค์ประกอบของ harness ที่สร้างพฤติกรรมนั้น:

```text
พฤติกรรมที่ต้องการหรือปัญหาที่ต้องแก้
→ การออกแบบ harness ที่ช่วยให้โมเดลทำได้
```

ประโยชน์ของวิธีนี้คือทุก component มีหน้าที่เฉพาะ **ถ้าอธิบายไม่ได้ว่า component หนึ่งมีไว้สร้างพฤติกรรมอะไร มันอาจไม่ควรอยู่ในระบบ**

ส่วนต่อไปจะไล่องค์ประกอบตามลำดับใกล้เคียงกับที่ Viv ใช้ พร้อม pattern ที่ผมเห็นว่าน่านำไปใช้

### Filesystem และ Git: state ที่คงทน

Filesystem เป็น primitive พื้นฐานที่สุดและมักถูกมองข้ามเพราะมันธรรมดา โมเดลทำงานโดยตรงได้เฉพาะสิ่งที่อยู่ใน context ถ้าไม่มี filesystem เราก็แค่คัดลอกข้อความเข้าออก chat window ซึ่งยังไม่ใช่ workflow

เมื่อมี filesystem agent จะได้:

- workspace สำหรับอ่านข้อมูล โค้ด และเอกสาร
- ที่เก็บงานระหว่างทางแทนการถือทุกอย่างไว้ใน context
- พื้นที่กลางให้หลาย agents และมนุษย์ประสานงานผ่านไฟล์ร่วมกัน

เมื่อเพิ่ม Git ก็ได้ versioning โดยไม่ต้องสร้างใหม่ Agent จึงติดตามความคืบหน้า rollback ความผิดพลาด และแยก branch สำหรับการทดลองได้ Harness primitives อื่นจำนวนมากจึงย้อนกลับมาใช้ filesystem ไม่ทางใดก็ทางหนึ่ง

### Bash และการรันโค้ด: เครื่องมือเอนกประสงค์

Agent loop หลักในปัจจุบันมักเป็น ReAct loop: โมเดลคิด เลือก action ผ่าน tool call สังเกตผล แล้วทำซ้ำ แต่ harness เรียกใช้ได้เฉพาะ tools ที่มันมี logic รองรับ เราอาจสร้าง tool ล่วงหน้าสำหรับทุก action ที่เป็นไปได้ หรือมอบ bash ให้ agent เพื่อสร้างเครื่องมือย่อยที่จำเป็นขึ้นเอง

มุมมองของ Willison คือ agents ใช้ shell commands ได้เก่งอยู่แล้ว และงานจำนวนมากยุบเหลือ CLI calls ที่เลือกมาอย่างเหมาะสมเพียงไม่กี่คำสั่ง Harness ยังควรมี focused tools แต่ bash บวก code execution กลายเป็นกลยุทธ์เอนกประสงค์มาตรฐานสำหรับ autonomous problem solving ความแตกต่างคล้ายกับการสอนใครใช้เครื่องครัวชิ้นเดียว เทียบกับมอบห้องครัวทั้งห้องให้เขา

### Sandboxes และเครื่องมือพื้นฐาน

Bash มีประโยชน์ก็ต่อเมื่อรันในที่ปลอดภัย การรันโค้ดที่ agent สร้างบน laptop โดยตรงมีความเสี่ยง และ local environment เดียวก็ไม่รองรับ agents จำนวนมากที่ทำงานขนานกัน

Sandbox มอบ operating environment แบบแยกส่วน แทนที่จะ execute ในเครื่องหลัก harness จะเชื่อมไปยัง sandbox เพื่อรันโค้ด ตรวจไฟล์ ติดตั้ง dependencies และยืนยันผลงาน เราสามารถ:

- allow-list commands
- บังคับ network isolation
- สร้าง environment ใหม่ตามต้องการ
- ทำลาย environment เมื่อจบงาน

Sandbox ที่ดีควรมี defaults ที่ดีด้วย เช่น language runtimes และ packages ที่ใช้บ่อย Git และ test CLIs รวมถึง headless browser สำหรับโต้ตอบกับเว็บ Browsers, logs, screenshots และ test runners ช่วยให้ agent สังเกตผลงานตัวเองและปิด self-verification loop ได้

โมเดลไม่ได้เป็นผู้กำหนด execution environment การตัดสินว่า agent รันที่ไหน มีอะไรให้ใช้ และตรวจผลงานอย่างไร ล้วนเป็นการตัดสินใจระดับ harness

### Memory และ Search: การเรียนรู้อย่างต่อเนื่อง

โมเดลไม่มีความรู้เพิ่มเติมนอกเหนือจาก weights และสิ่งที่อยู่ใน context ปัจจุบัน หากแก้ weights ไม่ได้ วิธีเพิ่มความรู้ก็คือ context injection

Filesystem กลับมาเป็น primitive อีกครั้ง Harness รองรับมาตรฐาน memory file เช่น `AGENTS.md` ซึ่งถูก inject ทุกครั้งที่เริ่มงาน เมื่อ agent แก้ไฟล์นี้ harness จะโหลดใหม่ ทำให้ความรู้จาก session หนึ่งส่งต่อไปยัง session ถัดไป นี่คือ continual learning แบบหยาบแต่ใช้ได้จริง

สำหรับความรู้ที่ยังไม่มีตอนฝึก เช่น library รุ่นใหม่ เอกสารปัจจุบัน หรือข้อมูลวันนี้ web search และ MCP tools อย่าง Context7 ช่วยเชื่อมช่องว่างจาก knowledge cutoff ความสามารถเหล่านี้ควรเป็น primitives ของ harness แทนที่จะผลักภาระให้ผู้ใช้ทุกครั้ง

### ต่อสู้กับ Context Rot

Context rot คือข้อสังเกตว่าโมเดลมักคิดและทำงานแย่ลงเมื่อ context window เต็มขึ้น Context เป็นทรัพยากรหายาก และ harness ส่วนใหญ่ก็คือกลไกส่งมอบ context ที่ดี

เทคนิคสามแบบที่พบซ้ำบ่อยคือ:

**Compaction** — เมื่อ window ใกล้เต็ม ระบบต้องสรุปและ offload context เก่าอย่างฉลาดเพื่อให้ agent ทำงานต่อ การปล่อยให้ API error ไม่ใช่ทางเลือกสำหรับ production harness

**Tool-call offloading** — output ขนาดใหญ่ เช่น log 2,000 บรรทัด ทำให้ context รกโดยไม่ได้เพิ่ม signal มาก Harness จึงเก็บเฉพาะส่วนหัวและท้ายเหนือ threshold แล้วบันทึกฉบับเต็มลง filesystem เพื่อให้ agent เปิดอ่านเมื่อต้องการ

**Skills พร้อม progressive disclosure** — การโหลด tools และ MCP ทุกตัวเข้าบริบทตั้งแต่เริ่ม ทำให้ประสิทธิภาพลดลงก่อน agent ลงมือ Skills ช่วยเปิดเผย instructions และ tools เฉพาะเมื่อ task ต้องใช้จริง

โพสต์เรื่อง harness ของ Anthropic เพิ่มเทคนิคสำหรับงานที่ยาวมากคือ **full context reset**: harness ปิด session แล้วสร้างใหม่จาก handoff file ที่สรุปอย่างมีโครงสร้าง พวกเขาระบุชัดว่า *compaction อย่างเดียวไม่พอ* สำหรับงานยาว บางครั้งต้องเริ่มใหม่จาก brief ที่ดี วิธีนี้คล้ายการ onboard วิศวกรคนใหม่มากกว่าแนวคิด “memory” แบบเดิม

### งานระยะยาว: Ralph Loops, Planning และ Verification

งาน autonomous ระยะยาวเป็นเป้าหมายที่ทุกคนอยากได้และเป็นส่วนที่ทำให้ถูกต้องยากที่สุด โมเดลปัจจุบันยังมีปัญหาเรื่องหยุดเร็ว แบ่งปัญหาซับซ้อนไม่ดี และเสียความสอดคล้องเมื่อทำงานข้ามหลาย context windows Harness ต้องออกแบบเผื่อข้อจำกัดเหล่านี้

ผมเคยเขียนเรื่อง autonomous coding loops อย่าง Ralph Loop ในบทความ [self-improving agents](https://addyosmani.com/blog/self-improving-agents/) และ [2026 trends](https://beyond.addy.ie/2026-trends/) แต่เมื่อนำมามองผ่านกรอบ harness หลักการคือ hook จะดักตอนโมเดลพยายามจบ แล้ว inject prompt เดิมเข้า context window ใหม่ บังคับให้ agent ทำต่อจนถึง completion goal แต่ละ iteration เริ่มด้วย context สะอาดและอ่าน state จากรอบก่อนผ่าน filesystem นี่เป็นกลไกเรียบง่ายอย่างน่าประหลาดที่เปลี่ยน single-session agent ให้ทำงานหลาย session ได้ และเป็น primitive ที่เราไม่อาจได้มาจากคำแนะนำว่า “ใช้โมเดลฉลาดขึ้น” เพียงอย่างเดียว

**Planning** คือให้โมเดลแยกเป้าหมายเป็นลำดับขั้น มักเขียนลง plan file บน disk Harness สนับสนุนด้วย prompt และ reminders ว่าต้องใช้แผนอย่างไร หลังแต่ละขั้น agent ตรวจงานเอง: hooks รัน test suite ที่กำหนดไว้และส่ง failure text กลับเข้า loop หรือให้โมเดลเทียบ output กับเกณฑ์ชัดเจน

**การแยก Planner / Generator / Evaluator** — งานของ Anthropic เรื่อง harness ระยะยาวระบุว่าการแยกผู้สร้างออกจากผู้ประเมินเป็นคนละ agent ให้ผลดีกว่าการให้ agent ประเมินงานตัวเอง เพราะ agent มักให้คะแนนตัวเองในทางบวก pattern ที่เกี่ยวข้องคือ **sprint contract** ซึ่ง generator กับ evaluator ตกลงกันก่อนว่า “เสร็จ” หมายถึงอะไร ใน workflow ของผม การเขียน done-condition ก่อนเริ่มช่วยจับ scope drift ได้มากกว่าการปรับ prompt หลายครั้งเสียอีก

### Hooks: ชั้นที่ใช้บังคับจริง

Hooks คือสิ่งที่แยก “ผมบอกให้ agent ทำ X” ออกจาก “ระบบบังคับให้ X เกิดขึ้น”

Hook คือ script ที่ทำงาน ณ lifecycle point เฉพาะ เช่น ก่อน tool call หลังแก้ไฟล์ ก่อน commit หรือตอนเริ่ม session มันเหมาะกับสิ่งที่ agent ไม่ควรลืมแต่ลืมบ่อย เช่น

- รัน typecheck, lint และ tests หลังการแก้แต่ละครั้ง แล้วส่ง failures กลับ
- บล็อก destructive bash เช่น `rm -rf`, `git push --force` และ `DROP TABLE`
- ขอ approval ก่อนเปิด PR หรือ push เข้า `main`
- auto-format ตอนเขียนไฟล์ เพื่อไม่ให้ agent เปลือง tokens กับ whitespace

หลักการจาก HumanLayer ที่ผมเห็นด้วยคือ **เมื่อสำเร็จให้เงียบ เมื่อผิดพลาดให้อธิบายมาก** ถ้า typecheck ผ่าน agent ไม่ต้องได้ยินอะไร ถ้าล้มเหลว ให้ inject error text เข้า loop เพื่อให้มันแก้เอง Feedback loop จึงแทบไม่มีต้นทุนในกรณีปกติและให้ข้อมูลที่ลงมือแก้ได้ทันทีเมื่อมีปัญหา

### `AGENTS.md` และการเลือก Tools

Rulebook แบบ Markdown ที่ root ของ repository ยังเป็น configuration point ที่ให้ leverage สูงที่สุด เพราะมันเข้า system prompt ทุก turn ใช้เก็บ conventions เช่น package manager, test framework, formatting, “ห้ามแตะ `/legacy`” หรือ “ต้องใช้ logger ของเราเสมอ” บทเรียนสำคัญมีสองข้อ:

**ทำให้สั้น** — HumanLayer จำกัดไฟล์ของตนไว้ต่ำกว่า 60 บรรทัด ทุกบรรทัดแย่ง attention กัน กฎมากขึ้นทำให้แต่ละกฎมีน้ำหนักน้อยลง ควรเป็น checklist ของนักบิน ไม่ใช่ style guide

**ทุกบรรทัดต้องมีที่มา** — กฎควรย้อนกลับไปหาความล้มเหลวในอดีตหรือข้อจำกัดภายนอกที่แข็งจริง ถ้าไม่มี มันคือ noise ให้ ratchet จากปัญหาจริง ไม่ใช่ brainstorm กฎล่วงหน้า

วินัยเดียวกันใช้กับ tools ชื่อ คำอธิบาย และ schema ของ tool ทุกตัวถูกใส่ใน prompt ทุก request เครื่องมือเฉพาะทาง 10 ตัวมักดีกว่าเครื่องมือซ้ำซ้อน 50 ตัว เพราะโมเดลจำเมนูได้ HumanLayer ยังชี้ความเสี่ยงด้าน security: tool descriptions เข้า prompt ดังนั้น MCP server ที่ติดตั้งคือ trusted text ที่โมเดลจะอ่าน MCP ที่เขียนแย่หรือเป็นอันตรายสามารถ prompt-inject agent ก่อนผู้ใช้จะพิมพ์อะไรเสียอีก

### Harness ระดับ Production หน้าตาอย่างไร

ภาพสาธารณะที่ชัดที่สุดของ mature harness ที่ผมเคยเห็นคือ [การวิเคราะห์ architecture ของ Claude Code โดย Fareed Khan](https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0) ซึ่งควรใช้เวลาศึกษาแผนภาพอย่างจริงจัง

แนวคิดเกือบทุกข้อข้างต้นปรากฏเป็น component ที่มีชื่อ:

- Context injection อยู่ใน knowledge layer
- Loop state อยู่ใน memory store และ worktree isolator
- Destructive-action hooks อยู่หลัง permission gate
- Subagent context firewalls เป็น multi-agent layer ทั้งชั้น
- Tool dispatch registry คือจุดที่ MCP servers และ bash เชื่อมเข้าระบบ

ข้อสรุปของ Khan เหมือนกับ Viv แต่แสดงผ่านผลิตภัณฑ์ที่ใช้งานจริง: **วิวัฒนาการของ Claude Code เกิดจาก harness อย่างน้อยพอ ๆ กับโมเดลข้างใต้**

---

## Harness ไม่ได้หดตัว แต่มันย้ายตำแหน่ง

ข้อสังเกตที่ดีมากจากบทความของ Anthropic คือ เมื่อโมเดลเก่งขึ้น พื้นที่ของ harness combinations ที่น่าสนใจไม่ได้เล็กลง แต่มันย้ายไป

เรื่องเล่าแบบง่ายคือโมเดลที่ดีขึ้นจะทำให้ harness ล้าสมัย ถ้าโมเดลวางแผนเองได้ก็ไม่ต้องมี planner ถ้าทำงานระยะยาวได้อย่างสอดคล้องก็ไม่ต้อง reset context และจริงอยู่ Opus 4.6 ลดปัญหา context anxiety ได้มาก—Sonnet 4.5 เคยรีบปิดงานก่อนเวลาเมื่อคิดว่าตัวเองใกล้ถึง context limit—ทำให้ scaffolding ลดความกังวลหลายอย่างที่ผมเขียนเมื่อหกเดือนก่อนกลายเป็น dead code

แต่เพดานเลื่อนตามโมเดล งานที่เคยทำไม่ได้เริ่มเป็นไปได้ และมาพร้อม failure modes ใหม่ Scaffolding แบบเก่าหายไป แต่ต้องมี multi-day memory policy, harness ที่ประสาน specialized agents สามตัว หรือ evaluators สำหรับคุณภาพ design ของ UI ที่สร้างขึ้นมาแทน Assumptions เปลี่ยน และ scaffolding ที่ encode assumptions เหล่านั้นก็ต้องเปลี่ยนด้วย

Anthropic สรุปได้ตรงประเด็นว่า *“ทุก component ใน harness encode assumption ว่าโมเดลทำอะไรเองไม่ได้”* เมื่อโมเดลเก่งขึ้นในเรื่องหนึ่ง component นั้นก็ไม่รองรับน้ำหนักอะไรอีกและควรถอดออก เมื่อโมเดลปลดล็อกสิ่งใหม่ ก็ต้องมี scaffolding ใหม่เพื่อไปให้ถึงเพดานใหม่

### วงจรฝึกระหว่าง Model กับ Harness

อีกสิ่งที่กำลังเกิดขึ้นและ Viv เรียกชื่อชัดเจน คือ feedback loop ระหว่างการออกแบบ harness กับการฝึกโมเดล

ผลิตภัณฑ์ agent ปัจจุบันถูก post-train โดยมี harness อยู่ใน loop โมเดลจึงเก่งเป็นพิเศษกับ actions ที่ผู้ออกแบบ harness ต้องการ เช่น filesystem operations, bash, planning และ subagent dispatch นี่เป็นเหตุผลที่ Opus 4.6 ให้ความรู้สึกต่างกันเมื่ออยู่ใน Claude Code กับ custom harness และทำไมการเปลี่ยน logic ของ tool บางครั้งสร้าง regression แปลก ๆ โมเดลที่ general จริงไม่ควรสนว่าเราใช้ `apply_patch` หรือ `str_replace` แต่ co-training ทำให้เกิด overfitting ได้

ผลเชิงปฏิบัติมีสองข้อ:

1. **Harness เป็นระบบมีชีวิต ไม่ใช่ config file ที่ตั้งครั้งเดียวแล้วจบ**
2. Harness ที่ “ดีที่สุด” ไม่จำเป็นต้องเป็นตัวที่โมเดลถูกฝึกมาด้วย แต่คือตัวที่ออกแบบให้ตรง task ของเรา

การขยับจาก Top 30 ไป Top 5 บน Terminal Bench ด้วยการเปลี่ยน harness เป็นหลักฐานที่ชัดเจนที่สุดของประเด็นนี้

---

## Harness-as-a-Service

อีกแนวคิดจาก Viv คือ **[HaaS](https://www.vtrivedy.com/posts/claude-code-sdk-haas-harness-as-a-service)** หรือ Harness-as-a-Service เรากำลังเปลี่ยนจากการสร้างบน LLM APIs ที่ให้ completion ไปสู่ harness APIs ที่ให้ runtime

Claude Agent SDK, Codex SDK และ OpenAI Agents SDK ล้วนชี้ไปทางเดียวกัน: ผู้พัฒนาได้ loop, tools, context management, hooks และ sandbox primitives มาเป็นพื้นฐาน แล้วค่อย customize

อดีตเส้นทางมาตรฐานคือ:

1. สร้าง loop เอง
2. ต่อ tool calling เอง
3. จัดการ conversation state เอง
4. คิด approval flow เอง

เส้นทางใหม่คือ:

1. เลือก harness framework
2. ตั้งค่าตามสี่เสาหลัก: system prompt, tools, context และ subagents
3. ทุ่มแรงไปที่ domain-specific prompt และ tool design

นี่ทำให้การแก้ “skill issue” เป็นเรื่องจัดการได้ เราไม่ต้องสร้าง agent ใหม่ตั้งแต่ศูนย์ทุกครั้งที่เกิดปัญหา แต่ปรับ configuration surface ที่แยกส่วนมาดีแล้ว

ประโยคของ Viv ยังเป็นเหตุผลที่ดีให้เริ่มจากของที่ไม่สมบูรณ์: *“การสร้าง agent ที่ดีคือการทำซ้ำ เราทำซ้ำไม่ได้ถ้ายังไม่มี v0.1”*

---

## ทิศทางต่อไป

เมื่อวาง coding agents ชั้นนำไว้ข้างกัน—Claude Code, Cursor, Codex, Aider และ Cline—**พวกมันดูคล้ายกันมากกว่าโมเดลข้างใต้เสียอีก** โมเดลต่างกัน แต่ patterns ของ harness กำลังบรรจบกัน นี่น่าจะเป็นผลจากอุตสาหกรรมค่อย ๆ ค้นพบ scaffolding ที่รับน้ำหนักจริงและเปลี่ยน generative model ให้ส่งมอบงานได้

ปัญหาเปิดที่ Viv มองว่าน่าตื่นเต้น ได้แก่:

- ประสาน agents จำนวนมากให้ทำงานขนานบน codebase ร่วมกัน
- ให้ agents วิเคราะห์ traces ของตัวเอง เพื่อค้นหาและแก้ failure modes ระดับ harness
- ให้ harness ประกอบ tools และ context ที่เหมาะแบบ just-in-time ตาม task แทนการตั้งค่าคงที่ตั้งแต่เริ่ม

ข้อสุดท้ายทำให้ **harness หยุดเป็น static config และเริ่มมีลักษณะคล้าย compiler** มากขึ้น

---

## Related Notes

- [[The New Software Lifecycle]]
- [[The Factory Model]]
- [[Agentic Code Review]]
- [[The Orchestration Tax]]

## Reference

- [Addy Osmani — Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — ต้นฉบับภาษาอังกฤษ อ่านเมื่อ 17 กันยายน 2026
