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
<style>
  table, th, td {
    border: 1px solid #ccc;
    border-collapse: collapse;
  }
  th, td {
    padding: 6px;
    text-align: left;       /* horizontal alignment */
    vertical-align: top;    /* vertical alignment */
  }
</style>
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
      <td><code>reference</code></td>
      <td>Required</td>
      <td>A reference to the patient resource</td>
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
      <td><code>Patient.name</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td>Used <code>patient.name.family</code> and <code>patient.name.given</code></td>
    </tr>
    <tr>
      <td><code>Patient.birthDate</code></td>
      <td><code>date</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.gender</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>Required Binding: <a href="http://hl7.org/fhir/administrative-gender">AdministrativeGender</a><br>Allowed: <code>male</code>, <code>female</code>, <code>other</code>, <code>unknown</code></td>
    </tr>
    <tr>
      <td><code>Patient.contact.telecom.system</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>Required Binding: <a href="http://hl7.org/fhir/contact-point-system">ContactPointSystem</a><br>Allowed: <code>phone</code>, <code>fax</code>, <code>email</code>, <code>pager</code>, <code>url</code>, <code>sms</code>, <code>other</code></td>
    </tr>
    <tr>
      <td><code>Patient.contact.telecom.value</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.contact.address.city</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.contact.address.line</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.contact.address.state</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.contact.address.postalCode</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.contact.address.country</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.photo.contentType</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>Binding: <em>Mime Types</em> value set (Required Binding)</td>
    </tr>
    <tr>
      <td><code>Patient.photo.data</code></td>
      <td><code>base64Binary</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.identifier.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Patient.identifier.value</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
  </tbody>
</table>


## Condition

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
      <td><code>Condition.subject.reference</code></td>
      <td><code>reference</code></td>
      <td>Required</td>
      <td>A reference to the patient resource</td>
    </tr>
    <tr>
      <td><code>Condition.code</code></td>
      <td><code>date</code></td>
      <td>Required</td>
      <td>
        Preferred Binding: Clinical Finding Code<br>
        This subset was defined using the intensional definition of <code>404684003 | Clinical finding (finding)</code> against the substrate SNOMED CT Canadian Edition.<br>
        This resource is an informative value set; a normative subset containing the expanded values can be found on Canada Health Infoway's Terminology Gateway.<br>
        <a href="https://fhir.infoway-inforoute.ca/ValueSet/clinicalfindingcode">https://fhir.infoway-inforoute.ca/ValueSet/clinicalfindingcode</a>
      </td>
    </tr>
    <tr>
      <td><code>Condition.code.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Condition.code.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>Condition.code.coding.display</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
  </tbody>
</table>


## Medication
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
      <td><code>patient.identifier</code></td>
      <td><code>reference</code></td>
      <td>Required</td>
      <td>A reference to the patient resource</td>
    </tr>
    <tr>
      <td><code>medication.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>medication.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td><code>PrescriptionMedicinalProduct</code></td>
    </tr>
    <tr>
      <td><code>medication.coding.display</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>status.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>status.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td><code>Medication Status Codes</code></td>
    </tr>
    <tr>
      <td><code>effective.date</code></td>
      <td><code>date</code></td>
      <td>Required</td>
      <td></td>
    </tr>
  </tbody>
</table>

## Allergy Intolerance
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
      <td><code>patient.identifier</code></td>
      <td><code>reference</code></td>
      <td>Required</td>
      <td>A reference to the patient resource</td>
    </tr>
    <tr>
      <td><code>substance.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td>SNOMED CT CA</td>
    </tr>
    <tr>
      <td><code>substance.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td>PharmaceuticalBiologicProductAndSubstanceCode</td>
    </tr>
    <tr>
      <td><code>substance.coding.display</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>reaction.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>SNOMED CT CA</td>
    </tr>
    <tr>
      <td><code>reaction.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>ClinicalFindingCode</td>
    </tr>
    <tr>
      <td><code>reaction.coding.display</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>clinicalStatus.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>clinicalStatus.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>AllergyIntoleranceClinicalStatusCodes</td>
    </tr>
    <tr>
      <td><code>verificationStatus.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>verificationStatus.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>AllergyIntoleranceVerificationStatusCodes</td>
    </tr>
    <tr>
      <td><code>criticality.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>criticality.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>AllergyIntoleranceCriticality</td>
    </tr>
    <tr>
      <td><code>severity.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>severity.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td>AllergyIntoleranceSeverity</td>
    </tr>
  </tbody>
</table>


## Immunization
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
      <td><code>patient.identifier</code></td>
      <td><code>reference</code></td>
      <td>Required</td>
      <td>A reference to the patient resource</td>
    </tr>
    <tr>
      <td><code>occurrence.date</code></td>
      <td><code>date</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>status.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>status.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td><b>Binding Strength:</b>Requried <br> <b>Value Set:</b> ImmunizationStatusCodes <br> https://fhir.infoway-inforoute.ca/ValueSet/immunizationstatuscodes</td>
    </tr>
    <tr>
      <td><code>status.coding.display</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>vaccine.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Required</td>
      <td>SNOMED CT CA</td>
    </tr>
    <tr>
      <td><code>vaccine.coding.code</code></td>
      <td><code>code</code></td>
      <td>Required</td>
      <td><b>Binding Strength:</b> Preferred <br> <b>Value Set:</b> VaccineAdministeredTradeNameCode <br> https://fhir.infoway-inforoute.ca/ValueSet/vaccineadministeredtradenamecode</td>
    </tr>
    <tr>
      <td><code>vaccine.coding.display</code></td>
      <td><code>string</code></td>
      <td>Required</td>
      <td></td>
    </tr>
    <tr>
      <td><code>site.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>HL7</td>
    </tr>
    <tr>
      <td><code>site.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td><b>Binding Strength:</b> Example <br> <b>Value Set:</b> CodesForImmunizationSiteOfAdministration <br> http://hl7.org/fhir/ValueSet/immunization-site </td>
    </tr>
    <tr>
      <td><code>site.coding.display</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
    <tr>
      <td><code>route.coding.system</code></td>
      <td><code>uri</code></td>
      <td>Optional</td>
      <td>SNOMED CT CA</td>
    </tr>
    <tr>
      <td><code>route.coding.code</code></td>
      <td><code>code</code></td>
      <td>Optional</td>
      <td><b>Binding Strength:</b> Preferred <br> <b>Value Set:</b> ImmunizationRouteOfAdministrationCode <br> https://fhir.infoway-inforoute.ca/ValueSet/immunizationrouteofadministrationcode </td>
    </tr>
    <tr>
      <td><code>route.coding.display</code></td>
      <td><code>string</code></td>
      <td>Optional</td>
      <td></td>
    </tr>
  </tbody>
</table>
