#!/usr/bin/env python3
"""
Secure Code Examples
Demonstrates insecure vs secure coding patterns.
"""

import hashlib
import html
import re


class InsecureCode:
    """Examples of insecure code patterns."""

    @staticmethod
    def sql_query(user_input):
        """Vulnerable to SQL injection."""
        # NEVER DO THIS
        query = f"SELECT * FROM users WHERE username = '{user_input}'"
        return query

    @staticmethod
    def display_user_input(user_input):
        """Vulnerable to XSS."""
        # NEVER DO THIS
        html_output = f"<div>{user_input}</div>"
        return html_output

    @staticmethod
    def verify_password(stored_hash, password):
        """Timing attack vulnerable."""
        # NEVER DO THIS - direct comparison leaks timing info
        return stored_hash == hashlib.md5(password.encode()).hexdigest()

    @staticmethod
    def parse_command(user_input):
        """Command injection vulnerable."""
        # NEVER DO THIS
        import os
        os.system(f"ping {user_input}")


class SecureCode:
    """Examples of secure code patterns."""

    @staticmethod
    def sql_query(user_input):
        """Secure parameterized query."""
        # Use parameterized queries
        # query = "SELECT * FROM users WHERE username = ?"
        # cursor.execute(query, (user_input,))
        return "SELECT * FROM users WHERE username = ?", (user_input,)

    @staticmethod
    def display_user_input(user_input):
        """Secure output encoding."""
        # Encode output for HTML context
        safe_output = html.escape(user_input)
        return f"<div>{safe_output}</div>"

    @staticmethod
    def verify_password(stored_hash, password):
        """Timing-safe comparison."""
        # Use constant-time comparison
        import hmac
        computed = hashlib.sha256(password.encode()).hexdigest()
        return hmac.compare_digest(stored_hash, computed)

    @staticmethod
    def validate_input(user_input, pattern):
        """Whitelist input validation."""
        if re.match(pattern, user_input):
            return True, user_input
        return False, None


def demo_sql_injection():
    """Demonstrate SQL injection and prevention."""
    print("\n" + "=" * 60)
    print("SQL INJECTION PREVENTION")
    print("=" * 60)

    user_input = "admin' OR '1'='1"

    print(f"\nUser input: {user_input}")

    print("\n--- INSECURE ---")
    query = InsecureCode.sql_query(user_input)
    print(f"Query: {query}")
    print("Result: SQL injection successful!")

    print("\n--- SECURE ---")
    query, params = SecureCode.sql_query(user_input)
    print(f"Query: {query}")
    print(f"Parameters: {params}")
    print("Result: Input treated as parameter, not executable code")

    print("\nBest Practice: Always use parameterized queries/prepared statements")


def demo_xss_prevention():
    """Demonstrate XSS prevention."""
    print("\n" + "=" * 60)
    print("XSS PREVENTION")
    print("=" * 60)

    user_input = '<script>alert("XSS")</script>'

    print(f"\nUser input: {user_input}")

    print("\n--- INSECURE ---")
    output = InsecureCode.display_user_input(user_input)
    print(f"HTML: {output}")
    print("Result: Script executes in browser!")

    print("\n--- SECURE ---")
    output = SecureCode.display_user_input(user_input)
    print(f"HTML: {output}")
    print("Result: Script displayed as text, does not execute")

    print("\nBest Practice: Encode all output based on context (HTML, JS, CSS, URL)")


def demo_input_validation():
    """Demonstrate input validation."""
    print("\n" + "=" * 60)
    print("INPUT VALIDATION")
    print("=" * 60)

    test_cases = [
        ("john_doe_123", r'^[a-zA-Z0-9_]{3,20}$', "Username"),
        ("john@example.com", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', "Email"),
        ("<script>", r'^[a-zA-Z0-9_]{3,20}$', "Username"),
        ("192.168.1.1", r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', "IP"),
    ]

    print(f"\n{'Input':<25} {'Type':<15} {'Valid?':<10} {'Result'}")
    print("─" * 70)
    for value, pattern, input_type in test_cases:
        valid, result = SecureCode.validate_input(value, pattern)
        status = "YES" if valid else "NO"
        print(f"{value:<25} {input_type:<15} {status:<10} {result if result else 'REJECTED'}")

    print("\nBest Practice: Use whitelist validation - define what's allowed")


def demo_secure_authentication():
    """Demonstrate secure authentication patterns."""
    print("\n" + "=" * 60)
    print("SECURE AUTHENTICATION")
    print("=" * 60)

    print("\nPassword Storage Comparison:")
    password = "user_password_123"

    print("\n--- INSECURE (Plaintext) ---")
    print(f"Stored: {password}")
    print("Risk: If database leaked, all passwords exposed")

    print("\n--- INSECURE (MD5 Hash) ---")
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    print(f"Stored: {md5_hash}")
    print("Risk: MD5 is fast - attackers can crack billions/second")

    print("\n--- SECURE (Salted + Slow Hash) ---")
    import secrets
    salt = secrets.token_hex(16)
    # In production: use bcrypt, Argon2, or PBKDF2
    salted = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    print(f"Salt: {salt}")
    print(f"Hash: {salted.hex()[:40]}...")
    print("Benefit: Slow computation resists brute force")

    print("\nBest Practice: Use bcrypt, Argon2, or PBKDF2 with unique salts")


def main():
    print("=" * 60)
    print("SECURE CODE EXAMPLES")
    print("=" * 60)
    print("Learn secure coding through before/after comparisons.\n")

    while True:
        print("\nMenu:")
        print("1. SQL Injection Prevention")
        print("2. XSS Prevention")
        print("3. Input Validation")
        print("4. Secure Authentication")
        print("5. Run All Demos")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            demo_sql_injection()
        elif choice == "2":
            demo_xss_prevention()
        elif choice == "3":
            demo_input_validation()
        elif choice == "4":
            demo_secure_authentication()
        elif choice == "5":
            demo_sql_injection()
            demo_xss_prevention()
            demo_input_validation()
            demo_secure_authentication()
        elif choice == "6":
            print("Code securely!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
