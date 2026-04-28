"""Geolocation and IP reputation utilities for risk scoring."""
import math
import ipaddress
from typing import Optional, Dict, Any

# Known Tor exit nodes (sample subset — in production, fetch from https://check.torproject.org/exit-addresses)
_TOR_EXIT_NODES = {
    "185.220.101.0", "185.220.101.1", "185.220.101.2", "185.220.101.3",
    "185.220.101.4", "185.220.101.5", "185.220.101.6", "185.220.101.7",
    "185.220.101.8", "185.220.101.9", "185.220.101.10", "185.220.101.11",
    "185.220.101.12", "185.220.101.13", "185.220.101.14", "185.220.101.15",
    "185.220.101.16", "185.220.101.17", "185.220.101.18", "185.220.101.19",
    "185.220.101.20", "185.220.101.21", "185.220.101.22", "185.220.101.23",
    "185.220.101.24", "185.220.101.25", "185.220.101.26", "185.220.101.27",
    "185.220.101.28", "185.220.101.29", "185.220.101.30", "185.220.101.31",
    "185.220.101.32", "185.220.101.33", "185.220.101.34", "185.220.101.35",
    "185.220.101.36", "185.220.101.37", "185.220.101.38", "185.220.101.39",
    "185.220.101.40", "185.220.101.41", "185.220.101.42", "185.220.101.43",
    "185.220.101.44", "185.220.101.45", "185.220.101.46", "185.220.101.47",
    "185.220.101.48", "185.220.101.49", "185.220.101.50", "185.220.101.51",
    "185.220.101.52", "185.220.101.53", "185.220.101.54", "185.220.101.55",
    "185.220.101.56", "185.220.101.57", "185.220.101.58", "185.220.101.59",
    "185.220.101.60", "185.220.101.61", "185.220.101.62", "185.220.101.63",
    "185.220.101.64", "185.220.101.65", "185.220.101.66", "185.220.101.67",
    "185.220.101.68", "185.220.101.69", "185.220.101.70", "185.220.101.71",
    "185.220.101.72", "185.220.101.73", "185.220.101.74", "185.220.101.75",
    "185.220.101.76", "185.220.101.77", "185.220.101.78", "185.220.101.79",
    "185.220.101.80", "185.220.101.81", "185.220.101.82", "185.220.101.83",
    "185.220.101.84", "185.220.101.85", "185.220.101.86", "185.220.101.87",
    "185.220.101.88", "185.220.101.89", "185.220.101.90", "185.220.101.91",
    "185.220.101.92", "185.220.101.93", "185.220.101.94", "185.220.101.95",
    "185.220.101.96", "185.220.101.97", "185.220.101.98", "185.220.101.99",
    "185.220.101.100", "185.220.101.101", "185.220.101.102", "185.220.101.103",
    "185.220.101.104", "185.220.101.105", "185.220.101.106", "185.220.101.107",
    "185.220.101.108", "185.220.101.109", "185.220.101.110", "185.220.101.111",
    "185.220.101.112", "185.220.101.113", "185.220.101.114", "185.220.101.115",
    "185.220.101.116", "185.220.101.117", "185.220.101.118", "185.220.101.119",
    "185.220.101.120", "185.220.101.121", "185.220.101.122", "185.220.101.123",
    "185.220.101.124", "185.220.101.125", "185.220.101.126", "185.220.101.127",
    "185.220.101.128", "185.220.101.129", "185.220.101.130", "185.220.101.131",
    "185.220.101.132", "185.220.101.133", "185.220.101.134", "185.220.101.135",
    "185.220.101.136", "185.220.101.137", "185.220.101.138", "185.220.101.139",
    "185.220.101.140", "185.220.101.141", "185.220.101.142", "185.220.101.143",
    "185.220.101.144", "185.220.101.145", "185.220.101.146", "185.220.101.147",
    "185.220.101.148", "185.220.101.149", "185.220.101.150", "185.220.101.151",
    "185.220.101.152", "185.220.101.153", "185.220.101.154", "185.220.101.155",
    "185.220.101.156", "185.220.101.157", "185.220.101.158", "185.220.101.159",
    "185.220.101.160", "185.220.101.161", "185.220.101.162", "185.220.101.163",
    "185.220.101.164", "185.220.101.165", "185.220.101.166", "185.220.101.167",
    "185.220.101.168", "185.220.101.169", "185.220.101.170", "185.220.101.171",
    "185.220.101.172", "185.220.101.173", "185.220.101.174", "185.220.101.175",
    "185.220.101.176", "185.220.101.177", "185.220.101.178", "185.220.101.179",
    "185.220.101.180", "185.220.101.181", "185.220.101.182", "185.220.101.183",
    "185.220.101.184", "185.220.101.185", "185.220.101.186", "185.220.101.187",
    "185.220.101.188", "185.220.101.189", "185.220.101.190", "185.220.101.191",
    "185.220.101.192", "185.220.101.193", "185.220.101.194", "185.220.101.195",
    "185.220.101.196", "185.220.101.197", "185.220.101.198", "185.220.101.199",
    "185.220.101.200", "185.220.101.201", "185.220.101.202", "185.220.101.203",
    "185.220.101.204", "185.220.101.205", "185.220.101.206", "185.220.101.207",
    "185.220.101.208", "185.220.101.209", "185.220.101.210", "185.220.101.211",
    "185.220.101.212", "185.220.101.213", "185.220.101.214", "185.220.101.215",
    "185.220.101.216", "185.220.101.217", "185.220.101.218", "185.220.101.219",
    "185.220.101.220", "185.220.101.221", "185.220.101.222", "185.220.101.223",
    "185.220.101.224", "185.220.101.225", "185.220.101.226", "185.220.101.227",
    "185.220.101.228", "185.220.101.229", "185.220.101.230", "185.220.101.231",
    "185.220.101.232", "185.220.101.233", "185.220.101.234", "185.220.101.235",
    "185.220.101.236", "185.220.101.237", "185.220.101.238", "185.220.101.239",
    "185.220.101.240", "185.220.101.241", "185.220.101.242", "185.220.101.243",
    "185.220.101.244", "185.220.101.245", "185.220.101.246", "185.220.101.247",
    "185.220.101.248", "185.220.101.249", "185.220.101.250", "185.220.101.251",
    "185.220.101.252", "185.220.101.253", "185.220.101.254", "185.220.101.255",
    "45.128.232.0", "45.128.232.1", "45.128.232.2", "45.128.232.3",
    "95.214.52.0", "95.214.52.1", "95.214.52.2", "95.214.52.3",
    "104.244.72.0", "104.244.72.1", "104.244.72.2", "104.244.72.3",
    "107.189.0.0", "107.189.0.1", "107.189.0.2", "107.189.0.3",
}

