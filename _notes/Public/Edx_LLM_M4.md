---
title : Edx - LLM Application through Production (Module 4)
notetype : feed
date : 30-03-2024
---

# Module 4: Fine-tuning and Evaluating LLMs

## Summary
- Fine-tuning ช่วยให้เราสามารถ customize model ได้ให้ specific มากขึ้น
- When and How

## 1. Applying Foundation LLMs
### Note
- เราสามารถนำข้อมูลที่มีอยู่เช่น NEWS API + Example แล้วนำเข้า model LLM เพื่อให้ได้ Summary
- Model LLM มาจาก
    - Few-shot Learning with open-sourced
    - Open-source instruction-following LLM
    - Paid LLM-as-a-Service
    - DIY
- Fine-Tuning ช่วยให้เราไม่ต้องไปสร้างใหม่ตั้งแต่ต้น, ทำให้ model เหมาะกับงานที่ใช้
- มี Tools ต่างๆถูกสร้างขึ้นเพื่อช่วยในการพัฒนา Trining/Fine-Tuning process
- การ Evaluating model นั้นสำคัญ
    - Generic evaluation tasks นั้นเหมาะกับทุก model
    - Specific evalution tasks นั้นเกี่ยวข้องกับ LLM Focus

![flow_develop](/assets/img/edx/llm/edx_llm_m4_apply.png)

### ChatGPT 3.5
```
Module 4 delves into the adaptability of large language models, stressing the importance of tailoring them to specific needs when necessary. It offers guidance on fine-tuning models using tools like DeepSpeed and Hugging Face, and emphasizes the importance of evaluating and customizing models for desired outcomes. The transcript also outlines the typical structure of large language model releases, including various sizes and versions suited for different tasks. Developers are advised to consider factors like accuracy, speed, and task-specific performance when selecting a model. Finally, the module focuses on creating an application that summarizes news articles and transforms them into riddles, showcasing practical applications of large language models.
```

## 2.Fine-Tuning: Few-shot learning
### Note
- Few-shot Learning (ใช้ model ต้นทาง และ ต้องมี premade example เพื่อสร้าง prompt ที่อยากได้)
- ข้อดีคือ 
    - เริ่มสร้างได้ง่ายและเร็ว 
    - Good performance
    - จ่ายแค่ค่า computation
- ข้อเสียคือ 
    - Data ที่เอามาทำ few-shot ต้องดีและครอบคลุมทุกเป้าหมายที่วางไว้ 
    - เนื่องจากเราไม่ได้ train มาทำให้ต้องใช้ model ใหญ่เพื่อให้ได้ performance ที่ดีกว่าแต่ model ใหญ้ไม่เหมาะกับ Computer ทั่วไป

![few-shot](/assets/img/edx/llm/edx_llm_m4_few-shot.png)

### ChatGPT 3.5
```
The transcript explores using few-shot learning as a solution to a problem. It outlines the setup, including access to a news API and pre-made examples of articles turned into riddles. Few-shot learning is described as quick to develop since it requires minimal data and computation costs. However, it necessitates high-quality examples covering the task's scope. Larger models are recommended for better performance, but they may pose space and computation challenges. The implementation involves constructing a prompt for the large language model to summarize articles and create riddles. Considerations include the need for long input sequence models and selecting an appropriate base model size. The transcript hints at exploring another option in the subsequent video.
```

## 3.Fine-Tuning: Instruction-following LLMs
- ถ้าเรามี Premade example เราสามารถทำท่าคล้ายๆกับ Few-shot Learning ได้เลย
- แต่ถ้าเราไม่มี Premade exmaple เราสามารถ follow ตาม instuction ของ model ได้เลย
- ข้อดี
    - ไม่ได้ต้องการ Data เหมือน Few-shot หรือจะเรียกวิธีนี้ว่า zero-shot learning
    - Performance ขึ้นกับ model ที่เอามา Train ว่าเหมาะรึเปล่า
    - จ่ายแค่ค่า computation
- ข้อเสีย
    - ถ้า data ที่ใช้ train model ไม่เหมือนกับ Dataset ของเราจะทำให้ performance แย่ไปเลย
    - เนื่องจากเราไม่ได้ train มาทำให้ต้องใช้ model ใหญ่เพื่อให้ได้ performance ที่ดีกว่าแต่ model ใหญ้ไม่เหมาะกับ Computer ทั่วไป

