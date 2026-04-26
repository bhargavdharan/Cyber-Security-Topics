#!/usr/bin/env python3
"""
Vulnerable Web App Simulator
Command-line simulation of common web application vulnerabilities.
"""

import hashlib
import secrets


class VulnerableApp:
    """Simulates a web application with common vulnerabilities."""

    def __init__(self):
        self.users = {
            "admin": {"password": "admin123", "role": "admin", "id": "1"},
            "john": {"password": "password", "role": "user", "id": "2"},
            "jane": {"password": "123456", "role": "user", "id": "3"},
        }
        self.sessions = {}

    def vulnerable_login(self, username, password):
        """Vulnerable login: no rate limiting, verbose errors, weak comparison."""
        if username not in self.users:
            return {"success": False, "error": "User not found"}

        user = self.users[username]
        # Vulnerable: timing attack possible (direct string compare)
        # Vulnerable: no account lockout
        # Vulnerable: verbose error messages
        if user["password"] == password:
            session_id = hashlib.md5(f"{username}:{password}".encode()).hexdigest()
            self.sessions[session_id] = {"user": username, "role": user["role"]}
            return {
                "success": True,
                "session_id": session_id,
                "user": username,
                "role": user["role"],
            }
        else:
            return {"success": False, "error": "Password incorrect"}

    def secure_login(self, username, password):
        """Secure login implementation."""
        # Secure: generic error message (don't reveal if username exists)
        # Secure: constant-time comparison
        # Secure: strong session IDs
        generic_error = {"success": False, "error": "Invalid credentials"}

        if username not in self.users:
            return generic_error

        user = self.users[username]
        # In real code, use hmac.compare_digest for constant-time comparison
        if not secrets.compare_digest(user["password"], password):
            return generic_error

        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {"user": username, "role": user["role"]}
        return {
            "success": True,
            "session_id": session_id,
            "message": "Login successful",
        }

    def insecure_direct_object_reference(self, user_id, session):
        """Vulnerable: no authorization check."""
        # Vulnerable: any logged-in user can access any user's data
        for username, data in self.users.items():
            if data["id"] == user_id:
                return {
                    "username": username,
                    "role": data["role"],
                    "password": data["password"],  # Exposing password!
                }
        return {"error": "User not found"}

    def secure_data_access(self, user_id, session):
        """Secure: verify authorization."""
        if not session or "user" not in session:
            return {"error": "Not authenticated"}

        current_user = session["user"]
        current_role = self.users[current_user]["role"]

        # Users can only access their own data unless they're admin
        target_user = None
        for username, data in self.users.items():
            if data["id"] == user_id:
                target_user = username
                break

        if not target_user:
            return {"error": "Not found"}

        if current_role != "admin" and target_user != current_user:
            return {"error": "Access denied"}

        # Never return passwords
        return {
            "username": target_user,
            "role": self.users[target_user]["role"],
            "id": user_id,
        }


def demo_broken_authentication():
    print("\n" + "=" * 60)
    print("BROKEN AUTHENTICATION DEMO")
    print("=" * 60)

    app = VulnerableApp()

    print("\n--- Vulnerable Login ---")
    print("Attempt 1: Valid login")
    result = app.vulnerable_login("john", "password")
    print(f"Result: {result}")

    print("\nAttempt 2: Wrong password")
    result = app.vulnerable_login("john", "wrong")
    print(f"Result: {result}")
    print("VULNERABILITY: Specific error reveals the username exists!")

    print("\nAttempt 3: Username doesn't exist")
    result = app.vulnerable_login("hacker", "password")
    print(f"Result: {result}")

    print("\nAttempt 4: Weak session ID (predictable)")
    result = app.vulnerable_login("admin", "admin123")
    print(f"Session ID: {result.get('session_id', 'N/A')}")
    print("VULNERABILITY: Session ID derived from credentials - easily guessable!")

    print("\n--- Secure Login ---")
    result = app.secure_login("john", "password")
    print(f"Result: {result}")

    print("\n--- Wrong Password (Secure) ---")
    result = app.secure_login("john", "wrong")
    print(f"Result: {result}")
    print("SECURE: Generic error doesn't reveal if username exists.")

    print("\nPREVENTION:")
    print("  - Use generic error messages for failed logins")
    print("  - Implement account lockout after failed attempts")
    print("  - Use cryptographically secure random session IDs")
    print("  - Implement multi-factor authentication (MFA)")


