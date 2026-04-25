#!/usr/bin/env python3
"""
VPN Tunnel Simulator
Demonstrates how VPNs encrypt and encapsulate network traffic.
"""

from cryptography.fernet import Fernet


class VPNTunnel:
    """Simulates a VPN tunnel with encryption."""

    def __init__(self, name):
        self.name = name
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.connected = False
        self.client_ip = None
        self.server_ip = None

    def connect(self, client_ip, server_ip):
        """Establish VPN connection."""
        print(f"\n[{self.name}] Establishing connection...")
        print(f"  Client: {client_ip}")
        print(f"  Server: {server_ip}")
        print(f"  Key exchanged: {self.key.decode()[:20]}...")

        self.client_ip = client_ip
        self.server_ip = server_ip
        self.connected = True

        print(f"  Status: CONNECTED")
        print(f"  Virtual IP assigned: 10.8.0.2 (client), 10.8.0.1 (server)")

    def encrypt_packet(self, packet):
        """Encrypt a packet for tunnel transmission."""
        if not self.connected:
            raise Exception("Tunnel not connected")

        plaintext = str(packet).encode()
        ciphertext = self.cipher.encrypt(plaintext)
        return ciphertext

    def decrypt_packet(self, ciphertext):
        """Decrypt a packet from tunnel transmission."""
        if not self.connected:
            raise Exception("Tunnel not connected")

        plaintext = self.cipher.decrypt(ciphertext)
        return eval(plaintext.decode())

    def encapsulate(self, original_packet):
        """Wrap original packet in VPN outer packet."""
        encrypted_payload = self.encrypt_packet(original_packet)

        # Outer packet (what ISP/router sees)
        outer_packet = {
            "src": self.client_ip,
            "dst": self.server_ip,
            "protocol": "UDP",
            "port": 1194,  # OpenVPN default
            "payload": encrypted_payload,
            "size": len(encrypted_payload),
        }
        return outer_packet

    def display_packet_comparison(self, original):
        """Show before/after VPN encapsulation."""
        outer = self.encapsulate(original)

        print(f"\n{'─' * 60}")
        print("PACKET COMPARISON")
        print(f"{'─' * 60}")

        print("\nWITHOUT VPN (ISP/Router sees everything):")
        print(f"  Source:      {original['src']}")
        print(f"  Destination: {original['dst']}")
        print(f"  Protocol:    {original['protocol']}")
        print(f"  Port:        {original['port']}")
        print(f"  Payload:     {original['payload'][:60]}...")

        print("\nWITH VPN (ISP/Router sees encrypted tunnel):")
        print(f"  Source:      {outer['src']}")
        print(f"  Destination: {outer['dst']}")
        print(f"  Protocol:    {outer['protocol']}")
        print(f"  Port:        {outer['port']} (VPN port)")
        print(f"  Payload:     [ENCRYPTED] {outer['payload'][:30]}...")
        print(f"  Size:        {outer['size']} bytes")

        print("\nDestination server decrypts to reveal:")
        decrypted = self.decrypt_packet(outer['payload'])
        print(f"  Original destination: {decrypted['dst']}")
        print(f"  Original payload:     {decrypted['payload'][:60]}...")


def demo_site_to_site():
    """Demonstrate site-to-site VPN."""
    print("\n" + "=" * 60)
    print("SITE-TO-SITE VPN DEMO")
    print("=" * 60)
    print("Connecting two office networks securely over the internet.\n")

    tunnel = VPNTunnel("Office-A-to-Office-B")
    tunnel.connect("203.0.113.10", "198.51.100.20")

    packet = {
        "src": "10.0.1.50 (HR server)",
        "dst": "10.0.2.100 (Finance DB)",
        "protocol": "TCP",
        "port": 1433,
        "payload": "SELECT * FROM employee_salaries WHERE department='HR'",
    }

    tunnel.display_packet_comparison(packet)

    print("\nBenefits:")
    print("  - Internet traffic is encrypted (ISP cannot read contents)")
    print("  - Private IPs are hidden from public internet")
    print("  - No need for dedicated leased lines between offices")


def demo_remote_access():
    """Demonstrate remote access VPN."""
    print("\n" + "=" * 60)
    print("REMOTE ACCESS VPN DEMO")
    print("=" * 60)
    print("Employee working from home accessing corporate resources.\n")

    tunnel = VPNTunnel("Remote-Worker-VPN")
    tunnel.connect("192.168.1.100 (home)", "203.0.113.5 (office VPN)")

    packet = {
        "src": "192.168.1.100 (laptop)",
        "dst": "10.0.0.50 (internal file server)",
        "protocol": "SMB",
        "port": 445,
        "payload": "ACCESS \\fileserver\payroll\q4_salaries.xlsx",
    }

    tunnel.display_packet_comparison(packet)

    print("\nWithout VPN:")
    print("  - Cannot access 10.0.0.x from home (private IP range)")
    print("  - If exposed, data travels unencrypted over internet")

    print("\nWith VPN:")
    print("  - Employee gets virtual IP in corporate range (10.8.0.x)")
    print("  - All traffic encrypted between laptop and VPN server")
    print("  - Can access internal resources as if in the office")


def demo_split_tunnel():
    """Demonstrate split tunneling concepts."""
    print("\n" + "=" * 60)
    print("SPLIT TUNNELING DEMO")
    print("=" * 60)
    print("Compare full tunnel vs split tunnel VPN configurations.\n")

    print("FULL TUNNEL (all traffic through VPN):")
    routes = [
        ("10.0.0.0/8", "VPN tunnel", "Corporate network"),
        ("0.0.0.0/0", "VPN tunnel", "Internet (via office)"),
    ]
    for network, path, desc in routes:
        print(f"  {network:<18} -> {path:<15} ({desc})")
    print("  Pros: All traffic encrypted, central filtering")
    print("  Cons: Slower internet, more bandwidth on office connection")

    print("\nSPLIT TUNNEL (only corporate traffic through VPN):")
    routes = [
        ("10.0.0.0/8", "VPN tunnel", "Corporate network"),
        ("0.0.0.0/0", "Direct", "Internet (via home ISP)"),
    ]
    for network, path, desc in routes:
        print(f"  {network:<18} -> {path:<15} ({desc})")
    print("  Pros: Faster internet, less office bandwidth")
    print("  Cons: Personal traffic not protected by corporate security")


def main():
    print("=" * 60)
    print("VPN TUNNEL SIMULATOR")
    print("=" * 60)
    print("Learn how Virtual Private Networks protect data in transit.\n")

    while True:
        print("\nMenu:")
        print("1. Site-to-Site VPN")
        print("2. Remote Access VPN")
        print("3. Split Tunneling Concepts")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_site_to_site()
        elif choice == "2":
            demo_remote_access()
        elif choice == "3":
            demo_split_tunnel()
        elif choice == "4":
            demo_site_to_site()
            demo_remote_access()
            demo_split_tunnel()
        elif choice == "5":
            print("Encrypt everything!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
