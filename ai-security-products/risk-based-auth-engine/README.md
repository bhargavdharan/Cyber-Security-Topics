# Risk-Based Authentication Engine

A production-grade, real-time risk scoring engine for adaptive authentication. Protects any application from account takeovers, credential stuffing, and anomalous login behavior — without adding friction for legitimate users.

---

## 📋 Problem Statement

Traditional authentication is binary: username + password → allow or deny. This model is broken because:

- **81% of breaches** involve stolen or weak passwords (Verizon DBIR)
- **Credential stuffing** attacks use millions of leaked credentials automatically
- **Account takeovers** cost enterprises billions in fraud, support, and reputation damage
- **Static MFA** annoys users on every login, leading to fatigue and bypass
- **Legitimate users** traveling, using new devices, or working odd hours get falsely blocked

**The core problem:** How do you distinguish a hacker with stolen credentials from a real user on a new device?

---

## 🎯 Why Use This Project

This engine solves the problem by analyzing **context, not just credentials**. Every login is scored on multiple risk dimensions in real time. You get:

| Benefit | What It Means |
|---------|---------------|
| **Frictionless UX** | Low-risk users log in seamlessly — no unnecessary MFA prompts |
| **Intelligent MFA** | Step-up authentication only when risk is elevated |
| **Fraud Prevention** | Block account takeovers, bots, and credential stuffing before damage occurs |
| **Zero-Trust Login** | Continuously verify trust based on behavior, not just a one-time password |
| **Fast Integration** | Drop-in REST API — works with any auth system (Auth0, Cognito, Keycloak, custom) |

### Who Is This For

- **SaaS platforms** protecting customer accounts
- **FinTech / Banking apps** meeting compliance (PSD2, FFIEC)
- **Enterprise IT** securing internal applications
- **E-commerce** preventing account takeover and fraud
- **Developers** building auth systems who want enterprise-grade risk detection

---

## ✨ Features

### 6-Factor Risk Scoring
Every login is analyzed across six independent risk dimensions:

| Factor | Detects | Weight |
|--------|---------|--------|
| **Device Trust** | New devices, emulators, fingerprint spoofing, browser anomalies | 20% |
| **Geo Anomaly** | Impossible travel, new countries/cities, high-risk regions | 25% |
| **Time Analysis** | Off-hours logins, unusual session timing, holiday access | 10% |
| **IP Reputation** | VPNs, proxies, Tor exit nodes, known malicious IPs | 15% |
| **Velocity** | Brute-force bursts, enumeration attacks, rapid retry patterns | 15% |
| **Behavioral Baseline** | Deviations from the user's established login patterns | 15% |

### Adaptive Decision Engine
Risk scores map to concrete actions — no guesswork:

| Score | Level | Action | Example Scenario |
|-------|-------|--------|-----------------|
| 0.00–0.25 | **LOW** | `ALLOW` | Normal login from known laptop at home |
| 0.25–0.50 | **MEDIUM** | `MFA` | New phone, same city, daytime — prompt for 2FA |
| 0.50–0.75 | **HIGH** | `REVIEW` | New country + VPN + off-hours — flag for admin review |
| 0.75–1.00 | **CRITICAL** | `BLOCK` | Impossible travel, Tor, brute-force pattern — block immediately |

### User Baseline Learning
- Automatically builds a behavioral profile per user over **14 days**
- Stores known devices, locations, and time patterns in **Redis**
- Adapts thresholds dynamically — what is "anomalous" varies by user

### Real-Time Dashboard
- React-based admin dashboard at `http://localhost:3000`
- Live risk score visualization with Recharts
- Per-user assessment history and baseline inspection
- Health monitoring for API, database, and cache layers

### Production-Ready Infrastructure
- **Async FastAPI** backend with PostgreSQL + SQLAlchemy async
- **Redis** caching for sub-millisecond baseline lookups
- **Docker Compose** for one-command deployment
- **GitHub Actions CI/CD** with 19+ automated tests
- **OpenAPI/Swagger** docs auto-generated at `/docs`
- **Rate limiting** built-in via SlowAPI

---

## 🏗️ Architecture

```
┌─────────────┐      POST /risk/assess      ┌─────────────────────┐
│  Your App   │  ─────────────────────────→  │  FastAPI Backend    │
│  (Any)      │  ← risk_score + action       │  (Python 3.12+)     │
└─────────────┘                              └─────────────────────┘
                                                      │
                        ┌─────────────┬──────────────┘
                        ▼             ▼
                ┌──────────┐  ┌──────────┐
                │PostgreSQL│  │  Redis   │
                │ (Logs)   │  │(Baselines│
                └──────────┘  │  & Cache)│
                              └──────────┘
                                     │
                                     ▼
                        ┌─────────────────────┐
                        │  React Dashboard    │
                        │  (Port 3000)        │
                        └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI, Pydantic v2, Uvicorn |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 (async) |
| Cache | Redis 7 |
| ML/Scoring | Custom rule engine + statistical anomaly detection |
| Frontend | React 18, Vite, Recharts, Axios |
| Testing | pytest, pytest-asyncio, httpx |
| Deployment | Docker, Docker Compose, GitHub Actions |

---

## ⚡ How to Use

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- OR: Python 3.12+ + PostgreSQL + Redis (for local dev)

### Option 1: Docker (Recommended — 2 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/bhargavdharan/Cyber-Security-Topics.git
cd Cyber-Security-Topics/ai-security-products/risk-based-auth-engine

# 2. Start all services (API + DB + Redis + Dashboard)
docker-compose up -d

# 3. Verify health
curl http://localhost:8000/health
curl http://localhost:8000/health/ready

# 4. Open the dashboard
open http://localhost:3000        # macOS
start http://localhost:3000       # Windows
```

