#!/usr/bin/env python3
"""
IOC Analyzer
Tool for analyzing and classifying Indicators of Compromise.
"""

import hashlib
import ipaddress
import re


class IOCAnalyzer:
    """Analyzes Indicators of Compromise."""

    def __init__(self):
        self.threat_intel_db = {
            "ips": ["203.0.113.77", "198.51.100.50", "192.0.2.100"],
            "domains": ["evil-c2.xyz", "malware-dl.com", "phishing-bank.net"],
            "hashes": [
                "d41d8cd98f00b204e9800998ecf8427e",
                "e99a18c428cb38d5f260853678922e03",
            ],
        }

    def classify_ioc(self, value):
        """Classify the type of IOC."""
        # Check if IP address
        try:
            ipaddress.ip_address(value)
            return "IP_ADDRESS"
        except ValueError:
            pass

        # Check if hash
        if re.match(r'^[a-fA-F0-9]{32}$', value):
            return "MD5_HASH"
        if re.match(r'^[a-fA-F0-9]{40}$', value):
            return "SHA1_HASH"
        if re.match(r'^[a-fA-F0-9]{64}$', value):
            return "SHA256_HASH"

        # Check if domain
        if re.match(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', value):
            return "DOMAIN"

        # Check if email
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            return "EMAIL"

        return "UNKNOWN"

    def check_reputation(self, ioc_type, value):
        """Check if IOC is in threat intelligence database."""
        if ioc_type == "IP_ADDRESS" and value in self.threat_intel_db["ips"]:
            return "MALICIOUS", "Known malicious IP"
        if ioc_type == "DOMAIN" and value in self.threat_intel_db["domains"]:
            return "MALICIOUS", "Known malicious domain"
        if ioc_type in ["MD5_HASH", "SHA1_HASH", "SHA256_HASH"] and value in self.threat_intel_db["hashes"]:
            return "MALICIOUS", "Known malware hash"

        return "UNKNOWN", "Not in threat intelligence database"

    def analyze(self, value):
        """Full analysis of an IOC."""
        print(f"\n{'─' * 60}")
        print(f"ANALYZING: {value}")
        print(f"{'─' * 60}")

        ioc_type = self.classify_ioc(value)
        print(f"Type: {ioc_type}")

        if ioc_type == "UNKNOWN":
            print("Could not determine IOC type")
            return

        reputation, reason = self.check_reputation(ioc_type, value)
        print(f"Reputation: {reputation}")
        print(f"Reason: {reason}")

        # Type-specific analysis
        if ioc_type == "IP_ADDRESS":
            self._analyze_ip(value)
        elif ioc_type == "DOMAIN":
            self._analyze_domain(value)
        elif ioc_type in ["MD5_HASH", "SHA1_HASH", "SHA256_HASH"]:
            self._analyze_hash(value)

    def _analyze_ip(self, ip):
        """Analyze IP address characteristics."""
        try:
            addr = ipaddress.ip_address(ip)
            print(f"Version: IPv{addr.version}")
            print(f"Private: {addr.is_private}")
            print(f"Loopback: {addr.is_loopback}")
            print(f"Multicast: {addr.is_multicast}")
            print(f"Reserved: {addr.is_reserved}")

            if addr.is_private:
                print("Note: Private IP - likely internal lateral movement indicator")
            if addr.is_global:
                print("Note: Public IP - possible C2 or exfiltration destination")
        except Exception as e:
            print(f"Error analyzing IP: {e}")

    def _analyze_domain(self, domain):
        """Analyze domain characteristics."""
        print(f"Length: {len(domain)} characters")

        # Check for suspicious patterns
        suspicious = []
        if len(domain) > 30:
            suspicious.append("Unusually long domain")
        if domain.count('-') > 2:
            suspicious.append("Excessive hyphens")
        if re.search(r'\d{4,}', domain):
            suspicious.append("Many consecutive digits")
        if any(domain.endswith(tld) for tld in ['.tk', '.ml', '.ga', '.cf']):
            suspicious.append("Free TLD commonly abused")

        if suspicious:
            print("Suspicious patterns detected:")
            for s in suspicious:
                print(f"  - {s}")
        else:
            print("No obvious suspicious patterns")

    def _analyze_hash(self, hash_value):
        """Analyze hash characteristics."""
        hash_types = {
            32: "MD5",
            40: "SHA-1",
            64: "SHA-256",
        }
        htype = hash_types.get(len(hash_value), "Unknown")
        print(f"Algorithm: {htype}")

        if htype == "MD5":
            print("Warning: MD5 is cryptographically broken. Collisions possible.")
        elif htype == "SHA-1":
            print("Warning: SHA-1 is deprecated. Use SHA-256 for verification.")

        print(f"Entropy check: Valid {htype} format")


def demo_batch_analysis():
    """Analyze multiple IOCs."""
    print("\n" + "=" * 60)
    print("BATCH IOC ANALYSIS")
    print("=" * 60)

    analyzer = IOCAnalyzer()

    iocs = [
        "203.0.113.77",
        "evil-c2.xyz",
        "d41d8cd98f00b204e9800998ecf8427e",
        "192.168.1.100",
        "google.com",
        "e99a18c428cb38d5f260853678922e03",
        "10.0.0.5",
        "suspicious-site-12345.tk",
    ]

    for ioc in iocs:
        analyzer.analyze(ioc)
        input("\nPress Enter for next IOC...")


def demo_ioc_extraction():
    """Extract IOCs from text."""
    print("\n" + "=" * 60)
    print("IOC EXTRACTION FROM TEXT")
    print("=" * 60)

    sample_text = """
    On 2024-03-15, we observed suspicious activity from IP 203.0.113.77.
    The attacker domain was evil-c2.xyz and the malware hash was
    d41d8cd98f00b204e9800998ecf8427e. Additional contact was made to
    198.51.100.50 and backup C2 at malware-dl.com.
    """

    print("\nSample text:")
    print(sample_text)

    # Extract IPs
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ips = re.findall(ip_pattern, sample_text)

    # Extract domains
    domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    domains = re.findall(domain_pattern, sample_text)

    # Extract hashes
    hash_pattern = r'\b[a-fA-F0-9]{32}\b'
    hashes = re.findall(hash_pattern, sample_text)

    print("Extracted IOCs:")
    print(f"  IPs: {ips}")
    print(f"  Domains: {domains}")
    print(f"  Hashes: {hashes}")


def main():
    print("=" * 60)
    print("IOC ANALYZER")
    print("=" * 60)
    print("Analyze and classify Indicators of Compromise.\n")

    analyzer = IOCAnalyzer()

    while True:
        print("\nMenu:")
        print("1. Analyze Single IOC")
        print("2. Batch Analysis Demo")
        print("3. IOC Extraction from Text")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            value = input("Enter IOC to analyze: ").strip()
            if value:
                analyzer.analyze(value)
        elif choice == "2":
            demo_batch_analysis()
        elif choice == "3":
            demo_ioc_extraction()
        elif choice == "4":
            print("Hunt those threats!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
