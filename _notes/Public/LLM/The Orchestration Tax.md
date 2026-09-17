---
title: "The Orchestration Tax"
notetype: feed
date: 2026-09-16
last_modified: 2026-09-17
tags: [AI, AI-agents, agentic-engineering, orchestration, productivity]
status: published
---

# The Orchestration Tax: ต้นทุนการควบคุม Agents

> ฉบับแปลภาษาไทยจาก [The Orchestration Tax](https://addyosmani.com/blog/orchestration-tax/) โดย Addy Osmani — 24 พฤษภาคม 2026

![ภาพปก The Orchestration Tax](/assets/img/LLM/Agentic-Engineering/orchestration-tax.jpg)

*ภาพปก: [Addy Osmani](https://addyosmani.com/assets/images/orchestration-tax.jpg)*

*ทุกวันนี้การเริ่ม agent เพิ่มเป็นเรื่องง่าย แต่ agents ที่รันมากขึ้นไม่ได้ทำให้มี “ตัวเรา” เพิ่มขึ้นตามไปด้วย Cognitive bandwidth ของเรา parallelize ไม่ได้ Judgment ทั้งหมดที่ใช้กำกับ agents และ merge โค้ดกลับเข้า codebase ยังคงต้องวิ่งผ่าน serial processor เพียงตัวเดียว—คือตัวเรา Orchestration tax คือราคาที่ต้องจ่ายเมื่อเราลืมข้อเท็จจริงนี้ ทางแก้จริงคือเริ่มออกแบบ attention ของตัวเองเหมือนที่ออกแบบ concurrent system*

สัปดาห์นี้ผมร่วม [panel ที่ Google I/O](https://www.youtube.com/watch?v=VTYx7Ex-0bA) กับ Richard Seroter, Aja Hammerly และ Ciera Jaspan เพื่อคุยว่าวิศวกรรมซอฟต์แวร์ตอนนี้หน้าตาอย่างไรและน่าจะเปลี่ยนไปทางไหน ช่วงท้าย Richard ถามว่า มีสิ่งใดหนึ่งอย่างที่นักพัฒนาควรกลับไปทำต่างจากเดิม ผมตอบเรื่องที่วนคิดมาหลายเดือน:

> **ความรู้สึกว่ายุ่ง ไม่ได้แปลว่ากำลังสร้างผลงาน**

เรารัน agents 20 ตัวและรู้สึกยุ่งมากได้ แต่นั่นไม่ได้เท่ากับงานที่ส่งมอบแล้ว 20 เท่า

ก่อนหน้านั้น Richard ตั้งชื่อให้ปัญหานี้ว่า “orchestration tax” เขาพูดว่า *“คุณจัดการ agents ยี่สิบตัวในสมองตัวเองให้สำเร็จไม่ได้”* เขาพูดถูก ผมอยากแยกแนวคิดนี้ให้ชัด เพราะมันไม่ใช่ปัญหาเรื่องวินัย แต่เป็นปัญหาด้าน architecture

ประโยคจาก panel ที่ผมยังคิดถึงคือประโยคที่พูดออกไปแทบไม่ทันตั้งตัว:

> การรัน agents หลายตัวไม่ได้ทำให้มีตัวคุณเพิ่มขึ้น

---

## ความไม่สมมาตรที่คนมักไม่คิดต้นทุน

Agentic workflows มีความไม่สมมาตรซ่อนอยู่ การเริ่ม agent มีต้นทุนต่ำมาก เพียงกดแป้นหรือเขียน prompt หนึ่งประโยค แต่การปิด loop ของ agent ไม่ได้ถูกเลย ต้องมีใครบางคนตรวจว่าสิ่งที่กลับมาถูกหรือไม่ และปรับมันให้เข้ากับสิ่งที่ agents ตัวอื่นแตะไปแล้ว คนนั้นคือเรา และมีเราเพียงคนเดียว

เดือนก่อนผมเขียนเรื่องส่วนหนึ่งของปัญหานี้ใน [Your Parallel Agent Limit](https://addyosmani.com/blog/cognitive-parallel-agents/) โดยเน้นความกังวลเบื้องหลังจากการไม่รู้ว่า thread ไหนกำลังล้มเงียบ ๆ บทความนี้มองรูปทรงจริงที่อยู่ใต้ต้นทุนนั้น

เมื่อเริ่มมอง agent development เป็น concurrent system เราจะเห็นว่ามนุษย์เป็นเพียง component หนึ่งในระบบ และเป็น component ที่ทำงานแบบ serial อย่างช้า ๆ

---

## คุณคือ Single-Threaded Resource

หากเคยเขียน concurrent code เรามี intuition ที่ถูกอยู่แล้ว เพียงแต่เคยชี้มันไปยังส่วนผิดของระบบ

Python มี Global Interpreter Lock หรือ GIL เราสร้าง threads ได้มากเท่าไรก็ได้ แต่ในขณะหนึ่งมีเพียง thread เดียวที่ execute Python bytecode เพราะทุก thread ต้องแย่ง lock เดียวกัน

> **คุณคือ GIL ของ AI agents ของคุณ**

Agents ทุกตัวทำงานพร้อมกันได้ แต่เมื่อผลงานใดต้องการความเข้าใจ architecture จริง ๆ หรือต้องแก้ merge conflict งานนั้นต้อง acquire lock มี lock เดียว และเราเป็นผู้ถือมัน

[Amdahl’s Law](https://en.wikipedia.org/wiki/Amdahl%27s_law) อธิบายข้อจำกัดนี้อย่างแม่นยำ Speedup จาก parallelization ถูกจำกัดด้วยสัดส่วนงานที่ยังคงเป็น serial หาก pipeline ส่วนใหญ่ parallelize ไม่ได้ ระบบจะชนเพดานแข็งไม่ว่าจะเพิ่ม cores อีกเท่าใด

ใน agent development ส่วนที่เป็น serial คือ **judgment** การสร้าง agents 8 ตัวไม่ได้เร่งเวลาที่ใช้ judgment แต่เพียงทำให้คิวงานที่ไหลเข้าหามันลึกขึ้น

นี่เป็นความจริงเก่าของ performance engineering ที่ยังทำให้คนประหลาดใจ: การ optimize ส่วนที่ไม่ใช่ bottleneck ไม่เพิ่ม throughput มันเพียงเพิ่มกอง unfinished work หน้าคอขวด การเพิ่ม agents เป็นการ optimize ส่วนที่ไม่เคยเป็นข้อจำกัด ข้อจำกัดคือ review step และ throughput ของระบบเท่ากับ throughput ของขั้นตอนนั้น

**Orchestration tax คือช่องว่างเชิงโครงสร้างระหว่างสิ่งที่ agents ผลิตกับสิ่งที่เราสามารถตรวจและ merge ได้จริง** มันคือผลของการให้ทรัพยากร single-threaded รับผิดชอบระบบ concurrent

---

## การฝืนทำงานหนักขึ้นแก้ข้อจำกัดเชิงโครงสร้างไม่ได้

ใน panel ผมบอกว่าไม่เคยรู้สึก productive กับเครื่องมือได้เท่านี้ แต่ก็ไม่เคยเหนื่อยเท่านี้ ทั้งสองด้านเป็นจริงพร้อมกันและมีสาเหตุเดียวกัน

ความเหนื่อยมีต้นเหตุเฉพาะ: มันคือความรู้สึกของการรัน serial processor ที่ 100% โดยไม่มี slack

ทุกครั้งที่กลับไปดู agent ซึ่งปล่อยไว้ เราจ่าย context-switch cost ต้องล้างสมองแล้วโหลด context ใหม่แบบ cold CPUs ทำสิ่งนี้ในระดับ microseconds และ architects ยังพยายามหลีกเลี่ยง มนุษย์ใช้เวลาหลายนาทีและโหลด context กลับมาได้ไม่สมบูรณ์

Agents 5 ตัวไม่ใช่ workload 1 ชุดที่ทำซ้ำห้าครั้ง แต่มันคือ cold reload ห้าครั้ง บวก background process ในสมองที่คอยกังวลว่าควรไปตรวจตัวไหน

เราไม่สามารถแก้ structural limit ด้วยการพยายามให้หนักขึ้น Tax ยังต้องถูกจ่าย หากเลือก grind ผ่านมัน ข้อจำกัดจะแสดงออกเป็น code review แบบผิวเผิน หรือ [cognitive surrender](https://addyosmani.com/blog/cognitive-surrender/) ซึ่งเรายอมรับโค้ดของ agent เพราะการสร้างความเห็นของตัวเองใช้ attention ที่ไม่เหลือแล้ว

เรามีสองทาง: จ่าย tax อย่างตั้งใจ หรือปล่อยให้มันทำลายความเข้าใจระบบของเราอย่างเงียบ ๆ

---

## ออกแบบ Attention ของคุณ

เราจึงต้องมอง attention เป็น scarce serial resource เราคงไม่ออกแบบ distributed system โดยไม่คิดถึง bottleneck อย่างจริงจัง ก็ควรให้ความเคารพกับสมองตัวเองแบบเดียวกัน

สิ่งต่อไปนี้เป็นแนวทางที่ยังใช้ได้ดีสำหรับผม

### 1. ขยาย Fleet ตาม Review Rate ไม่ใช่ตาม UI

Concurrent system ที่ดีใช้ backpressure เพื่อไม่ให้คิวโตไม่สิ้นสุด Producer ต้องชะลอให้พอดีกับ consumer

- จำนวน agents คือ producer
- Review rate ของเราคือ consumer

จำนวน agents ที่ถูกต้องคือจำนวนที่เรายัง code review ได้อย่างเหมาะสม สำหรับคนส่วนใหญ่มักเป็นเลขหลักเดียวค่าต่ำ เครื่องมือ AI ยอมให้เปิด 20 ตัวได้ แต่นั่นเป็นเพียง UI feature ไม่ใช่ throughput ที่เรารับได้จริง

### 2. จัดประเภทงาน

ผมแบ่ง tasks เป็นสองกอง:

**กองแรก: งานแยกอิสระ** — ยินดี delegate ให้ background agents บน cloud งานเหล่านี้รัน async และมักต้องการผมเฉพาะ final gate

**กองที่สอง: งานซับซ้อนที่ judgment คือตัวงาน** — เช่น bug ประหลาดหรือ architecture design

ความผิดพลาดใหญ่คือพยายาม parallelize กองที่สอง การทำ complex tasks หลายงานพร้อมกันไม่ได้ scale output แต่ทำให้ lock thrash และทุกงานออกมาแย่ลง

### 3. Review เป็น Batch

Context switching มีต้นทุนสูงทุกครั้ง การ review agents 4 ตัวในช่วงเดียวกันถูกกว่าการตรวจหนึ่งตัว ออกไปทำอย่างอื่น แล้วกลับมาโหลด context ใหม่

ให้ agents มีสายจูงที่ยาวขึ้น ปล่อยให้งานสะสมเล็กน้อย แล้วประมวลผลเป็น batch

### 4. ใช้ Lock เฉพาะกับ Judgment

อย่าเสียสมองกับสิ่งที่เครื่องยืนยันเองได้ ให้ agent เขียน test ที่ผ่านหรือสร้าง screenshot เป็นหลักฐาน ให้มันพิสูจน์ 80% ที่น่าเบื่อด้วยตัวเอง เพื่อให้ attention ที่หายากของเราเหลือสำหรับ 20% ซึ่งต้องการมนุษย์จริง ๆ

### 5. ปกป้อง Serial Time

Bottleneck ต้องได้เวลาที่ดีที่สุดของเรา ไม่ใช่นาทีที่เหลือระหว่างการสลับไปดู agents บางครั้งการกระทำที่ leverage สูงที่สุดคือหยุด orchestration ทั้งหมด ปิด laptop ที่เต็มไปด้วย agents แล้วคิดเรื่องเดียวอย่างลึก โดยถือ lock ไว้ตลอดช่วง

Orchestration ไม่ใช่งานจริง แต่มันคือ overhead รอบงาน

Aja ชี้ว่า architecture คือทักษะเร่งด่วนตอนนี้ เราต้องรู้ว่าสิ่งใดควรอยู่ภายใน agent ตัวเดียวและสิ่งใดใหญ่เกินไป ผมอยากเพิ่มว่า ตัวเราเองก็เป็น component ในระบบ Attention ของเรามี serial throughput ต่ำและวัดได้ ระบบต้องเคารพตัวเลขนี้ ไม่เช่นนั้นมันจะหลบข้อจำกัดด้วยการลดมาตรฐานของเราอย่างเงียบ ๆ

---

## ยุ่งกับ Productive ไม่ใช่สิ่งเดียวกัน

เรื่องนี้สำคัญเพราะ failure mode มองไม่เห็นจากข้างใน

Agents 20 ตัวที่กำลังรันให้ความรู้สึกเหมือน productivity มหาศาล Dashboard เต็มและทุกอย่างเคลื่อนไหว แต่ความรู้สึกนี้แยกขาดจากการส่ง good code เข้า `main` เราอาจยุ่งถึงขีดสุดแต่แทบไม่ส่งมอบอะไรเลย และจากข้างในสองสถานการณ์นี้ให้ความรู้สึกเหมือนกัน

Ciera กล่าวถึง [งานของ Margaret-Anne Storey เรื่อง debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) เราคุยกันทั้ง technical debt และ cognitive debt Orchestration tax ที่ค้างชำระทำให้เราสะสมสองอย่างพร้อมกัน:

- Merge สิ่งที่ไม่ได้อ่านอย่างดี
- Mental model ของ codebase ล้าสมัย
- เข้าใจสิ่งที่ตัวเองเป็นเจ้าของน้อยลงเรื่อย ๆ

วันนี้ dashboard ไม่แสดงปัญหาเหล่านี้ มันจะปรากฏเมื่อ production พัง แล้วเรามองระบบตรงหน้าและพบว่าไม่รู้แล้วว่ามันทำงานอย่างไร

ดังนั้นข้อสรุปจริงคือ การ spawn agents ไม่ใช่ทักษะ ใครก็เปิด 20 ตัวได้ ทักษะคือการออกแบบระบบรอบทรัพยากร serial หนึ่งเดียวที่ clone หรือ parallelize ไม่ได้

ทรัพยากรนั้นคือ **attention ของคุณ**

จงออกแบบมันเหมือนสิ่งอื่นที่คุณพึ่งพาใน production

---

## Related Notes

- [[The New Software Lifecycle]]
- [[The Factory Model]]
- [[Agent Harness Engineering]]
- [[Agentic Code Review]]

## Reference

- [Addy Osmani — The Orchestration Tax](https://addyosmani.com/blog/orchestration-tax/) — ต้นฉบับภาษาอังกฤษ อ่านเมื่อ 17 กันยายน 2026
