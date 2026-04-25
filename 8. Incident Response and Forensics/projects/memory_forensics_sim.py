#!/usr/bin/env python3
"""
Memory Forensics Simulator
Demonstrates how memory analysis detects advanced threats.
"""

import random


class MemoryDump:
    """Simulates a memory dump with various processes and artifacts."""

    def __init__(self):
        self.processes = []
        self.network_connections = []
        self.loaded_dlls = {}
        self.suspicious_regions = []
        self._generate_memory_contents()

    def _generate_memory_contents(self):
        """Generate realistic memory contents with hidden malware."""
        # Normal processes
        normal_processes = [
            {"pid": 100, "name": "explorer.exe", "ppid": 1, "path": "C:\\Windows\\explorer.exe"},
            {"pid": 200, "name": "chrome.exe", "ppid": 100, "path": "C:\\Program Files\\Google\\Chrome\\chrome.exe"},
            {"pid": 300, "name": "svchost.exe", "ppid": 1, "path": "C:\\Windows\\System32\\svchost.exe"},
            {"pid": 400, "name": "notepad.exe", "ppid": 100, "path": "C:\\Windows\\notepad.exe"},
            {"pid": 500, "name": "lsass.exe", "ppid": 1, "path": "C:\\Windows\\System32\\lsass.exe"},
        ]

        # Malicious process masquerading as legitimate
        malicious = {
            "pid": 2048,
            "name": "svchost.exe",  # Same name as legitimate!
            "ppid": 100,
            "path": "C:\\Users\\John\\AppData\\Local\\Temp\\svchost.exe",  # Wrong path!
        }

        # Process with injected code
        injected = {
            "pid": 512,
            "name": "chrome.exe",
            "ppid": 100,
            "path": "C:\\Program Files\\Google\\Chrome\\chrome.exe",
            "injected": True,
        }

        self.processes = normal_processes + [malicious, injected]

        # Network connections
        self.network_connections = [
            {"pid": 200, "local": "192.168.1.100:54321", "remote": "142.250.185.78:443", "state": "ESTABLISHED"},  # Chrome to Google
            {"pid": 200, "local": "192.168.1.100:54322", "remote": "142.250.185.78:443", "state": "ESTABLISHED"},
            {"pid": 2048, "local": "192.168.1.100:49152", "remote": "203.0.113.77:4444", "state": "ESTABLISHED"},  # Malware C2
            {"pid": 300, "local": "0.0.0.0:445", "remote": "0.0.0.0:0", "state": "LISTENING"},
        ]

        # Suspicious memory regions
        self.suspicious_regions = [
            {"pid": 2048, "address": "0x7ff80000", "protection": "RWX", "size": 4096, "note": "Executable heap (suspicious)"},
            {"pid": 512, "address": "0x6a000000", "protection": "RWX", "size": 262144, "note": "Injected code segment"},
        ]


