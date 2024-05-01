---
title : Feature Store - Feast
notetype : feed
date : 01-04-2024
---

# Summary

![overview](/assets/img/edx/feast/feast_0.avif)

- [Feast](https://docs.feast.dev/) ย่อมาจาก (**Fea**ture **St**ore)
- [Feast](https://docs.feast.dev/#what-is-feast)  ช่วยทำให้
    - Feature พร้อมใช้ทั้ง Training และ Serving
    - สร้าง Data แบบ point-in-time ในช่วงเวลานั้น ทำให้ป้องกันที่ Future data จะไม่ leak ไปที่ model ขณะ Training
    - แยกส่วน Data ที่จะใช้ใน Model ออกจาก data infrastructure พื้นฐานทำให้เวลาเอาไปใช้จะง่ายกว่ามาก
- [Feast](https://docs.feast.dev/#who-is-feast-for)  เหมาะกับ
    - รู้ Business Impact เวลาใช้ Data
    - Data ที่เป็น structured data
    - ต้องการ low latency feature retrieval (e.g. p99 feature retrieval << 10ms)
    - มีหลาย use cases (ใช้ Feature ร่วมกันทำได้หลายอย่าง)
- [Feast](https://docs.feast.dev/#what-feast-is-not)  ไม่ใช่
    - ETL Tools เหมือนกับ dbt
    - Data orchestration ที่เอาไว้จัดการ DAGs
    - Database ที่เอาไว้เก็บ แต่เป็นการจัดการ data store
- [Feast](https://docs.feast.dev/#feast-does-not-fully-solve) ยัง support ไม่หมด
    - ยังไม่สามารถ reproducible model training ได้ เพราะไม่ได้มี data version control และไม่ได้ manage Train/test split
    - ปกติ Feast จะเก็บเฉพาะ Data ที่ process แล้วเหมากับการเอาไปใช้ได้เลย โดยส่วมมาก Feast จะถูกต่อเข้ากับ upstream systems
    - Feast ถูกสร้างให้ push streaming feature เข้ามาแต่ไม่ได้ถูกออกแบบให้ไป pull จาก streaming source
    - Feast สามารถเชื่อม feature store กับ model version ได้แต่ไม่ได้มีความสามารถถึงขนาด capturing end-to-end lineage from raw data sources to model versions
    - Feast สามารถเชื่อมต่อกับ  Great Expectations ได้แต่ไม่สามารถที่จะช่วยตรวจจับ หรือ แก้ไขปัญหา data drift / data quality ได้ (ควรไปตรวจจับที่ data pipeline)
- [Use Cases](https://docs.feast.dev/#example-use-cases)
    - Personalizing online recommendations
    - Online fraud detection
    - Churn prediction
    - Credit scoring

# Concept (TBD)

## [Architecture](https://docs.feast.dev/getting-started/architecture-and-components/overview)


![Architecture](/assets/img/edx/feast/feast_architecture_0.avif)