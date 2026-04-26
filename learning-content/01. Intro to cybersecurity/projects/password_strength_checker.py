#!/usr/bin/env python3
"""
Password Strength Checker
Analyzes password complexity and provides actionable feedback.
"""

import math
import re


def check_length(password):
    """Check password length."""
    length = len(password)
    if length < 8:
        return 0, "Too short (minimum 8 characters)"
    elif length < 12:
        return 1, "Acceptable length (12+ recommended)"
    elif length < 16:
        return 2, "Good length"
    else:
        return 3, "Excellent length"


def check_character_types(password):
    """Check for different character types."""
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>\[\]\\;/~`_+=\-|]', password))

    types_found = sum([has_lower, has_upper, has_digit, has_special])

    feedback = []
    if not has_lower:
        feedback.append("Add lowercase letters")
    if not has_upper:
        feedback.append("Add uppercase letters")
    if not has_digit:
        feedback.append("Add numbers")
    if not has_special:
        feedback.append("Add special characters (!@#$ etc.)")

    return types_found, feedback


def check_patterns(password):
    """Check for common weak patterns."""
    issues = []
    lower_pwd = password.lower()

    # Common passwords (top 20)
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', 'letmein', 'dragon', '111111', 'baseball',
        'iloveyou', 'trustno1', 'sunshine', 'princess', 'admin',
        'welcome', 'shadow', 'ashley', 'football', 'jesus'
    ]

    if lower_pwd in common_passwords:
        issues.append("This is one of the most commonly used passwords!")

    # Sequential characters
    sequences = ['abcdefghijklmnopqrstuvwxyz', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm', '0123456789']
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lower_pwd:
                issues.append(f"Contains sequential characters: '{seq[i:i+3]}'")
                break

    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        issues.append("Contains repeated characters (e.g., 'aaa', '111')")

    # Keyboard patterns
    keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
    for row in keyboard_rows:
        for i in range(len(row) - 2):
            if row[i:i+3] in lower_pwd:
                issues.append(f"Contains keyboard pattern: '{row[i:i+3]}'")
                break

    # Dates
    if re.search(r'(19|20)\d{2}', password):
        issues.append("Contains a year (common in passwords)")

    return issues


def calculate_entropy(password):
    """Calculate password entropy in bits."""
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset_size += 33

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return entropy


def rate_password(password):
    """Rate password strength from 0-100."""
    if not password:
        return 0, "Empty password"

    score = 0
    feedback = []

    # Length scoring
    length_score, length_msg = check_length(password)
    score += length_score * 10
    if length_score < 2:
        feedback.append(length_msg)

    # Character variety scoring
    types_found, type_feedback = check_character_types(password)
    score += types_found * 10
    feedback.extend(type_feedback)

    # Pattern penalties
    pattern_issues = check_patterns(password)
    for issue in pattern_issues:
        score -= 15
        feedback.append(issue)

    # Entropy bonus
    entropy = calculate_entropy(password)
    if entropy > 80:
        score += 20
    elif entropy > 60:
        score += 10
    elif entropy > 40:
        score += 5
    else:
        feedback.append(f"Low entropy ({entropy:.1f} bits) - too predictable")

    # Length bonus for very long passwords
    if len(password) >= 20:
        score += 10
    elif len(password) >= 16:
        score += 5

    score = max(0, min(100, score))
    return score, entropy, feedback


def get_strength_label(score):
    """Convert score to strength label."""
    if score >= 90:
        return "VERY STRONG", "green"
    elif score >= 70:
        return "STRONG", "light_green"
    elif score >= 50:
        return "MODERATE", "yellow"
    elif score >= 30:
        return "WEAK", "orange"
    else:
        return "VERY WEAK", "red"


def print_meter(score):
    """Print a visual strength meter."""
    filled = int(score / 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    print(f"[{bar}] {score}/100")


def generate_suggestion(feedback):
    """Generate improvement suggestions."""
    if not feedback:
        return "Great job! Your password is strong."

    print("\nSuggestions for improvement:")
    for i, item in enumerate(feedback, 1):
        print(f"  {i}. {item}")

    print("\nTip: Use a passphrase of 4-5 random words with numbers")
    print("and symbols mixed in (e.g., 'Correct-Horse-42-Battery!')")


def main():
    print("=" * 60)
    print("PASSWORD STRENGTH CHECKER")
    print("=" * 60)
    print("This tool analyzes password complexity and estimates cracking time.\n")

    while True:
        password = input("Enter a password to analyze (or 'quit' to exit): ")

        if password.lower() == 'quit':
            print("Stay secure! Use unique, strong passwords for every account.")
            break

        score, entropy, feedback = rate_password(password)
        label, _ = get_strength_label(score)

        print(f"\n{'=' * 60}")
        print(f"ANALYSIS RESULT")
        print(f"{'=' * 60}")
        print(f"Length:           {len(password)} characters")
        print(f"Entropy:          {entropy:.1f} bits")
        print(f"Strength Score:   {score}/100")
        print(f"Rating:           {label}")
        print(f"\nStrength Meter:")
        print_meter(score)

        # Estimate crack time (rough approximation for online brute force)
        if entropy > 0:
            seconds = 2 ** entropy / 1e9  # Assume 1 billion guesses/second
            if seconds < 1:
                time_str = "Instantly"
            elif seconds < 60:
                time_str = f"{seconds:.1f} seconds"
            elif seconds < 3600:
                time_str = f"{seconds/60:.1f} minutes"
            elif seconds < 86400:
                time_str = f"{seconds/3600:.1f} hours"
            elif seconds < 31536000:
                time_str = f"{seconds/86400:.1f} days"
            elif seconds < 3153600000:
                time_str = f"{seconds/31536000:.1f} years"
            else:
                time_str = "Centuries"
            print(f"Est. Crack Time:  {time_str}")

        generate_suggestion(feedback)
        print()


if __name__ == "__main__":
    main()
