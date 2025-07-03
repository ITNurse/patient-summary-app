import uuid
import json
import pandas as pd
from fhir.resources.immunization import Immunization
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

from config import SNOMED_SYSTEM


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

    for _, row in patient_immunizations.iterrows():
        immunization_id = str(uuid.uuid4())
        occurrence_date = pd.to_datetime(row["date"]).isoformat()

        immunization = Immunization(
            id=immunization_id,
            status="completed",
            vaccineCode=CodeableConcept(coding=[
                Coding(
                    system=SNOMED_SYSTEM,
                    code=str(row["vaccine.code"]),
                    display=row["vaccine.display"]
                )
            ]),
            patient=Reference(reference=f"urn:uuid:{patient_id}"),
            occurrenceDateTime=occurrence_date,
            primarySource=True,
            site=CodeableConcept(coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0493",
                    code=row["site.code"],
                    display=row["site.display"]
                )
            ]),
            route=CodeableConcept(coding=[
                Coding(
                    system=row["route.system"],
                    code=row["route.code"],
                    display=row["route.display"]
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

    return immunization_entries

def get_immunization_references(immunization_entries):
    """
    Extract references for composition sections.

    Args:
        immunization_entries: List of immunization entries

    Returns:
        list: List of immunization references
    """
    return [entry["fullUrl"] for entry in immunization_entries]