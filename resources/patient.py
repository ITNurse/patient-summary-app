import uuid
from config import HEALTH_CARD_SYSTEM
import os
import base64

def encode_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return None

def create_patient_resource(patient_row):
    """
    Create a FHIR Patient resource from patient CSV data.
    
    Args:
        patient_row: Pandas Series containing patient data
        
    Returns:
        tuple: (patient_id, patient_resource)
    """
    patient_id = str(uuid.uuid4())

    # Handle photo
    photo_data = None
    photo_field = []
    photo_column = patient_row.get("profile.photo", "")
    photo_path = os.path.join("data", photo_column) if photo_column else ""
    photo_data = encode_image_base64(photo_path)
    if photo_data:
        photo_field = [{
            "contentType": "image/jpeg",
            "data": photo_data
        }]

    patient_resource = {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [{
            "system": HEALTH_CARD_SYSTEM,
            "value": patient_row["identifier"]
        }],
        "name": [{
            "family": patient_row["name.family"],
            "given": [patient_row["name.given"]]
        }],
        "gender": patient_row["gender"].lower(),
        "birthDate": patient_row["birthDate"],
        "telecom": [
            {
                "system": "phone",
                "value": patient_row["PhoneNumber"],
                "use": "home"
            },
            {
                "system": "email",
                "value": patient_row["Email"],
                "use": "home"
            }
        ],
        "address": [{
            "line": [patient_row["AddressLine"]],
            "city": patient_row["City"],
            "state": patient_row["Province"],
            "postalCode": patient_row["PostalCode"],
            "country": patient_row["Country"]
        }],
        "photo": photo_field
    }

    return patient_id, patient_resource
