import json
import re
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Initialize client
load_dotenv()

# Get API key from environment (works both local + Streamlit Cloud secrets)
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ ANTHROPIC_API_KEY is missing in environment variables")

client = Anthropic(api_key=api_key)

# Load input data
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Extract JSON safely from model output
def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return None
        return json.loads(text[start:end+1])
    except:
        return None

# Validate output structure
def validate_output(output_text):
    parsed = extract_json(output_text)

    if not parsed:
        return False, "Invalid JSON output"

    required_keys = [
        "release_decision",
        "confidence_score",
        "key_risks",
        "missing_validations",
        "recommendations"
    ]

    for key in required_keys:
        if key not in parsed:
            return False, f"Missing key: {key}"

    return True, parsed

# Main execution
def run_gatekeeper(data):

    prompt = f"""
Evaluate this software release and return structured JSON:

INPUT DATA:
{json.dumps(data, indent=2)}

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "release_decision": "GO | NO_GO | CONDITIONAL",
  "confidence_score": 0.0,
  "top_3_decision_factors": [],
  "confidence_reason": "",
  "key_risks": [],
  "missing_validations": [],
  "recommendations": []
}}

Additional Signals:
- performance_tested: Indicates if performance validation was done
- security_scan: Indicates if security validation was done

Rules:
- Output ONLY valid JSON
- No markdown
- No explanation
- No extra text

Additional Rules:
- If performance_tested or security_scan is "Not Provided", include in missing_validations
- If either is "Failed", treat as high risk

Additional Requirements:
- Identify top 3 strongest factors influencing the decision
- Clearly explain why the confidence score is not higher or lower

"""

    max_attempts = 3
    error_context = ""

    for attempt in range(max_attempts):

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            messages=[
                {
                    "role": "user",
                    "content": prompt + ("\n\nPrevious failure:\n" + error_context if error_context else "")
                }
            ],
            system="You are a strict JSON generator. Output ONLY valid JSON."
        )

        output_text = response.content[0].text

        valid, parsed = validate_output(output_text)

        if valid:
            print("\n✅ Final Decision:\n")
            print(json.dumps(parsed, indent=2))
            return parsed

        error_context = output_text[:500]
        print(f"⚠️ Attempt {attempt+1} failed: {parsed}")

    return {
    "release_decision": "ERROR",
    "confidence_score": 0.0,
    "key_risks": ["Model failed to produce valid JSON"],
    "missing_validations": [],
    "recommendations": ["Check prompt / model stability"]
}
# Entry point
if __name__ == "__main__":
    data = load_data("data/complex.json")
    run_gatekeeper(data)

def compute_breakdown(data):
    breakdown = []

    if data["coverage"] < 70:
        breakdown.append("Low test coverage increases risk")

    if data["p1_defects"] > 0:
        breakdown.append("Presence of P1 defects is a major risk factor")

    if data["flaky_tests"] > 5:
        breakdown.append("High flaky tests reduce confidence in test reliability")

    if not data["rollback_ready"]:
        breakdown.append("No rollback plan increases release risk")

    if data["recent_incidents"] > 2:
        breakdown.append("Recent production incidents indicate instability")

    if data.get("performance_tested") == "Not Provided":
        breakdown.append("Performance validation missing")

    if data.get("security_scan") == "Not Provided":
        breakdown.append("Security validation missing")

    if data.get("performance_tested") == "Failed":
        breakdown.append("Performance tests failed - high risk")

    if data.get("security_scan") == "Failed":
        breakdown.append("Security scan failed - high risk")

    return breakdown

def run_pipeline(input_data):
    result = run_gatekeeper(input_data)

    # Add deterministic breakdown
    breakdown = compute_breakdown(input_data)

    if isinstance(result, dict):
        result["decision_breakdown"] = breakdown

    return result


if __name__ == "__main__":
    sample = {
        "coverage": 80,
        "p1_defects": 1,
        "flaky_tests": 5,
        "rollback_ready": True,
        "recent_incidents": 0
    }

    print(run_pipeline(sample))
