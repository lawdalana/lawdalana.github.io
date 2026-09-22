---
title: "Jev by TypeSafe AI: System One Model สำหรับ Typed Decisions"
notetype: feed
date: 2026-09-22
last_modified: 2026-09-22
tags: [AI, Jev, TypeSafe-AI, System-One, RLCD, structured-output, calibrated-confidence, model-routing, AI-agents]
status: published
---

# Jev by TypeSafe AI: เมื่อ AI ไม่ต้องเขียนข้อความ แต่ต้องตัดสินใจให้โค้ดใช้ต่อได้

![Jev System One decision flow](/assets/img/LLM/Jev/jev-system-one-flow.svg)

> **ข้อมูล ณ วันที่ 22 กันยายน 2026:** TypeSafe AI เปิดตัว Jev เมื่อ 15 กันยายน 2026 และผลิตภัณฑ์ยังอยู่ในช่วงต้น บทความนี้อ้างอิงเอกสารของ TypeSafe, model card, cookbooks, privacy policy และข้อมูลการใช้งานจาก Vercel โดยแยก **ข้อเท็จจริงที่ตรวจสอบได้** ออกจาก **ตัวเลข benchmark ที่บริษัทผู้พัฒนาเผยแพร่เอง**

## TL;DR

- **Jev ไม่ใช่ chat LLM และไม่ใช่โมเดลสำหรับเขียนข้อความหรือโค้ด** แต่เป็นโมเดลตัดสินใจเชิงความหมาย (probabilistic decision model) ที่รับ `state` กับคำถามแบบมีชนิด แล้วคืนค่าที่โค้ดใช้ได้โดยตรง
- คำถามมีสาม primitive: **Choice** เลือกหนึ่งตัวเลือก, **Score** ให้คะแนนตาม rubric และ **Noul** คืนความน่าจะเป็นของคำตอบแบบ yes/no
- จุดต่างสำคัญจาก LLM ที่ใช้ JSON mode คือ Jev คืน **probability distribution เป็นผลลัพธ์หลักของโมเดล** และประเมินหลายคำถามต่อ state เดียวอย่างอิสระและขนานกัน
- คำว่า **type-safe** หมายถึงผลลัพธ์ไม่หลุดจาก answer space ที่กำหนด ไม่ได้แปลว่าคำตอบถูกเสมอไป Jev ยังเลือกตัวเลือกที่ผิดได้
- รุ่นปัจจุบันขณะเขียนคือ `jev-1.13.0`; direct API คิดราคา **$0.042 ต่อ 1 ล้าน input tokens** และไม่คิด output tokens
- งานที่เหมาะคือ classification, routing, scoring, reranking, guardrails, citation checking และการตัดสินใจย่อยใน agent harness
- งานที่ไม่เหมาะคือ generation, การคำนวณแม่นยำ, การนับ, การเปรียบเทียบวันที่, reasoning หลายทอด และ input ที่เต็มไปด้วยรายละเอียดไม่เกี่ยวข้อง
- แนวทาง production ที่ปลอดภัยคือ **ให้โค้ดควบคุม workflow และ side effects**, ใช้ Jev เฉพาะ semantic judgment, วัดผลกับ labeled data ของตนเอง และส่งกรณีไม่แน่ใจไปให้คนหรือ reasoning model

---

## Jev คืออะไร

[Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) คือโมเดลสาธารณะตัวแรกในกลุ่มที่ TypeSafe AI เรียกว่า **System One Models** เป้าหมายไม่ใช่สร้างข้อความให้มนุษย์อ่าน แต่สร้างการตัดสินใจแบบมีโครงสร้างให้ซอฟต์แวร์นำไป branch, rank, route หรือ threshold ต่อได้

อินเทอร์เฟซหลักย่อได้เป็น

```text
state + typed questions
        ↓
       Jev
        ↓
typed answers + probabilities (+ confidence บางชนิด)
```

ตัวอย่างเช่น ระบบ support อาจส่งข้อความลูกค้า นโยบายคืนเงิน และข้อมูลคำสั่งซื้อเป็น `state` แล้วถามพร้อมกันว่า

- ควรส่ง ticket ไปทีมใด
- ปัญหารุนแรงระดับไหน
- ลูกค้าขอคืนเงินจริงหรือไม่

โค้ดเป็นผู้ตัดสินใจขั้นสุดท้ายว่าจะ assign งาน, ขอข้อมูลเพิ่ม, ส่งให้มนุษย์ตรวจ หรือเรียกโมเดลที่ reasoning ได้ลึกกว่า

ชื่อ **System One** อ้างอิงแนวคิด System 1 ในหนังสือ *Thinking, Fast and Slow*—การตัดสินใจที่เร็วและเฉพาะจุด ส่วนชื่อ **Jev** มาจาก William Stanley Jevons และแนวคิด Jevons paradox: เมื่อประสิทธิภาพดีขึ้นและต้นทุนลดลง ปริมาณการใช้งานอาจเพิ่มขึ้นแทนที่จะลดลง

