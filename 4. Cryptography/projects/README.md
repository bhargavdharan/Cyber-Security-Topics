# Projects: Cryptography

Hands-on cryptographic tools and simulations for learning encryption, hashing, and key exchange.

---

## Projects Included

### 1. AES File Encryptor (`aes_file_encryptor.py`)
A real encryption tool using the Python `cryptography` library:
- Encrypt and decrypt files with AES-256-GCM
- Password-based key derivation (PBKDF2)
- Automatic salt and nonce generation

**How to run:**
```bash
python aes_file_encryptor.py
```

### 2. Hash Generator & Verifier (`hash_tool.py`)
Demonstrates cryptographic hash functions:
- Calculate MD5, SHA-1, SHA-256, SHA-512 hashes
- Verify file integrity against known hashes
- Compare hash algorithm strengths

**How to run:**
```bash
python hash_tool.py
```

### 3. RSA Key Exchange Demo (`rsa_demo.py`)
Interactive demonstration of asymmetric cryptography:
- Generate RSA key pairs
- Encrypt and decrypt messages
- Sign and verify digital signatures

**How to run:**
```bash
python rsa_demo.py
```

---

## Learning Objectives

- Understand symmetric vs asymmetric encryption practically
- Learn how hashing ensures data integrity
- Experience public-key cryptography operations

## Requirements

- Python 3.x
- `cryptography` library (`pip install cryptography`)
