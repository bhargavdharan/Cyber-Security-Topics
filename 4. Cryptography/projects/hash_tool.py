#!/usr/bin/env python3
"""
Hash Generator & Verifier
Educational tool for exploring cryptographic hash functions.
"""

import hashlib
import os


def calculate_hash(data, algorithm="sha256"):
    """Calculate hash of data using specified algorithm."""
    if algorithm == "md5":
        return hashlib.md5(data).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(data).hexdigest()
    elif algorithm == "blake2b":
        return hashlib.blake2b(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def hash_string():
    """Hash a user-provided string."""
    text = input("\nEnter text to hash: ")
    data = text.encode()

    print("\n" + "─" * 60)
    print("HASH RESULTS")
    print("─" * 60)

    algorithms = ["md5", "sha1", "sha256", "sha512", "blake2b"]
    for algo in algorithms:
        h = calculate_hash(data, algo)
        print(f"\n{algo.upper():<10} ({len(h)*4} bits)")
        print(f"  {h}")

    # Show avalanche effect
    if len(text) > 0:
        modified = text[:-1] + (chr((ord(text[-1]) + 1) % 128)) if text else "x"
        print("\n" + "─" * 60)
        print("AVALANCHE EFFECT DEMONSTRATION")
        print("─" * 60)
        print(f"Original:    '{text}'")
        print(f"Modified:    '{modified}'")

        orig_hash = calculate_hash(text.encode(), "sha256")
        mod_hash = calculate_hash(modified.encode(), "sha256")

        # Count differing bits
        diff_bits = sum(
            bin(int(a, 16) ^ int(b, 16)).count('1')
            for a, b in zip(orig_hash, mod_hash)
        )

        print(f"\nOriginal SHA-256:  {orig_hash}")
        print(f"Modified SHA-256:  {mod_hash}")
        print(f"\nDiffering bits: {diff_bits} / 256 ({diff_bits/256*100:.1f}%)")
        print("A good hash function should change ~50% of bits for any small change.")


def hash_file():
    """Hash a file."""
    filepath = input("\nEnter file path: ").strip()
    if not os.path.exists(filepath):
        print("File not found.")
        return

    print("\nCalculating hashes...")
    print("─" * 60)

    algorithms = ["md5", "sha1", "sha256", "sha512"]
    for algo in algorithms:
        hasher = hashlib.new(algo)
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        h = hasher.hexdigest()
        print(f"{algo.upper():<10} {h}")


def verify_integrity():
    """Verify a file against a known hash."""
    filepath = input("\nFile to verify: ").strip()
    if not os.path.exists(filepath):
        print("File not found.")
        return

    expected_hash = input("Expected SHA-256 hash: ").strip().lower()
    if len(expected_hash) != 64:
        print("Invalid SHA-256 hash length. Must be 64 hex characters.")
        return

    print("\nVerifying file integrity...")
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    actual_hash = hasher.hexdigest()

    print(f"\nExpected: {expected_hash}")
    print(f"Actual:   {actual_hash}")

    if actual_hash == expected_hash:
        print("\n[PASS] File integrity verified. Hashes match!")
    else:
        print("\n[FAIL] File has been modified or corrupted!")
        # Show differences
        diff = [i for i, (a, b) in enumerate(zip(expected_hash, actual_hash)) if a != b]
        print(f"Differences at positions: {diff[:10]}{'...' if len(diff) > 10 else ''}")


def collision_resistance_demo():
    """Demonstrate why MD5 and SHA-1 are considered broken."""
    print("\n" + "=" * 60)
    print("HASH ALGORITHM SECURITY COMPARISON")
    print("=" * 60)

    algorithms = [
        ("MD5", "128 bits", "BROKEN - Collision attacks feasible since 2004"),
        ("SHA-1", "160 bits", "BROKEN - Google demonstrated collision in 2017"),
        ("SHA-256", "256 bits", "SECURE - No practical attacks known"),
        ("SHA-512", "512 bits", "SECURE - No practical attacks known"),
        ("BLAKE2b", "512 bits", "SECURE - Fast and modern alternative"),
    ]

    print("\n{:<12} {:<12} {:<50}".format("Algorithm", "Output Size", "Security Status"))
    print("─" * 74)
    for name, size, status in algorithms:
        print(f"{name:<12} {size:<12} {status}")

    print("\nWhy MD5/SHA-1 are broken for security:")
    print("  - Attackers can create two DIFFERENT files with the SAME hash")
    print("  - This allows forging digital signatures and certificates")
    print("  - Always use SHA-256 or better for security applications")

    print("\nReal-world impact:")
    print("  - Flame malware (2012) used forged SHA-1 certificates")
    print("  - SHA-1 deprecation in browsers (2017)")
    print("  - MD5 banned in SSL certificates since 2015")


def password_hashing_demo():
    """Demonstrate why plain hashing is insufficient for passwords."""
    print("\n" + "=" * 60)
    print("PASSWORD HASHING CONCEPTS")
    print("=" * 60)

    password = input("Enter a sample password: ") or "password123"
    simple_hash = hashlib.sha256(password.encode()).hexdigest()

    print(f"\nSimple SHA-256 of password: {simple_hash}")
    print("\nPROBLEM: If two users have the same password, they have the same hash!")
    print("Also: Attackers can pre-compute hashes for common passwords (rainbow tables).")

    print("\nSOLUTION: Add a random SALT to each password before hashing")
    import secrets
    salt = secrets.token_hex(16)
    salted = hashlib.sha256((salt + password).encode()).hexdigest()
    print(f"Salt: {salt}")
    print(f"Salted hash: {salted}")

    print("\nBETTER SOLUTION: Use slow hash functions like bcrypt, Argon2, or PBKDF2")
    print("These are designed to be computationally expensive, slowing brute-force attacks.")


def main():
    print("=" * 60)
    print("HASH GENERATOR & VERIFIER")
    print("=" * 60)
    print("Explore cryptographic hash functions interactively.\n")

    while True:
        print("\nMenu:")
        print("1. Hash a String")
        print("2. Hash a File")
        print("3. Verify File Integrity")
        print("4. Algorithm Security Comparison")
        print("5. Password Hashing Concepts")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            hash_string()
        elif choice == "2":
            hash_file()
        elif choice == "3":
            verify_integrity()
        elif choice == "4":
            collision_resistance_demo()
        elif choice == "5":
            password_hashing_demo()
        elif choice == "6":
            print("Hash carefully!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
