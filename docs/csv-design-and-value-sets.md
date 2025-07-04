# CSV File Design Decisions
This section identifies the rationale behind why the csv files used as the base patient data for the patient summaries were created as they were.

## PS-CA Implementation Guide
The Trial Implementation version (v1.0.0 TI) of the [PS-CA implementation guide](https://simplifier.net/guide/pan-canadian-patient-summary-v1.0-ti-fhir-implementation-guide?version=1.0.0) and the associated resource definitions on simplifier.net were used as the basis for all design decisions. The PS-CA is closely aligned with the [International Patient Summary (IPS) Implementation Guide](https://hl7.org/fhir/uv/ips/), which indicates that every IPS must include the following sections: Header (subject, authorh, attester, custodian), Medication Summary, Allergies & Intolerances, and Problem List.

![Screenshot of IPS composition showing required sections as: Header (subject, author, attester, custodian), Medication Summary, Allergies & Intolerances, and Problem List](docs/images/patient-summary-viewer-screenshot.jpg)
docs\images\ips-composition.png

Therefore, the following FHIR resources are required for the PS-CA:
- [CompositionPSCA](https://simplifier.net/ps-ca-r1/compositionpsca)
- [PatientPSCA](https://simplifier.net/ps-ca-r1/patientpsca)
- [MedicationStatementPSCA](https://simplifier.net/ps-ca-r1/medicationstatementpsca)
- [AllergyIntolerancePSCA](https://simplifier.net/ps-ca-r1/allergyintolerancepsca)
- [ConditionPSCA](https://simplifier.net/ps-ca-r1/conditionpsca)

All of these resources are grouped together as a [BundlePSCA](https://simplifier.net/ps-ca-r1/bundlepsca) resource.

In an effort to make this project a more well-rounded educational resource, the following two resources were also created:
- [ImmunizationPSCA](https://simplifier.net/ps-ca-r1/immunizationpsca)
- [OrganizationCACore](https://simplifier.net/ca-core/organization-ca-core)

## Composition
### CompositionPSCA Profile Fields and Bindings

| Field                                                   | Type           | Requirement | Notes                                                                                                                                                              |
|---------------------------------------------------------|----------------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CompositionPSCA.subject.reference`                     | `string`       | Required    | A reference to a location at which the other resource is found                                                                                                     |
| `CompositionPSCA.status`                                | `code`         | Required    | Binding: [CompositionStatus](http://hl7.org/fhir/composition-status) (required) <br> Allowed: `preliminary`, `final`, `amended`, `entered-in-error`              |
| `CompositionPSCA.type`                                  | `CodeableConcept` | Required | Binding: `FHIRDocumentTypeCodes (P)` <br> Includes codes from LOINC (where SCALE_TYP = "Doc")                                                                     |
| `Composition.date`                                      | `dateTime`     | Required    |                                                                                                                                                                    |
| `CompositionPSCA.author`                                | `Reference`    | Required    | Must reference: `PractitionerProfile`, `PractitionerRoleProfile`, `Device`, `PatientPSCA`, `RelatedPerson`, or `OrganizationProfile`                              |
| `CompositionPSCA.title`                                 | `string`       | Required    |                                                                                                                                                                    |
| `CompositionPSCA.section`                               | `BackboneElement` | Required | Sections comprising the PSCA                                                                                                                                        |
| `Composition.section:sectionMedications.title`          | `string`       | Required    |                                                                                                                                                                    |
| `Composition.section:sectionMedications.code`           | `CodeableConcept` | Required | Binding: [DocumentSectionCodes](https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879)                                                             |
| `Composition.section:sectionAllergies.title`            | `string`       | Required    |                                                                                                                                                                    |
| `Composition.section:sectionAllergies.code`             | `CodeableConcept` | Required | Binding: [DocumentSectionCodes](https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879)                                                             |
| `Composition.section:sectionProblems.title`             | `string`       | Required    |                                                                                                                                                                    |
| `Composition.section:sectionProblems.code`              | `CodeableConcept` | Required | Binding: [DocumentSectionCodes](https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879)                                                             |


## PS-CA_Patient.csv


## PS-CA_Medication.csv

## PS-CA_Condition.csv

## PS-CA_AllergyIntolerance.csv

## PS-CA_Immunization.csv