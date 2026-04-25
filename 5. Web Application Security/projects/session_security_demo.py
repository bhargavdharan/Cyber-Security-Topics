#!/usr/bin/env python3
"""
Session Security Demo
Demonstrates secure vs insecure session management techniques.
"""

import hashlib
import random
import secrets
import time
from datetime import datetime, timedelta


class InsecureSessionManager:
    """Demonstrates common session management vulnerabilities."""

    def __init__(self):
        self.sessions = {}
        self.counter = 1000

    def create_session(self, username):
        """Vulnerable: predictable session IDs."""
        self.counter += 1
        session_id = f"sess_{self.counter:06d}"  # Predictable!
        self.sessions[session_id] = {
            "user": username,
            "created": time.time(),
            "expires": time.time() + 86400,  # 24 hours, no sliding
        }
        return session_id

    def validate_session(self, session_id):
        """Vulnerable: no expiration check in this version."""
        return session_id in self.sessions


class SecureSessionManager:
    """Demonstrates secure session management."""

    def __init__(self):
        self.sessions = {}
        self.timeout = 1800  # 30 minutes

    def create_session(self, username, ip_address, user_agent):
        """Secure: cryptographically random session ID with metadata."""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            "user": username,
            "created": time.time(),
            "last_accessed": time.time(),
            "ip_address": ip_address,
            "user_agent_hash": hashlib.sha256(user_agent.encode()).hexdigest()[:16],
        }
        return session_id

    def validate_session(self, session_id, ip_address, user_agent):
        """Secure: validate session with multiple checks."""
        if session_id not in self.sessions:
            return False, "Session not found"

        session = self.sessions[session_id]

        # Check expiration
        if time.time() - session["last_accessed"] > self.timeout:
            del self.sessions[session_id]
            return False, "Session expired"

        # Check IP binding (optional but recommended for sensitive apps)
        if session["ip_address"] != ip_address:
            return False, "IP address mismatch"

        # Check user agent consistency
        ua_hash = hashlib.sha256(user_agent.encode()).hexdigest()[:16]
        if session["user_agent_hash"] != ua_hash:
            return False, "User agent mismatch"

        # Update last accessed (sliding expiration)
        session["last_accessed"] = time.time()
        return True, "Valid"

    def destroy_session(self, session_id):
        """Secure session logout."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


def demo_predictable_sessions():
    print("\n" + "=" * 60)
    print("PREDICTABLE SESSION ID DEMO")
    print("=" * 60)

    manager = InsecureSessionManager()

    print("\n--- Generating Sessions ---")
    sessions = []
    for user in ["alice", "bob", "charlie"]:
        sid = manager.create_session(user)
        sessions.append((user, sid))
        print(f"User: {user:<10} Session ID: {sid}")

    print("\n--- Attack Simulation ---")
    print("Attacker observes session ID pattern:")
    print("  sess_001001, sess_001002, sess_001003...")
    print("Attacker can predict: alice might have sess_001000 or sess_001004")
    print("By trying sequential IDs, attacker can hijack sessions!")

    guessed_id = "sess_001002"
    print(f"\nGuessed session ID: {guessed_id}")
    print(f"Valid: {manager.validate_session(guessed_id)}")
    if guessed_id in manager.sessions:
        print(f"Hijacked user: {manager.sessions[guessed_id]['user']}")

    print("\nPREVENTION:")
    print("  - Use cryptographically secure random session IDs")
    print("  - Minimum 128 bits of entropy")
    print("  - Regenerate session ID on privilege changes (login, password change)")


def demo_session_fixation():
    print("\n" + "=" * 60)
    print("SESSION FIXATION DEMO")
    print("=" * 60)

    print("\n--- Attack Scenario ---")
    print("1. Attacker visits site, gets session ID: ABC123")
    print("2. Attacker tricks victim into logging in with URL:")
    print("   https://site.com/login?sessionid=ABC123")
    print("3. Victim logs in, session ABC123 is now authenticated!")
    print("4. Attacker uses ABC123 to access victim's account")

    print("\n--- Prevention ---")
    print("Regenerate session ID upon authentication:")
    print("  BEFORE login:  sess_unauth_abc123")
    print("  AFTER login:   sess_auth_xyz789 (completely new)")
    print("This renders the fixed session ID useless to attacker.")

    print("\nPREVENTION:")
    print("  - Regenerate session ID on login")
    print("  - Accept session IDs only from cookies, not URLs")
    print("  - Mark pre-authentication sessions as unprivileged")


def demo_secure_sessions():
    print("\n" + "=" * 60)
    print("SECURE SESSION MANAGEMENT DEMO")
    print("=" * 60)

    manager = SecureSessionManager()

    print("\n--- Creating Secure Session ---")
    username = "alice"
    ip = "192.168.1.100"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    session_id = manager.create_session(username, ip, user_agent)
    print(f"User: {username}")
    print(f"Session ID: {session_id}")
    print(f"Length: {len(session_id)} chars (high entropy)")

    print("\n--- Validating Session ---")
    valid, msg = manager.validate_session(session_id, ip, user_agent)
    print(f"Same IP/UA: {valid} ({msg})")

    print("\n--- Attack: Session Hijacking from Different IP ---")
    attacker_ip = "10.0.0.50"
    valid, msg = manager.validate_session(session_id, attacker_ip, user_agent)
    print(f"Different IP: {valid} ({msg})")

    print("\n--- Attack: Stolen Session with Changed User Agent ---")
    attacker_ua = "HackerBrowser/1.0"
    valid, msg = manager.validate_session(session_id, ip, attacker_ua)
    print(f"Different UA: {valid} ({msg})")

    print("\n--- Session Timeout Demo ---")
    print("Simulating 31 minutes of inactivity...")
    manager.sessions[session_id]["last_accessed"] = time.time() - 1860
    valid, msg = manager.validate_session(session_id, ip, user_agent)
    print(f"After timeout: {valid} ({msg})")

    print("\n--- Secure Logout ---")
    new_session = manager.create_session("alice", ip, user_agent)
    print(f"Created session: {new_session[:20]}...")
    manager.destroy_session(new_session)
    valid, msg = manager.validate_session(new_session, ip, user_agent)
    print(f"After logout: {valid} ({msg})")


def demo_session_best_practices():
    print("\n" + "=" * 60)
    print("SESSION SECURITY BEST PRACTICES")
    print("=" * 60)

    practices = [
        ("Cookie Attributes", [
            "HttpOnly: Prevent JavaScript access to session cookie",
            "Secure: Only transmit over HTTPS",
            "SameSite: Prevent CSRF attacks",
            "Path: Limit cookie to specific paths",
        ]),
        ("Session Lifecycle", [
            "Regenerate ID on login, privilege change, password change",
            "Implement absolute timeout (e.g., 24 hours max)",
            "Implement idle timeout (e.g., 30 minutes)",
            "Invalidate session server-side on logout",
        ]),
        ("Session Storage", [
            "Store sessions server-side (database, Redis)",
            "Don't store sensitive data in client-side sessions",
            "Encrypt session data at rest",
        ]),
        ("Detection", [
            "Monitor for concurrent sessions from different locations",
            "Alert on suspicious session patterns",
            "Log all session creation and destruction events",
        ]),
    ]

    for category, items in practices:
        print(f"\n{category}:")
        for item in items:
            print(f"  - {item}")


def main():
    print("=" * 60)
    print("SESSION SECURITY DEMO")
    print("=" * 60)
    print("Learn how to manage web sessions securely.\n")

    while True:
        print("\nMenu:")
        print("1. Predictable Session IDs")
        print("2. Session Fixation Attack")
        print("3. Secure Session Management")
        print("4. Best Practices")
        print("5. Run All Demos")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            demo_predictable_sessions()
        elif choice == "2":
            demo_session_fixation()
        elif choice == "3":
            demo_secure_sessions()
        elif choice == "4":
            demo_session_best_practices()
        elif choice == "5":
            demo_predictable_sessions()
            demo_session_fixation()
            demo_secure_sessions()
            demo_session_best_practices()
        elif choice == "6":
            print("Protect those sessions!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
