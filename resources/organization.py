from fhir.resources.organization import Organization
from config import ORGANIZATION_ID, ORGANIZATION_NAME


def create_organization_resource():
    """
    Create a FHIR Organization resource using fhir.resources.

    Returns:
        tuple: (organization_id, organization_resource_dict)
    """
    organization = Organization(
        id=ORGANIZATION_ID,
        name=ORGANIZATION_NAME
    )

    return ORGANIZATION_ID, organization.dict(by_alias=True)