"""
NetSage AI
Evidence-Driven Cisco Network Troubleshooting Assistant

Deterministic validation engine for common network configuration issues.
This tool complements AI diagnosis with rule-based checks.
"""

import re
import json
import argparse
from datetime import datetime


class NetworkChecker:
    def __init__(self, evidence):
        self.evidence = evidence.lower()
        self.findings = []

    def add_finding(self, severity, category, message, suggestion):
        self.findings.append({
            "severity": severity,
            "category": category,
            "message": message,
            "suggestion": suggestion
        })

    def check_interfaces(self):
        if "administratively down" in self.evidence:
            self.add_finding(
                "HIGH",
                "Interface",
                "One or more interfaces are administratively down.",
                "Run 'show ip interface brief' and enable the affected interface."
            )

        elif "down/down" in self.evidence:
            self.add_finding(
                "HIGH",
                "Interface",
                "An interface appears to be down.",
                "Check cable connection, interface status and 'show interfaces'."
            )

    def check_vlan(self):
        if "vlan" not in self.evidence:
            return

        if "missing vlan" in self.evidence or "vlan does not exist" in self.evidence:
            self.add_finding(
                "HIGH",
                "VLAN",
                "A required VLAN appears to be missing.",
                "Run 'show vlan brief' and create/configure the required VLAN."
            )

        if "not allowed" in self.evidence and "trunk" in self.evidence:
            self.add_finding(
                "HIGH",
                "Trunk",
                "A VLAN may be missing from the trunk allowed list.",
                "Run 'show interfaces trunk' and verify the allowed VLAN list."
            )

    def check_gateway(self):
        gateway_pattern = r"default gateway.*(?:unknown|not set)"
        if re.search(gateway_pattern, self.evidence):
            self.add_finding(
                "HIGH",
                "Gateway",
                "Default gateway information is missing.",
                "Verify the host default gateway and VLAN gateway configuration."
            )

        if "wrong gateway" in self.evidence:
            self.add_finding(
                "HIGH",
                "Gateway",
                "The configured default gateway may be incorrect.",
                "Verify the gateway belongs to the correct subnet."
            )

    def check_dhcp(self):
        dhcp_errors = [
            "dhcp failed",
            "dhcp timeout",
            "dhcp server unreachable",
            "no dhcp",
            "dhcp request failed"
        ]

        if any(error in self.evidence for error in dhcp_errors):
            self.add_finding(
                "HIGH",
                "DHCP",
                "DHCP service or reachability problem detected.",
                "Verify DHCP pool, excluded addresses, gateway and DHCP server reachability."
            )

    def check_acl(self):
        if "acl" in self.evidence or "access-list" in self.evidence:
            if any(word in self.evidence for word in [
                "deny",
                "blocked",
                "implicit deny",
                "access denied"
            ]):
                self.add_finding(
                    "HIGH",
                    "ACL",
                    "An ACL rule may be blocking required traffic.",
                    "Run 'show access-lists' and verify permit/deny rules and their order."
                )

    def check_routing(self):
        routing_errors = [
            "network unreachable",
            "no route",
            "route not found",
            "routing table missing",
            "destination unreachable"
        ]

        if any(error in self.evidence for error in routing_errors):
            self.add_finding(
                "HIGH",
                "Routing",
                "A routing problem may be preventing communication.",
                "Run 'show ip route' and verify the destination network and next hop."
            )

    def check_nat(self):
        nat_errors = [
            "nat failed",
            "nat translation missing",
            "no translation",
            "internet unreachable"
        ]

        if any(error in self.evidence for error in nat_errors):
            self.add_finding(
                "MEDIUM",
                "NAT",
                "Possible NAT or internet connectivity issue detected.",
                "Run 'show ip nat translations' and verify inside/outside interfaces."
            )

    def check_dns(self):
        if "dns" in self.evidence:
            if any(word in self.evidence for word in [
                "failed",
                "unreachable",
                "timeout",
                "blocked"
            ]):
                self.add_finding(
                    "MEDIUM",
                    "DNS",
                    "DNS resolution or DNS reachability problem detected.",
                    "Verify DNS server IP, routing and ACL rules."
                )

    def check_ip_conflict(self):
        if any(word in self.evidence for word in [
            "duplicate ip",
            "ip conflict",
            "address conflict"
        ]):
            self.add_finding(
                "CRITICAL",
                "IP Addressing",
                "Possible duplicate IP address detected.",
                "Verify host addressing and DHCP/static IP assignments."
            )

    def run_checks(self):
        self.check_interfaces()
        self.check_vlan()
        self.check_gateway()
        self.check_dhcp()
        self.check_acl()
        self.check_routing()
        self.check_nat()
        self.check_dns()
        self.check_ip_conflict()

        if not self.findings:
            self.add_finding(
                "INFO",
                "Validation",
                "No deterministic fault was identified from the supplied evidence.",
                "Collect additional evidence using show commands before making a diagnosis."
            )

        return self.findings


def calculate_confidence(findings):
    if not findings:
        return 0.30

    highest = findings[0]["severity"]

    if highest == "CRITICAL":
        return 0.95
    if highest == "HIGH":
        return 0.88
    if highest == "MEDIUM":
        return 0.72

    return 0.50


def print_report(findings, confidence):
    print("\n" + "=" * 65)
    print("                 NETSAGE AI")
    print("        NETWORK VALIDATION REPORT")
    print("=" * 65)

    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Confidence: {confidence:.0%}")
    print("\nFindings:")
    print("-" * 65)

    for number, finding in enumerate(findings, start=1):
        print(f"\n[{number}] {finding['severity']} | {finding['category']}")
        print(f"Problem : {finding['message']}")
        print(f"Action  : {finding['suggestion']}")

    print("\n" + "-" * 65)
    print("HUMAN REVIEW REQUIRED")
    print("The rule-based result is an aid, not an automatic configuration change.")
    print("=" * 65 + "\n")


def save_report(findings, confidence, filename):
    report = {
        "tool": "NetSage AI",
        "timestamp": datetime.now().isoformat(),
        "confidence": confidence,
        "human_review_required": True,
        "findings": findings
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Report saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="NetSage AI network configuration checker"
    )

    parser.add_argument(
        "--evidence",
        type=str,
        help="Network symptom or show-command evidence"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Text file containing network evidence"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="validation_report.json",
        help="Output JSON report filename"
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as file:
            evidence = file.read()
    elif args.evidence:
        evidence = args.evidence
    else:
        evidence = input("Enter network symptom/evidence: ")

    checker = NetworkChecker(evidence)
    findings = checker.run_checks()

    confidence = calculate_confidence(findings)

    print_report(findings, confidence)
    save_report(findings, confidence, args.output)


if __name__ == "__main__":
    main()
