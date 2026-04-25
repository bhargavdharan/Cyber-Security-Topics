#!/usr/bin/env python3
"""
App Permission Analyzer
Simulates analyzing mobile app permissions for privacy risks.
"""

import random


# Common mobile permissions and their risk levels
PERMISSION_CATALOG = {
    "android.permission.CAMERA": {"name": "Camera", "risk": "HIGH", "purpose": "Take photos/videos"},
    "android.permission.RECORD_AUDIO": {"name": "Microphone", "risk": "HIGH", "purpose": "Record audio"},
    "android.permission.ACCESS_FINE_LOCATION": {"name": "Precise Location", "risk": "HIGH", "purpose": "GPS tracking"},
    "android.permission.READ_CONTACTS": {"name": "Contacts", "risk": "HIGH", "purpose": "Access contact list"},
    "android.permission.READ_SMS": {"name": "SMS", "risk": "HIGH", "purpose": "Read text messages"},
    "android.permission.CALL_PHONE": {"name": "Phone Calls", "risk": "MEDIUM", "purpose": "Make phone calls"},
    "android.permission.READ_EXTERNAL_STORAGE": {"name": "Storage Read", "risk": "MEDIUM", "purpose": "Read files"},
    "android.permission.INTERNET": {"name": "Internet", "risk": "LOW", "purpose": "Network access"},
    "android.permission.ACCESS_NETWORK_STATE": {"name": "Network State", "risk": "LOW", "purpose": "Check connectivity"},
    "android.permission.VIBRATE": {"name": "Vibration", "risk": "LOW", "purpose": "Vibrate device"},
    "android.permission.FOREGROUND_SERVICE": {"name": "Foreground Service", "risk": "MEDIUM", "purpose": "Run background tasks"},
    "android.permission.SYSTEM_ALERT_WINDOW": {"name": "Draw Over Apps", "risk": "HIGH", "purpose": "Display over other apps"},
    "android.permission.BIND_ACCESSIBILITY_SERVICE": {"name": "Accessibility", "risk": "CRITICAL", "purpose": "Control device"},
    "android.permission.REQUEST_INSTALL_PACKAGES": {"name": "Install Apps", "risk": "HIGH", "purpose": "Install other apps"},
}


class MobileApp:
    """Simulates a mobile application."""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.permissions = []
        self._assign_permissions()

    def _assign_permissions(self):
        """Assign realistic permissions based on app category."""
        category_permissions = {
            "Game": ["INTERNET", "ACCESS_NETWORK_STATE", "VIBRATE"],
            "Camera": ["CAMERA", "RECORD_AUDIO", "INTERNET", "READ_EXTERNAL_STORAGE"],
            "Social": ["INTERNET", "CAMERA", "RECORD_AUDIO", "ACCESS_FINE_LOCATION", "READ_CONTACTS", "READ_EXTERNAL_STORAGE"],
            "Calculator": ["INTERNET"],
            "Flashlight": ["CAMERA", "INTERNET"],  # Camera permission for flashlight is suspicious
            "Banking": ["INTERNET", "ACCESS_NETWORK_STATE", "CAMERA", "FINGERPRINT"],
            "Weather": ["INTERNET", "ACCESS_FINE_LOCATION", "ACCESS_NETWORK_STATE"],
        }

        base = category_permissions.get(self.category, ["INTERNET"])

        # Add some random permissions
        all_perms = list(PERMISSION_CATALOG.keys())
        self.permissions = [p for p in all_perms if any(b in p for b in base)]

        # Sometimes add suspicious permissions
        if random.random() < 0.3:
            suspicious = ["SYSTEM_ALERT_WINDOW", "BIND_ACCESSIBILITY_SERVICE", "REQUEST_INSTALL_PACKAGES"]
            self.permissions.extend([p for p in all_perms if any(s in p for s in suspicious)])


