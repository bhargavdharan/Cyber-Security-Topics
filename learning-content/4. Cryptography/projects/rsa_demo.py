#!/usr/bin/env python3
"""
RSA Key Exchange Demo
Interactive demonstration of asymmetric cryptography using RSA.

Requires: pip install cryptography
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from getpass import getpass


def generate_keypair():
    """Generate a new RSA key pair."""
    print("\nGenerating 2048-bit RSA key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    print("Key generation complete!")
    return private_key, public_key


def save_keys(private_key, public_key, private_file="private.pem", public_file="public.pem"):
    """Save keys to PEM files."""
    # Private key (encrypted with password)
    password = getpass("Password to protect private key: ").encode()
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password),
    )
    with open(private_file, "wb") as f:
        f.write(pem_private)

    # Public key
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(public_file, "wb") as f:
        f.write(pem_public)

    print(f"Keys saved: {private_file}, {public_file}")


def load_private_key(filepath):
    """Load a private key from PEM file."""
    with open(filepath, "rb") as f:
        pem = f.read()

    if b"ENCRYPTED" in pem:
        password = getpass("Private key password: ").encode()
    else:
        password = None

    return serialization.load_pem_private_key(pem, password=password)


def load_public_key(filepath):
    """Load a public key from PEM file."""
    with open(filepath, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def encrypt_message(public_key, message: str):
    """Encrypt a message with RSA public key."""
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
    return ciphertext


def decrypt_message(private_key, ciphertext):
    """Decrypt a message with RSA private key."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
    return plaintext.decode()


def sign_message(private_key, message: str):
    """Sign a message with RSA private key."""
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def verify_signature(public_key, message: str, signature):
    """Verify a signature with RSA public key."""
    try:
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def demo_encryption():
    """Run encryption/decryption demo."""
    print("\n" + "=" * 60)
    print("ENCRYPTION / DECRYPTION DEMO")
    print("=" * 60)
    print("In asymmetric cryptography, anyone can encrypt with the PUBLIC key,")
    print("but only the PRIVATE key holder can decrypt.\n")

    private_key, public_key = generate_keypair()

    message = input("Enter a secret message: ") or "Hello, secure world!"

    print(f"\nOriginal message: {message}")

    # Encrypt
    print("\nEncrypting with PUBLIC key...")
    ciphertext = encrypt_message(public_key, message)
    print(f"Ciphertext (hex): {ciphertext.hex()[:64]}...")
    print(f"Ciphertext length: {len(ciphertext)} bytes")

    # Decrypt
    print("\nDecrypting with PRIVATE key...")
    decrypted = decrypt_message(private_key, ciphertext)
    print(f"Decrypted message: {decrypted}")

    if decrypted == message:
        print("\n[SUCCESS] Message encrypted and decrypted correctly!")
    else:
        print("\n[FAILURE] Decryption mismatch!")


def demo_signature():
    """Run digital signature demo."""
    print("\n" + "=" * 60)
    print("DIGITAL SIGNATURE DEMO")
    print("=" * 60)
    print("Digital signatures prove authenticity and integrity.")
    print("Only the PRIVATE key holder can sign, but anyone can verify with the PUBLIC key.\n")

    private_key, public_key = generate_keypair()

    document = input("Enter a document/message to sign: ") or "I authorize this transaction."

    print(f"\nDocument: {document}")

    # Sign
    print("\nSigning with PRIVATE key...")
    signature = sign_message(private_key, document)
    print(f"Signature (hex): {signature.hex()[:64]}...")
    print(f"Signature length: {len(signature)} bytes")

    # Verify
    print("\nVerifying with PUBLIC key...")
    is_valid = verify_signature(public_key, document, signature)

    if is_valid:
        print("\n[VALID] Signature is authentic! Document has not been tampered with.")
    else:
        print("\n[INVALID] Signature verification failed!")

    # Demonstrate tampering detection
    print("\n--- Tampering Simulation ---")
    tampered_doc = document + " (modified by attacker)"
    is_valid_tampered = verify_signature(public_key, tampered_doc, signature)

    if not is_valid_tampered:
        print("Tampered document detected! Signature no longer matches.")
        print("This is how digital signatures ensure INTEGRITY.")


