import uuid
import os
import base64
import json
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.address import Address
from fhir.resources.attachment import Attachment
from resources.profile_utils import add_meta_profile
from config import HEALTH_CARD_SYSTEM


def encode_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    return None


def create_patient_resource(patient_row):
    """
    Create a FHIR Patient resource from patient CSV data using fhir.resources.

    Args:
        patient_row: Pandas Series containing patient data

    Returns:
        tuple: (patient_id, patient_resource_dict)
    """
    patient_id = str(uuid.uuid4())

    # Handle optional photo
    photo_column = patient_row.get("profile.photo", "")
    photo_path = os.path.join("data", photo_column) if photo_column else ""
    photo_data = encode_image_base64(photo_path)
    photo = [Attachment(
        contentType="image/jpeg",
        data=photo_data
    )] if photo_data else None
    birth_date_raw = patient_row["birthDate"]
    birth_date = birth_date_raw.isoformat() if hasattr(birth_date_raw, "isoformat") else str(birth_date_raw) 

    patient = Patient(
        id=patient_id,
        identifier=[Identifier(
            system=HEALTH_CARD_SYSTEM,
            value=patient_row["identifier"]
        )],
        name=[HumanName(
            family=patient_row["name.family"],
            given=[patient_row["name.given"]]
        )],
        gender=patient_row["gender"].lower(),
        birthDate=birth_date,
        telecom=[
            ContactPoint(
                system="phone",
                value=patient_row["PhoneNumber"],
                use="home"
            ),
            ContactPoint(
                system="email",
                value=patient_row["Email"],
                use="home"
            )
        ],
        address=[Address(
            line=[patient_row["AddressLine"]],
            city=patient_row["City"],
            state=patient_row["Province"],
            postalCode=patient_row["PostalCode"],
            country=patient_row["Country"]
        )],
        photo=photo
    )

    return patient_id, add_meta_profile(json.loads(patient.json(by_alias=True)), "Patient")
