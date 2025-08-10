# CSV File Design Decisions
This section identifies the rationale behind why the csv files used as the base patient data for the patient summaries were created as they were.

## PS-CA Implementation Guide
The Trial Implementation version (v1.0.0 TI) of the [PS-CA implementation guide](https://simplifier.net/guide/pan-canadian-patient-summary-v1.0-ti-fhir-implementation-guide?version=1.0.0) and the associated resource definitions on simplifier.net were used as the basis for all design decisions. The PS-CA is closely aligned with the [International Patient Summary (IPS) Implementation Guide](https://hl7.org/fhir/uv/ips/), which indicates that every IPS must include the following sections: Header (subject, author, attester, custodian), Medication Summary, Allergies & Intolerances, and Problem List.

![Screenshot of IPS composition showing required sections as: Header (subject, author, attester, custodian), Medication Summary, Allergies & Intolerances, and Problem List](images/ips-composition.png)
(Image Source: https://build.fhir.org/ig/HL7/fhir-ips/Structure-of-the-International-Patient-Summary.html)

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

## Special Note: 
Because the patient data is created as CSV files, any values within those files that contain commas (i.e. a condition display name) will cause issues. To get around this, all text fields should be wrapped in double quotes.

## Organization

| Field                                                   | Type              | Requirement | Notes                                                                                                                                               |
|---------------------------------------------------------|-------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `Organization.name`                                     | `string`          | Required    | Name used for the organization                                                                                                                      |
| `CompositionPSCA.status`                                | `CodeableConcept` | Optional    | Example Binding: [OrganizationType](http://terminology.hl7.org/CodeSystem/organization-type)                                                        |



## Composition

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Type</th>
      <th>Requirement</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>CompositionPSCA.subject.reference</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td>Reference to the patient</td>
    </tr>
    <tr>
      <td><code>CompositionPSCA.status</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td>Required Binding: <a href="http://hl7.org/fhir/composition-status">CompositionStatus</a><br>Allowed: <code>preliminary</code>, <code>final</code>, <code>amended</code>, <code>entered-in-error</code></td>
    </tr>
    <tr>
      <td><code>CompositionPSCA.type</code></td>
      <td><code>CodeableConcept</code></td>
      <td>Required</td>
      <td>Preferred Binding: <code>FHIRDocumentTypeCodes</code><br>Includes codes from LOINC (where SCALE_TYP = "Doc")</td>
    </tr>
    <tr>
      <td><code>Composition.date</code></td>
      <td><code>dateTime</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>CompositionPSCA.author</code></td>
      <td><code>Reference</code></td>
      <td>Required</td>
      <td>Must reference: <code>PractitionerProfile</code>, <code>PractitionerRoleProfile</code>, <code>Device</code>, <code>PatientPSCA</code>, <code>RelatedPerson</code>, or <code>OrganizationProfile</code></td>
    </tr>
    <tr>
      <td><code>CompositionPSCA.title</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>CompositionPSCA.section</code></td>
      <td><code>BackboneElement</code></td>
      <td>Required</td>
      <td>Sections comprising the PSCA</td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionMedications.title</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td>Required if medication section is included</td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionMedications.code</code></td>
      <td><code>CodeableConcept</code></td>
      <td>Required</td>
      <td>Required Binding: <a href="https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879">DocumentSectionCodes</a></td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionAllergies.title</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td>Required if allergy-intolerance section</td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionAllergies.code</code></td>
      <td><code>CodeableConcept</code></td>
      <td>Required</td>
      <td>Required Binding: <a href="https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879">DocumentSectionCodes</a></td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionProblems.title</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Composition.section:sectionProblems.code</code></td>
      <td><code>CodeableConcept</code></td>
      <td>Required</td>
      <td>Required Binding: <a href="https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/2831879">DocumentSectionCodes</a></td>
    </tr>
  </tbody>
</table>


## Patient

| Field                                        | Type           | Requirement  | Notes                                                                                                                                              |
|---------------------------------------------|----------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `Patient.name`                              | `string`       | Required     | Used `patient.name.family` and `patient.name.given`                                                                                                |
| `Patient.birthDate`                         | `date`         | Required     |                                                                                                                                                    |
| `Patient.gender`                            | `code`         | Not required | Required Binding: [AdministrativeGender](http://hl7.org/fhir/administrative-gender) <br> Allowed: `male`, `female`, `other`, `unknown`                 |
| `Patient.contact.telecom.system`            | `code`         | Not required | Required Binding: [ContactPointSystem](http://hl7.org/fhir/contact-point-system) <br> Allowed: `phone`, `fax`, `email`, `pager`, `url`, `sms`, `other`     |
| `Patient.contact.telecom.value`             | `string`       | Not required |                                                                                                                                                    |
| `Patient.contact.address.city`              | `string`       | Not required |                                                                                                                                                    |
| `Patient.contact.address.line`              | `string`       | Not required |                                                                                                                                                    |
| `Patient.contact.address.state`             | `string`       | Not required |                                                                                                                                                    |
| `Patient.contact.address.postalCode`        | `string`       | Not required |                                                                                                                                                    |
| `Patient.contact.address.country`           | `string`       | Not required |                                                                                                                                                    |
| `Patient.photo.contentType`                 | `code`         | Not required | Binding: *Mime Types* value set (Required Binding)                                                                               |
| `Patient.photo.data`                        | `base64Binary` | Not required |                                                                                                                                                    |
| `Patient.identifier.system`                 | `uri`          | Required     |                                                                                                                                                    |
| `Patient.identifier.value`                  | `string`       | Required     |                                                                                                                                                    |

## Condition

| Field                                        | Type           | Requirement  | Notes                                                                                                                                                                            |
|---------------------------------------------|----------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Condition.subject.reference`            | `string`       | Required     | A reference to a location at which the other resource is found  |
| `Condition.code`                         | `date`         | Required     | Preferred Binding: Clinical Finding Code <br>  This subset was defined using the intensional definition of 404684003 &#124; Clinical finding (finding) against the substrate SNOMED CT Canadian Edition. <br> This resource is an informative value set; a normative subset containing the expanded values can be found on Canada Health Infoway's Terminology Gateway. <br> [https://fhir.infoway-inforoute.ca/ValueSet/clinicalfindingcode](https://fhir.infoway-inforoute.ca/ValueSet/clinicalfindingcode) |
| `Condition.code.coding.system`          | `uri`         | Required |                                                                                                                                                                                             |
| `Condition.code.coding.code`            | `code`         | Required |                                                                                                                                                                                             |
| `Condition.code.coding.display`             | `string`       | Required |                                                                                                                                                                                        |


## Medication
[Enter table here]

## Allergy Intolerance
[Enter table here]

## Immunization
[Enter table here]