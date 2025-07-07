# Using Power Query and Power BI
The Microsoft Power BI desktop application (with built-in Power Query) was used to access the PS-CA patient summaries from the HAPI FHIR server, unpack the .json into tabular format, and display the data in a visual way. 

## Web Connector vs FHIR Connector

## Unpacking json to tabular format
The m code used in Power Query to connect to each FHIR endpoint and unpack the json data into tabular format is below.
### Patients
```bash
let
    // Step 1: Load JSON from FHIR Patient endpoint
    Source = Json.Document(Web.Contents("http://localhost:8080/fhir/Patient?_count=50&_summary=false")),
    PatientEntries = Source[entry],

    // Step 2: Convert list to table and expand resource details
    PatientList = Table.FromList(PatientEntries, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedEntry = Table.ExpandRecordColumn(PatientList, "Column1", {"fullUrl", "resource"}, {"FullUrl", "Resource"}),
    ExpandedResource = Table.ExpandRecordColumn(ExpandedEntry, "Resource", {"id", "gender", "birthDate", "identifier", "name", "telecom", "address", "photo"}, {"ID", "Gender", "BirthDate", "Identifier", "Name", "Telecom", "Address", "Photo"}),
    ChangedIDType = Table.TransformColumnTypes(ExpandedResource,{{"ID", type text}}),

    // Step 3: Extract and format patient name fields
    FirstNameOnly = Table.TransformColumns(ChangedIDType, {{"Name", each if List.IsEmpty(_) then null else _{0}}}),
    ExpandedName = Table.ExpandRecordColumn(FirstNameOnly, "Name", {"given", "family"}, {"GivenNames", "FamilyName"}),
    CombinedGivenNames = Table.TransformColumns(ExpandedName, {{"GivenNames", each Text.Combine(_, " "), type text}}),

    // Step 4: Parse birth date and calculate age
    ParsedBirthDate = Table.TransformColumns(CombinedGivenNames, {{"BirthDate", each try Date.From(_) otherwise null, type nullable date}}),
    AddedAge = Table.AddColumn(ParsedBirthDate, "Age", each if [BirthDate] <> null then Number.RoundDown(Duration.Days(Date.From(DateTime.LocalNow()) - [BirthDate]) / 365) else null, Int64.Type),

    // Step 5: Extract Health Card Number (first identifier only)
    FirstIdentifierOnly = Table.TransformColumns(AddedAge, {{"Identifier", each if List.IsEmpty(_) then null else _{0}}}),
    ExpandedIdentifier = Table.ExpandRecordColumn(FirstIdentifierOnly, "Identifier", {"value"}, {"HealthCardNumber"}),

    // Step 6: Expand address fields
    ExpandedAddressList = Table.ExpandListColumn(ExpandedIdentifier, "Address"),
    ExpandedAddressFields = Table.ExpandRecordColumn(ExpandedAddressList, "Address", {"line", "city", "state", "postalCode", "country"}, {"AddressLine1", "City", "State", "PostalCode", "Country"}),
    CombinedAddressLine = Table.TransformColumns(ExpandedAddressFields, {"AddressLine1", each Text.Combine(List.Transform(_, Text.From), ","), type text}),

    // Step 7: Expand telecom fields and pivot by system type (e.g. phone, email)
    ExpandedTelecomList = Table.ExpandListColumn(CombinedAddressLine, "Telecom"),
    ExpandedTelecomFields = Table.ExpandRecordColumn(ExpandedTelecomList, "Telecom", {"system", "value"}),
    PivotedTelecom = Table.Pivot(
        ExpandedTelecomFields,
        List.Distinct(ExpandedTelecomFields[system]),
        "system",
        "value"
    ),
    RenamedTelecomColumns = Table.RenameColumns(PivotedTelecom,{{"phone", "Phone"}, {"email", "Email"}}),

    // Step 8: Expand photo and construct base64 image URI string
    ExpandedPhotoList = Table.ExpandListColumn(RenamedTelecomColumns, "Photo"),
    ExpandedPhotoFields = Table.ExpandRecordColumn(ExpandedPhotoList, "Photo", {"contentType", "data"}, {"Photo.contentType", "Photo.data"}),
    ConstructedPhotoURI = Table.AddColumn(ExpandedPhotoFields, "Photo", each Text.Combine({"data:", [Photo.contentType], ";base64, ", [Photo.data]}, ""))
in
    ConstructedPhotoURI

```
### Conditions
### Immunizations
### Medications
```bash
let
    // Step 1: Retrieve MedicationStatement resources from the local FHIR server
    Source = Json.Document(Web.Contents("http://localhost:8080/fhir/MedicationStatement?_count=100&_summary=false")),
    MedicationEntries = Source[entry],

    // Step 2: Convert the list of entries into a table and expand the main columns
    ToTable = Table.FromList(MedicationEntries, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedEntry = Table.ExpandRecordColumn(ToTable, "Column1", {"fullUrl", "resource", "search"}, {"FullUrl", "Resource", "Search"}),

    // Step 3: Expand fields from the resource object
    ExpandedResource = Table.ExpandRecordColumn(ExpandedEntry, "Resource", {"resourceType", "id", "meta", "status", "medicationCodeableConcept", "subject"}, {"ResourceType", "ID", "Meta", "Status", "MedicationCodeableConcept", "Subject"}),

    // Step 4: Expand metadata to access versioning and timestamp info
    ExpandedMeta = Table.ExpandRecordColumn(ExpandedResource, "Meta", {"versionId", "lastUpdated", "source"}, {"VersionId", "LastUpdated", "Source"}),

    // Step 5: Expand the medication codeable concept to access codings
    ExpandedMedicationConcept = Table.ExpandRecordColumn(ExpandedMeta, "MedicationCodeableConcept", {"coding"}, {"Coding"}),

    // Step 6: Unpack the list of codings into individual rows (in case of multiple codings per medication)
    ExpandedCodingList = Table.ExpandListColumn(ExpandedMedicationConcept, "Coding"),

    // Step 7: Expand each coding object to get system, code, and display text
    ExpandedCoding = Table.ExpandRecordColumn(ExpandedCodingList, "Coding", {"system", "code", "display"}, {"System", "MedicationCode", "MedicationDisplay"}),

    // Step 8: Extract patient ID from subject.reference (e.g. "Patient/123" becomes "123")
    ExpandedSubject = Table.ExpandRecordColumn(ExpandedCoding, "Subject", {"reference"}, {"PatientReference"}),
    ExtractedPatientID = Table.ReplaceValue(ExpandedSubject, "Patient/", "", Replacer.ReplaceText, {"PatientReference"}),

    // Step 9: Rename columns for clarity
    RenamedPatientID = Table.RenameColumns(ExtractedPatientID, {{"PatientReference", "PatientID"}}),

    // Step 10: Keep only the necessary columns
    SelectedColumns = Table.SelectColumns(RenamedPatientID, {"ID", "PatientID", "MedicationCode", "MedicationDisplay", "Status", "System"}),

    // Step 11: Final column renaming for clarity
    FinalOutput = Table.RenameColumns(SelectedColumns, {{"ID", "MedicationStatementID"}})
in
    FinalOutput
```