### สิ่งที่ Jev ไม่ใช่

- ไม่ใช่โมเดลแทน Claude, GPT หรือโมเดลหลักของ coding agent
- ไม่สนทนา ไม่เขียนคำอธิบาย ไม่สร้างโค้ด และไม่เรียก tool เอง
- ไม่ใช่ workflow engine หรือ authorization layer
- ไม่ได้เข้าถึงฐานข้อมูล ไฟล์ หรือนโยบายของเราเอง เว้นแต่ application จะส่งหลักฐานเหล่านั้นมาใน `state`

จึงควรมอง Jev เป็น **semantic function ภายในโปรแกรม** มากกว่าเป็นผู้ช่วยสนทนา

---

## สัญญาการเรียกใช้: State, Questions, Answers

### 1. State

`state` คือข้อมูลที่โมเดลต้องพิจารณา รับได้เป็น string, JSON object หรือ array ของข้อความ การใช้ object มักดีกว่าเพราะตั้งชื่อ field และระบุความสัมพันธ์ได้ชัด

```json
{
  "ticket": {
    "message": "I was charged twice. Please refund the duplicate.",
    "plan": "pro"
  },
  "policy": {
    "duplicate_charge": "Eligible for refund after verification"
  }
}
```

หลักสำคัญคือส่งเฉพาะข้อมูลที่จำเป็นต่อคำถาม การยัดทั้งเอกสารหรือทั้งประวัติเข้าไปโดยไม่กรองทำให้เสียทั้ง token และ accuracy

### 2. Typed Questions

| Primitive | ใช้เมื่อ | ผลลัพธ์หลัก | ข้อจำกัดปัจจุบัน |
|---|---|---|---|
| **Choice** | เลือกหนึ่งคำตอบจากชุดที่กำหนด | `choice`, probability ของทุก option, `confidence` | สูงสุด 255 options |
| **Score** | ประเมินตำแหน่งบนสเกลที่มีคำอธิบาย | weighted `score`, probability ของทุก level, `confidence` | 2–10 levels |
| **Noul** | คำถาม yes/no ที่ต้องการความน่าจะเป็น | `noul` ระหว่าง 0–1 | ไม่มี `confidence` แยก |

#### Choice

เหมาะกับ category ที่ไม่มีลำดับ เช่น `billing`, `technical`, `account` ผลลัพธ์ประกอบด้วยตัวเลือกที่ probability สูงสุดและ distribution ครบทุกตัวเลือก ควรเพิ่ม `other` หรือ `none_of_the_above` เมื่อ taxonomy อาจไม่ครอบคลุม input

#### Score

เหมาะกับมิติที่เรียงลำดับได้ เช่นความรุนแรงของ incident โดยแต่ละ level ต้องเป็นคำอธิบายสถานการณ์จริง ไม่ใช่เพียง `low`, `medium`, `high`

```text
0: Cosmetic; functionality still works
1: Feature degraded; workaround exists
2: Blocking; no workaround exists
```

ค่า `score` คือค่าเฉลี่ยถ่วงน้ำหนักจาก probability ของแต่ละ level จึงอาจอยู่ระหว่าง level เช่น `1.3` และต้องอ่าน distribution ประกอบ ไม่ควรตีความเป็นการวัดเชิงปริมาณที่แม่นยำ

#### Noul

Noul คืนค่า probability ว่าข้อความเป็นจริงหรือคำตอบคือ “ใช่” เช่น `0.95` หมายถึง strong yes, `0.05` หมายถึง strong no และค่าราว `0.5` หมายถึงสองฝั่งใกล้เคียงกัน

Noul ไม่ใช่สเกลระดับกลาง ตัวอย่างเช่น `0.5` ของคำถาม “ผู้สมัครเก่ง Python หรือไม่” ไม่ได้แปลว่าทักษะอยู่ระดับกลาง แต่แปลว่าโมเดลยังแบ่งน้ำหนักระหว่าง yes/no เท่า ๆ กัน หากต้องการวัดระดับทักษะควรใช้ Score

### 3. Answers

คำตอบทุกตัวอยู่ใต้ question ID เดิม แต่ ID มีไว้ให้โค้ด map ผลลัพธ์กลับเท่านั้น ตัวโมเดลไม่ได้เห็น ID ดังนั้น `instructions` ต้องเขียนคำถามให้ครบถ้วน ไม่ควรหวังว่า key ชื่อ `refund_requested` จะช่วยอธิบายคำถาม

---

## Probability กับ Confidence ไม่ใช่สิ่งเดียวกัน

สำหรับ Choice และ Score, Jev คืนทั้ง `probabilities` และ `confidence`

- **Probability** บอกน้ำหนักของ outcome แต่ละตัว
- **Confidence** สรุปรูปร่างของ distribution ว่ากระจุกหรือกระจายเพียงใด

สมมติ Choice มีสามทีม

