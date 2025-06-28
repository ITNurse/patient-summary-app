import pandas as pd
from config import PATIENT_CSV, CONDITION_CSV, MEDICATION_CSV, ALLERGY_CSV, IMMUNIZATION_CSV


def load_csv_data():
    """
    Load all CSV data files.
    
    Returns:
        tuple: (patients_df, conditions_df, medications_df, allergies_df)
    """
    try:
        patients_df = pd.read_csv(PATIENT_CSV)
        conditions_df = pd.read_csv(CONDITION_CSV)
        medications_df = pd.read_csv(MEDICATION_CSV)
        allergies_df = pd.read_csv(ALLERGY_CSV)
        immunizations_df = pd.read_csv(IMMUNIZATION_CSV)
        
        return patients_df, conditions_df, medications_df, allergies_df, immunizations_df
    
    except FileNotFoundError as e:
        print(f"❌ Error loading CSV file: {e}")
        raise
    except Exception as e:
        print(f"❌ Error reading CSV data: {e}")
        raise


def validate_data(patients_df, conditions_df, medications_df, allergies_df, immunizations_df):
    """
    Basic validation of loaded data.
    
    Args:
        patients_df: Patients DataFrame
        conditions_df: Conditions DataFrame
        medications_df: Medications DataFrame
        allergies_df: Allergies DataFrame
        immunizations_df: Immunizations DataFrame

    Returns:
        bool: True if data appears valid
    """
    required_patient_cols = ["identifier", "name.family", "name.given", "gender", "birthDate"]
    required_condition_cols = ["patient.identifier", "condition.code", "condition.display"]
    required_medication_cols = ["patient.identifier", "medication.code", "medication.display"]
    required_allergy_cols = ["patient.identifier", "substance.code", "substance.display", "criticality", "severity"]
    required_immunization_cols = [
    "patient.identifier", "vaccine.code", "vaccine.display",
    "date", "site.code", "site.display", "route.code", "route.system", "route.display"]


    
    # Check required columns exist
    if not all(col in patients_df.columns for col in required_patient_cols):
        print("❌ Missing required columns in patients CSV")
        return False
    
    if not all(col in conditions_df.columns for col in required_condition_cols):
        print("❌ Missing required columns in conditions CSV")
        return False
    
    if not all(col in medications_df.columns for col in required_medication_cols):
        print("❌ Missing required columns in medications CSV")
        return False
    
    if not all(col in allergies_df.columns for col in required_allergy_cols):
        print("❌ Missing required columns in allergies CSV")
        return False
    
    if not all(col in immunizations_df.columns for col in required_immunization_cols):
        print("❌ Missing required columns in immunizations CSV")
        return False

    # Check for empty DataFrames
    if patients_df.empty:
        print("❌ Patients CSV is empty")
        return False
    
    print(f"✅ Data import validation passed")
    print(f"   - {len(patients_df)} patients")
    print(f"   - {len(conditions_df)} conditions")
    print(f"   - {len(medications_df)} medications")
    print(f"   - {len(allergies_df)} allergies")
    print(f"   - {len(immunizations_df)} allergies")
    
    return True