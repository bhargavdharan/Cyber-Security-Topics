#!/usr/bin/env python3
"""
Simple TCP Port Scanner
Educational tool for understanding port scanning concepts.

WARNING: Only scan hosts you own or have explicit written permission to scan.
Unauthorized port scanning may be illegal in your jurisdiction.
"""

import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Common ports and their typical services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
}


def scan_port(target, port, timeout=1):
    """Scan a single TCP port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except (OSError, socket.error):
                    service = COMMON_PORTS.get(port, "Unknown")
                return port, True, service
            return port, False, None
    except socket.gaierror:
        return None, None, None
    except Exception:
        return port, False, None


def scan_host(target, ports, max_workers=50):
    """Scan multiple ports on a target host."""
    open_ports = []
    closed_count = 0

    print(f"\nScanning {target}...")
    print(f"Ports to scan: {len(ports)}")
    print("-" * 40)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}

        for future in as_completed(futures):
            port, is_open, service = future.result()
            if port is None:
                print("Error: Could not resolve target.")
                return []
            if is_open:
                open_ports.append((port, service))
                print(f"[OPEN] Port {port:<5} - {service}")
            else:
                closed_count += 1

    print("-" * 40)
    print(f"Scan complete. Open ports: {len(open_ports)}, Closed: {closed_count}")
    return open_ports


def get_port_range():
    """Get port range from user."""
    print("\nPort range options:")
    print("1. Common ports only (top 14)")
    print("2. Well-known ports (1-1024)")
    print("3. Full range (1-65535)")
    print("4. Custom range")

    choice = input("Select option (1-4): ").strip()

    if choice == "1":
        return sorted(COMMON_PORTS.keys())
    elif choice == "2":
        return list(range(1, 1025))
    elif choice == "3":
        return list(range(1, 65536))
    elif choice == "4":
        start = int(input("Start port: ") or "1")
        end = int(input("End port: ") or "1024")
        return list(range(max(1, start), min(65536, end + 1)))
    else:
        return sorted(COMMON_PORTS.keys())


def banner_grab(target, port):
    """Attempt to grab a service banner."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((target, port))
            # Send a generic probe
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            if banner:
                return banner[:200]
    except Exception:
        pass
    return None


def main():
    print("=" * 60)
    print("TCP PORT SCANNER (EDUCATIONAL)")
    print("=" * 60)
    print("WARNING: Only scan systems you own or have permission to scan!")
    print("=" * 60)

    target = input("\nEnter target IP or hostname: ").strip()
    if not target:
        print("No target provided. Exiting.")
        return

    # Resolve hostname to IP for display
    try:
        ip = socket.gethostbyname(target)
        if ip != target:
            print(f"Resolved {target} to {ip}")
    except socket.gaierror:
        print(f"Could not resolve {target}")
        return

    ports = get_port_range()

    # Confirmation
    confirm = input(f"\nScan {len(ports)} ports on {target}? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("Scan cancelled.")
        return

    open_ports = scan_host(target, ports)

    if open_ports:
        print(f"\n{'=' * 60}")
        print("OPEN PORTS SUMMARY")
        print(f"{'=' * 60}")
        for port, service in sorted(open_ports):
            print(f"  Port {port}/tcp - {service}")

        # Optional banner grab
        grab = input("\nAttempt banner grabbing on open ports? (yes/no): ").strip().lower()
        if grab in ["yes", "y"]:
            print("\nBanner Grabbing Results:")
            for port, service in sorted(open_ports):
                banner = banner_grab(target, port)
                if banner:
                    print(f"  Port {port}: {banner[:100]}")
                else:
                    print(f"  Port {port}: No banner received")
    else:
        print("\nNo open ports found (or host is unreachable).")

    print("\nScanning complete. Remember: ethical hacking requires authorization!")


if __name__ == "__main__":
    main()