```json
{
  "billing": 0.48,
  "technical": 0.46,
  "account": 0.06
}
```

`billing` ยังเป็นคำตอบอันดับหนึ่ง แต่การกระจายเกือบเท่ากับ `technical` บ่งชี้ว่ากรณีนี้กำกวมและควรเข้าสู่ review path

สิ่งที่ต้องระวังมีสามข้อ

1. **Confidence สูงไม่รับประกันว่าถูก** มันบอกว่าการกระจายของโมเดลชัด ไม่ใช่ ground truth
2. **Calibration เป็นคุณสมบัติของกลุ่มตัวอย่าง** ถ้าคำตอบที่ให้ probability 0.8 ถูกประมาณ 80% เมื่อดูหลายกรณี จึงเรียกว่า calibrated; ไม่ได้ทำให้กรณีใดกรณีหนึ่งถูก 80%
3. **Threshold ต้องตั้งจากข้อมูลของงานจริง** ค่า 0.7 หรือ 0.9 ในตัวอย่างเอกสารเป็นเพียงจุดเริ่มต้น ความเสียหายจาก false positive และ false negative ของแต่ละ action ไม่เท่ากัน

กรณี read-only ที่แก้ย้อนกลับง่ายอาจใช้ threshold ต่ำกว่า action ที่โอนเงิน ลบข้อมูล หรือแตะ production

---

## ตัวอย่าง Python: ให้โมเดลจำแนก แต่ให้โค้ดตัดสินใจ

ติดตั้ง official SDK และกำหนด `TYPESAFE_API_KEY`

```bash
pip install typesafe-sdk
```

ตัวอย่างต่อไป pin รุ่นโมเดลเพื่อไม่ให้ behavior เปลี่ยนเมื่อ alias `jev-latest` ถูกเลื่อนไปรุ่นใหม่

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

state = {
    "ticket": {
        "message": (
            "My Stripe connection has failed for three days and I am "
            "losing sales. Please refund this month."
        ),
        "plan": "pro",
    },
    "policy": {
        "refunds": "Refunds require a separate eligibility check."
    },
}

questions = {
    "department": Choice(
        instructions="Which team can resolve the primary problem in `ticket.message`?",
        criteria={
            "billing": "Charges, invoices, subscriptions, and refunds",
            "technical": "Bugs, outages, and integration failures",
            "account": "Login, permissions, and profile changes",
            "other": "The request does not fit the other options",
        },
    ),
    "severity": Score(
        instructions="How severe is the reported operational impact?",
        criteria=[
            "Cosmetic or informational; work is unaffected",
            "Degraded, but a practical workaround exists",
            "Blocking with no workaround",
            "Blocking and causing financial or data loss",
        ],
    ),
    "refund_requested": Noul(
        instructions="Does `ticket.message` explicitly ask for money back?"
    ),
}

with TypeSafeClient() as client:
    response = client.system_one(
        state=state,
        questions=questions,
        model="jev-1.13.0",
    )

department = response.answers["department"]
severity = response.answers["severity"]
refund_requested = response.answers["refund_requested"]

selected_probability = department.probabilities[department.choice]

if department.confidence < 0.70 or selected_probability < 0.75:
    decision = {"action": "human_review", "reason": "ambiguous_department"}
else:
    decision = {
        "action": "assign",
        "department": department.choice,
        "severity": severity.score,
        # นี่คือการตรวจ intent เท่านั้น ไม่ใช่การอนุมัติคืนเงิน
        "refund_requested": refund_requested.noul >= 0.80,
    }
