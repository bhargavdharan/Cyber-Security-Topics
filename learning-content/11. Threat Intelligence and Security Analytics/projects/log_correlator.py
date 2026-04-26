#!/usr/bin/env python3
"""
Log Correlator
Correlates security events across multiple log sources.
"""

from datetime import datetime, timedelta


class LogCorrelator:
    """Correlates events from multiple log sources."""

    def __init__(self):
        self.events = []

    def add_event(self, timestamp, source, event_type, description, metadata=None):
        """Add an event to the correlator."""
        self.events.append({
            "timestamp": timestamp,
            "source": source,
            "type": event_type,
            "description": description,
            "metadata": metadata or {},
        })

    def correlate_by_time(self, window_seconds=300):
        """Group events that occur within a time window."""
        print(f"\n{'=' * 60}")
        print(f"TIME-BASED CORRELATION (Window: {window_seconds}s)")
        print(f"{'=' * 60}")

        sorted_events = sorted(self.events, key=lambda x: x["timestamp"])
        clusters = []
        current_cluster = []

        for event in sorted_events:
            if not current_cluster:
                current_cluster = [event]
            else:
                last_time = current_cluster[-1]["timestamp"]
                if (event["timestamp"] - last_time).total_seconds() <= window_seconds:
                    current_cluster.append(event)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [event]

        if current_cluster:
            clusters.append(current_cluster)

        for i, cluster in enumerate(clusters, 1):
            print(f"\n--- Event Cluster {i} ({len(cluster)} events) ---")
            for event in cluster:
                print(f"  [{event['timestamp'].strftime('%H:%M:%S')}] "
                      f"{event['source']:<15} {event['type']:<15} {event['description']}")

        return clusters

    def correlate_by_entity(self, entity_key, entity_value):
        """Find all events related to a specific entity."""
        print(f"\n{'=' * 60}")
        print(f"ENTITY CORRELATION: {entity_key}={entity_value}")
        print(f"{'=' * 60}")

        related = []
        for event in self.events:
            if event["metadata"].get(entity_key) == entity_value:
                related.append(event)

        if not related:
            print("No related events found")
            return []

        for event in sorted(related, key=lambda x: x["timestamp"]):
            print(f"  [{event['timestamp'].strftime('%H:%M:%S')}] "
                  f"{event['source']:<15} {event['type']:<15} {event['description']}")

        return related

    def detect_attack_chains(self):
        """Detect multi-stage attack patterns."""
        print(f"\n{'=' * 60}")
        print("ATTACK CHAIN DETECTION")
        print(f"{'=' * 60}")

        # Define attack chain patterns
        patterns = [
            {
                "name": "Brute Force -> Lateral Movement",
                "stages": ["AUTH_FAILURE", "AUTH_FAILURE", "AUTH_SUCCESS", "LATERAL_MOVEMENT"],
            },
            {
                "name": "Phishing -> Malware -> C2",
                "stages": ["EMAIL_PHISHING", "MALWARE_EXECUTION", "C2_CONNECTION"],
            },
            {
                "name": "Reconnaissance -> Exploitation",
                "stages": ["PORT_SCAN", "VULNERABILITY_EXPLOIT", "PRIVILEGE_ESCALATION"],
            },
        ]

        event_types = [e["type"] for e in sorted(self.events, key=lambda x: x["timestamp"])]

        for pattern in patterns:
            # Simple pattern matching
            pattern_str = ",".join(pattern["stages"])
            events_str = ",".join(event_types)
            if pattern_str in events_str or all(stage in event_types for stage in pattern["stages"]):
                print(f"\n[!] DETECTED: {pattern['name']}")
                print("Stages observed:")
                for stage in pattern["stages"]:
                    matching = [e for e in self.events if e["type"] == stage]
                    for e in matching[:1]:  # Show first occurrence
                        print(f"  - {stage}: {e['description']}")


def demo_correlation():
    """Demonstrate log correlation with sample data."""
    print("\n" + "=" * 60)
    print("LOG CORRELATION DEMO")
    print("=" * 60)

    correlator = LogCorrelator()
    base_time = datetime(2024, 3, 15, 14, 0, 0)

    # Simulate a multi-stage attack
    events = [
        (0, "Firewall", "PORT_SCAN", "Port scan from 203.0.113.77", {"src_ip": "203.0.113.77"}),
        (2, "Email", "EMAIL_PHISHING", "Phishing email delivered to user", {"user": "john"}),
        (5, "Web", "MALWARE_DOWNLOAD", "User downloaded suspicious file", {"user": "john", "file": "invoice.exe"}),
        (10, "Endpoint", "MALWARE_EXECUTION", "Process invoice.exe started", {"user": "john", "process": "invoice.exe"}),
        (15, "Auth", "AUTH_FAILURE", "Failed login for admin", {"user": "admin", "src_ip": "203.0.113.77"}),
        (16, "Auth", "AUTH_FAILURE", "Failed login for admin", {"user": "admin", "src_ip": "203.0.113.77"}),
        (17, "Auth", "AUTH_FAILURE", "Failed login for admin", {"user": "admin", "src_ip": "203.0.113.77"}),
        (18, "Auth", "AUTH_SUCCESS", "Successful login for admin", {"user": "admin", "src_ip": "203.0.113.77"}),
        (20, "Network", "C2_CONNECTION", "Outbound connection to 185.220.101.5", {"src_ip": "10.0.0.50"}),
        (25, "Endpoint", "PRIVILEGE_ESCALATION", "Admin privilege escalation detected", {"user": "admin"}),
        (30, "File", "DATA_ACCESS", "Bulk file access detected", {"user": "admin", "files": 150}),
    ]

    for offset, source, event_type, desc, meta in events:
        correlator.add_event(base_time + timedelta(minutes=offset), source, event_type, desc, meta)

    # Show all events
    print("\n--- All Events ---")
    for event in correlator.events:
        print(f"[{event['timestamp'].strftime('%H:%M')}] {event['source']:<12} "
              f"{event['type']:<20} {event['description']}")

    # Run correlations
    correlator.correlate_by_time(window_seconds=600)
    correlator.correlate_by_entity("user", "admin")
    correlator.correlate_by_entity("src_ip", "203.0.113.77")
    correlator.detect_attack_chains()


def main():
    print("=" * 60)
    print("LOG CORRELATOR")
    print("=" * 60)
    print("Learn to correlate security events across multiple sources.\n")

    while True:
        print("\nMenu:")
        print("1. Correlation Demo")
        print("2. Exit")

        choice = input("\nSelect option (1-2): ").strip()

        if choice == "1":
            demo_correlation()
        elif choice == "2":
            print("Connect the dots!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
