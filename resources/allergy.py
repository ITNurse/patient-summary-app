import uuid
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.annotation import Annotation
from fhir.resources.fhirtypes import DateTime


def create_allergy_resources(allergies_df, hcn, patient_id):
    """
    Create FHIR AllergyIntolerance resources for a patient using fhir.resources.

    Args:
        allergies_df: DataFrame containing allergy data
        hcn: Health card number to filter by
        patient_id: Patient UUID reference

    Returns:
        list: List of allergy resource entries for bundle
    """
    allergy_entries = []
    patient_allergies = allergies_df[allergies_df["patient.identifier"] == hcn]

    for _, allergy_row in patient_allergies.iterrows():
        allergy_id = str(uuid.uuid4())

        # Build the AllergyIntolerance resource
        allergy = AllergyIntolerance(
            id=allergy_id,
            clinicalStatus=CodeableConcept(coding=[
                Coding(system=allergy_row["clinicalStatus.coding.system"], code=allergy_row["clinicalStatus.coding.code"])
            ]),
            verificationStatus=CodeableConcept(coding=[
                Coding(system=allergy_row["verificationStatus.coding.system"], code=allergy_row["verificationStatus.coding.code"])
            ]),
            code=CodeableConcept(coding=[
                Coding(
                    system=allergy_row["substance.coding.system"],
                    code=allergy_row["substance.coding.code"],
                    display=allergy_row["substance.coding.display"]
                )
            ]),
            reaction=[{
                "manifestation": [CodeableConcept(coding=[
                    Coding(
                        system=allergy_row["reaction.coding.system"],
                        code=allergy_row["reaction.coding.code"],
                        display=allergy_row["reaction.coding.display"]
                    )
                ])],
                "severity": allergy_row["severity.coding.code"].lower()
            }],
            patient=Reference(reference=f"urn:uuid:{patient_id}")
        )

        allergy_entry = {
            "fullUrl": f"urn:uuid:{allergy_id}",
            "resource": allergy.dict(by_alias=True),
            "request": {
                "method": "PUT",
                "url": f"AllergyIntolerance/{allergy_id}"
            }
        }

        allergy_entries.append(allergy_entry)

    return allergy_entries


def get_allergy_references(allergy_entries):
    """
    Extract references for composition sections.

    Args:
        allergy_entries: List of allergy entries

    Returns:
        list: List of allergy references
    """
    return [entry["fullUrl"] for entry in allergy_entries]
