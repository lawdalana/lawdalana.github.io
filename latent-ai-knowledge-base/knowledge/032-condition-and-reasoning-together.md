# 032 — Condition กับ Reasoning เขียนร่วมกันได้

อ่านเพิ่ม: [ผลตรวจและงานวิจัยรอบ 2](#research-review-2)

แหล่งที่มา: `post.md` บรรทัด 228-235 · [ต้นฉบับ](../original/post.md) · ภาพ: ![explicit vs latent](../original/image-20.png) · วันที่ค้นคว้า: 2026-09-20

โพสต์บอกว่าเราเขียน condition กับ reasoning ไปพร้อมกันได้ และแนบ paper `The Latent Space: Foundation, Evolution, Mechanism, Ability, and Outlook` ภาพเทียบ explicit space กับ latent space: explicit มี human-readable, evaluability, controllability, discrete/symbolic แต่ inefficient/semantically lossy; latent มี machine-native, operability, expressiveness, scalability, generalization, high-fidelity แต่ตีความยากกว่า

paper ระบุว่า latent space กำลังเป็น native substrate สำหรับ language-based models และงานจำนวนมากพบว่ากระบวนการภายในหลายอย่างเหมาะกับ continuous latent space มากกว่า explicit token-level generation ผู้เขียนจัด landscape เป็น Foundation, Evolution, Mechanism, Ability, Outlook และพูดถึง reasoning, planning, modeling, perception, memory, collaboration, embodiment ([arXiv:2604.02029](https://arxiv.org/abs/2604.02029)).

การเขียน condition กับ reasoning ร่วมกันหมายถึงไม่ต้องแยก “กฎ” เป็น if/else ยาว ๆ แล้วค่อยเรียก AI ด้านนอกเสมอไป เราอาจ encode condition เป็น constraints, masks, reward shaping, verifier หรือ symbolic pruning ที่อยู่ใน loop reasoning ตัวอย่างเกม: NPC อยากช่วยเพื่อน แต่กฎบอกห้ามเดินเข้ากองไฟ ระบบจึง propose action หลายทางใน latent แล้ว prune ทางที่ผิดกฎก่อน commit

แบบฝึก: เขียน state `hungry, afraid, friend_near, fire_near` แล้วให้ score action ด้วย weighted reasoning เช่น หาอาหาร, หนี, ช่วยเพื่อน จากนั้นเพิ่ม hard constraint “ถ้า fire_near ห้าม move_toward_fire” เปรียบเทียบกับ if/else nested จะเห็นว่ากฎบางอย่างอยู่เป็น verifier ได้

ข้อจำกัด: latent space ไม่ได้แทน explicit space ทุกอย่าง งานที่ต้อง audit เช่น กฎหมาย การเงิน หรือ safety ยังต้องมี representation ที่อ่านและตรวจได้

คำถามฝึก: condition ใดของคุณควรเป็น hard rule และ condition ใดควรเป็น soft preference?

<a id="research-review-2"></a>

## ตรวจสอบและค้นคว้าเพิ่มเติม — รอบ 2

<!-- RESEARCH_REVIEW_2_START -->
วันที่ตรวจเพิ่ม: 2026-09-20

**คำถามวิจัย:** “เขียน condition กับ reasoning ไปพร้อมกัน” ทำได้ที่ชั้นใดบ้าง? แหล่งใหม่คือ OpenAI Structured Outputs ซึ่งอธิบายการให้โมเดลสร้าง output ให้ตรง JSON Schema ตามเอกสาร official [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs). อีกแหล่งคือ Decode-Time Grammars ปี 2026 ซึ่งเสนอ grammar fragments ที่ผูกกับ runtime environment เพื่อกัน ghost references เช่นชื่อตัวแปรหรือ field ที่ไม่มีอยู่จริง [arXiv:2607.18357](https://arxiv.org/abs/2607.18357).

**กลไกที่เกี่ยวกับโพสต์:** condition อาจเข้าไปใน reasoning ได้หลายระดับ: mask token ตอน decode, grammar/schema ของ output, runtime symbol table, lattice ของ candidate, หรือ verifier หลัง propose จุดสำคัญคือแต่ละชั้นคุมคนละความผิด JSON schema กัน field หายหรือ enum หลุด schema ได้ แต่ไม่ได้พิสูจน์ logic ของ quest; environment-indexed grammar กัน reference ผิดได้ แต่ยังไม่รู้ว่า algorithm ดีที่สุดหรือ rule ทั้งระบบ consistent หรือไม่

**ผลเชิงปฏิบัติ:** ถ้าทำ Rust latent space สำหรับเกม ให้แยก condition เป็น data structure ไม่ใช่ if/else กระจัดกระจาย เช่น `allowed_items(zone)`, `valid_targets(npc_state)`, `cooldown_rules`, `economy_invariants` แล้วให้ proposer เห็น mask/constraint ตั้งแต่ต้น วิธีนี้ช่วยลด invalid output ก่อน validator แต่ยังต้องมี fallback เมื่อ constraint ชนกันจนไม่มีทางออก

**แบบฝึก:** สร้าง mini quest decoder ที่ grammar บังคับ `{giver,target,item,reward}` และ runtime environment มี item เฉพาะ zone ถ้า zone ไม่มี `milk` decoder ต้องไม่เลือก `milk` ตั้งแต่แรก จากนั้นให้ verifier ตรวจ timeline และ economy เพิ่ม Caveat คือ grammar-constrained decoding อาจเพิ่ม overhead และถ้า schema ออกแบบแคบเกินไปจะตัด quest ดี ๆ ทิ้ง
<!-- RESEARCH_REVIEW_2_END -->

<!-- POST_NAV_START -->
---

[สารบัญ](README.md) · [← โพสต์ 031](031-primitive-first-vs-compose-first.md) · [โพสต์ 033 →](033-noob-learning-streams.md)

หัวข้อที่เกี่ยวข้อง: [03 Neuro-symbolic, constraints, types และการตรวจคำตอบ](topics/03-neuro-symbolic-types-and-verification.md) · [09 RAG, code healing และความเป็นส่วนตัวของ embedding](topics/09-rag-code-healing-and-privacy.md)
<!-- POST_NAV_END -->
