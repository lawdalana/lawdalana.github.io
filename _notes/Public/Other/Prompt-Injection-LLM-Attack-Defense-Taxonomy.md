---
title: "Prompt Injection & LLM Attack/Defense Taxonomy — จาก 200 Papers"
notetype: feed
date: 2026-06-09
last_modified: "2026-06-09"
tags: [llm, security, prompt-injection, ai-safety, research, survey]
status: published
---

# Prompt Injection & LLM Attack/Defense Taxonomy

> Synthesis จาก 200 papers (80 red team + 120 blue team) ที่ review ทั้งหมด 16.6M characters ของ evidence — จัดกลุ่มทุก attack sub-type และ defense sub-type ที่พบ พร้อม ASR benchmark อ้างอิง
>
> *อ้างอิง: Synthesis of 200 Papers on Prompt Injection, Jailbreak, Agent/RAG Security (2026-06-04)*

## Executive Summary

Prompt injection ไม่ใช่แค่ "ผู้ใช้พิมพ์ข้อความหลอก model" อีกต่อไป — แต่เป็นปัญหา **control-plane security** ของระบบ LLM ทั้งชุด เมื่อ LLM ต่อกับ RAG, browser, email, calendar, GUI, file system, plugin, MCP server, memory หรือ external tools, prompt injection กลายเป็นช่องทางให้ข้อมูลที่ไม่น่าเชื่อถือสั่งให้ระบบทำ action ที่มีผลจริง

**บทเรียนหลัก:** defense ที่ฝากความปลอดภัยไว้กับ prompt หรือ model behavior อย่างเดียว **ไม่พอ** — ต้องใช้ defense-in-depth

---

## ⚡ TL;DR — Attack & Defense at a Glance

### Attack Summary (9 Families, 56+40 = 96 Sub-types)

| Family | Sub-types | ASR Range | อันตรายสุด |
|--------|-----------|-----------|------------|
| **A1. Direct Injection** | 5 | 23.6% – 86.1% | HOUYI app attack (86.1%) |
| **A2. Indirect Injection (IPI)** | 9 | 70% – 100% | Calendar injection (94.6%), Email exfil (100%) |
| **A3. Agent/Tool/MCP Hijack** | 12 | 45.9% – 100% | Tool selection (100%), ObliInjection (99.6%) |
| **A4. RAG/Memory Poisoning** | 9 | 85% – 98.2% | BadRAG (98.2%), PoisonedRAG (97%) |
| **A5. Multimodal/GUI/Audio** | 9 | 34% – 100% | Image Hijacks (100%), Audio (98.1%), Mobile (93%) |
| **A6. Automated/Optimization** | 14 | 75% – 100% | GCG (100%), Adaptive (100%), ForgeDAN (98.5%) |
| **A7. Jailbreak/Safety Bypass** | 6 | 31% – 100% | Simple adaptive (100%), Poetry (Gemini 90–100%) |
| **A8. Encoding/Obfuscation** | 4 | varies | Bypass text-centric filters |
| **A9. Multi-agent/Supply Chain** | 9 | varies | Alignment poisoning, Agent-to-agent infection |

### Defense Summary (6 Families, 42+25 = 67 Sub-types)

| Family | Sub-types | Best ASR Achieved | แข็งแกร่งสุด |
|--------|-----------|-------------------|-------------|
| **D1. Instruction/Data Separation** | 8 | 0% – 2% | StruQ (0%), Spotlighting (<2%) |
| **D2. Detection/Guardrail** | 10 | 0.03% – 3.8% | InstructDetector (0.03%) |
| **D3. Auth/Privilege Control** | 6 | 0% – 3.9% | FATH (0%), Progent (1.0%) |
| **D4. Secure Architecture/IFC** | 10 | 0% – 4.8% | IFC (0%), Sanitizer (0%), ARGUS (3.8%) |
| **D5. Training/Alignment** | 10 | 0.9% – 8% | SecAlign (0–2%), SmoothLLM (~1%) |
| **D6. Runtime Verification** | 8 | 0% – 0.24% | MELON (0.24%), AttriGuard (0%), AgentSentry (0%) |

> ⚠️ **ASR จากต่าง benchmark ไม่สามารถเทียบกันตรงๆ ได้** — ค่าเหล่านี้เป็น reported range จากแต่ละ paper

## Attack Taxonomy

## Exhaustive Paper-by-Paper Sub-types (#101–#200)

> ทุก sub-type ที่ extract จาก paper #101–#200 โดยใช้หมายเลข paper อ้างอิง