```

ตัวอย่างนี้จงใจไม่แสดง output ตายตัว เพราะผล inference อาจเปลี่ยนได้ ประเด็นสำคัญคือ **Jev จำแนก intent แต่โค้ดยังต้องตรวจสิทธิ์ นโยบาย และข้อมูลธุรกรรมก่อนอนุมัติ refund**

---

## ต่างจาก Structured Output ของ LLM อย่างไร

LLM ทั่วไปก็สามารถคืน JSON ที่ตรง schema ได้ คำถามจึงไม่ใช่ว่า “ทำ structured output ได้หรือไม่” แต่คือโมเดลถูกออกแบบและฝึกมาเพื่ออะไร

| มิติ | Jev | LLM + Structured Output |
|---|---|---|
| งานหลัก | การตัดสินใจแบบ bounded | สร้างข้อความ, reasoning, code และ tool use |
| Answer space | นิยามล่วงหน้าด้วย Choice/Score/Noul | นิยามผ่าน JSON schema หรือ tool schema |
| Probability | เป็น native output; Choice/Score คืน distribution ครบ | มักไม่มี หรือเป็นตัวเลขที่โมเดล generate ตาม prompt |
| หลายคำถาม | ประเมินอิสระและขนานกับ state เดียว | มักตอบร่วมกันใน generation เดียว จึงมี hidden interaction ได้ |
| Generation | ไม่มี | มี |
| Media/tool use | ไม่มี; ต้อง preprocess และให้โค้ดจัดการ | หลายรุ่นรองรับภาพ เสียง และ tools |
| Failure mode หลัก | เลือกคำตอบที่อนุญาตแต่ผิด | เลือกผิด, format ผิด หรือ generate เกินขอบเขตตามระบบที่ใช้ |

Jev เหมาะเมื่อ output ที่ต้องการ **ปิดขอบเขตได้ล่วงหน้า** และ application ต้องการ probability เพื่อกำหนดเส้นทางต่อ ส่วน LLM เหมาะกว่าเมื่อระบบต้องสร้างคำตอบใหม่ สืบค้นด้วย tools อธิบายเหตุผล หรือแก้ปัญหาหลายขั้น

สองแบบนี้จึงใช้ร่วมกันได้ เช่น Jev route request หรือคัดกรองความเสี่ยงก่อนส่งงานซับซ้อนไป reasoning model

---

## “Zero Hallucinations” ต้องตีความอย่างระมัดระวัง

หน้าเว็บ TypeSafe ใช้คำว่า **“Zero Hallucinations”** และบทความเปิดตัวกล่าวว่า Jev “can’t hallucinate” ข้อความนี้จริงเฉพาะนิยามที่แคบมาก

### สิ่งที่รับประกันได้

- โมเดลไม่สร้าง prose นอก schema
- Choice คืนเฉพาะ option ที่ผู้พัฒนากำหนด
- Score อยู่ในช่วง level ที่กำหนด
- response มีรูปแบบที่โค้ด parse ได้

### สิ่งที่รับประกันไม่ได้

- option ที่เลือกถูกต้องตามโลกจริง
- probability calibrated กับโดเมนของเราโดยไม่ทดสอบ
- input ที่ขาดหลักฐานจะไม่ทำให้โมเดลเดา
- adversarial text หรือ prompt injection ใน `state` จะไม่มีผล
- confidence สูงจะไม่เกิดพร้อมคำตอบที่ผิด

ดังนั้นคำอธิบายที่แม่นกว่าคือ **“ไม่มี schema hallucination แต่ยังมี semantic decision error ได้”** Type safety ลด failure surface ที่สำคัญ แต่ไม่เท่ากับ factual correctness

---

## Model card และราคา ณ 22 กันยายน 2026

| รายการ | Direct TypeSafe API |
|---|---|
| รุ่น stable | `jev-1.13.0` |
| aliases | `jev-latest`, `jev-preview` ซึ่งขณะเขียนชี้ไป `jev-1.13.0` |
| ราคา input | **$0.042 / 1M tokens** หรือ $42 / 1B tokens |
| ราคา output | ไม่คิดค่าใช้จ่าย |
| Rate limit ที่ประกาศ | 250,000 tokens/วินาที และ 1,200 requests/นาที; บริษัทระบุว่าอาจปรับแบบ dynamic |
| Context | 64k tokens ต่อ request รวม; `state` + คำถามที่ยาวที่สุดต้องไม่เกิน 32k |
| Input | ข้อความเท่านั้น ผ่าน string/object/array |
| ภาษา | English เป็นภาษาหลัก; ภาษาอื่นรวม CJK รองรับแต่คุณภาพไม่เท่ากัน |

TypeSafe ระบุว่า query ส่วนใหญ่ใช้เวลาประมาณ **100 ms** และบทความเปิดตัวให้ช่วง end-to-end ราว **70–500 ms** อย่างไรก็ตาม latency จริงขึ้นกับ region, network, load, ขนาด state และ integration provider

หากเรียกผ่าน Vercel AI Gateway เอกสาร Vercel แสดง model ID `typesafe-ai/jev`, ราคาเท่ากัน และ context 32k ดังนั้นอย่านำ limit ของ direct API ไปสมมติว่าใช้กับ gateway ทุกแห่งโดยอัตโนมัติ

### Pin รุ่นใน production

`jev-latest` สะดวกสำหรับทดลอง แต่ alias จะเคลื่อนเมื่อมีรุ่นใหม่ ทำให้คำตอบเปลี่ยนได้โดย code ไม่เปลี่ยน หาก threshold ผ่านการ tune กับรุ่นใดแล้วควร

1. pin versioned ID เช่น `jev-1.13.0`
2. log `response.model` ทุกครั้ง
3. run regression/evaluation ก่อนย้ายรุ่น

---

## ทำไม Parallel Questions จึงสำคัญ

Jev อ่าน `state` ครั้งเดียว แล้วประเมินคำถามแต่ละข้ออย่างอิสระและขนานกัน จึงเหมาะกับ pattern **speculative fan-out**: ถามทุกสิ่งที่อาจต้องใช้ใน request เดียว แล้วให้โค้ดเลือกอ่านเฉพาะคำตอบที่เกี่ยวข้อง

```text
หนึ่ง state
  ├─ Choice: topic
  ├─ Noul: contains PII?
  ├─ Noul: asks for refund?
  ├─ Score: urgency
  └─ Score: frustration
