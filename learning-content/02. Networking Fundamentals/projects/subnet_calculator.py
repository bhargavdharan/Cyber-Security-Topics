#!/usr/bin/env python3
"""
Subnet Calculator
Calculates network address, broadcast, usable hosts, and other subnet details.
Educational tool for learning IPv4 subnetting.
"""

import ipaddress


def ip_to_binary(ip_str):
    """Convert dotted-decimal IP to binary string."""
    octets = ip_str.split('.')
    return '.'.join(format(int(o), '08b') for o in octets)


def calculate_subnet(ip_with_cidr):
    """Calculate and display subnet information."""
    try:
        network = ipaddress.IPv4Network(ip_with_cidr, strict=False)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    # Basic info
    ip = network.network_address
    mask = network.netmask
    wildcard = ipaddress.IPv4Address(int(mask) ^ 0xFFFFFFFF)
    broadcast = network.broadcast_address

    # Host count
    total_hosts = network.num_addresses
    usable_hosts = max(0, total_hosts - 2) if total_hosts > 2 else 0

    # Class identification
    first_octet = int(str(ip).split('.')[0])
    if first_octet <= 127:
        ip_class = "A"
        default_mask = "255.0.0.0"
    elif first_octet <= 191:
        ip_class = "B"
        default_mask = "255.255.0.0"
    elif first_octet <= 223:
        ip_class = "C"
        default_mask = "255.255.255.0"
    elif first_octet <= 239:
        ip_class = "D (Multicast)"
        default_mask = "N/A"
    else:
        ip_class = "E (Experimental)"
        default_mask = "N/A"

    # Usable range
    if usable_hosts > 0:
        first_usable = ip + 1
        last_usable = broadcast - 1
        host_range = f"{first_usable} - {last_usable}"
    else:
        host_range = "N/A (network/host address)"

    # Output
    print("\n" + "=" * 60)
    print("SUBNET CALCULATION RESULTS")
    print("=" * 60)

    print(f"\n{'Input:':<25} {ip_with_cidr}")
    print(f"{'IP Address:':<25} {ip}")
    print(f"{'IP Class:':<25} {ip_class}")
    print(f"{'Default Subnet Mask:':<25} {default_mask}")

    print(f"\n{'CIDR Notation:':<25} /{network.prefixlen}")
    print(f"{'Subnet Mask:':<25} {mask}")
    print(f"{'Wildcard Mask:':<25} {wildcard}")

    print(f"\n{'Network Address:':<25} {ip}")
    print(f"{'Broadcast Address:':<25} {broadcast}")
    print(f"{'Usable Host Range:':<25} {host_range}")
    print(f"{'Usable Hosts:':<25} {usable_hosts:,}")
    print(f"{'Total Addresses:':<25} {total_hosts:,}")

    print(f"\n{'Binary IP Address:':<25} {ip_to_binary(str(ip))}")
    print(f"{'Binary Subnet Mask:':<25} {ip_to_binary(str(mask))}")

    # Network type
    if ip.is_private:
        print(f"\n{'Network Type:':<25} Private (RFC 1918)")
    elif ip.is_loopback:
        print(f"\n{'Network Type:':<25} Loopback")
    else:
        print(f"\n{'Network Type:':<25} Public")

    # Subnetting context
    if network.prefixlen > 24:
        print(f"\nThis is a subnetted Class C network.")
        print(f"Number of subnets: {2 ** (network.prefixlen - 24)}")
    elif network.prefixlen > 16:
        print(f"\nThis is a subnetted Class B network.")
        print(f"Number of subnets: {2 ** (network.prefixlen - 16)}")
    elif network.prefixlen > 8:
        print(f"\nThis is a subnetted Class A network.")
        print(f"Number of subnets: {2 ** (network.prefixlen - 8)}")


def subnetting_practice():
    """Generate practice problems for subnetting."""
    import random

    print("\n" + "=" * 60)
    print("SUBNETTING PRACTICE MODE")
    print("=" * 60)
    print("I'll give you an IP and CIDR. Calculate the answers, then")
    print("press Enter to see the correct solution.\n")

    for i in range(3):
        # Generate random private IP
        first_octet = random.choice([10, 172, 192])
        if first_octet == 10:
            ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        elif first_octet == 172:
            ip = f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
        else:
            ip = f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

        cidr = random.choice([24, 25, 26, 27, 28, 16, 17, 18, 20, 22])

        print(f"\nProblem {i+1}: {ip}/{cidr}")
        print("Calculate:")
        print("  1. Network address")
        print("  2. Broadcast address")
        print("  3. Number of usable hosts")
        print("  4. Usable IP range")

        input("\nPress Enter to see the answer...")
        calculate_subnet(f"{ip}/{cidr}")
        input("\nPress Enter for next problem...")


def main():
    print("=" * 60)
    print("SUBNET CALCULATOR")
    print("=" * 60)
    print("Learn IPv4 subnetting with interactive calculations.\n")

    while True:
        print("\nMenu:")
        print("1. Calculate Subnet")
        print("2. Practice Mode (Quiz)")
        print("3. Exit")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == "1":
            user_input = input("Enter IP with CIDR (e.g., 192.168.1.0/24): ").strip()
            if user_input:
                calculate_subnet(user_input)
        elif choice == "2":
            subnetting_practice()
        elif choice == "3":
            print("Happy subnetting!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
