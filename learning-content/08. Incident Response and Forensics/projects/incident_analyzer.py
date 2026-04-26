#!/usr/bin/env python3
"""
Incident Analyzer
Simulates investigating a security incident through log analysis and timeline reconstruction.
"""

import random
from datetime import datetime, timedelta


class IncidentScenario:
    """Generates a realistic security incident scenario."""

    def __init__(self):
        self.events = []
        self.iocs = {
            "attacker_ip": "203.0.113.77",
            "compromised_account": "jsmith",
            "malware_hash": "d41d8cd98f00b204e9800998ecf8427e",
            "c2_domain": "evil-update.xyz",
        }
        self._generate_timeline()

    def _generate_timeline(self):
        """Generate a realistic attack timeline."""
        base_time = datetime(2024, 3, 15, 9, 0, 0)

        timeline = [
            (0, "firewall", f"Connection attempt from {self.iocs['attacker_ip']} to port 3389 (RDP) - BLOCKED"),
            (5, "firewall", f"Connection attempt from {self.iocs['attacker_ip']} to port 22 (SSH) - BLOCKED"),
            (10, "email_gateway", f"Phishing email delivered to {self.iocs['compromised_account']}@company.com"),
            (12, "email_gateway", f"User {self.iocs['compromised_account']} clicked link in phishing email"),
            (15, "web_proxy", f"{self.iocs['compromised_account']} accessed http://{self.iocs['c2_domain']}/update.exe"),
            (16, "endpoint", f"Process created: C:\\Users\\{self.iocs['compromised_account']}\\AppData\\Local\\Temp\\update.exe"),
            (17, "endpoint", f"Registry modification: HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SystemUpdate"),
            (20, "endpoint", f"Suspicious outbound connection from update.exe to {self.iocs['attacker_ip']}:4444"),
            (25, "auth", f"Successful login for {self.iocs['compromised_account']} from {self.iocs['attacker_ip']} via VPN"),
            (30, "file_server", f"{self.iocs['compromised_account']} accessed \\fileserver\\finance\\Q1_reports.xlsx"),
            (35, "file_server", f"Bulk file access by {self.iocs['compromised_account']}: 150 files in 2 minutes"),
            (40, "endpoint", f"Data compression activity: 7z.exe creating archive temp.zip"),
            (45, "network", f"Large outbound transfer: 2.3 GB to {self.iocs['attacker_ip']}"),
            (50, "endpoint", f"Windows Defender alert: Trojan:Win32/Malware detected in update.exe"),
        ]

        for offset_minutes, source, description in timeline:
            timestamp = base_time + timedelta(minutes=offset_minutes)
            self.events.append({
                "time": timestamp,
                "source": source,
                "description": description,
            })

    def get_events(self):
        return self.events