### Attack Sub-types (40 entries)

| Paper | Family | Description | ASR/Result |
|-------|--------|-------------|------------|
| 101-1 | **A6** | PISmith: RL-based red teaming — GRPO with reward shaping to optimize injected prompts in black-box | ASR@10=1.0, ASR@1=0.87 |
| 104-1 | **A2** | LLMail-Inject: realistic adaptive prompt injection challenge dataset for email systems | — |
| 102-1 | **A5/A3** | EVA: evolving indirect PI against GUI agents — uses visual attention feedback to evolve payload | static 48% → >80% |
| 103-1 | **A5/A3** | AEIA-MN: active environmental injection against multimodal mobile agents | max 93% ASR |
| 109-1 | **A5/A3** | AgentTypo: adaptive typographic PI against black-box multimodal agents | — |
| 131-1 | **A3** | Protocol exploit: from prompt injection to protocol-level exploits in LLM agent workflows | — |
| 132-1 | **A3** | MCP threat landscape: comprehensive security threat analysis of Model Context Protocol | — |
| 133-1 | **A3** | Third-party plugin injection: prompt injection risks in AI chatbot plugins | — |
| 121-1 | **A4** | Practical poisoning: practical poisoning attacks against RAG in realistic settings | 0.85–0.97 ASR |
| 122-1 | **A4** | DeRAG: black-box adversarial attacks on multiple RAG applications via prompt optimization | — |
| 124-1 | **A4** | NeuroGenPoisoning: neuron-guided attacks on RAG via genetic optimization of external knowledge | — |
| 128-1 | **A4** | RAG-targeted adversarial attack on LLM-based threat detection/mitigation framework | — |
| 108-1 | **A5** | Multimodal PI survey: risks and defenses for modern multimodal LLMs | — |
| 112-1 | **A5** | Visual modality jailbreak: 4 attacks exploiting VLM vision component (symbol sequences, harmful text, etc.) | — |
| 113-1 | **A5** | Typographic visual prompt injection in cross-modality generation models (VLP + I2I) | — |
| 116-1 | **A5** | Visual adversarial examples jailbreak aligned LLMs via image perturbation | — |
| 117-1 | **A5** | Text-to-Image model jailbreak via LLM-generated prompts | — |
| 118-1 | **A5** | Visual contextual attack: image-driven context injection to jailbreak MLLMs | — |
| 135-1 | **A7/A9** | PromptWare: jailbroken GenAI model flips from serving app to attacking it — new attack class | — |
| 136-1 | **A7/A9** | PromptWare via invitation: maliciously engineered prompts manipulate LLM-powered assistants in production | — |
| 142-1 | **A6** | PAIR (20 queries): jailbreaking black-box LLMs in ~20 queries via iterative attack refinement | — |
| 144-1 | **A7** | In-the-wild jailbreak characterization: taxonomy of real jailbreak prompts collected from forums/communities | — |
| 148-1 | **A7** | SequentialBreak: embedding jailbreak prompts into sequential prompt chains | — |
| 149-1 | **A6/A7** | Jailbreak scaling laws: adversarial PI amplifies ASR from polynomial to exponential growth | — |
| 150-1 | **A7** | Wolf in Sheep's Clothing: generalized nested jailbreak prompts — multi-layer nesting | — |
| 153-1 | **A7** | Multilingual jailbreak: non-English languages bypass safety alignment more easily | — |
| 169-1 | **A7** | Stealthy jailbreak via benign data mirroring: camouflages harmful intent behind benign-looking content | — |
| 171-1 | **A7** | Camouflaged jailbreaks: benchmarking disguised attacks that bypass detection | — |
| 173-1 | **A7** | Multilingual jailbreak on closed-source LLMs: cross-language prompt variation | — |
| 177-1 | **A6** | Robust jailbreak prompt generation: one model transfer to all — cross-model transfer | — |
| 178-1 | **A6** | GPTFUZZER: auto-generated jailbreak prompts via genetic fuzzing | top-1/top-5 99/100% |
| 179-1 | **A6** | AutoDAN (stealthy): generating stealthy jailbreak prompts via genetic algorithm | — |
| 180-1 | **A6** | AutoDAN (gradient): interpretable gradient-based adversarial attacks on LLMs | — |
| 182-1 | **A7** | Multi-round jailbreak: iterative multi-turn attack that progressively erodes refusal | — |
| 183-1 | **A6** | ForgeDAN: evolutionary framework for jailbreaking — population-based optimization | 98.46% Gemma-2, 87.12% Qwen |
| 184-1 | **A6** | AutoDAN-Turbo: lifelong agent for strategy self-exploration to jailbreak LLMs — discovers strategies autonomously | — |
| 198-1 | **A6** | MasterKey: automated jailbreaking across multiple LLM chatbots — time-based analysis | — |
| 200-1 | **A6** | Compliance-direction initialization: extract compliance directions from activation space for better attack init | — |
| 129-1 | **A9** | Generative AI in cybersecurity: comprehensive review of LLM vulnerabilities in security applications | — |
| 130-1 | **A9** | Real-world LLM security: security concerns in real-world LLM-based systems | — |

