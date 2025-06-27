from config import ORGANIZATION_ID, ORGANIZATION_NAME


def create_organization_resource():
    """
    Create a FHIR Organization resource.
    
    Returns:
        tuple: (organization_id, organization_resource)
    """
    organization_resource = {
        "resourceType": "Organization",
        "id": ORGANIZATION_ID,
        "name": ORGANIZATION_NAME
    }
    
    return ORGANIZATION_ID, organization_resource