---
title: "API Security Testing Tools Guide 2026"
notetype: feed
date: 2026-05-30
last_modified: 2026-09-16
tags: [security, api, owasp, testing, devsecops, pentesting, tools]
status: published
---

## ทำไม API Security ถึงสำคัญ

API เป็นช่องทางสำคัญที่ผู้โจมตีใช้เข้าถึงแอปสมัยใหม่ OWASP API Top 10 รวบรวมความเสี่ยงด้านความปลอดภัยของ API ตั้งแต่ Broken Authentication ไปจนถึง SSRF

เครื่องมือ DAST ที่ออกแบบมาสำหรับเว็บทั่วไปอาจตรวจช่องโหว่เฉพาะของ API ได้ไม่ครบ เนื่องจาก API มีลักษณะต่างจากเว็บทั่วไป เช่น:

- API ใช้ JSON ไม่ใช่ HTML
- Auth ใช้ JWT/OAuth ไม่ใช่ cookies
- Attack surface อยู่ที่ endpoint schemas ไม่ใช่ crawlable links

> กรณีศึกษา: เว็บราชการไทยรั่วเพราะ API ไม่มี auth → ข้อมูล 34 ล้านคนเข้าถึงได้โดยตรง

---

## ประเภท Security Testing

| ประเภท | ชื่อเต็ม | ทำอะไร |
|--------|----------|--------|
| **SAST** | Static Application Security Testing | อ่าน source code หาช่องโหว่ |
| **DAST** | Dynamic Application Security Testing | ยิง request จริงเข้าระบบที่รันอยู่ |
| **IAST** | Interactive Application Security Testing | ตรวจขณะ app กำลังทดสอบ |
| **SCA** | Software Composition Analysis | ตรวจ dependencies ที่มีช่องโหว่ |
| **API Spec Analysis** | - | วิเคราะห์ OpenAPI/Swagger spec ก่อน deploy |

---

## Top 7 Open Source Tools

### 1. OWASP ZAP (Zed Attack Proxy)

| | |
|---|---|
| **ประเภท** | DAST |
| **REST** | ✅ (OpenAPI import) |
| **GraphQL** | ⚠️ Partial |
| **CI/CD** | ✅ Docker + GitHub Actions |
| **ราคา** | ฟรี (Apache 2.0) |

เครื่องมือ DAST ฟรีที่ใช้กันอย่างแพร่หลาย สามารถนำเข้า OpenAPI/Swagger spec เพื่อสแกน endpoint ที่ระบุไว้โดยอัตโนมัติ

```yaml
# GitHub Actions
- name: ZAP API scan
  uses: zaproxy/action-api-scan@v0.7.0
  with:
    target: "https://api.example.com/openapi.json"
    fail_action: true
```

---

### 2. Nuclei (ProjectDiscovery)

| | |
|---|---|
| **ประเภท** | Template-based Scanner |
| **GitHub Stars** | 26,000+ |
| **Templates** | 12,000+ |
| **ราคา** | ฟรี (MIT) |

เลือก template เพื่อตรวจเฉพาะประเด็นที่ต้องการได้ เช่น JWT confusion, BOLA/IDOR, GraphQL introspection, SSRF และ API key exposure

```bash
nuclei -l api-endpoints.txt -t nuclei-templates/exposures/apis/ -severity high,critical
```

---

### 3. mitmproxy

| | |
|---|---|
| **ประเภท** | Interactive HTTPS Proxy |
| **ราคา** | ฟรี (MIT) |

ดักดู request/response ของ API ที่ส่งผ่าน proxy แบบ real-time เพื่อทดสอบการแก้ user ID, เปลี่ยน JWT claims, ลบ auth headers หรือส่ง request ซ้ำ

```bash
mitmproxy --mode regular --listen-port 8080
# เปิด browser ผ่าน proxy → เห็นทุก API call ที่ frontend ยิง
```

---

### 4. 42Crunch API Audit

| | |
|---|---|
| **ประเภท** | Static (Spec Analysis) |
| **ราคา** | Free tier / Commercial |

วิเคราะห์ OpenAPI spec ก่อนเขียนโค้ด เพื่อหาจุดที่ไม่ได้กำหนดการยืนยันตัวตน schema ที่เปิดกว้างเกินไป และการตรวจสอบ input ที่ยังไม่ครบ

---

### 5. Escape

| | |
|---|---|
| **ประเภท** | DAST + AI Fuzzing |
| **GraphQL** | ✅ (ดีสุด) |
| **ราคา** | Free tier / Commercial |

ใช้ AI ช่วยทำ fuzzing และสร้าง test cases อัตโนมัติ โดยมีการรองรับ GraphQL เป็นจุดเด่น

---

### 6. Bearer

| | |
|---|---|
| **ประเภท** | SAST (Source Code) |
| **Frameworks** | Express, Rails, Django, Spring |
| **ราคา** | ฟรี (ELv2) |

อ่าน source code หา hardcoded secrets, missing auth middleware, SQL injection, PII exposure

```bash
bearer scan ./src --severity=high --exit-code=1
```

---

