---
title: "The Factory Model"
notetype: feed
date: 2026-09-16
last_modified: 2026-09-17
tags: [AI, AI-agents, agentic-engineering, software-engineering, TDD]
status: published
---

# The Factory Model: Coding Agents เปลี่ยนวิศวกรรมซอฟต์แวร์อย่างไร

> ฉบับแปลภาษาไทยจาก [The Factory Model: How Coding Agents Changed Software Engineering](https://addyosmani.com/blog/factory-model/) โดย Addy Osmani — 25 กุมภาพันธ์ 2026

![ภาพปก The Factory Model](/assets/img/LLM/Agentic-Engineering/factory-model.jpg)

*ภาพปก: [Addy Osmani](https://addyosmani.com/assets/images/factory-model.jpg)*

เมื่อไม่นานมานี้มีบางอย่างเปลี่ยนไปในโลกของ [agentic engineering](https://addyosmani.com/blog/agentic-engineering/) และให้ความรู้สึกเหมือน “ระดับ abstraction” ขยับขึ้นอีกครั้ง ไม่ใช่การเปลี่ยนแบบเดิมที่เครื่องมือค่อย ๆ ดีขึ้นและ workflow ค่อย ๆ วิวัฒน์ แต่เป็นการกระโดดข้ามขั้น นักพัฒนาที่เขียนซอฟต์แวร์มาหลายสิบปีอธิบายตรงกันว่า จุดศูนย์ถ่วงของวิชาชีพนี้ย้ายไปแล้ว

สิ่งที่มีประโยชน์ที่สุดในตอนนี้คือถือสองความคิดที่ดูตึงกันไว้พร้อมกัน:

> **การเขียนโค้ดเปลี่ยนไปอย่างมหาศาล แต่วิศวกรรมซอฟต์แวร์ที่แก่นกลางยังไม่ได้เปลี่ยน**

ช่องว่างระหว่างสองประโยคนี้คือเรื่องราวที่น่าสนใจ และการเข้าใจมันให้ชัดคือสิ่งที่แยกวิศวกรซึ่งเติบโตในยุคนี้ออกจากคนที่ตามไม่ทัน

ผมอ่าน [ความคิดเห็นของ Michael Truell แห่ง Cursor](https://x.com/mntruell/status/2026736314272591924) แล้วอยากขยายแนวคิดเหล่านั้นให้ลึกขึ้น

---

## เส้นทางของ Abstraction

**ประวัติศาสตร์ของวิศวกรรมซอฟต์แวร์คือประวัติศาสตร์ของการยกระดับ abstraction** เราเดินทางจาก bits ไปสู่ instructions จาก instructions ไปสู่ functions จาก functions ไปสู่ objects จาก objects ไปสู่ services และจาก services ไปสู่ distributed systems ทุกครั้งที่ stack กระโดดขึ้นอีกชั้น นักพัฒนาแต่ละคนมี productivity สูงขึ้น และคนจำนวนมากขึ้นสามารถเข้ามาสร้างซอฟต์แวร์ได้

Assembly เปิดทางให้ C, C เปิดทางให้ managed languages และ garbage collection จากนั้น managed languages เปิดทางให้ frameworks, package ecosystems และ cloud infrastructure ทุกการเปลี่ยนผ่านดูรุนแรงในยุคของมัน แต่เมื่อมองย้อนกลับไป แต่ละขั้นก็เป็นเพียงช่วงถัดไปของเส้นทางที่ต่อเนื่องยาวนาน

**สิ่งที่เรากำลังเผชิญอยู่ขณะนี้คืออีกก้าวหนึ่งบนเส้นทางเดิม เรากำลังเปลี่ยนจากการเขียนโค้ด ไปสู่การกำกับระบบที่เขียนโค้ด**

Grady Booch เรียกกรอบนี้ว่า [ยุคที่สามของซอฟต์แวร์](https://newsletter.pragmaticengineer.com/p/the-third-golden-age-of-software) หรือยุคทองใหม่ซึ่งเกิดจาก abstraction ที่สูงขึ้น และงานของนักพัฒนาเปลี่ยนจากการเขียน instructions ไปเป็นการนิยาม intent

กรอบคิดนี้สำคัญ เพราะมันบอกเราว่าอะไรควรยึดไว้ และอะไรควรปล่อยไป

---

## เครื่องมือเขียนโค้ดด้วย AI สามยุค

เราควรแยกวิวัฒนาการแต่ละยุคให้ชัด เพราะการรวมทุกอย่างเข้าด้วยกันทำให้เราประเมินความเปลี่ยนแปลงต่ำเกินจริง

### ยุคแรก: Accelerated Autocomplete

เครื่องมือยุคแรกคาดเดาบรรทัดถัดไป เติม boilerplate และประหยัดการกดแป้นใน pattern ซ้ำ ๆ มันมีประโยชน์และประหยัดเวลาจริง แต่ workflow ยังเหมือนเดิมทั้งหมด: เราเป็นคนขับ เครื่องมือเป็นผู้ช่วย Feedback loop ยังคงเป็น “เขียนโค้ด → รัน → debug → ทำซ้ำ” AI เพียงลดแรงเสียดทานภายใน loop นี้

### ยุคที่สอง: Synchronous Agents

เราอธิบาย task ด้วยภาษาธรรมชาติ โมเดลสร้างโค้ด เราตรวจ แก้ และ iterate ไปจนได้ผลลัพธ์ที่ทำงานได้ ระดับ abstraction สูงขึ้น เราพิมพ์น้อยลงและอธิบาย intent มากขึ้น แต่เรายังอยู่ในทุกขั้น Agent เป็นผู้ร่วมงาน ไม่ใช่ autonomous worker เรายังคงถือ context กำหนดก้าวถัดไป และจับความผิดพลาดแบบ real-time

### ยุคที่สาม: Autonomous Agents

Agents ยุคนี้รับ specification แล้วทำงานต่อเองได้ตั้งแต่สามสิบนาที หนึ่งชั่วโมง หลายชั่วโมง และนานขึ้นเรื่อย ๆ จนถึงหลายวัน พวกมันสามารถ:

- จัด environment
- ติดตั้ง dependencies
- เขียน tests
- เจอ failures แล้วค้นหาวิธีแก้บนอินเทอร์เน็ต
- แก้ปัญหาและเขียน implementation
- ทดสอบซ้ำ
- ตั้ง services
- ส่ง artifacts มาให้ตรวจ

เรามอบ task แล้วไปทำอย่างอื่น ก่อนกลับมาดู logs, previews และ pull requests เราไม่ได้โต้ตอบทีละบรรทัดอีกต่อไป แต่กำลังกำหนด outcomes และตรวจผลลัพธ์ นี่คือจุดที่ [ฝูง agents และ agents ที่ปรับปรุงตัวเอง](https://addyosmani.com/blog/self-improving-agents/) เริ่มมีบทบาท

จังหวะการทำงานเปลี่ยนไปจนยากจะอธิบายให้คนที่ยังไม่เคยสัมผัส งานที่เมื่อสามเดือนก่อนต้องใช้เวลาทั้งสุดสัปดาห์ ตอนนี้อาจเป็นสิ่งที่เราเริ่มไว้แล้วกลับมาตรวจในอีกสามสิบนาที

---

## Mental Model แบบโรงงาน

**กรอบคิดที่มีประโยชน์ที่สุดสำหรับ paradigm ใหม่นี้ คือเราไม่ได้แค่เขียนโค้ดอีกต่อไป แต่กำลังสร้างโรงงานที่สร้างซอฟต์แวร์ของเรา**

โรงงานนี้ประกอบด้วย fleets of agents แต่ละ agent มี:

- task
- toolbelt เช่น repositories, test runners, deployment scripts และ documentation
- context เช่น specs, architecture decisions และข้อจำกัดเดิม
- feedback loop

แทนที่จะคอยจูง agent ตัวเดียวผ่าน task เดียว เราสร้าง agents หลายตัวให้ทำงานขนานกัน ตัวหนึ่ง refactor backend อีกตัวสร้าง feature อีกตัวเขียน integration tests และอีกตัวอัปเดตเอกสาร เราตรวจ outputs ให้ feedback ปรับ specs และ deploy ใหม่

คำเปรียบเทียบกับโรงงานลึกกว่าที่เห็น โรงงานมี quality control มี process documentation มี inputs ซึ่งต้องระบุอย่างแม่นยำ ไม่เช่นนั้น output จะผิด และโรงงานหยุดเมื่อ environment ไม่น่าเชื่อถือ คุณสมบัติทั้งหมดนี้ตรงกับ agentic software development การจริงจังกับ analogy นี้ชี้ให้เห็นสิ่งที่ควรลงทุนจริง

ในทีมที่นำโมเดลนี้ไปใช้อย่างเต็มที่ pull requests ที่ merge แล้วจำนวนมากเริ่มต้นจาก agents ซึ่งรันอัตโนมัติใน cloud environments นี่ไม่ใช่ทฤษฎีอีกต่อไป แต่เป็น production reality ขององค์กรวิศวกรรมที่เพิ่มจำนวนขึ้นเรื่อย ๆ

ความคิดเห็นจาก Cursor ที่ว่า *“งานของนักพัฒนากำลังกลายเป็นการสร้างระบบที่สร้างซอฟต์แวร์—สร้างโรงงาน ไม่ใช่แค่ตัวผลิตภัณฑ์”* และ *“การ review ไอเดียสนุกกว่าการ review โค้ดมาก”* สอดคล้องกับภาพนี้อย่างชัดเจน

---

## มีความคล้ายคลึงกับการ Onboard วิศวกรใหม่

หนึ่งในรูปแบบที่โดดเด่นที่สุดคือ วิธีทำงานของ agent คล้ายการ onboard วิศวกรใหม่มาก

1. เรามอบ spec ให้
2. เขาแบ่งเป็น subtasks
3. สำรวจ codebase เพื่อเข้าใจโครงสร้าง
4. เมื่อติดขัด เขาค้น commit history
5. ใช้ `git blame` เพื่อดูว่าใครแก้ subsystem ล่าสุด
6. ขอความรู้เฉพาะโดเมนจากคนที่เหมาะสมผ่าน Slack หรือช่องทางคล้ายกัน
7. ทำต่อและ iterate จนผ่าน acceptance criteria

Loop นี้คุ้นเคยเพราะเป็นวิธีทำงานของมนุษย์ ผลตามมาคือ Slack และ email กำลังกลายเป็น interface ระหว่างมนุษย์กับ agents ไม่ใช่แค่ระหว่างมนุษย์ด้วยกัน Git history กำลังเปลี่ยนเป็น knowledge graph ที่ agent ใช้นำทางเพื่อเข้าใจ architecture decisions และ documentation กำลังกลายเป็น training material สำหรับ autonomous execution

หากอยากรู้ว่าควรลงทุนอะไรใน codebase ตอนนี้ ลองถามว่า:

> วิศวกรใหม่ที่มีเพียง documentation และ commit history จะเข้าใจหรือไม่ว่าเหตุใดโค้ดจึงมีโครงสร้างแบบนี้?

ถ้าคำตอบคือไม่ Agents ก็จะติดขัดตรงนั้น และ leverage ที่ควรได้จะถูกจำกัดเช่นกัน

---

## Spec คือ Leverage ของคุณ

นี่คือ insight ที่เปลี่ยนวิธีคิดเรื่องคุณค่าของวิศวกร

หากเรากำกับ agents 20, 30 หรือ 50 ตัวพร้อมกัน ความต่างระหว่าง output ระดับกลางกับ output ยอดเยี่ยมแทบทั้งหมดขึ้นอยู่กับคุณภาพของ specification เมื่อถึง scale นี้ ความคิดที่คลุมเครือไม่ได้แค่ทำให้งานช้า แต่มันทวีคูณ Ambiguous requirements แพร่ไปสู่ autonomous runs หลายสิบงาน แต่ละตัวผิดไปคนละทิศเล็กน้อย Architectural decision ที่แย่ตั้งแต่ต้นไม่ได้กระทบ implementation เดียว แต่มันแพร่ไปทั้ง fleet

**เราไม่สามารถเขียน spec ที่อยู่รอดใน environment นี้ได้ หากไม่เข้าใจ architecture, integration boundaries, edge cases, failure modes และ invariants ที่ห้ามพังอย่างลึกซึ้ง**

Spec ไม่ใช่ prompt อีกต่อไป แต่คือ product thinking ที่ถูกทำให้ explicit

นี่คือเหตุผลที่วิศวกรซอฟต์แวร์ที่แข็งแรงได้ leverage จากเครื่องมือเหล่านี้มากกว่า ไม่ใช่น้อยกว่า งานเชิงกลของการพิมพ์โค้ดกำลังถูก automate แต่งานทางปัญญาในการเข้าใจระบบกำลังถูก amplify ทุกชั่วโมงที่ลงทุนสร้าง architectural understanding และ systems thinking ตอนนี้ส่งผลผ่าน autonomous workers ทั้ง fleet แทนที่จะส่งผลแค่ output ของตัวเราเอง

---

## สิ่งที่แทบไม่ได้เปลี่ยน

เราควรแยกให้ชัด เพราะกระแส AI coding อาจทำให้ดูเหมือนทักษะวิศวกรรมซอฟต์แวร์แบบเดิมล้าสมัยแล้ว แต่จริง ๆ ไม่ใช่

### Requirements ที่ชัดเจน

**ถ้าเราอธิบายไม่ได้ว่าความสำเร็จหน้าตาอย่างไรในรูปแบบที่ประเมินได้ การ execute อัตโนมัติมากแค่ไหนก็สร้างมันไม่ได้** Agents ไม่สามารถขอความชัดเจนจาก requirement ที่ไม่เคยได้รับ พวกมันจะเติมช่องว่างด้วย assumptions และ assumptions เหล่านั้นจะทบกัน

### Abstractions ที่แข็งแรง

Agent ที่ทำงานบนระบบออกแบบดี มี module boundaries ชัด interfaces สอดคล้อง และแยก concerns ดี จะให้ผลดีกว่า agent ที่ทำงานบน codebase พันกันซึ่งทุกอย่างพึ่งทุกอย่าง Clean architecture ไม่ได้มีค่าน้อยลงเมื่อ agent เป็นผู้ implement แต่มากขึ้น เพราะ agents amplify คุณสมบัติของระบบที่มันทำงานอยู่

### Tests ที่เชื่อถือได้

ประเด็นนี้สำคัญจนต้องมีหัวข้อแยก

### การตัดสิน Trade-offs อย่างรอบคอบ

Agents optimize ตาม objective ที่ระบุ แต่ไม่ได้ balance concerns ที่ขัดกัน คาดผลกระทบลำดับสอง หรือเตือนโดยธรรมชาติว่า solution ซึ่งถูกทางเทคนิคอาจผิดทางผลิตภัณฑ์ Judgment นี้ยังอยู่กับมนุษย์

### [Human Oversight](https://addyosmani.com/agentic-engineering/human-in-the-loop/)

Agents ทำงานได้น่าประทับใจ แต่ก็ผิดอย่างมั่นใจได้ คุณภาพ output ดีพอที่จะผ่าน casual review ดังนั้นมาตรฐานทักษะ review ต้องสูงขึ้น ไม่ใช่ลดลง

---

## ทำไม Tests จึงสำคัญกว่าที่เคย

Tests ที่ดีและ Test-driven Development (TDD) เป็นแนวปฏิบัติที่ดีอยู่แล้ว ใน agentic workflow มันเข้าใกล้สิ่งที่ขาดไม่ได้

Red/green TDD มีขั้นตอนชัด:

1. เขียน tests ก่อน implementation
2. ยืนยันว่า tests ล้มเหลวจริง — red phase
3. Iterate implementation จน tests ผ่าน — green phase

ลำดับนี้ไม่ใช่พิธีกรรม แต่เป็นกลไกที่ทำให้มั่นใจว่า implementation ทำสิ่งที่เราคิดจริง

เมื่อมีนักพัฒนาคนเดียว ต้นทุนของการข้าม test-first คืออาจเขียน test ที่ผ่านไม่ว่า implementation ถูกหรือไม่ หรือพลาด edge cases ซึ่งกลายเป็น regression ภายหลัง ต้นทุนเหล่านี้จริงแต่ยังจัดการได้

เมื่อมี agents ทั้ง fleet สร้างโค้ดขนานกันหลายสิบ task ต้นทุนจะทวีคูณอย่างรุนแรง **Agent ที่ optimize เพื่อให้ tests ผ่านจะหาทางทำให้มันผ่าน หาก tests ถูกเขียนหลัง implementation มันมีแนวโน้มจะทดสอบสิ่งที่ implementation บังเอิญทำ มากกว่าสิ่งที่มันควรทำ**

ผลคือมีโค้ดจำนวนมากและ test suite ที่ยืนยันสิ่งผิด Comprehensive test-first suite เป็น leverage ที่ทรงพลังที่สุดในการยืนยันว่า autonomous output ถูกต้อง และปกป้อง behavior เดิมเมื่อ codebase โตขึ้น

“Red/green TDD” เป็น shorthand ที่โมเดลดี ๆ เข้าใจ มันหมายถึงเขียน tests ก่อน ยืนยันว่า fail ก่อน implement แล้วทำให้ผ่านด้วย implementation ที่ถูกต้อง ไม่ใช่ด้วยการหลอก test การสั่ง agent ให้ใช้ red/green TDD จึงเป็น instruction ที่ให้ leverage สูงมากตั้งแต่เริ่ม task

---

## ปัญหาที่ยังไม่ถูกแก้คือ Verification ไม่ใช่ Generation

Generation ไม่ใช่ bottleneck อีกต่อไป Verification ต่างหากที่เป็น

Agents สร้าง output น่าประทับใจ แต่ความท้าทายคือรู้ด้วยความมั่นใจว่าถูกต้องจริงหรือไม่ หลายปัจจัยทำให้ยากกว่าที่เห็น:

- Tests ที่ผ่านก่อน change ไม่ได้แปลว่าจะจับ regression จาก change ได้
- Agents อาจเขียน tests ที่ถูกต้องตามรูปแบบแต่พลาดกรณีสำคัญ
- UI verification ยังเปราะ Visual และ behavioral regressions จึงหลุดรอด
- [ข้อจำกัดของ context window](https://addyosmani.com/agentic-engineering/context-window/) ทำให้ agent บน codebase ใหญ่อาจพลาด constraints หรือ patterns ที่อยู่นอกบริบทปัจจุบัน
- Flaky environments ซึ่งรบกวนนักพัฒนาคนเดียวเป็นครั้งคราว จะกลายเป็น systemic blocker เมื่อ agents 40 ตัวชน flaky test เดียวกันพร้อมกัน โรงงานจึงหยุด

Infrastructure ที่ต้องมีเพื่อรองรับโมเดลนี้ในระดับ scale ได้แก่:

- automated regression detection ที่ดีกว่า
- artifact-level validation ที่ไปไกลกว่า diff ของบรรทัดที่แก้
- environment provisioning ที่เร็วและเชื่อถือได้
- [guardrails](https://addyosmani.com/agentic-engineering/guardrails/) ที่รองรับ parallel workloads

พื้นที่เหล่านี้ยังอยู่ระหว่างการลงทุนและยังไม่ถูกแก้หมด

จนกว่า verification จะตาม generation ทัน Human review ไม่ใช่ overhead ที่เลือกตัดได้ แต่มันคือระบบความปลอดภัย การตอบสนองต่อ output ที่ดูดีไม่ควรเป็นการเชื่อเพราะมันดูดี แต่ต้องมี architectural understanding และ testing discipline ที่ใช้ประเมินอย่างเข้มงวด

---

## รูปแบบใหม่ของ High-Leverage Engineering

วิศวกรที่สร้างผลกระทบสูงสุดในยุคนี้จะไม่ได้โดดเด่นเพราะพิมพ์เร็วหรือจำ syntax เก่ง แต่ด้วยความสามารถอีกชุดหนึ่ง

### Systems Thinking

ความสามารถในการถือ architecture ซับซ้อนไว้ในใจ เข้าใจ interaction ระหว่าง components และคาดว่าการเปลี่ยนจุดหนึ่งกระทบจุดอื่นอย่างไร ทักษะนี้พัฒนายากกว่าความเร็วการพิมพ์และมีค่ามากกว่าเมื่อเราต้องรวม output จาก agents ทั้ง fleet

### Problem Decomposition

การรู้ว่าควรแยกเป้าหมายใหญ่และกำกวมเป็น subtasks ขนาดใดเพื่อให้ agent ทำได้อย่างน่าเชื่อถือ Task ที่ใหญ่เกินมักหลุดทิศ Task ที่ scope ไม่ดีมักถูกตีความผิด การแยกปัญหาและตรวจว่าการแยกนั้นถูกต้องเป็นงานฝีมือจริง

### Architectural Judgment

การเข้าใจว่าทำไมระบบออกแบบแบบนี้ มัน optimize คุณสมบัติอะไร และเลือก trade-off ใด Agents implement ได้ แต่ตัดสินไม่ได้ว่าสิ่งที่กำลัง implement เป็น design ที่ถูกหรือไม่

### Specification Clarity

ความสามารถในการเขียน requirement ให้ไม่กำกวม ครบ edge cases สำคัญ และมีโครงสร้างที่ประเมินได้ง่าย Spec คลุมเครือสร้างผลคลุมเครือ Spec แม่นยำทวีคูณเป็น implementations ที่แม่นยำ

### Output Evaluation

Taste ที่มองออกว่าสิ่งหนึ่งดูถูกแต่จริง ๆ ผิด หรือ implementation แก้ปัญหาที่สั่งแต่สร้างปัญหาใหม่ หรือ architecture ของ solution ไม่เข้ากับระบบเดิม Judgment นี้ยัง automate ไม่ได้

### Orchestration Skill

ความสามารถเชิงปฏิบัติในการจัดการ workstreams ขนาน ให้ feedback ที่ดี รู้ว่าเมื่อไรควร redirect กับเมื่อไรควร retask และรักษาความสอดคล้องของ autonomous workers ทั้ง fleet

ทักษะเหล่านี้ไม่ใช่เรื่องใหม่ วิศวกรที่ดีต้องมีมาตลอด สิ่งที่เปลี่ยนคือความสำคัญสัมพัทธ์ ส่วนเชิงกลของ software development ถูกเครื่องจักรจัดการมากขึ้น ส่วนเชิงปัญญาถูก amplify

---

## ภาพใหญ่คืออะไร?

การสร้างเว็บไซต์ใหม่เพิ่มขึ้น 40% เมื่อเทียบปีต่อปี แอป iOS ใหม่เพิ่มเกือบ 50% และ code pushes บน GitHub ในสหรัฐฯ เพิ่ม 35% ตัวเลขเหล่านี้ทรงตัวมาหลายปีก่อนปลายปี 2024 แล้วกราฟจึงพุ่งขึ้น คนที่ไม่เคยเขียนโค้ดแม้แต่บรรทัดเดียวกำลังสร้างและเปิดตัวซอฟต์แวร์

เราควรจำไว้ว่าปริมาณมากขึ้นไม่ได้แปลว่าคุณภาพดีขึ้น แต่ความจริงยังคงอยู่ว่า barrier ในการสร้างซอฟต์แวร์ลดลงอย่างมาก และนี่คือการเปลี่ยนแปลงพื้นฐานของภูมิทัศน์วิศวกรรมซอฟต์แวร์

**Barrier ในการสร้างซอฟต์แวร์ลดลงจริง นี่ไม่ใช่ hype สำหรับวิศวกรมืออาชีพ มันไม่ได้แปลว่าทักษะมีค่าน้อยลง แต่ทักษะที่สำคัญขยับสูงขึ้นบน stack เช่นเดียวกับทุกการเปลี่ยนผ่านก่อนหน้า**

นักพัฒนาที่เติบโตหลังการเปลี่ยนจาก assembly ไป C ไม่ใช่คนที่เขียน assembly ฉลาดที่สุด แต่เป็นคนที่เข้าใจว่าเครื่องต้องทำอะไรและแสดง intent ด้วยภาษาระดับสูงได้ชัด นักพัฒนาที่เติบโตหลัง managed languages และ frameworks ไม่ใช่คนที่ต่อต้าน garbage collection ที่สุด แต่เป็นคนที่มอง cognitive capacity ซึ่งถูกปลดปล่อยเป็นโอกาสแก้ปัญหายากขึ้น

คนที่จะเติบโตในยุค agentic คือคนที่เข้าใจว่านี่เป็นอีกก้าวบนเส้นทางเดียวกันและลงทุนให้ถูก ไม่ต่อต้านเครื่องมือ และไม่ยอมจำนนต่อมันแบบไม่ตรวจสอบ แต่พัฒนา judgment, clarity และ systems thinking ที่ทำให้เครื่องมือมีประสิทธิภาพสูงสุด

นั่นหมายถึง:

- เขียน specs ให้ดีขึ้น
- ลงทุนกับ test infrastructure
- สร้าง architectural understanding จริงแทนความคุ้นเคยผิวเผิน
- พัฒนา taste ในการประเมิน output อย่างเข้มงวด
- ฝึก problem decomposition จนเป็นธรรมชาติ

ยุคที่ programming เป็นกิจกรรมของการกดแป้นเป็นหลักจบลงแล้ว ยุคที่ programming เป็นงานของความคิดและ judgment เป็นหลักดำเนินมาหลายสิบปี และเพิ่งเร่งขึ้นอีกระดับ

Factory model ไม่ใช่คำเปรียบเทียบเรื่องการสูญเสียการควบคุมซอฟต์แวร์ แต่เป็นเรื่องการสร้าง leverage วิศวกรที่เข้าใจเรื่องนี้จะสร้างสิ่งที่น่าสนใจที่สุดในทศวรรษหน้า

---

## Related Notes

- [[The New Software Lifecycle]]
- [[Agent Harness Engineering]]
- [[Agentic Code Review]]
- [[The Orchestration Tax]]

## Reference

- [Addy Osmani — The Factory Model](https://addyosmani.com/blog/factory-model/) — ต้นฉบับภาษาอังกฤษ อ่านเมื่อ 17 กันยายน 2026