Services will be available at:
- **API:** `http://localhost:8000`
- **Dashboard:** `http://localhost:3000`
- **API Docs:** `http://localhost:8000/docs`
- **PostgreSQL:** `localhost:5432`
- **Redis:** `localhost:6379`

### Option 2: Local Development

```bash
# 1. Backend setup
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env        # Windows
cp .env.example .env          # macOS/Linux
# Edit .env with your local DB and Redis URLs

# 3. Start PostgreSQL and Redis locally, then run the API
uvicorn app.main:app --reload --port 8000

# 4. Frontend setup (in a new terminal)
cd ../frontend
npm install
npm run dev
```

---

## 📡 API Usage

### Assess Login Risk

```bash
curl -X POST http://localhost:8000/risk/assess \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "ip_address": "203.0.113.45",
    "device_fingerprint": "abc123...",
    "location": {
      "lat": 40.7128,
      "lon": -74.0060,
      "city": "New York",
      "country": "US"
    }
  }'
```

**Response:**
```json
{
  "risk_score": 0.23,
  "risk_level": "LOW",
  "recommended_action": "ALLOW",
  "factors": [
    {
      "factor": "device_trust",
      "weight": 0.20,
      "score": 0.0,
      "description": "Known trusted device"
    },
    {
      "factor": "geo_anomaly",
      "weight": 0.25,
      "score": 0.0,
      "description": "Login 0 km from known location (New York)"
    }
  ],
  "raw_scores": {
    "device_trust": 0.0,
    "geo_anomaly": 0.0,
    "time_anomaly": 0.0,
    "ip_reputation": 0.1,
    "velocity": 0.0,
    "behavioral": 0.0
  }
}
```

### All Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health check |
| `/health/ready` | GET | Database + Redis connectivity |
| `/risk/assess` | POST | Score a login attempt |
| `/risk/evaluate-and-update` | POST | Score + update user baseline |
| `/risk/user/{id}/history` | GET | User's assessment history |
| `/risk/user/{id}/baseline` | GET | User's current baseline profile |

Full interactive API documentation: `http://localhost:8000/docs`

---

## 🔌 Integrating With Your Application

```python
import requests

def authenticate_user(username, password, request_context):
    # Step 1: Verify credentials
    if not verify_password(username, password):
        return {"error": "Invalid credentials"}

    # Step 2: Get real-time risk score
    risk_response = requests.post(
        "http://localhost:8000/risk/assess",
        json={
            "user_id": username,
            "ip_address": request_context.ip,
            "device_fingerprint": request_context.device_fp,
            "location": request_context.geo,
        },
        timeout=2
    )
    risk = risk_response.json()

    # Step 3: Enforce risk-aware policy
    action = risk["recommended_action"]

    if action == "BLOCK":
        log_suspicious(username, risk)
        return {"error": "Access denied", "risk_level": risk["risk_level"]}

    elif action == "MFA":
        return {"mfa_required": True, "risk_score": risk["risk_score"]}

    elif action == "REVIEW":
        flag_for_admin_review(username, risk)
        return {"token": generate_jwt(username), "risk": risk, "review_flag": True}

    # ALLOW — proceed normally
    return {"token": generate_jwt(username), "risk": risk}
```

---

## 🧪 Running Tests

```bash
cd backend

# Run all tests
pytest -v

# With coverage report
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_risk_engine.py -v
```

The test suite includes:
- Risk engine scoring logic (19+ test cases)
- API endpoint validation
- Database and Redis connectivity
- Edge cases (impossible travel, new users, Tor IPs)

---

## 🔒 Security Best Practices

- **Never** use the default `SECRET_KEY` in production
- Run behind a reverse proxy (Nginx, Traefik, AWS ALB) with TLS/HTTPS
- Rotate database and Redis credentials regularly
- Integrate with real threat intel feeds (AbuseIPDB, VirusTotal, MaxMind GeoIP)
- Enable rate limiting per user/IP (built-in, configurable via `.env`)
- Store baselines in Redis with persistence (AOF or RDB snapshots)

---

## 🚢 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to a cryptographically secure random string (≥32 bytes)
- [ ] Set `DEBUG=false` and `ENVIRONMENT=production`
- [ ] Configure PostgreSQL with SSL and restricted network access
- [ ] Enable Redis persistence (AOF or RDB)
- [ ] Add monitoring (Prometheus/Grafana) and alerting
- [ ] Configure centralized logging (ELK, Datadog, Splunk)
- [ ] Set up automated PostgreSQL backups
- [ ] Use a secrets manager (AWS Secrets Manager, Vault, Doppler)

### Cloud Platforms

| Platform | Stack |
|----------|-------|
| **AWS** | ECS Fargate + RDS PostgreSQL + ElastiCache Redis + ALB |
| **GCP** | Cloud Run + Cloud SQL + Memorystore + Cloud Load Balancing |
| **Azure** | Container Apps + Azure Database + Azure Cache + Front Door |
| **Railway / Render / Fly.io** | One-click deploy with `docker-compose.yml` |

---

## 📄 License

MIT License — Free for commercial and educational use.

---

Built with 💙 for the cybersecurity community.
