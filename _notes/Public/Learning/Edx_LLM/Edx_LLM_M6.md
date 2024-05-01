---
title : Edx - LLM Application through Production (Module 6)
notetype : feed
date : 30-04-2024
---

# Module 4: LLMOps

## Summary
- LLMOps เป็นการรวม MLOps + LLM
- MLOps เป้าหมายคือการ Maintain stable performance (KPIs, Update model, Reduce failures) และ Maintain long-term efficiency (Automate manual work, Reduce iteration cycle, Reduce risk of noncompliance)
- 

## 1. Traditional MLOps
### Note
- MLOps = DevOps + DataOps + ModelOps
    - Testing
    - CI/CD
    - Feature Store
    - Workflow
    - Automate
    - Model Registry
- แบ่งเป็น 3 Stage
    1. Dev เป็นส่วนที่ทำ EDA, POC Model, feature
    2. Staging เป็นส่วน unit tests, integration tests
    3. Production เป็นส่วน Model Training, Serving , Model Evaluate, Monitoring (MLFlow)

![MLOps](/assets/img/edx/llm/edx_llm_m6_MLOps.png)

### ChatGPT 3.5
```
LLMOps, or Legal and Ethical MLOps, adds another layer of complexity to traditional MLOps by integrating legal and ethical considerations into the management of ML assets. While traditional MLOps focuses on optimizing performance and efficiency, LLMOps extends this framework to ensure compliance with legal regulations and ethical standards. This involves implementing processes and automation to address issues such as data privacy, algorithmic fairness, transparency, and accountability throughout the ML lifecycle. By incorporating LLMOps, organizations can mitigate risks associated with legal liabilities and ethical concerns, ensuring that their ML systems are not only effective but also responsible and trustworthy.
```

## 2.LLMOps
### Note
- มีส่วนที่เปลี่ยนแปลงจาก MLOps ดังเดิม
- Model จะกลายเป็น LLM หรือ Pipieline เช่น LangChain หรือเป็นการเรียก service เช่น Vector Database
- Model Training จะกลายเป็น Model fine-tuning, Pipeline tunging, Prompt engineering และยังต้องใช้ Cost มากขึ้นเพื่อจัดการกับปัญหา Performance
![LLMOps Model](/assets/img/edx/llm/edx_llm_m6_LLMOps01.png)
![LLMOps Model](/assets/img/edx/llm/edx_llm_m6_LLMOps05.png)
- User feedback จะเป็น Data ที่สำคัญที่อาจจะรวมกันระหว่าง internal และ external
- Monitoring จะมี human feedback loop เข้ามาเสริมด้วย
![LLMOps FeedBack](/assets/img/edx/llm/edx_llm_m6_LLMOps02.png)
- Automate testing จะยากขึ้นและกลายเป็นงาน human evaluation ที่ต้องให้คนจำนวนน้อยๆ มาทดลองใช้ก่อน เพื่อเพิ่มความมั่นใจก่อนจะปล่อยไปให้ users ใช้
![Automate testing](/assets/img/edx/llm/edx_llm_m6_LLMOps03.png)
- Production tools มีการเปลี่ยน
    - Vector Database
    - ใช้ CPU, GPU มากขึ้น
![LLMOps Service](/assets/img/edx/llm/edx_llm_m6_LLMOps04.png)
- Inference & Serving ก็จะมีปัญหาเรื่องของ Cost, Latency, Performance tradeoffs โดยเฉพาะถ้าเราใช้ 3rd-party LLM APIs
![Serving](/assets/img/edx/llm/edx_llm_m6_LLMOps06.png)


![Serving](/assets/img/edx/llm/edx_llm_m6_LLMOps07.png)

### ChatGPT 3.5
```
LLMOps, or Legal and Ethical MLOps, adapts the traditional MLOps architecture to accommodate the unique challenges posed by legal and ethical considerations in machine learning. While many elements of the architecture remain consistent, such as the dev-staging-production workflow, access controls, and the use of git and model registries for shipping pipelines and models, several key areas require adjustment. Model training methods may shift from frequent retraining to lighter-weight approaches like model fine-tuning or pipeline tuning, reflecting the constraints of LLMs. Human feedback becomes paramount and is integrated as a crucial data source throughout the development and production stages. Monitoring and quality testing processes may necessitate a stronger reliance on human evaluation, particularly in the Continuous Deployment phase, where incremental rollouts and user feedback play a central role. Additionally, changes in production tooling, such as shifting to GPUs for serving larger models, and considerations of cost and performance trade-offs further distinguish LLMOps from traditional MLOps. Despite these adaptations, foundational aspects of MLOps, such as modular data pipelines, the Lakehouse data architecture, and CI infrastructure, remain essential components of LLMOps.
```

