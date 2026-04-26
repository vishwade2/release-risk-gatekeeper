import streamlit as st
from main import run_pipeline
st.title("🚦 AI Release Risk Gatekeeper")
st.caption("Explainable AI system for software release decision support (Claude-powered)")
st.divider()
st.subheader("🔧 Release Inputs")


# Inputs
coverage = st.slider("Test Coverage (%)", 0, 100, 75)

p1_defects = st.number_input("P1 Defects", 0, 50, 2)

flaky_tests = st.number_input("Flaky Tests", 0, 100, 5)

rollback_ready = st.checkbox("Rollback Ready", value=True)

recent_incidents = st.number_input("Recent Incidents", 0, 20, 1)

performance_tested = st.selectbox(
    "Performance Testing Status",
    ["Not Provided", "Passed", "Failed"]
)

security_scan = st.selectbox(
    "Security Scan Status",
    ["Not Provided", "Passed", "Failed"]
)

regression_status = st.selectbox(
    "Regression Test Status",
    ["Not Provided", "Passed", "Partial", "Failed"]
)

release_type = st.selectbox(
    "Release Type",
    ["Standard", "Hotfix", "Major"]
)


if st.button("Evaluate Release"):

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

    with st.expander("🧠 Full Explainability Output"):
        st.json(result)
