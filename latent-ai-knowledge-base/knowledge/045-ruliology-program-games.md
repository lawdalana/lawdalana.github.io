# 045 — Transformer, FSM, Game Theory และ Ruliology

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งต้นฉบับ: [post.md](../original/post.md) บรรทัด 73-79  
รูปประกอบ: ไม่มี  
วันที่ค้นคว้า: 2026-09-20

## ประเด็นจากต้นฉบับ

โพสต์ชวนดู “จุดผิด” ในรูปที่ไม่ได้แนบใน section นี้ แล้วโยง transformer, shallow reasoning, neuro-symbolic, ruliology, game theory และ finite state machine ว่ามาเจอกันใน Rust ได้อย่างไร พร้อมลิงก์บทความ Stephen Wolfram เรื่อง “Games between Programs: The Ruliology of Competition”

## ความรู้ที่ค้นเพิ่ม

บทความ Wolfram ตั้งโจทย์ว่าเกมการแข่งขันซ้ำระหว่าง agent สามารถมอง strategy เป็น “program” ได้ ผู้เล่นเลือก action จากประวัติการเล่นที่ผ่านมา และถ้าเราพิจารณา all possible strategies ก็กลายเป็นพื้นที่ให้ใช้ ruliological methods สำรวจ [Wolfram: Games between Programs](https://writings.stephenwolfram.com/2026/06/games-between-programs-the-ruliology-of-competition/). จุดนี้เชื่อมกับ finite state machine ได้ตรงมาก เพราะ FSM คือ program ที่มี state จำกัด รับ input แล้วเปลี่ยน state/ให้ output

ในบริบท AI, shallow reasoning หมายถึงการตัดสินใจที่ไม่ต้อง generate reasoning ยาว แต่ใช้ rule/state/search ขนาดเล็ก เช่น FSM, minimax, MCTS, constraint solver หรือ verifier ประกบ neural model ส่วน neuro-symbolic คือการให้ neural representation ทำงานร่วมกับ symbolic rules เช่น validator, grammar, state machine หรือ game rules

## วิธีลอง

ทำ repeated prisoner’s dilemma โดยเขียน strategy 3 แบบ:

- Always Cooperate
- Tit-for-Tat
- FSM ที่ลงโทษ 2 turn หลังถูก betray

จากนั้นให้แต่ละ strategy เล่นกัน 100 turn แล้วดู payoff matrix คุณจะเห็นว่า “เหตุผล” บางแบบไม่ต้องใช้ LLM เลย แค่ state + transition ก็เกิดพฤติกรรมซับซ้อนพอศึกษาได้

## ข้อควรระวัง

การพูดว่าไปถึง “หลักล้าน tokens/sec” ต้องระวังคำว่า token ถ้าเป็น token ของ LLM autoregressive จะต่างจาก token/event/state transition ของ system ภายใน ควรใช้หน่วยชัด เช่น states/sec, transitions/sec, decisions/sec หรือ generated tokens/sec เพื่อไม่ให้เทียบผิดชั้น

## แหล่งอ้างอิง

- [Stephen Wolfram: Games between Programs](https://writings.stephenwolfram.com/2026/06/games-between-programs-the-ruliology-of-competition/)

<!-- RESEARCH_REVIEW_2_START -->
<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

วันที่ตรวจเพิ่ม: 2026-09-20

**แหล่งหลักใหม่ที่อ่าน:** Robert Axelrod, [Effective Choice in the Prisoner’s Dilemma (1980)](https://doi.org/10.1177/002200278002400101) และ Axelrod & Hamilton, [The Evolution of Cooperation (Science, 1981) ผ่าน PubMed](https://pubmed.ncbi.nlm.nih.gov/7466396/). DOI/SAGE ของงานแรกให้ metadata/abstract แต่ publisher อาจจำกัด full text; PubMed ให้ provenance ของบทความ Science. แหล่งแรกเป็นงาน iterated prisoner’s dilemma ที่วิเคราะห์ strategy จากการแข่งขันซ้ำ แหล่งที่สองโยงการเกิด cooperation กับสถานการณ์ที่ผู้เล่นพบกันซ้ำและอนาคตมีน้ำหนักพอ

**สิ่งที่ขยายจากโพสต์:** Wolfram เรียก “เกมระหว่างโปรแกรม” ในเชิง ruliology; Axelrod/Hamilton เป็นฐาน game theory/agent tournament ที่ทำให้แนวคิดนี้จับต้องได้เชิงทดลอง Strategy แบบ Tit-for-Tat แสดงว่า program สั้นมากก็สร้างพฤติกรรมที่ดูมีเหตุผลได้เมื่ออยู่ใน environment ที่มี feedback ซ้ำ นี่เชื่อมกับ finite-state machine และ shallow reasoning โดยตรง: state เล็ก + transition ชัด + payoff function สามารถเรียนรู้/เปรียบเทียบได้ โดยไม่ต้อง generate chain-of-thought ยาว

**ตัวอย่างทดลอง:** สร้าง tournament 5 strategy: Always Cooperate, Always Defect, Tit-for-Tat, Forgiving Tit-for-Tat, และ FSM “ลงโทษ 2 turn หลังถูก betray แล้วกลับมา cooperate”. รัน 200 รอบต่อคู่ ใส่ noise 0%, 1%, 5% แล้วทำตาราง payoff เฉลี่ยและอันดับ. จากนั้นให้ LLM เขียน strategy ใหม่ แต่ต้อง export เป็น transition table ก่อนเข้าแข่ง วิธีนี้บังคับให้ “reasoning” กลายเป็น program ที่ตรวจได้

**ข้อจำกัด:** ผลของ Axelrod ขึ้นกับ payoff matrix, จำนวนรอบ, noise, และประชากร strategy ที่เอามาแข่ง จึงไม่ควรสรุปว่า strategy เดียวชนะทุกโลก. สำหรับโพสต์นี้ ประโยชน์คือกรอบทดลองว่า neuro-symbolic/ruliology ควรนิยาม state, action, payoff และ tournament ก่อนคุยว่า agent ฉลาดแค่ไหน
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 044](044-cpu-simd-gpu-crossover.md) · [โพสต์ 046 →](046-rules-shallow-reasoning-cargo-heal.md)

หัวข้อที่เกี่ยวข้อง: [03 Neuro-symbolic, constraints, types และการตรวจคำตอบ](topics/03-neuro-symbolic-types-and-verification.md) · [10 วิธีอ่าน paper, สร้างการทดลอง และวางแผนเรียน](topics/10-research-methods-and-learning.md)
<!-- POST_NAV_END -->
