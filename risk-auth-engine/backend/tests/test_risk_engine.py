"""Risk engine unit tests."""
import pytest
from datetime import datetime, timedelta
from app.core.risk_engine import RiskEngine
from app.core.geo import haversine_distance, calculate_geo_risk


class TestGeoUtils:
    def test_haversine_same_point(self):
        assert haversine_distance(40.7128, -74.0060, 40.7128, -74.0060) == 0.0
    
    def test_haversine_nyc_to_london(self):
        dist = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
        assert 5500 < dist < 5600  # ~5570 km
    
    def test_geo_risk_new_user(self):
        result = calculate_geo_risk(40.7128, -74.0060, [], 500)
        assert result["risk_score"] == 0.3
        assert result["factor"] == "new_location"
    
    def test_geo_risk_known_location(self):
        known = [{"lat": 40.7128, "lon": -74.0060, "city": "NYC"}]
        result = calculate_geo_risk(40.7130, -74.0062, known, 500)
        assert result["risk_score"] == 0.0
        assert result["factor"] == "known_location"
    
    def test_geo_risk_distant_location(self):
        known = [{"lat": 40.7128, "lon": -74.0060, "city": "NYC"}]
        result = calculate_geo_risk(51.5074, -0.1278, known, 500)
        assert result["risk_score"] > 0.5
        assert result["factor"] == "geo_anomaly"


class TestRiskEngine:
    @pytest.fixture
    def engine(self):
        return RiskEngine()
    
    @pytest.mark.asyncio
    async def test_low_risk_scenario(self, engine):
        """Simulate a user logging in from their usual setup."""
        result = await engine.assess_risk(
            user_id="regular_user",
            ip_address="192.168.1.10",
            device_fingerprint="trusted_device",
            location={"lat": 40.7128, "lon": -74.0060, "city": "NYC", "country": "US"},
            timestamp=datetime.utcnow().replace(hour=14, minute=0),
        )
        assert result["risk_level"] in ["LOW", "MEDIUM"]
        assert result["recommended_action"] in ["ALLOW", "MFA"]
    
    @pytest.mark.asyncio
    async def test_high_risk_scenario(self, engine):
        """Simulate suspicious login: new device, odd hours, distant location."""
        result = await engine.assess_risk(
            user_id="regular_user",
            ip_address="185.220.101.42",  # Suspicious IP
            device_fingerprint="unknown_device",
            location={"lat": 35.6762, "lon": 139.6503, "city": "Tokyo", "country": "JP"},
            timestamp=datetime.utcnow().replace(hour=3, minute=0),
        )
        # Should be elevated due to new device + off-hours + distant geo
        assert result["risk_score"] > 0.15
    
    def test_risk_decision_boundaries(self, engine):
        assert engine._get_risk_decision(0.1) == ("LOW", "ALLOW")
        assert engine._get_risk_decision(0.3) == ("MEDIUM", "MFA")
        assert engine._get_risk_decision(0.6) == ("HIGH", "REVIEW")
        assert engine._get_risk_decision(0.8) == ("CRITICAL", "BLOCK")
    
    def test_device_score_known(self, engine):
        result = engine._score_device("dev1", ["dev1", "dev2"])
        assert result["score"] == 0.0
    
    def test_device_score_new(self, engine):
        result = engine._score_device("dev3", ["dev1", "dev2"])
        assert result["score"] == 0.6
    
    def test_time_score_typical(self, engine):
        result = engine._score_time(
            datetime.utcnow().replace(hour=10),
            8, 18
        )
        assert result["score"] == 0.0
    
    def test_time_score_off_hours(self, engine):
        result = engine._score_time(
            datetime.utcnow().replace(hour=3),
            8, 18
        )
        assert result["score"] > 0.0