### 7. Schemathesis / RESTler

| | |
|---|---|
| **ประเภท** | Fuzzing |
| **ราคา** | Open Source |

- **Schemathesis**: property-based testing จาก OpenAPI spec → หา edge cases
- **RESTler** (Microsoft Research): ทดสอบ REST API แบบคำนึงถึงสถานะ โดยเรียก API ต่อเนื่องตามลำดับที่สัมพันธ์กัน

---

## Comparison Table

| Tool | ประเภท | REST | GraphQL | CI/CD | ราคา |
|------|--------|------|---------|-------|------|
| **ZAP** | DAST | ✅ | ⚠️ | ✅ | ฟรี |
| **Nuclei** | Template | ✅ | ✅ | ✅ | ฟรี |
| **mitmproxy** | Proxy | ✅ | ✅ | ❌ | ฟรี |
| **42Crunch** | Static | ✅ | ❌ | ✅ | Free tier |
| **Escape** | DAST+AI | ✅ | ✅ | ⚠️ | Free tier |
| **Bearer** | SAST | ✅ | ✅ | ✅ | ฟรี |
| **Schemathesis** | Fuzzing | ✅ | ❌ | ✅ | ฟรี |

---

## เครื่องมือเสริม

| Tool | ใช้ทำอะไร |
|------|----------|
| **Burp Suite** | Commercial DAST — intercept proxy + auto scanner |
| **ffuf / Feroxbuster** | Brute-force หา hidden API paths/endpoints |
| **Subfinder / Amass** | ค้นหา subdomains ทั้งหมด |
| **httpx** | Probe URLs ตรวจ status, title, tech stack |
| **Nikto** | Web server scanner พื้นฐาน |
| **Trivy** | Container + dependency scanner |
| **SonarQube** | SAST วิเคราะห์ code quality + security |
| **Semgrep** | Lightweight SAST — เร็ว, custom rules ง่าย |

---

## วิธีเลือก Tools ตามสถานการณ์

| สถานการณ์ | แนะนำ |
|-----------|-------|
| **เริ่มจากศูนย์** | 42Crunch (spec) + ZAP (DAST) + mitmproxy (manual) |
| **GraphQL API** | Escape + Nuclei GraphQL templates |
| **CI/CD pipeline** | ZAP Docker + Nuclei + Bearer |
| **Manual pentest** | Burp Suite + mitmproxy |
| **Scale / หลาย targets** | Nuclei (template-based, parallel) |
| **Source code review** | Bearer + Semgrep + SonarQube |
| **ค้นหา subdomains + endpoints** | Subfinder + httpx + ffuf |

---

## OWASP API Security Top 10 (2023)

| # | ช่องโหว่ | Tool ที่ตรวจได้ |
|---|----------|----------------|
| API1 | Broken Object Level Authorization (BOLA) | ZAP, Nuclei, mitmproxy |
| API2 | Broken Authentication | ZAP, Nuclei, Bearer |
| API3 | Broken Object Property Level Authorization | ZAP, Nuclei |
| API4 | Unrestricted Resource Consumption | ZAP, 42Crunch |
| API5 | Broken Function Level Authorization | ZAP, Nuclei |
| API6 | Unrestricted Access to Sensitive Business Flows | Escape, Nuclei |
| API7 | Server Side Request Forgery (SSRF) | Nuclei, ZAP |
| API8 | Security Misconfiguration | ZAP, Nuclei, 42Crunch |
| API9 | Improper Inventory Management | Nuclei, httpx |
| API10 | Unsafe Consumption of APIs | Bearer, Schemathesis |

---

## DevSecOps Pipeline Setup

```yaml
# .github/workflows/api-security.yml
name: API Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      # Spec analysis
      - name: 42Crunch Audit
        run: 42c-ast audit --fail-on-error --input openapi.yaml

      # Source code scan
      - name: Bearer Scan
        run: bearer scan ./src --severity=high --exit-code=1

      # Dynamic scan
      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: "https://staging.example.com/openapi.json"
          fail_action: true

      # Template scan
      - name: Nuclei Scan
        run: |
          nuclei -l api-endpoints.txt \
            -t nuclei-templates/exposures/apis/ \
            -severity high,critical
```

---

## สรุป

ตัวอย่างการใช้เครื่องมือร่วมกันในแต่ละช่วง:

1. **Design phase** → 42Crunch audit spec
2. **Development** → Bearer + Semgrep ใน CI
3. **Testing** → ZAP + Nuclei ใน staging
4. **Production** → mitmproxy manual test + monitoring

> Static analysis ช่วยหาปัญหาจากโค้ดและการออกแบบ ส่วน dynamic testing ตรวจพฤติกรรมขณะระบบทำงาน การใช้ร่วมกันจึงช่วยให้ตรวจสอบได้ครอบคลุมขึ้น

---

*Sources: [AppSec Santa](https://appsecsanta.com/api-security-tools/best-open-source-api-security-tools), [OWASP](https://owasp.org/www-project-web-security-testing-guide/), [Expert Insights](https://expertinsights.com/application-security/the-top-api-security-testing-tools)*