### Defense Sub-types (25 entries)

| Paper | Family | Description | ASR/Result |
|-------|--------|-------------|------------|
| 105-1 | **D2** | PIShield: detecting PI attacks via intrinsic LLM features (attention patterns, hidden states) | — |
| 107-1 | **D2** | Protect: robust guardrailing stack for trustworthy enterprise LLM systems | — |
| 123-1 | **D4** | ControlNet: firewall for RAG-based LLM systems — monitors retrieval flow | AUROC 0.974 |
| 134-1 | **D5** | Jatmo: task-specific fine-tuning as PI defense — narrow model less susceptible to injection | best attacks <0.5% |
| 138-1 | **D5** | Securing LLMs from PI: evaluation of JATMO and other defense approaches | — |
| 139-1 | **D5** | Adaptive defense eval: 20K+ attacks vs 9 defenses — every defense that hides prompts can be broken | — |
| 140-1 | **D5** | Innovative defenses beyond benchmark: novel defense approaches against PI | — |
| 155-1 | **D5** | Few-shot defense: how few-shot demonstrations affect prompt-based jailbreak defenses | — |
| 157-1 | **D5** | Adversarial tuning: defending against jailbreak via adversarial fine-tuning | — |
| 158-1 | **D5** | Short-length adversarial training: short adversarial examples help defend against long jailbreak attacks | — |
| 162-1 | **D6** | GuardNet: graph-attention filtering for jailbreak defense — token-level detection | F1 94.8/98.9% |
| 163-1 | **D6** | Round-trip translation defense: translate to another language and back to neutralize injection | — |
| 165-1 | **D5** | Semantic smoothing: defending LLMs against jailbreak via semantic-level smoothing | — |
| 166-1 | **D5** | LLM self-defense: LLMs can defend themselves against jailbreaking via self-checking | — |
| 167-1 | **D6** | BaThe: defense against jailbreak in MLLMs by treating harmful instruction as backdoor trigger | — |
| 172-1 | **D5** | Multi-level defense: prompt-level, system-level, and training-time taxonomy of jailbreak defenses | — |
| 174-1 | **D5** | In-context adversarial game: defending jailbreak prompts via in-context adversarial training | — |
| 175-1 | **D6** | Causal perspective: causal analysis framework for enhancing both attack and defense | — |
| 176-1 | **D5** | Jailbreak Antidote: runtime safety-utility balance via sparse representation adjustment | — |
| 181-1 | **D2** | Gradient Cuff: detecting jailbreak attacks by exploring refusal loss landscapes | — |
| 192-1 | **D5** | RLHF alignment base: training helpful and harmless assistant with RLHF | — |
| 193-1 | **D5** | Constitutional AI: harmlessness from AI feedback — self-improving alignment | — |
| 199-1 | **D5** | Mitigating many-shot jailbreaking: defense against long-context attacks | — |
| 126-1 | **D4** | Secure RAG: defense framework against RAG poisoning attacks | — |
| 156-1 | **D6** | Red teaming evaluation: systematic evaluation of PI and jailbreak vulnerabilities across LLMs | — |

### Surveys & Benchmarks (12 entries)

