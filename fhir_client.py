import requests
from config import FHIR_SERVER_URL, FHIR_HEADERS


def upload_bundle_to_server(bundle):
    """
    Upload a FHIR bundle to the server.
    
    Args:
        bundle: FHIR bundle to upload
        
    Returns:
        tuple: (success: bool, status_code: int, response_text: str)
    """
    try:
        response = requests.post(FHIR_SERVER_URL, headers=FHIR_HEADERS, json=bundle)
        
        success = response.status_code in [200, 201]
        return success, response.status_code, response.text
        
    except requests.exceptions.RequestException as e:
        return False, 0, str(e)


def test_server_connection():
    """
    Test connection to FHIR server.
    
    Returns:
        bool: True if server is reachable
    """
    try:
        response = requests.get(f"{FHIR_SERVER_URL}/metadata", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False