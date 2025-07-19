import uuid, datetime
import pandas as pd
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference


def create_medication_resources(medications_df, hcn, patient_id):
    """
    Create FHIR MedicationStatement resources for a patient using fhir.resources.

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

        medication = MedicationStatement(
            id=medication_id,
            status=medication_row["status.coding.code"],
            subject=Reference(reference=f"urn:uuid:{patient_id}"),
            
            # Commenting out the row below as I was unable to resovle the error "Object of type datetime is not JSON serializable" related to this date:
            # effectiveDateTime=medication_row["effectivedate"],
            
            medicationCodeableConcept=CodeableConcept(
                coding=[Coding(
                    system=medication_row["medication.coding.system"],
                    code=str(medication_row["medication.coding.code"]),
                    display=medication_row["medication.coding.display"]
                )]
            )
        )

        medication_entry = {
            "fullUrl": f"urn:uuid:{medication_id}",
            "resource": medication.dict(by_alias=True),
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
