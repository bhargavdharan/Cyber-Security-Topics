#!/usr/bin/env python3
"""
Log Monitor Simulator
Demonstrates how SIEM systems and log monitors detect suspicious activity.
Analyzes sample log entries for security events.
"""

import random
import re
from datetime import datetime, timedelta


# Sample log templates for different event types
LOG_TEMPLATES = {
    "normal_login": [
        "{timestamp} auth success: user={user} from={ip} method=password",
        "{timestamp} session opened for user {user} by (uid=0)",
    ],
    "failed_login": [
        "{timestamp} auth failure: user={user} from={ip} method=password reason=invalid_credentials",
        "{timestamp} Failed password for {user} from {ip} port {port} ssh2",
        "{timestamp} authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip} user={user}",
    ],
    "privilege_escalation": [
        "{timestamp} sudo: {user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/bin/bash",
        "{timestamp} sudo: {user} : user NOT in sudoers ; TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/bin/bash",
    ],
    "file_access": [
        "{timestamp} file_access: user={user} file=/etc/passwd action=read",
        "{timestamp} file_access: user={user} file=/var/log/syslog action=read",
        "{timestamp} file_access: user={user} file=/etc/shadow action=read_denied",
    ],
    "network": [
        "{timestamp} connection: src={ip}:54321 dst=192.168.1.10:22 proto=tcp state=established",
        "{timestamp} connection: src={ip}:12345 dst=192.168.1.10:3389 proto=tcp state=blocked",
        "{timestamp} firewall: BLOCKED connection from {ip} to port 23 (Telnet)",
    ],
    "malware": [
        "{timestamp} ALERT: suspicious process detected: pid={pid} cmd='/tmp/.hidden/script.sh' user={user}",
        "{timestamp} ALERT: outbound connection to known C2 server: {ip} port 4444",
        "{timestamp} WARNING: multiple failed login attempts followed by success: user={user}",
    ],
}

USERS = ["admin", "root", "john_doe", "jane_smith", "webserver", "backup_user", "guest"]
IPS = [f"192.168.1.{i}" for i in range(2, 20)] + ["10.0.0.5", "172.16.0.10"]
EXTERNAL_IPS = [f"203.0.113.{i}" for i in range(1, 20)]  # RFC 5737 documentation IPs


def generate_timestamp(base_time=None, offset_minutes=0):
    """Generate a log timestamp."""
    if base_time is None:
        base_time = datetime.now()
    time = base_time + timedelta(minutes=offset_minutes)
    return time.strftime("%Y-%m-%d %H:%M:%S")


def generate_sample_logs(count=50):
    """Generate a mixed log file with normal and suspicious events."""
    logs = []
    base_time = datetime.now() - timedelta(hours=2)

    # Generate brute force attack pattern
    attacker_ip = random.choice(EXTERNAL_IPS)
    target_user = random.choice(["admin", "root"])
    attack_start = 10

    for i in range(count):
        # Determine event type with weighted probabilities
        if 10 <= i <= 15:
            # Simulate brute force burst
            event_type = "failed_login"
            user = target_user
            ip = attacker_ip
        elif i == 16:
            # Successful login after brute force
            event_type = "normal_login"
            user = target_user
            ip = attacker_ip
        elif i == 17:
            # Privilege escalation attempt
            event_type = random.choice(["privilege_escalation", "file_access"])
            user = target_user
            ip = attacker_ip
        elif i == 18:
            # Malware indicator
            event_type = "malware"
            user = target_user
            ip = attacker_ip
        else:
            event_type = random.choice([
                "normal_login", "normal_login", "normal_login",
                "failed_login", "file_access", "network"
            ])
            user = random.choice(USERS)
            ip = random.choice(IPS + EXTERNAL_IPS)

        template = random.choice(LOG_TEMPLATES[event_type])
        log_entry = template.format(
            timestamp=generate_timestamp(base_time, i),
            user=user,
            ip=ip,
            port=random.randint(10000, 65000),
            pid=random.randint(1000, 9999),
        )
        logs.append((log_entry, event_type))

    return logs