class IncidentAnalyzer:
    """Analyzes incident data."""

    def __init__(self, scenario):
        self.scenario = scenario
        self.findings = []

    def reconstruct_timeline(self):
        """Display the attack timeline."""
        print("\n" + "=" * 70)
        print("INCIDENT TIMELINE RECONSTRUCTION")
        print("=" * 70)
        print(f"{'Time':<12} {'Source':<15} Event")
        print("─" * 70)

        for event in self.scenario.events:
            time_str = event["time"].strftime("%H:%M")
            source = event["source"]
            desc = event["description"]
            print(f"{time_str:<12} {source:<15} {desc}")

    def identify_attack_phases(self):
        """Map events to MITRE ATT&CK phases."""
        print("\n" + "=" * 70)
        print("ATTACK PHASE ANALYSIS (MITRE ATT&CK Mapping)")
        print("=" * 70)

        phases = [
            ("Initial Access", "09:10", "Phishing email delivered and clicked"),
            ("Execution", "09:15", "Malicious executable (update.exe) launched"),
            ("Persistence", "09:17", "Registry run key added for persistence"),
            ("Command & Control", "09:20", "Outbound connection to C2 server"),
            ("Lateral Movement", "09:25", "VPN login from attacker IP"),
            ("Collection", "09:30-09:35", "Bulk file access on file server"),
            ("Exfiltration", "09:40-09:45", "Data compressed and transferred outbound"),
            ("Discovery", "Throughout", "Reconnaissance via failed RDP/SSH attempts"),
        ]

        for phase, time_range, description in phases:
            print(f"\n[{phase}]")
            print(f"  Time: {time_range}")
            print(f"  Activity: {description}")

    def extract_iocs(self):
        """Extract Indicators of Compromise."""
        print("\n" + "=" * 70)
        print("INDICATORS OF COMPROMISE (IOCs)")
        print("=" * 70)

        iocs = self.scenario.iocs
        print("\nNetwork IOCs:")
        print(f"  Malicious IP:     {iocs['attacker_ip']}")
        print(f"  C2 Domain:        {iocs['c2_domain']}")
        print(f"  C2 Port:          4444")

        print("\nHost IOCs:")
        print(f"  Malware Hash:     {iocs['malware_hash']} (MD5)")
        print(f"  Malware Path:     C:\\Users\\{iocs['compromised_account']}\\AppData\\Local\\Temp\\update.exe")
        print(f"  Registry Key:     HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\SystemUpdate")
        print(f"  Archive File:     temp.zip")

        print("\nAccount IOCs:")
        print(f"  Compromised User: {iocs['compromised_account']}")
        print(f"  VPN Source IP:    {iocs['attacker_ip']}")

        print("\nRecommended Actions:")
        print("  1. Block IP and domain at firewall/proxy")
        print("  2. Reset compromised account password and revoke sessions")
        print("  3. Hunt for malware hash across all endpoints")
        print("  4. Check registry for persistence mechanism")
        print("  5. Review file server access logs for data theft scope")

    def assess_impact(self):
        """Assess the business impact."""
        print("\n" + "=" * 70)
        print("BUSINESS IMPACT ASSESSMENT")
        print("=" * 70)

        impacts = [
            ("Data Breach", "HIGH", "150 financial documents accessed, 2.3 GB exfiltrated"),
            ("System Compromise", "HIGH", "Malware installed with persistence mechanism"),
            ("Account Takeover", "MEDIUM", f"User account '{self.scenario.iocs['compromised_account']}' compromised"),
            ("Lateral Movement", "MEDIUM", "Attacker accessed VPN and file server"),
            ("Reputational Risk", "MEDIUM", "Potential regulatory notification required"),
        ]

        print(f"\n{'Category':<25} {'Severity':<10} Details")
        print("─" * 70)
        for category, severity, details in impacts:
            print(f"{category:<25} {severity:<10} {details}")

        print("\nRecommended Notifications:")
        print("  - Legal/Compliance team (data breach assessment)")
        print("  - HR (affected employee awareness training)")
        print("  - Customers (if PII/financial data involved)")
        print("  - Regulatory authorities (if required by law)")


def main():
    print("=" * 70)
    print("INCIDENT RESPONSE ANALYZER")
    print("=" * 70)
    print("Practice investigating a simulated security incident.\n")

    scenario = IncidentScenario()
    analyzer = IncidentAnalyzer(scenario)

    while True:
        print("\nMenu:")
        print("1. Reconstruct Timeline")
        print("2. Identify Attack Phases")
        print("3. Extract IOCs")
        print("4. Assess Business Impact")
        print("5. Full Investigation Report")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            analyzer.reconstruct_timeline()
        elif choice == "2":
            analyzer.identify_attack_phases()
        elif choice == "3":
            analyzer.extract_iocs()
        elif choice == "4":
            analyzer.assess_impact()
        elif choice == "5":
            analyzer.reconstruct_timeline()
            analyzer.identify_attack_phases()
            analyzer.extract_iocs()
            analyzer.assess_impact()
        elif choice == "6":
            print("Always have an incident response plan ready!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
