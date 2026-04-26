#!/usr/bin/env python3
"""
File Permission Analyzer
Educational tool for understanding Unix/Linux file permissions.
"""

import os
import stat


def decode_permission(perm_string):
    """Decode a permission string like 'rwxr-xr--'."""
    if len(perm_string) != 9:
        print("Permission string must be exactly 9 characters (rwxrwxrwx)")
        return

    print(f"\n{'─' * 50}")
    print(f"DECODING: {perm_string}")
    print(f"{'─' * 50}")

    parts = [
        ("Owner (User)", perm_string[0:3]),
        ("Group", perm_string[3:6]),
        ("Others (World)", perm_string[6:9]),
    ]

    for name, p in parts:
        read = "Yes" if p[0] == 'r' else "No"
        write = "Yes" if p[1] == 'w' else "No"
        execute = "Yes" if p[2] == 'x' else "No"

        print(f"\n{name}:")
        print(f"  Read (r):    {read}")
        print(f"  Write (w):   {write}")
        print(f"  Execute (x): {execute}")

    # Numeric equivalent
    numeric = permission_to_numeric(perm_string)
    print(f"\nNumeric Mode: {numeric}")

    # Security assessment
    assess_security(perm_string)


def permission_to_numeric(perm_string):
    """Convert rwxrwxrwx to numeric mode (e.g., 755)."""
    result = 0
    for i in range(3):
        segment = perm_string[i*3:(i+1)*3]
        value = 0
        if segment[0] == 'r':
            value += 4
        if segment[1] == 'w':
            value += 2
        if segment[2] == 'x':
            value += 1
        result = result * 10 + value
    return result


def numeric_to_permission(numeric):
    """Convert numeric mode to rwx string."""
    numeric_str = str(numeric).zfill(3)
    result = ""
    for digit in numeric_str:
        d = int(digit)
        result += 'r' if d & 4 else '-'
        result += 'w' if d & 2 else '-'
        result += 'x' if d & 1 else '-'
    return result


