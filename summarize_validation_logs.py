import os
import json
import pandas as pd
from config import OUTPUT_DIR  # Or replace with a string like "output"

def summarize_validation_logs(output_dir=OUTPUT_DIR):
    summary_records = []

    for filename in os.listdir(output_dir):
        if filename.startswith("validation_") and filename.endswith(".json"):
            path = os.path.join(output_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            summary_records.append({
                "HealthCard": data.get("health_card", "Unknown"),
                "StatusCode": data.get("status_code"),
                "TotalIssues": data.get("total_issues", 0),
                "Errors": len(data.get("errors", [])),
                "Warnings": len(data.get("warnings", [])),
                "Info": len(data.get("info", [])),
                "LogFile": filename
            })

    df = pd.DataFrame(summary_records)
    output_path = os.path.join(output_dir, "validation_summary.xlsx")
    df.to_excel(output_path, index=False)
    print(f"✅ Summary saved to: {output_path}")
    return df

def flatten_validation_issues(output_dir=OUTPUT_DIR):
    records = []

    for filename in os.listdir(output_dir):
        if filename.startswith("validation_") and filename.endswith(".json"):
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            hcn = data.get("health_card", "Unknown")
            issues = (
                data.get("errors", []) +
                data.get("warnings", []) +
                data.get("info", [])
            )

            for issue in issues:
                records.append({
                    "HealthCard": hcn,
                    "Severity": issue.get("severity", ""),
                    "Code": issue.get("code", ""),
                    "Diagnostics": issue.get("diagnostics", ""),
                    "LogFile": filename
                })

    df = pd.DataFrame(records)
    output_path = os.path.join(output_dir, "validation_issues_table.xlsx")
    df.to_excel(output_path, index=False)
    print(f"✅ Issue-level table saved to: {output_path}")
    return df
