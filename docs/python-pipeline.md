# How the Python App Works

This Python application takes structured CSV data and transforms it into HL7 FHIR Patient Summary Bundles conforming to the Pan-Canadian Patient Summary (PS-CA) Implementation Guide (https://simplifier.net/PS-CA-R1/~introduction)

## Overview

The pipeline performs the following major tasks:

1. Reads data from multiple CSV files (one per resource type)
2. Transforms each row into a FHIR-compliant resource using Python
3. Groups the resources into a FHIR Document Bundle (type: `document`)
4. Saves the bundle to the `document_bundles/` folder
5. Posts the bundle to a running FHIR server using a `transaction` request
6. Saves validation results, including response JSON and summary logs

---

## CSV Input Files

Each CSV corresponds to a specific FHIR resource type:
- `PS-CA_Patient.csv` → `Patient`
- `PS-CA_AllergyIntolerance.csv` → `AllergyIntolerance`
- `PS-CA_Condition.csv` → `Condition`
- `PS-CA_Immunization.csv` → `Immunization`
- `PS-CA_Medication.csv` → `MedicationStatement`

The files contain **synthetic data** aligned with required and example fields in the PS-CA guide. Where applicable, the fields contain values from the recommended value sets identified in the PS-CA implementation guide. 

---

## Resource Creation

Each resource is constructed using a dedicated Python class/module inside the `resources/` folder. For example:
- `resources/patient.py` creates `Patient` resources
- `resources/allergy.py` creates `AllergyIntolerance` resources
- `resources/condition.py` creates `Condition` resources
- `resources/immunization.py` creates `Immunization` resources
- `resources/medication.py` creates `Medication` resources

These use the `fhir.resources` Python package version 6.4.0 to generate properly structured JSON. Note that this version is required as it is the latest FHIR R4-compatible version. Also, it is necessary to downgrade to version 1.10.x of the pydantic library as the current version of fhir.resources is not compatible with pyndantic versions 2.0.0 and greater. The fhir-core library should also not be installed.

---

## Bundle Assembly

Resources are grouped into a single `Bundle` of type `document`, with:
- A `Composition` resource as the first entry (per FHIR requirements)
- Each clinical resource listed as a section in the `Composition`
- A unique identifier and timestamp for each bundle

The bundle is saved as:
```
document_bundles/bundle_<PatientID>.json
```

---

## Server Posting

The script sends the bundle to a running **HAPI FHIR server** using a `POST` request with:
- `Content-Type: application/fhir+json`
- Bundle payload as JSON

The server endpoint is typically:
```
http://localhost:8080/fhir
```

Transaction bundles create/update all included resources atomically.

---

## Validation Output

For each bundle:
- A raw server response is saved to `validation_<PatientID>.json`
- Any validation issues are tabulated and saved in `validation_issues_table.xlsx`
- A summary sheet aggregates key outcomes across all patients

---

## Running the Pipeline

Run the main script:

```bash
python main.py
```

Ensure your virtual environment is activated and the HAPI FHIR server is running first.

---


