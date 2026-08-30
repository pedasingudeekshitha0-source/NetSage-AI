"""
NetSage AI
AI-Assisted Network Troubleshooting Interface

This module combines deterministic network validation
with an explainable troubleshooting response.
"""

from checker import NetworkChecker, calculate_confidence


def generate_explanation(findings):
    if not findings:
        return "No network issue was identified."

    explanations = []

    for finding in findings:
        severity = finding["severity"]
        category = finding["category"]
        problem = finding["message"]
        action = finding["suggestion"]

        explanation = (
            f"{severity} - {category}\n"
            f"Finding: {problem}\n"
            f"Recommended action: {action}\n"
        )

        explanations.append(explanation)

    return "\n".join(explanations)


def main():
    print("=" * 65)
    print("                 NETSAGE AI")
    print("       AI-ASSISTED NETWORK TROUBLESHOOTING")
    print("=" * 65)

    evidence = input("\nEnter network symptom/evidence:\n> ")

    checker = NetworkChecker(evidence)
    findings = checker.run_checks()

    confidence = calculate_confidence(findings)

    print("\nAI-Assisted Analysis")
    print("-" * 65)
    print(generate_explanation(findings))
    print(f"Confidence: {confidence:.0%}")

    print("\nHuman Review Required")
    print("Verify the diagnosis using actual network evidence")
    print("before making configuration changes.")


if __name__ == "__main__":
    main()
