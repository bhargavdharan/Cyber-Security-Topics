#!/usr/bin/env python3
"""
Quantum Key Distribution Simulation
Simplified BB84 protocol demonstration.
"""

import random


class QuantumChannel:
    """Simulates a quantum communication channel."""

    def __init__(self):
        self.eavesdropper = False

    def send_photon(self, bit, basis):
        """Send a photon encoded with bit in given basis."""
        # In real QKD, this would be a polarized photon
        return {"bit": bit, "basis": basis}

    def measure_photon(self, photon, measurement_basis):
        """Measure a photon in a given basis."""
        if self.eavesdropper:
            # Eavesdropper randomly chooses basis
            eve_basis = random.choice(["+", "x"])
            if eve_basis != photon["basis"]:
                # Wrong basis - random result
                photon["bit"] = random.choice([0, 1])
                photon["disturbed"] = True

        if measurement_basis == photon["basis"]:
            return photon["bit"]
        else:
            # Wrong basis - random result, photon disturbed
            photon["disturbed"] = True
            return random.choice([0, 1])


class BB84Protocol:
    """Simplified BB84 QKD protocol simulation."""

    def __init__(self, num_bits=20):
        self.num_bits = num_bits
        self.channel = QuantumChannel()
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_results = []
        self.shared_key = []

    def run_protocol(self):
        """Execute the BB84 protocol."""
        print(f"\n{'=' * 60}")
        print("BB84 QUANTUM KEY DISTRIBUTION")
        print(f"{'=' * 60}")
        print(f"Generating {self.num_bits} quantum bits...\n")

        # Step 1: Alice generates random bits and bases
        self.alice_bits = [random.choice([0, 1]) for _ in range(self.num_bits)]
        self.alice_bases = [random.choice(["+", "x"]) for _ in range(self.num_bits)]

        print("Alice's random bits:  ", self.alice_bits)
        print("Alice's random bases: ", self.alice_bases)

        # Step 2: Bob chooses random bases
        self.bob_bases = [random.choice(["+", "x"]) for _ in range(self.num_bits)]
        print("Bob's random bases:   ", self.bob_bases)

        # Step 3: Quantum transmission
        print("\n--- Quantum Transmission ---")
        for i in range(self.num_bits):
            photon = self.channel.send_photon(self.alice_bits[i], self.alice_bases[i])
            result = self.channel.measure_photon(photon, self.bob_bases[i])
            self.bob_results.append(result)

        print("Bob's measurements:   ", self.bob_results)

        # Step 4: Basis reconciliation
        print("\n--- Basis Reconciliation ---")
        matching_bases = [a == b for a, b in zip(self.alice_bases, self.bob_bases)]
        print("Matching bases:       ", ["Y" if m else "N" for m in matching_bases])

        # Step 5: Key sifting
        self.shared_key = [self.alice_bits[i] for i in range(self.num_bits) if matching_bases[i]]
        bob_key = [self.bob_results[i] for i in range(self.num_bits) if matching_bases[i]]

        print(f"\nAlice's sifted key:   {self.shared_key}")
        print(f"Bob's sifted key:     {bob_key}")

        # Step 6: Error checking
        errors = sum(1 for a, b in zip(self.shared_key, bob_key) if a != b)
        error_rate = errors / len(self.shared_key) if self.shared_key else 0

        print(f"\nError rate: {error_rate:.1%} ({errors}/{len(self.shared_key)})")

        if error_rate > 0.11:  # BB84 threshold
            print("[!] High error rate detected - possible eavesdropping!")
            print("    Protocol aborted. Key discarded.")
            self.shared_key = []
        elif errors > 0:
            print("[!] Some errors detected (may be noise or eavesdropping)")
            print("    Privacy amplification will reduce key length")
        else:
            print("[OK] Keys match. Secure communication established.")

        return self.shared_key


def demo_bb84():
    """Run BB84 demonstration."""
    protocol = BB84Protocol(num_bits=20)
    key = protocol.run_protocol()

    if key:
        print(f"\nFinal shared key length: {len(key)} bits")
        print(f"Key efficiency: {len(key)}/20 = {len(key)/20:.0%}")


def demo_eavesdropping():
    """Demonstrate eavesdropping detection."""
    print("\n" + "=" * 60)
    print("EAVESDROPPING DETECTION")
    print("=" * 60)

    protocol = BB84Protocol(num_bits=50)
    protocol.channel.eavesdropper = True  # Eve is listening!

    print("\n[!] Eavesdropper (Eve) is intercepting photons...")
    print("Eve measures each photon in a random basis and resends it")

    key = protocol.run_protocol()

    print("""
Why eavesdropping is detected:
  1. When Eve measures in wrong basis, she disturbs the photon
  2. This introduces errors in Bob's measurements
  3. Alice and Bob compare subset of bits publicly
  4. If error rate > 11%, they know Eve is listening
  5. They discard the key and try again

This is the quantum advantage:
  - Classical signals can be copied without detection
  - Quantum states cannot be measured without disturbing them
  - Any interception leaves detectable traces
    """)


def demo_quantum_vs_classical():
    """Compare quantum vs classical key distribution."""
    print("\n" + "=" * 60)
    print("QUANTUM vs CLASSICAL KEY DISTRIBUTION")
    print("=" * 60)

    comparisons = [
        ("Eavesdropping Detection", "Yes - guaranteed by physics", "No - impossible to detect"),
        ("Key Security", "Information-theoretic secure", "Computationally secure"),
        ("Future-Proof", "Resistant to quantum computers", "Broken by quantum computers (RSA, ECC)"),
        ("Distance", "Limited (~100km fiber)", "Unlimited with internet"),
        (("Hardware Requirements", "Specialized quantum hardware", "Standard computers")),
    ]

    print(f"\n{'Feature':<25} {'Quantum (QKD)':<35} {'Classical'}")
    print("─" * 90)
    for feature, quantum, classical in comparisons:
        print(f"{feature:<25} {quantum:<35} {classical}")

    print("\nWhen will quantum computers break current encryption?")
    print("  - Current estimates: 10-30 years for cryptographically-relevant quantum computer")
    print("  - NIST already standardizing post-quantum cryptography")
    print("  - 'Harvest now, decrypt later' threat is immediate concern")


def main():
    print("=" * 60)
    print("QUANTUM KEY DISTRIBUTION SIMULATOR")
    print("=" * 60)
    print("Simplified BB84 protocol demonstration.\n")

    while True:
        print("\nMenu:")
        print("1. BB84 Protocol Demo")
        print("2. Eavesdropping Detection")
        print("3. Quantum vs Classical Comparison")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_bb84()
        elif choice == "2":
            demo_eavesdropping()
        elif choice == "3":
            demo_quantum_vs_classical()
        elif choice == "4":
            demo_bb84()
            demo_eavesdropping()
            demo_quantum_vs_classical()
        elif choice == "5":
            print("The future is quantum!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
