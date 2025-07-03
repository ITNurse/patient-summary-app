#!/usr/bin/env python3
"""
FHIR Bundle Generator and Uploader
Main script to orchestrate the creation and upload of FHIR bundles from CSV data.
"""

import pandas as pd
import sys
from pathlib import Path

# Import our modules
from data_loader import load_csv_data, validate_data
from fhir_client import upload_bundle_to_server, test_server_connection
from bundle_builder import create_transaction_bundle, create_document_bundle, save_document_bundle
from config import LOG_OUTPUT_PATH, FHIR_SERVER_URL

# Import resource modules
from resources.patient import create_patient_resource
from resources.organization import create_organization_resource
from resources.condition import create_condition_resources, get_condition_references
from resources.medication import create_medication_resources, get_medication_references
from resources.allergy import create_allergy_resources, get_allergy_references
from resources.composition import create_composition_resource
from resources.immunization import create_immunization_resources, get_immunization_references

def process_patient(patient_row, conditions_df, medications_df, allergies_df, immunizations_df):
    """
    Process a single patient and create all associated resources.
    
    Args:
        patient_row: Patient data row
        conditions_df: Conditions DataFrame
        medications_df: Medications DataFrame
        allergies_df: Allergies DataFrame
        immunizations_df: Immunizations DataFrame
        
    Returns:
        tuple: (transaction_bundle, document_bundle, hcn)
    """
    
    hcn = patient_row["identifier"]
    
    # Create core resources
    patient_id, patient_resource = create_patient_resource(patient_row)
    org_id, org_resource = create_organization_resource()
    
    # Create clinical resources
    condition_entries = create_condition_resources(conditions_df, hcn, patient_id)
    medication_entries = create_medication_resources(medications_df, hcn, patient_id)
    allergy_entries = create_allergy_resources(allergies_df, hcn, patient_id)
    immunization_entries = create_immunization_resources(immunizations_df, hcn, patient_id)

    # Get references for composition
    condition_refs = get_condition_references(condition_entries)
    medication_refs = get_medication_references(medication_entries)
    allergy_refs = get_allergy_references(allergy_entries)
    immunization_refs = get_immunization_references(immunization_entries)

    # Create composition
    composition_id, composition_resource = create_composition_resource(
        patient_id, allergy_refs, condition_refs, medication_refs, immunization_refs
    )
    
    # Create bundles
    transaction_bundle = create_transaction_bundle(
        patient_id, patient_resource, org_id, org_resource,
        allergy_entries, condition_entries, medication_entries, immunization_entries
    )
    
    document_bundle = create_document_bundle(
        patient_id, patient_resource, org_id, org_resource, composition_resource,
        allergy_entries, condition_entries, medication_entries, immunization_entries
    )
    
    return transaction_bundle, document_bundle, hcn


def main():
    """Main execution function."""
    print("FHIR Bundle Generator and Uploader")
    print("=" * 50)
    
    # Test server connection
    print("Testing FHIR server connection...")
    if not test_server_connection():
        print("Cannot connect to FHIR server. Please check server is running.")        
        sys.exit(1)
    print("FHIR server connection successful")
    
    # Load and validate csv data
    print("\nLoading CSV data...")
    try:
        patients_df, conditions_df, medications_df, allergies_df, immunizations_df = load_csv_data()
    except Exception as e:
        print(f"Exception during CSV loading: {e}")
        sys.exit(1)
    if not validate_data(patients_df, conditions_df, medications_df, allergies_df, immunizations_df):
        print("CSV file data validation failed. Please check the structure and contents of your CSV files.")
        sys.exit(1)
    
    # Process each patient
    print(f"\nProcessing {len(patients_df)} patients...")
    log = []
    
    for index, patient_row in patients_df.iterrows():
        print(f"\n[Patient {index+1}/{len(patients_df)}]")
        try:
            # Process patient
            transaction_bundle, document_bundle, hcn = process_patient(
                patient_row, conditions_df, medications_df, allergies_df, immunizations_df
            )

            # Save document bundle to file
            save_success, bundle_path = save_document_bundle(document_bundle, hcn)

            if save_success:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Save Bundle",
                    "Status": "Success",
                    "FilePath": bundle_path
                })
                print(f"✅ Created and saved bundle for patient {hcn} to {bundle_path}")
            else:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Save Bundle",
                    "Status": "Failed",
                    "FilePath": ""
                })
                print(f"❌ Failed to save bundle for patient {hcn}")
                continue  # Skip upload if save failed

            # Upload transaction bundle to server
            success, status_code, response_text = upload_bundle_to_server(transaction_bundle)

            if success:
                log.append({
                    "HealthCard": hcn,
                    "Action": "Upload Bundle",
                    "Status": f"Success ({status_code})",
                })
                print(f"✅ Uploaded bundle for patient {hcn} to {FHIR_SERVER_URL}")
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

    
    # Save log
    print(f"\nSaving upload log to {LOG_OUTPUT_PATH}...")

    try:
        df_log = pd.DataFrame(log)
        df_log.to_csv(LOG_OUTPUT_PATH, index=False)
        print("✅ Upload log saved successfully.")
    except Exception as e:
        print(f"❌ Failed to save upload log: {e}")


if __name__ == "__main__":
    main()