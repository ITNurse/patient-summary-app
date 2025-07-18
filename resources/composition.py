import uuid
import datetime
import json
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

from config import ORGANIZATION_ID, ORGANIZATION_NAME


def create_composition_resource(patient_id, allergy_refs, condition_refs, medication_refs, immunization_refs, composition_row):
    """
    Create a FHIR Composition resource for patient summary using CSV metadata.

    Args:
        patient_id: Patient UUID reference
        allergy_refs: List of allergy references
        condition_refs: List of condition references
        medication_refs: List of medication references
        immunization_refs: List of immunization references
        composition_row: Row from compositions_df with codes/display for this patient

    Returns:
        tuple: (composition_id, composition_resource_dict)
    """
    composition_id = str(uuid.uuid4())
    sections = []

    def build_section(title, system, code, display, refs):
        """Helper to create a Composition section dynamically from CSV metadata"""
        return CompositionSection(
            title=title,
            code=CodeableConcept(
                coding=[Coding(system=system, code=code, display=display)]
            ),
            entry=[Reference(reference=ref) for ref in refs]
        )

    # Build each section dynamically from CSV row
    if allergy_refs:
        sections.append(
            build_section(
                title="Allergies",
                system=composition_row["allergy.coding.code"],
                code=composition_row["allergy.coding.display"],
                display=composition_row["allergy.coding.system"],
                refs=allergy_refs
            )
        )

    if condition_refs:
        sections.append(
            build_section(
                title="Problems",
                system=composition_row["condition.coding.code"],
                code=composition_row["condition.coding.display"],
                display=composition_row["condition.coding.system"],
                refs=condition_refs
            )
        )

    if medication_refs:
        sections.append(
            build_section(
                title="Medications",
                system=composition_row["medication.coding.code"],
                code=composition_row["medication.coding.display"],
                display=composition_row["medication.coding.system"],
                refs=medication_refs
            )
        )

    if immunization_refs:
        sections.append(
            build_section(
                title="Immunizations",
                system=composition_row["immunization.coding.code"],
                code=composition_row["immunization.coding.display"],
                display=composition_row["immunization.coding.system"],
                refs=immunization_refs
            )
        )

    # ✅ Composition top-level metadata from CSV
    composition = Composition(
        id=composition_id,
        status=composition_row["status"],
        type=CodeableConcept(
            coding=[Coding(
                system=composition_row["composition.coding.code"],    
                code=composition_row["title"],                     
                display=composition_row["composition.coding.system"] 
            )]
        ),
        subject=Reference(reference=f"urn:uuid:{patient_id}"),
        date=str(datetime.datetime.now(datetime.timezone.utc).isoformat()),
        title=composition_row["id"], 
        author=[Reference(reference=f"urn:uuid:{ORGANIZATION_ID}", display=ORGANIZATION_NAME)],
        custodian=Reference(reference=f"urn:uuid:{ORGANIZATION_ID}", display=ORGANIZATION_NAME),
        section=sections
    )

    return composition_id, json.loads(composition.json(by_alias=True))
