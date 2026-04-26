import React, { useState } from 'react';
import { assessRisk } from '../services/api';

const RiskTester = () => {
  const [formData, setFormData] = useState({
    user_id: 'demo_user_001',
    ip_address: '192.168.1.100',
    device_fingerprint: 'chrome_windows_trusted',
    location: { lat: 40.7128, lon: -74.0060, city: 'New York', country: 'US' },
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await assessRisk(formData);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Assessment failed');
    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (level) => {
    switch (level) {
      case 'LOW': return 'risk-low';
      case 'MEDIUM': return 'risk-medium';
      case 'HIGH': return 'risk-high';
      case 'CRITICAL': return 'risk-critical';
      default: return 'risk-low';
    }
  };

  const getActionBadge = (action) => {
    switch (action) {
      case 'ALLOW': return 'bg-success';
      case 'MFA': return 'bg-warning text-dark';
      case 'REVIEW': return 'bg-info text-dark';
      case 'BLOCK': return 'bg-danger';
      default: return 'bg-secondary';
    }
  };

  const presets = {
    safe: {
      user_id: 'regular_user',
      ip_address: '192.168.1.10',
      device_fingerprint: 'trusted_device_001',
      location: { lat: 40.7128, lon: -74.0060, city: 'New York', country: 'US' },
    },
    suspicious: {
      user_id: 'regular_user',
      ip_address: '185.220.101.42',
      device_fingerprint: 'unknown_device_xyz',
      location: { lat: 35.6762, lon: 139.6503, city: 'Tokyo', country: 'JP' },
    },
    new_user: {
      user_id: 'brand_new_user_999',
      ip_address: '203.0.113.50',
      device_fingerprint: 'new_device_abc',
      location: { lat: 51.5074, lon: -0.1278, city: 'London', country: 'UK' },
    },
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="text-center mb-5">
            <h2><i className="bi bi-shield-check me-2 text-primary"></i>Risk Assessment Tester</h2>
            <p className="text-muted">Simulate authentication attempts and see real-time risk scoring</p>
          </div>

          {/* Preset Buttons */}
          <div className="d-flex justify-content-center gap-2 mb-4">
            <button className="btn btn-outline-success" onClick={() => setFormData(presets.safe)}>
              <i className="bi bi-check-circle me-1"></i>Safe Login
            </button>
            <button className="btn btn-outline-warning" onClick={() => setFormData(presets.suspicious)}>
              <i className="bi bi-exclamation-triangle me-1"></i>Suspicious Login
            </button>
            <button className="btn btn-outline-info" onClick={() => setFormData(presets.new_user)}>
              <i className="bi bi-person-plus me-1"></i>New User
            </button>
          </div>

          {/* Form */}
          <div className="card shadow-sm">
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">User ID</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.user_id}
                      onChange={(e) => setFormData({...formData, user_id: e.target.value})}
                      required
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">IP Address</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.ip_address}
                      onChange={(e) => setFormData({...formData, ip_address: e.target.value})}
                      required
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label">Device Fingerprint</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.device_fingerprint}
                      onChange={(e) => setFormData({...formData, device_fingerprint: e.target.value})}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Latitude</label>
                    <input
                      type="number"
                      step="any"
                      className="form-control"
                      value={formData.location.lat}
                      onChange={(e) => setFormData({...formData, location: {...formData.location, lat: parseFloat(e.target.value)}})}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Longitude</label>
                    <input
                      type="number"
                      step="any"
                      className="form-control"
                      value={formData.location.lon}
                      onChange={(e) => setFormData({...formData, location: {...formData.location, lon: parseFloat(e.target.value)}})}
                    />
                  </div>
                </div>
                <div className="mt-4 d-grid">
                  <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                    {loading ? (
                      <><span className="spinner-border spinner-border-sm me-2"></span>Assessing...</>
                    ) : (
                      <><i className="bi bi-play-fill me-2"></i>Run Risk Assessment</>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="alert alert-danger mt-4">{error}</div>
          )}

          {/* Results */}
          {result && (
            <div className="mt-4">
              <div className="card shadow">
                <div className="card-header bg-white">
                  <h5 className="mb-0">Assessment Result</h5>
                </div>
                <div className="card-body">
                  <div className="row align-items-center">
                    <div className="col-md-4 text-center">
                      <div className={`risk-score-circle ${getRiskClass(result.risk_level)}`}>
                        {(result.risk_score * 100).toFixed(0)}
                      </div>
                      <div className="mt-2">
                        <span className={`badge ${getActionBadge(result.recommended_action)} fs-6`}>
                          {result.risk_level} — {result.recommended_action}
                        </span>
                      </div>
                    </div>
                    <div className="col-md-8">
                      <h6>Risk Factors</h6>
                      <div className="row g-2">
                        {result.factors.map((f, i) => (
                          <div className="col-6" key={i}>
                            <div className="card factor-card">
                              <div className="card-body p-2">
                                <div className="d-flex justify-content-between">
                                  <small className="fw-bold text-capitalize">{f.factor.replace('_', ' ')}</small>
                                  <small className="text-muted">{(f.weight * 100).toFixed(0)}%</small>
                                </div>
                                <small className="text-muted">{f.description}</small>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Raw JSON */}
                  <div className="mt-4">
                    <h6>Raw Response</h6>
                    <pre className="api-response">{JSON.stringify(result, null, 2)}</pre>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RiskTester;
