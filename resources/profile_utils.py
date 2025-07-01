def add_meta_profile(resource: dict, resource_type: str) -> dict:
    PSCA_PROFILES = {
        "AllergyIntolerance": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/AllergyIntolerance-ps-ca",
        "Condition": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/Condition-ps-ca",
        "MedicationStatement": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/MedicationStatement-ps-ca",
        "Immunization": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/Immunization-ps-ca",
        "Composition": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/Composition-ps-ca",
        "Patient": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/Patient-ps-ca",
        "Organization": "http://fhir.infoway-inforoute.ca/io/psca/StructureDefinition/Organization-ps-ca"
    }
    if resource_type in PSCA_PROFILES:
        resource.setdefault("meta", {})["profile"] = [PSCA_PROFILES[resource_type]]
    return resource