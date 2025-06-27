import json
import os
import requests

FHIR_SERVER_URL = "http://localhost:8080/fhir"  # Change if needed

def validate_bundle(bundle_path, hcn, index, total):
    """
    Validate a FHIR bundle using HAPI FHIR's $validate endpoint and save a JSON validation log.
    
    Args:
        bundle_path (str): Path to the saved document bundle file.
        hcn (str): Health Card Number (used in filenames and logs).
        index (int): Patient index in loop.
        total (int): Total number of patients being processed.
    
    Returns:
        bool: True if bundle is valid (no errors), False otherwise.
    """
    print(f"🔎 [{index+1}/{total}] Validating bundle for patient {hcn}...")

    # Load the bundle
    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    # POST to $validate
    url = f"{FHIR_SERVER_URL}/Bundle/$validate"
    headers = {"Content-Type": "application/fhir+json"}
    try:
        response = requests.post(url, headers=headers, json=bundle)
    except requests.exceptions.RequestException as e:
        print(f"❌ Validation request failed: {e}")
        return False

    if response.status_code != 200:
        print(f"❌ Server returned status {response.status_code}")
        print(f"   Body: {response.text[:200]}...")
        return False

    outcome = response.json()
    issues = outcome.get("issue", [])

    errors = [i for i in issues if i.get("severity") in ["fatal", "error"]]
    warnings = [i for i in issues if i.get("severity") == "warning"]
    info = [i for i in issues if i.get("severity") == "information"]

    if errors:
        print(f"❌ {len(errors)} validation error(s), {len(warnings)} warning(s):")
        for e in errors:
            print(f"  - {e.get('diagnostics', 'No detail')}")
    else:
        print(f"✅ Bundle is valid! ({len(warnings)} warnings)")

    # ✅ Save the validation log
    log_data = {
        "health_card": hcn,
        "status_code": response.status_code,
        "total_issues": len(issues),
        "errors": errors,
        "warnings": warnings,
        "info": info,
    }

    log_filename = f"validation_{hcn.replace(' ', '')}.json"
    log_path = os.path.join(os.path.dirname(bundle_path), log_filename)
    with open(log_path, "w", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, indent=2)

    print(f"📝 Validation log saved to: {log_path}")
    return len(errors) == 0
