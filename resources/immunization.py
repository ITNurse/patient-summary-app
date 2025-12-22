import uuid
import json
import pandas as pd
from fhir.resources.immunization import Immunization
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference


def create_immunization_resources(immunizations_df, hcn, patient_id):
    """
    Create FHIR Immunization resources for a patient using fhir.resources.

    Args:
        immunizations_df: DataFrame containing immunization data
        hcn: Health card number to filter by
        patient_id: Patient UUID reference

    Returns:
        list: List of immunization resource entries for bundle
    """
    immunization_entries = []
    patient_immunizations = immunizations_df[immunizations_df["patient.identifier"] == hcn]
    num_immunizations = len(patient_immunizations)

    for _, row in patient_immunizations.iterrows():
        immunization_id = str(uuid.uuid4())
        occurrence_date = pd.to_datetime(row["occurrence.date"]).isoformat()

        immunization = Immunization(
            id=immunization_id,
            status=row["status.coding.code"],
            vaccineCode=CodeableConcept(coding=[
                Coding(
                    system=row["vaccine.coding.system"],
                    code=str(row["vaccine.coding.code"]),
                    display=row["vaccine.coding.display"]
                )
            ]),
            patient=Reference(reference=f"urn:uuid:{patient_id}"),
            occurrenceDateTime=occurrence_date,
            primarySource=True,
            site=CodeableConcept(coding=[
                Coding(
                    system=row["site.coding.system"],
                    code=row["site.coding.code"],
                    display=row["site.coding.display"]
                )
            ]),
            route=CodeableConcept(coding=[
                Coding(
                    system=row["route.coding.system"],
                    code=row["route.coding.code"],
                    display=row["route.coding.display"]
                )
            ])
        )

        immunization_entry = {
        "fullUrl": f"urn:uuid:{immunization_id}",
        "resource": json.loads(immunization.json(by_alias=True)),
        "request": {
            "method": "PUT",
            "url": f"Immunization/{immunization_id}"
        }
    }

        immunization_entries.append(immunization_entry)

    return num_immunizations, immunization_entries

def get_immunization_references(immunization_entries):
    """
    Extract references for composition sections.

    Args:
        immunization_entries: List of immunization entries

    Returns:
        list: List of immunization references
    """
    return [entry["fullUrl"] for entry in immunization_entries]