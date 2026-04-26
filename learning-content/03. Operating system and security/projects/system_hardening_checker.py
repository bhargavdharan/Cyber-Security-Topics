#!/usr/bin/env python3
"""
System Hardening Checker
Simulates an OS security audit by checking common hardening criteria.
Works on any OS by using simulated checks where native APIs aren't available.
"""

import platform
import random
import socket


class SimulatedSystemCheck:
    """Simulates system checks for educational purposes."""

    def __init__(self):
        self.os_name = platform.system()
        self.issues = []
        self.warnings = []
        self.passed = []

    def check_password_policy(self):
        """Check password policy settings."""
        print("\n[1/6] Checking Password Policy...")

        # In a real tool, this would check /etc/login.defs, GPO, etc.
        # For simulation, we generate realistic scenarios
        checks = [
            ("Minimum password length", random.choice([6, 8, 12, 14]), 12),
            ("Password complexity required", random.choice([True, True, False]), True),
            ("Password history enforced", random.choice([True, False]), True),
            ("Maximum password age (days)", random.choice([30, 60, 90, 99999]), 90),
            ("Account lockout threshold", random.choice([3, 5, 10, 999]), 5),
        ]

        for name, current, recommended in checks:
            if isinstance(recommended, bool):
                status = "PASS" if current == recommended else "FAIL"
            else:
                status = "PASS" if current <= recommended else "FAIL"

            if status == "PASS":
                self.passed.append(f"{name}: {current}")
                print(f"  [PASS] {name}: {current}")
            else:
                self.issues.append(f"{name}: {current} (recommend: {recommended})")
                print(f"  [FAIL] {name}: {current} (recommend: {recommended})")

    def check_user_accounts(self):
        """Check user account security."""
        print("\n[2/6] Checking User Accounts...")

        checks = [
            ("Guest account disabled", random.choice([True, True, False]), True),
            ("Default admin renamed", random.choice([True, False]), True),
            ("Unused accounts present", random.choice([True, False]), False),
            ("Shared accounts exist", random.choice([True, False, False]), False),
            ("Passwords expired accounts", random.choice([0, 2, 5]), 0),
        ]

        for name, current, recommended in checks:
            if isinstance(recommended, bool):
                status = "PASS" if current == recommended else "FAIL"
            else:
                status = "PASS" if current <= recommended else "FAIL"

            if status == "PASS":
                self.passed.append(f"{name}: {current}")
                print(f"  [PASS] {name}: {current}")
            else:
                self.warnings.append(f"{name}: {current}")
                print(f"  [WARN] {name}: {current}")

    def check_network_services(self):
        """Check network services and ports."""
        print("\n[3/6] Checking Network Services...")

        # Get actual local IP for realism
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "127.0.0.1"

        common_ports = [22, 80, 443, 3389, 21, 23, 445, 3306]
        open_ports = []

        # Simulate port scan (don't actually scan to avoid firewall prompts)
        for port in common_ports:
            # Simulate: SSH/HTTP/HTTPS usually open, Telnet/FTP sometimes
            if port in [22, 80, 443]:
                is_open = random.choice([True, True, False])
            else:
                is_open = random.choice([True, False, False, False])

            if is_open:
                open_ports.append(port)

        print(f"  Local IP: {local_ip}")
        print(f"  Open ports found: {len(open_ports)}")

        risky_ports = {
            21: "FTP (consider SFTP)",
            23: "Telnet (insecure - use SSH)",
            3389: "RDP (ensure strong auth and limited access)",
            445: "SMB (ensure not exposed to internet)",
        }

        for port in open_ports:
            service = risky_ports.get(port, "Standard service")
            if port in risky_ports:
                self.warnings.append(f"Port {port} open: {service}")
                print(f"  [WARN] Port {port}/tcp open - {service}")
            else:
                self.passed.append(f"Port {port} open (expected)")
                print(f"  [PASS] Port {port}/tcp open - {service}")

        if 23 in open_ports:
            self.issues.append("Telnet (port 23) is running. Disable immediately!")
            print(f"  [CRIT] Telnet detected! Replace with SSH immediately.")

    def check_patch_status(self):
        """Check system patch status."""
        print("\n[4/6] Checking Patch Status...")

        days_since_update = random.choice([1, 7, 15, 30, 45, 90])
        critical_patches = random.choice([0, 0, 1, 3, 5])

        print(f"  Days since last update: {days_since_update}")
        print(f"  Missing critical patches: {critical_patches}")

        if days_since_update > 30:
            self.warnings.append(f"System not updated in {days_since_update} days")
            print(f"  [WARN] System overdue for updates")
        else:
            self.passed.append("Patch status current")
            print(f"  [PASS] System recently updated")

        if critical_patches > 0:
            self.issues.append(f"{critical_patches} critical patches missing")
            print(f"  [FAIL] {critical_patches} critical security patches need installation")

    def check_logging(self):
        """Check logging configuration."""
        print("\n[5/6] Checking Logging & Monitoring...")

        checks = [
            ("System logging enabled", random.choice([True, True, False]), True),
            ("Failed login logging", random.choice([True, False]), True),
            ("Privilege escalation logging", random.choice([True, False]), True),
            ("Log retention (days)", random.choice([7, 30, 90, 365]), 90),
            ("Remote log forwarding", random.choice([True, False]), True),
        ]

        for name, current, recommended in checks:
            if isinstance(recommended, bool):
                status = "PASS" if current == recommended else "WARN"
            else:
                status = "PASS" if current >= recommended else "WARN"

            if status == "PASS":
                self.passed.append(f"{name}: {current}")
                print(f"  [PASS] {name}: {current}")
            else:
                self.warnings.append(f"{name}: {current}")
                print(f"  [WARN] {name}: {current}")

    def check_firewall(self):
        """Check firewall status."""
        print("\n[6/6] Checking Firewall Status...")

        firewall_enabled = random.choice([True, True, True, False])
        default_deny = random.choice([True, False])

        if firewall_enabled:
            self.passed.append("Host firewall is enabled")
            print(f"  [PASS] Host firewall is active")
        else:
            self.issues.append("Host firewall is DISABLED")
            print(f"  [FAIL] Host firewall is DISABLED - enable immediately!")

        if default_deny:
            self.passed.append("Default deny policy configured")
            print(f"  [PASS] Default policy: DENY (good)")
        else:
            self.warnings.append("Default allow policy detected")
            print(f"  [WARN] Default policy: ALLOW (consider default deny)")

    def generate_report(self):
        """Generate final hardening report."""
        print("\n" + "=" * 60)
        print("SYSTEM HARDENING REPORT")
        print("=" * 60)
        print(f"OS Detected: {self.os_name}")
        print(f"Scan Date: Simulated")

        total_checks = len(self.passed) + len(self.warnings) + len(self.issues)
        score = int((len(self.passed) / total_checks) * 100) if total_checks > 0 else 100

        print(f"\n{'─' * 60}")
        print(f"SCORE: {score}/100")
        print(f"{'─' * 60}")

        if score >= 90:
            print("Status: EXCELLENT - System is well-hardened")
        elif score >= 70:
            print("Status: GOOD - Minor improvements recommended")
        elif score >= 50:
            print("Status: FAIR - Several issues need attention")
        else:
            print("Status: POOR - Significant hardening required")

        print(f"\nPassed:   {len(self.passed)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Issues:   {len(self.issues)}")

        if self.issues:
            print(f"\n{'─' * 60}")
            print("CRITICAL ISSUES (Fix Immediately):")
            print(f"{'─' * 60}")
            for issue in self.issues:
                print(f"  ! {issue}")

        if self.warnings:
            print(f"\n{'─' * 60}")
            print("WARNINGS (Recommended Fixes):")
            print(f"{'─' * 60}")
            for warning in self.warnings:
                print(f"  - {warning}")

        print(f"\n{'─' * 60}")
        print("HARDENING RECOMMENDATIONS:")
        print(f"{'─' * 60}")
        print("  1. Enable automatic security updates")
        print("  2. Disable unnecessary services and ports")
        print("  3. Enforce strong password policies")
        print("  4. Enable and configure host firewall")
        print("  5. Implement centralized logging")
        print("  6. Remove or disable default accounts")
        print("  7. Apply principle of least privilege")


def main():
    print("=" * 60)
    print("SYSTEM HARDENING CHECKER")
    print("=" * 60)
    print("This tool simulates an OS security audit.")
    print("It checks password policies, user accounts, network services,")
    print("patch status, logging, and firewall configuration.\n")
    print("NOTE: This is a SIMULATION for educational purposes.")
    print("For real hardening, use CIS Benchmarks and vendor tools.\n")

    input("Press Enter to begin the audit...")

    checker = SimulatedSystemCheck()
    checker.check_password_policy()
    checker.check_user_accounts()
    checker.check_network_services()
    checker.check_patch_status()
    checker.check_logging()
    checker.check_firewall()
    checker.generate_report()

    print("\n" + "=" * 60)
    print("Audit complete! Review the issues above and apply fixes.")
    print("=" * 60)


if __name__ == "__main__":
    main()