### Allergies
```bash
let
    // Step 1: Load JSON data from the FHIR AllergyIntolerance endpoint
    Source = Json.Document(Web.Contents("http://localhost:8080/fhir/AllergyIntolerance?_count=100")),
    AllergyEntries = Source[entry],

    // Step 2: Convert list of entries into a table and expand top-level entry fields
    AllergyList = Table.FromList(AllergyEntries, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    ExpandedEntry = Table.ExpandRecordColumn(AllergyList, "Column1", {"fullUrl", "resource"}, {"FullUrl", "Resource"}),

    // Step 3: Expand key fields from the resource
    ExpandedResource = Table.ExpandRecordColumn(ExpandedEntry, "Resource", {"id", "patient", "code", "reaction", "criticality"}, {"ID", "Patient", "Substance", "Reaction", "Criticality"}),

    // Step 4: Extract patient ID from the Patient reference (e.g. "Patient/12345" -> "12345")
    ExtractedPatientRef = Table.AddColumn(ExpandedResource, "PatientID", each Text.AfterDelimiter([Patient][reference], "/")),

    // Step 5: Expand allergen substance coding to get code and display
    SubstanceCoding = Table.ExpandRecordColumn(ExtractedPatientRef, "Substance", {"coding"}, {"Coding"}),
    ExpandedCodingList = Table.ExpandListColumn(SubstanceCoding, "Coding"),
    ExpandedCoding = Table.ExpandRecordColumn(ExpandedCodingList, "Coding", {"code", "display"}, {"AllergenCode", "AllergenDisplay"}),

    // Step 6: Expand the first reaction and its manifestations (if any)
    FirstReactionOnly = Table.TransformColumns(ExpandedCoding, {{"Reaction", each if List.IsEmpty(_) then null else _{0}}}),
    ExpandedReaction = Table.ExpandRecordColumn(FirstReactionOnly, "Reaction", {"manifestation", "severity"}, {"ManifestationList", "Severity"}),

    // Step 7: Expand first manifestation coding to get reaction display text
    FirstManifestation = Table.TransformColumns(ExpandedReaction, {{"ManifestationList", each if List.IsEmpty(_) then null else _{0}}}),
    ExpandedManifestation = Table.ExpandRecordColumn(FirstManifestation, "ManifestationList", {"coding"}, {"ManifestationCoding"}),
    ManifestationCodeList = Table.ExpandListColumn(ExpandedManifestation, "ManifestationCoding"),
    ExpandedManifestationCode = Table.ExpandRecordColumn(ManifestationCodeList, "ManifestationCoding", {"code", "display"}, {"ReactionCode", "ReactionDisplay"}),

    // Step 8: Keep only final columns of interest
    FinalOutput = Table.SelectColumns(ExpandedManifestationCode, {"ID", "PatientID", "AllergenCode", "AllergenDisplay", "ReactionCode", "ReactionDisplay", "Severity", "Criticality"})
in
    FinalOutput
```

## Relating tables

## Data visualization

## Publish to Power BI Service