class MemoryAnalyzer:
    """Analyzes memory dumps for threats."""

    def __init__(self, memory_dump):
        self.memory = memory_dump
        self.findings = []

    def analyze_processes(self):
        """Analyze processes for anomalies."""
        print("\n" + "=" * 70)
        print("PROCESS ANALYSIS")
        print("=" * 70)

        # Check for process masquerading
        process_names = {}
        for proc in self.memory.processes:
            name = proc["name"]
            if name not in process_names:
                process_names[name] = []
            process_names[name].append(proc)

        print(f"\n{'PID':<8} {'Name':<20} {'Parent':<8} {'Path'}")
        print("─" * 70)
        for proc in self.memory.processes:
            injected = " [INJECTED]" if proc.get("injected") else ""
            print(f"{proc['pid']:<8} {proc['name']:<20} {proc['ppid']:<8} {proc['path']}{injected}")

        # Detect masquerading
        for name, procs in process_names.items():
            if len(procs) > 1:
                print(f"\n[!] DUPLICATE PROCESS DETECTED: {name}")
                for p in procs:
                    print(f"    PID {p['pid']}: {p['path']}")

                # Check for suspicious path
                for p in procs:
                    if "Temp" in p["path"] or "AppData" in p["path"]:
                        finding = {
                            "type": "MASQUERADING",
                            "severity": "HIGH",
                            "description": f"{name} running from suspicious path: {p['path']}",
                            "pid": p["pid"],
                        }
                        self.findings.append(finding)
                        print(f"    [CRITICAL] Likely malware masquerading as {name}")

        # Detect injected processes
        for proc in self.memory.processes:
            if proc.get("injected"):
                finding = {
                    "type": "CODE_INJECTION",
                    "severity": "CRITICAL",
                    "description": f"Code injection detected in {proc['name']} (PID {proc['pid']})",
                    "pid": proc["pid"],
                }
                self.findings.append(finding)
                print(f"\n[!] CODE INJECTION: {proc['name']} (PID {proc['pid']})")

    def analyze_network(self):
        """Analyze network connections from memory."""
        print("\n" + "=" * 70)
        print("NETWORK CONNECTION ANALYSIS")
        print("=" * 70)

        suspicious_ports = [4444, 5555, 6666, 31337, 12345]
        suspicious_ips = ["203.0.113.77", "198.51.100.50"]

        print(f"\n{'PID':<8} {'Local':<25} {'Remote':<25} {'State'}")
        print("─" * 70)
        for conn in self.memory.network_connections:
            marker = ""
            remote_ip = conn["remote"].split(":")[0]
            remote_port = int(conn["remote"].split(":")[1])

            if remote_port in suspicious_ports or remote_ip in suspicious_ips:
                marker = " [!]"
                finding = {
                    "type": "SUSPICIOUS_CONNECTION",
                    "severity": "HIGH",
                    "description": f"Connection to suspicious endpoint: {conn['remote']}",
                    "pid": conn["pid"],
                }
                self.findings.append(finding)

            print(f"{conn['pid']:<8} {conn['local']:<25} {conn['remote']:<25} {conn['state']}{marker}")

    def analyze_memory_regions(self):
        """Analyze memory regions for suspicious protections."""
        print("\n" + "=" * 70)
        print("MEMORY REGION ANALYSIS")
        print("=" * 70)

        print(f"\n{'PID':<8} {'Address':<16} {'Protection':<10} {'Size':<12} {'Note'}")
        print("─" * 70)
        for region in self.memory.suspicious_regions:
            print(f"{region['pid']:<8} {region['address']:<16} {region['protection']:<10} "
                  f"{region['size']:<12} {region['note']}")

            if region["protection"] == "RWX":
                finding = {
                    "type": "SUSPICIOUS_MEMORY",
                    "severity": "HIGH",
                    "description": f"Read-Write-Execute memory in PID {region['pid']}: {region['note']}",
                    "pid": region["pid"],
                }
                self.findings.append(finding)
                print(f"  [!] RWX memory is highly suspicious - possible shellcode")

    def generate_report(self):
        """Generate final analysis report."""
        print("\n" + "=" * 70)
        print("MEMORY FORENSICS REPORT")
        print("=" * 70)

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1

        print(f"\nTotal Findings: {len(self.findings)}")
        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev}: {count}")

        if self.findings:
            print(f"\n{'─' * 70}")
            print("DETAILED FINDINGS")
            print(f"{'─' * 70}")
            for i, finding in enumerate(self.findings, 1):
                print(f"\n{i}. [{finding['severity']}] {finding['type']}")
                print(f"   PID: {finding.get('pid', 'N/A')}")
                print(f"   {finding['description']}")

        print(f"\n{'─' * 70}")
        print("RECOMMENDED ACTIONS")
        print(f"{'─' * 70}")
        print("1. Terminate malicious processes (PID 2048)")
        print("2. Isolate infected host from network")
        print("3. Collect memory dump for full analysis")
        print("4. Check for persistence mechanisms (registry, scheduled tasks)")
        print("5. Hunt for similar indicators across the enterprise")


def main():
    print("=" * 70)
    print("MEMORY FORENSICS SIMULATOR")
    print("=" * 70)
    print("Learn how memory analysis detects fileless malware and advanced threats.\n")

    print("Generating simulated memory dump...")
    memory = MemoryDump()
    analyzer = MemoryAnalyzer(memory)

    input("\nPress Enter to begin analysis...")

    analyzer.analyze_processes()
    analyzer.analyze_network()
    analyzer.analyze_memory_regions()
    analyzer.generate_report()

    print("\n" + "=" * 70)
    print("Memory forensics is essential for detecting fileless malware")
    print("and understanding the full scope of a compromise.")
    print("=" * 70)


if __name__ == "__main__":
    main()
