#!/usr/bin/env python3
"""
Blockchain Security Demo
Demonstrates blockchain security concepts through simulation.
"""

import hashlib
import json
import time


class Block:
    """Represents a block in the blockchain."""

    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the block's hash."""
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        """Mine the block with proof of work."""
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")


class Blockchain:
    """Simulates a blockchain with security features."""

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []

    def create_genesis_block(self):
        """Create the first block."""
        return Block(0, "0", ["Genesis Block"])

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        """Add a transaction to pending list."""
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
        })

    def mine_pending_transactions(self):
        """Mine pending transactions into a new block."""
        block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            self.pending_transactions,
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []

    def is_chain_valid(self):
        """Validate the entire chain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Check current block hash
            if current.hash != current.calculate_hash():
                print(f"[!] Block {i} hash invalid")
                return False

            # Check link to previous block
            if current.previous_hash != previous.hash:
                print(f"[!] Block {i} previous hash link broken")
                return False

        return True

    def tamper_with_block(self, block_index, new_transactions):
        """Simulate tampering with a block."""
        if 0 < block_index < len(self.chain):
            print(f"\n[!] ATTACKER: Modifying block {block_index}...")
            self.chain[block_index].transactions = new_transactions
            # Attacker would need to recalculate hash and all subsequent blocks
            print("Transactions changed but hash not recalculated!")

    def display_chain(self):
        """Display the blockchain."""
        print(f"\n{'=' * 60}")
        print("BLOCKCHAIN CONTENTS")
        print(f"{'=' * 60}")

        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"  Hash:        {block.hash}")
            print(f"  Previous:    {block.previous_hash}")
            print(f"  Timestamp:   {block.timestamp}")
            print(f"  Nonce:       {block.nonce}")
            print(f"  Transactions: {block.transactions}")


def demo_blockchain_basics():
    """Demonstrate basic blockchain operation."""
    print("\n" + "=" * 60)
    print("BLOCKCHAIN BASICS")
    print("=" * 60)

    blockchain = Blockchain()

    print("\nAdding transactions...")
    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.add_transaction("Bob", "Charlie", 25)
    blockchain.mine_pending_transactions()

    blockchain.add_transaction("Charlie", "Alice", 10)
    blockchain.mine_pending_transactions()

    blockchain.display_chain()

    print(f"\nChain valid: {blockchain.is_chain_valid()}")


def demo_tamper_detection():
    """Demonstrate tamper detection."""
    print("\n" + "=" * 60)
    print("BLOCKCHAIN TAMPER DETECTION")
    print("=" * 60)

    blockchain = Blockchain()

    blockchain.add_transaction("Alice", "Bob", 50)
    blockchain.mine_pending_transactions()

    blockchain.add_transaction("Bob", "Charlie", 25)
    blockchain.mine_pending_transactions()

    print("\nBefore tampering:")
    print(f"Chain valid: {blockchain.is_chain_valid()}")

    blockchain.tamper_with_block(1, [{"sender": "Alice", "recipient": "Eve", "amount": 50}])

    print("\nAfter tampering:")
    print(f"Chain valid: {blockchain.is_chain_valid()}")

    print("""
Why tampering is detected:
  1. Changing transactions changes block hash
  2. Next block's 'previous_hash' no longer matches
  3. Attacker must recalculate ALL subsequent blocks
  4. With Proof of Work, this is computationally infeasible
    """)


def demo_consensus():
    """Demonstrate consensus concepts."""
    print("\n" + "=" * 60)
    print("CONSENSUS MECHANISMS")
    print("=" * 60)

    mechanisms = {
        "Proof of Work (PoW)": {
            "description": "Miners solve computational puzzles",
            "pros": ["Proven security", "Decentralized"],
            "cons": ["Energy intensive", "Slow transactions"],
            "examples": ["Bitcoin", "Ethereum (pre-2.0)"],
        },
        "Proof of Stake (PoS)": {
            "description": "Validators stake cryptocurrency",
            "pros": ["Energy efficient", "Faster"],
            "cons": ["Wealth concentration", "Complex slashing rules"],
            "examples": ["Ethereum 2.0", "Cardano", "Solana"],
        },
        "Delegated PoS (DPoS)": {
            "description": "Token holders vote for delegates",
            "pros": ["Fast", "Scalable"],
            "cons": ["Less decentralized", "Voter apathy"],
            "examples": ["EOS", "Tron"],
        },
    }

    for name, details in mechanisms.items():
        print(f"\n[{name}]")
        print(f"  How it works: {details['description']}")
        print(f"  Pros: {', '.join(details['pros'])}")
        print(f"  Cons: {', '.join(details['cons'])}")
        print(f"  Examples: {', '.join(details['examples'])}")


def demo_smart_contract_risks():
    """Demonstrate smart contract security risks."""
    print("\n" + "=" * 60)
    print("SMART CONTRACT SECURITY RISKS")
    print("=" * 60)

    vulnerabilities = [
        {
            "name": "Reentrancy",
            "description": "Contract calls external contract before updating state",
            "example": "DAO Hack (2016) - $60M stolen",
            "prevention": "Checks-Effects-Interactions pattern",
        },
        {
            "name": "Integer Overflow/Underflow",
            "description": "Arithmetic operations wrap around unexpectedly",
            "example": "BeautyChain (2018) - Overflow created unlimited tokens",
            "prevention": "Use SafeMath libraries or Solidity 0.8+ built-in checks",
        },
        {
            "name": "Access Control",
            "description": "Missing authorization checks on sensitive functions",
            "example": "Parity Wallet (2017) - $30M stolen due to unprotected init",
            "prevention": "Explicit access control modifiers (onlyOwner, roles)",
        },
        {
            "name": "Front-Running",
            "description": "Attacker sees pending transaction and submits higher fee",
            "example": "DEX trading - MEV extraction",
            "prevention": "Commit-reveal schemes, batch auctions",
        },
    ]

    for vuln in vulnerabilities:
        print(f"\n[{vuln['name']}]")
        print(f"  Description: {vuln['description']}")
        print(f"  Example:     {vuln['example']}")
        print(f"  Prevention:  {vuln['prevention']}")

    print("\nBest Practices:")
    print("  - Formal verification of critical contracts")
    print("  - Multiple independent audits")
    print("  - Bug bounty programs")
    print("  - Test on testnets before mainnet")
    print("  - Upgrade mechanisms (proxy patterns)")


def main():
    print("=" * 60)
    print("BLOCKCHAIN SECURITY DEMO")
    print("=" * 60)
    print("Learn blockchain security concepts through simulation.\n")

    while True:
        print("\nMenu:")
        print("1. Blockchain Basics")
        print("2. Tamper Detection")
        print("3. Consensus Mechanisms")
        print("4. Smart Contract Risks")
        print("5. Run All Demos")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            demo_blockchain_basics()
        elif choice == "2":
            demo_tamper_detection()
        elif choice == "3":
            demo_consensus()
        elif choice == "4":
            demo_smart_contract_risks()
        elif choice == "5":
            demo_blockchain_basics()
            demo_tamper_detection()
            demo_consensus()
            demo_smart_contract_risks()
        elif choice == "6":
            print("Block by block!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
