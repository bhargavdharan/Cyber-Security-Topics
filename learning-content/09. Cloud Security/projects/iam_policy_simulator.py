#!/usr/bin/env python3
"""
IAM Policy Simulator
Simulates cloud IAM policy evaluation for learning access control concepts.
"""

import json


class IAMSimulator:
    """Simulates AWS-style IAM policy evaluation."""

    def __init__(self):
        self.users = {}
        self.groups = {}
        self.policies = {}

    def create_user(self, username, groups=None):
        """Create a user and optionally add to groups."""
        self.users[username] = {
            "groups": groups or [],
            "attached_policies": [],
        }
        print(f"Created user: {username}")

    def create_group(self, group_name, policies=None):
        """Create a group with policies."""
        self.groups[group_name] = {
            "policies": policies or [],
        }
        print(f"Created group: {group_name}")

    def create_policy(self, name, statements):
        """Create an IAM policy."""
        self.policies[name] = {"Version": "2012-10-17", "Statement": statements}
        print(f"Created policy: {name}")

    def attach_user_policy(self, username, policy_name):
        """Attach a policy directly to a user."""
        if username in self.users:
            self.users[username]["attached_policies"].append(policy_name)
            print(f"Attached {policy_name} to user {username}")

    def evaluate_access(self, username, action, resource):
        """Evaluate whether a user can perform an action on a resource."""
        print(f"\n{'─' * 60}")
        print(f"EVALUATING: Can '{username}' perform '{action}' on '{resource}'?")
        print(f"{'─' * 60}")

        # Collect all applicable policies
        applicable_policies = []

        # User-attached policies
        if username in self.users:
            for policy_name in self.users[username]["attached_policies"]:
                if policy_name in self.policies:
                    applicable_policies.append(("user", policy_name, self.policies[policy_name]))

            # Group policies
            for group_name in self.users[username]["groups"]:
                if group_name in self.groups:
                    for policy_name in self.groups[group_name]["policies"]:
                        if policy_name in self.policies:
                            applicable_policies.append(("group", policy_name, self.policies[policy_name]))

        if not applicable_policies:
            print("No policies found. Default: DENY")
            return False

        # Evaluate policies
        explicit_deny = False
        explicit_allow = False

        for source, policy_name, policy in applicable_policies:
            for statement in policy.get("Statement", []):
                effect = statement.get("Effect", "Deny")
                actions = statement.get("Action", [])
                resources = statement.get("Resource", [])

                # Check if action matches
                action_match = False
                for pattern in actions:
                    if pattern == "*" or pattern == action:
                        action_match = True
                        break
                    if pattern.endswith("*") and action.startswith(pattern[:-1]):
                        action_match = True
                        break

                # Check if resource matches
                resource_match = False
                for pattern in resources:
                    if pattern == "*" or pattern == resource:
                        resource_match = True
                        break

                if action_match and resource_match:
                    print(f"  [{effect}] from {source} policy '{policy_name}'")
                    if effect == "Deny":
                        explicit_deny = True
                    elif effect == "Allow":
                        explicit_allow = True

        # Decision logic: explicit deny overrides allow
        if explicit_deny:
            print(f"\nDecision: DENY (explicit deny found)")
            return False
        elif explicit_allow:
            print(f"\nDecision: ALLOW")
            return True
        else:
            print(f"\nDecision: DENY (no explicit allow found)")
            return False


