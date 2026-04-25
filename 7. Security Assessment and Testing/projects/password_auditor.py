#!/usr/bin/env python3
"""
Password Security Auditor
Educational tool for understanding password strength and cracking concepts.

WARNING: For educational purposes only. Only test passwords you own.
"""

import hashlib
import math
import time


COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "letmein", "dragon", "111111", "baseball",
    "iloveyou", "trustno1", "sunshine", "princess", "admin",
    "welcome", "shadow", "ashley", "football", "jesus",
    "mustang", "access", "love", "pussy", "696969",
    "qwertyuiop", "superman", "harley", "batman", "master",
]


def estimate_crack_time(password):
    """Estimate time to brute force a password."""
    # Estimate character space
    space = 0
    if any(c.islower() for c in password):
        space += 26
    if any(c.isupper() for c in password):
        space += 26
    if any(c.isdigit() for c in password):
        space += 10
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in password):
        space += 33

    if space == 0:
        return "instantly", 0

    combinations = space ** len(password)

    # Assume powerful attacker (GPUs) at 10 billion guesses/second
    guesses_per_second = 10_000_000_000
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "instantly", seconds
    elif seconds < 60:
        return f"{seconds:.1f} seconds", seconds
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes", seconds
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours", seconds
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days", seconds
    elif seconds < 3153600000:
        return f"{seconds/31536000:.1f} years", seconds
    else:
        return f"{seconds/3153600000:.1f} centuries", seconds


def dictionary_attack_simulation(password):
    """Simulate a dictionary attack."""
    print("\n--- Dictionary Attack Simulation ---")
    print("Checking against common password list...")

    start_time = time.time()
    checked = 0

    for common in COMMON_PASSWORDS:
        checked += 1
        if common == password.lower():
            elapsed = time.time() - start_time
            print(f"MATCH FOUND after {checked} attempts!")
            print(f"Time: {elapsed:.4f} seconds")
            print("Password is in common dictionary - VERY INSECURE")
            return True

    elapsed = time.time() - start_time
    print(f"No match found after {checked} dictionary words.")
    print(f"Time: {elapsed:.4f} seconds")
    return False


def brute_force_simulation(password):
    """Simulate brute force timing."""
    print("\n--- Brute Force Estimation ---")
    time_str, seconds = estimate_crack_time(password)
    print(f"Estimated crack time: {time_str}")

    # Show scale
    print("\nComparative scale:")
    benchmarks = [
        ("8 chars, lowercase only", 26**8),
        ("8 chars, mixed case", 52**8),
        ("8 chars, mixed + digits", 62**8),
        ("8 chars, all character types", 95**8),
        ("12 chars, all character types", 95**12),
        ("16 chars, all character types", 95**16),
    ]

    pwd_space = 0
    if any(c.islower() for c in password):
        pwd_space += 26
    if any(c.isupper() for c in password):
        pwd_space += 26
    if any(c.isdigit() for c in password):
        pwd_space += 10
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in password):
        pwd_space += 33

    user_combinations = pwd_space ** len(password)

    for desc, combinations in benchmarks:
        ratio = user_combinations / combinations if combinations > 0 else 0
        marker = " <-- YOUR PASSWORD" if abs(ratio - 1.0) < 0.1 or (ratio > 0.5 and ratio < 2) else ""
        print(f"  {desc:<35} {combinations:>20,} combos{marker}")


def hash_comparison(password):
    """Compare different hash algorithms."""
    print("\n--- Password Hash Comparison ---")
    print("Different algorithms have different cracking speeds:\n")

    # Hash the password
    pwd_bytes = password.encode()
    md5_hash = hashlib.md5(pwd_bytes).hexdigest()
    sha1_hash = hashlib.sha1(pwd_bytes).hexdigest()
    sha256_hash = hashlib.sha256(pwd_bytes).hexdigest()

    print(f"Password: {password}")
    print(f"MD5:      {md5_hash}  (BROKEN - 100+ billion guesses/sec)")
    print(f"SHA1:     {sha1_hash}  (BROKEN - 50+ billion guesses/sec)")
    print(f"SHA256:   {sha256_hash}  (Fast but no collision attacks)")
    print(f"bcrypt:   [simulated slow hash]  (Designed to be slow: ~100ms/hash)")
    print(f"Argon2:   [modern slow hash]     (Memory-hard, GPU-resistant)")

    print("\nWhy slow hashes matter:")
    print("  MD5/SHA*: Designed for speed. Attackers can test billions/second.")
    print("  bcrypt/Argon2: Designed to be slow. Attackers limited to ~10-100/second.")
    print("  For password storage, ALWAYS use bcrypt, Argon2, or PBKDF2.")


def password_policy_check(password):
    """Check password against common policies."""
    print("\n--- Password Policy Compliance ---")

    checks = [
        ("Minimum 8 characters", len(password) >= 8),
        ("Minimum 12 characters", len(password) >= 12),
        ("Contains lowercase", any(c.islower() for c in password)),
        ("Contains uppercase", any(c.isupper() for c in password)),
        ("Contains digit", any(c.isdigit() for c in password)),
        ("Contains special char", any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?`~' for c in password)),
        ("No common patterns", password.lower() not in COMMON_PASSWORDS),
    ]

    passed = 0
    for check, result in checks:
        status = "PASS" if result else "FAIL"
        if result:
            passed += 1
        print(f"  [{status}] {check}")

    print(f"\nScore: {passed}/{len(checks)} checks passed")

    if passed == len(checks):
        print("Excellent password!")
    elif passed >= 5:
        print("Good password with minor improvements possible.")
    elif passed >= 3:
        print("Weak password. Consider using a passphrase.")
    else:
        print("Very weak password. Change immediately!")


def main():
    print("=" * 70)
    print("PASSWORD SECURITY AUDITOR")
    print("=" * 70)
    print("Educational tool for understanding password strength.")
    print("WARNING: Only analyze passwords you own!\n")

    password = input("Enter a password to analyze: ")
    if not password:
        print("No password entered.")
        return

    print(f"\n{'=' * 70}")
    print(f"ANALYSIS FOR: {'*' * len(password)}")
    print(f"{'=' * 70}")

    password_policy_check(password)
    dictionary_attack_simulation(password)
    brute_force_simulation(password)
    hash_comparison(password)

    print(f"\n{'=' * 70}")
    print("RECOMMENDATIONS")
    print(f"{'=' * 70}")
    print("1. Use a password manager to generate and store unique passwords")
    print("2. Aim for 16+ character passphrases (4-5 random words)")
    print("3. Enable multi-factor authentication everywhere")
    print("4. Never reuse passwords across different sites")
    print("5. Check if your password has been leaked: haveibeenpwned.com")


if __name__ == "__main__":
    main()
