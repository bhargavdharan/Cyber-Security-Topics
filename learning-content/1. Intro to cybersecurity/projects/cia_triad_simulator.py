#!/usr/bin/env python3
"""
CIA Triad Simulator
Demonstrates Confidentiality, Integrity, and Availability principles
through interactive simulations.
"""

import hashlib
import random
import string
import time


def demonstrate_confidentiality():
    """Demonstrate confidentiality using a Caesar cipher."""
    print("\n" + "=" * 60)
    print("CONFIDENTIALITY DEMO")
    print("=" * 60)
    print("Confidentiality ensures that information is accessible only")
    print("to authorized individuals.\n")

    message = input("Enter a secret message to encrypt: ") or "Hello, Secret World!"
    shift = int(input("Enter shift key (1-25) [default: 3]: ") or "3")

    # Caesar cipher encryption
    encrypted = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char

    print(f"\nOriginal Message: {message}")
    print(f"Encrypted Message:  {encrypted}")
    print(f"Shift Key:          {shift}")
    print("\n[Simulation] Only someone with the shift key can decrypt this!")

    # Decrypt to verify
    decrypted = ""
    for char in encrypted:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            decrypted += chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted += char

    print(f"Decrypted Message:  {decrypted}")
    print("\nNote: In real systems, we use strong algorithms like AES-256,")
    print("not Caesar cipher, which is easily broken with brute force.")


def demonstrate_integrity():
    """Demonstrate integrity using hash verification."""
    print("\n" + "=" * 60)
    print("INTEGRITY DEMO")
    print("=" * 60)
    print("Integrity ensures that data is accurate and has not been")
    print("tampered with.\n")

    original_text = input("Enter some text to hash [default: 'Important Document']: ") or "Important Document"

    # Generate hash of original
    original_hash = hashlib.sha256(original_text.encode()).hexdigest()
    print(f"\nOriginal Text: {original_text}")
    print(f"SHA-256 Hash:  {original_hash}")

    # Simulate tampering
    print("\n--- Simulating Data Tampering ---")
    tampered_text = original_text.replace("Document", "Data")
    if tampered_text == original_text:
        tampered_text = original_text + " (modified)"

    tampered_hash = hashlib.sha256(tampered_text.encode()).hexdigest()
    print(f"Tampered Text: {tampered_text}")
    print(f"New Hash:      {tampered_hash}")

    # Verify integrity
    print("\n--- Integrity Verification ---")
    if original_hash == tampered_hash:
        print("PASS: Data integrity verified. Hashes match.")
    else:
        print("FAIL: Data has been tampered with!")
        print("Hash mismatch detected.")

    print("\nIn production, digital signatures combine hashing with")
    print("asymmetric encryption to verify both integrity AND authenticity.")


def demonstrate_availability():
    """Simulate availability monitoring."""
    print("\n" + "=" * 60)
    print("AVAILABILITY DEMO")
    print("=" * 60)
    print("Availability ensures systems are accessible when needed.\n")

    service_name = input("Enter service name [default: 'Web Server']: ") or "Web Server"
    check_count = int(input("Number of availability checks [default: 10]: ") or "10")
    failure_rate = float(input("Simulated failure rate (0.0 - 1.0) [default: 0.2]: ") or "0.2")

    print(f"\nMonitoring {service_name} for {check_count} cycles...\n")

    uptime_count = 0
    for i in range(1, check_count + 1):
        is_up = random.random() > failure_rate
        status = "UP" if is_up else "DOWN"
        symbol = "OK" if is_up else "FAIL"

        if is_up:
            uptime_count += 1
            response_time = random.randint(10, 200)
        else:
            response_time = "TIMEOUT"

        print(f"Check #{i:02d}: [{symbol}] {service_name} is {status} | Response: {response_time}ms")
        time.sleep(0.3)

    availability_pct = (uptime_count / check_count) * 100
    print(f"\n{'=' * 60}")
    print(f"AVAILABILITY REPORT")
    print(f"{'=' * 60}")
    print(f"Total Checks:   {check_count}")
    print(f"Uptime Count:   {uptime_count}")
    print(f"Downtime Count: {check_count - uptime_count}")
    print(f"Availability:   {availability_pct:.1f}%")

    if availability_pct >= 99.9:
        print("Status: EXCELLENT (Three 9's)")
    elif availability_pct >= 99.0:
        print("Status: GOOD (Two 9's)")
    elif availability_pct >= 95.0:
        print("Status: ACCEPTABLE")
    else:
        print("Status: CRITICAL - Service needs attention!")

    print("\nReal-world availability targets:")
    print("  99.9%   = 8.76 hours downtime/year")
    print("  99.99%  = 52.56 minutes downtime/year")
    print("  99.999% = 5.26 minutes downtime/year")


def main():
    print("=" * 60)
    print("CIA TRIAD SIMULATOR")
    print("Cybersecurity Fundamentals - Interactive Demo")
    print("=" * 60)

    while True:
        print("\nSelect a principle to demonstrate:")
        print("1. Confidentiality (Encryption Demo)")
        print("2. Integrity (Hash Verification Demo)")
        print("3. Availability (Uptime Monitoring Demo)")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            demonstrate_confidentiality()
        elif choice == "2":
            demonstrate_integrity()
        elif choice == "3":
            demonstrate_availability()
        elif choice == "4":
            demonstrate_confidentiality()
            demonstrate_integrity()
            demonstrate_availability()
        elif choice == "5":
            print("\nThank you for using the CIA Triad Simulator!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
