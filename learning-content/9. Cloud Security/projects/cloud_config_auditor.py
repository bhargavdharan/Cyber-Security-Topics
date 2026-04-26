#!/usr/bin/env python3
"""
Cloud Configuration Auditor
Simulates auditing cloud infrastructure for security misconfigurations.
"""

import random


class CloudResource:
    """Base class for cloud resources."""

    def __init__(self, name, resource_type):
        self.name = name
        self.resource_type = resource_type
        self.tags = {}


class SecurityGroup(CloudResource):
    """Simulates a cloud security group / firewall."""

    def __init__(self, name):
        super().__init__(name, "SecurityGroup")
        self.rules = []
        self._generate_rules()

    def _generate_rules(self):
        """Generate random security group rules."""
        # Potentially risky rules
        risky_rules = [
            {"protocol": "tcp", "from_port": 22, "to_port": 22, "source": "0.0.0.0/0", "action": "allow"},
            {"protocol": "tcp", "from_port": 3389, "to_port": 3389, "source": "0.0.0.0/0", "action": "allow"},
            {"protocol": "tcp", "from_port": 3306, "to_port": 3306, "source": "0.0.0.0/0", "action": "allow"},
        ]

        # Safe rules
        safe_rules = [
            {"protocol": "tcp", "from_port": 443, "to_port": 443, "source": "0.0.0.0/0", "action": "allow"},
            {"protocol": "tcp", "from_port": 80, "to_port": 80, "source": "0.0.0.0/0", "action": "allow"},
            {"protocol": "tcp", "from_port": 22, "to_port": 22, "source": "10.0.0.0/8", "action": "allow"},
        ]

        self.rules = random.sample(safe_rules, random.randint(1, 3))
        if random.random() < 0.4:  # 40% chance of risky rule
            self.rules.extend(random.sample(risky_rules, random.randint(1, 2)))


class ComputeInstance(CloudResource):
    """Simulates a cloud compute instance / VM."""

    def __init__(self, name):
        super().__init__(name, "ComputeInstance")
        self.public_ip = random.choice([True, False, False])
        self.encryption = random.choice(["Enabled", "Enabled", "Disabled"])
        self.imds_v2 = random.choice(["Required", "Optional", "Optional"])
        self.ssm_agent = random.choice(["Installed", "Missing", "Missing"])


class CloudAuditor:
    """Audits cloud resources for security issues."""

    def __init__(self):
        self.resources = []
        self.findings = []

    def add_resource(self, resource):
        self.resources.append(resource)

    def audit_security_groups(self):
        """Audit security group configurations."""
        print("\n" + "=" * 60)
        print("SECURITY GROUP AUDIT")
        print("=" * 60)

        for resource in self.resources:
            if isinstance(resource, SecurityGroup):
                print(f"\nSecurity Group: {resource.name}")
                print(f"{'Protocol':<10} {'Ports':<15} {'Source':<18} {'Status'}")
                print("─" * 60)

                for rule in resource.rules:
                    port_range = f"{rule['from_port']}-{rule['to_port']}" if rule['from_port'] != rule['to_port'] else str(rule['from_port'])

                    risky = False
                    if rule["source"] == "0.0.0.0/0" and rule["from_port"] in [22, 3389, 3306, 5432, 6379]:
                        risky = True

                    status = "[!] RISKY" if risky else "[OK]"
                    print(f"{rule['protocol']:<10} {port_range:<15} {rule['source']:<18} {status}")

                    if risky:
                        finding = {
                            "resource": resource.name,
                            "type": "SecurityGroup",
                            "severity": "HIGH",
                            "issue": f"Port {rule['from_port']} open to the world (0.0.0.0/0)",
                        }
                        self.findings.append(finding)

    def audit_compute(self):
        """Audit compute instances."""
        print("\n" + "=" * 60)
        print("COMPUTE INSTANCE AUDIT")
        print("=" * 60)

        for resource in self.resources:
            if isinstance(resource, ComputeInstance):
                print(f"\nInstance: {resource.name}")
                print(f"  Public IP:     {resource.public_ip}")
                print(f"  Disk Encrypt:  {resource.encryption}")
                print(f"  IMDSv2:        {resource.imds_v2}")
                print(f"  SSM Agent:     {resource.ssm_agent}")

                if not resource.public_ip and resource.encryption == "Disabled":
                    print("  [WARN] Private instance without encryption")

                if resource.public_ip:
                    if resource.imds_v2 == "Optional":
                        finding = {
                            "resource": resource.name,
                            "type": "ComputeInstance",
                            "severity": "MEDIUM",
                            "issue": "Public instance with IMDSv2 optional - metadata service vulnerable",
                        }
                        self.findings.append(finding)
                        print("  [!] IMDSv2 should be required for public instances")

                if resource.encryption == "Disabled":
                    finding = {
                        "resource": resource.name,
                        "type": "ComputeInstance",
                        "severity": "MEDIUM",
                        "issue": "Disk encryption not enabled",
                    }
                    self.findings.append(finding)
                    print("  [!] Disk encryption should be enabled")

    def generate_report(self):
        """Generate audit report."""
        print("\n" + "=" * 60)
        print("CLOUD CONFIGURATION AUDIT REPORT")
        print("=" * 60)

        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1

        total = len(self.findings)
        print(f"\nResources Audited: {len(self.resources)}")
        print(f"Total Findings: {total}")
        for sev, count in severity_counts.items():
            if count > 0:
                print(f"  {sev}: {count}")

        if self.findings:
            print(f"\n{'─' * 60}")
            print("FINDINGS SUMMARY")
            print(f"{'─' * 60}")
            for finding in self.findings:
                print(f"\n[{finding['severity']}] {finding['resource']} ({finding['type']})")
                print(f"  {finding['issue']}")

        print(f"\n{'─' * 60}")
        print("RECOMMENDATIONS")
        print(f"{'─' * 60}")
        print("Security Groups:")
        print("  - Restrict SSH/RDP to specific IP ranges")
        print("  - Don't expose database ports to internet")
        print("  - Use default deny and explicit allows")
        print("\nCompute Instances:")
        print("  - Enable disk encryption by default")
        print("  - Require IMDSv2 on all instances")
        print("  - Minimize public IP usage")
        print("  - Keep SSM/agent software updated")
        print("\nGeneral:")
        print("  - Use Infrastructure as Code with security linting")
        print("  - Enable CloudTrail/activity logging")
        print("  - Implement automated compliance scanning")


def demo_audit():
    """Run a cloud infrastructure audit demo."""
    print("\n" + "=" * 60)
    print("CLOUD INFRASTRUCTURE AUDIT")
    print("=" * 60)

    auditor = CloudAuditor()

    # Create sample resources
    resources = [
        SecurityGroup("web-server-sg"),
        SecurityGroup("database-sg"),
        SecurityGroup("bastion-sg"),
        ComputeInstance("web-server-01"),
        ComputeInstance("app-server-01"),
        ComputeInstance("database-01"),
    ]

    for resource in resources:
        auditor.add_resource(resource)

    auditor.audit_security_groups()
    auditor.audit_compute()
    auditor.generate_report()


def main():
    print("=" * 60)
    print("CLOUD CONFIGURATION AUDITOR")
    print("=" * 60)
    print("Simulate auditing cloud infrastructure for misconfigurations.\n")

    while True:
        print("\nMenu:")
        print("1. Run Cloud Audit Demo")
        print("2. Exit")

        choice = input("\nSelect option (1-2): ").strip()

        if choice == "1":
            demo_audit()
        elif choice == "2":
            print("Audit everything!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
