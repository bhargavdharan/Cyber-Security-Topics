# AI Security Products

A collection of production-grade, AI-driven security tools designed to protect modern applications, infrastructure, and users from evolving cyber threats. Each product is built as a standalone, deployable microservice that can integrate with existing security stacks or operate independently.

---

## 🎯 Vision

As cyberattacks become faster, smarter, and more automated, traditional rule-based security systems struggle to keep up. This suite applies **machine learning, behavioral analytics, and real-time risk scoring** to security problems that were previously solved with static rules and manual review.

**Core principles across all products:**
- **Intelligence over rules** — Adaptive models that learn normal vs. anomalous behavior
- **Real-time decisions** — Sub-second scoring and response at scale
- **Zero-trust by default** — Verify every access, every request, every time
- **Developer-first** — REST APIs, Docker deployments, clear documentation
- **Privacy-respecting** — Edge scoring where possible, minimal data collection

---

## 📦 Products

### Current

| # | Product | Status | Description |
|---|---------|--------|-------------|
| 1 | [**Risk-Based Authentication Engine**](./risk-based-auth-engine/) | ✅ Production Ready | Real-time 6-factor risk scoring for login events. Detects account takeovers, credential stuffing, and anomalous access patterns. Outputs risk scores (0.0–1.0) and recommended actions (ALLOW / MFA / REVIEW / BLOCK). |

### In Development

| # | Product | Status | Description |
|---|---------|--------|-------------|
| 2 | **AI-Powered Phishing Detection System** | 🚧 Planned | Analyzes emails, URLs, and web content using NLP and computer vision to detect phishing attempts, brand impersonation, and social engineering — before users click. |
| 3 | **Intelligent SIEM Log Analyzer** | 🚧 Planned | Replaces static SIEM correlation rules with unsupervised anomaly detection. Automatically baselines network traffic, auth logs, and system events to surface true threats without alert fatigue. |
| 4 | **Malware Behavior Classifier** | 🚧 Planned | Sandboxes file executions and uses behavioral sequence modeling to classify malware families, zero-day variants, and ransomware — without relying on known signatures. |
| 5 | **Insider Threat Detection Engine** | 🚧 Planned | Monitors user activity across endpoints, cloud apps, and data repositories. Uses graph neural networks to detect data exfiltration, privilege abuse, and lateral movement by trusted insiders. |
| 6 | **Vulnerability Prioritization AI** | 🚧 Planned | Ingests vulnerability scan results (SAST/DAST/container), threat intel feeds, and asset criticality to predict which CVEs are actually exploitable in your environment — cutting noise by 90%+. |
| 7 | **Adaptive Web Application Firewall (WAF)** | 🚧 Planned | Learns your application's normal traffic patterns to block SQL injection, XSS, and bot attacks with far fewer false positives than regex-based WAFs. |

---

## 🏗️ Shared Architecture

Every product in this suite follows a consistent architectural pattern:

```
┌─────────────────────────────────────────────┐
│              React Dashboard                │
│          (Vite + Recharts + Axios)          │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         FastAPI Backend Service             │
│    (Python 3.12+, Pydantic, Uvicorn)        │
│                                             │
│  ┌────────────┐  ┌────────────┐            │
│  │ ML/Scoring │  │   Rules    │            │
│  │  Engine    │  │  Engine    │            │
│  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │  │  Queue   │
│ (Events) │  │ (Cache & │  │(Celery / │
│          │  │Baselines)│  │  Redis)  │
└──────────┘  └──────────┘  └──────────┘
```

**Shared Infrastructure:**
- **API Gateway Pattern** — Each product exposes REST + WebSocket APIs
- **Event Streaming** — Products can publish security events to a shared Kafka/Redis Stream bus
- **Unified Dashboard** — Single-pane view across all products (future roadmap)
- **Containerized** — Every product ships with `docker-compose.yml` for one-command deployment

---

## 🛠️ Common Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI, Pydantic v2, Uvicorn |
| ML/AI | scikit-learn, PyTorch, ONNX Runtime |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| Cache | Redis 7 |
| Queue | Celery + Redis / RabbitMQ |
| Frontend | React 18, Vite, Recharts, Tailwind CSS |
| Testing | pytest, pytest-asyncio, httpx, locust |
| Deployment | Docker, Docker Compose, GitHub Actions |
| Observability | Prometheus, Grafana, structured logging |

---

## 🚀 Quick Start (Any Product)

```bash
# 1. Navigate to the product
cd ai-security-products/<product-name>

# 2. Start with Docker
docker-compose up -d

# 3. Verify health
curl http://localhost:8000/health

# 4. Open dashboard
open http://localhost:3000
```

Each product has its own detailed README with API docs, integration guides, and deployment instructions.

---

## 📊 Product Roadmap

### Phase 1 — Authentication & Access (Q2 2026)
- ✅ Risk-Based Authentication Engine

### Phase 2 — Perimeter Defense (Q3 2026)
- 🚧 AI-Powered Phishing Detection System
- 🚧 Adaptive Web Application Firewall (WAF)

### Phase 3 — Detection & Response (Q4 2026)
- 🚧 Intelligent SIEM Log Analyzer
- 🚧 Malware Behavior Classifier

### Phase 4 — Advanced Threats (Q1 2027)
- 🚧 Insider Threat Detection Engine
- 🚧 Vulnerability Prioritization AI

### Phase 5 — Unified Platform (Q2 2027)
- Centralized security dashboard across all products
- Cross-product threat correlation
- Single sign-on and unified alerting

---

## 🤝 Contributing

Each product is designed to be independently useful. If you want to:
- **Add a new product** — Propose it via issue with a problem statement and architecture sketch
- **Improve an existing product** — Check the product's README for specific contribution guidelines
- **Integrate with your stack** — Every product exposes OpenAPI docs at `/docs`

---

## 📄 License

All products in this suite are released under the **MIT License** — free for commercial and educational use.

---

Built with 💙 for defenders who refuse to play catch-up.