def demo_basic_policies():
    """Demonstrate basic IAM policy evaluation."""
    print("\n" + "=" * 60)
    print("IAM POLICY EVALUATION DEMO")
    print("=" * 60)

    iam = IAMSimulator()

    # Create policies
    iam.create_policy("S3ReadOnly", [
        {"Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"], "Resource": "*"}
    ])

    iam.create_policy("S3FullAccess", [
        {"Effect": "Allow", "Action": ["s3:*"], "Resource": "*"}
    ])

    iam.create_policy("DenySensitiveBuckets", [
        {"Effect": "Deny", "Action": ["s3:*"], "Resource": "arn:aws:s3:::finance-*"}
    ])

    # Create groups
    iam.create_group("Developers", ["S3ReadOnly"])
    iam.create_group("Admins", ["S3FullAccess"])

    # Create users
    iam.create_user("alice", ["Developers"])
    iam.create_user("bob", ["Admins"])
    iam.create_user("charlie", ["Developers"])
    iam.attach_user_policy("charlie", "DenySensitiveBuckets")

    # Test scenarios
    scenarios = [
        ("alice", "s3:GetObject", "arn:aws:s3:::public-bucket/file.txt"),
        ("alice", "s3:DeleteObject", "arn:aws:s3:::public-bucket/file.txt"),
        ("bob", "s3:DeleteObject", "arn:aws:s3:::public-bucket/file.txt"),
        ("charlie", "s3:GetObject", "arn:aws:s3:::public-bucket/file.txt"),
        ("charlie", "s3:GetObject", "arn:aws:s3:::finance-reports/q1.csv"),
    ]

    for user, action, resource in scenarios:
        iam.evaluate_access(user, action, resource)
        input("\nPress Enter for next scenario...")


def demo_least_privilege():
    """Demonstrate least privilege principle."""
    print("\n" + "=" * 60)
    print("LEAST PRIVILEGE PRINCIPLE")
    print("=" * 60)

    iam = IAMSimulator()

    # Overly permissive policy
    iam.create_policy("AdminAccess", [
        {"Effect": "Allow", "Action": ["*"], "Resource": ["*"]}
    ])

    # Least privilege policy
    iam.create_policy("WebAppLimited", [
        {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": "arn:aws:s3:::webapp-bucket/*"},
        {"Effect": "Allow", "Action": ["dynamodb:GetItem", "dynamodb:Query"], "Resource": "arn:aws:dynamodb:::table/Users"},
    ])

    print("\n--- Overly Permissive Policy ---")
    print("Grants ALL actions on ALL resources")
    print("Risk: If compromised, attacker has full cloud access")

    print("\n--- Least Privilege Policy ---")
    print("Grants ONLY required actions on specific resources")
    print("Risk: Limited blast radius if compromised")

    print("\nBEST PRACTICES:")
    print("  1. Start with zero permissions")
    print("  2. Add only required permissions")
    print("  3. Use resource-level restrictions")
    print("  4. Regularly audit and remove unused permissions")
    print("  5. Use IAM Access Analyzer to find unintended access")


def interactive_policy_builder():
    """Let users build and test their own policies."""
    print("\n" + "=" * 60)
    print("INTERACTIVE POLICY BUILDER")
    print("=" * 60)

    iam = IAMSimulator()

    print("\nCreate a policy (JSON format, simplified):")
    print("Example: [{\"Effect\": \"Allow\", \"Action\": [\"s3:GetObject\"], \"Resource\": [\"*\"]}]")

    policy_input = input("Policy statements: ").strip()
    if not policy_input:
        policy_input = '[{"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["*"]}]'

    try:
        statements = json.loads(policy_input)
        iam.create_policy("CustomPolicy", statements)
    except json.JSONDecodeError:
        print("Invalid JSON. Using default policy.")
        iam.create_policy("CustomPolicy", [
            {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["*"]}
        ])

    iam.create_user("testuser")
    iam.attach_user_policy("testuser", "CustomPolicy")

    print("\nTest the policy:")
    while True:
        action = input("Action (or 'quit'): ").strip()
        if action.lower() == 'quit':
            break
        resource = input("Resource: ").strip() or "*"
        iam.evaluate_access("testuser", action, resource)


def main():
    print("=" * 60)
    print("IAM POLICY SIMULATOR")
    print("=" * 60)
    print("Learn cloud access control through interactive policy evaluation.\n")

    while True:
        print("\nMenu:")
        print("1. Basic Policy Evaluation")
        print("2. Least Privilege Principle")
        print("3. Interactive Policy Builder")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            demo_basic_policies()
        elif choice == "2":
            demo_least_privilege()
        elif choice == "3":
            interactive_policy_builder()
        elif choice == "4":
            demo_basic_policies()
            demo_least_privilege()
        elif choice == "5":
            print("Grant least privilege!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
