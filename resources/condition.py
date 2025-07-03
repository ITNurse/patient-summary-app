import uuid
from fhir.resources.condition import Condition
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

from config import SNOMED_SYSTEM


def create_condition_resources(conditions_df, hcn, patient_id):
    """
    Create FHIR Condition resources for a patient using fhir.resources.

    Args:
        conditions_df: DataFrame containing condition data
        hcn: Health card number to filter by
        patient_id: Patient UUID reference

    Returns:
        list: List of condition resource entries for bundle
    """
    condition_entries = []
    patient_conditions = conditions_df[conditions_df["patient.identifier"] == hcn]

    for _, condition_row in patient_conditions.iterrows():
        condition_id = str(uuid.uuid4())

        condition = Condition(
            id=condition_id,
            subject=Reference(reference=f"urn:uuid:{patient_id}"),
            code=CodeableConcept(
                coding=[Coding(
                    system=SNOMED_SYSTEM,
                    code=str(condition_row["condition.code"]),
                    display=condition_row["condition.display"]
                )]
            )
        )

        condition_entry = {
            "fullUrl": f"urn:uuid:{condition_id}",
            "resource": condition.dict(by_alias=True),
            "request": {
                "method": "PUT",
                "url": f"Condition/{condition_id}"
            }
        }

        condition_entries.append(condition_entry)

    return condition_entries


def get_condition_references(condition_entries):
    """
    Extract references for composition sections.

    Args:
        condition_entries: List of condition entries

    Returns:
        list: List of condition references
    """
    return [entry["fullUrl"] for entry in condition_entries]
