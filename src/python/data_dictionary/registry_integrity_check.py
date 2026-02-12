import pandas as pd
import sys

# Simplified integrity check for public framework
# This ensures required columns are present in the master registry

required_columns = [
    'original_variable_name',
    'generalized_variable_name',
    'datatype',
    'levels'
]

def check_integrity(file_path='clinical_registry_master.csv'):
    try:
        df = pd.read_csv(file_path, nrows=0)
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            print(f"SCHEMA ERROR: Missing columns: {', '.join(missing)}")
            return False
        
        print("SCHEMA OK: All required columns present.")
        return True
    except FileNotFoundError:
        print(f"ERROR: {file_path} not found.")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    if check_integrity():
        sys.exit(0)
    else:
        sys.exit(1)
