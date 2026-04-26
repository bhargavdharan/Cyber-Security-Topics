#!/usr/bin/env python3
"""
ICS Network Simulator
Simulates industrial control network architecture and protocols.
"""

import random
import time


class ICSDevice:
    """Base class for ICS devices."""

    def __init__(self, name, device_type, level):
        self.name = name
        self.device_type = device_type
        self.level = level  # Purdue model level
        self.status = "ONLINE"
        self.data = {}

    def read_register(self, address):
        return self.data.get(address, 0)

    def write_register(self, address, value):
        self.data[address] = value


class PLCSimulator(ICSDevice):
    """Simulates a Programmable Logic Controller."""

    def __init__(self, name):
        super().__init__(name, "PLC", 1)
        self.program = {}
        self.inputs = {}
        self.outputs = {}

    def run_cycle(self):
        """Execute one PLC scan cycle."""
        # Read inputs
        for addr in self.inputs:
            self.inputs[addr] = self.read_register(addr)

        # Execute logic (simplified)
        for addr, logic in self.program.items():
            self.outputs[addr] = logic(self.inputs)

        # Write outputs
        for addr, value in self.outputs.items():
            self.write_register(addr, value)

    def modbus_read(self, unit_id, function_code, address, count=1):
        """Simulate Modbus read operation."""
        print(f"  [MODBUS] Unit {unit_id}, FC{function_code}, Addr {address}, Count {count}")
        if function_code == 1:  # Read Coils
            return [self.read_register(address + i) for i in range(count)]
        elif function_code == 3:  # Read Holding Registers
            return [self.read_register(40001 + address + i) for i in range(count)]
        return []

    def modbus_write(self, unit_id, function_code, address, values):
        """Simulate Modbus write operation."""
        print(f"  [MODBUS] Unit {unit_id}, FC{function_code}, Addr {address}, Values {values}")
        if function_code == 6:  # Write Single Register
            self.write_register(40001 + address, values[0])
        elif function_code == 16:  # Write Multiple Registers
            for i, value in enumerate(values):
                self.write_register(40001 + address + i, value)


class ICSNetwork:
    """Simulates an ICS network with Purdue model levels."""

    def __init__(self):
        self.devices = {}
        self.segments = {
            "Enterprise": [],      # Level 4/5
            "DMZ": [],             # Between IT and OT
            "Operations": [],      # Level 3
            "Control": [],         # Level 2
            "Process": [],         # Level 1
            "Physical": [],        # Level 0
        }

    def add_device(self, device, segment):
        self.devices[device.name] = device
        self.segments[segment].append(device)

    def show_architecture(self):
        """Display the network architecture."""
        print("\n" + "=" * 60)
        print("ICS NETWORK ARCHITECTURE (Purdue Model)")
        print("=" * 60)

        for segment, devices in self.segments.items():
            if devices:
                print(f"\n[{segment}]")
                for device in devices:
                    print(f"  {device.name:<20} ({device.device_type}, Level {device.level})")

    def simulate_protocol_traffic(self, protocol="modbus"):
        """Simulate OT protocol traffic."""
        print(f"\n{'=' * 60}")
        print(f"{protocol.upper()} PROTOCOL SIMULATION")
        print(f"{'=' * 60}")

        if protocol == "modbus":
            plc = self.devices.get("PLC-01")
            if plc:
                # Initialize some registers
                plc.write_register(40001, 250)  # Temperature
                plc.write_register(40002, 65)   # Pressure
                plc.write_register(40003, 1)    # Pump status

                print("\nReading process values:")
                temps = plc.modbus_read(1, 3, 0, 3)
                print(f"  Temperature: {temps[0]} C")
                print(f"  Pressure: {temps[1]} PSI")
                print(f"  Pump Status: {'RUNNING' if temps[2] else 'STOPPED'}")

                print("\nWriting control command:")
                plc.modbus_write(1, 6, 3, [1])  # Start pump

        elif protocol == "dnp3":
            print("DNP3 (Distributed Network Protocol) - Common in utilities")
            print("Features: Time synchronization, event buffering, secure authentication")
            print("Typical use: Electric grids, water/wastewater systems")

    def simulate_attack(self, attack_type="man_in_the_middle"):
        """Simulate an attack on the ICS network."""
        print(f"\n{'=' * 60}")
        print(f"ATTACK SIMULATION: {attack_type.upper()}")
        print(f"{'=' * 60}")

        if attack_type == "man_in_the_middle":
            print("\nAttacker positions between HMI and PLC...")
            print("  - Intercepts Modbus read requests")
            print("  - Modifies temperature values before display")
            print("  - Operators see normal values while process is abnormal")
            print("\nImpact: Physical damage possible before detection")

        elif attack_type == "unauthorized_command":
            print("\nAttacker sends unauthorized Modbus write command...")
            print("  - FC 06 (Write Single Register) to pump control")
            print("  - Changes pump state without authorization")
            print("\nImpact: Process disruption, potential safety hazard")

        elif attack_type == "reconnaissance":
            print("\nAttacker scans OT network...")
            print("  - Enumerates Modbus unit IDs")
            print("  - Maps register addresses")
            print("  - Identifies PLC programs and configurations")
            print("\nImpact: Information gathering for targeted attack")