# Known VPN / proxy / hosting provider ranges (commonly abused)
_SUSPICIOUS_NETWORKS = [
    ipaddress.ip_network("146.59.0.0/16"),   # OVH VPS
    ipaddress.ip_network("51.178.0.0/16"),   # OVH
    ipaddress.ip_network("198.245.0.0/16"),  # Hosting
]


def _is_in_networks(ip: ipaddress.IPv4Address, networks: list) -> bool:
    """Check if an IP address falls within any of the given networks."""
    for net in networks:
        try:
            if ip in net:
                return True
        except TypeError:
            continue
    return False


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
    """Check IP reputation using local threat intel heuristics.
    
    In production, integrate with AbuseIPDB, VirusTotal, or IPQualityScore APIs.
    """
    try:
        ip = ipaddress.ip_address(ip_address)
    except ValueError:
        # Invalid IP — treat as suspicious
        return {
            "is_private": False,
            "is_tor": False,
            "is_vpn": False,
            "is_proxy": False,
            "reputation_score": 0.5,
            "threat_intel_sources": ["invalid_ip_format"],
        }
    
    is_private = ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_multicast
    
    # Check against known Tor exit nodes
    is_tor = ip_address in _TOR_EXIT_NODES
    
    # Check against known suspicious hosting/VPN networks
    is_hosting = False
    if isinstance(ip, ipaddress.IPv4Address) and not is_private:
        is_hosting = _is_in_networks(ip, _SUSPICIOUS_NETWORKS)
    
    # Heuristic: treat hosting providers as potential proxy/VPN
    is_vpn = is_hosting
    is_proxy = is_hosting
    
    # Calculate reputation score
    reputation_score = 0.0
    if is_private:
        reputation_score = 0.0  # Private IPs are not inherently bad
    elif is_tor:
        reputation_score = 0.7  # Tor is high-risk for most auth flows
    elif is_vpn or is_proxy:
        reputation_score = 0.4  # VPN/proxy = elevated but not always malicious
    else:
        reputation_score = 0.1  # Public IP, no flags
    
    sources = []
    if is_tor:
        sources.append("tor_exit_node")
    if is_vpn:
        sources.append("known_vpn_range")
    if is_proxy:
        sources.append("known_proxy_range")
    if is_private:
        sources.append("private_range")
    
    return {
        "is_private": is_private,
        "is_tor": is_tor,
        "is_vpn": is_vpn,
        "is_proxy": is_proxy,
        "reputation_score": reputation_score,
        "threat_intel_sources": sources,
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
