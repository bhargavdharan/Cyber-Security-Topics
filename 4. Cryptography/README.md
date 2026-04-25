## Cryptography

Cryptography is the practice of securing information by transforming it into an unreadable format using mathematical algorithms. It plays a crucial role in ensuring data confidentiality, integrity, authenticity, and non-repudiation. Let's explore the following subtopics:

### Symmetric Encryption

Symmetric encryption, also known as secret-key encryption, uses a single secret key to both encrypt and decrypt the data. The same key is shared between the sender and receiver.

- **Encryption Process:** The plaintext (original message) and the secret key are input into an encryption algorithm, producing the ciphertext (encrypted message).
- **Decryption Process:** The ciphertext and the secret key are input into a decryption algorithm, which recovers the original plaintext.
- **Common Algorithms:**
  - **AES (Advanced Encryption Standard):** The most widely used symmetric algorithm, available in key sizes of 128, 192, and 256 bits. It is fast, secure, and used in various applications including file encryption, VPNs, and wireless security (WPA2/WPA3).
  - **DES (Data Encryption Standard):** An older algorithm with a 56-bit key, now considered insecure due to brute-force attacks.
  - **3DES (Triple DES):** Applies DES three times for increased security, but is being phased out in favor of AES.
  - **ChaCha20:** A modern stream cipher often used in mobile and low-power devices, praised for its speed and security.
- **Use Cases:** Symmetric encryption is commonly used for securing data transmission over a network, such as encrypted email communication, secure file transfer, virtual private networks (VPNs), and disk encryption.
- **Challenges:** Secure key distribution is the primary challenge—if the secret key is intercepted, the encrypted data is compromised.

### Asymmetric Encryption

Asymmetric encryption, also known as public-key encryption, uses a pair of mathematically related keys: a public key for encryption and a private key for decryption. The public key can be freely distributed, while the private key must be kept confidential.

- **Encryption Process:** The sender uses the recipient's public key to encrypt the message, generating the ciphertext.
- **Decryption Process:** The recipient uses their private key to decrypt the ciphertext and retrieve the original plaintext.
- **Common Algorithms:**
  - **RSA (Rivest-Shamir-Adleman):** One of the most widely used asymmetric algorithms, based on the difficulty of factoring large prime numbers. Common key sizes range from 2048 to 4096 bits.
  - **ECC (Elliptic Curve Cryptography):** Provides equivalent security to RSA with smaller key sizes, making it efficient for mobile devices and IoT. Examples include ECDSA and Curve25519.
  - **Diffie-Hellman (DH):** A key exchange protocol that allows two parties to establish a shared secret over an insecure channel.
- **Use Cases:** Asymmetric encryption is used for secure communication, digital signatures, key exchange protocols (TLS/SSL handshake), and encrypting small amounts of data.
- **Performance:** Asymmetric encryption is computationally intensive and slower than symmetric encryption. In practice, hybrid systems use asymmetric encryption to exchange a symmetric key, then use symmetric encryption for the actual data transfer.

### Hash Functions and Message Digests

Hash functions are mathematical algorithms that take an input (message) and produce a fixed-size string of characters, known as a hash value or message digest.

- **Properties:**
  - **Deterministic:** The same input always produces the same hash.
  - **Fast Computation:** Hashing should be quick for any input size.
  - **Pre-image Resistance:** It should be computationally infeasible to reverse-engineer the input from the hash.
  - **Collision Resistance:** It should be extremely difficult to find two different inputs that produce the same hash.
  - **Avalanche Effect:** Even a small change in the input should produce a significantly different hash.
- **Common Algorithms:**
  - **SHA-256 (Secure Hash Algorithm 256-bit):** Part of the SHA-2 family, widely used in blockchain, digital certificates, and password hashing.
  - **SHA-3:** The latest member of the Secure Hash Algorithm family, designed with a different internal structure (Keccak sponge construction).
  - **MD5 (Message Digest 5):** An older, 128-bit hash function now considered broken and unsuitable for security purposes due to collision vulnerabilities.
  - **BLAKE2/BLAKE3:** Fast, modern hash functions optimized for software performance.
- **Use Cases:** Hash functions are used for password storage (storing hashed passwords with salt instead of plain text), data integrity verification, digital forensics, checksum verification, and blockchain technology.

### Digital Signatures and Certificates

Digital signatures provide integrity, authenticity, and non-repudiation to digital documents or messages. They use asymmetric encryption and hash functions to verify the integrity of the signed data and the identity of the signer.

- **Signing Process:** The sender creates a hash of the document, then encrypts the hash with their private key, creating the digital signature. The recipient verifies the signature using the sender's public key and compares the computed hash value with the received hash value.
- **Certificates:** Certificates bind an entity's identity (such as a person, organization, or website) to their public key. Certificate authorities (CAs) digitally sign these certificates, validating the authenticity of the public key and the identity of the entity.
- **PKI (Public Key Infrastructure):** The ecosystem of hardware, software, policies, and standards that manages the creation, distribution, and revocation of digital certificates.
- **Use Cases:** Digital signatures are used for ensuring the authenticity and integrity of electronic documents, software distribution, secure online transactions (code signing), email security (S/MIME, PGP), and legal contracts.

### Cryptographic Protocols

- **TLS/SSL (Transport Layer Security/Secure Sockets Layer):** Protocols that provide encrypted communication over a network, widely used for HTTPS websites, email, and VPNs.
- **IPsec (Internet Protocol Security):** A suite of protocols that secure IP communications by authenticating and encrypting each IP packet in a data stream.
- **SSH (Secure Shell):** A protocol for secure remote login and command execution on servers.
- **PGP/GPG (Pretty Good Privacy/GNU Privacy Guard):** Tools for encrypting and signing emails and files.

## Conclusion

Cryptography provides the foundation for secure communication, data protection, and information integrity. By understanding symmetric and asymmetric encryption, hash functions and message digests, digital signatures, certificates, and cryptographic protocols, individuals and organizations can employ cryptographic techniques to protect sensitive information, ensure secure communication, and establish trust in digital transactions.

## Projects

Check out the [projects folder](./projects/) for hands-on tools:
- AES File Encryptor
- Hash Generator & Verifier
- RSA Key Exchange Demo
