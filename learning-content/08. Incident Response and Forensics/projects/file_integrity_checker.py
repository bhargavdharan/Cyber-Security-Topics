#!/usr/bin/env python3
"""
File Integrity Checker
Demonstrates evidence integrity verification for digital forensics.
"""

import hashlib
import json
import os
from datetime import datetime


class EvidenceLocker:
    """Manages digital evidence with chain of custody."""

    def __init__(self, case_id):
        self.case_id = case_id
        self.evidence = []
        self.custody_log = []

    def add_evidence(self, filepath, collected_by, description):
        """Add evidence to the case."""
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return None

        # Calculate multiple hashes
        hashes = self._calculate_hashes(filepath)

        evidence = {
            "id": f"EVD-{len(self.evidence)+1:03d}",
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "size": os.path.getsize(filepath),
            "hashes": hashes,
            "collected_by": collected_by,
            "collected_at": datetime.now().isoformat(),
            "description": description,
        }

        self.evidence.append(evidence)
        self._add_custody_entry(evidence["id"], "COLLECTED", collected_by,
                               f"Evidence collected: {description}")

        return evidence

    def _calculate_hashes(self, filepath):
        """Calculate multiple hash types for a file."""
        hashes = {}

        with open(filepath, "rb") as f:
            data = f.read()

        hashes["md5"] = hashlib.md5(data).hexdigest()
        hashes["sha1"] = hashlib.sha1(data).hexdigest()
        hashes["sha256"] = hashlib.sha256(data).hexdigest()

        return hashes

    def _add_custody_entry(self, evidence_id, action, person, notes):
        """Add an entry to the chain of custody log."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "evidence_id": evidence_id,
            "action": action,
            "person": person,
            "notes": notes,
        }
        self.custody_log.append(entry)

    def transfer_custody(self, evidence_id, from_person, to_person, reason):
        """Transfer evidence custody."""
        self._add_custody_entry(evidence_id, "TRANSFERRED", from_person,
                               f"Transferred to {to_person}: {reason}")
        self._add_custody_entry(evidence_id, "RECEIVED", to_person,
                               f"Received from {from_person}: {reason}")
        print(f"Custody of {evidence_id} transferred from {from_person} to {to_person}")

    def verify_integrity(self, evidence_id):
        """Verify evidence integrity against recorded hashes."""
        evidence = next((e for e in self.evidence if e["id"] == evidence_id), None)
        if not evidence:
            print(f"Evidence {evidence_id} not found")
            return False

        print(f"\nVerifying integrity of {evidence_id}...")
        print(f"File: {evidence['filepath']}")

        current_hashes = self._calculate_hashes(evidence['filepath'])

        all_match = True
        for algo in ["md5", "sha1", "sha256"]:
            original = evidence["hashes"][algo]
            current = current_hashes[algo]
            match = original == current
            status = "MATCH" if match else "MISMATCH"
            print(f"  [{status}] {algo.upper()}: {current}")
            if not match:
                all_match = False

        if all_match:
            print(f"\n[PASS] Integrity verified. File has not been modified.")
            self._add_custody_entry(evidence_id, "VERIFIED", "System", "Integrity check passed")
        else:
            print(f"\n[FAIL] INTEGRITY BREACH DETECTED!")
            print("The file has been modified since collection.")
            self._add_custody_entry(evidence_id, "TAMPERED", "System", "Integrity check failed")

        return all_match

    def generate_report(self):
        """Generate chain of custody report."""
        print(f"\n{'=' * 70}")
        print(f"CHAIN OF CUSTODY REPORT")
        print(f"Case ID: {self.case_id}")
        print(f"Generated: {datetime.now().isoformat()}")
        print(f"{'=' * 70}")

        print(f"\nEVIDENCE ITEMS ({len(self.evidence)} total):")
        print("─" * 70)
        for ev in self.evidence:
            print(f"\n{ev['id']}: {ev['filename']}")
            print(f"  Path: {ev['filepath']}")
            print(f"  Size: {ev['size']} bytes")
            print(f"  Collected: {ev['collected_at']} by {ev['collected_by']}")
            print(f"  Description: {ev['description']}")
            print(f"  SHA256: {ev['hashes']['sha256']}")

        print(f"\n{'─' * 70}")
        print(f"CUSTODY LOG ({len(self.custody_log)} entries):")
        print("─" * 70)
        for entry in self.custody_log:
            print(f"\n{entry['timestamp']}")
            print(f"  Evidence: {entry['evidence_id']}")
            print(f"  Action:   {entry['action']}")
            print(f"  Person:   {entry['person']}")
            print(f"  Notes:    {entry['notes']}")


def demo_evidence_handling():
    """Demonstrate complete evidence handling workflow."""
    print("\n" + "=" * 70)
    print("DIGITAL FORENSICS EVIDENCE HANDLING DEMO")
    print("=" * 70)

    # Create a test file
    test_file = "suspicious_document.txt"
    with open(test_file, "w") as f:
        f.write("This is a suspicious document found on the compromised system.\n")
        f.write("It contains evidence of unauthorized access.\n")

    locker = EvidenceLocker("CASE-2024-0315")

    # Step 1: Collect evidence
    print("\n[Step 1] Collecting evidence...")
    evidence = locker.add_evidence(
        test_file,
        collected_by="Officer Smith",
        description="Suspicious document found on compromised workstation",
    )
    print(f"Evidence ID: {evidence['id']}")
    print(f"SHA256: {evidence['hashes']['sha256']}")

    # Step 2: Verify integrity
    print("\n[Step 2] Initial integrity verification...")
    locker.verify_integrity(evidence['id'])

    # Step 3: Transfer custody
    print("\n[Step 3] Transferring to forensic lab...")
    locker.transfer_custody(
        evidence['id'],
        from_person="Officer Smith",
        to_person="Forensic Analyst Jones",
        reason="Malware analysis required",
    )

    # Step 4: Simulate tampering
    print("\n[Step 4] Simulating file tampering...")
    with open(test_file, "a") as f:
        f.write("\n[ATTACKER MODIFIED THIS FILE]")
    print("File was modified (simulating tampering or corruption)")

    # Step 5: Re-verify
    print("\n[Step 5] Re-verifying integrity after transfer...")
    locker.verify_integrity(evidence['id'])

    # Step 6: Generate report
    print("\n[Step 6] Generating chain of custody report...")
    locker.generate_report()

    # Cleanup
    os.remove(test_file)


def demo_hash_algorithms():
    """Compare hash algorithms for forensic use."""
    print("\n" + "=" * 70)
    print("HASH ALGORITHMS IN FORENSICS")
    print("=" * 70)

    test_data = b"Digital evidence sample for hash comparison"

    algorithms = [
        ("MD5", hashlib.md5(test_data).hexdigest()),
        ("SHA-1", hashlib.sha1(test_data).hexdigest()),
        ("SHA-256", hashlib.sha256(test_data).hexdigest()),
        ("SHA-512", hashlib.sha512(test_data).hexdigest()),
    ]

    print(f"\nTest data: '{test_data.decode()}'")
    print(f"\n{'Algorithm':<12} {'Hash':<64} {'Length'}")
    print("─" * 90)
    for name, h in algorithms:
        print(f"{name:<12} {h:<64} {len(h)*4} bits")

    print("\nForensic Recommendations:")
    print("  - MD5: Fast but collision-vulnerable. Use for quick screening only.")
    print("  - SHA-1: Deprecated. Do not use for new evidence.")
    print("  - SHA-256: Current standard for forensic integrity.")
    print("  - SHA-512: Higher security margin, useful for long-term archiving.")
    print("\nBest Practice: Calculate multiple hashes (SHA-256 + SHA-512) for critical evidence.")


def main():
    print("=" * 70)
    print("FILE INTEGRITY CHECKER")
    print("=" * 70)
    print("Learn digital forensics evidence handling and integrity verification.\n")

    while True:
        print("\nMenu:")
        print("1. Evidence Handling Demo")
        print("2. Hash Algorithms Comparison")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_evidence_handling()
        elif choice == "2":
            demo_hash_algorithms()
        elif choice == "3":
            demo_evidence_handling()
            demo_hash_algorithms()
        elif choice == "4":
            print("Preserve that evidence!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
