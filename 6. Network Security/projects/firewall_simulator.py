#!/usr/bin/env python3
"""
Firewall Rule Simulator
Educational tool for understanding packet filtering and firewall rules.
"""

import ipaddress
import random


class Firewall:
    """Simulates a packet-filtering firewall."""

    def __init__(self):
        self.rules = []
        self.default_action = "DENY"
        self.log = []

    def add_rule(self, name, action, protocol="any", src_ip="any", dst_ip="any",
                 src_port="any", dst_port="any", enabled=True):
        """Add a firewall rule."""
        rule = {
            "name": name,
            "action": action.upper(),
            "protocol": protocol.lower(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": str(src_port),
            "dst_port": str(dst_port),
            "enabled": enabled,
        }
        self.rules.append(rule)
        return rule

    def check_match(self, rule, packet):
        """Check if a packet matches a rule."""
        if not rule["enabled"]:
            return False

        checks = [
            self._match_protocol(rule["protocol"], packet["protocol"]),
            self._match_ip(rule["src_ip"], packet["src_ip"]),
            self._match_ip(rule["dst_ip"], packet["dst_ip"]),
            self._match_port(rule["src_port"], packet["src_port"]),
            self._match_port(rule["dst_port"], packet["dst_port"]),
        ]
        return all(checks)

    def _match_protocol(self, rule_proto, packet_proto):
        return rule_proto == "any" or rule_proto == packet_proto.lower()

    def _match_ip(self, rule_ip, packet_ip):
        if rule_ip == "any":
            return True
        try:
            network = ipaddress.ip_network(rule_ip, strict=False)
            address = ipaddress.ip_address(packet_ip)
            return address in network
        except ValueError:
            return rule_ip == packet_ip

    def _match_port(self, rule_port, packet_port):
        if rule_port == "any":
            return True
        if "-" in rule_port:
            start, end = map(int, rule_port.split("-"))
            return start <= packet_port <= end
        return int(rule_port) == packet_port

    def process_packet(self, packet):
        """Process a packet through the firewall rules."""
        for i, rule in enumerate(self.rules, 1):
            if self.check_match(rule, packet):
                result = {
                    "packet": packet,
                    "rule": rule,
                    "rule_number": i,
                    "action": rule["action"],
                    "matched": True,
                }
                self.log.append(result)
                return result

        # Default action
        result = {
            "packet": packet,
            "rule": None,
            "rule_number": None,
            "action": self.default_action,
            "matched": False,
        }
        self.log.append(result)
        return result

    def list_rules(self):
        """Display all rules."""
        print(f"\n{'─' * 70}")
        print(f"{'#':<4} {'Name':<20} {'Action':<7} {'Protocol':<10} {'Src':<18} {'Dst':<18} {'Port':<10}")
        print(f"{'─' * 70}")
        for i, rule in enumerate(self.rules, 1):
            status = "ON" if rule["enabled"] else "OFF"
            src = rule["src_ip"]
            dst = rule["dst_ip"]
            port = rule["dst_port"]
            print(f"{i:<4} {rule['name']:<20} {rule['action']:<7} {rule['protocol']:<10} "
                  f"{src:<18} {dst:<18} {port:<10} [{status}]")
        print(f"{'─' * 70}")
        print(f"Default Policy: {self.default_action}")


def demo_basic_firewall():
    """Demonstrate basic firewall operation."""
    print("\n" + "=" * 60)
    print("BASIC FIREWALL SIMULATION")
    print("=" * 60)

    fw = Firewall()
    fw.default_action = "DENY"

    # Add rules
    fw.add_rule("Allow HTTP", "ALLOW", "tcp", "any", "any", "any", 80)
    fw.add_rule("Allow HTTPS", "ALLOW", "tcp", "any", "any", "any", 443)
    fw.add_rule("Allow SSH Internal", "ALLOW", "tcp", "10.0.0.0/8", "any", "any", 22)
    fw.add_rule("Deny SSH External", "DENY", "tcp", "any", "any", "any", 22)
    fw.add_rule("Allow DNS", "ALLOW", "udp", "any", "any", "any", 53)

    fw.list_rules()

    test_packets = [
        {"protocol": "tcp", "src_ip": "192.168.1.100", "dst_ip": "8.8.8.8", "src_port": 54321, "dst_port": 80},
        {"protocol": "tcp", "src_ip": "203.0.113.50", "dst_ip": "10.0.0.5", "src_port": 12345, "dst_port": 22},
        {"protocol": "tcp", "src_ip": "10.0.0.15", "dst_ip": "10.0.0.5", "src_port": 55555, "dst_port": 22},
        {"protocol": "tcp", "src_ip": "192.168.1.100", "dst_ip": "8.8.8.8", "src_port": 54321, "dst_port": 3389},
        {"protocol": "udp", "src_ip": "192.168.1.100", "dst_ip": "8.8.8.8", "src_port": 12345, "dst_port": 53},
    ]

    print("\nTesting Packets:")
    print(f"{'─' * 70}")
    for packet in test_packets:
        result = fw.process_packet(packet)
        action = result["action"]
        rule_name = result["rule"]["name"] if result["rule"] else "Default Policy"
        print(f"{packet['protocol']:<6} {packet['src_ip']:<16}:{packet['src_port']:<6} -> "
              f"{packet['dst_ip']:<16}:{packet['dst_port']:<6} | [{action}] ({rule_name})")


def interactive_firewall():
    """Interactive firewall builder."""
    print("\n" + "=" * 60)
    print("INTERACTIVE FIREWALL BUILDER")
    print("=" * 60)
    print("Build your own firewall rule set and test packets against it.\n")

    fw = Firewall()
    fw.default_action = input("Default policy (ALLOW/DENY) [DENY]: ").strip().upper() or "DENY"

    print("\nAdd firewall rules (leave name empty to finish):")
    print("Format: name | action | protocol | src_ip | dst_ip | dst_port")
    print("Example: Allow Web | ALLOW | tcp | any | any | 80")
    print("Tips: Use CIDR notation for networks (e.g., 192.168.1.0/24)")
    print("      Use port ranges (e.g., 1000-2000)")

    while True:
        rule_input = input("\nRule: ").strip()
        if not rule_input:
            break
        parts = [p.strip() for p in rule_input.split("|")]
        if len(parts) >= 6:
            fw.add_rule(parts[0], parts[1], parts[2], parts[3], parts[4], "any", parts[5])
            print(f"Added rule: {parts[0]}")
        else:
            print("Invalid format. Use: name | action | protocol | src_ip | dst_ip | dst_port")

    fw.list_rules()

    print("\nTest packets (leave empty to finish):")
    print("Format: protocol | src_ip | dst_ip | src_port | dst_port")

    while True:
        pkt_input = input("\nPacket: ").strip()
        if not pkt_input:
            break
        parts = [p.strip() for p in pkt_input.split("|")]
        if len(parts) >= 5:
            packet = {
                "protocol": parts[0],
                "src_ip": parts[1],
                "dst_ip": parts[2],
                "src_port": int(parts[3]),
                "dst_port": int(parts[4]),
            }
            result = fw.process_packet(packet)
            action = result["action"]
            rule = result["rule"]["name"] if result["rule"] else "Default"
            print(f"Result: [{action}] via {rule}")
        else:
            print("Invalid format. Use: protocol | src_ip | dst_ip | src_port | dst_port")


def demo_rule_ordering():
    """Demonstrate why rule order matters."""
    print("\n" + "=" * 60)
    print("RULE ORDERING IMPORTANCE")
    print("=" * 60)

    print("\nFirewall A: Specific rules first")
    fw_a = Firewall()
    fw_a.default_action = "DENY"
    fw_a.add_rule("Deny Telnet", "DENY", "tcp", "any", "any", "any", 23)
    fw_a.add_rule("Allow All TCP", "ALLOW", "tcp", "any", "any", "any", "any")

    packet = {"protocol": "tcp", "src_ip": "10.0.0.1", "dst_ip": "10.0.0.2",
              "src_port": 12345, "dst_port": 23}
    result = fw_a.process_packet(packet)
    print(f"Telnet packet: [{result['action']}] (Rule: {result['rule']['name']})")

    print("\nFirewall B: General rule first (WRONG ORDER)")
    fw_b = Firewall()
    fw_b.default_action = "DENY"
    fw_b.add_rule("Allow All TCP", "ALLOW", "tcp", "any", "any", "any", "any")
    fw_b.add_rule("Deny Telnet", "DENY", "tcp", "any", "any", "any", 23)

    result = fw_b.process_packet(packet)
    print(f"Telnet packet: [{result['action']}] (Rule: {result['rule']['name']})")
    print("\nVULNERABILITY: Telnet is allowed because the general rule matched first!")

    print("\nBEST PRACTICE: Order rules from most specific to most general.")


def main():
    print("=" * 60)
    print("FIREWALL RULE SIMULATOR")
    print("=" * 60)
    print("Learn how packet filtering firewalls evaluate traffic.\n")

    while True:
        print("\nMenu:")
        print("1. Basic Firewall Demo")
        print("2. Interactive Firewall Builder")
        print("3. Rule Ordering Demo")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_basic_firewall()
        elif choice == "2":
            interactive_firewall()
        elif choice == "3":
            demo_rule_ordering()
        elif choice == "4":
            demo_basic_firewall()
            demo_rule_ordering()
        elif choice == "5":
            print("Keep your network secure!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
