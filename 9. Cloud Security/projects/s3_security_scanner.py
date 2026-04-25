#!/usr/bin/env python3
"""
S3 Bucket Security Scanner
Simulates checking cloud storage configurations for security issues.
"""

import random


class S3Bucket:
    """Simulates a cloud storage bucket."""

    def __init__(self, name):
        self.name = name
        self.public_access = random.choice([True, False, False, False])
        self.encryption = random.choice(["AES-256", "AES-256", "None"])
        self.versioning = random.choice(["Enabled", "Disabled", "Disabled"])
        self.logging = random.choice(["Enabled", "Disabled", "Disabled"])
        self.mfa_delete = random.choice(["Enabled", "Disabled", "Disabled", "Disabled"])
        self.policy = self._generate_policy()

    def _generate_policy(self):
        """Generate a bucket policy."""
        if self.public_access:
            return {
                "public_read": True,
                "public_write": random.choice([True, False]),
                "authenticated_read": True,
            }
        return {
            "public_read": False,
            "public_write": False,
            "authenticated_read": False,
        }


class S3SecurityScanner:
    """Scans buckets for security misconfigurations."""

    def __init__(self):
        self.buckets = []
        self.findings = []

    def add_bucket(self, bucket):
        self.buckets.append(bucket)

    def scan_public_access(self):
        """Check for public access configurations."""
        print("\n" + "=" * 60)
        print("PUBLIC ACCESS SCAN")
        print("=" * 60)

        for bucket in self.buckets:
            if bucket.public_access:
                finding = {
                    "bucket": bucket.name,
                    "severity": "CRITICAL" if bucket.policy["public_write"] else "HIGH",
                    "issue": f"Public access enabled (write={bucket.policy['public_write']})",
                }
                self.findings.append(finding)
                print(f"[!] {bucket.name}: Public access enabled")
                if bucket.policy["public_write"]:
                    print(f"    CRITICAL: Anyone can read AND write to this bucket!")
                else:
                    print(f"    HIGH: Anyone can read objects in this bucket")
            else:
                print(f"[OK] {bucket.name}: Not publicly accessible")

    def scan_encryption(self):
        """Check encryption settings."""
        print("\n" + "=" * 60)
        print("ENCRYPTION SCAN")
        print("=" * 60)

        for bucket in self.buckets:
            if bucket.encryption == "None":
                finding = {
                    "bucket": bucket.name,
                    "severity": "HIGH",
                    "issue": "Server-side encryption not enabled",
                }
                self.findings.append(finding)
                print(f"[!] {bucket.name}: Encryption disabled")
            else:
                print(f"[OK] {bucket.name}: {bucket.encryption} encryption enabled")

    def scan_versioning(self):
        """Check versioning configuration."""
        print("\n" + "=" * 60)
        print("VERSIONING & MFA DELETE SCAN")
        print("=" * 60)

        for bucket in self.buckets:
            if bucket.versioning == "Disabled":
                finding = {
                    "bucket": bucket.name,
                    "severity": "MEDIUM",
                    "issue": "Versioning disabled - no protection against accidental deletion",
                }
                self.findings.append(finding)
                print(f"[!] {bucket.name}: Versioning disabled")
            else:
                print(f"[OK] {bucket.name}: Versioning enabled")

            if bucket.mfa_delete == "Disabled":
                finding = {
                    "bucket": bucket.name,
                    "severity": "MEDIUM",
                    "issue": "MFA delete disabled - sensitive deletions don't require MFA",
                }
                self.findings.append(finding)
                print(f"[!] {bucket.name}: MFA delete disabled")
            else:
                print(f"[OK] {bucket.name}: MFA delete enabled")

    def scan_logging(self):
        """Check logging configuration."""
        print("\n" + "=" * 60)
        print("ACCESS LOGGING SCAN")
        print("=" * 60)

        for bucket in self.buckets:
            if bucket.logging == "Disabled":
                finding = {
                    "bucket": bucket.name,
                    "severity": "MEDIUM",
                    "issue": "Access logging disabled - cannot audit access",
                }
                self.findings.append(finding)
                print(f"[!] {bucket.name}: Access logging disabled")
            else:
                print(f"[OK] {bucket.name}: Access logging enabled")

    def generate_report(self):
        """Generate comprehensive security report."""
        print("\n" + "=" * 60)
        print("S3 BUCKET SECURITY REPORT")
        print("=" * 60)

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1

        total = len(self.findings)
        print(f"\nBuckets Scanned: {len(self.buckets)}")
        print(f"Total Findings: {total}")
        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev}: {count}")

        if self.findings:
            print(f"\n{'─' * 60}")
            print("DETAILED FINDINGS")
            print(f"{'─' * 60}")
            for finding in self.findings:
                print(f"\n[{finding['severity']}] {finding['bucket']}")
                print(f"  {finding['issue']}")

        print(f"\n{'─' * 60}")
        print("REMEDIATION STEPS")
        print(f"{'─' * 60}")
        print("1. Disable all public access unless absolutely necessary")
        print("2. Enable default encryption (AES-256 or KMS)")
        print("3. Enable versioning for data protection")
        print("4. Enable MFA delete for critical buckets")
        print("5. Enable access logging for audit trails")
        print("6. Implement least-privilege bucket policies")
        print("7. Regularly scan for misconfigurations")


def demo_scan():
    """Run a demonstration scan."""
    print("\n" + "=" * 60)
    print("CLOUD STORAGE SECURITY SCAN")
    print("=" * 60)

    scanner = S3SecurityScanner()

    # Create sample buckets
    bucket_names = [
        "company-public-website",
        "finance-reports-2024",
        "backup-database-daily",
        "temp-uploads-staging",
        "customer-documents-prod",
    ]

    for name in bucket_names:
        scanner.add_bucket(S3Bucket(name))

    scanner.scan_public_access()
    scanner.scan_encryption()
    scanner.scan_versioning()
    scanner.scan_logging()
    scanner.generate_report()


def demo_data_breach_scenario():
    """Demonstrate a real-world data breach scenario."""
    print("\n" + "=" * 60)
    print("REAL-WORLD SCENARIO: MISCONFIGURED BUCKET")
    print("=" * 60)

    print("""
Scenario: A company stores customer PII in cloud storage.
A developer accidentally configures the bucket with public read access.

Timeline:
  Day 0:  Bucket created with sensitive customer data
  Day 1:  Developer enables "Public Read" for testing, forgets to disable
  Day 30: Security scanner detects public access
  Day 45: Data discovered by security researcher (or attacker)

Impact:
  - 100,000 customer records exposed
  - Regulatory fines (GDPR, CCPA)
  - Reputational damage
  - Required breach notification

How it could have been prevented:
  - Block Public Access setting at account level
  - Automated scanning in CI/CD pipeline
  - Regular security audits
  - Least-privilege bucket policies
    """)


def main():
    print("=" * 60)
    print("S3 BUCKET SECURITY SCANNER")
    print("=" * 60)
    print("Learn to identify and fix cloud storage misconfigurations.\n")

    while True:
        print("\nMenu:")
        print("1. Run Security Scan Demo")
        print("2. Data Breach Scenario")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_scan()
        elif choice == "2":
            demo_data_breach_scenario()
        elif choice == "3":
            demo_scan()
            demo_data_breach_scenario()
        elif choice == "4":
            print("Secure the cloud!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
