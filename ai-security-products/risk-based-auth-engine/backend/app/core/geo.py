"""Geolocation utilities for risk scoring."""
import math
from typing import Optional, Dict, Any


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in kilometers between two coordinates."""
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_ip_reputation(ip_address: str) -> Dict[str, Any]:
    """Check IP reputation (simplified - integrate with AbuseIPDB, VirusTotal, etc.)."""
    # TODO: Integrate with real threat intel APIs
    # For now, check common private/reserved ranges
    private_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255"),
        ("127.0.0.0", "127.255.255.255"),
    ]
    
    is_private = False
    # Simplified check - in production use ipaddress module
    if ip_address.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.",
                               "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                               "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                               "172.30.", "172.31.", "192.168.", "127.")):
        is_private = True
    
    return {
        "is_private": is_private,
        "is_tor": False,  # TODO: Check Tor exit nodes
        "is_vpn": False,   # TODO: Check VPN IP ranges
        "is_proxy": False, # TODO: Check proxy lists
        "reputation_score": 0.0 if is_private else 0.1,  # Neutral by default
        "threat_intel_sources": [],
    }


def calculate_geo_risk(
    current_lat: float,
    current_lon: float,
    known_locations: list,
    threshold_km: int = 500
) -> Dict[str, Any]:
    """Calculate geo anomaly risk based on distance from known locations."""
    if not known_locations:
        return {
            "risk_score": 0.3,  # Slightly elevated for first-time location
            "factor": "new_location",
            "description": "No baseline locations established yet",
            "distance_km": None,
        }
    
    min_distance = float('inf')
    closest_location = None
    
    for loc in known_locations:
        dist = haversine_distance(
            current_lat, current_lon,
            loc.get("lat", 0), loc.get("lon", 0)
        )
        if dist < min_distance:
            min_distance = dist
            closest_location = loc
    
    # Risk increases with distance
    if min_distance < 50:
        risk_score = 0.0
        factor = "known_location"
    elif min_distance < threshold_km:
        risk_score = min(min_distance / threshold_km * 0.5, 0.5)
        factor = "distant_location"
    else:
        risk_score = min(0.3 + (min_distance - threshold_km) / 1000, 0.9)
        factor = "geo_anomaly"
    
    return {
        "risk_score": risk_score,
        "factor": factor,
        "description": f"Login {min_distance:.0f} km from known location ({closest_location.get('city', 'Unknown')})",
        "distance_km": round(min_distance, 1),
    }