def analyze_logs(logs):
    """Analyze logs for security incidents."""
    print("\n" + "=" * 60)
    print("LOG ANALYSIS RESULTS")
    print("=" * 60)

    findings = {
        "brute_force": [],
        "privilege_escalation": [],
        "suspicious_files": [],
        "malware_indicators": [],
        "external_access": [],
    }

    # Track failed logins by IP
    failed_logins_by_ip = {}
    login_attempts = {}

    for log_entry, event_type in logs:
        # Extract IP if present
        ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', log_entry)
        ip = ip_match.group(1) if ip_match else "unknown"

        if event_type == "failed_login":
            failed_logins_by_ip[ip] = failed_logins_by_ip.get(ip, 0) + 1

        if "user=" in log_entry:
            user_match = re.search(r'user=(\S+)', log_entry)
            user = user_match.group(1) if user_match else "unknown"
            if user not in login_attempts:
                login_attempts[user] = {"success": 0, "failure": 0}
            if event_type == "normal_login":
                login_attempts[user]["success"] += 1
            elif event_type == "failed_login":
                login_attempts[user]["failure"] += 1

        if "sudo:" in log_entry and "USER=root" in log_entry:
            if "NOT in sudoers" in log_entry:
                findings["privilege_escalation"].append(log_entry)
            else:
                findings["privilege_escalation"].append(log_entry)

        if "action=read_denied" in log_entry and "/etc/shadow" in log_entry:
            findings["suspicious_files"].append(log_entry)

        if "ALERT:" in log_entry or "WARNING:" in log_entry:
            findings["malware_indicators"].append(log_entry)

        if ip in EXTERNAL_IPS and event_type in ["normal_login", "failed_login"]:
            findings["external_access"].append(log_entry)

    # Detect brute force (5+ failed from same IP)
    for ip, count in failed_logins_by_ip.items():
        if count >= 5:
            findings["brute_force"].append(f"IP {ip}: {count} failed login attempts")

    # Detect successful login after multiple failures
    for user, attempts in login_attempts.items():
        if attempts["failure"] >= 3 and attempts["success"] >= 1:
            findings["brute_force"].append(
                f"User '{user}': {attempts['failure']} failures followed by success (potential breach)"
            )

    # Display findings
    total_findings = sum(len(v) for v in findings.values())
    print(f"\nTotal security events detected: {total_findings}")

    severity_colors = {
        "brute_force": "HIGH",
        "privilege_escalation": "HIGH",
        "suspicious_files": "MEDIUM",
        "malware_indicators": "CRITICAL",
        "external_access": "MEDIUM",
    }

    for category, items in findings.items():
        if items:
            severity = severity_colors.get(category, "LOW")
            print(f"\n[{severity}] {category.upper().replace('_', ' ')} ({len(items)} events)")
            for item in items:
                print(f"  - {item[:100]}")

    return findings


def display_raw_logs(logs):
    """Display the generated log entries."""
    print("\n" + "=" * 60)
    print("GENERATED LOG ENTRIES")
    print("=" * 60)
    for log_entry, event_type in logs:
        marker = ""
        if event_type in ["failed_login", "privilege_escalation", "malware"]:
            marker = "*"
        print(f"{marker:<2} {log_entry}")


def main():
    print("=" * 60)
    print("LOG MONITOR SIMULATOR")
    print("=" * 60)
    print("This tool generates simulated system logs and analyzes them")
    print("for security threats including brute force, privilege escalation,")
    print("and malware indicators.\n")

    log_count = int(input("Number of log entries to generate [default: 50]: ") or "50")
    logs = generate_sample_logs(log_count)

    while True:
        print("\nMenu:")
        print("1. View Raw Logs")
        print("2. Run Security Analysis")
        print("3. View Both")
        print("4. Generate New Logs")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            display_raw_logs(logs)
        elif choice == "2":
            analyze_logs(logs)
        elif choice == "3":
            display_raw_logs(logs)
            analyze_logs(logs)
        elif choice == "4":
            log_count = int(input("Number of log entries [default: 50]: ") or "50")
            logs = generate_sample_logs(log_count)
            print(f"Generated {log_count} new log entries.")
        elif choice == "5":
            print("Keep monitoring those logs!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
