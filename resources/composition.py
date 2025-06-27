import uuid
import datetime
from config import LOINC_SYSTEM, ORGANIZATION_ID, ORGANIZATION_NAME


def create_composition_resource(patient_id, allergy_refs, condition_refs, medication_refs, immunization_refs):

    """
    Create a FHIR Composition resource for patient summary.
    
    Args:
        patient_id: Patient UUID reference
        allergy_refs: List of allergy references
        condition_refs: List of condition references
        medication_refs: List of medication references
        immunization_refs: List of immunization references
        
    Returns:
        tuple: (composition_id, composition_resource)
    """
    composition_id = str(uuid.uuid4())
    
    # Build sections based on available data
    sections = []
    
    if allergy_refs:
        sections.append({
            "title": "Allergies",
            "code": {
                "coding": [{
                    "system": LOINC_SYSTEM,
                    "code": "48765-2",
                    "display": "Allergies and adverse reactions"
                }]
            },
            "entry": [{"reference": ref} for ref in allergy_refs]
        })
    
    if condition_refs:
        sections.append({
            "title": "Problems",
            "code": {
                "coding": [{
                    "system": LOINC_SYSTEM,
                    "code": "11450-4",
                    "display": "Problem List"
                }]
            },
            "entry": [{"reference": ref} for ref in condition_refs]
        })
    
    if medication_refs:
        sections.append({
            "title": "Medications",
            "code": {
                "coding": [{
                    "system": LOINC_SYSTEM,
                    "code": "10160-0",
                    "display": "History of Medication Use"
                }]
            },
            "entry": [{"reference": ref} for ref in medication_refs]
        })
    
    if immunization_refs:
        sections.append({
            "title": "Immunizations",
            "code": {
                "coding": [{
                    "system": LOINC_SYSTEM,
                    "code": "11369-6",
                    "display": "History of immunizations"
                }]
            },
            "entry": [{"reference": ref} for ref in immunization_refs]
        })
    
    composition_resource = {
        "resourceType": "Composition",
        "id": composition_id,
        "status": "final",
        "type": {
            "coding": [{
                "system": LOINC_SYSTEM,
                "code": "60591-5",
                "display": "Patient Summary"
            }]
        },
        "subject": {"reference": f"urn:uuid:{patient_id}"},
        "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "title": "PS-CA Patient Summary",
        "author": [{
            "reference": f"urn:uuid:{ORGANIZATION_ID}",
            "display": ORGANIZATION_NAME
        }],
        "custodian": {
            "reference": f"urn:uuid:{ORGANIZATION_ID}",
            "display": ORGANIZATION_NAME
        },
        "section": sections
    }
    
    return composition_id, composition_resource