def demo_purdue_model():
    """Demonstrate the Purdue model architecture."""
    network = ICSNetwork()

    # Enterprise (Level 4/5)
    network.add_device(ICSDevice("ERP-Server", "Server", 4), "Enterprise")
    network.add_device(ICSDevice("Email-Server", "Server", 4), "Enterprise")

    # DMZ
    network.add_device(ICSDevice("Data-Historian", "Server", 3), "DMZ")

    # Operations (Level 3)
    network.add_device(ICSDevice("Engineering-WS", "Workstation", 3), "Operations")
    network.add_device(ICSDevice("MES-Server", "Server", 3), "Operations")

    # Control (Level 2)
    network.add_device(ICSDevice("HMI-01", "HMI", 2), "Control")
    network.add_device(ICSDevice("HMI-02", "HMI", 2), "Control")

    # Process (Level 1)
    plc = PLCSimulator("PLC-01")
    network.add_device(plc, "Process")
    network.add_device(ICSDevice("RTU-01", "RTU", 1), "Process")

    # Physical (Level 0)
    network.add_device(ICSDevice("Temp-Sensor", "Sensor", 0), "Physical")
    network.add_device(ICSDevice("Pressure-Sensor", "Sensor", 0), "Physical")
    network.add_device(ICSDevice("Pump-01", "Actuator", 0), "Physical")

    network.show_architecture()
    network.simulate_protocol_traffic("modbus")
    network.simulate_attack("man_in_the_middle")


def demo_segmentation():
    """Demonstrate network segmentation importance."""
    print("\n" + "=" * 60)
    print("NETWORK SEGMENTATION IN ICS")
    print("=" * 60)

    print("""
Without Segmentation (Flat Network):
  [Enterprise] <---> [OT Network] <---> [Internet]
  Risk: Ransomware from email spreads directly to PLCs

With Proper Segmentation:
  [Enterprise] --|FW|--> [DMZ] --|FW|--> [OT Network]
  Risk: Firewall blocks lateral movement, containment possible

Recommended Segmentation:
  - Unidirectional gateways (data diodes) for critical systems
  - VLANs for different process areas
  - Industrial firewalls with protocol-aware inspection
  - No direct internet access to Level 0-2 devices
    """)


def main():
    print("=" * 60)
    print("ICS NETWORK SIMULATOR")
    print("=" * 60)
    print("Learn industrial control network architecture.\n")

    while True:
        print("\nMenu:")
        print("1. Purdue Model Architecture")
        print("2. Network Segmentation Concepts")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_purdue_model()
        elif choice == "2":
            demo_segmentation()
        elif choice == "3":
            demo_purdue_model()
            demo_segmentation()
        elif choice == "4":
            print("Protect critical infrastructure!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
