import os

# ============================
# File Paths Configuration
# ============================
BASE_DIR = r"C:\Python\Wellness_Way"

# Input CSV files
COMPOSITION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Composition.csv")
PATIENT_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Patient.csv")
CONDITION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Condition.csv")
MEDICATION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Medication.csv")
ALLERGY_CSV = os.path.join(BASE_DIR, "data", "PS-CA_AllergyIntolerance.csv")
IMMUNIZATION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Immunization.csv")
ORGANIZATION_CSV = os.path.join(BASE_DIR, "data", "PS-CA_Organization.csv")

# Output paths
OUTPUT_DIR = os.path.join(BASE_DIR, "document_bundles")
LOG_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "upload_log.csv")

# ============================
# FHIR Server Configuration
# ============================
FHIR_SERVER_URL = "http://localhost:8080/fhir"
FHIR_HEADERS = {"Content-Type": "application/fhir+json"}

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)