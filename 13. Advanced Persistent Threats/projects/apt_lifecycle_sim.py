#!/usr/bin/env python3
"""
APT Lifecycle Simulator
Simulates the complete APT kill chain with MITRE ATT&CK mapping.
"""

from datetime import datetime, timedelta


class APTCampaign:
    """Simulates an APT campaign."""

    def __init__(self, name, actor):
        self.name = name
        self.actor = actor
        self.stages = []
        self._build_campaign()

    def _build_campaign(self):
        """Build the APT campaign timeline."""
        base_time = datetime(2024, 1, 1, 0, 0)

        stages = [
            {
                "phase": "Reconnaissance",
                "time": base_time,
                "mitre": "T1593 - Search Open Websites/Domains",
                "activity": "Actor searches LinkedIn for company employees and org chart",
                "detection": "OSINT monitoring, dark web forum monitoring",
            },
            {
                "phase": "Weaponization",
                "time": base_time + timedelta(days=7),
                "mitre": "T1203 - Exploitation for Client Execution",
                "activity": "Create malicious Word document with macro payload",
                "detection": "Threat intelligence on actor TTPs",
            },
            {
                "phase": "Delivery",
                "time": base_time + timedelta(days=14),
                "mitre": "T1566.001 - Spearphishing Attachment",
                "activity": "Send spear-phishing email to HR manager with malicious attachment",
                "detection": "Email gateway filtering, user reporting",
            },
            {
                "phase": "Exploitation",
                "time": base_time + timedelta(days=14, hours=2),
                "mitre": "T1059.005 - Visual Basic",
                "activity": "Macro executes, downloads second-stage payload",
                "detection": "Macro execution logging, network monitoring",
            },
            {
                "phase": "Installation",
                "time": base_time + timedelta(days=14, hours=3),
                "mitre": "T1547.001 - Registry Run Keys",
                "activity": "Install persistence via registry run key",
                "detection": "Registry monitoring, EDR alerts",
            },
            {
                "phase": "Command & Control",
                "time": base_time + timedelta(days=15),
                "mitre": "T1071.001 - Application Layer Protocol: Web Protocols",
                "activity": "Beacon to C2 server via HTTPS (blends with normal traffic)",
                "detection": "DNS monitoring, SSL inspection, beaconing detection",
            },
            {
                "phase": "Lateral Movement",
                "time": base_time + timedelta(days=20),
                "mitre": "T1021.002 - SMB/Windows Admin Shares",
                "activity": "Use stolen credentials to move to domain controller",
                "detection": "Authentication monitoring, lateral movement analytics",
            },
            {
                "phase": "Privilege Escalation",
                "time": base_time + timedelta(days=22),
                "mitre": "T1078.002 - Domain Accounts",
                "activity": "Compromise domain admin account",
                "detection": "Privileged access monitoring, anomaly detection",
            },
            {
                "phase": "Collection",
                "time": base_time + timedelta(days=25),
                "mitre": "T1560 - Archive Collected Data",
                "activity": "Compress sensitive documents into password-protected archive",
                "detection": "DLP alerts, file access monitoring",
            },
            {
                "phase": "Exfiltration",
                "time": base_time + timedelta(days=28),
                "mitre": "T1041 - Exfiltration Over C2 Channel",
                "activity": "Upload archived data to cloud storage via C2 channel",
                "detection": "DLP, network traffic analysis, CASB",
            },
        ]

        self.stages = stages

    def display_timeline(self):
        """Display the campaign timeline."""
        print(f"\n{'=' * 70}")
        print(f"APT CAMPAIGN: {self.name}")
        print(f"Threat Actor: {self.actor}")
        print(f"{'=' * 70}")

        for stage in self.stages:
            print(f"\n[{stage['phase']}]")
            print(f"  Time:       {stage['time'].strftime('%Y-%m-%d %H:%M')}")
            print(f"  MITRE:      {stage['mitre']}")
            print(f"  Activity:   {stage['activity']}")
            print(f"  Detection:  {stage['detection']}")

    def display_detection_opportunities(self):
        """Show detection opportunities at each stage."""
        print(f"\n{'=' * 70}")
        print("DETECTION OPPORTUNITIES")
        print(f"{'=' * 70}")

        for stage in self.stages:
            print(f"\n{stage['phase']:<20} {stage['detection']}")

    def calculate_dwell_time(self):
        """Calculate attacker dwell time."""
        first = self.stages[0]['time']
        last = self.stages[-1]['time']
        dwell = (last - first).days

        print(f"\n{'=' * 70}")
        print("DWELL TIME ANALYSIS")
        print(f"{'=' * 70}")
        print(f"Initial Compromise: {first.strftime('%Y-%m-%d')}")
        print(f"Discovery/Exfiltration: {last.strftime('%Y-%m-%d')}")
        print(f"Dwell Time: {dwell} days")
        print(f"\nIndustry average dwell time: ~280 days")
        print(f"Goal: Reduce to <24 hours through enhanced detection")


def demo_apt_campaign():
    """Run the APT campaign simulation."""
    campaign = APTCampaign("Operation Silent Harvest", "APT-29 (Cozy Bear)")
    campaign.display_timeline()
    campaign.display_detection_opportunities()
    campaign.calculate_dwell_time()


def demo_mitre_attck_mapping():
    """Show MITRE ATT&CK framework mapping."""
    print("\n" + "=" * 70)
    print("MITRE ATT&CK MAPPING")
    print("=" * 70)

    techniques = {
        "Initial Access": ["T1566 (Phishing)", "T1190 (Exploit Public-Facing App)", "T1133 (External Remote Services)"],
        "Execution": ["T1059 (Command and Scripting Interpreter)", "T1203 (Exploitation for Client Execution)"],
        "Persistence": ["T1547 (Boot or Logon Autostart Execution)", "T1136 (Create Account)"],
        "Privilege Escalation": ["T1078 (Valid Accounts)", "T1068 (Exploitation for Privilege Escalation)"],
        "Defense Evasion": ["T1027 (Obfuscated Files or Information)", "T1070 (Indicator Removal)"],
        "Credential Access": ["T1003 (OS Credential Dumping)", "T1558 (Steal or Forge Kerberos Tickets)"],
        "Discovery": ["T1083 (File and Directory Discovery)", "T1018 (Remote System Discovery)"],
        "Lateral Movement": ["T1021 (Remote Services)", "T1210 (Exploitation of Remote Services)"],
        "Collection": ["T1560 (Archive Collected Data)", "T1005 (Data from Local System)"],
        "Exfiltration": ["T1041 (Exfiltration Over C2)", "T1567 (Exfiltration Over Web Service)"],
    }

    for tactic, techs in techniques.items():
        print(f"\n[{tactic}]")
        for tech in techs:
            print(f"  {tech}")


def main():
    print("=" * 70)
    print("APT LIFECYCLE SIMULATOR")
    print("=" * 70)
    print("Understand the complete APT kill chain and detection opportunities.\n")

    while True:
        print("\nMenu:")
        print("1. APT Campaign Simulation")
        print("2. MITRE ATT&CK Mapping")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_apt_campaign()
        elif choice == "2":
            demo_mitre_attck_mapping()
        elif choice == "3":
            demo_apt_campaign()
            demo_mitre_attck_mapping()
        elif choice == "4":
            print("Detect early, respond fast!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
