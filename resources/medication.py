import uuid
from config import MEDICATION_SYSTEM


def create_medication_resources(medications_df, hcn, patient_id):
    """
    Create FHIR MedicationStatement resources for a patient.
    
    Args:
        medications_df: DataFrame containing medication data
        hcn: Health card number to filter by
        patient_id: Patient UUID reference
        
    Returns:
        list: List of medication resource entries for bundle
    """
    medication_entries = []
    
    patient_medications = medications_df[medications_df["patient.identifier"] == hcn]
    
    for _, medication_row in patient_medications.iterrows():
        medication_id = str(uuid.uuid4())
        
        medication_resource = {
            "resourceType": "MedicationStatement",
            "id": medication_id,
            "subject": {"reference": f"urn:uuid:{patient_id}"},
            "medicationCodeableConcept": {
                "coding": [{
                    "system": MEDICATION_SYSTEM,
                    "code": str(medication_row["medication.code"]),
                    "display": medication_row["medication.display"]
                }]
            },
            "status": "active"
        }
        
        medication_entry = {
            "fullUrl": f"urn:uuid:{medication_id}",
            "resource": medication_resource,
            "request": {
                "method": "PUT",
                "url": f"MedicationStatement/{medication_id}"
            }
        }
        
        medication_entries.append(medication_entry)
    
    return medication_entries


def get_medication_references(medication_entries):
    """
    Extract references for composition sections.
    
    Args:
        medication_entries: List of medication entries
        
    Returns:
        list: List of medication references
    """
    return [entry["fullUrl"] for entry in medication_entries]