# Risk-Based Authentication Engine

A production-grade, real-time risk scoring engine for adaptive authentication. Protects any application from account takeovers, credential stuffing, and anomalous login behavior.

## 🚀 What It Does

Every time a user tries to log in, this engine analyzes:

| Factor | What It Detects |
|--------|----------------|
| **Device Trust** | New devices, emulators, fingerprint changes |
| **Geo Anomaly** | Impossible travel, new cities/countries |
| **Time Analysis** | Off-hours logins, unusual patterns |
| **IP Reputation** | VPNs, proxies, Tor, known bad IPs |
| **Velocity** | Too many attempts, brute-force patterns |
| **Behavioral** | Deviations from established baseline |

**Output:** A risk score (0.0–1.0), risk level (LOW/MEDIUM/HIGH/CRITICAL), and recommended action (ALLOW / MFA / REVIEW / BLOCK).

---

## 🏗️ Architecture

```
┌─────────────┐      POST /risk/assess      ┌─────────────────────┐
│  Your App   │  ─────────────────────────→  │  FastAPI Backend    │
│  (Any)      │  ← risk_score + action       │  (Python 3.12)      │
└─────────────┘                              └─────────────────────┘
                                                      │
                        ┌─────────────┬──────────────┘
                        ▼             ▼
                ┌──────────┐  ┌──────────┐
                │ PostgreSQL│  │  Redis   │
                │ (Logs)   │  │(Baselines│
                └──────────┘  │  & Cache)│
                              └──────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI, Pydantic, Uvicorn |
| Database | PostgreSQL + SQLAlchemy Async |
| Cache | Redis |
| ML/Scoring | Custom rule engine + anomaly detection |
| Frontend | React 18, Vite, Recharts |
| Deployment | Docker, Docker Compose, GitHub Actions |

---

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- OR: Python 3.12 + PostgreSQL + Redis

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/bhargavdharan/Cyber-Security-Topics.git
cd Cyber-Security-Topics/risk-auth-engine

# Start everything
docker-compose up -d

# Check health
curl http://localhost:8000/health

# Open dashboard
open http://localhost:3000
```

### Option 2: Local Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your DB and Redis URLs

# Run database migrations (auto-created on startup)
# Start the API
uvicorn app.main:app --reload --port 8000

# In another terminal, start frontend
cd ../frontend
npm install
npm run dev
```

---

## 📡 API Endpoints

### Assess Risk
```bash
POST /risk/assess
Content-Type: application/json

{
  "user_id": "user_123",
  "ip_address": "203.0.113.45",
  "device_fingerprint": "abc123...",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "city": "New York",
    "country": "US"
  }
}
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
      "description": "Known trusted device"
    },
    {
      "factor": "geo_anomaly",
      "weight": 0.25,
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

### Other Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health |
| `/health/ready` | GET | DB + Redis connectivity |
| `/risk/assess` | POST | Score a login attempt |
| `/risk/evaluate-and-update` | POST | Score + update baseline |
| `/risk/user/{id}/history` | GET | User's assessment history |
| `/risk/user/{id}/baseline` | GET | User's current baseline |

Full OpenAPI docs at `http://localhost:8000/docs`

---

## 🧪 Running Tests

```bash
cd backend
pytest -v

# With coverage
pytest --cov=app --cov-report=html
```

---

## 🔒 Security Considerations

- **Never** use the default `SECRET_KEY` in production
- Run behind a reverse proxy (Nginx, Traefik, AWS ALB)
- Use TLS/HTTPS for all traffic
- Rotate Redis and DB credentials regularly
- Integrate with real threat intel feeds (AbuseIPDB, VirusTotal)
- Add rate limiting per user/IP (built-in with SlowAPI)

---

## 🚢 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to a cryptographically secure random string
- [ ] Set `DEBUG=false` and `ENVIRONMENT=production`
- [ ] Configure PostgreSQL with SSL
- [ ] Set up Redis persistence (AOF or RDB)
- [ ] Add monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation
- [ ] Set up backup strategy for PostgreSQL

### Cloud Platforms

**AWS:** ECS Fargate + RDS PostgreSQL + ElastiCache Redis + ALB
**GCP:** Cloud Run + Cloud SQL + Memorystore + Cloud Load Balancing
**Azure:** Container Apps + Azure Database + Azure Cache + Front Door
**Railway/Render/Fly.io:** One-click deploy with `docker-compose.yml`

---

## 📊 Risk Score Thresholds

| Score | Level | Action | Use Case |
|-------|-------|--------|----------|
| 0.00–0.25 | LOW | ALLOW | Normal login from known device/location |
| 0.25–0.50 | MEDIUM | MFA | New device, slightly off-hours, new city |
| 0.50–0.75 | HIGH | REVIEW | Multiple anomalies, possible compromise |
| 0.75–1.00 | CRITICAL | BLOCK | Confirmed attack pattern, impossible travel |

---

## 🤝 Integrating With Your App

```python
import requests

def authenticate_user(username, password, request_context):
    # Step 1: Check credentials
    if not verify_password(username, password):
        return {"error": "Invalid credentials"}
    
    # Step 2: Get risk score
    risk_response = requests.post("http://risk-engine:8000/risk/assess", json={
        "user_id": username,
        "ip_address": request_context.ip,
        "device_fingerprint": request_context.device_fp,
        "location": request_context.geo,
    })
    
    risk = risk_response.json()
    
    # Step 3: Enforce policy
    if risk["recommended_action"] == "BLOCK":
        log_suspicious(username, risk)
        return {"error": "Access denied", "risk_level": risk["risk_level"]}
    
    elif risk["recommended_action"] == "MFA":
        return {"mfa_required": True, "risk_score": risk["risk_score"]}
    
    # ALLOW or REVIEW → proceed
    return {"token": generate_jwt(username), "risk": risk}
```

---

## 📄 License

MIT License — Free for commercial and educational use.

---

Built with 💙 for the cybersecurity community.