```

ข้อดีคือ

- ไม่ส่ง state เดิมซ้ำหลายรอบ
- ลด network round trips
- การเพิ่มคำถามหนึ่งข้อไม่กลายเป็น hidden context ของอีกข้อ
- โค้ดสามารถ ignore speculative answer ที่ไม่เกี่ยวกับเส้นทางจริง

[TypeSafe cookbook เรื่อง parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions) ทดสอบคำถาม 13 ข้อกับบทความ GDPR โดยเรียกซ้ำแบบ batch และแยกข้ออย่างละ 5 รอบ รายงานว่า batch ถูกกว่า **12.2 เท่า** และเร็วกว่า **10.0 เท่า** โดยไม่พบการเปลี่ยนคำตอบจากวิธี batching ในตัวอย่างนั้น

ต้องอ่านผลนี้ตามขอบเขต: เป็นการทดลองของ TypeSafe เอง ใช้ Jev 1.12 กับเอกสารและชุดคำถามเดียว ไม่ใช่หลักฐานว่าทุก workload จะได้อัตราเร่งเท่ากัน

---

## หลักฐานด้านประสิทธิภาพ: อะไรวัดได้ และอะไรยังเป็น claim

### ตัวเลขที่ TypeSafe รายงาน

หน้าเปิดตัวอ้างว่าใน workflow evals ของบริษัท Jev เร็วกว่า **193.6 เท่า** และถูกกว่า **444.6 เท่า** เมื่อเทียบกับ LLM ใน System One-shaped workflows บริษัทเองระบุว่าตัวเลขนี้น่าจะอยู่ด้านสูงของประโยชน์ที่พบในงานจริง

วิธีประเมินมีข้อควรรู้

- ใช้ workflow 4 แบบที่ทีม model capabilities ของ TypeSafe สร้าง
- แตกงานเป็นคำถามย่อยและ logic ในโค้ด
- ใช้ค่าเฉลี่ยคำตอบจาก GPT-6 Astra และ Fable 5.1 เป็น reference probabilities
- บังคับ LLM คู่แข่งผ่าน System One adapter เพื่อคืน probability-compatible outputs
- reference ไม่ใช่ human ground truth แบบ benchmark classification ทั่วไป
- ผู้สร้าง eval เป็นผู้สร้างโมเดล จึงยังต้องการ replication จากบุคคลที่สาม

ตัวเลขจึงแสดงว่า architecture แบบ specialized decision model **มีโอกาสได้ cost/latency advantage สูง** แต่ยังไม่ควรถูกอ่านเป็นข้อพิสูจน์ว่า Jev ฉลาดกว่า LLM ทุกงาน

### ผล cookbook ที่ตรวจสอบโค้ดและ cache ได้

TypeSafe เผยแพร่ cookbooks พร้อมโค้ดและ cached responses เช่น

- **Legal reranking:** BM25 shortlist 30 passages สำหรับ 40 CLERC queries แล้วใช้ Jev rerank; top-1 accuracy เพิ่มจาก 5% เป็น 18% และ top-10 จาก 38% เป็น 62%
- **Citation checking:** ตัวอย่าง 8 citations เกี่ยวกับ RFC 7519 ตรวจพบ planted failures ทั้ง 4 กรณี; citation ที่ถูก 4 กรณีได้ verdict `verified` ด้วย confidence อย่างน้อย 0.93
- **Parallel questions:** batch 13 คำถามใน request เดียวลด cost และ latency ตามตัวเลขด้านบน

ทั้งหมดเป็นหลักฐานที่ดีกว่า screenshot เพราะมีวิธีทดลอง แต่ยังเป็น **vendor-published examples** และส่วนใหญ่ใช้ Jev 1.12 จึงต้องทดสอบซ้ำกับข้อมูล production ของเรา

### Adoption signal จาก Vercel

[Vercel รายงาน](https://vercel.com/blog/ai-gateway-jev-model-launch) ว่าภายใน 24 ชั่วโมงแรก Jev ถูกใช้โดยเกือบ 13% ของ paid teams บน AI Gateway มากกว่าสถิติเปิดตัวโมเดลก่อนหน้าบน gateway ของ Vercel ตัวเลขนี้สะท้อนความสนใจช่วงเปิดตัว ไม่ใช่การพิสูจน์ accuracy หรือการใช้งานระยะยาว และ Vercel เองก็ระบุว่าคำถามถัดไปคือ adoption จะคงอยู่หรือไม่

---

## งานที่เหมาะกับ Jev

### 1. Classification และ Routing

- จัด ticket ไปทีมที่เหมาะ
- เลือก model หรือ subagent จาก allowlist
- เลือก tool category ก่อนให้โค้ดตรวจ permission อีกชั้น
- จัดประเภทเอกสาร ผลิตภัณฑ์ หรือ intent

### 2. Scoring และ Prioritization

- severity, urgency, relevance, quality
- sentiment หรือ frustration ตาม rubric ที่เขียนชัด
- risk indicator หลายมิติ ก่อนรวมด้วย weight ในโค้ด

### 3. Retrieval และ Reranking

- ให้ lexical/embedding search สร้าง shortlist ก่อน
- ให้ Jev ประเมิน query–candidate relevance
- sort ด้วย Noul probability หรือ Score

ไม่ควรส่ง corpus ทั้งหมดให้ Jev โดยตรงเมื่อ code หรือ retrieval system สามารถลด candidate ได้ก่อน

### 4. LLM Guardrails และ Verification

- ตรวจ prompt injection หรือ policy violation
- ตรวจ tool-call intent และ risk
- ตรวจว่าคำตอบ address คำถามหรือไม่
- ตรวจว่า citation support claim หรือไม่

Guardrail ก็เป็น model และถูกโจมตีหรือผิดได้ จึงควรเป็นหนึ่ง layer ใน defense-in-depth ไม่ใช่ security boundary เพียงชั้นเดียว

### 5. Feature Extraction

Probability ของคำถามย่อยสามารถเป็น feature ให้ classical ML model ต่อ เช่น churn, fraud หรือ lead scoring โดย logic การรวมอยู่ภายนอก Jev และตรวจสอบได้

### 6. Real-time Semantic Decisions

Latency ระดับร้อยมิลลิวินาทีทำให้ใช้ใน UI, เกม หรือ request path ที่ LLM reasoning ปกติช้าเกินไปได้ ตราบใดที่ action space ถูกจำกัดและมี fallback

---

## ข้อจำกัดของ Jev 1.13 ที่ TypeSafe ระบุเอง

เอกสาร [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) เปิดเผย failure modes ไว้ค่อนข้างตรงไปตรงมา

| ข้อจำกัด | อาการ | วิธีออกแบบแทน |
|---|---|---|
| Literal reading | ตอบตามถ้อยคำ ไม่ได้เดา intent ที่ผู้เขียนละไว้ | เขียน condition และ boundary cases ให้ตรง |
| Math และ counting | นับคำ รายการ หรือคำนวณไม่แม่น | parse, count และคำนวณในโค้ด |
| Date/time comparison | เรียงวันที่หรือคำนวณช่วงเวลาไม่น่าเชื่อถือ | ให้โมเดล extract component แล้วให้โค้ดเทียบ |
| Indirection | ความแม่นลดเมื่อมี double negative หรือหลาย reasoning hops | ลดจำนวนทอดและชี้ field ที่เกี่ยวข้องโดยตรง |
| Context rot | state ใหญ่และมี distractors ทำให้ accuracy ลด | retrieve/filter ก่อนส่ง |
| Adversarial content | ไม่ถือว่า state เป็น hostile โดย default | ทดสอบ prompt injection และใช้ controls ชั้นอื่น |
| Contradictory criteria | instructions กับ criteria ขัดกันทำให้สับสน | ทำ rubric ให้สอดคล้องกัน |
| Structural invariants | คำถามเดียวกันคนละ primitive หรือคำถามกับ negation อาจไม่รวมกันตามสมการที่คาด | ใช้ formulation เดียวและ tune threshold แยก |
| Generation | ไม่ได้ฝึกให้เขียนข้อความ | ใช้ generative model |
| Non-English | English แม่นที่สุด ภาษาอื่นคุณภาพไม่เท่ากัน | ทำ evaluation แยกตามภาษา |
| Non-text input | รับภาพ เสียง วิดีโอ หรือ binary โดยตรงไม่ได้ | extract/OCR/transcribe ก่อน และตรวจคุณภาพ extraction |

ประเด็น adversarial content สำคัญมากสำหรับงาน guardrail: หากข้อความผู้ใช้มีคำสั่งพยายามชักนำ classifier, Jev 1.13 ยังอาจถูก steer ได้ เอกสารแนะนำให้เขียน criteria ชัดและทดสอบ edge cases แต่สำหรับ action ที่มีผลร้ายแรงควรมี deterministic validation และ permission enforcement เพิ่มเสมอ

---

## Blueprint สำหรับใช้ใน Production

### 1. เริ่มจาก decision ที่มีขอบเขต

เขียนก่อนว่า application ต้องเลือกอะไร เช่น `approve | review | reject` ไม่ใช่เริ่มจาก prompt กว้างอย่าง “วิเคราะห์คำขอนี้แล้วทำสิ่งที่เหมาะสม”

### 2. ให้โค้ดทำสิ่งที่โค้ดทำได้แน่นอน

- คำนวณตัวเลขและวันที่
- ตรวจ permission และ account state
- validate schema และ identifier
- execute side effects
- enforce allowlist/denylist ที่เป็นกฎตายตัว

ใช้ Jev เฉพาะส่วนที่ต้องตีความภาษา บริบท หรือความหมาย

### 3. แตก judgment ให้ atomic

แทนคำถาม “ควรอนุมัติ refund หรือไม่” ให้แยกเป็น

- ลูกค้าขอ refund หรือไม่
- หลักฐานบ่งชี้ duplicate charge หรือไม่
- ข้อความตรงกับข้อยกเว้นของ policy หรือไม่

จากนั้นให้โค้ดตรวจ transaction จริงและรวมเงื่อนไข

### 4. ส่ง context เท่าที่จำเป็น

อย่าใช้ context window เป็นเป้าหมายที่ต้องเติมให้เต็ม ยิ่งมีข้อมูลไม่เกี่ยวข้อง ยิ่งเพิ่ม distractor และความเสี่ยงด้าน privacy

### 5. Fan-out คำถามที่ใช้ state เดียวกัน

รวมคำถามอิสระใน call เดียว แล้วให้โค้ดเลือกใช้ผลตามเส้นทาง ไม่ต้องสร้าง serial chain ถ้าคำถามข้อหลังไม่ได้พึ่งคำตอบข้อแรกจริง ๆ

### 6. สร้าง labeled evaluation set

เก็บตัวอย่างจากงานจริง ครอบคลุม

- กรณีชัดและกำกวม
- class imbalance
- ภาษาที่ใช้งานจริง
- adversarial และ out-of-distribution input
- failure ของ upstream extraction

วัด accuracy, calibration, coverage หลัง confidence gate และต้นทุนของข้อผิดพลาดแต่ละชนิด

### 7. ตั้ง threshold ต่อ action

อย่ามี “threshold ของโมเดล” เพียงค่าเดียว ควรมี threshold ตามผลกระทบ

```text
read-only suggestion   → threshold ต่ำกว่า
customer-facing change → threshold สูงขึ้น + confirmation
destructive action     → deterministic authorization + human approval
```

### 8. ออกแบบ fallback และ failure path

จัดการ `429`, `529`, timeout และ malformed response โดยไม่ทำ ticket หายหรือ default ไป action ที่เสี่ยง SDK มี retry/backoff แต่ application ยังต้องมี fallback ที่ปลอดภัย

### 9. Pin, log และ version ทุกอย่าง

เก็บ model version, question definitions, criteria, threshold, state schema และ outcome เพื่อ replay regression ได้

### 10. แยก Classification ออกจาก Authorization

Jev อาจบอกว่า command “ดูเหมือนปลอดภัย” หรือผู้ใช้ “ต้องการ refund” ได้ แต่ **ไม่มีสิทธิ์อนุมัติ action** Permission, entitlement, policy และ transaction truth ต้องตรวจด้วยระบบที่เชื่อถือได้อีกชั้น

---

## Data Privacy: “No Training” ไม่เท่ากับ “Zero Retention”

[Privacy Policy ของ TypeSafe](https://typesafe.ai/legal/privacy-policy) ระบุว่า

- บริการเก็บ prompts, data, instructions และ input ที่ผู้ใช้ส่ง
- จะไม่ใช้ Input ฝึกหรือ fine-tune โมเดล
- จะไม่เปิดเผย Input แก่บุคคลที่สามนอกจาก service providers
- เก็บ personal data เท่าที่เห็นว่าจำเป็นต่อการให้บริการหรือวัตถุประสงค์ทางธุรกิจ

ส่วน model docs ระบุว่า **Zero Data Retention (ZDR)** มีสำหรับ enterprise customers ขณะที่ Vercel AI Gateway ระบุว่าสามารถขอ ZDR และ No Training ต่อ request ได้

ข้อสรุปเชิงปฏิบัติคือ

- อย่าส่ง secret, credential หรือ PII ที่ไม่จำเป็น
- ทำ redaction/minimization ก่อนเรียก API
- ตรวจ DPA, region, retention และ subprocessor ให้ตรงข้อกำหนดองค์กร
- อย่าอนุมานว่า “ไม่เอาไปฝึก” หมายถึง “ไม่เก็บเลย”

---

## Integration ที่มีอยู่

- **HTTP API:** `POST https://api.typesafe.ai/v1/systemone`
- **Python SDK:** `typesafe-sdk`, รองรับ sync/async และ Python 3.10+
- **JavaScript/TypeScript SDK:** `@typesafe-ai/sdk`, รองรับ type inference และ Node.js 20+
- **Vercel AI SDK / AI Gateway:** evaluation model `typesafe-ai/jev` ผ่าน `experimental_evaluate`
- **Agent Skill:** context สำหรับ Claude Code, Codex และ agent อื่นเพื่อช่วยเขียน integration ให้ถูกต้อง
- **System One Adapter:** open-source wrapper สำหรับรัน LLM ผ่าน interface เดียวกันเพื่อเปรียบเทียบ cost, latency และคำตอบ

