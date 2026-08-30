"""
NetSage AI
Evidence-Driven Network Troubleshooting Assistant

Web interface for collecting network symptoms/evidence
and displaying deterministic validation results.
"""

import streamlit as st
from checker import NetworkChecker, calculate_confidence


st.set_page_config(
    page_title="NetSage AI",
    page_icon="🌐",
    layout="wide"
)


def main():
    st.title("🌐 NetSage AI")
    st.subheader("Evidence-Driven Network Troubleshooting Assistant")

    st.info(
        "Enter a network symptom and available evidence. "
        "The validation engine will identify possible configuration issues. "
        "Human verification is required before applying any fix."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        symptom = st.text_area(
            "Network Symptom",
            placeholder=(
                "Example: PC cannot reach the server "
                "even though the gateway is reachable."
            ),
            height=150
        )

    with col2:
        evidence = st.text_area(
            "Network Evidence / Show Command Output",
            placeholder=(
                "Example:\n"
                "show ip route\n"
                "Destination network is not present"
            ),
            height=150
        )

    if st.button("🔍 Analyze Incident", use_container_width=True):

        if not symptom.strip() and not evidence.strip():
            st.warning("Please provide a symptom or network evidence.")
            return

        combined_input = f"{symptom}\n{evidence}"

        checker = NetworkChecker(combined_input)
        findings = checker.run_checks()
        confidence = calculate_confidence(findings)

        st.divider()
        st.header("Diagnostic Results")

        st.metric(
            "Confidence",
            f"{confidence:.0%}"
        )

        if findings:

            for finding in findings:

                severity = finding["severity"]

                if severity == "CRITICAL":
                    st.error(
                        f"🚨 {severity} — {finding['category']}"
                    )

                elif severity == "HIGH":
                    st.warning(
                        f"⚠️ {severity} — {finding['category']}"
                    )

                elif severity == "MEDIUM":
                    st.info(
                        f"ℹ️ {severity} — {finding['category']}"
                    )

                else:
                    st.success(
                        f"✓ {severity} — {finding['category']}"
                    )

                st.write(
                    f"**Finding:** {finding['message']}"
                )

                st.write(
                    f"**Recommended Action:** "
                    f"{finding['suggestion']}"
                )

                st.divider()

        st.subheader("Human Review")

        review = st.radio(
            "Reviewer Decision",
            ["Not Reviewed", "Accepted", "Edited", "Rejected"],
            horizontal=True
        )

        if review != "Not Reviewed":
            st.success(
                f"Review status recorded: **{review}**"
            )

        st.caption(
            "NetSage AI provides troubleshooting assistance. "
            "Do not apply configuration changes without validating "
            "the recommendation against the actual network."
        )


if __name__ == "__main__":
    main()
