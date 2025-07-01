import uuid
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from resources.profile_utils import add_meta_profile
from config import MEDICATION_SYSTEM


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
            status="active",
            subject=Reference(reference=f"urn:uuid:{patient_id}"),
            medicationCodeableConcept=CodeableConcept(
                coding=[Coding(
                    system=MEDICATION_SYSTEM,
                    code=str(medication_row["medication.code"]),
                    display=medication_row["medication.display"]
                )]
            )
        )

        medication_entry = {
            "fullUrl": f"urn:uuid:{medication_id}",
            "resource": add_meta_profile(medication.dict(by_alias=True), "MedicationStatement"),
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