Agent Skill ไม่ได้เปลี่ยน Jev ให้เป็น coding model มันเพียงสอน coding agent ให้รู้วิธีสร้างระบบที่เรียก Jev

---

## เลือก Code, Jev หรือ LLM อย่างไร

| งาน | ตัวเลือกหลัก |
|---|---|
| คำนวณ, parse, validate, permission, exact matching | **Code** |
| ตัดสินเชิงความหมายจาก answer space จำกัด พร้อม probability | **Jev** |
| เขียนข้อความ, code, explanation หรือ content ใหม่ | **Generative LLM** |
| reasoning หลายขั้น, วางแผน, ใช้ tools | **Reasoning LLM / agent** |
| ตัดสินใจ bounded แล้วทำงานซับซ้อนต่อ | **Jev → code gate → LLM/agent** |
| action เสี่ยงสูง | **Model ช่วยแนะนำ + deterministic checks + human/explicit approval** |

กฎง่ายที่สุดคือ **ถ้า code คำนวณได้แน่นอน อย่าใช้โมเดล; ถ้าคำตอบกำหนดชุดล่วงหน้าได้และต้องตีความ semantics ให้พิจารณา Jev; ถ้าต้องสร้างหรือ reason ให้ใช้ LLM**

---

## มุมมองสรุป

