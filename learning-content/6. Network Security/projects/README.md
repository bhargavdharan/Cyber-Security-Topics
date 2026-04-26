# Projects: Network Security

Hands-on simulations and tools for understanding network security concepts.

---

## Projects Included

### 1. Firewall Rule Simulator (`firewall_simulator.py`)
Simulates a packet-filtering firewall where you can:
- Define allow/deny rules based on source/dest IP, port, and protocol
- Test packets against your rule set
- Understand rule ordering and default policies

**How to run:**
```bash
python firewall_simulator.py
```

### 2. IDS Alert Simulator (`ids_simulator.py`)
Simulates an Intrusion Detection System that:
- Analyzes network traffic for suspicious patterns
- Detects port scans, brute force attempts, and malware C2 traffic
- Generates alerts with severity levels

**How to run:**
```bash
python ids_simulator.py
```

### 3. VPN Tunnel Simulator (`vpn_tunnel_sim.py`)
Demonstrates the concept of VPN encryption:
- Simulates plaintext vs encrypted tunnel traffic
- Shows how packets are encapsulated
- Demonstrates key exchange concepts

**How to run:**
```bash
python vpn_tunnel_sim.py
```

---

## Learning Objectives

- Understand how firewall rules are evaluated
- Learn to recognize suspicious network patterns
- Grasp VPN encapsulation and encryption concepts

## Requirements

- Python 3.x (standard library only)
