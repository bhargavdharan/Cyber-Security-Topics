#!/usr/bin/env python3
"""
Web Directory Enumerator Simulator
Educational tool demonstrating directory enumeration concepts.
"""

import random

# Common web paths that might exist on a server
COMMON_PATHS = [
    "/admin", "/administrator", "/login", "/api", "/backup",
    "/config", "/console", "/dashboard", "/db", "/debug",
    "/files", "/images", "/includes", "/install", "/js",
    "/logs", "/old", "/phpmyadmin", "/robots.txt", "/server-status",
    "/sitemap.xml", "/source", "/sql", "/test", "/tmp",
    "/uploads", "/wp-admin", "/wp-content", "/wp-login.php",
    "/.env", "/.git", "/.htaccess", "/.svn", "/cgi-bin",
    "/api/v1", "/api/v2", "/swagger", "/docs", "/graphql",
]

# Simulated responses for a target server
SIMULATED_RESPONSES = {
    "/admin": (200, "Admin Panel", True),
    "/login": (200, "Login Page", True),
    "/api": (200, "API Documentation", True),
    "/robots.txt": (200, "User-agent: *", False),
    "/sitemap.xml": (200, "XML Sitemap", False),
    "/.env": (200, "DB_PASSWORD=secret123", True),  # Sensitive!
    "/backup": (200, "Directory Listing", True),
    "/phpmyadmin": (200, "phpMyAdmin Login", True),
    "/server-status": (200, "Apache Status", True),
    "/.git": (200, "Git Repository", True),
    "/debug": (200, "Debug Info: SQL queries...", True),
    "/test": (200, "Test Page", False),
    "/uploads": (200, "File Upload Directory", True),
}


def simulate_request(target, path):
    """Simulate an HTTP request to a path."""
    # Add some realistic behavior
    if path in SIMULATED_RESPONSES:
        status, content, sensitive = SIMULATED_RESPONSES[path]
        return {
            "status": status,
            "path": path,
            "size": len(content) * 10 + random.randint(100, 5000),
            "content_type": "text/html" if "xml" not in path else "application/xml",
            "sensitive": sensitive,
        }
    else:
        # Random 404 with occasional redirect
        rand = random.random()
        if rand < 0.05:
            return {"status": 301, "path": path, "redirect": path + "/", "sensitive": False}
        return {"status": 404, "path": path, "sensitive": False}


def enumerate_directories(target, wordlist, delay=0):
    """Enumerate directories on a target."""
    print(f"\nStarting enumeration of {target}")
    print(f"Wordlist size: {len(wordlist)} paths")
    print(f"{'─' * 60}")

    found = []
    for path in wordlist:
        response = simulate_request(target, path)

        if response["status"] != 404:
            found.append(response)
            marker = "[!]" if response.get("sensitive") else "[+]"
            size = response.get("size", 0)
            print(f"{marker} {response['status']:>3}  {size:>6}b  {path:<25}", end="")
            if "redirect" in response:
                print(f" -> {response['redirect']}")
            else:
                print()

    print(f"{'─' * 60}")
    print(f"Found {len(found)} accessible paths out of {len(wordlist)} tested")
    return found


def demo_enumeration():
    """Demonstrate directory enumeration."""
    print("\n" + "=" * 60)
    print("DIRECTORY ENUMERATION DEMO")
    print("=" * 60)

    target = "http://example-target.local"
    print(f"\nTarget: {target}")
    print("This simulates discovering hidden directories and files.\n")

    results = enumerate_directories(target, COMMON_PATHS)

    print("\n" + "=" * 60)
    print("SECURITY ANALYSIS")
    print("=" * 60)

    sensitive = [r for r in results if r.get("sensitive")]
    if sensitive:
        print(f"\n[!] FOUND {len(sensitive)} POTENTIALLY SENSITIVE RESOURCES:")
        for r in sensitive:
            print(f"    {r['path']} (Status: {r['status']})")
        print("\nThese should be reviewed and restricted if unnecessary.")
    else:
        print("\nNo obviously sensitive resources found.")

    print("\nBEST PRACTICES:")
    print("  - Remove backup, test, and debug files from production")
    print("  - Restrict access to admin panels by IP")
    print("  - Never expose .env, .git, or config files")
    print("  - Use authentication for all administrative interfaces")
    print("  - Return 404 (not 403) for unauthorized resources")


def demo_rate_limiting():
    """Demonstrate rate limiting concepts."""
    print("\n" + "=" * 60)
    print("RATE LIMITING CONCEPTS")
    print("=" * 60)

    print("\nWhy rate limiting matters:")
    print("  Without rate limiting, attackers can send thousands of")
    print("  requests per second to find hidden directories.")

    scenarios = [
        ("No Rate Limit", 1000, "1 second", "Attacker finds everything quickly"),
        ("Basic Limit (10/sec)", 1000, "100 seconds", "Slows down attacker significantly"),
        ("Aggressive Limit (1/sec)", 1000, "16+ minutes", "Very slow reconnaissance"),
        ("With CAPTCHA after failures", 1000, "Hours", "Automated tools blocked"),
    ]

    print(f"\n{'Strategy':<25} {'Requests':<12} {'Time':<15} {'Impact'}")
    print("─" * 75)
    for name, reqs, time_str, impact in scenarios:
        print(f"{name:<25} {reqs:<12} {time_str:<15} {impact}")

    print("\nRate limiting techniques:")
    print("  - IP-based request throttling")
    print("  - Progressive delays (exponential backoff)")
    print("  - CAPTCHA after threshold")
    print("  - Temporary IP bans")
    print("  - Require authentication for enumeration endpoints")


def interactive_enumeration():
    """Let user configure their own scan."""
    print("\n" + "=" * 60)
    print("INTERACTIVE ENUMERATION")
    print("=" * 60)

    target = input("Target URL [default: http://target.local]: ").strip() or "http://target.local"
    print(f"\nAvailable wordlists:")
    print("1. Common paths (50 items)")
    print("2. Admin panels only (10 items)")
    print("3. API endpoints (15 items)")
    print("4. Full wordlist")

    choice = input("Select wordlist (1-4) [4]: ").strip() or "4"

    if choice == "1":
        wordlist = COMMON_PATHS[:50]
    elif choice == "2":
        wordlist = [p for p in COMMON_PATHS if "admin" in p.lower() or "login" in p.lower()]
    elif choice == "3":
        wordlist = [p for p in COMMON_PATHS if "api" in p.lower()]
    else:
        wordlist = COMMON_PATHS

    # Randomize which paths exist for replayability
    global SIMULATED_RESPONSES
    keys = list(SIMULATED_RESPONSES.keys())
    random.shuffle(keys)
    new_responses = {k: SIMULATED_RESPONSES[k] for k in keys[:random.randint(5, 12)]}
    SIMULATED_RESPONSES = new_responses

    enumerate_directories(target, wordlist)


def main():
    print("=" * 60)
    print("WEB DIRECTORY ENUMERATOR SIMULATOR")
    print("=" * 60)
    print("Learn how attackers discover hidden web resources.\n")
    print("NOTE: This is a SIMULATION for educational purposes.")
    print("Real enumeration requires explicit authorization!\n")

    while True:
        print("\nMenu:")
        print("1. Directory Enumeration Demo")
        print("2. Rate Limiting Concepts")
        print("3. Interactive Enumeration")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_enumeration()
        elif choice == "2":
            demo_rate_limiting()
        elif choice == "3":
            interactive_enumeration()
        elif choice == "4":
            demo_enumeration()
            demo_rate_limiting()
        elif choice == "5":
            print("Enumerate ethically!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
