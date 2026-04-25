
# 🚦 AI Release Risk Gatekeeper

An explainable AI system that evaluates software release readiness using structured inputs, deterministic scoring, and Claude-based 
reasoning.

---

## 🧠 Problem Statement

Release decisions in software engineering are often:
- subjective
- inconsistent across teams
- not explainable after the fact

This project builds an **AI-powered decision intelligence layer** that standardizes release evaluation with explainability.

---

## ⚙️ System Overview

The system combines:

- 🧮 Deterministic scoring (Python logic)
- 🧠 LLM reasoning (Anthropic Claude)
- 📊 Structured validation + JSON output
- 🖥️ Interactive UI (Streamlit)

---

## 🏗️ Architecture

Streamlit UI
↓
run_pipeline()
↓
run_gatekeeper()
↓
Claude reasoning engine
↓
JSON structured decision output


---

## 📥 Input Signals

- Test Coverage (%)
- P1 Defects
- Flaky Tests
- Rollback Readiness
- Recent Production Incidents

---

## 📤 Output

- Release Decision → GO / NO-GO / CONDITIONAL
- Confidence Score
- Key Risks
- Recommendations
- Full Explainability (JSON view)

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py


🧪 Tech Stack
Python
Streamlit
Anthropic Claude API
JSON structured reasoning layer


