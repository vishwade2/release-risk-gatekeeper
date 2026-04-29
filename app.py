import streamlit as st
from main import run_pipeline
SCENARIOS = {
    "Custom": {
        "coverage": 75,
        "p1_defects": 1,
        "flaky_tests": 5,
        "rollback_ready": True,
        "recent_incidents": 1,
        "performance_tested": "Not Provided",
        "security_scan": "Not Provided",
        "regression_status": "Partial",
        "release_type": "Standard"
    },
    "Safe Standard Release": {
        "coverage": 90,
        "p1_defects": 0,
        "flaky_tests": 1,
        "rollback_ready": True,
        "recent_incidents": 0,
        "performance_tested": "Passed",
        "security_scan": "Passed",
        "regression_status": "Passed",
        "release_type": "Standard"
    },
    "Risky Major Release": {
        "coverage": 62,
        "p1_defects": 2,
        "flaky_tests": 12,
        "rollback_ready": False,
        "recent_incidents": 3,
        "performance_tested": "Failed",
        "security_scan": "Not Provided",
        "regression_status": "Partial",
        "release_type": "Major"
    },
    "Hotfix with Limited Validation": {
        "coverage": 72,
        "p1_defects": 0,
        "flaky_tests": 4,
        "rollback_ready": True,
        "recent_incidents": 1,
        "performance_tested": "Not Provided",
        "security_scan": "Passed",
        "regression_status": "Partial",
        "release_type": "Hotfix"
    }
}
st.title("🚦 AI Release Risk Gatekeeper")
st.caption("Explainable AI-assisted Release Decision System")
st.info(
    """This prototype combines rule-based scoring for consistent evaluation 
    with AI-assisted reasoning to explain risks, missing validations, and recommendations. 
    It is designed to support — not replace — cross-functional release decision-making."""
)
with st.expander("ℹ️ What this prototype is designed to demonstrate"):
    st.write(
        """
        This prototype is not intended to be just a form or a score calculator.

        It demonstrates how release decision support can combine:
        - structured release signals
        - configurable scoring logic
        - deterministic risk indicators
        - AI-assisted reasoning for risks, gaps, and recommendations

        A simple checklist can confirm whether items are present.
        This system attempts to interpret the combined release context and explain why a release may be GO, NO-GO, or CONDITIONAL.

        The current version is intentionally lightweight. Future versions can connect directly to release tools, test reports, CI/CD 
        pipelines, and historical release outcomes.
        """
    )
with st.expander("📌 Current scope and future direction"):
    st.write(
        """
        Current version:
        - manual input / scenario-based evaluation
        - configurable rule-based confidence score
        - AI-assisted risk reasoning
        - explainable output

        Future direction:
        - CSV / Excel upload
        - integration with ADO, Jira, test management tools, and CI/CD pipelines
        - feedback loop based on release outcomes
        - multi-stage evaluation pipeline
        - controlled modular / agent-style reasoning
        """
    )
st.divider()
st.subheader("🔧 Release Inputs")
scenario_name = st.selectbox(
    "Start with a sample release scenario",
    list(SCENARIOS.keys()),
    help="Pre-fills inputs with realistic release situations. You can still adjust values before evaluating."
)
st.caption("Scenario presets reduce manual entry and help compare how different release contexts affect the decision.")
scenario = SCENARIOS[scenario_name]
st.subheader("1️⃣ Select a scenario or adjust release inputs")
# Inputs
coverage = st.slider("Test Coverage (%)", 0, 100, scenario["coverage"])

p1_defects = st.number_input("P1 Defects", 0, 50, scenario["p1_defects"])

flaky_tests = st.number_input("Flaky Tests", 0, 100, scenario["flaky_tests"])

rollback_ready = st.checkbox("Rollback Ready", value=scenario["rollback_ready"])

recent_incidents = st.number_input("Recent Incidents", 0, 20, scenario["recent_incidents"])

performance_tested = st.selectbox(
    "Performance Testing Status",
    ["Not Provided", "Passed", "Failed"],
    index=["Not Provided", "Passed", "Failed"].index(scenario["performance_tested"])

)

security_scan = st.selectbox(
    "Security Scan Status",
    ["Not Provided", "Passed", "Failed"],
    index=["Not Provided", "Passed", "Failed"].index(scenario["security_scan"])
)

regression_status = st.selectbox(
    "Regression Test Status",
    ["Not Provided", "Passed", "Partial", "Failed"],
    index=["Not Provided", "Passed", "Partial", "Failed"].index(scenario["regression_status"])
)

release_type = st.selectbox(
    "Release Type",
    ["Standard", "Hotfix", "Major"],
    index=["Standard", "Hotfix", "Major"].index(scenario["release_type"])
)

st.divider()
st.subheader("2️⃣ Run release evaluation")
st.caption("Click below to generate the release decision, confidence score, risks, and recommendations.")

evaluate_clicked = st.button(
    "🚦 Evaluate Release Readiness",
    type="primary",
    use_container_width=True
)

if evaluate_clicked:

    input_data = {
      "coverage": coverage,
      "p1_defects": p1_defects,
      "flaky_tests": flaky_tests,
      "rollback_ready": rollback_ready,
      "recent_incidents": recent_incidents,
      "performance_tested": performance_tested,
      "security_scan": security_scan,
      "regression_status": regression_status,
      "release_type": release_type
    }
    result = run_pipeline(input_data)

    st.subheader("📊 Decision")

    st.markdown(f"### {result.get('release_decision', 'UNKNOWN')}")

    st.subheader("🔍 Decision Breakdown (Deterministic Signals)")
    for item in (result.get("decision_breakdown") or []):
        st.write(f"• {item}")

    st.subheader("⚠️ Key Risks")
    for r in result.get("key_risks", []):
        st.write(f"• {r}")

    st.subheader("💡 Recommendations")
    for r in result.get("recommendations", []):
        st.write(f"• {r}")

    st.metric("Confidence Score", result.get("confidence_score", 0))

    st.caption(
    "Confidence score is a rule-based release readiness indicator (0–1), derived from weighted risk signals — not a probability of success."
)
    with st.expander("🧠 Full Explainability Output"):
        st.json(result)
