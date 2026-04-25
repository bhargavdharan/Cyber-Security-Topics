#!/usr/bin/env python3
"""
Mobile Threat Simulator
Simulates common mobile security threats for educational purposes.
"""

import random


class MobileDevice:
    """Simulates a mobile device."""

    def __init__(self, name, os_type):
        self.name = name
        self.os = os_type
        self.installed_apps = []
        self.network_connections = []
        self.permissions_granted = {}
        self.compromised = False

    def install_app(self, app):
        self.installed_apps.append(app)
        self.permissions_granted[app.name] = app.permissions

    def connect_to_network(self, network_name, secure=True):
        self.network_connections.append({"name": network_name, "secure": secure})


class MobileApp:
    """Simulates a mobile application."""

    def __init__(self, name, developer, permissions=None):
        self.name = name
        self.developer = developer
        self.permissions = permissions or []
        self.behaviors = []

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)


class ThreatSimulator:
    """Simulates mobile threat scenarios."""

    def __init__(self):
        self.threats = []

    def simulate_malicious_app(self):
        """Simulate a malicious app installation."""
        print("\n" + "=" * 60)
        print("SCENARIO: MALICIOUS APP INSTALLATION")
        print("=" * 60)

        device = MobileDevice("User's Phone", "Android")

        # Install legitimate apps
        legit_app = MobileApp("SocialMedia", "TrustedCorp", ["INTERNET", "CAMERA"])
        device.install_app(legit_app)
        print(f"Installed legitimate app: {legit_app.name}")

        # Install malicious app
        malware = MobileApp("SystemOptimizer", "UnknownDev", [
            "INTERNET", "READ_SMS", "READ_CONTACTS", "ACCESS_FINE_LOCATION",
            "SYSTEM_ALERT_WINDOW", "BIND_ACCESSIBILITY_SERVICE"
        ])
        malware.add_behavior("keylogger")
        malware.add_behavior("data_exfiltration")
        malware.add_behavior("ad_fraud")
        device.install_app(malware)

        print(f"\n[!] Installed suspicious app: {malware.name}")
        print(f"Developer: {malware.developer}")
        print(f"Permissions requested:")
        for perm in malware.permissions:
            risk = "HIGH" if perm in ["READ_SMS", "READ_CONTACTS", "BIND_ACCESSIBILITY_SERVICE"] else "MEDIUM"
            print(f"  [{risk}] {perm}")

        print("\nDetected behaviors after installation:")
        for behavior in malware.behaviors:
            print(f"  - {behavior}")

        print("\nINDICATORS OF MALICIOUS APP:")
        print("  - Excessive permissions unrelated to functionality")
        print("  - Unknown/unverified developer")
        print("  - Requested accessibility service (major red flag)")
        print("  - Negative reviews mentioning unwanted behavior")

        print("\nPROTECTION:")
        print("  - Only install from official app stores")
        print("  - Check developer reputation")
        print("  - Review permissions carefully")
        print("  - Use mobile security/anti-malware solutions")

    def simulate_network_interception(self):
        """Simulate network interception on public Wi-Fi."""
        print("\n" + "=" * 60)
        print("SCENARIO: NETWORK INTERCEPTION (MAN-IN-THE-MIDDLE)")
        print("=" * 60)

        device = MobileDevice("User's Phone", "iOS")
        device.connect_to_network("Starbucks_Free_WiFi", secure=False)

        print("\nUser connects to public Wi-Fi at coffee shop...")
        print("Network: Starbucks_Free_WiFi (Open, no password)")

        print("\n--- Attacker Setup ---")
        print("Attacker creates fake access point:")
        print("  Fake AP name: 'Starbucks_Free_WiFi' (same as real)")
        print("  Attacker's device acts as router")
        print("  All traffic routed through attacker")

        print("\n--- Traffic Analysis ---")
        traffic = [
            ("GET http://bank.com/login", "UNENCRYPTED - credentials visible!"),
            ("POST http://shopping.com/checkout", "UNENCRYPTED - credit card exposed!"),
            ("GET https://email.com/inbox", "ENCRYPTED - attacker sees destination only"),
            ("DNS query: bank.com", "VISIBLE - reveals banking activity"),
        ]

        for request, result in traffic:
            print(f"  {request}")
            print(f"    -> {result}")

        print("\nPROTECTION:")
        print("  - Use VPN on all public Wi-Fi")
        print("  - Verify HTTPS on all sensitive sites")
        print("  - Disable auto-connect to open networks")
        print("  - Use mobile data for sensitive transactions")

    def simulate_smishing(self):
        """Simulate SMS phishing attack."""
        print("\n" + "=" * 60)
        print("SCENARIO: SMISHING (SMS PHISHING)")
        print("=" * 60)

        messages = [
            {
                "from": "+1-800-BANK",
                "text": "Your account has been locked. Click to verify: http://bank-secure-verify.com/login",
                "indicators": ["Urgency", "Suspicious link", "Not from official number"],
            },
            {
                "from": "DeliveryService",
                "text": "Package delivery failed. Pay $2.99 redelivery fee: http://bit.ly/deliver-pkg",
                "indicators": ["Unexpected fee", "URL shortener", "Not expecting package"],
            },
            {
                "from": "TaxAgency",
                "text": "You have a tax refund pending. Click to claim: http://tax-refund-now.com",
                "indicators": ["Too good to be true", "Suspicious domain", "Urgency"],
            },
        ]

        for msg in messages:
            print(f"\nFrom: {msg['from']}")
            print(f"Message: {msg['text']}")
            print("Red flags:")
            for indicator in msg['indicators']:
                print(f"  - {indicator}")

        print("\nPROTECTION:")
        print("  - Never click links in SMS from unknown senders")
        print("  - Verify through official app or website directly")
        print("  - Check sender number against known official numbers")
        print("  - Report spam/phishing to carrier")

    def simulate_device_compromise(self):
        """Simulate indicators of device compromise."""
        print("\n" + "=" * 60)
        print("SCENARIO: DEVICE COMPROMISE INDICATORS")
        print("=" * 60)

        indicators = [
            ("Battery drains unusually fast", "Malware running in background"),
            ("Phone heats up when not in use", "Cryptominer or spyware active"),
            ("Unknown apps appear", "Malware installed itself"),
            ("Data usage spikes", "Large data exfiltration"),
            ("Pop-ups and ads everywhere", "Adware infection"),
            ("Apps crash frequently", "System instability from rootkit"),
            ("Unusual SMS sent from your number", "Premium SMS malware"),
            ("Camera/mic indicators light up unexpectedly", "Spyware accessing sensors"),
        ]

        print("\nWarning signs your device may be compromised:")
        print(f"\n{'Indicator':<40} {'Possible Cause'}")
        print("─" * 70)
        for indicator, cause in indicators:
            print(f"{indicator:<40} {cause}")

        print("\nWHAT TO DO IF COMPROMISED:")
        print("  1. Disconnect from internet immediately")
        print("  2. Run anti-malware scan from reputable vendor")
        print("  3. Remove suspicious apps")
        print("  4. Change all passwords from a clean device")
        print("  5. Check for unauthorized account access")
        print("  6. Factory reset if compromise confirmed")
        print("  7. Restore from clean backup only")


def main():
    print("=" * 60)
    print("MOBILE THREAT SIMULATOR")
    print("=" * 60)
    print("Learn to recognize and protect against mobile threats.\n")

    simulator = ThreatSimulator()

    while True:
        print("\nMenu:")
        print("1. Malicious App Installation")
        print("2. Network Interception (Public Wi-Fi)")
        print("3. Smishing (SMS Phishing)")
        print("4. Device Compromise Indicators")
        print("5. Run All Scenarios")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            simulator.simulate_malicious_app()
        elif choice == "2":
            simulator.simulate_network_interception()
        elif choice == "3":
            simulator.simulate_smishing()
        elif choice == "4":
            simulator.simulate_device_compromise()
        elif choice == "5":
            simulator.simulate_malicious_app()
            simulator.simulate_network_interception()
            simulator.simulate_smishing()
            simulator.simulate_device_compromise()
        elif choice == "6":
            print("Stay safe on mobile!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
