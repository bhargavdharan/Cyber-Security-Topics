#!/usr/bin/env python3
"""
Threat Modeling Exercise
Interactive threat modeling simulation using STRIDE.
"""


class ThreatModel:
    """Simulates threat modeling for an application."""

    def __init__(self, app_name):
        self.app_name = app_name
        self.components = []
        self.threats = []
        self.mitigations = []

    def add_component(self, name, type_, data_flow):
        self.components.append({"name": name, "type": type_, "data_flow": data_flow})

    def identify_threats(self):
        """Identify threats using STRIDE methodology."""
        print(f"\n{'=' * 60}")
        print(f"THREAT IDENTIFICATION: {self.app_name}")
        print(f"{'=' * 60}")

        stride_categories = {
            "S": "Spoofing - Can an attacker pretend to be someone else?",
            "T": "Tampering - Can an attacker modify data?",
            "R": "Repudiation - Can an attacker deny performing an action?",
            "I": "Information Disclosure - Can data be exposed to unauthorized parties?",
            "D": "Denial of Service - Can the system be made unavailable?",
            "E": "Elevation of Privilege - Can an attacker gain unauthorized access?",
        }

        print("\nSTRIDE Categories:")
        for letter, description in stride_categories.items():
            print(f"  {letter}: {description}")

        # Simulate threat identification
        sample_threats = [
            {
                "id": "T1",
                "component": "Login API",
                "stride": "S",
                "threat": "Attacker spoofs legitimate user credentials",
                "severity": "HIGH",
            },
            {
                "id": "T2",
                "component": "Database",
                "stride": "I",
                "threat": "SQL injection exposes sensitive customer data",
                "severity": "CRITICAL",
            },
            {
                "id": "T3",
                "component": "Session Token",
                "stride": "T",
                "threat": "Attacker intercepts and modifies session token",
                "severity": "HIGH",
            },
            {
                "id": "T4",
                "component": "Audit Log",
                "stride": "R",
                "threat": "Attacker deletes logs to cover tracks",
                "severity": "MEDIUM",
            },
            {
                "id": "T5",
                "component": "API Gateway",
                "stride": "D",
                "threat": "DDoS attack overwhelms API capacity",
                "severity": "MEDIUM",
            },
            {
                "id": "T6",
                "component": "Admin Panel",
                "stride": "E",
                "threat": "Regular user gains admin privileges through parameter tampering",
                "severity": "CRITICAL",
            },
        ]

        self.threats = sample_threats

        print(f"\n{'─' * 60}")
        print("IDENTIFIED THREATS")
        print(f"{'─' * 60}")

        for threat in self.threats:
            print(f"\n{threat['id']}: [{threat['stride']}] {threat['threat']}")
            print(f"  Component: {threat['component']}")
            print(f"  Severity:  {threat['severity']}")

    def plan_mitigations(self):
        """Plan mitigations for identified threats."""
        print(f"\n{'=' * 60}")
        print("MITIGATION PLANNING")
        print(f"{'=' * 60}")

        mitigations = {
            "T1": ["Implement MFA", "Use strong password policy", "Monitor for brute force"],
            "T2": ["Use parameterized queries", "Input validation", "Principle of least privilege for DB"],
            "T3": ["Use HTTPS/TLS", "Implement token binding", "Short token expiration"],
            "T4": ["Immutable audit logs", "SIEM integration", "Alert on log tampering"],
            "T5": ["Rate limiting", "DDoS protection", "Auto-scaling"],
            "T6": ["Server-side authorization checks", "Role-based access control", "Audit all admin actions"],
        }

        for threat in self.threats:
            tid = threat["id"]
            print(f"\n{tid}: {threat['threat']}")
            print("Mitigations:")
            for mitigation in mitigations.get(tid, ["Review and implement controls"]):
                print(f"  - {mitigation}")

    def assess_risk(self):
        """Assess overall risk."""
        print(f"\n{'=' * 60}")
        print("RISK ASSESSMENT")
        print(f"{'=' * 60}")

        severity_scores = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        total_score = sum(severity_scores.get(t["severity"], 0) for t in self.threats)

        print(f"\nTotal Threats: {len(self.threats)}")
        print(f"Risk Score: {total_score}/24")

        if total_score >= 18:
            print("Overall Risk: CRITICAL - Address before release")
        elif total_score >= 12:
            print("Overall Risk: HIGH - Major improvements needed")
        elif total_score >= 6:
            print("Overall Risk: MEDIUM - Some improvements needed")
        else:
            print("Overall Risk: LOW - Minor improvements optional")


def demo_web_app_threat_model():
    """Threat model a web application."""
    model = ThreatModel("E-Commerce Web Application")

    model.add_component("Login API", "API Endpoint", "Username/Password -> Auth Service")
    model.add_component("Product API", "API Endpoint", "Product Data -> Database")
    model.add_component("Payment Gateway", "External Service", "Card Data -> Payment Processor")
    model.add_component("Admin Panel", "Web Interface", "Admin Actions -> Backend")
    model.add_component("Database", "Data Store", "All Application Data")

    model.identify_threats()
    model.plan_mitigations()
    model.assess_risk()


def demo_stride_explanation():
    """Explain STRIDE methodology."""
    print("\n" + "=" * 60)
    print("STRIDE THREAT MODELING FRAMEWORK")
    print("=" * 60)

    stride = {
        "Spoofing": {
            "description": "Pretending to be someone or something else",
            "examples": ["Stolen credentials", "Forged tokens", "DNS spoofing"],
            "mitigation": "Authentication, digital signatures",
        },
        "Tampering": {
            "description": "Modifying data or code",
            "examples": ["SQL injection", "Parameter tampering", "Man-in-the-middle"],
            "mitigation": "Integrity checks, digital signatures, HTTPS",
        },
        "Repudiation": {
            "description": "Denying that an action occurred",
            "examples": ["Deleting audit logs", "Denying transactions"],
            "mitigation": "Audit logging, digital signatures, timestamps",
        },
        "Information Disclosure": {
            "description": "Exposing data to unauthorized parties",
            "examples": ["Data breaches", "Side-channel attacks", "Error messages leaking info"],
            "mitigation": "Encryption, access control, input validation",
        },
        "Denial of Service": {
            "description": "Making the system unavailable",
            "examples": ["DDoS attacks", "Resource exhaustion", "Application crashes"],
            "mitigation": "Rate limiting, redundancy, resource quotas",
        },
        "Elevation of Privilege": {
            "description": "Gaining unauthorized access",
            "examples": ["Privilege escalation", "Vertical/horizontal authorization bypass"],
            "mitigation": "Authorization checks, sandboxing, least privilege",
        },
    }

    for category, details in stride.items():
        print(f"\n[{category}]")
        print(f"  Definition: {details['description']}")
        print(f"  Examples:   {', '.join(details['examples'])}")
        print(f"  Mitigation: {details['mitigation']}")


def main():
    print("=" * 60)
    print("THREAT MODELING EXERCISE")
    print("=" * 60)
    print("Learn threat modeling with STRIDE methodology.\n")

    while True:
        print("\nMenu:")
        print("1. Web Application Threat Model")
        print("2. STRIDE Framework Explanation")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_web_app_threat_model()
        elif choice == "2":
            demo_stride_explanation()
        elif choice == "3":
            demo_web_app_threat_model()
            demo_stride_explanation()
        elif choice == "4":
            print("Threat model everything!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
