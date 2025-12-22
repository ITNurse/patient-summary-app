#!/usr/bin/env python3
"""
FHIR Bundle Generator and Uploader
Main script to orchestrate the creation and upload of FHIR bundles from CSV data.
"""

import pandas as pd
import sys

# Import our modules
from data_loader import load_csv_data, validate_data
from fhir_client import upload_bundle_to_server, test_server_connection
from bundle_builder import save_document_bundle
from process_patient import process_patient
from config import LOG_OUTPUT_PATH, FHIR_SERVER_URL

def main():
    print("\n ------  SCRIPT STARTING  ------\n\n")
    
    
    # Step 1: Test server connection
    # ------------------------------
    print("STEP 1: TESTING FHIR SERVER CONNECTION")
    print("--------------------------------------")
    if not test_server_connection():
        print("Cannot connect to FHIR server. Please check server is running.")        
        sys.exit(1)
    print("✅ FHIR server connection successful")
    
    # Step 2: Load and validate csv data
    # -----------------------------------
    print("\n STEP 2: LOADING CSV DATA")
    print("---------------------------")
    try:
        organization_df, compositions_df, patients_df, conditions_df, medications_df, allergies_df, immunizations_df = load_csv_data()
    except Exception as e:
        print(f"Exception during CSV loading: {e}")
        sys.exit(1)
    if not validate_data(organization_df, compositions_df, patients_df, conditions_df, medications_df, allergies_df, immunizations_df):
        print("CSV file data validation failed. Please check the structure and contents of your CSV files.")
        sys.exit(1)
    
    # Step 3: Process each patient
    # ----------------------------
    print(f"\nSTEP 3: PROCESSING PATIENTS")
    print("------------------------------")
    log = []
    
    for index, patient_row in patients_df.iterrows():
        print(f"\nProcessing Patient [{index+1}/{len(patients_df)}]:")
        try:
            # Step 3a: Process patient
            # --------------------------
            transaction_bundle, document_bundle, hcn, composition_resource = process_patient(
                patient_row, organization_df, compositions_df, conditions_df, medications_df, allergies_df, immunizations_df
            )
            
            # Step 3b: Save document bundle to file and record results in log
            # ----------------------------------------------------------------
            save_success, bundle_path = save_document_bundle(document_bundle, hcn)

            if save_success:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Save Bundle",
                    "Status": "Success",
                    "FilePath": bundle_path
                })
                print(f"-- Created and saved bundle for patient to {bundle_path}")
            else:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Save Bundle",
                    "Status": "Failed",
                    "FilePath": ""
                })
                print(f"❌ Failed to save bundle for patient {hcn}")
                continue  # Skip upload if save failed

            # Step 3c: Upload transaction bundle to server and record results in log
            # ----------------------------------------------------------------------
            success, status_code, response_text = upload_bundle_to_server(transaction_bundle)

            if success:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Upload Bundle",
                    "Status": f"Success ({status_code})",
                })
                print(f"-- Uploaded bundle for patient to {FHIR_SERVER_URL}")
            else:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Upload Bundle",
                    "Status": f"Failed ({status_code})"
                })
                print(f"❌ Failed to upload bundle for patient {hcn}: {status_code}")
                if status_code != 0:
                    print(f"   Response: {response_text[:200]}...")

        except Exception as e:
            log.append({
                "HealthCard": patient_row.get("identifier", "Unknown"),
                "Action": "Process Patient",
                "Status": f"Error: {str(e)[:100]}"
            })
            print(f"Error processing patient: {e}")

    
    # Step 4: Save log
    # -----------------
    print(f"\n\nSTEP 4: SAVING LOG TO {LOG_OUTPUT_PATH}")
    print("----------------------------------------------------------------------------")

    try:
        df_log = pd.DataFrame(log)
        df_log.to_csv(LOG_OUTPUT_PATH, index=False)
        print("✅ Output log saved successfully")
    except Exception as e:
        print(f"❌ Failed to save output log: {e}")

    print("\n\n ------ 🎉 SCRIPT COMPLETED 🎉 ------\n\n")

if __name__ == "__main__":
    main()