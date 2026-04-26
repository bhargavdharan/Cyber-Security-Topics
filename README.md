# Cyber Security Topics

A comprehensive repository covering fundamental and advanced cybersecurity concepts, designed for learners, professionals, and enthusiasts.

---

## Repository Structure

This repository is organized into three main sections:

| Directory | Description |
|-----------|-------------|
| [`learning-content/`](./learning-content/) | 15 cybersecurity topics with README lessons and Python simulation projects |
| [`lms-platform/`](./lms-platform/) | Full-stack **Cybersecurity LMS** (Flask + React + MySQL) |
| [`ai-security-products/`](./ai-security-products/) | **AI Security Products** — starting with Risk-Based Authentication Engine |

---

## Table of Contents

1. [Introduction to Cybersecurity](./learning-content/1.%20Intro%20to%20cybersecurity/)
   - [Confidentiality](./learning-content/1.%20Intro%20to%20cybersecurity/confidentiality/)
   - [Integrity](./learning-content/1.%20Intro%20to%20cybersecurity/integrity/)
   - [Availability](./learning-content/1.%20Intro%20to%20cybersecurity/availability/)
2. [Networking Fundamentals](./learning-content/2.%20Networking%20Fundamentals/)
3. [Operating Systems and Security](./learning-content/3.%20Operating%20system%20and%20security/)
4. [Cryptography](./learning-content/4.%20Cryptography/)
5. [Web Application Security](./learning-content/5.%20Web%20Application%20Security/)
6. [Network Security](./learning-content/6.%20Network%20Security/)
7. [Security Assessment and Testing](./learning-content/7.%20Security%20Assessment%20and%20Testing/)
8. [Incident Response and Forensics](./learning-content/8.%20Incident%20Response%20and%20Forensics/)
9. [Cloud Security](./learning-content/9.%20Cloud%20Security/)
10. [Mobile Security](./learning-content/10.%20Mobile%20Security/)
11. [Threat Intelligence and Security Analytics](./learning-content/11.%20Threat%20Intelligence%20and%20Security%20Analytics/)
12. [Industrial Control Systems (ICS) Security](./learning-content/12.%20Industrial%20Control%20Systems%20Security/)
13. [Advanced Persistent Threats (APTs)](./learning-content/13.%20Advanced%20Persistent%20Threats/)
14. [Secure Software Development](./learning-content/14.%20Secure%20Software%20Development/)
15. [Emerging Technologies in Cybersecurity](./learning-content/15.%20Emerging%20Technologies%20in%20Cybersecurity/)

---

## Overview of Topics

### 1. Introduction to Cybersecurity
Covers the CIA Triad (Confidentiality, Integrity, Availability), importance of cybersecurity, common threats, and security principles.

### 2. Networking Fundamentals
Explores TCP/IP, IP addressing, subnetting, network devices, and core protocols (HTTP, DNS, DHCP, FTP).

### 3. Operating Systems and Security
Security features of Windows, Linux, and macOS; user management, access controls, file system security, and hardening.

### 4. Cryptography
Symmetric and asymmetric encryption, hash functions, digital signatures, certificates, and cryptographic protocols.

### 5. Web Application Security
OWASP Top 10 vulnerabilities, secure architecture, input validation, output encoding, and Web Application Firewalls (WAF).

### 6. Network Security
Firewalls, IDS/IPS, VPNs, wireless security, and network traffic analysis.

### 7. Security Assessment and Testing
Vulnerability assessments, penetration testing methodologies, scanning, and exploitation techniques.

### 8. Incident Response and Forensics
Incident response frameworks, digital forensics, evidence handling, and malware analysis.

### 9. Cloud Security
Cloud models, security architecture, Identity and Access Management (IAM), and data protection in cloud environments.

### 10. Mobile Security
Mobile device security, application security, Mobile Device Management (MDM), and secure development practices.

### 11. Threat Intelligence and Security Analytics
Threat intelligence sources, SIEM systems, log analysis, and security data visualization.

### 12. Industrial Control Systems (ICS) Security
ICS architecture, attack vectors, security standards, and critical infrastructure protection.

### 13. Advanced Persistent Threats (APTs)
APT lifecycle, detection strategies, advanced malware analysis, and real-world case studies.

### 14. Secure Software Development
Secure coding practices, Software Development Lifecycle (SDL), threat modeling, and security testing.

### 15. Emerging Technologies in Cybersecurity
IoT security, AI/ML in security, blockchain security, and post-quantum cryptography.

---

## How to Use This Repository

Each topic folder contains a dedicated `README.md` with:
- Detailed explanations
- Real-world use cases
- Best practices
- Key takeaways

Navigate through the topics sequentially or jump to specific areas of interest.

---

## Cybersecurity LMS Platform

The [`lms-platform/`](./lms-platform/) directory contains a full-stack learning management system built with:
- **Backend:** Flask (Python) with JWT auth, MySQL database, REST API
- **Frontend:** React + Vite with interactive lesson rendering, quizzes, and simulations
- **Features:** 15 topics, 4 quizzes per topic, Python simulations with live execution, progress tracking

### Quick Start
```bash
cd lms-platform/backend
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

## AI Security Products

The [`ai-security-products/`](./ai-security-products/) directory contains production-grade security tools built with modern AI/ML practices.

### Risk-Based Authentication Engine
- **Stack:** FastAPI + React + PostgreSQL + Redis + Docker
- **Features:** Real-time 6-factor risk scoring (device, geo, time, IP, velocity, behavioral), admin dashboard, Docker Compose deployment
- **Tests:** 19+ pytest tests with CI/CD via GitHub Actions

### Quick Start
```bash
cd ai-security-products/risk-based-auth-engine
docker-compose up -d
# Open http://localhost:3000
```

---

## Contributing

Contributions are welcome! Feel free to submit enhancements, corrections, or additional topics to expand this cybersecurity knowledge base.