Jev เสนอ abstraction ที่น่าสนใจ: แทนที่จะบังคับโมเดลสร้างข้อความแล้ว parse กลับมาเป็น decision ก็ฝึกและให้บริการโมเดลรอบ decision contract โดยตรง สิ่งที่มีคุณค่าที่สุดจึงไม่ใช่คำโฆษณา “ไม่มี hallucination” แต่คือ

- answer space ที่จำกัดตั้งแต่ต้น
- probability ที่ application ใช้กำหนด risk policy ได้
- การถามหลาย judgment ต่อ state เดียวแบบขนาน
- การทำให้ control flow กลับมาอยู่ในโค้ดที่ตรวจสอบและทดสอบได้

อย่างไรก็ตาม Jev ยังเป็นโมเดลที่เพิ่งเปิดตัว ตัวเลขเด่นส่วนใหญ่มาจาก TypeSafe เอง ความแม่นไม่สม่ำเสมอตาม task และเอกสารยอมรับจุดอ่อนเรื่อง math, dates, indirection, context rot และ adversarial input อย่างชัดเจน

ข้อสรุปที่สมเหตุสมผลคือ **Jev ไม่ได้แทน LLM แต่ลดจำนวนจุดที่เราจำเป็นต้องใช้ LLM ขนาดใหญ่** สำหรับงาน decision-shaped ที่มี volume สูงและ latency/cost สำคัญ มันควรค่าแก่การทำ proof of concept โดยมี labeled eval, confidence gate และ fallback ก่อนให้มีอำนาจกระทำการจริง

