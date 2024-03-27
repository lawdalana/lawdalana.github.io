---
title : 
notetype : [Edx] Large Language Models: Application through Production (Module: 3)
date : 16-03-2022
---

# Module 3: Multi-stage Reasoning

## 1. Prompt Engineering
### Note
- Prompt เป็นส่วนสำคัญของ LLM ที่จะช่วยให้ได้คำตอบอย่างที่ต้องการและมีประสิทธิภาพ
- ตัว Prompt ต้องประกอบด้วย
    - task description
    - input
    - output format 

### ChatGPT 3.5
```
The video discusses the importance of well-written prompts in eliciting good responses from large language models (LLMs). A systematic approach to prompt engineering is emphasized to ensure optimal performance. The process involves creating prompt templates and using them to guide the LLM in generating summaries of articles, with a focus on emotive phrases. The summary prompt template is constructed step by step, including task description and input variables. The generated summaries can then be used as input for sentiment analysis. The video introduces the concept of chaining LLMs, where the output of one model serves as input for another, paving the way for further exploration into LLM chains in subsequent videos.
```
## 2.LLM Chains
### Note
- คือการนำเอา LLM มาทำงานร่วมกัน ช่วยในการตอบคำถามหรือทำงานได้อย่างมีประสิทธิภาพมากขึ้น
- Exmaple: Article -> Summarise Article (LLM) -> Classify sentiment of article (LLM) -> Sentiment of Article
- เราสามารถเลือก LLM Model ในแต่ละส่วนได้ (เลือก model ที่เหมาะกับงาน)
- LangChain คือ Tool ที่ช่วยให้ทำงานง่ายขึ้นในการ Chain LLM
- บางงานเราต้องทำการ evaluation tool for correctness. และต้อง

### ChatGPT 3.5
```
The video introduces LLM chains, a concept where multiple large language models (LLMs) are interconnected with various tools, popularized by the LangChain library in 2022. LangChain facilitates the integration of LLMs and tools, enabling diverse applications.

The transcript discusses creating prompt templates for tasks like summarization and sentiment analysis, establishing workflows by connecting different LLMs. It also explores LLMs' ability to interact with mathematical, programming, and search libraries, showcasing their versatility in executing tasks based on natural language input.

Additionally, it underscores the importance of well-trained LLMs capable of generating code snippets from natural language, allowing them to act as central reasoning tools with access to resources like search engines and email clients. Ultimately, the transcript highlights the potential of LLMs and LLM chains to drive complex and innovative applications across various domains.
```
## 3.Agents
- Agents are LLM-based systems that execute the ReadsonAction loop.
- เพื่อที่จะแก้ปัญหาตาม Task ใดๆจะต้องมีส่วนประกอบ 2 ส่วนคือ
    - LLM = Reasoning/Decision (Brain)
    - Set of tools ที่จะใช้สำหรับแก้ปัญหา (เช่น search web / save memory)

### ChatGPT 3.5
```
The video introduces LLM chains, a concept where multiple large language models (LLMs) are interconnected with various tools, popularized by the LangChain library in 2022. LangChain facilitates the integration of LLMs and tools, enabling diverse applications.

The transcript discusses creating prompt templates for tasks like summarization and sentiment analysis, establishing workflows by connecting different LLMs. It also explores LLMs' ability to interact with mathematical, programming, and search libraries, showcasing their versatility in executing tasks based on natural language input.

Additionally, it underscores the importance of well-trained LLMs capable of generating code snippets from natural language, allowing them to act as central reasoning tools with access to resources like search engines and email clients. Ultimately, the transcript highlights the potential of LLMs and LLM chains to drive complex and innovative applications across various domains.
```