#!/usr/bin/env python3
"""
DNS Lookup Tool
Educational tool for understanding DNS resolution and record types.
"""

import socket


def forward_lookup(hostname):
    """Resolve hostname to IP address(es)."""
    print(f"\n{'─' * 50}")
    print(f"FORWARD DNS LOOKUP: {hostname}")
    print(f"{'─' * 50}")

    try:
        # gethostbyname only returns one IPv4
        ipv4 = socket.gethostbyname(hostname)
        print(f"IPv4 Address: {ipv4}")
    except socket.gaierror as e:
        print(f"IPv4 lookup failed: {e}")

    try:
        # getaddrinfo returns all addresses
        results = socket.getaddrinfo(hostname, None)
        addresses = set()
        for res in results:
            family, socktype, proto, canonname, sockaddr = res
            addresses.add(sockaddr[0])

        print(f"\nAll resolved addresses:")
        for addr in sorted(addresses):
            ip_type = "IPv6" if ":" in addr else "IPv4"
            print(f"  [{ip_type}] {addr}")

        if len(addresses) > 1:
            print(f"\nNote: This host has {len(addresses)} DNS records (load balancing/redundancy).")

    except socket.gaierror as e:
        print(f"Lookup failed: {e}")


def reverse_lookup(ip_address):
    """Perform reverse DNS lookup."""
    print(f"\n{'─' * 50}")
    print(f"REVERSE DNS LOOKUP: {ip_address}")
    print(f"{'─' * 50}")

    try:
        hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip_address)
        print(f"Primary Hostname: {hostname}")
        if aliaslist:
            print(f"Aliases (CNAMEs): {', '.join(aliaslist)}")
        print(f"IP Addresses:     {', '.join(ipaddrlist)}")
    except socket.herror as e:
        print(f"Reverse lookup failed: No PTR record found for this IP")


def demonstrate_dns_resolution():
    """Demonstrate the DNS resolution process."""
    print("\n" + "=" * 60)
    print("HOW DNS RESOLUTION WORKS (Step-by-Step)")
    print("=" * 60)

    steps = [
        ("1. User Query", "You type 'www.example.com' in your browser"),
        ("2. Browser Cache", "Browser checks if it recently resolved this domain"),
        ("3. OS Cache", "Operating system checks its DNS cache"),
        ("4. Resolver (ISP)", "Query sent to configured DNS resolver (e.g., 8.8.8.8)"),
        ("5. Root Server", "Resolver asks Root DNS server: 'Where is .com?'"),
        ("6. TLD Server", "Root directs to .com TLD server"),
        ("7. Authoritative", "TLD directs to example.com's authoritative nameserver"),
        ("8. Record Found", "Authoritative server returns the A/AAAA record"),
        ("9. Caching", "Result is cached at each level for TTL duration"),
        ("10. Connection", "Browser connects to the resolved IP address"),
    ]

    for step, description in steps:
        print(f"\n{step}")
        print(f"   {description}")

    print("\n" + "=" * 60)
    print("DNS RECORD TYPES")
    print("=" * 60)

    records = [
        ("A", "Maps hostname to IPv4 address"),
        ("AAAA", "Maps hostname to IPv6 address"),
        ("CNAME", "Alias pointing to another domain name"),
        ("MX", "Mail exchange server for the domain"),
        ("NS", "Authoritative nameserver for the domain"),
        ("PTR", "Reverse DNS - maps IP to hostname"),
        ("TXT", "Text records (SPF, DKIM, verification)"),
        ("SOA", "Start of Authority - zone administration info"),
    ]

    for record, description in records:
        print(f"  {record:<6} - {description}")


def main():
    print("=" * 60)
    print("DNS LOOKUP TOOL")
    print("=" * 60)
    print("Learn how DNS resolution works with interactive lookups.\n")

    while True:
        print("\nMenu:")
        print("1. Forward DNS Lookup (hostname to IP)")
        print("2. Reverse DNS Lookup (IP to hostname)")
        print("3. Learn How DNS Works")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            hostname = input("Enter hostname (e.g., google.com): ").strip()
            if hostname:
                forward_lookup(hostname)
        elif choice == "2":
            ip = input("Enter IP address (e.g., 8.8.8.8): ").strip()
            if ip:
                reverse_lookup(ip)
        elif choice == "3":
            demonstrate_dns_resolution()
        elif choice == "4":
            print("Goodbye! Remember: DNS is the phonebook of the internet.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