| Paper | Type | Description |
|-------|------|-------------|
| 137-1 | **Survey** | SLR on LLM defenses: systematic literature review on PI and jailbreak defenses |
| 141-1 | **Survey** | Survey of attacks on LLMs: comprehensive taxonomy of all LLM attack vectors |
| 146-1 | **Survey** | Jailbreak survey: jailbreak attacks and defenses against LLMs — broad survey |
| 152-1 | **Survey** | Jailbreaking and mitigation survey: vulnerabilities and mitigation strategies |
| 161-1 | **Survey** | Cross-language generalization: do jailbreak/defense methods generalize across languages? |
| 186-1 | **Benchmark** | HarmBench: standardized evaluation framework for automated red teaming |
| 187-1 | **Benchmark** | JailbreakBench: open robustness benchmark — standardized jailbreak evaluation |
| 188-1 | **Benchmark** | StrongREJECT: identifies empty/exaggerated jailbreak claims — evaluation discipline |
| 189-1 | **Benchmark** | XSTest: test suite for exaggerated safety behaviors / over-refusal |
| 190-1 | **Red Team** | Red teaming at scale: methods, scaling behaviors, and lessons learned |
| 191-1 | **Eval** | Model-written evaluations: discovering LM behaviors with automated eval generation |
| 194-1 | **Red Team** | Red teaming LMs with LMs: using language models to red team other language models |

### 🔴 A1. Direct Prompt Injection

Attacker พิมพ์คำสั่งใหม่ใน user prompt โดยตรง

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A1.1 | **Goal Hijacking** | เปลี่ยนจุดประสงค์คำตอบเป็นอย่างอื่น | 58.6% | [3] |
| A1.2 | **Prompt Leaking** | ดึง system prompt ออกมาแสดง | 23.6% | [3] |
| A1.3 | **HOUYI-style App Attack** | โจมตี LLM-integrated apps จริงเพื่อขโมย prompt/ใช้ computation | 86.1% | [1] |
| A1.4 | **Token-efficient Attack** | ใช้ token น้อยเพื่อหยุด LLM reasoning (adaptive token compression) | — | [55] |
| A1.5 | **Simple MCQ Injection** | injection ในคำถามเลือกตอบง่ายๆ ที่ LLM ยังตอบผิด | — | [63] |

### 🔴 A2. Indirect Prompt Injection (IPI)

Payload ซ่อนใน external content ที่ model อ่านภายหลัง

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A2.1 | **Webpage Injection** | ซ่อน instruction ใน HTML/web content | >70% adaptive | [2], [85] |
| A2.2 | **Email Injection** | hidden text ใน email ที่ agent summarize | 100% exfil | [13], [76] |
| A2.3 | **Document/PDF Injection** | metadata, hidden text ใน documents | — | [5] |
| A2.4 | **Calendar/Task Injection** | ฝังใน schedule entries/calendar invites | 94.6% | [59] |
| A2.5 | **Social-web Injection** | posts, comments, reviews ใน social platforms | — | [75], [85] |
| A2.6 | **Tool Output Injection** | ข้อมูลที่ส่งกลับจาก tool/API มี hidden instruction | — | [13], [38] |
| A2.7 | **RAG Chunk Injection** | ฝังใน retrieved passages | 90–97% | [119], [120] |
| A2.8 | **Hidden-in-Plain-Text** | injection ผ่าน social-web data ใน RAG pipeline | — | [75] |
| A2.9 | **Real-world IPI (in the wild)** | empirical study ของ IPI บน production systems | — | [77], [85] |

### 🔴 A3. Agent / Tool / MCP Hijacking

Prompt injection กลายเป็น action injection — ไม่ใช่แค่คำตอบผิด

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A3.1 | **Tool Selection Attack** | หลอกให้ model เลือก tool ผิด | 74–100% | [72] |
| A3.2 | **Tool Argument Manipulation** | แก้ parameter ของ function call | — | [38] |
| A3.3 | **Data Exfiltration via Tool** | ส่งข้อมูลออกผ่าน email/SendMessage tool | 100% | [13], [76] |
| A3.4 | **MCP Protocol Attack** | exploit Model Context Protocol systems | 75.83% peak | [98] |
| A3.5 | **Chat Template Abuse (ChatInject)** | ใช้ chat template injection เพิ่ม ASR | 5% → 45.9% | [86] |
| A3.6 | **Skill/File Injection** | ฝังใน agent skill files | — | [89] |
| A3.7 | **Feedback Loop Hijacking (IterInject)** | ใช้ feedback loop ปรับ injection แบบ iterative | 90.3% | [93] |
| A3.8 | **Context-informed Agent Attack** | ใช้ context awareness เจาะ email assistant | 96.7% | [87] |
| A3.9 | **Tool Metadata Attack (Semantic)** | โจมตีผ่าน tool description/metadata | — | [99] |
| A3.10 | **ObliInjection** | order-oblivious payload ไม่สนตำแหน่งใน context | 98.7–99.6% | [74] |
| A3.11 | **Privacy Leakage via Agent** | ดึง personal data ที่ agent เห็นระหว่างทำงาน | — | [76] |
| A3.12 | **Commercial Agent Attack** | โจมตี commercial agents จริง (GPT Store, etc.) | — | [46] |

