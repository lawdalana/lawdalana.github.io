---
title: "API Security Testing Tools Guide 2026"
notetype: feed
date: 05-30-2026
last_modified: 05-30-2026
tags: [security, api, owasp, testing, devsecops, pentesting, tools]
status: published
---

## ทำไม API Security ถึงสำคัญ

API คือ attack surface หลักของแอปสมัยใหม่ — OWASP API Top 10 ระบุช่องโหว่ที่โดน exploit มากที่สุด ตั้งแต่ Broken Authentication ไปจนถึง SSRF

ปัญหาคือ general-purpose DAST tools มักพลาดช่องโหว่เฉพาะ API เพราะ:
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

DAST tool ฟรีที่ใช้กันที่สุดในโลก — import OpenAPI/Swagger spec แล้ว scan ทุก endpoint อัตโนมัติ

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

Template granularity สูง — รันเฉพาะ check ที่ต้องการ ครอบคลุม JWT confusion, BOLA/IDOR, GraphQL introspection, SSRF, API key exposure

```bash
nuclei -l api-endpoints.txt -t nuclei-templates/exposures/apis/ -severity high,critical
```

---

### 3. mitmproxy

| | |
|---|---|
| **ประเภท** | Interactive HTTPS Proxy |
| **ราคา** | ฟรี (MIT) |

Intercept ทุก API request/response แบบ real-time — แก้ user ID, เปลี่ยน JWT claims, ลบ auth headers, replay request

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

วิเคราะห์ OpenAPI spec ก่อนเขียนโค้ด — จับ missing auth, permissive schemas, input validation gaps

---

### 5. Escape

| | |
|---|---|
| **ประเภท** | DAST + AI Fuzzing |
| **GraphQL** | ✅ (ดีสุด) |
| **ราคา** | Free tier / Commercial |

AI-assisted fuzzing สร้าง test cases อัตโนมัติ — GraphQL support ดีที่สุดในบรรดา free tools

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
- **RESTler** (Microsoft Research): stateful REST API fuzzer → chain API calls ตามลำดับ

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

Combination ที่ดีที่สุด:
1. **Design phase** → 42Crunch audit spec
2. **Development** → Bearer + Semgrep ใน CI
3. **Testing** → ZAP + Nuclei ใน staging
4. **Production** → mitmproxy manual test + monitoring

> Static analysis จับ design flaws, Dynamic testing จับ runtime bugs — ต้องใช้คู่กัน

---

*Sources: [AppSec Santa](https://appsecsanta.com/api-security-tools/best-open-source-api-security-tools), [OWASP](https://owasp.org/www-project-web-security-testing-guide/), [Expert Insights](https://expertinsights.com/application-security/the-top-api-security-testing-tools)*
