# NetSage AI

## Evidence-Driven Network Troubleshooting Assistant

NetSage AI is a network troubleshooting assistant designed for Cisco-style lab environments.

It combines deterministic Python-based validation with an AI-assisted diagnosis workflow to help identify possible network configuration problems and recommend evidence-based troubleshooting steps.

---

## Problem Statement

Network troubleshooting often requires checking multiple configuration outputs such as VLANs, routing tables, ACLs, DHCP, NAT and interface status.

NetSage AI aims to organize this troubleshooting process by taking network symptoms and available evidence, identifying possible root causes, recommending verification commands, and keeping a human reviewer in the decision loop.

---

## Key Features

- Network symptom and evidence analysis
- Rule-based configuration validation
- VLAN troubleshooting
- Gateway validation
- DHCP issue detection
- ACL issue detection
- Routing issue detection
- NAT issue detection
- DNS issue detection
- IP conflict detection
- Severity classification
- Confidence scoring
- Recommended verification commands
- Human review workflow
- Structured troubleshooting dataset

---

## Project Architecture

```text
Network Evidence
       |
       v
+----------------------+
|  NetSage AI Input    |
+----------+-----------+
           |
           v
+----------------------+
| Python Rule Checker  |
+----------+-----------+
           |
           v
+----------------------+
| Finding Generation   |
+----------+-----------+
           |
           v
+----------------------+
| AI-Assisted Analysis |
+----------+-----------+
           |
           v
+----------------------+
| Human Review         |
| Accept / Edit / Reject|
+----------------------+
