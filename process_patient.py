# Import resource modules
from resources.patient import create_patient_resource
from resources.organization import create_organization_resource
from resources.condition import create_condition_resources, get_condition_references
from resources.medication import create_medication_resources, get_medication_references
from resources.allergy import create_allergy_resources, get_allergy_references
from resources.composition import create_composition_resource
from resources.immunization import create_immunization_resources, get_immunization_references
from bundle_builder import create_transaction_bundle, create_document_bundle


def process_patient(patient_row, organization_df, compositions_df, conditions_df, medications_df, allergies_df, immunizations_df):
    """
    Process a single patient and create all associated resources.
    
    Args:
        patient_row: Patient data row
        compositions_df: Composition DataFrame
        conditions_df: Conditions DataFrame
        medications_df: Medications DataFrame
        allergies_df: Allergies DataFrame
        immunizations_df: Immunizations DataFrame
        
    Returns:
        tuple: (transaction_bundle, document_bundle, hcn)
    """
    
    hcn = patient_row["identifier"]
    
    # Step 1: Create patient resource
    patient_id, patient_resource = create_patient_resource(patient_row)
    print(f"-- Patient Resource Created: {patient_id}")

    # Step 2: Create organization resource
    org_id, org_resource = create_organization_resource(organization_df)
    
    # Step 3: Create condition resources
    num_conditions, condition_entries = create_condition_resources(conditions_df, hcn, patient_id)
    print(f"--- {num_conditions} Condition Resource(s) Created")

    # Step 4: Create medication resources
    num_medications, medication_entries = create_medication_resources(medications_df, hcn, patient_id)
    print(f"--- {num_medications} Medication Resource(s) Created")

    # Step 5: Create allergy-intolerance resources
    num_allergies, allergy_entries = create_allergy_resources(allergies_df, hcn, patient_id)
    print(f"--- {num_allergies} Allergy-Intolerance Resource(s) Created")

    # Step 6: Create immunization resources
    num_immunizations, immunization_entries = create_immunization_resources(immunizations_df, hcn, patient_id)
    print(f"--- {num_immunizations} Immunization Resource(s) Created")

    # Step 7: Get references for composition
    condition_refs = get_condition_references(condition_entries)
    medication_refs = get_medication_references(medication_entries)
    allergy_refs = get_allergy_references(allergy_entries)
    immunization_refs = get_immunization_references(immunization_entries)

    # Lookup the correct composition metadata row for this patient
    composition_row = compositions_df[compositions_df["patient.identifier"] == hcn].iloc[0]

    # Step 8: Create composition resource
    composition_id, composition_resource = create_composition_resource(
        org_id, org_resource["name"], patient_id, allergy_refs, condition_refs, medication_refs, 
        immunization_refs, composition_row
    )
    
    # Step 9 Create transaction bundle
    transaction_bundle = create_transaction_bundle(
        composition_id, patient_id, patient_resource, org_id, org_resource, composition_resource,
        allergy_entries, condition_entries, medication_entries, immunization_entries
    )
    
    #Step 10: Create document bundle
    document_bundle = create_document_bundle(
        composition_id, patient_id, patient_resource, org_id, org_resource, composition_resource,
        allergy_entries, condition_entries, medication_entries, immunization_entries
    )
    
    return transaction_bundle, document_bundle, hcn, composition_resource