### 🔴 A4. RAG / Retrieval / Memory Poisoning

ทำให้เอกสารพิษถูก retrieve หรือฝังใน memory/knowledge base

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A4.1 | **Corpus Poisoning (PoisonedRAG)** | ใส่เอกสารพิษจำนวนน้อยใน knowledge base ขนาดใหญ่ | 90–97% (5 texts) | [119] |
| A4.2 | **Retriever Manipulation (BadRAG)** | adversarial passages ที่ทำให้ retriever เลือกผิด | 98.2% (0.04% corpus) | [120] |
| A4.3 | **Backdoored Retriever** | ฝัง trigger ใน retrieval model เอง | — | [29] |
| A4.4 | **HijackRAG** | hijacking attacks ต่อ RAG systems | — | [34] |
| A4.5 | **CorruptRAG** | single poisoned text per query | 0.85–0.97 | [121] |
| A4.6 | **Multimodal RAG Poisoning (Poisoned-MRAG)** | image-text pairs ที่เป็นพิษ | 98% (5 pairs) | [125] |
| A4.7 | **Memory Poisoning (MemoryGraft)** | poisoned experiences ค้างข้าม session | PRP ~50% | [127] |
| A4.8 | **Selective Disclosure Attack** | หลอก RAG เปิดเผยข้อมูลที่ควรซ่อน | — | [73] |
| A4.9 | **RAG App Framework Manipulation** | end-to-end manipulation ใน LLM app frameworks | — | [19] |

### 🔴 A5. Multimodal / GUI / Audio Injection

Payload อยู่ในรูปภาพ, typography, screenshot, mobile UI, audio — ไม่ใช่ text ล้วน

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A5.1 | **Visual Prompt Injection (FigStep)** | typographic text ในรูปภาพที่ model อ่าน | 82.5% avg | [114] |
| A5.2 | **Adversarial Image Perturbation** | แก้ pixel ควบคุม generative model output | 90–100% | [115] |
| A5.3 | **Image Hijacks** | adversarial images ควบคุม model runtime | 100% string hijack | [115] |
| A5.4 | **CrossMPI Image-only Injection** | image-only perturbation ที่ transfer ข้าม models | 66.36% avg | [110] |
| A5.5 | **Adversarial PI on MLLMs** | โจมตี multimodal LLMs รุ่นใหญ่ (GPT-4o, Gemini) | 81% GPT-4o | [111] |
| A5.6 | **GUI/Screenshot Injection (EVA)** | popup/UI text หลอก GUI agent | >80% | [102] |
| A5.7 | **Mobile Environment Injection (AEIA-MN)** | environmental injection บนมือถือ | 93% | [103] |
| A5.8 | **Audio Prompt Injection** | ซ่อน instruction ในเสียง | 98.11% peak | [197] |
| A5.9 | **Visual Goal Hijacking** | visual prompt injection บน LVLMs | — | [21] |

### 🔴 A6. Automated / Optimization-based Attacks

ใช้ fuzzing, RL, gradient, evolutionary search เพื่อค้นหา trigger ที่ ASR สูง

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A6.1 | **GCG / Universal Adversarial Suffix** | gradient-based optimization หา suffix | 100% Vicuna, 84% GPT transfer | [185] |
| A6.2 | **Fuzzing (PROMPTFUZZ)** | genetic search/fuzzing หา injection prompts | 75.33% | [18] |
| A6.3 | **RL-based Attack (PISmith)** | reinforcement learning สร้าง injection | ASR@10=100% | [101] |
| A6.4 | **Tree-search (TAP)** | tree-of-attacks ที่ query-efficient | 94% GPT-4o | [143] |
| A6.5 | **Best-of-N Sampling** | ลองหลายครั้งเลือกอันทะลุ | 98.11% audio | [197] |
| A6.6 | **Fine-tuning API Abuse** | ใช้ fine-tune API หา trigger ใน closed models | 82% | [42] |
| A6.7 | **Neural Exec** | เรียนรู้ execution triggers แบบ neural | — | [15] |
| A6.8 | **ForgeDAN** | evolutionary jailbreak generation | 98.46% Gemma-2 | [183] |
| A6.9 | **Universal Prompt Injection** | trigger ที่ transfer ข้าม objectives | >80% | [9] |
| A6.10 | **Goal-guided Generative Attack** | generative search หา injection | 44.87% | [10] |
| A6.11 | **Adaptive Attack (Breaks Defenses)** | adaptive attack ที่รู้ defense และ break ได้ | 100% | [48], [147] |
| A6.12 | **LLM-as-Judge Attack (JudgeDeceiver)** | optimization-based injection หลอก LLM judge | 89–99% | [14] |
| A6.13 | **Automated RL Injection** | RL-based automated prompt injection | — | [88] |
| A6.14 | **Segregated/Distributed Prompt** | แบ่งคำขออันตรายเป็นชิ้นเล็กๆ | — | [51] |

