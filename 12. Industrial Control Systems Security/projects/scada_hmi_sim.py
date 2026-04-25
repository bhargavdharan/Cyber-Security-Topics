#!/usr/bin/env python3
"""
SCADA HMI Simulator
Simulates a SCADA Human-Machine Interface with security features.
"""

import random
import time


class SCADAProcess:
    """Simulates an industrial process."""

    def __init__(self):
        self.temperature = 150.0  # Celsius
        self.pressure = 50.0     # PSI
        self.flow_rate = 100.0   # L/min
        self.pump_status = True
        self.valve_position = 75  # Percent open
        self.alarms = []

    def update(self):
        """Update process values with realistic variations."""
        self.temperature += random.uniform(-2, 2)
        self.pressure += random.uniform(-1, 1)
        self.flow_rate += random.uniform(-3, 3)

        # Check alarm conditions
        self.alarms = []
        if self.temperature > 180:
            self.alarms.append(("CRITICAL", "High Temperature", self.temperature))
        elif self.temperature > 160:
            self.alarms.append(("WARNING", "Elevated Temperature", self.temperature))

        if self.pressure > 70:
            self.alarms.append(("CRITICAL", "High Pressure", self.pressure))
        elif self.pressure > 60:
            self.alarms.append(("WARNING", "Elevated Pressure", self.pressure))

        if self.flow_rate < 50:
            self.alarms.append(("WARNING", "Low Flow Rate", self.flow_rate))

    def set_pump(self, status):
        self.pump_status = status

    def set_valve(self, position):
        self.valve_position = max(0, min(100, position))


class SCADAHMI:
    """Simulates a SCADA HMI with security logging."""

    def __init__(self):
        self.process = SCADAProcess()
        self.operator_log = []
        self.authenticated = False
        self.current_user = None
        self.command_whitelist = ["READ", "PUMP_ON", "PUMP_OFF", "VALVE_ADJUST"]

    def authenticate(self, username, password):
        """Simulate operator authentication."""
        # In real systems, this uses proper authentication
        if password == "admin123":  # Intentionally weak for demo
            print("[!] WEAK PASSWORD DETECTED - Security policy violation")

        self.authenticated = True
        self.current_user = username
        print(f"Operator '{username}' authenticated")
        self._log_action("LOGIN", f"User {username} logged in")
        return True

    def display_process(self):
        """Display current process values."""
        print(f"\n{'=' * 50}")
        print(f"PROCESS OVERVIEW")
        print(f"{'=' * 50}")
        print(f"Temperature:    {self.process.temperature:.1f} C")
        print(f"Pressure:       {self.process.pressure:.1f} PSI")
        print(f"Flow Rate:      {self.process.flow_rate:.1f} L/min")
        print(f"Pump Status:    {'RUNNING' if self.process.pump_status else 'STOPPED'}")
        print(f"Valve Position: {self.process.valve_position}%")

        if self.process.alarms:
            print(f"\n[!] ACTIVE ALARMS:")
            for severity, name, value in self.process.alarms:
                print(f"  [{severity}] {name}: {value:.1f}")
        else:
            print(f"\n[OK] No active alarms")

    def send_command(self, command, value=None):
        """Send control command with validation."""
        if not self.authenticated:
            print("ERROR: Authentication required")
            self._log_action("COMMAND_REJECTED", "Unauthenticated command attempt")
            return False

        # Validate command
        if command not in self.command_whitelist:
            print(f"[!] SECURITY ALERT: Unauthorized command '{command}'")
            self._log_action("SECURITY_ALERT", f"Unauthorized command: {command}")
            return False

        # Execute command
        if command == "PUMP_ON":
            self.process.set_pump(True)
            print("Command executed: Pump STARTED")
        elif command == "PUMP_OFF":
            self.process.set_pump(False)
            print("Command executed: Pump STOPPED")
        elif command == "VALVE_ADJUST" and value is not None:
            old_pos = self.process.valve_position
            self.process.set_valve(value)
            print(f"Command executed: Valve adjusted from {old_pos}% to {value}%")

        self._log_action("COMMAND", f"{command} by {self.current_user}")
        return True

    def _log_action(self, action_type, description):
        """Log operator actions."""
        self.operator_log.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": action_type,
            "description": description,
            "user": self.current_user,
        })

    def show_audit_log(self):
        """Display operator audit log."""
        print(f"\n{'=' * 50}")
        print(f"OPERATOR AUDIT LOG")
        print(f"{'=' * 50}")
        for entry in self.operator_log:
            print(f"{entry['timestamp']} [{entry['type']:<15}] {entry['description']}")


def demo_scada_operation():
    """Demonstrate SCADA operations with security."""
    print("\n" + "=" * 60)
    print("SCADA HMI OPERATIONS")
    print("=" * 60)

    hmi = SCADAHMI()

    # Try unauthorized command
    print("\n--- Attempting unauthenticated command ---")
    hmi.send_command("PUMP_OFF")

    # Authenticate
    print("\n--- Operator Authentication ---")
    hmi.authenticate("operator_john", "op123")

    # Normal operations
    print("\n--- Normal Operations ---")
    hmi.display_process()
    hmi.send_command("VALVE_ADJUST", 80)

    # Simulate process changes
    for _ in range(3):
        hmi.process.update()
        hmi.display_process()
        time.sleep(0.5)

    # Attempt unauthorized command
    print("\n--- Security Test: Unauthorized Command ---")
    hmi.send_command("DELETE_DATABASE")

    # Show audit log
    hmi.show_audit_log()


def demo_safety_systems():
    """Demonstrate safety instrumented systems."""
    print("\n" + "=" * 60)
    print("SAFETY INSTRUMENTED SYSTEMS (SIS)")
    print("=" * 60)

    print("""
Safety Systems operate independently of the control system:

  BPCS (Basic Process Control):
    - Normal operation control
    - Human operator oversight
    - Can be compromised by cyber attacks

  SIS (Safety Instrumented System):
    - Independent safety functions
    - Hardwired safety interlocks
    - NOT accessible from control network
    - Triggers on dangerous conditions

Example Safety Function:
  IF Pressure > 100 PSI THEN
    Open Relief Valve
    Shutdown Pump
    Alert Operator
  END IF

Security Considerations:
  - SIS should be physically separate from BPCS
  - No network connection between SIS and corporate network
  - Safety functions must work even if control system is compromised
  - Triton malware targeted SIS (2017) - extremely dangerous
    """)


def main():
    print("=" * 60)
    print("SCADA HMI SIMULATOR")
    print("=" * 60)
    print("Learn SCADA operations and security concepts.\n")

    while True:
        print("\nMenu:")
        print("1. SCADA Operations Demo")
        print("2. Safety Systems Concepts")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_scada_operation()
        elif choice == "2":
            demo_safety_systems()
        elif choice == "3":
            demo_scada_operation()
            demo_safety_systems()
        elif choice == "4":
            print("Safety first!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
