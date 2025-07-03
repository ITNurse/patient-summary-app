import json
import os
from config import OUTPUT_DIR


def create_transaction_bundle(patient_id, patient_resource, org_id, org_resource,
                              allergy_entries, condition_entries, medication_entries, immunization_entries):
    """
    Create a FHIR transaction bundle for Patient, Organization, AllergyIntolerance, Condition, MedicationStatement, and Immunization resources.

    Args:
        patient_id: Patient UUID
        patient_resource: Patient FHIR resource (dictionary)
        org_id: Organization UUID
        org_resource: Organization FHIR resource (dictionary)
        allergy_entries: List of AllergyIntolerance entries
        condition_entries: List of Condition entries
        medication_entries: List of MedicationStatement entries
        immunization_entries: List of Immunization entries

    Returns:
        dict: FHIR transaction bundle
    """
    transaction_bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": [
            {
                "fullUrl": f"urn:uuid:{patient_id}",
                "resource": patient_resource,
                "request": {
                    "method": "PUT",
                    "url": f"Patient/{patient_id}"
                }
            },
            {
                "fullUrl": f"urn:uuid:{org_id}",
                "resource": org_resource,
                "request": {
                    "method": "PUT",
                    "url": f"Organization/{org_id}"
                }
            }
        ] + allergy_entries + condition_entries + medication_entries + immunization_entries
    }

    return transaction_bundle


def create_document_bundle(patient_id, patient_resource, org_id, org_resource, composition_resource,
                           allergy_entries, condition_entries, medication_entries, immunization_entries):
    """
    Create a FHIR document bundle for Patient Summary.

    Args:
        patient_id: Patient UUID
        patient_resource: Patient FHIR resource
        org_id: Organization UUID
        org_resource: Organization FHIR resource
        composition_resource: Composition resource (dict)
        allergy_entries: List of AllergyIntolerance entries
        condition_entries: List of Condition entries
        medication_entries: List of MedicationStatement entries
        immunization_entries: List of Immunization entries

    Returns:
        dict: FHIR document bundle
    """
    document_bundle = {
        "resourceType": "Bundle",
        "type": "document",
        "entry": [
            {"fullUrl": f"urn:uuid:{composition_resource['id']}", "resource": composition_resource},
            {"fullUrl": f"urn:uuid:{patient_id}", "resource": patient_resource},
            {"fullUrl": f"urn:uuid:{org_id}", "resource": org_resource},
        ] + [
            {"fullUrl": entry["fullUrl"], "resource": entry["resource"]}
            for entry in (allergy_entries + condition_entries + medication_entries + immunization_entries)
        ]
    }

    return document_bundle


def save_document_bundle(document_bundle, hcn):
    """
    Save document bundle to file.

    Args:
        document_bundle: FHIR document bundle
        hcn: Health card number for filename

    Returns:
        tuple: (success: bool, file_path: str or None)
    """
    try:
        filename = f"bundle_{hcn.replace(' ', '')}.json"
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(document_bundle, f, indent=2)
        return True, file_path
    except Exception as e:
        print(f"Failed to save bundle for {hcn}: {e}")
        return False, None