### 🔴 A7. Jailbreak / Safety Filter Bypass

ข้าม refusal/safety alignment ด้วยเทคนิคต่างๆ

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A7.1 | **Role-play / Character (DAN)** | สวมบทบาทเป็น character ที่ไม่มีข้อจำกัด | — | [135], [136] |
| A7.2 | **Multi-turn Jailbreak** | ค่อยๆ ขยับ boundary หลายรอบสนทนา | — | [142] |
| A7.3 | **Many-shot Jailbreak** | ยัดตัวอย่างเยอะๆ ใน context window | 31% Claude | [195] |
| A7.4 | **Stylistic / Poetry Framing** | ใช้บทกวี/สำนวน bypass safety | 62% avg, Gemini 90–100% | [196] |
| A7.5 | **Nested Prompt** | ซ้อน prompt หลายชั้น | — | [148] |
| A7.6 | **Simple Adaptive Random Search** | adaptive search ทะลุทุก safety-aligned LLM | 100% | [147] |

### 🔴 A8. Encoding / Obfuscation

| # | Sub-type | คำอธิบาย | Refs |
|---|----------|-----------|------|
| A8.1 | **Base64/Cipher Encoding** | เข้ารหัส instruction ให้ model decode เอง | — |
| A8.2 | **Emoji/Unicode Attack** | ใช้ตัวอักษรพิเศษแทนคำ | — |
| A8.3 | **Homoglyph Substitution** | ตัวอักษรที่ดูเหมือนกันแต่ codepoint ต่าง | — |
| A8.4 | **Language Mixing** | ผสมภาษา bypass English-centric filter | — |

### 🔴 A9. Multi-agent / Supply Chain / System-level

| # | Sub-type | คำอธิบาย | Peak ASR | Refs |
|---|----------|-----------|----------|------|
| A9.1 | **Agent-to-Agent Infection** | Prompt Infection ใน multi-agent systems | — | [26] |
| A9.2 | **Persuasion Propagation** | แพร่ persuasion ข้าม agents | — | [90] |
| A9.3 | **Cross-agent Context Bleeding** | ข้อมูลรั่วข้าม agent sessions | — | — |
| A9.4 | **Alignment Poisoning** | ฝังฝั่งใน DPO/RLHF data | +0.33 attack success | [28] |
| A9.5 | **Backdoor in Pre-trained Weights** | ซื้อ model มาพร้อมช่องโหว่ | — | — |
| A9.6 | **Peer Review / Scientific Review Attack** | โจมตีระบบ peer review ที่ใช้ LLM | — | [65], [66] |
| A9.7 | **Machine Translation Attack** | injection ใน MT pipeline | — | [16] |
| A9.8 | **Robotics Attack** | injection ต่อ LLM-integrated robotic systems | — | [20] |
| A9.9 | **Medical AI Attack** | injection ใน medical LLM applications | — | [84] |

---

## Defense Taxonomy

### 🟢 D1. Instruction/Data Separation

แยก data กับ instruction ให้ชัด — ทำให้ model ไม่ตีความ untrusted data เป็น instruction

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D1.1 | **Structured Queries (StruQ)** | แยก structure ของ query | undefended 96% → 0% | [6] |
| D1.2 | **Spotlighting** | delimiting/datamarking/encoding boundary | ASR >50% → <2% | [11] |
| D1.3 | **Signed Prompt** | authentication ด้วย signature | — | [7] |
| D1.4 | **Instruction Hierarchy** | สอน model ให้ prioritize privileged instructions | — | [12] |
| D1.5 | **Instruction Referencing** | refer กลับไป executed instruction เพื่อ validate | — | [54] |
| D1.6 | **InstructDetector** | ตรวจจับ instruction ใน data | ASR 0.03% | [58] |
| D1.7 | **Polymorphic Prompt** | เปลี่ยนรูปแบบ prompt ทุกครั้ง | — | [78] |
| D1.8 | **Intent Alignment** | จับความไม่ตรงกันของ instruction intent | — | [100] |

