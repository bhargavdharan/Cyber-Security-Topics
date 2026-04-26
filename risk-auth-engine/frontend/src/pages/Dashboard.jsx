import React, { useState, useEffect } from 'react';
import { getHealth } from '../services/api';

const Dashboard = () => {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const data = await getHealth();
      setHealth(data);
    } catch (err) {
      console.error('Health check failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      icon: 'bi-bolt',
      title: 'Real-Time Scoring',
      desc: 'Sub-100ms risk assessment for every authentication attempt',
    },
    {
      icon: 'bi-geo-alt',
      title: 'Geo Anomaly Detection',
      desc: 'Detect impossible travel and new location patterns',
    },
    {
      icon: 'bi-phone',
      title: 'Device Trust',
      desc: 'Build device reputation baselines per user',
    },
    {
      icon: 'bi-clock',
      title: 'Time Analysis',
      desc: 'Off-hours login detection with adaptive thresholds',
    },
    {
      icon: 'bi-speedometer2',
      title: 'Velocity Checks',
      desc: 'Detect brute-force and credential stuffing patterns',
    },
    {
      icon: 'bi-braces',
      title: 'API First',
      desc: 'RESTful API with auto-generated OpenAPI docs',
    },
  ];

  return (
    <div className="container py-5">
      <div className="text-center mb-5">
        <h2>Risk-Based Authentication Engine</h2>
        <p className="text-muted">Production-grade adaptive authentication for any organization</p>
      </div>

      {/* Status Card */}
      <div className="row justify-content-center mb-5">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body text-center">
              {loading ? (
                <div className="spinner-border text-primary" role="status"></div>
              ) : health ? (
                <>
                  <div className="mb-3">
                    <span className="badge bg-success fs-5">
                      <i className="bi bi-check-circle me-2"></i>API Online
                    </span>
                  </div>
                  <p className="mb-1"><strong>Service:</strong> {health.service}</p>
                  <p className="mb-1"><strong>Version:</strong> {health.version}</p>
                  <p className="mb-0"><strong>Uptime:</strong> {health.uptime_seconds}s</p>
                </>
              ) : (
                <div className="alert alert-warning mb-0">
                  <i className="bi bi-exclamation-triangle me-2"></i>
                  API unavailable. Make sure the backend is running.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* API Usage */}
      <div className="card mb-5">
        <div className="card-header bg-white">
          <h5 className="mb-0"><i className="bi bi-code-slash me-2"></i>API Usage</h5>
        </div>
        <div className="card-body">
          <pre className="api-response mb-0">
{`POST /risk/assess
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

→ Response:
{
  "risk_score": 0.23,
  "risk_level": "LOW",
  "recommended_action": "ALLOW",
  "factors": [...]
}`}
          </pre>
        </div>
      </div>

      {/* Features Grid */}
      <h4 className="mb-3">Key Features</h4>
      <div className="row g-4">
        {features.map((f, i) => (
          <div className="col-md-4" key={i}>
            <div className="card h-100">
              <div className="card-body">
                <i className={`bi ${f.icon} fs-2 text-primary mb-3`}></i>
                <h5>{f.title}</h5>
                <p className="text-muted mb-0">{f.desc}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Architecture */}
      <div className="mt-5">
        <h4 className="mb-3">Architecture</h4>
        <div className="card">
          <div className="card-body">
            <div className="row text-center">
              <div className="col-md-3">
                <div className="p-3 border rounded">
                  <i className="bi bi-globe fs-1 text-primary"></i>
                  <div className="mt-2 fw-bold">Login App</div>
                  <small className="text-muted">Your application</small>
                </div>
              </div>
              <div className="col-md-1 d-flex align-items-center justify-content-center">
                <i className="bi bi-arrow-right fs-3 text-muted"></i>
              </div>
              <div className="col-md-3">
                <div className="p-3 border rounded bg-primary text-white">
                  <i className="bi bi-shield-check fs-1"></i>
                  <div className="mt-2 fw-bold">Risk Engine API</div>
                  <small>FastAPI + Python</small>
                </div>
              </div>
              <div className="col-md-1 d-flex align-items-center justify-content-center">
                <i className="bi bi-arrow-right fs-3 text-muted"></i>
              </div>
              <div className="col-md-4">
                <div className="row g-2">
                  <div className="col-6">
                    <div className="p-2 border rounded">
                      <i className="bi bi-database fs-4 text-success"></i>
                      <div className="small fw-bold">PostgreSQL</div>
                    </div>
                  </div>
                  <div className="col-6">
                    <div className="p-2 border rounded">
                      <i className="bi bi-hdd-stack fs-4 text-danger"></i>
                      <div className="small fw-bold">Redis</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Deployment */}
      <div className="mt-5 mb-5">
        <h4 className="mb-3">Deploy in Minutes</h4>
        <div className="card">
          <div className="card-body">
            <pre className="api-response mb-0">
{`# Clone and start
git clone <repo>
cd risk-auth-engine

# Start everything
docker-compose up -d

# API available at http://localhost:8000
# Dashboard at http://localhost:3000
# Docs at http://localhost:8000/docs`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
