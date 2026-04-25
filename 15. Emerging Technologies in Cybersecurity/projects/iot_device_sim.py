#!/usr/bin/env python3
"""
IoT Device Simulator
Simulates IoT device security configurations and communications.
"""

import hashlib
import json
import random
import secrets


class IoTDevice:
    """Base class for IoT devices."""

    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.connected = False
        self.firmware_version = "1.0.0"
        self.data = {}

    def connect(self):
        self.connected = True
        print(f"{self.name} connected")

    def disconnect(self):
        self.connected = False
        print(f"{self.name} disconnected")


class InsecureIoTDevice(IoTDevice):
    """Simulates an insecure IoT device."""

    def __init__(self, name, device_type):
        super().__init__(name, device_type)
        self.password = "admin"  # Default password
        self.use_encryption = False
        self.auth_token = "token123"  # Predictable token

    def send_data(self, data):
        """Send data without encryption."""
        print(f"\n[INSECURE] {self.name} sending data:")
        print(f"  Payload: {json.dumps(data)}")
        print(f"  Encryption: None")
        print(f"  Authentication: Basic password '{self.password}'")
        print("  RISK: Anyone on the network can intercept and read this!")

    def update_firmware(self, firmware_url):
        """Update firmware without verification."""
        print(f"\n[INSECURE] {self.name} updating firmware from {firmware_url}")
        print("  Signature verification: SKIPPED")
        print("  Source authentication: NONE")
        print("  RISK: Malicious firmware could be installed!")


class SecureIoTDevice(IoTDevice):
    """Simulates a secure IoT device."""

    def __init__(self, name, device_type):
        super().__init__(name, device_type)
        self.certificate = secrets.token_hex(32)
        self.use_encryption = True
        self.auth_token = secrets.token_urlsafe(32)

    def send_data(self, data):
        """Send encrypted data."""
        encrypted = self._encrypt(json.dumps(data))
        print(f"\n[SECURE] {self.name} sending data:")
        print(f"  Encrypted payload: {encrypted[:50]}...")
        print(f"  Encryption: AES-256-GCM")
        print(f"  Authentication: X.509 certificate")
        print("  SECURE: Data is confidential and authenticated")

    def _encrypt(self, data):
        """Simulate encryption."""
        return hashlib.sha256((data + self.certificate).encode()).hexdigest()

    def update_firmware(self, firmware_url, signature):
        """Update firmware with verification."""
        print(f"\n[SECURE] {self.name} updating firmware:")
        print(f"  URL: {firmware_url}")
        print(f"  Signature: {signature[:40]}...")
        print("  Verification: PASSED")
        print("  Rollback protection: ENABLED")
        print("  SECURE: Only signed firmware from trusted source accepted")


def demo_device_comparison():
    """Compare secure vs insecure IoT devices."""
    print("\n" + "=" * 60)
    print("IoT DEVICE SECURITY COMPARISON")
    print("=" * 60)

    insecure = InsecureIoTDevice("CheapCamera", "Camera")
    secure = SecureIoTDevice("SecureCamera", "Camera")

    print("\n--- Insecure Device ---")
    insecure.connect()
    insecure.send_data({"temperature": 25.5, "motion": True})
    insecure.update_firmware("http://updates.example.com/firmware.bin")

    print("\n--- Secure Device ---")
    secure.connect()
    secure.send_data({"temperature": 25.5, "motion": True})
    secure.update_firmware("https://updates.example.com/firmware.bin",
                           "sha256:abcd1234...")


def demo_iot_attack_scenarios():
    """Demonstrate IoT attack scenarios."""
    print("\n" + "=" * 60)
    print("IoT ATTACK SCENARIOS")
    print("=" * 60)

    scenarios = [
        {
            "name": "Mirai Botnet Recruitment",
            "vector": "Default credentials on IoT cameras and routers",
            "impact": "Device recruited into DDoS botnet",
            "prevention": "Change default passwords, disable Telnet",
        },
        {
            "name": "Smart Home Invasion",
            "vector": "Unencrypted communication from smart lock",
            "impact": "Attacker unlocks door remotely",
            "prevention": "End-to-end encryption, certificate pinning",
        },
        {
            "name": "Medical Device Tampering",
            "vector": "Unauthenticated firmware update on insulin pump",
            "impact": "Dosage manipulation, patient harm",
            "prevention": "Signed firmware, secure boot, FDA guidance",
        },
        {
            "name": "Industrial Sensor Spoofing",
            "vector": "Unauthenticated MQTT messages",
            "impact": "False sensor data causes process failures",
            "prevention": "MQTT authentication, TLS encryption, message signing",
        },
    ]

    for scenario in scenarios:
        print(f"\n[{scenario['name']}]")
        print(f"  Attack Vector: {scenario['vector']}")
        print(f"  Impact:        {scenario['impact']}")
        print(f"  Prevention:    {scenario['prevention']}")


def demo_mqtt_security():
    """Demonstrate MQTT security concepts."""
    print("\n" + "=" * 60)
    print("MQTT SECURITY FOR IoT")
    print("=" * 60)

    print("\nInsecure MQTT Configuration:")
    print("  Broker: mqtt://broker.local:1883 (plaintext)")
    print("  Auth:   None (allow anonymous)")
    print("  ACL:    None (anyone can publish/subscribe to any topic)")
    print("  Result: Anyone can read/control all devices!")

    print("\nSecure MQTT Configuration:")
    print("  Broker: mqtts://broker.local:8883 (TLS)")
    print("  Auth:   Username/password or client certificates")
    print("  ACL:    Per-device topic restrictions")
    print("  Result: Encrypted, authenticated, authorized communication")

    print("\nAdditional IoT Security Best Practices:")
    print("  - Network segmentation (IoT VLAN isolated from corporate)")
    print("  - Device discovery and inventory")
    print("  - Automated vulnerability scanning")
    print("  - Secure Over-the-Air (OTA) updates")
    print("  - Hardware security modules (HSM) for key storage")


def main():
    print("=" * 60)
    print("IoT DEVICE SIMULATOR")
    print("=" * 60)
    print("Learn IoT security through device simulations.\n")

    while True:
        print("\nMenu:")
        print("1. Secure vs Insecure Device Comparison")
        print("2. IoT Attack Scenarios")
        print("3. MQTT Security Concepts")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_device_comparison()
        elif choice == "2":
            demo_iot_attack_scenarios()
        elif choice == "3":
            demo_mqtt_security()
        elif choice == "4":
            demo_device_comparison()
            demo_iot_attack_scenarios()
            demo_mqtt_security()
        elif choice == "5":
            print("Secure all the things!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
