from fhir.resources.organization import Organization
from resources.profile_utils import add_meta_profile
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

    return ORGANIZATION_ID, add_meta_profile(organization.dict(by_alias=True), "Organization")