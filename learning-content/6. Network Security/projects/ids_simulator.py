#!/usr/bin/env python3
"""
IDS Alert Simulator
Demonstrates how Intrusion Detection Systems analyze traffic for threats.
"""

import random
from datetime import datetime, timedelta


class IDSSimulator:
    """Simulates a network-based intrusion detection system."""

    def __init__(self):
        self.signatures = [
            {
                "name": "Port Scan Detected",
                "description": "Multiple ports accessed from single source",
                "severity": "MEDIUM",
                "check": self.detect_port_scan,
            },
            {
                "name": "Brute Force Login",
                "description": "Multiple failed login attempts",
                "severity": "HIGH",
                "check": self.detect_brute_force,
            },
            {
                "name": "Suspected C2 Beacon",
                "description": "Regular connections to known suspicious IP",
                "severity": "HIGH",
                "check": self.detect_c2_beacon,
            },
            {
                "name": "Large Data Transfer",
                "description": "Unusually large outbound data transfer",
                "severity": "MEDIUM",
                "check": self.detect_data_exfil,
            },
            {
                "name": "Telnet Cleartext Protocol",
                "description": "Insecure Telnet connection detected",
                "severity": "LOW",
                "check": self.detect_telnet,
            },
        ]
        self.alerts = []

    def analyze_traffic(self, connection_log):
        """Analyze a connection log for threats."""
        for sig in self.signatures:
            if sig["check"](connection_log):
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "name": sig["name"],
                    "description": sig["description"],
                    "severity": sig["severity"],
                    "source": connection_log.get("src_ip", "unknown"),
                    "target": connection_log.get("dst_ip", "unknown"),
                }
                self.alerts.append(alert)
                return alert
        return None

    def detect_port_scan(self, log):
        """Detect if a source IP hit many different ports."""
        return len(log.get("ports_accessed", [])) >= 10

    def detect_brute_force(self, log):
        """Detect multiple failed login attempts."""
        return log.get("failed_logins", 0) >= 5

    def detect_c2_beacon(self, log):
        """Detect regular connections to suspicious IP."""
        return log.get("suspicious_ip", False) and log.get("connection_count", 0) >= 20

    def detect_data_exfil(self, log):
        """Detect large data transfers."""
        return log.get("bytes_outbound", 0) > 1_000_000_000  # 1 GB

    def detect_telnet(self, log):
        """Detect Telnet connections."""
        return 23 in log.get("ports_accessed", [])

    def generate_suspicious_traffic(self):
        """Generate simulated suspicious traffic patterns."""
        scenarios = [
            {
                "type": "Port Scan",
                "src_ip": "203.0.113.50",
                "dst_ip": "192.168.1.10",
                "ports_accessed": list(range(20, 85)),
                "failed_logins": 0,
                "suspicious_ip": False,
                "connection_count": 1,
                "bytes_outbound": 5000,
            },
            {
                "type": "Brute Force",
                "src_ip": "198.51.100.25",
                "dst_ip": "192.168.1.5",
                "ports_accessed": [22],
                "failed_logins": 15,
                "suspicious_ip": False,
                "connection_count": 15,
                "bytes_outbound": 2000,
            },
            {
                "type": "C2 Beacon",
                "src_ip": "192.168.1.100",
                "dst_ip": "185.220.101.42",
                "ports_accessed": [4444, 8080],
                "failed_logins": 0,
                "suspicious_ip": True,
                "connection_count": 50,
                "bytes_outbound": 500_000,
            },
            {
                "type": "Data Exfiltration",
                "src_ip": "192.168.1.50",
                "dst_ip": "203.0.113.80",
                "ports_accessed": [443],
                "failed_logins": 0,
                "suspicious_ip": False,
                "connection_count": 5,
                "bytes_outbound": 5_000_000_000,
            },
            {
                "type": "Normal Traffic",
                "src_ip": "192.168.1.20",
                "dst_ip": "8.8.8.8",
                "ports_accessed": [53, 443],
                "failed_logins": 0,
                "suspicious_ip": False,
                "connection_count": 10,
                "bytes_outbound": 50_000,
            },
        ]
        return scenarios

    def display_alert(self, alert):
        """Display an alert in a formatted way."""
        severity_colors = {
            "CRITICAL": "!!!",
            "HIGH": "!! ",
            "MEDIUM": "!  ",
            "LOW": "   ",
        }
        marker = severity_colors.get(alert["severity"], "   ")
        print(f"\n[{marker}] {alert['severity']} ALERT")
        print(f"  Time:   {alert['timestamp']}")
        print(f"  Name:   {alert['name']}")
        print(f"  Desc:   {alert['description']}")
        print(f"  Source: {alert['source']} -> {alert['target']}")

    def display_summary(self):
        """Display alert summary."""
        if not self.alerts:
            print("\nNo alerts generated.")
            return

        print(f"\n{'=' * 60}")
        print(f"ALERT SUMMARY")
        print(f"{'=' * 60}")

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for alert in self.alerts:
            severity_counts[alert["severity"]] = severity_counts.get(alert["severity"], 0) + 1

        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev:<10}: {count}")

        print(f"\nTotal Alerts: {len(self.alerts)}")