class PermissionAnalyzer:
    """Analyzes app permissions for risks."""

    def __init__(self):
        self.apps = []

    def add_app(self, app):
        self.apps.append(app)

    def analyze_app(self, app):
        """Analyze a single app's permissions."""
        print(f"\n{'─' * 60}")
        print(f"Analyzing: {app.name} ({app.category})")
        print(f"{'─' * 60}")

        risk_score = 0
        high_risk_perms = []

        for perm in app.permissions:
            info = PERMISSION_CATALOG.get(perm, {"name": perm, "risk": "UNKNOWN", "purpose": "Unknown"})
            marker = ""
            if info["risk"] in ["HIGH", "CRITICAL"]:
                marker = " [!]"
                risk_score += 3 if info["risk"] == "CRITICAL" else 2
                high_risk_perms.append(info)
            elif info["risk"] == "MEDIUM":
                marker = " [?]"
                risk_score += 1

            print(f"  {info['name']:<20} {info['risk']:<10} {info['purpose']}{marker}")

        # Score interpretation
        print(f"\n  Risk Score: {risk_score}/20")
        if risk_score >= 8:
            print(f"  Assessment: HIGH RISK - Review permissions carefully")
        elif risk_score >= 4:
            print(f"  Assessment: MEDIUM RISK - Some permissions may be unnecessary")
        else:
            print(f"  Assessment: LOW RISK - Permissions appear reasonable")

        # Check for unnecessary permissions
        unnecessary = self._check_unnecessary_permissions(app)
        if unnecessary:
            print(f"\n  Potentially unnecessary permissions for {app.category} app:")
            for perm in unnecessary:
                print(f"    - {perm['name']}: {perm['purpose']}")

        return risk_score

    def _check_unnecessary_permissions(self, app):
        """Check for permissions that don't match the app category."""
        unnecessary = []

        category_expectations = {
            "Game": ["INTERNET", "NETWORK_STATE", "VIBRATE"],
            "Calculator": ["INTERNET"],
            "Flashlight": [],  # Should not need internet or contacts
            "Weather": ["INTERNET", "LOCATION", "NETWORK_STATE"],
        }

        expected = category_expectations.get(app.category, [])

        for perm in app.permissions:
            info = PERMISSION_CATALOG.get(perm)
            if not info:
                continue
            # If permission is high risk and not expected for category
            if info["risk"] in ["HIGH", "CRITICAL"] and not any(e in perm for e in expected):
                unnecessary.append(info)

        return unnecessary

    def compare_privacy(self):
        """Compare privacy ratings of all apps."""
        print("\n" + "=" * 60)
        print("PRIVACY COMPARISON")
        print("=" * 60)

        results = []
        for app in self.apps:
            score = sum(
                3 if PERMISSION_CATALOG.get(p, {}).get("risk") == "CRITICAL" else
                2 if PERMISSION_CATALOG.get(p, {}).get("risk") == "HIGH" else
                1 if PERMISSION_CATALOG.get(p, {}).get("risk") == "MEDIUM" else 0
                for p in app.permissions
            )
            results.append((app, score))

        results.sort(key=lambda x: x[1])

        print(f"\n{'App':<25} {'Category':<15} {'Risk Score':<12} {'Rating'}")
        print("─" * 60)
        for app, score in results:
            if score >= 8:
                rating = "DANGEROUS"
            elif score >= 4:
                rating = "CAUTION"
            else:
                rating = "SAFE"
            print(f"{app.name:<25} {app.category:<15} {score:<12} {rating}")


def demo_permission_analysis():
    """Run permission analysis demo."""
    print("\n" + "=" * 60)
    print("MOBILE APP PERMISSION ANALYSIS")
    print("=" * 60)

    analyzer = PermissionAnalyzer()

    apps = [
        MobileApp("SuperFlashlight", "Flashlight"),
        MobileApp("PixelGame", "Game"),
        MobileApp("SocialConnect", "Social"),
        MobileApp("BasicCalculator", "Calculator"),
        MobileApp("WeatherNow", "Weather"),
    ]

    for app in apps:
        analyzer.add_app(app)
        analyzer.analyze_app(app)

    analyzer.compare_privacy()


def demo_permission_abuse():
    """Demonstrate how permissions can be abused."""
    print("\n" + "=" * 60)
    print("PERMISSION ABUSE SCENARIOS")
    print("=" * 60)

    scenarios = [
        {
            "permission": "Accessibility Service",
            "normal_use": "Help users with disabilities interact with apps",
            "malicious_use": "Keylogger, click other apps, steal 2FA codes, install apps silently",
            "severity": "CRITICAL",
        },
        {
            "permission": "Draw Over Apps",
            "normal_use": "Floating chat heads, screen filters",
            "malicious_use": "Click jacking, fake login overlays, block uninstall screens",
            "severity": "HIGH",
        },
        {
            "permission": "Camera",
            "normal_use": "Take photos, video chat",
            "malicious_use": "Spy on user, record surroundings, capture QR codes",
            "severity": "HIGH",
        },
        {
            "permission": "Location",
            "normal_use": "Maps, local weather, find nearby stores",
            "malicious_use": "Track user movements, stalking, sell location data",
            "severity": "HIGH",
        },
    ]

    for scenario in scenarios:
        print(f"\n[{scenario['severity']}] {scenario['permission']}")
        print(f"  Normal use:    {scenario['normal_use']}")
        print(f"  Malicious use: {scenario['malicious_use']}")

    print("\nPROTECTION TIPS:")
    print("  - Only install apps from official stores")
    print("  - Review permissions before installing")
    print("  - Deny permissions that don't match app functionality")
    print("  - Regularly audit installed app permissions")
    print("  - Remove unused apps")


def main():
    print("=" * 60)
    print("APP PERMISSION ANALYZER")
    print("=" * 60)
    print("Learn to identify risky mobile app permissions.\n")

    while True:
        print("\nMenu:")
        print("1. Permission Analysis Demo")
        print("2. Permission Abuse Scenarios")
        print("3. Run All Demos")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            demo_permission_analysis()
        elif choice == "2":
            demo_permission_abuse()
        elif choice == "3":
            demo_permission_analysis()
            demo_permission_abuse()
        elif choice == "4":
            print("Protect your privacy!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