def demo_key_exchange():
    """Simulate a secure key exchange scenario."""
    print("\n" + "=" * 60)
    print("SECURE KEY EXCHANGE SCENARIO")
    print("=" * 60)
    print("Alice and Bob want to communicate securely over an insecure channel.\n")

    # Alice generates keys
    print("Step 1: Alice generates her RSA key pair...")
    alice_private, alice_public = generate_keypair()

    # Bob generates keys
    print("Step 2: Bob generates his RSA key pair...")
    bob_private, bob_public = generate_keypair()

    print("\nStep 3: They exchange PUBLIC keys over the insecure channel.")
    print("(Eve can see the public keys, but that's OK - they're public!)")

    # Alice sends encrypted message
    message = "Meet me at the secure location at noon."
    print(f"\nStep 4: Alice encrypts a message with Bob's public key:")
    print(f'  "{message}"')

    encrypted = encrypt_message(bob_public, message)

    print("\nStep 5: Alice sends the ciphertext to Bob.")
    print("(Eve intercepts it but cannot decrypt without Bob's private key)")

    # Bob decrypts
    decrypted = decrypt_message(bob_private, encrypted)
    print(f'\nStep 6: Bob decrypts with his private key: "{decrypted}"')

    # Bob replies with signed message
    reply = "Confirmed. I'll be there."
    print(f"\nStep 7: Bob sends a signed reply:")
    print(f'  "{reply}"')

    signature = sign_message(bob_private, reply)
    print("Step 8: Alice verifies Bob's signature with his public key...")

    if verify_signature(bob_public, reply, signature):
        print("  [VALID] Alice knows the message truly came from Bob.")

    print("\n" + "=" * 60)
    print("Result: Secure, authenticated communication achieved!")
    print("Even though Eve saw everything on the network, she cannot:")
    print("  - Read the encrypted messages (no private keys)")
    print("  - Forge signatures (no private keys)")


def print_explanation():
    print("\n" + "=" * 60)
    print("HOW RSA WORKS (Simplified)")
    print("=" * 60)
    print("""
RSA is an asymmetric algorithm based on the mathematical difficulty
of factoring large prime numbers.

KEY GENERATION:
  1. Choose two large prime numbers: p and q
  2. Compute n = p * q (the modulus, used in both keys)
  3. Compute φ(n) = (p-1) * (q-1)
  4. Choose public exponent e (commonly 65537)
  5. Compute private exponent d where (d * e) mod φ(n) = 1
  6. Public key: (n, e)  |  Private key: (n, d)

ENCRYPTION:  ciphertext = message^e mod n
DECRYPTION:  message = ciphertext^d mod n

SECURITY:
  - Factoring n into p and q is computationally infeasible for large n
  - 2048-bit RSA is currently considered secure
  - 4096-bit RSA provides additional margin against future advances

IMPORTANT LIMITATION:
  RSA can only encrypt data smaller than the key size (~190 bytes for 2048-bit)
  In practice, RSA is used to encrypt a symmetric key, which then encrypts the data.
    """)


def main():
    print("=" * 60)
    print("RSA KEY EXCHANGE DEMO")
    print("=" * 60)
    print("Interactive demonstration of public-key cryptography.\n")

    while True:
        print("\nMenu:")
        print("1. Encryption / Decryption Demo")
        print("2. Digital Signature Demo")
        print("3. Secure Key Exchange Scenario")
        print("4. How RSA Works")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_encryption()
        elif choice == "2":
            demo_signature()
        elif choice == "3":
            demo_key_exchange()
        elif choice == "4":
            print_explanation()
        elif choice == "5":
            print("Public key cryptography is the foundation of internet security!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
