#!/usr/bin/env python3
"""
Secure Storage Demo
Demonstrates secure vs insecure mobile data storage practices.
"""

import base64
import hashlib
import json
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class InsecureStorage:
    """Simulates insecure mobile data storage."""

    def __init__(self, app_name):
        self.app_name = app_name
        self.storage_path = f"/data/data/{app_name}/"

    def save_credentials(self, username, password):
        """Save credentials in plaintext (DANGEROUS)."""
        data = {
            "username": username,
            "password": password,
        }
        filepath = f"{self.storage_path}credentials.json"
        print(f"\n[INSECURE] Saving to: {filepath}")
        print(f"Content: {json.dumps(data, indent=2)}")
        print("RISK: Any app with storage access can read this!")
        return filepath

    def save_preferences(self, api_key, auth_token):
        """Save sensitive data in SharedPreferences (INSECURE)."""
        prefs = {
            "api_key": api_key,
            "auth_token": auth_token,
            "user_id": "12345",
        }
        filepath = f"{self.storage_path}shared_prefs/app_settings.xml"
        print(f"\n[INSECURE] Saving to SharedPreferences: {filepath}")
        print(f"Content: {json.dumps(prefs, indent=2)}")
        print("RISK: SharedPreferences are stored in plaintext XML!")
        return prefs


class SecureStorage:
    """Simulates secure mobile data storage."""

    def __init__(self, app_name):
        self.app_name = app_name
        self.storage_path = f"/data/data/{app_name}/"
        self._init_keystore()

    def _init_keystore(self):
        """Simulate Android Keystore / iOS Keychain initialization."""
        # In real apps, this uses hardware-backed keystore
        self.master_key = Fernet.generate_key()
        self.cipher = Fernet(self.master_key)
        print(f"\n[SECURE] Hardware-backed keystore initialized")
        print(f"Master key stored in: Android Keystore / iOS Keychain")

    def encrypt_data(self, data):
        """Encrypt data before storage."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        """Decrypt data from storage."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def save_credentials(self, username, password):
        """Save credentials securely."""
        encrypted_password = self.encrypt_data(password)
        data = {
            "username": username,
            "password_encrypted": encrypted_password,
            "encryption": "AES-256-GCM (Keystore-backed)",
        }
        filepath = f"{self.storage_path}secure/credentials.enc"
        print(f"\n[SECURE] Saving to: {filepath}")
        print(f"Encrypted content: {encrypted_password[:50]}...")
        print("PROTECTION: Data encrypted with hardware-backed key")
        return filepath

    def save_api_key(self, api_key):
        """Save API key in secure storage."""
        encrypted = self.encrypt_data(api_key)
        print(f"\n[SECURE] API key encrypted and stored in Keystore")
        print(f"Encrypted: {encrypted[:40]}...")
        return encrypted


def demo_insecure_vs_secure():
    """Compare insecure and secure storage side by side."""
    print("\n" + "=" * 60)
    print("INSECURE vs SECURE STORAGE COMPARISON")
    print("=" * 60)

    username = "john_doe"
    password = "MyS3cr3tP@ss!"
    api_key = "sk_live_abcdef123456789"

    print("\n" + "─" * 60)
    print("SCENARIO: Storing user credentials")
    print("─" * 60)

    # Insecure
    insecure = InsecureStorage("com.example.badapp")
    insecure.save_credentials(username, password)

    # Secure
    secure = SecureStorage("com.example.goodapp")
    secure.save_credentials(username, password)

    print("\n" + "─" * 60)
    print("SCENARIO: Storing API keys")
    print("─" * 60)

    insecure.save_preferences(api_key, "token_12345")
    secure.save_api_key(api_key)


def demo_data_extraction():
    """Simulate how attackers extract data from insecure storage."""
    print("\n" + "=" * 60)
    print("DATA EXTRACTION SIMULATION")
    print("=" * 60)

    print("\nAttacker gains access to device backup or rooted device...")
    print("\n--- Insecure App ---")
    print("Files found:")
    print("  /data/data/com.example.badapp/credentials.json")
    print("    -> Contains: username + password in PLAINTEXT")
    print("  /data/data/com.example.badapp/shared_prefs/app_settings.xml")
    print("    -> Contains: API keys and auth tokens in PLAINTEXT")
    print("\nResult: FULL ACCOUNT TAKEOVER possible")

    print("\n--- Secure App ---")
    print("Files found:")
    print("  /data/data/com.example.goodapp/secure/credentials.enc")
    print("    -> Contains: Encrypted data (unreadable without keystore key)")
    print("  Android Keystore / iOS Keychain")
    print("    -> Hardware-backed, extraction extremely difficult")
    print("\nResult: Data protected even if storage is compromised")


def demo_best_practices():
    """Show mobile storage security best practices."""
    print("\n" + "=" * 60)
    print("MOBILE STORAGE SECURITY BEST PRACTICES")
    print("=" * 60)

    practices = [
        ("NEVER store passwords in plaintext", "Use platform Keystore/Keychain"),
        ("NEVER store API keys in code", "Use secure cloud configuration"),
        ("NEVER use SharedPreferences for sensitive data", "Use EncryptedSharedPreferences"),
        ("NEVER log sensitive data", "Sanitize logs before shipping"),
        ("NEVER rely on device encryption alone", "App-level encryption for critical data"),
        ("ALWAYS use hardware-backed keys when available", "Require StrongBox on Android"),
        ("ALWAYS clear sensitive data from memory", "Use secure memory handling"),
        ("ALWAYS validate data integrity", "Use HMAC for tamper detection"),
    ]

    print(f"\n{'DON\'T':<45} {'DO INSTEAD'}")
    print("─" * 70)
    for dont, do in practices:
        print(f"{dont:<45} {do}")

    print("\nPlatform-Specific Recommendations:")
    print("\nAndroid:")
    print("  - EncryptedSharedPreferences (AndroidX Security)")
    print("  - Android Keystore System (hardware-backed when available)")
    print("  - BiometricPrompt for sensitive operations")
    print("\niOS:")
    print("  - Keychain Services (kSecAttrAccessible levels)")
    print("  - Data Protection API (NSFileProtectionComplete)")
    print("  - Secure Enclave for cryptographic operations")


def main():
    print("=" * 60)
    print("SECURE STORAGE DEMO")
    print("=" * 60)
    print("Learn how to protect sensitive data on mobile devices.\n")

    while True:
        print("\nMenu:")
        print("1. Insecure vs Secure Storage Comparison")
        print("2. Data Extraction Simulation")
        print("3. Best Practices")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_insecure_vs_secure()
        elif choice == "2":
            demo_data_extraction()
        elif choice == "3":
            demo_best_practices()
        elif choice == "4":
            demo_insecure_vs_secure()
            demo_data_extraction()
            demo_best_practices()
        elif choice == "5":
            print("Encrypt everything!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
