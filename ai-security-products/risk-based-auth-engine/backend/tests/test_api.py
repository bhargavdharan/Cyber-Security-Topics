"""API endpoint tests."""
import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Risk-Based Authentication Engine"


@pytest.mark.asyncio
async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "endpoints" in data


@pytest.mark.asyncio
async def test_risk_assessment_low_risk(client):
    """Test risk assessment for a known, safe login scenario."""
    payload = {
        "user_id": "test_user_001",
        "ip_address": "192.168.1.100",
        "device_fingerprint": "device_abc123",
        "location": {"lat": 40.7128, "lon": -74.0060, "city": "New York", "country": "US"},
    }
    response = await client.post("/risk/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_score" in data
    assert "risk_level" in data
    assert "recommended_action" in data
    assert "factors" in data
    assert 0.0 <= data["risk_score"] <= 1.0
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert data["recommended_action"] in ["ALLOW", "MFA", "BLOCK", "REVIEW"]
    assert isinstance(data["factors"], list)
    assert len(data["factors"]) == 6  # All 6 risk factors


@pytest.mark.asyncio
async def test_risk_assessment_new_user(client):
    """Test that new users get a slightly elevated but not critical score."""
    payload = {
        "user_id": "brand_new_user_999",
        "ip_address": "203.0.113.50",
        "device_fingerprint": "new_device_xyz",
        "location": {"lat": 51.5074, "lon": -0.1278, "city": "London", "country": "UK"},
    }
    response = await client.post("/risk/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # New user should be MEDIUM or below, not CRITICAL
    assert data["risk_level"] in ["LOW", "MEDIUM"]
    assert data["risk_score"] < 0.75


@pytest.mark.asyncio
async def test_risk_assessment_missing_fields(client):
    """Test validation of required fields."""
    payload = {
        "user_id": "",  # Empty user_id should fail
        "ip_address": "192.168.1.1",
    }
    response = await client.post("/risk/assess", json=payload)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_user_risk_history_empty(client):
    """Test history endpoint for user with no history."""
    response = await client.get("/risk/user/nonexistent_user/history")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "nonexistent_user"
    assert data["count"] == 0
    assert data["assessments"] == []


@pytest.mark.asyncio
async def test_user_baseline_not_found(client):
    """Test baseline endpoint for non-existent user."""
    response = await client.get("/risk/user/nonexistent_user/baseline")
    assert response.status_code == 404
