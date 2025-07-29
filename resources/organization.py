from fhir.resources.organization import Organization
import uuid

def create_organization_resource(organization_df):
    """
    Create a FHIR Organization resource using the first row of organization_df.

    Args:
        organization_df (pd.DataFrame): DataFrame containing organization.name and organization.type

    Returns:
        tuple: (organization_id, organization_resource_dict)
    """
    # Use the first row of the DataFrame
    org_row = organization_df.iloc[0]

    organization_id = str(uuid.uuid4())
    organization = Organization(
        id=organization_id,
        name=org_row["organization.name"]
    )

    return organization_id, organization.dict(by_alias=True)
