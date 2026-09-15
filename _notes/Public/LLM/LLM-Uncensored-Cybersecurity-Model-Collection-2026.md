---
title: "LLM Uncensored, Fable & Cybersecurity Model Collection 2026"
notetype: feed
date: 2026-06-25
last_modified: 2026-09-16
tags: [LLM, uncensored, cybersecurity, fable, heretic, abliterated, GGUF, quantized, local-llm]
status: published
---

# LLM Uncensored, Fable & Cybersecurity Model Collection

> รวบรวม repository บน GitHub และโมเดลบน Hugging Face ที่เกี่ยวข้องกับ Prompt Injection, Uncensored LLM (Heretic/Abliterated), โมเดลที่ fine-tune ด้วย Fable และโมเดลด้าน Cybersecurity พร้อมระบุว่ารุ่นใดรันได้บน GPU 12GB

---

## 📊 ตารางเปรียบเทียบรวมทุกหมวด

### GitHub Repos (Prompt Injection & Leaked Prompts)

| # | Repo | ⭐ Stars | ประเภท | จำนวนไฟล์ | ลิงก์ |
|---|------|---------|--------|----------|-------|
| 1 | x1xhlol/system-prompts-and-models-of-ai-tools | 141,142 | Leaked System Prompts | 36 | [→](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) |
| 2 | asgeirtj/system_prompts_leaks | 45,965 | Leaked System Prompts | 16 | [→](https://github.com/asgeirtj/system_prompts_leaks) |
| 3 | elder-plinius/CL4R1T4S | 43,834 | Leaked System Prompts | 27 | [→](https://github.com/elder-plinius/CL4R1T4S) |
| 4 | yunwei37/prompt-hacker-collections | 333 | Prompt Attack/Defense | 9 | [→](https://github.com/yunwei37/prompt-hacker-collections) |
| 5 | SkullSplitter2020/Awesome-GTP-Super-Prompting | 3 | Jailbreak + Injection | README (large) | [→](https://github.com/SkullSplitter2020/Awesome-GTP-Super-Prompting) |
| 6 | gmh5225/LLM-Attack-Prompt | 6 | Jailbreak + Injection | 37 files | [→](https://github.com/gmh5225/LLM-Attack-Prompt) |
| 7 | SecNode/AISecLists | 15 | AI Red Teaming | 3 | [→](https://github.com/SecNode/AISecLists) |

### HuggingFace Models — Uncensored + Quantized (12GB GPU)

| # | Model | Base | Uncensor | Q4 Size | ใช้กับ GPU 12GB | ลิงก์ |
|---|-------|------|----------|---------|--------|-------|
| 1 | Qwen3.6-12B-IQ-Ultra-Heretic | Qwen 3.6 12B | ✅ Heretic | 6.98 GB | ✅ | [→](https://huggingface.co/KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF) |
| 2 | Qwen3.5-9B Claude 4.6 Heretic NEOCODE | Qwen 3.5 9B | ✅ Heretic | 6.52 GB | ✅ | [→](https://huggingface.co/DavidAU/Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING-MAX-NEOCODE-Imatrix-GGUF) |
| 3 | Gemma-3-12B Ultra Uncensored Heretic | Gemma 3 12B | ✅ Heretic | 6.25 GB | ✅ | [→](https://huggingface.co/llmfan46/gemma-3-12b-it-ultra-uncensored-heretic-GGUF) |
| 4 | Gemma-3-12B GLM-4.7 Cross Heretic | Gemma 3 12B | ✅ Heretic | 6-8 GB | ✅ | [→](https://huggingface.co/mradermacher/gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking-i1-GGUF) |
| 5 | Qwen3.5-9B Claude Opus Uncensored Distilled | Qwen 3.5 9B | ✅ Distilled | 5.37 GB | ✅ | [→](https://huggingface.co/LuffyTheFox/Qwen3.5-9B-Claude-4.6-Opus-Uncensored-Distilled-GGUF) |

### HuggingFace Models — Fable + Uncensored

| # | Model | Base | Fable | Uncensor | Q4 Size | ใช้กับ GPU 12GB | ลิงก์ |
|---|-------|------|-------|----------|---------|--------|-------|
| 1 | Gemma-4-12B Fable5 Composer Uncensored Heretic | Gemma 4 12B | ✅ | ✅ Heretic | 7.0 GB | ✅ | [→](https://huggingface.co/llmfan46/gemma-4-12B-coder-fable5-composer2.5-v1-uncensored-heretic-GGUF) |
| 2 | Qwable-9B Claude Fable-5 Heretic | Qwen 3.5 9B | ✅ | ✅ Heretic | 5.4 GB | ✅ | [→](https://huggingface.co/mradermacher/Qwable-9B-Claude-Fable-5-heretic-GGUF) |
| 3 | Gemma-4-12B Fable5 Composer Abliterated | Gemma 4 12B | ✅ | ✅ Abliterated | 7.0 GB | ✅ | [→](https://huggingface.co/KakTakOne/Huihui-gemma-4-12B-coder-fable5-composer2.5-v1-abliterated-GGUF) |
| 4 | Qwen3.6-14B-A3B FableVibes | Qwen 3.6 14B MoE | ✅ | ❌ | 8.1 GB | ✅ | [→](https://huggingface.co/tvall43/Qwen3.6-14B-A3B-FableVibes-GGUF) |
| 5 | Qwen3.5-9B Fable-5 v1 | Qwen 3.5 9B | ✅ | ❌ | 5.4 GB | ✅ | [→](https://huggingface.co/TeichAI/Qwen3.5-9B-Fable-5-v1-GGUF) |
| 6 | Qwen3.6-27B Fable-5 Experimental | Qwen 3.6 27B | ✅ | ❌ | ~16 GB | ❌ | [→](https://huggingface.co/TeichAI/Qwen3.6-27B-Fable-5-Experimental-GGUF) |
| 7 | Qwen3.5-9B Fable-5 SDFT (Self-Distill) | Qwen 3.5 9B | ✅ | ❌ | 5.4 GB | ✅ | [→](https://huggingface.co/armand0e/Qwen3.5-9B-Fable-5-SDFT-GGUF) |

### HuggingFace Models — Cybersecurity + Uncensored

| # | Model | Base | Cyber | Uncensor | Q4 Size | ใช้กับ GPU 12GB | ลิงก์ |
|---|-------|------|-------|----------|---------|--------|-------|
| 1 | Josiefied Qwen3-8B Security Abliterated | Qwen3 8B | ✅ | ✅ Abliterated | 4.8 GB | ✅ | [→](https://huggingface.co/mradermacher/Josiefied-Qwen3-8B-security-abliterated-v1-i1-GGUF) |
| 2 | Qwen3-4B Cybersecurity Heretic | Qwen3 4B | ✅ | ✅ Heretic | 2.4 GB | ✅ | [→](https://huggingface.co/DexopT/Qwen3-4B-Cybersecurity-Heretic-16bit) |
| 3 | WRN 2.5 Qwen 2.5 Coder Obliterated | Qwen 2.5 7B | ✅ | ✅ Abliterated | 4.5 GB | ✅ | [→](https://huggingface.co/mradermacher/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-OBLITERATED-i1-GGUF) |
| 4 | WRN 2.5 Qwen 2.5 Coder (censored) | Qwen 2.5 7B | ✅ | ❌ | 4.5 GB | ✅ | [→](https://huggingface.co/bartowski/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-GGUF) |
| 5 | WRN V3 7B | 7B | ✅ | ❌ | 4.5 GB | ✅ | [→](https://huggingface.co/bartowski/WhiteRabbitNeo_WhiteRabbitNeo-V3-7B-GGUF) |
| 6 | WRN Llama 3.1 8B | Llama 3.1 8B | ✅ | ❌ | 4.7 GB | ✅ | [→](https://huggingface.co/bartowski/Llama-3.1-WhiteRabbitNeo-2-8B-GGUF) |
| 7 | WRN 13B | Llama 2 13B | ✅ | ❌ | 7.5 GB | ✅ | [→](https://huggingface.co/TheBloke/WhiteRabbitNeo-13B-GGUF) |
| 8 | RavenX CyberAgent v5.1 | Qwen 3.6 35B MoE | ✅ | ✅ Abliterated | 20.2 GB | ❌ | [→](https://huggingface.co/deadbydawn101/RavenX-CyberAgent-Qwen3.6-35B-A3B-Opus-4.7-OpenMythos-Pentester-BugHunter-RATH-GGUF) |
| 9 | RavenX CyberAgent v6.2 Experimental | Qwen 3.6 35B MoE | ✅ | ✅ Abliterated | 20.2 GB | ❌ | [→](https://huggingface.co/deadbydawn101/RavenX-CyberAgent-v6.2-Experimental-GGUF) |
| 10 | GPT-OSS Cybersecurity 20B Heretic | GPT-OSS 20B MoE | ✅ | ✅ Heretic | 15.1 GB | ❌ | [→](https://huggingface.co/mradermacher/GPT-OSS-Cybersecurity-20B-Merged-heretic-i1-GGUF) |
| 11 | GPT-OSS Cybersecurity 20B Abliterated | GPT-OSS 20B MoE | ✅ | ✅ Abliterated | 15.1 GB | ❌ | [→](https://huggingface.co/mradermacher/GPT-OSS-Cybersecurity-20B-Merged-advanced-abliterated-GGUF) |
| 12 | GPT-OSS Cybersecurity 20B (censored) | GPT-OSS 20B MoE | ✅ | ❌ | 13.3 GB | ❌ | [→](https://huggingface.co/mradermacher/GPT-OSS-Cybersecurity-20B-Merged-i1-GGUF) |

---

## 🔓 Heretic vs Abliterated — ความต่าง

| | Heretic | Abliterated |
|---|---------|-------------|
| **วิธี** | เครื่องมือทำ directional ablation พร้อมค้นหาพารามิเตอร์ที่เหมาะสมโดยอัตโนมัติ | โมเดลที่ผ่านการปรับ weights ด้วย directional ablation |
| **เทรนเพิ่ม?** | กระบวนการของ Heretic ไม่ต้องใช้ post-training ที่มีต้นทุนสูง | ต้องอ่านขั้นตอนของแต่ละ checkpoint ว่ามีการฝึกอื่นร่วมด้วยหรือไม่ |
| **เปลี่ยน personality?** | พฤติกรรมอาจเปลี่ยน ต้องทดสอบกับโมเดลจริง | พฤติกรรมอาจเปลี่ยน ต้องทดสอบกับโมเดลจริง |
| **Uncensor สมบูรณ์?** | ยังอาจปฏิเสธบางคำขอ | ไม่ได้รับประกันว่าจะตอบทุกคำขอ |
| **ความรู้เดิม?** | พยายามลดความต่างจากโมเดลเดิม แต่ยังต้องประเมิน | ไม่ได้รับประกันว่าจะรักษาความสามารถเดิมทั้งหมด |
| **Benchmark?** | ต้องวัดหลังปรับโมเดล | ต้องวัดหลังปรับโมเดล |

> **Heretic** เป็นเครื่องมือทำ **abliteration แบบอัตโนมัติ** โดยค้นหาพารามิเตอร์เพื่อลดทั้งจำนวนคำขอที่โมเดลปฏิเสธและความต่างของการแจกแจงผลลัพธ์จากโมเดลเดิม (KL divergence) ส่วน **abliterated** อธิบายโมเดลที่ผ่านวิธีนี้ ชื่อทั้งสองจึงไม่ได้หมายถึงวิธีที่แยกขาดจากกัน และไม่ได้รับประกันว่าจะลบการปฏิเสธทั้งหมดหรือรักษาคะแนน benchmark เดิมไว้ได้ ดู [README ของ Heretic](https://github.com/p-e-w/heretic)

---

## 📚 GitHub Repos — Prompt Injection & Leaked Prompts

### 1. x1xhlol/system-prompts-and-models-of-ai-tools ⭐141,142
- **ขนาด:** มีรายการมากที่สุดในกลุ่มนี้
- **เนื้อหา:** System prompts ที่หลุดออกมาจาก Augment Code, Claude Code, Cursor, Devin, Manus, Notion AI ฯลฯ
- **ปริมาณ:** 36 รายการในไดเรกทอรีหลัก
- [→ GitHub](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)

### 2. asgeirtj/system_prompts_leaks ⭐45,965
- **เนื้อหา:** Claude Fable 5, Opus 4.8, Claude Code, ChatGPT 5.5, Claude Design
- **ปริมาณ:** 16 รายการ
- [→ GitHub](https://github.com/asgeirtj/system_prompts_leaks)

### 3. elder-plinius/CL4R1T4S ⭐43,834
- **เนื้อหา:** System prompts ที่หลุดออกมาจาก ChatGPT, Claude, Gemini, Grok, Perplexity, Cursor, Lovable, Replit
- **ปริมาณ:** 27 รายการในไดเรกทอรีหลักและโฟลเดอร์ย่อย
- [→ GitHub](https://github.com/elder-plinius/CL4R1T4S)

### 4. yunwei37/prompt-hacker-collections ⭐333
- **เนื้อหา:** การโจมตีและป้องกันผ่าน prompt พร้อมบันทึกและตัวอย่างการทำ reverse engineering
- **ปริมาณ:** 9 รายการ พร้อมคำอธิบายภาษาจีนและอังกฤษ
- [→ GitHub](https://github.com/yunwei37/prompt-hacker-collections)

### 5. SkullSplitter2020/Awesome-GTP-Super-Prompting ⭐3
- **เนื้อหา:** ChatGPT Jailbreaks, GPT Assistants Prompt Leaks, Prompt Injection, Super Prompts
- **ปริมาณ:** README ขนาดใหญ่ที่รวบรวมรายการทั้งหมดไว้ในไฟล์เดียว (awesome list)
- [→ GitHub](https://github.com/SkullSplitter2020/Awesome-GTP-Super-Prompting)

### 6. gmh5225/LLM-Attack-Prompt ⭐6
- **เนื้อหา:** แบ่งเป็น 3 หมวด: jailbreaks (25 ไฟล์), prompt_injection (4 ไฟล์), system_prompt (8 ไฟล์)
- **ปริมาณ:** รวม 37 ไฟล์
- [→ GitHub](https://github.com/gmh5225/LLM-Attack-Prompt)

### 7. SecNode/AISecLists ⭐15
- **เนื้อหา:** AI Red Teaming Arsenal — รายการ prompt ที่คัดไว้สำหรับประเมินความปลอดภัย
- **ปริมาณ:** 3 รายการ
- [→ GitHub](https://github.com/SecNode/AISecLists)

---

## 🎭 HuggingFace Models — Fable + Uncensored

### Top Pick: Gemma-4-12B Fable5 Composer Uncensored Heretic
- **Base:** Gemma 4 12B → Fable 5 + Composer 2.5 + Heretic Uncensored
- **Tags:** `uncensored`, `abliterated`, `heretic`, `coding`, `reasoning`, `thinking`
- **Q4_K_M:** 7.0 GB | **Q5_K_M:** 8.1 GB
- [→ HF](https://huggingface.co/llmfan46/gemma-4-12B-coder-fable5-composer2.5-v1-uncensored-heretic-GGUF)

### Qwable-9B Claude Fable-5 Heretic
- **Base:** Qwen 3.5 9B → Fable 5 + Heretic Uncensored ("Qwable" = Qwen + Fable)
- **Q4_K_M:** 5.4 GB | **Q6_K:** 7.0 GB | **Q8_0:** 9.1 GB
- [→ HF](https://huggingface.co/mradermacher/Qwable-9B-Claude-Fable-5-heretic-GGUF)

### Qwen3.6-14B-A3B FableVibes
- **Base:** Qwen 3.6 14B MoE (A3B = Active 3B) → Fable 5 reasoning traces
- **Q4_K_M:** 8.1 GB (GPU 12GB ต้องเผื่อพื้นที่ให้ KV cache และ runtime ด้วย ส่วน active 3B หมายถึงพารามิเตอร์ที่ใช้คำนวณต่อ token ไม่ใช่ขนาด weights ทั้งหมดที่ต้องเก็บในหน่วยความจำ)
- [→ HF](https://huggingface.co/tvall43/Qwen3.6-14B-A3B-FableVibes-GGUF)

### Qwen3.5-9B Fable-5 v1
- **Base:** Qwen 3.5 9B → Fable 5 distill (dataset: `armand0e/claude-fable-5-claude-code`)
- **Benchmark:** ARC +7%, ARC-Easy +9% เมื่อเทียบกับโมเดลตั้งต้น
- **Q4_K_M:** 5.4 GB | **Q8_0:** 9.1 GB
- [→ HF](https://huggingface.co/TeichAI/Qwen3.5-9B-Fable-5-v1-GGUF)

---

## 🛡️ HuggingFace Models — Cybersecurity

### สำหรับ GPU 12GB (แนะนำ)

**Josiefied Qwen3-8B Security Abliterated** — สมดุลที่สุด
- Base: Qwen3 8B → Security finetune → Abliterated
- Q4_K_M: 4.8 GB | Q6_K: 6.4 GB
- [→ HF](https://huggingface.co/mradermacher/Josiefied-Qwen3-8B-security-abliterated-v1-i1-GGUF)

**Qwen3-4B Cybersecurity Heretic** — โมเดลขนาดเล็กที่สุด
- Base: Qwen3 4B → Cybersecurity → Heretic abliteration
- Datasets: `DexopT/cyber_heretic`, offensive security, pentest
- Refusal pass rate: 76% (38/50)
- Q4_K_M: 2.4 GB
- [→ HF](https://huggingface.co/DexopT/Qwen3-4B-Cybersecurity-Heretic-16bit)

**WRN 2.5 Qwen 2.5 Coder Obliterated** — มีความรู้ด้าน Cybersecurity มากที่สุด
- Base: Qwen 2.5 Coder 7B → Cybersecurity → Obliterated (Abliterated)
- Q4_K_M: 4.5 GB | Q8_0: 7.7 GB
- [→ HF](https://huggingface.co/mradermacher/WhiteRabbitNeo-2.5-Qwen-2.5-Coder-7B-OBLITERATED-i1-GGUF)

### สำหรับ GPU 24GB+ (ใหญ่เกิน 12GB)

**RavenX CyberAgent v6.2** — สมบูรณ์ที่สุด
- Base: Qwen3.6-35B-A3B (Abliterated by huihui-ai) → Pentester/BugHunter
- Q4_K_M: 20.2 GB
- Benchmark: Code 97.9%, Security/RATH 70.8%, Overall 80.9%
- [→ HF](https://huggingface.co/deadbydawn101/RavenX-CyberAgent-v6.2-Experimental-GGUF)

**GPT-OSS Cybersecurity 20B Heretic**
- Base: GPT-OSS 20B MoE → Cybersecurity → Heretic
- Datasets: Trendyol Cybersecurity, Fenrir v2.0, Primus-Instruct
- Q4_K_M: 15.1 GB
- [→ HF](https://huggingface.co/mradermacher/GPT-OSS-Cybersecurity-20B-Merged-heretic-i1-GGUF)

---

## 📌 คำแนะนำ

| การใช้งาน | โมเดลที่แนะนำ | Quant |
|----------|------------|-------|
| Uncensored ทั่วไป | Qwen3.6-12B-IQ-Ultra-Heretic | Q4_K_M (7 GB) |
| Coding + Fable + Uncensored | Gemma-4-12B Fable5 Heretic | Q4_K_M (7 GB) |
| เบาสุด + Fable | Qwable-9B Fable-5 Heretic | Q4_K_M (5.4 GB) |
| Cybersecurity (12GB) | Josiefied Qwen3-8B Security Abliterated | Q6_K (6.4 GB) |
| Cybersecurity (เบาสุด) | Qwen3-4B Cyber Heretic | Q4_K_M (2.4 GB) |
| Cybersecurity (ความรู้แน่น) | WRN 2.5 Qwen 2.5 Obliterated | Q8_0 (7.7 GB) |
| Cybersecurity (24GB+) | RavenX CyberAgent v6.2 | Q4_K_M (20.2 GB) |

---

*Updated: 25 June 2026*
