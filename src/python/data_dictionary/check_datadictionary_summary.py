import pandas as pd

# Path to the processed clinical registry
csv_path = 'clinical_registry_master.csv'

try:
    df = pd.read_csv(csv_path)

    # Summarize shape
    rows, cols = df.shape
    print(f"Shape of '{csv_path}': {rows} rows, {cols} columns")

    # Summarize missing data (NaN counts)
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0] # Only show columns with missing data

    if not missing_data.empty:
        print("\nMissing Data (NaN counts per column):")
        print(missing_data)
    else:
        print("\nNo missing data (NaN values) found in any column.")

except FileNotFoundError:
    print(f"Error: File not found at {csv_path}")
except Exception as e:
    print(f"An error occurred: {e}")
