import uuid
import datetime
import json
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
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
        tuple: (composition_id, composition_resource_dict)
    """
    composition_id = str(uuid.uuid4())
    sections = []

    def build_section(title, code, display, refs):
        return CompositionSection(
            title=title,
            code=CodeableConcept(coding=[Coding(system=LOINC_SYSTEM, code=code, display=display)]),
            entry=[Reference(reference=ref) for ref in refs]
        )

    if allergy_refs:
        sections.append(build_section("Allergies", "48765-2", "Allergies and adverse reactions", allergy_refs))
    if condition_refs:
        sections.append(build_section("Problems", "11450-4", "Problem List", condition_refs))
    if medication_refs:
        sections.append(build_section("Medications", "10160-0", "History of Medication Use", medication_refs))
    if immunization_refs:
        sections.append(build_section("Immunizations", "11369-6", "History of immunizations", immunization_refs))

    composition = Composition(
        id=composition_id,
        status="final",
        type=CodeableConcept(coding=[Coding(
            system=LOINC_SYSTEM,
            code="60591-5",
            display="Patient Summary"
        )]),
        subject=Reference(reference=f"urn:uuid:{patient_id}"),
        date=str(datetime.datetime.now(datetime.timezone.utc).isoformat()),
        title="PS-CA Patient Summary",
        author=[Reference(reference=f"urn:uuid:{ORGANIZATION_ID}", display=ORGANIZATION_NAME)],
        custodian=Reference(reference=f"urn:uuid:{ORGANIZATION_ID}", display=ORGANIZATION_NAME),
        section=sections
    )

    return composition_id, json.loads(composition.json(by_alias=True))
