import json
import os
from config import OUTPUT_DIR


def create_transaction_bundle(patient_id, patient_resource, org_id, org_resource, 
                            composition_id, composition_resource, resource_entries):
    """
    Create a FHIR transaction bundle for HAPI FHIR server.
    
    Args:
        patient_id: Patient UUID
        patient_resource: Patient FHIR resource
        org_id: Organization UUID
        org_resource: Organization FHIR resource
        composition_id: Composition UUID
        composition_resource: Composition FHIR resource
        resource_entries: List of other resource entries (conditions, medications, allergies)
        
    Returns:
        dict: Transaction bundle
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
            },
            {
                "fullUrl": f"urn:uuid:{composition_id}",
                "resource": composition_resource,
                "request": {
                    "method": "PUT",
                    "url": f"Composition/{composition_id}"
                }
            }
        ] + resource_entries
    }
    
    return transaction_bundle


def create_document_bundle(patient_id, patient_resource, org_id, org_resource,
                         composition_id, composition_resource, resource_entries):
    """
    Create a FHIR document bundle for IPS compliance.
    
    Args:
        patient_id: Patient UUID
        patient_resource: Patient FHIR resource
        org_id: Organization UUID
        org_resource: Organization FHIR resource
        composition_id: Composition UUID
        composition_resource: Composition FHIR resource
        resource_entries: List of other resource entries (conditions, medications, allergies)
        
    Returns:
        dict: Document bundle
    """
    document_bundle = {
        "resourceType": "Bundle",
        "type": "document",
        "entry": [
            {"fullUrl": f"urn:uuid:{composition_id}", "resource": composition_resource},
            {"fullUrl": f"urn:uuid:{patient_id}", "resource": patient_resource},
            {"fullUrl": f"urn:uuid:{org_id}", "resource": org_resource},
        ] + [{"fullUrl": entry["fullUrl"], "resource": entry["resource"]} for entry in resource_entries]
    }
    
    return document_bundle


def save_document_bundle(document_bundle, hcn):
    """
    Save document bundle to file.
    
    Args:
        document_bundle: FHIR document bundle
        hcn: Health card number for filename
        
    Returns:
        str: Path to saved file
    """
    bundle_filename = f"bundle_{hcn.replace(' ', '')}.json"
    bundle_path = os.path.join(OUTPUT_DIR, bundle_filename)
    
    with open(bundle_path, "w", encoding="utf-8") as f:
        json.dump(document_bundle, f, indent=2)
    
    return bundle_path