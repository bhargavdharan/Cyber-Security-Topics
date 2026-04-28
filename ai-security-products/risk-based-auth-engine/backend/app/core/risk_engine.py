"""Production risk scoring engine."""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from app.config import get_settings
from app.core.geo import calculate_geo_risk, get_ip_reputation
from app.db.redis_client import get_json, set_json, get_list_range

settings = get_settings()


class RiskEngine:
    """Real-time risk assessment engine for authentication events."""
    
    # Risk score thresholds
    LOW_THRESHOLD = 0.25
    MEDIUM_THRESHOLD = 0.50
    HIGH_THRESHOLD = 0.75
    
    def __init__(self):
        self.weights = {
            "device_trust": 0.20,
            "geo_anomaly": 0.25,
            "time_anomaly": 0.10,
            "ip_reputation": 0.15,
            "velocity": 0.15,
            "behavioral": 0.15,
        }
    
    async def assess_risk(
        self,
        user_id: str,
        ip_address: str,
        device_fingerprint: Optional[str],
        location: Optional[Dict[str, float]],
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Perform full risk assessment for an authentication attempt."""
        
        timestamp = timestamp or datetime.utcnow()
        
        # Load user's baseline from Redis (fallback to defaults)
        baseline = await get_json(f"baseline:{user_id}") or {
            "known_devices": [],
            "known_ips": [],
            "known_locations": [],
            "typical_login_hour_start": 8,
            "typical_login_hour_end": 18,
            "avg_login_frequency_per_day": 3.0,
        }
        
        factors = []
        
        # 1. Device Trust Score
        device_result = self._score_device(device_fingerprint, baseline.get("known_devices", []))
        factors.append({
            "factor": "device_trust",
            "weight": self.weights["device_trust"],
            "score": device_result["score"],
            "description": device_result["description"],
        })
        
        # 2. Geo Anomaly Score
        geo_result = {"score": 0.0, "description": "No location provided"}
        if location and location.get("lat") is not None and location.get("lon") is not None:
            geo_result = calculate_geo_risk(
                location["lat"], location["lon"],
                baseline.get("known_locations", []),
                settings.geo_anomaly_km_threshold,
            )
        factors.append({
            "factor": "geo_anomaly",
            "weight": self.weights["geo_anomaly"],
            "score": geo_result.get("risk_score", 0.0),
            "description": geo_result.get("description", "Location check skipped"),
        })
        
        # 3. Time Anomaly Score
        time_result = self._score_time(
            timestamp,
            baseline.get("typical_login_hour_start", 8),
            baseline.get("typical_login_hour_end", 18),
        )
        factors.append({
            "factor": "time_anomaly",
            "weight": self.weights["time_anomaly"],
            "score": time_result["score"],
            "description": time_result["description"],
        })
        
        # 4. IP Reputation Score
        ip_rep = get_ip_reputation(ip_address)
        ip_score = ip_rep["reputation_score"]
        if ip_address not in baseline.get("known_ips", []):
            ip_score += 0.1  # Slightly elevate for new IP
        factors.append({
            "factor": "ip_reputation",
            "weight": self.weights["ip_reputation"],
            "score": min(ip_score, 1.0),
            "description": f"IP {'known' if ip_address in baseline.get('known_ips', []) else 'new'} ({'private' if ip_rep['is_private'] else 'public'})",
        })
        
        # 5. Velocity Score (check recent login attempts)
        velocity_result = await self._score_velocity(user_id, timestamp)
        factors.append({
            "factor": "velocity",
            "weight": self.weights["velocity"],
            "score": velocity_result["score"],
            "description": velocity_result["description"],
        })
        
        # 6. Behavioral Score (pattern deviation)
        behavioral_result = await self._score_behavioral(user_id, baseline, timestamp)
        factors.append({
            "factor": "behavioral",
            "weight": self.weights["behavioral"],
            "score": behavioral_result["score"],
            "description": behavioral_result["description"],
        })
        
        # Calculate weighted total score
        total_score = sum(f["weight"] * f["score"] for f in factors)
        total_score = round(min(max(total_score, 0.0), 1.0), 3)
        
        # Determine risk level and action
        risk_level, recommended_action = self._get_risk_decision(total_score)
        
        return {
            "risk_score": total_score,
            "risk_level": risk_level,
            "recommended_action": recommended_action,
            "factors": [{"factor": f["factor"], "weight": f["weight"], "description": f["description"]} for f in factors],
            "raw_scores": {f["factor"]: f["score"] for f in factors},
        }
    
    def _score_device(self, device_fingerprint: Optional[str], known_devices: List[str]) -> Dict[str, Any]:
        """Score device trustworthiness."""
        if not device_fingerprint:
            return {"score": 0.5, "description": "No device fingerprint provided"}
        
        if device_fingerprint in known_devices:
            return {"score": 0.0, "description": "Known trusted device"}
        
        if len(known_devices) == 0:
            return {"score": 0.2, "description": "First device for this user"}
        
        return {"score": 0.6, "description": "New device not seen before"}
    
    def _score_time(
        self,
        timestamp: datetime,
        typical_start: int,
        typical_end: int,
    ) -> Dict[str, Any]:
        """Score time-of-day anomaly."""
        hour = timestamp.hour
        
        # Check if within typical hours
        if typical_start <= typical_end:
            is_typical = typical_start <= hour <= typical_end
        else:  # Handles overnight shifts (e.g., 22:00 - 06:00)
            is_typical = hour >= typical_start or hour <= typical_end
        
        if is_typical:
            return {"score": 0.0, "description": f"Login during typical hours ({typical_start}:00-{typical_end}:00)"}
        
        # Calculate distance from typical hours
        if typical_start <= typical_end:
            mid = (typical_start + typical_end) / 2
        else:
            mid = ((typical_start + typical_end + 24) / 2) % 24
        
        dist = min(abs(hour - mid), 24 - abs(hour - mid))
        score = min(dist / 12, 1.0) * 0.5  # Max 0.5 for time alone
        
        return {
            "score": score,
            "description": f"Off-hours login at {hour:02d}:00 (typical: {typical_start:02d}:00-{typical_end:02d}:00)",
        }
    
    async def _score_velocity(self, user_id: str, timestamp: datetime) -> Dict[str, Any]:
        """Score login velocity (too many attempts, impossible travel)."""
        # Get recent login events from Redis list
        recent_events = await get_list_range(f"events:{user_id}:recent", 0, 99)
        
        # Filter to last hour
        one_hour_ago = (timestamp - timedelta(hours=1)).isoformat()
        recent_count = sum(1 for e in recent_events if e.get("timestamp", "") > one_hour_ago)
        
        if recent_count == 0:
            return {"score": 0.0, "description": "Normal login frequency"}
        elif recent_count <= 3:
            return {"score": 0.1, "description": f"{recent_count} recent logins in last hour"}
        elif recent_count <= 10:
            return {"score": 0.4, "description": f"Elevated activity: {recent_count} logins in last hour"}
        else:
            return {"score": 0.9, "description": f"Suspicious velocity: {recent_count} logins in last hour"}
    
    async def _score_behavioral(self, user_id: str, baseline: Dict, timestamp: datetime) -> Dict[str, Any]:
        """Score behavioral pattern deviation."""
        # Check if user has established baseline
        has_baseline = (
            len(baseline.get("known_devices", [])) > 0 and
            len(baseline.get("known_locations", [])) > 0
        )
        
        if not has_baseline:
            return {"score": 0.2, "description": "Baseline still learning (new user)"}
        
        # Check for recent failures from Redis list
        recent_failures = await get_list_range(f"events:{user_id}:failures", 0, 99)
        one_hour_ago = (timestamp - timedelta(hours=1)).isoformat()
        failure_count = sum(1 for e in recent_failures if e.get("timestamp", "") > one_hour_ago)
        
        if failure_count >= 5:
            return {"score": 0.8, "description": f"Multiple recent failures ({failure_count} in last hour)"}
        elif failure_count >= 3:
            return {"score": 0.4, "description": f"Some recent failures ({failure_count} in last hour)"}
        
        return {"score": 0.0, "description": "Normal behavioral pattern"}
    
    def _get_risk_decision(self, score: float) -> tuple:
        """Map risk score to level and recommended action."""
        if score < self.LOW_THRESHOLD:
            return "LOW", "ALLOW"
        elif score < self.MEDIUM_THRESHOLD:
            return "MEDIUM", "MFA"
        elif score < self.HIGH_THRESHOLD:
            return "HIGH", "REVIEW"
        else:
            return "CRITICAL", "BLOCK"
    
    async def update_baseline(
        self,
        user_id: str,
        device_fingerprint: Optional[str],
        ip_address: str,
        location: Optional[Dict[str, Any]],
        success: bool,
    ) -> None:
        """Update user baseline after successful authentication."""
        baseline_key = f"baseline:{user_id}"
        baseline = await get_json(baseline_key) or {
            "known_devices": [],
            "known_ips": [],
            "known_locations": [],
            "typical_login_hour_start": 8,
            "typical_login_hour_end": 18,
            "avg_login_frequency_per_day": 3.0,
        }
        
        if success:
            # Add device if new
            if device_fingerprint and device_fingerprint not in baseline["known_devices"]:
                baseline["known_devices"].append(device_fingerprint)
                if len(baseline["known_devices"]) > 20:  # Keep last 20
                    baseline["known_devices"] = baseline["known_devices"][-20:]
            
            # Add IP if new
            if ip_address not in baseline["known_ips"]:
                baseline["known_ips"].append(ip_address)
                if len(baseline["known_ips"]) > 50:
                    baseline["known_ips"] = baseline["known_ips"][-50:]
            
            # Add location if new and valid
            if location and location.get("lat") and location.get("lon"):
                loc_entry = {
                    "lat": location["lat"],
                    "lon": location["lon"],
                    "city": location.get("city", "Unknown"),
                    "country": location.get("country", "Unknown"),
                    "timestamp": datetime.utcnow().isoformat(),
                }
                # Check if too close to existing
                is_new = True
                for existing in baseline["known_locations"]:
                    from app.core.geo import haversine_distance
                    dist = haversine_distance(
                        loc_entry["lat"], loc_entry["lon"],
                        existing["lat"], existing["lon"]
                    )
                    if dist < 10:  # Within 10km, update existing
                        existing.update(loc_entry)
                        is_new = False
                        break
                
                if is_new:
                    baseline["known_locations"].append(loc_entry)
                    if len(baseline["known_locations"]) > 10:
                        baseline["known_locations"] = baseline["known_locations"][-10:]
        
        await set_json(baseline_key, baseline, ttl=settings.redis_ttl_seconds)