![zero_shot](/assets/img/edx/llm/edx_llm_m4_instruction_follow.png)

### ChatGPT 3.5
```
This segment explores another approach to utilizing open-sourced large language models (LLMs) by employing pre-fine-tuned instruction-following versions. If pre-made examples are unavailable, zero-shot learning is suggested, where the task is described and the model is given the article to summarize. Considerations include crafting specific prompts for the model, potential performance based on the fine-tuned model's training data, and computation costs only at inference. However, if the fine-tuned model isn't adept at the task, performance may suffer. Implementation involves providing a concise prompt describing the task and inputting the article for summarization. Depending on the model's training, results may vary, and alternative options may need exploration.
```

## 4.Fine-Tuning: Fine-Tuning: LLMs-as-a-Service Video
- เป็นการสร้าง Application จาก LLM paid service ซึ่งต้องดูด้วยว่า service llm ที่ใช้เหมาะกับ dataset ตัวเองด้วยหรือไม่
- ข้อดี
    - สร้าง Application ได้เร็วมากขึ้นเพราะเป็นแค่การ Call API
    - Performance ดีเพราะ compute ทุกอยากบน Server
- ข้อเสีย
    - ค่าใช้จ่ายจะเป็น token ที่ส่งและรับ
    - Data privacy / Security
    - Vendor lock-in

![LLMaaS](/assets/img/edx/llm/edx_llm_m4_LLMaaS.png)

### ChatGPT 3.5
```
This section explores utilizing a proprietary or LLM (Large Language Model) as a service to address application development needs. Assuming no pre-made examples are available, the focus is on incorporating the LLM service into the application workflow. Benefits include quick setup and high performance due to server-side computation and infrastructure. However, the downside is the cost associated with each token sent and received. Additionally, there are concerns regarding data privacy and security, as well as the risk of vendor lock-in. Implementation involves describing the prompt and sending tokens to the API along with an API key. This approach is noted for its simplicity and generally high performance, particularly as proprietary LLMs currently outperform open-source alternatives. Finally, if none of the available options fit the requirements, the next step would involve fine-tuning a large language model.
```

## 5.Fine-Tuning: DIY Video
- ถ้าเราลองทั้งหมดแล้วไม่ตอบโจทย์กับปัญหาของเรา และเรามี premade-exmaple จำนวนมากพอ วิธีนี้จะเป็นอีกวิธีที่เราได้ model ตามที่เราต้องการ
- วิธีสร้าง LLM มี 2 วิธี
    - Create from scratch (ข้อจำกัดมากเกินไป แทบจะเป็นไปไม่ได้)
    - Fine-tune an existing model
- ข้อดี
    - ปรับแต่ง model ได้ตามงาน
    - ยิ้งปรับแต่ เราก็สามารถใช้ model ที่มีขนาดเล็กลงได้ช่วยให้ inference ได้เร็วขึ้น
    - ทั้ง model และ Data อยู่ในการควบคุมทั้งหมด
- ข้อเสีย
    - ต้องใช้เวลาและเงิน จำนวนมากในการ Train
    - ต้องใช้ Data จำนวนมาก
    - คนที่ทำต้องมี skill expertise ใน LLM
- เราสามาร fine-tuning ขึ้นกับ data ที่เรามีโดยสามารถทำได้โดย
    - Self-instuction (Alpaca/Dolly V1 ใช้ LLM ในการช่วยสร้าง data set โดยการ augmentation)
    - High-quality fine-tune (Dolly V2 ถ้ามี Data ดีอยู่แล้วก็สามารถ fine-tuning ได้เลย)

![LLM DIY](/assets/img/edx/llm/edx_llm_m4_LLM_DIY.png)