## 3.LLMOps Details
- Key Concerns
    - Prompt Engineering
    - Packaging models or pipelines for deployment
    - Scaling out
    - Managing cost/performance tradeoffs
    - Human feedback, testing, and monitoring
    - Deploying models vs. deploying code
    - Service infrastructure: vector database and complex models
- Prompt Engineering เป็นส่วนที่สำคัญที่สุดแม้แต่บน production
    - Track queies, response, compare ของ prompt โดยใช้ Tools เช่น MLFlow
    - Template สร้างมาเพื่อ standardize prompt format ให้ตรงกับที่เราต้องการ Tools ที่ใช้เช่น LangChain, LlamaIndex
    - Automate แทนที่ Manual Prompt Engineering ด้วย Automated Tuning เช่น DSP (Demonstrate-Search-Predict-Framework)
- Packaging models or pipeline for deployment พยายามส้ราง standard ในการ deploy model หลายๆแบบ เช่นการใช้ MLFlow มาช่วย
![Packaging models](/assets/img/edx/llm/edx_llm_m6_LLMOps08.png)
![MLFlow](/assets/img/edx/llm/edx_llm_m6_LLMOps10.png)
- Scaling Out เพื่อรองรับกับ Data และ Model ขนาดใหญ่
    - Fine-Tunging and Training เช่น Tensorflow, PyTorch, DeepSpeed, Ray
    - Serving and inferences
        - Real Time: Sacle out `End Points`
        - Streanimg and batch: Sacle out `pipelines` (ใช้ Spark + Delta Lake)
- Managing cost / performance tradeoffs
    - Metric to optimize
        - Cost ต่อ Queries หรือ Training
        - เวลาในการ develop
        - ROI
        - Accuracy / metric model
        - Latency
    - Tips
        - ทำจากง่ายก่อน Existing models -> Prompt engineering
        - ให้คำนวน cost ทั้งบน Dev และ Prod
        - ลด cost โดยการปรับแต่ง model, queries และ configuration
        - รับ Human feedback
        - อย่า optimize มากเกินไปเพราะอีก 6 เดือนข้างหน้า อาจจะเปลี่ยนไปแล้ว
- Human feedback เป็นส่วนที่สำคัญมากส่วนหนึ่ง เราควรวางแผนเพื่อเก็บจาก Application และจัดเก็บให้เหมือนกับ Data อื่นๆ พร้อมที่จะนำไปทำ analysis หรือ tuning
- Deploy model vs Deploy code เราต้องเลือกว่าจะเอาอะไรขึ้น prod บ้าง
- Service architecture 
    - กรณีที่ใช้ Vector Database
    ![Vector Database](/assets/img/edx/llm/edx_llm_m6_LLMOps11.png)
    - Complex model ด้านหลังมีสิ่งที่ต้องระวัง
        - เราไม่สามารถควบคุม Models behavior ได้มากนัก
        - เราอาจจะต้องทำ Model version ไว้ด้วย แต่ถ้าใช้ API 3rd-party บางรายก็มีทำ support ไว้อยู่แล้ว

### ChatGPT 3.5
```
LLMOps, or Legal and Ethical MLOps, delves into the nuances of integrating legal and ethical considerations into the machine learning operations lifecycle. While some topics overlap with traditional MLOps, such as model training and fine-tuning, LLMOps introduces unique challenges. Prompt engineering, for instance, involves tracking, templating, and automating prompts to align with production requirements. MLflow serves as a pivotal tool for standardizing model deployment, facilitating the movement of models and pipelines from development to production. Scaling computation for large data and models requires familiar concepts like distributed training and serving, albeit with potentially different tools. Managing cost-performance trade-offs entails optimizing metrics like query costs and development time, while also prioritizing human feedback to ensure user-centric model performance. Differentiating between deploying models and deploying code prompts considerations of versioning and stability in service architectures, emphasizing the need for clear endpoint versioning and deterministic inference configurations.
```