### 🟢 D2. Detection / Classifier / Guardrail

ใช้ model/classifier/embedding/attention เพื่อจับ malicious content

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D2.1 | **MBERT/Logistic Classifier** | embedding-based classification | 96.55% accuracy | [22] |
| D2.2 | **GenTel-Shield** | unified benchmark + shielding | 96.81% accuracy, F1 96.74 | [23] |
| D2.3 | **Embedding-based Classifier** | lightweight embedding detection | — | [32] |
| D2.4 | **Attention Tracker** | attention pattern analysis | — | [37] |
| D2.5 | **JailGuard** | universal text+image detector | 86.14% text, 82.90% image | [145] |
| D2.6 | **PromptShield** | deployable production detection | — | [41] |
| D2.7 | **Game-theoretic Detection (DataSentinel)** | game theory approach | — | [53] |
| D2.8 | **Explainable Detection** | detection + generative explanation | — | [45] |
| D2.9 | **Recursive Procedural Detection (RLM-JB)** | recursive detection สำหรับ tool-augmented agents | F1 98.49% | [106] |
| D2.10 | **GuardNet** | graph-attention token-level detection | F1 94.8/98.9% | [162] |

### 🟢 D3. Authentication / Authorization / Privilege Control

ตรวจว่า instruction มาจากใคร — ไม่ใช่แค่ว่าพูดอะไร

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D3.1 | **Signed-Prompt Authentication** | signature-based prompt verification | — | [7] |
| D3.2 | **FATH Test-time Auth** | authentication-based defense ที่ inference time | 0% ASR | [31] |
| D3.3 | **Programmable Privilege Control (Progent)** | policy กำหนดสิทธิ์ tool/action | 39.9% → 1.0% | [52] |
| D3.4 | **Encrypted Prompt** | authorization defense ผ่าน encryption | — | [50] |
| D3.5 | **Tool-dependency Graph (IPIGuard)** | graph-based tool dependency check | — | [64] |
| D3.6 | **Surgical Precision Defense** | precision-targeted injection defense | — | [97] |

### 🟢 D4. Secure Architecture / IFC / Sandboxing

เปลี่ยน architecture ให้ untrusted content ควบคุม trusted action ไม่ได้

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D4.1 | **Information Flow Control (IFC)** | system-level flow control | 0% ASR all models | [24] |
| D4.2 | **CaMeL (Defeating by Design)** | แยก data path กับ action path, policy enforcement นอก model | — | [49] |
| D4.3 | **Tool Output Firewall / Sanitizer** | filter tool output ก่อนเข้า model | 0% ASR, recall 99.53% | [68] |
| D4.4 | **Provenance Graph (ARGUS)** | trace ที่มาของข้อมูลใน agent | 3.8% ASR | [83] |
| D4.5 | **Task Shield** | enforce task alignment ป้องกัน injection | 2.23% ASR | [39] |
| D4.6 | **Selective Disclosure (SD-RAG)** | ควบคุมข้อมูลที่ RAG เปิดเผย | — | [73] |
| D4.7 | **Dynamic Rule-based Defense (DRIFT)** | dynamic rules + injection isolation | 4.8% ASR | [96] |
| D4.8 | **Design Patterns for Secure Agents** | architectural patterns สำหรับ secure agents | — | [81] |
| D4.9 | **CleanBase** | malicious document detection ใน RAG | — | [79] |
| D4.10 | **Secure RAG Chatbot Design** | applied secure RAG architecture | — | [80] |

### 🟢 D5. Training / Alignment Defenses

Fine-tuning, DPO, adversarial training เพื่อเพิ่ม baseline robustness

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D5.1 | **SecAlign / DPO** | preference optimization ต่อ prompt injection | Max ASR 0–2% | [25] |
| D5.2 | **Meta SecAlign-70B** | secure foundation model | 1.9% AgentDojo, 0% WASP | [60] |
| D5.3 | **Jatmo (Task-specific Fine-tuning)** | สร้าง task-specific model ที่แข็งแกร่ง | best attacks <0.5% | [134] |
| D5.4 | **SmoothLLM** | randomized smoothing กับ perturbation | ASR ~0.9–1.6% | [151] |
| D5.5 | **CCFC (Dual-track Protection)** | confusion + calibration defense | 0% GCG/AutoDAN | [154] |
| D5.6 | **Defensive Prompt Patch** | prompt patch ที่ robust กว่า baseline | avg ASR 3.80% | [159] |
| D5.7 | **SecurityLingua** | prompt compression ลด attack surface | avg jailbreak 1% | [160] |
| D5.8 | **JBShield (Activation Defense)** | activation-based detection + defense | ASR 61% → 2% | [164] |
| D5.9 | **HSF (Hidden-state Filtering)** | filter hidden states ที่เกี่ยวกับ injection | 0–8% ASR | [168] |
| D5.10 | **SelfDefend** | self-checking defense | ASR 65.7% → 0.236 | [170] |