### ChatGPT 3.5
```
If existing LLM offerings don't meet our requirements, the next step is to build our own. Assuming we have sufficient pre-made examples and access to a news API, we can either create a base model from scratch or fine-tune an existing one. Building a foundation model from scratch is rarely pursued due to resource and time constraints. Instead, fine-tuning an existing model allows for task-specific customization and control over data. Although this approach requires computational investment, it can lead to smaller, more efficient models tailored to specific use cases. However, it necessitates a substantial dataset and expertise in fine-tuning techniques. Recent advancements in fine-tuning instruction-following models, such as Dolly V2, offer promising results, especially with the release of open-source datasets. Dolly V2, developed by Databricks, is particularly noteworthy for its use of open-source data, marking a significant advancement in the field.
```

## 6.Dolly
![dolly](/assets/img/edx/llm/edx_llm_m4_dolly.png)

- [Dolly](https://huggingface.co/databricks/dolly-v2-12b) เป็น instuction-following LLM ที่มี parameter ขนาด 12B
    - เริ่มจากนำโมเดลจาก Pythia 12 billion มา Train โดยใช้ [Pile Dataset](https://pile.eleuther.ai/)
    - หลังจากนั้นก็ Fine-tuning โดยใช้ Databrick-dolly-15k dataset (Data high quality intellectual tasks produced by the employees of Databricks)
- เป็น Project ที่ insprired มาจาก Stanford Alpaca Project แต่ไม่มีปัญหาเรื่อง commercial เหมือน Alpaca

![dolly](/assets/img/edx/llm/edx_llm_m4_alpaca.png)

- Future of Dolly
    - 2018 - 2023 สร้าง transformer models ที่ใหญ่จน parameter แตะ 1 Trillion.
    - 2023 -> now สร้าง model ขนาดเล็กและนำไปใช้ใน application ต่างๆ

### ChatGPT 3.5
```
Dolly, introduced in 2023, revolutionized large language modeling by focusing on instruction-following tasks. It is a 12 billion parameter model based on the Eleutha AI Pythia 12 billion parameter model. Unlike previous approaches, Dolly emphasizes combining open-source models with high-quality, open-source datasets, such as the Databricks-Dolly-15K dataset, released for commercial use. This dataset, consisting of instruction-response pairs, was crucial in Dolly's development and is unique for its open and commercially usable nature. Although not state-of-the-art, Dolly showcases the potential of using small models with high-quality datasets for commercial viability. The idea for Dolly originated from the Stanford Alpaca project, which experimented with instruction generation and fine-tuning models. Moving forward, the focus in the field of large language models seems to be shifting towards smaller, task-specific models rather than chasing larger models. This shift opens up new possibilities for diverse applications and continued evolution in the field.
```

## 7.Evaluating LLMs
- ต่อให้การ fine-tuning จะดีแต่ไหน ยังไงเราก็จำเป็นจะต้องทำ Evaluating LLM อยู่ดีเพื่อวัด Perfomacne
- เราดู loss เหมือนกับ Deep learning models อื่นๆแต่เราจะไม่ได้ใช้ Accury, F1, Precision เหมือน models อื่นๆ
- Models LLM ที่ดีควรจะมี Accuracy สูงแต่ Perplexity ต่ำ
    - Accuracy = คำต่อไปถูกหรือผิด
    - Perplexity = ตัวเลือกนั้นมั่นใจแค่ไหน
- [[Perplexity]] ดีกว่า Accuracy แต่ยังไม่สามารถวัดคุณภาพของ result ได้อยู่ดี
- ดังนั้น Task อื่นๆจะใช้การวัดผลที่เหมาะกับงานนั้นๆเช่น 
    - Translation - [[BLEU]]
    - Summarization - [[ROUGE]]

![dolly](/assets/img/edx/llm/edx_llm_m4_perplexity.png)
> [Perplexity คืออะไร](https://medium.com/@gunanini784/%E0%B8%A7%E0%B8%B4%E0%B8%96%E0%B8%B5%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%A1%E0%B8%B4%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%AA%E0%B8%B4%E0%B8%97%E0%B8%98%E0%B8%B4%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%82%E0%B8%AD%E0%B8%87%E0%B9%82%E0%B8%A1%E0%B9%80%E0%B8%94%E0%B8%A5-cf98823a1a02) วิธีง่ายๆในการประเมินประสิทธิภาพของโมเดล คือ ประเมินว่าผลลัพท์ที่ได้ออกมานั้นทำให้เราประหลาดใจมากเพียงใด ถ้าทำให้เรารู้สึกประหลาดใจหรือต่างจากที่เราคิดไว้มากเท่าใด ก็เท่ากับว่าค่า perplexity นั้นก็จะสูงตามไปด้วย จึงพูดได้ว่าค่า perplexity และ ความรู้สึกประหลาดใจ มีความสัมพันธ์เป็นสัดส่วนเชิงเส้นต่อกัน (linearly proportional)
โดยตามทฤษฎีแล้วถ้าค่า k เพิ่มขึ้น ค่า Perplexity ก็จะน้อยลง และถ้าพบว่าค่า Perplexity “ต่ำ” มากเท่าไร ก็หมายความว่าโมเดลนั้นมีประสิทธิภาพดีมากเท่านั้น 

### ChatGPT 3.5
```
Fine-tuning large language models (LLMs) offers numerous applications, but evaluating their performance is essential. While traditional metrics like loss and validation scores are used during retraining, they may not provide meaningful insights for LLMs due to their nature of generating probability distributions over tokens. Perplexity, measuring the spread of these distributions, can indicate model confidence, but it doesn't guarantee quality results. For tasks like conversation or summarization, accuracy and low perplexity are desired, but they don't ensure coherence or contextuality. Thus, task-specific evaluation metrics are crucial for assessing LLM performance accurately, a topic to be explored in the next video.
```

## 8.Task-specific Evaluations
- BiLingual Evaluation Understaudy ([[BLEU]]) for translation
    - unigram จะเป็นการเช็ต word ว่าเกิดขึ้นกี่ครั้ง เปรียบเทียบระหว่าง predict กับ Actual
    - bigram = เทียบ 2 คำต่อกัน, Trigram = เทียบ 3 คำต่อกัน
    - ค่ามาก = model translation ยิ่งดี

![dolly](/assets/img/edx/llm/edx_llm_m4_BLEU.png)
- Recall-Oriented Understudy for Gisting Evaluation ([[ROUGE]]) for summarization
    - คล้ายกับการคำนวน BLEU Score แต่ของ ROUGE จะเป็นการคำนวน จำนวนคำที่ match / จำนวนคำที่มี

![dolly](/assets/img/edx/llm/edx_llm_m4_ROUGE.png)

- แต่การวัด Score นั้นไม่ควรวัดเพียงแค่ Data ของเราเองแต่เราควรใช้ Data ของคนอื่นด้วย
- Standard Question and Answering Dataset [[SQuAD]] Dataset คือ dataset ถามตอบที่ใช้กันทั่วไปในการ วัดผลเปรียบเทียบ Models LLM
- Evaluation Metrics at the cutting edge
    - Target application
        - NLP Task เช่จ Q&A, reading comprehension, and summarization
        - เลือก queries ที่ตรงกับ API
        - ให้คนมาโหวต
    - Aligment
        - `Helpful` ทำได้ตาม instuction และตอบคำถามตามที่ User ต้องการ วัดผลได้โดยให้คน Vote
        - `Honest` วัดผลโดยคนให้คะแนนเรื่อง [[hallucinations]] และใช้ TruthfulQA benchmark dataset
        - `Harmless` วัดผลโดยคนให้และระบบอัตโนมัติให้คะแนนความ toxicity (RealToxicityPrompts) หรือ ระบบวัด Bias(Winogender, CrowS-Pairs)

### Related link
- [ว่าด้วยเรื่อง metrics](https://thaikeras.com/community/main-forum/on-metrics/)
- [Understanding BLEU and ROUGE score for NLP evaluation](https://medium.com/@sthanikamsanthosh1994/understanding-bleu-and-rouge-score-for-nlp-evaluation-1ab334ecadcb)

### ChatGPT 3.5
```
Task-specific evaluation metrics are essential for assessing language model performance in various applications. BLEU is commonly used for translation tasks, measuring similarity between model outputs and reference translations based on n-grams. ROUGE is employed for summarization, evaluating overlap between model-generated summaries and reference samples, considering content similarity and summary length. Benchmark datasets like SQuAD facilitate model evaluation and comparison in the research community. Advanced metrics focus on alignment, hallucination detection, and toxicity analysis, ensuring model reliability and effectiveness. Ongoing research aims to address challenges in model alignment and enhance language model evaluation techniques.
```

## 9.Guest Lecture from Harrison Chase (Evaluation of llm chains and agent)
- ปกติเราใช้ LLM Agent เป็นตัวช่วยในการตัดสินใจ (The reasoning engine)
- ยกตัวอย่าง Application ที่ใช้กันก็คือ Retrieval Augmented Generation Chatbot (RAGs) โดยปกติเราจะใช้ LLM ในการช่วยในการตัดสินใจว่า Query ที่ใส่เข้าไปเกี่ยวข้องกันยังไง
- คำถาม: ทำไมการวัดผลถึงยาก = ปัญหาแรกเลยคือ Data ไม่พอ
    - โดยปกติแล้วจะไม่เริ่มต้นด้วย Dataset แต่จะเริ่มจาก Idea/Proplem แล้วสร้าง Application ขึ้นมาซึ่งถ้าเจาะจงมากก็จะไม่สามารถหา Dataset ตั้งต้นได้
    - รวมถึงการที่เราไม่รู้ว่าเราควรรวบรวม Data หน้าตาแบบไหน เพราะมันไม่มี guide ในการรวบรวม Data

![dolly](/assets/img/edx/llm/edx_llm_m4_guest.png)
- คำถาม: ทำไมการวัดผลถึงยาก = ปัญหาต่อมาเลยคือ Metrics ที่ใช้วัดไม่เพียงพอ
    - Metrics ที่ใช้วัด Task ML ตัวไปเช่น Perplexity, BLEU, ROUGE, SQuAD ทำได้ไม่ดีนักเนื่องจาก Chatbot จะตอบคำถามเป็น Freeform Text ทำให้วัดได้ยาก
- Potential Solution - Best Practices 
    - Lack of data
        - สร้าง test Dataset โดยใช้ LLM เป็นคนช่วย Generate
        - โดยที่เราแบ่ง Document ออกเป็นแต่ละส่วน และโยนแต่ละส่วนเพื่อสร้าง Q&A Pairs
        - ![dolly](/assets/img/edx/llm/edx_llm_m4_lackdata.png)
        - หรือถ้าเรามี Application ที่รันอยู่ในขนาดนั้นก็ควรเก็บ Input และ Output มาพัฒนาตลอดเวลา
    - Lack of Metrics
        - logging ทุก output ของแต่ละ Process จะช่วยทำให้ตรวจสอบได้ง่าย
        - ใช้ LLM มาช่วยในการตัดสินว่า Final Answer นั้นตรงกับที่เรา Query รึเปล่า
        - รับ Feedback โดยตรงจาก User ทั้ง Direct/Indirect Feeback
- ขั้นตอนการทำ Offline Evaluation
    - สร้าง test dataset
    - รัน test data ด้วย model LLM ของเราที่ fine-tuning แล้ว
    - ตรวจสอบเบื้องต้นด้วยตา (not scalable)
    - ใช้ LLM มาทำการช่วยให้คะแนนตัว Final Answer
- ขั้นตอนการทำ Online Evaluation
    - เก็บ Feedback จาก User ทุกครั้งที่มีการเรียก
        - Direct Feeback (Thumbs up/Thumbs down) explicit data
        - Indirect Feedback (clicked on link, did not click) implicit data
    - Track Feedback overtime


### ChatGPT 3.5
```
Harrison Chase, the creator of LangChain, discusses the evaluation of LLM chains and agents, focusing on their overview, challenges, potential solutions, and evaluation methods. LLM chains leverage language models as reasoning engines, utilizing external data and computation for knowledge while grounding responses in retrieved data. Evaluating these agents is difficult due to a lack of data and metrics. Solutions include generating datasets programmatically or accumulating data over time. Metrics challenges are addressed by visually inspecting outputs, using language models to judge correctness, and gathering user feedback. Offline evaluation involves testing against a dataset, visually inspecting, and auto-grading, while online evaluation gathers feedback from deployed models, either directly or indirectly through user interactions. Continuous monitoring ensures model performance in production, with emerging best practices shaping the field's development.
```