# Using Power Query and Power BI
The Microsoft Power BI desktop application (with built-in Power Query) was used to access the PS-CA patient summaries from the HAPI FHIR server, unpack the .json into tabular format, and display the data in a visual way. 

## Web Connector vs FHIR Connector

## Unpacking json to tabular format

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
### Allergies

## Relating tables

## Data visualization

## Publish to Power BI Service