#!/usr/bin/env python3
"""
Social Engineering Awareness Quiz
Test your ability to recognize common social engineering tactics.
"""

import random

QUESTIONS = [
    {
        "scenario": (
            "You receive an email from 'support@amaz0n-security.com' stating your account "
            "has been compromised and you must click a link immediately to verify your identity."
        ),
        "type": "Phishing",
        "options": [
            "A. Click the link and enter your credentials to secure your account",
            "B. Check the sender's email domain carefully and report it as phishing",
            "C. Forward the email to friends to warn them",
            "D. Reply to the email asking if it's legitimate"
        ],
        "correct": "B",
        "explanation": (
            "The domain 'amaz0n-security.com' is a lookalike domain (note the zero instead of 'o'). "
            "Legitimate companies will never ask you to click links in emails to verify accounts. "
            "Always check sender domains carefully and report suspicious emails."
        )
    },
    {
        "scenario": (
            "A person wearing a technician uniform shows up at your office door holding a clipboard. "
            "They say they're from 'IT Support' and need to check the server room immediately due to "
            'an urgent network issue. They ask you to hold the door open for them.'
        ),
        "type": "Pretexting / Tailgating",
        "options": [
            "A. Hold the door open - they're in a uniform and seem official",
            "B. Ask to see their company ID badge and verify with IT department",
            "C. Let them in but watch what they do",
            "D. Ask them to wait outside while you find your manager"
        ],
        "correct": "B",
        "explanation": (
            "This is a classic tailgating/pretexting attack. The uniform creates a false sense of legitimacy. "
            "Always verify unknown visitors' identities through proper channels before granting access to secure areas."
        )
    },
    {
        "scenario": (
            "You find a USB drive labeled 'Q4 Salary Reports - Confidential' in the parking lot. "
            "You're curious about the contents and wonder if it belongs to someone in your department."
        ),
        "type": "Baiting",
        "options": [
            "A. Plug it into your work computer to see if you can identify the owner",
            "B. Hand it to IT security without plugging it in",
            "C. Plug it into your personal laptop (safer than work computer)",
            "D. Leave it where you found it"
        ],
        "correct": "B",
        "explanation": (
            "This is a baiting attack. Malicious USB drives can contain malware that executes automatically "
            "(USB drops). Never plug in unknown USB devices. Hand them to your security/IT team for safe analysis."
        )
    },
    {
        "scenario": (
            "You receive a phone call from someone claiming to be from your bank's fraud department. "
            "They know your full name and last 4 digits of your credit card. They ask you to confirm "
            "your full card number and CVV to 'verify your identity' and reverse suspicious charges."
        ),
        "type": "Vishing (Voice Phishing)",
        "options": [
            "A. Provide the information since they already know some of your details",
            "B. Hang up and call your bank using the number on your card",
            "C. Ask them to send you an email with their credentials",
            "D. Give them partial information to see if they accept it"
        ],
        "correct": "B",
        "explanation": (
            "Never provide sensitive information to incoming callers, even if they seem legitimate. "
            "Fraudsters can obtain partial information from data breaches. Always hang up and call "
            "the institution directly using a verified phone number."
        )
    },
    {
        "scenario": (
            "A new colleague you just met on LinkedIn sends you a direct message with a link: "
            "'Check out this hilarious video of our CEO at the company retreat!' The link uses a URL shortener."
        ),
        "type": "Social Media Phishing",
        "options": [
            "A. Click the link - it sounds funny and they're a colleague",
            "B. Ignore the message and report it as suspicious",
            "C. Ask them to send the full URL before clicking",
            "D. Forward it to your team chat so everyone can see"
        ],
        "correct": "B",
        "explanation": (
            "Attackers create fake LinkedIn profiles to build trust and then distribute malicious links. "
            "URL shorteners hide the true destination. Never click suspicious links, even from apparent colleagues."
        )
    },
    {
        "scenario": (
            "You receive an urgent text message: 'Your package delivery failed. Click here to reschedule "
            "delivery and pay the $2.99 redelivery fee: http://bit.ly/xyz123'"
        ),
        "type": "Smishing (SMS Phishing)",
        "options": [
            "A. Click the link and pay the small fee to get your package",
            "B. Check your email for legitimate tracking information from the carrier",
            "C. Reply STOP to the message",
            "D. Call the number that sent the text"
        ],
        "correct": "B",
        "explanation": (
            "Smishing attacks use urgent language and small fees to trick victims into clicking malicious links. "
            "Always verify delivery issues through the official carrier website or app using your tracking number."
        )
    },
    {
        "scenario": (
            "An email from your 'CEO' arrives with the subject 'URGENT: Wire Transfer Needed'. "
            "It asks you to immediately process a $50,000 wire transfer to a vendor for a confidential "
            "acquisition. The CEO says they're in a meeting and can't be disturbed."
        ),
        "type": "Business Email Compromise (BEC)",
        "options": [
            "A. Process the transfer quickly since it's from the CEO and marked urgent",
            "B. Verify the request via a separate communication channel (phone, in-person)",
            "C. Reply to the email asking for more details",
            "D. Forward it to accounting to handle"
        ],
        "correct": "B",
        "explanation": (
            "BEC attacks spoof executive emails to trick employees into transferring funds. "
            "Always verify unusual financial requests through a separate, trusted communication channel. "
            "Never use reply-to addresses for verification."
        )
    },
]


def run_quiz():
    print("=" * 70)
    print("SOCIAL ENGINEERING AWARENESS QUIZ")
    print("=" * 70)
    print("Test your ability to recognize common social engineering tactics.\n")
    print("Instructions: Read each scenario and choose the BEST response.\n")

    # Shuffle questions
    questions = random.sample(QUESTIONS, len(QUESTIONS))
    score = 0

    for i, q in enumerate(questions, 1):
        print(f"\n{'─' * 70}")
        print(f"QUESTION {i} of {len(questions)} | Type: {q['type']}")
        print(f"{'─' * 70}")
        print(f"Scenario: {q['scenario']}\n")

        for option in q['options']:
            print(f"  {option}")

        answer = input("\nYour answer (A/B/C/D): ").strip().upper()

        while answer not in ['A', 'B', 'C', 'D']:
            answer = input("Please enter A, B, C, or D: ").strip().upper()

        if answer == q['correct']:
            print("\n CORRECT!")
            score += 1
        else:
            print(f"\n INCORRECT. The correct answer was {q['correct']}.")

        print(f"\nExplanation: {q['explanation']}")
        input("\nPress Enter to continue...")

    # Final score
    print(f"\n{'=' * 70}")
    print(f"QUIZ COMPLETE!")
    print(f"{'=' * 70}")
    print(f"Your Score: {score}/{len(questions)} ({score/len(questions)*100:.0f}%)")

    if score == len(questions):
        print("Perfect score! You're well-prepared to spot social engineering attacks!")
    elif score >= len(questions) * 0.8:
        print("Great job! You have strong awareness of social engineering tactics.")
    elif score >= len(questions) * 0.6:
        print("Good effort, but there's room for improvement. Review the explanations above.")
    else:
        print("Keep learning! Social engineering is a major threat vector. Study the scenarios carefully.")

    print("\nKey Takeaways:")
    print("  - Always verify unexpected requests through separate channels")
    print("  - Check sender domains, URLs, and phone numbers carefully")
    print("  - Be suspicious of urgency, fear, and curiosity triggers")
    print("  - Never plug in unknown USB devices or click suspicious links")


if __name__ == "__main__":
    run_quiz()
