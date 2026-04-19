import json

def validate_input(data):
    required_fields = [
        "test_coverage",
        "critical_defects",
    ]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    return True, None

import json

def extract_json(text):
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    candidate = text[start:end+1]

    try:
        return json.loads(candidate)
    except:
        return None


def validate_output(output_text):
    parsed = extract_json(output_text)

    if not parsed:
        return False, "No valid JSON found"

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

    except Exception as e:
        return False, f"Invalid JSON: {str(e)}"