---

## Sources

### TypeSafe AI — แหล่งข้อมูลหลัก

- [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) — ประกาศเปิดตัว วิธีประเมิน และ caveats ของบริษัท
- [Introduction](https://docs.typesafe.ai/) และ [System One](https://docs.typesafe.ai/concepts/system-one)
- [Primitives: Choice, Score, Noul](https://docs.typesafe.ai/primitives)
- [Confidence](https://docs.typesafe.ai/confidence)
- [Models](https://docs.typesafe.ai/models) — รุ่น ราคา limits, context และ language support
- [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) — failure modes ที่ผู้พัฒนาระบุ
- [How to build with TypeSafe](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)
- [HTTP API](https://docs.typesafe.ai/api) และ [Client SDKs](https://docs.typesafe.ai/sdk)
- [Workflow evals](https://evals.typesafe.ai/)
- [Parallel questions cookbook](https://docs.typesafe.ai/cookbooks/parallel_questions)
- [Re-ranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
- [Citation checking cookbook](https://docs.typesafe.ai/cookbooks/citation_check)
- [Privacy Policy](https://typesafe.ai/legal/privacy-policy)

### Integration และข้อมูลจากบุคคลภายนอก

- Vercel — [How to classify, route, and score with Jev and AI SDK](https://vercel.com/kb/guide/typesafe-jev-and-ai-sdk)
- Vercel — [Jev is the fastest-adopted model in AI Gateway history](https://vercel.com/blog/ai-gateway-jev-model-launch)
- Vercel — [Jev vs. GPT-6 Astra](https://vercel.com/i/jev-vs-gpt-6-astra)

แหล่งข้อมูลทั้งหมดอ่านและตรวจสอบล่าสุดเมื่อ 22 กันยายน 2026 ตัวเลขราคา รุ่น limits และ integration อาจเปลี่ยนได้ ควรตรวจ model docs ก่อนนำไปใช้จริง

## Related Notes

- [[Agent Harness Engineering]]
- [[Agentic Code Review]]
- [[The Orchestration Tax]]
- [[RAG (Retrieval-Augmented Generation)]]
- [[Constraint Pruner: Neuro-Symbolic Token Pruning for LLM Generation]]

*เรียบเรียงและตรวจสอบล่าสุด: 22 กันยายน 2026*
