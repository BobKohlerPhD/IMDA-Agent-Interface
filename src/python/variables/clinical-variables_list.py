import pandas as pd
import argparse
import os
import difflib

def get_filtered_variable_names(search_keyword=None, search_column='generalized_variable_name', output_column='original_variable_name', fuzzy=True):
    try:
        dict_path = 'clinical_registry_master.csv'
        if not os.path.exists(dict_path):
            dict_path = os.path.join('data', 'processed', 'clinical_registry_master.csv')
            
        df_dict = pd.read_csv(dict_path, low_memory=False)
    except FileNotFoundError:
        return []
    
    if not search_keyword:
        return df_dict[output_column].drop_duplicates().tolist()

    # Strict filtering
    mask = df_dict[search_column].astype(str).str.contains(search_keyword, case=False, na=False)
    filtered_df = df_dict[mask]

    # Fuzzy logic if strict fails or if fuzzy is explicitly enabled
    if filtered_df.empty and fuzzy:
        all_names = df_dict[search_column].astype(str).tolist()
        matches = difflib.get_close_matches(search_keyword, all_names, n=5, cutoff=0.6)
        if matches:
            filtered_df = df_dict[df_dict[search_column].isin(matches)]
    
    return filtered_df[output_column].drop_duplicates().tolist()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List and filter clinical variables.")
    parser.add_argument("--keyword", type=str, help="Keyword to search for.")
    parser.add_argument("--search_col", type=str, default="generalized_variable_name", help="Column to search in.")
    parser.add_argument("--output_col", type=str, default="original_variable_name", help="Column to return.")
    
    args = parser.parse_args()
    
    vars = get_filtered_variable_names(args.keyword, args.search_col, args.output_col)
    for v in vars:
        print(v)