def demo_broken_access_control():
    print("\n" + "=" * 60)
    print("BROKEN ACCESS CONTROL DEMO")
    print("=" * 60)

    app = VulnerableApp()

    # Login as regular user
    login_result = app.vulnerable_login("john", "password")
    session = app.sessions.get(login_result.get("session_id"))

    print("\n--- Insecure Direct Object Reference (IDOR) ---")
    print("Logged in as: john (regular user)")
    print("Attempting to access admin's data (user_id=1)...")
    result = app.insecure_direct_object_reference("1", session)
    print(f"Result: {result}")
    print("VULNERABILITY: Regular user can access admin's password!")

    print("\n--- Secure Access Control ---")
    result = app.secure_data_access("1", session)
    print(f"Result: {result}")
    print("SECURE: Access denied - users can't access other users' data.")

    print("\nPREVENTION:")
    print("  - Implement server-side authorization checks")
    print("  - Use indirect reference maps (GUIDs instead of sequential IDs)")
    print("  - Deny by default, allow explicitly")
    print("  - Log access control failures")


def demo_security_misconfiguration():
    print("\n" + "=" * 60)
    print("SECURITY MISCONFIGURATION DEMO")
    print("=" * 60)

    configs = {
        "Production": {
            "debug_mode": False,
            "default_credentials": False,
            "error_details": False,
            "security_headers": True,
            "version_disclosure": False,
        },
        "Misconfigured": {
            "debug_mode": True,
            "default_credentials": True,
            "error_details": True,
            "security_headers": False,
            "version_disclosure": True,
        },
    }

    for name, config in configs.items():
        print(f"\n--- {name} Configuration ---")
        issues = 0
        for setting, value in config.items():
            status = "OK" if not value or setting in ["security_headers"] and value else "RISK"
            if status == "RISK":
                issues += 1
            print(f"  [{status}] {setting}: {value}")
        print(f"Security issues found: {issues}")

    print("\nPREVENTION:")
    print("  - Automate hardening (CIS benchmarks, infrastructure-as-code)")
    print("  - Remove default accounts and passwords")
    print("  - Disable debug mode in production")
    print("  - Implement security headers (HSTS, CSP, X-Frame-Options)")


def demo_sensitive_data_exposure():
    print("\n" + "=" * 60)
    print("SENSITIVE DATA EXPOSURE DEMO")
    print("=" * 60)

    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "ssn": "123-45-6789",
        "credit_card": "4532-1234-5678-9012",
        "password_hash": "5f4dcc3b5aa765d61d8327deb882cf99",  # md5('password')
    }

    print("\n--- Vulnerable Data Exposure ---")
    print("API Response (insecure):")
    print(f"  {user_data}")
    print("VULNERABILITY: All sensitive data exposed, weak hash algorithm!")

    print("\n--- Secure Data Handling ---")
    secure_response = {
        "username": user_data["username"],
        "email": user_data["email"],
        "ssn": "***-**-6789",  # Masked
        "credit_card": "****-****-****-9012",  # Tokenized
        "password_hash": "[REDACTED]",
    }
    print("API Response (secure):")
    print(f"  {secure_response}")

    print("\nPREVENTION:")
    print("  - Encrypt sensitive data at rest (AES-256)")
    print("  - Use TLS for data in transit")
    print("  - Mask sensitive data in logs and UI")
    print("  - Use strong password hashing (bcrypt, Argon2)")
    print("  - Minimize data collection (only store what's needed)")


def main():
    print("=" * 60)
    print("VULNERABLE WEB APP SIMULATOR")
    print("=" * 60)
    print("Learn about web vulnerabilities through interactive simulations.\n")

    while True:
        print("\nMenu:")
        print("1. Broken Authentication")
        print("2. Broken Access Control (IDOR)")
        print("3. Security Misconfiguration")
        print("4. Sensitive Data Exposure")
        print("5. Run All Demos")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            demo_broken_authentication()
        elif choice == "2":
            demo_broken_access_control()
        elif choice == "3":
            demo_security_misconfiguration()
        elif choice == "4":
            demo_sensitive_data_exposure()
        elif choice == "5":
            demo_broken_authentication()
            demo_broken_access_control()
            demo_security_misconfiguration()
            demo_sensitive_data_exposure()
        elif choice == "6":
            print("Secure coding is everyone's responsibility!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