### 🟢 D6. Runtime Verification / Re-execution / Causal Attribution

ตรวจสอบขณะ runtime — rerun, causal trace, context purification

| # | Sub-type | คำอธิบาย | Best Result | Refs |
|---|----------|-----------|-------------|------|
| D6.1 | **MELON (Masked Re-execution)** | mask แล้ว rerun เปรียบเทียบ | 0.24% ASR GPT-4o | [43] |
| D6.2 | **CachePrune** | neural attribution defense | — | [56] |
| D6.3 | **AttriGuard (Causal Attribution)** | causal attribution ของ tool invocations | 0% static ASR | [91] |
| D6.4 | **AgentSentry (Temporal Causal)** | temporal causal diagnostics + context purification | 0% ASR | [94] |
| D6.5 | **Multi-agent Defense Pipeline** | ใช้หลาย agent ตรวจจับร่วมกัน | — | [67] |
| D6.6 | **PromptArmor** | prompt removal + guardrail | 55% → 0% | [92] |
| D6.7 | **RTBAS** | defense ต่อ PI + privacy leakage | — | [44] |
| D6.8 | **Tool Result Parsing** | parse tool results ตรวจ injection | — | [95] |

---

## Risk Ranking

### Attack Risk (สูงสุด → ต่ำสุด)

| Rank | Attack Family | เหตุผล |
|------|---------------|--------|
| 1 | **RAG/Memory Poisoning** | เอกสารพิษจำนวนน้อยให้ ASR สูง และ persistent ข้าม session |
| 2 | **Agent/Tool/MCP Hijacking** | ทำให้เกิด external action/data exfiltration ไม่ใช่แค่คำตอบผิด |
| 3 | **Automated Adaptive Jailbreak** | adaptive search/RL/fuzzing ทำให้ static defenses พัง |
| 4 | **Multimodal/GUI/Audio Injection** | text-only guardrail มองไม่เห็น payload |
| 5 | **Long-context/Stylistic Jailbreak** | model safety พึ่ง pattern มากเกินไป |
| 6 | **Direct Prompt Injection** | พื้นฐานแต่ยังใช้ได้ — ผลกระทบสูงสุดเมื่อรวม tool/RAG |

### Defense Effectiveness (สูงสุด → ต่ำสุด)

| Rank | Defense Strategy | เหตุผล |
|------|------------------|--------|
| 1 | **System-level Controls + IFC/Sandboxing** | ไม่ฝาก security ไว้ที่ model อย่างเดียว |
| 2 | **Structured Separation + Authentication** | ลด ASR มากแต่ต้องกัน adaptive bypass |
| 3 | **Runtime Verification / Causal Attribution** | จับ inconsistency ได้ดี โดยเฉพาะ agents |
| 4 | **Detection/Guardrail (เป็น layer หนึ่ง)** | accuracy สูงแต่มี over-refusal + adaptive evasion |
| 5 | **Training/Alignment** | ช่วยลด baseline ASR แต่ adaptive attacks เจาะได้ |
| 6 | **Prompt-only Reminders** | ง่ายแต่เปราะ — มักถูก counterattack |

---

## Practical Recommendation

Production systems ควรใช้ **defense-in-depth**:

1. **Typed instruction/data separation** — แยกชัดว่าอะไรคือ instruction อะไรคือ data
2. **Tool-output sanitizer** — filter ทุก output จาก external tool
3. **Explicit privilege policy** — กำหนดสิทธิ์ action ชัดเจน
4. **Provenance/causal check** — ตรวจที่มาก่อน execute action
5. **Detector/classifier** — จับ known bad patterns
6. **Evaluation suite** — ทดสอบด้วย adaptive attacks + วัด over-refusal

> **ไม่มี paper ไหนสนับสนุนใช้ prompt-only reminders เป็น defense หลัก**

---

*Synthesis จาก 200 papers: 80 red team (attack) + 120 blue team (defense), 16.6M characters evidence, 2022–2026*
