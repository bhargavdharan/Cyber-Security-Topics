#!/usr/bin/env python3
"""
Threat Hunting Simulator
Demonstrates proactive threat hunting methodologies.
"""

import random


class ThreatHunt:
    """Simulates threat hunting scenarios."""

    def __init__(self):
        self.baseline = self._establish_baseline()
        self.current_state = {}

    def _establish_baseline(self):
        """Establish normal behavior baseline."""
        return {
            "normal_processes": ["explorer.exe", "chrome.exe", "svchost.exe", "lsass.exe"],
            "normal_ports": [80, 443, 53, 123],
            "normal_logins_per_hour": 10,
            "normal_data_transfer_mb": 500,
            "normal_admin_actions_per_day": 5,
        }

    def hunt_lateral_movement(self):
        """Hunt for signs of lateral movement."""
        print("\n" + "=" * 60)
        print("HYPOTHESIS: Lateral Movement in Progress")
        print("=" * 60)

        # Simulate findings
        findings = [
            "Multiple authentication attempts from single source to multiple targets",
            "PSExec usage detected on workstation (unusual for this user)",
            "WMI connections observed between unrelated subnets",
            "Kerberos ticket requests spike at 3 AM",
            "New admin account created outside change window",
        ]

        print("\nHunting queries executed:")
        print("  1. Find auth events: same source -> multiple targets")
        print("  2. Search for PSExec, WMI, WinRM usage")
        print("  3. Check for new admin account creation")
        print("  4. Analyze Kerberos ticket patterns")

        print("\nFindings:")
        for finding in findings[:3]:
            print(f"  [!] {finding}")

        print("\nCONCLUSION: Evidence of lateral movement detected")
        print("Recommended: Isolate affected systems, reset compromised accounts")

    def hunt_fileless_malware(self):
        """Hunt for fileless malware indicators."""
        print("\n" + "=" * 60)
        print("HYPOTHESIS: Fileless Malware Present")
        print("=" * 60)

        indicators = [
            "PowerShell executed with encoded command (-enc flag)",
            "Script block logging shows suspicious Base64 content",
            "No executable file on disk for running process",
            "Registry run key points to PowerShell command",
            "AMSI (Anti-Malware Scan Interface) bypass attempt detected",
        ]

        print("\nHunting queries:")
        print("  1. PowerShell with -enc, -encodedcommand")
        print("  2. Processes without associated disk image")
        print("  3. Registry persistence with script content")
        print("  4. AMSI/ETW tampering events")

        print("\nSuspicious indicators:")
        for indicator in indicators[:3]:
            print(f"  [!] {indicator}")

        print("\nCONCLUSION: Fileless malware indicators present")
        print("Recommended: Memory dump analysis, EDR deep scan")

    def hunt_data_exfiltration(self):
        """Hunt for data exfiltration."""
        print("\n" + "=" * 60)
        print("HYPOTHESIS: Data Exfiltration Occurring")
        print("=" * 60)

        baseline = self.baseline["normal_data_transfer_mb"]
        current = random.randint(2000, 5000)  # Much higher than baseline

        print(f"\nBaseline outbound data: {baseline} MB/day")
        print(f"Current outbound data: {current} MB/day")
        print(f"Deviation: {(current/baseline - 1)*100:.0f}% above baseline")

        findings = [
            "Large ZIP archive created in temp directory",
            "Unusual outbound HTTPS to file sharing service",
            "Database dump utility executed by non-DBA user",
            "Multiple sensitive files accessed in sequence",
        ]

        print("\nAdditional indicators:")
        for finding in findings[:3]:
            print(f"  [!] {finding}")

        print("\nCONCLUSION: Potential data exfiltration detected")
        print("Recommended: Block external uploads, investigate DLP alerts")

    def hunt_insider_threat(self):
        """Hunt for insider threat indicators."""
        print("\n" + "=" * 60)
        print("HYPOTHESIS: Insider Threat Activity")
        print("=" * 60)

        anomalies = [
            "Employee accessed files outside their department (after hours)",
            "USB device connected to workstation with sensitive data access",
            "Cloud storage upload to personal account detected",
            "Email with large attachment sent to personal address",
            "VPN login from unusual geographic location",
            "Mass print job for confidential documents",
        ]

        print("\nUser behavior baseline:")
        print("  - Normal working hours: 9 AM - 6 PM")
        print("  - Typical file access: 20-50 files/day")
        print("  - No personal cloud storage usage")
        print("  - No USB usage on sensitive workstations")

        print("\nObserved anomalies:")
        for anomaly in anomalies[:4]:
            print(f"  [!] {anomaly}")

        print("\nCONCLUSION: Insider threat indicators detected")
        print("Recommended: HR notification, enhanced monitoring, access review")


def main():
    print("=" * 60)
    print("THREAT HUNTING SIMULATOR")
    print("=" * 60)
    print("Practice proactive threat hunting scenarios.\n")

    hunt = ThreatHunt()

    while True:
        print("\nMenu:")
        print("1. Hunt: Lateral Movement")
        print("2. Hunt: Fileless Malware")
        print("3. Hunt: Data Exfiltration")
        print("4. Hunt: Insider Threat")
        print("5. Run All Hunts")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            hunt.hunt_lateral_movement()
        elif choice == "2":
            hunt.hunt_fileless_malware()
        elif choice == "3":
            hunt.hunt_data_exfiltration()
        elif choice == "4":
            hunt.hunt_insider_threat()
        elif choice == "5":
            hunt.hunt_lateral_movement()
            hunt.hunt_fileless_malware()
            hunt.hunt_data_exfiltration()
            hunt.hunt_insider_threat()
        elif choice == "6":
            print("Happy hunting!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