def demo_ids_analysis():
    print("\n" + "=" * 60)
    print("IDS TRAFFIC ANALYSIS DEMO")
    print("=" * 60)

    ids = IDSSimulator()
    scenarios = ids.generate_suspicious_traffic()

    print("\nAnalyzing network traffic patterns...\n")

    for scenario in scenarios:
        print(f"Traffic Type: {scenario['type']}")
        print(f"  Source: {scenario['src_ip']} -> {scenario['dst_ip']}")
        print(f"  Ports: {scenario['ports_accessed'][:5]}... "
              f"({len(scenario['ports_accessed'])} total)")
        print(f"  Failed Logins: {scenario['failed_logins']}")
        print(f"  Connections: {scenario['connection_count']}")
        print(f"  Data Out: {scenario['bytes_outbound']:,} bytes")

        alert = ids.analyze_traffic(scenario)
        if alert:
            ids.display_alert(alert)
        else:
            print("  [OK] No suspicious activity detected")
        print()

    ids.display_summary()


def interactive_packet_analysis():
    print("\n" + "=" * 60)
    print("INTERACTIVE PACKET ANALYSIS")
    print("=" * 60)
    print("Create custom traffic patterns and see what the IDS detects.\n")

    ids = IDSSimulator()

    print("Enter connection details:")
    src_ip = input("Source IP: ").strip() or "192.168.1.100"
    dst_ip = input("Destination IP: ").strip() or "203.0.113.50"

    ports_input = input("Ports accessed (comma-separated): ").strip() or "22,80,443"
    ports = [int(p.strip()) for p in ports_input.split(",")]

    failed_logins = int(input("Failed login attempts: ").strip() or "0")
    suspicious = input("Is destination IP suspicious? (yes/no): ").strip().lower() == "yes"
    conn_count = int(input("Connection count: ").strip() or "1")
    bytes_out = int(input("Outbound bytes: ").strip() or "1000")

    log = {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "ports_accessed": ports,
        "failed_logins": failed_logins,
        "suspicious_ip": suspicious,
        "connection_count": conn_count,
        "bytes_outbound": bytes_out,
    }

    print("\nAnalyzing...")
    alert = ids.analyze_traffic(log)
    if alert:
        ids.display_alert(alert)
    else:
        print("\n[OK] Traffic appears normal.")


def demo_anomaly_detection():
    print("\n" + "=" * 60)
    print("ANOMALY-BASED DETECTION")
    print("=" * 60)
    print("Unlike signature-based detection, anomaly detection learns")
    print("normal behavior and flags deviations.\n")

    # Establish baseline
    baseline = {
        "avg_connections_per_hour": 50,
        "avg_data_transfer": 100_000,  # bytes
        "typical_ports": [80, 443, 53],
        "typical_hours": list(range(8, 18)),  # Business hours
    }

    print("Baseline (Normal Behavior):")
    print(f"  Avg connections/hour: {baseline['avg_connections_per_hour']}")
    print(f"  Avg data transfer: {baseline['avg_data_transfer']:,} bytes")
    print(f"  Typical ports: {baseline['typical_ports']}")
    print(f"  Active hours: {baseline['typical_hours']}")

    test_cases = [
        {
            "name": "Normal Business Hours",
            "connections": 45,
            "data": 80_000,
            "ports": [80, 443],
            "hour": 14,
        },
        {
            "name": "After-Hours Activity",
            "connections": 200,
            "data": 500_000,
            "ports": [22, 3389],
            "hour": 2,
        },
        {
            "name": "Data Exfiltration Attempt",
            "connections": 30,
            "data": 2_000_000_000,
            "ports": [443],
            "hour": 10,
        },
    ]

    print("\n--- Anomaly Detection Results ---")
    for case in test_cases:
        anomalies = 0
        if case["connections"] > baseline["avg_connections_per_hour"] * 2:
            anomalies += 1
        if case["data"] > baseline["avg_data_transfer"] * 10:
            anomalies += 1
        if any(p not in baseline["typical_ports"] for p in case["ports"]):
            anomalies += 1
        if case["hour"] not in baseline["typical_hours"]:
            anomalies += 1

        status = "ANOMALY" if anomalies >= 2 else "NORMAL" if anomalies == 0 else "SUSPICIOUS"
        print(f"\n{case['name']}: [{status}]")
        print(f"  Connections: {case['connections']}, Data: {case['data']:,} bytes")
        print(f"  Ports: {case['ports']}, Hour: {case['hour']}")
        print(f"  Anomaly score: {anomalies}/4")


def main():
    print("=" * 60)
    print("IDS ALERT SIMULATOR")
    print("=" * 60)
    print("Learn how intrusion detection systems identify threats.\n")

    while True:
        print("\nMenu:")
        print("1. IDS Traffic Analysis Demo")
        print("2. Interactive Packet Analysis")
        print("3. Anomaly Detection Demo")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_ids_analysis()
        elif choice == "2":
            interactive_packet_analysis()
        elif choice == "3":
            demo_anomaly_detection()
        elif choice == "4":
            demo_ids_analysis()
            demo_anomaly_detection()
        elif choice == "5":
            print("Stay vigilant!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