def assess_security(perm_string):
    """Assess the security implications of permissions."""
    print(f"\n{'─' * 50}")
    print("SECURITY ASSESSMENT")
    print(f"{'─' * 50}")

    issues = []
    warnings = []

    owner, group, others = perm_string[0:3], perm_string[3:6], perm_string[6:9]

    # Check world-writable
    if others[1] == 'w':
        issues.append("CRITICAL: File is world-writable. ANY user can modify it!")

    # Check world-executable for sensitive files
    if others[2] == 'x' and owner[2] == 'x':
        warnings.append("File is executable by everyone. Ensure this is intentional.")

    # Check group-writable
    if group[1] == 'w':
        warnings.append("Group has write access. Verify group membership is restricted.")

    # Check no owner read
    if owner[0] != 'r':
        warnings.append("Owner cannot read the file. Is this intentional?")

    # Check SUID/SGID hints (not in basic 9-char string but worth mentioning)
    print("Checks performed:")
    print("  - World writable detection")
    print("  - Overly permissive execution rights")
    print("  - Group write risks")
    print("  - Owner access verification")

    if issues:
        print(f"\nISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"  [CRITICAL] {issue}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  [WARNING] {warning}")

    if not issues and not warnings:
        print("\nNo major security issues detected with these permissions.")

    print("\nRecommendations:")
    print("  - Avoid world-writable files (chmod o-w)")
    print("  - Use least privilege principle")
    print("  - Regularly audit file permissions with 'find / -perm -002'")


def permission_calculator():
    """Interactive permission calculator."""
    print("\n" + "=" * 50)
    print("PERMISSION CALCULATOR")
    print("=" * 50)

    print("\nSelect permissions for each category:")

    def get_permission_set(name):
        print(f"\n{name}:")
        r = input("  Read? (y/n): ").strip().lower() == 'y'
        w = input("  Write? (y/n): ").strip().lower() == 'y'
        x = input("  Execute? (y/n): ").strip().lower() == 'y'
        return ('r' if r else '-') + ('w' if w else '-') + ('x' if x else '-')

    owner = get_permission_set("Owner")
    group = get_permission_set("Group")
    others = get_permission_set("Others")

    perm_string = owner + group + others
    numeric = permission_to_numeric(perm_string)

    print(f"\n{'─' * 50}")
    print(f"RESULT: {perm_string} = {numeric}")
    print(f"{'─' * 50}")

    # Show chmod command
    print(f"\nLinux command:")
    print(f"  chmod {numeric} filename")
    print(f"  chmod {perm_string} filename")

    decode_permission(perm_string)


def analyze_local_file():
    """Analyze a file on the local system (if supported)."""
    filepath = input("\nEnter file path to analyze: ").strip()

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    try:
        file_stat = os.stat(filepath)
        mode = stat.filemode(file_stat.st_mode)

        print(f"\nFile: {filepath}")
        print(f"Permissions: {mode}")
        print(f"Owner UID: {file_stat.st_uid}")
        print(f"Group GID: {file_stat.st_gid}")
        print(f"Size: {file_stat.st_size} bytes")

        # Extract just the rwx part
        perm_only = mode[1:10]
        decode_permission(perm_only)

    except Exception as e:
        print(f"Error analyzing file: {e}")


def main():
    print("=" * 60)
    print("FILE PERMISSION ANALYZER")
    print("=" * 60)
    print("Learn Unix/Linux file permissions through interactive analysis.\n")

    while True:
        print("\nMenu:")
        print("1. Decode Permission String (e.g., rwxr-xr--)")
        print("2. Permission Calculator (build your own)")
        print("3. Analyze Local File (if running on Unix/Linux/Mac)")
        print("4. Quick Reference")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            perm = input("Enter 9-character permission string: ").strip()
            if len(perm) == 9:
                decode_permission(perm)
            else:
                print("Invalid format. Use exactly 9 characters like 'rwxr-xr-x'")
        elif choice == "2":
            permission_calculator()
        elif choice == "3":
            analyze_local_file()
        elif choice == "4":
            print_quick_reference()
        elif choice == "5":
            print("Keep your permissions tight!")
            break
        else:
            print("Invalid choice.")


def print_quick_reference():
    """Print a quick reference guide."""
    print("\n" + "=" * 60)
    print("PERMISSION QUICK REFERENCE")
    print("=" * 60)

    print("\nNumeric Values:")
    print("  4 = Read (r)")
    print("  2 = Write (w)")
    print("  1 = Execute (x)")
    print("  Add values: 7 = rwx, 6 = rw-, 5 = r-x, 4 = r--")

    print("\nCommon Permission Modes:")
    common = [
        ("777", "rwxrwxrwx", "Full access for everyone (DANGEROUS)"),
        ("755", "rwxr-xr-x", "Standard for executables"),
        ("644", "rw-r--r--", "Standard for files (owner rw, others r)"),
        ("600", "rw-------", "Private file (only owner can read/write)"),
        ("700", "rwx------", "Private executable (only owner)"),
        ("750", "rwxr-x---", "Owner full, group read/execute, others none"),
        ("440", "r--r-----", "Read-only for owner and group"),
        ("000", "---------", "No permissions (completely locked)"),
    ]

    for numeric, sym, desc in common:
        print(f"  {numeric} = {sym}  {desc}")

    print("\nSpecial Permission Bits:")
    print("  SUID (4000) - Run as file owner (e.g., /usr/bin/passwd)")
    print("  SGID (2000) - Run as file group, or inherit directory group")
    print("  Sticky (1000) - Only owner can delete files in directory")
    print("  Example: chmod 4755 file (SUID + 755)")

    print("\nUseful Commands:")
    print("  chmod 755 file       - Change permissions")
    print("  chown user:group file - Change owner and group")
    print("  ls -la               - List files with permissions")
    print("  find / -perm -002    - Find world-writable files")


if __name__ == "__main__":
    main()
