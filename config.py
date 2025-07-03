import os
import uuid

# ============================
# File Paths Configuration
# ============================
BASE_DIR = r"C:\Python\Wellness_Way"

# Input CSV files
PATIENT_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Patient.csv")
CONDITION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Condition.csv")
MEDICATION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Medication.csv")
ALLERGY_CSV = os.path.join(BASE_DIR, "data", "PS-CA_AllergyIntolerance.csv")
IMMUNIZATION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Immunization.csv")

# Output paths
OUTPUT_DIR = os.path.join(BASE_DIR, "document_bundles")
LOG_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "upload_log.csv")

# ============================
# FHIR Server Configuration
# ============================
FHIR_SERVER_URL = "http://localhost:8080/fhir"
FHIR_HEADERS = {"Content-Type": "application/fhir+json"}

# ============================
# Organization Configuration
# ============================
ORGANIZATION_ID =  str(uuid.uuid4())
ORGANIZATION_NAME = "Wellness Way Hospital"

# ============================
# System URIs
# ============================
HEALTH_CARD_SYSTEM = "http://example.org/healthcardnumber"
SNOMED_SYSTEM = "http://snomed.info/sct"
LOINC_SYSTEM = "http://loinc.org"
MEDICATION_SYSTEM = "http://terminology.hl7.org/CodeSystem/hc-CCDD"
ALLERGY_CLINICAL_SYSTEM = "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical"
ALLERGY_VERIFICATION_SYSTEM = "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)