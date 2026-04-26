#!/usr/bin/env python3
"""
AES File Encryptor
Real file encryption using AES-256-GCM with password-based key derivation.

Requires: pip install cryptography
"""

import os
import secrets
from getpass import getpass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


SALT_LENGTH = 32
NONCE_LENGTH = 12
ITERATIONS = 100_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive an AES key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode())


def encrypt_file(input_path: str, output_path: str, password: str):
    """Encrypt a file using AES-256-GCM."""
    # Read file
    with open(input_path, "rb") as f:
        plaintext = f.read()

    # Generate random salt and nonce
    salt = secrets.token_bytes(SALT_LENGTH)
    nonce = secrets.token_bytes(NONCE_LENGTH)

    # Derive key and encrypt
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # Write: salt + nonce + ciphertext
    with open(output_path, "wb") as f:
        f.write(salt + nonce + ciphertext)

    return len(plaintext)


def decrypt_file(input_path: str, output_path: str, password: str):
    """Decrypt a file encrypted with AES-256-GCM."""
    with open(input_path, "rb") as f:
        data = f.read()

    # Extract salt, nonce, and ciphertext
    salt = data[:SALT_LENGTH]
    nonce = data[SALT_LENGTH:SALT_LENGTH + NONCE_LENGTH]
    ciphertext = data[SALT_LENGTH + NONCE_LENGTH:]

    # Derive key and decrypt
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    except Exception as e:
        raise ValueError("Decryption failed. Wrong password or corrupted file.") from e

    with open(output_path, "wb") as f:
        f.write(plaintext)

    return len(plaintext)


def create_test_file(filename="test_secret.txt"):
    """Create a sample file to encrypt."""
    content = """TOP SECRET DOCUMENT
Classification: Confidential

Project: Crypto Learning Module
Status: In Progress

This file demonstrates secure encryption using AES-256-GCM.
The password you provide will be used to derive the encryption key.

Remember: Always use strong, unique passwords for encryption!
"""
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created test file: {filename}")
    return filename


def main():
    print("=" * 60)
    print("AES-256-GCM FILE ENCRYPTOR")
    print("=" * 60)
    print("Real encryption using industry-standard algorithms.")
    print("Key derivation: PBKDF2-HMAC-SHA256 (100,000 iterations)")
    print("Encryption: AES-256-GCM (Authenticated Encryption)\n")

    while True:
        print("\nMenu:")
        print("1. Create Test File")
        print("2. Encrypt File")
        print("3. Decrypt File")
        print("4. How It Works")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            create_test_file()

        elif choice == "2":
            infile = input("File to encrypt: ").strip()
            if not os.path.exists(infile):
                print("File not found.")
                continue
            outfile = input("Output filename [default: encrypted.bin]: ").strip() or "encrypted.bin"
            password = getpass("Password: ")
            confirm = getpass("Confirm password: ")
            if password != confirm:
                print("Passwords do not match!")
                continue
            if len(password) < 8:
                print("Warning: Password is very short. Use 12+ characters for security.")

            size = encrypt_file(infile, outfile, password)
            print(f"\nEncrypted {size} bytes -> {outfile}")
            print("Keep your password safe! Without it, the file cannot be recovered.")

        elif choice == "3":
            infile = input("File to decrypt: ").strip()
            if not os.path.exists(infile):
                print("File not found.")
                continue
            outfile = input("Output filename [default: decrypted.txt]: ").strip() or "decrypted.txt"
            password = getpass("Password: ")

            try:
                size = decrypt_file(infile, outfile, password)
                print(f"\nDecrypted {size} bytes -> {outfile}")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == "4":
            print_explanation()

        elif choice == "5":
            print("Remember: Encryption is only as strong as your password!")
            break
        else:
            print("Invalid choice.")


def print_explanation():
    print("\n" + "=" * 60)
    print("HOW THE ENCRYPTION WORKS")
    print("=" * 60)
    print("""
1. PASSWORD-BASED KEY DERIVATION (PBKDF2)
   Your password is combined with a random 32-byte SALT.
   PBKDF2-HMAC-SHA256 runs for 100,000 iterations to produce
   a 256-bit AES key. The salt prevents rainbow table attacks.

2. AES-256-GCM ENCRYPTION
   - AES: Advanced Encryption Standard with 256-bit keys
   - GCM: Galois/Counter Mode provides BOTH:
     * Confidentiality (encryption)
     * Authenticity (integrity checking via authentication tag)
   - A random 12-byte NONCE ensures unique ciphertexts

3. FILE FORMAT
   [32 bytes salt][12 bytes nonce][ciphertext + auth tag]

4. SECURITY PROPERTIES
   - Without the password, brute-forcing the key is computationally
     infeasible (2^256 possible keys).
   - The salt ensures identical passwords produce different keys.
   - GCM detects tampering: modified ciphertext will fail decryption.
    """)


if __name__ == "__main__":
    main()
