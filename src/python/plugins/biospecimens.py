import pandas as pd
from pathlib import Path
from src.python.core.harmonizer import BaseHarmonizer

class BiospecimenHarmonizer(BaseHarmonizer):
    """
    Standard Plugin for Biological Specimen Handling.
    Processes Laboratory Information Management System (LIMS) extracts,
    blood panel readouts, and biobank catalog sheets.
    """
    
    def ingest(self, source_path: Path) -> pd.DataFrame:
        if source_path.suffix == '.csv':
            return pd.read_csv(source_path)
        else:
            self.logger.error(f"Unsupported biospecimen file format: {source_path.suffix}")
            return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        mapped_vars = self.registry['original_variable_name'].tolist()
        available_cols = [c for c in df.columns if c in mapped_vars]
        
        # Zero-Trust Selection for mapped specimen properties and labs
        result = df[available_cols].copy()
        
        # Dynamic modality tagging based on specimen type
        if 'specimen_type' in df.columns:
            specimen = str(result['specimen_type'].iloc[0]).lower()
            if 'blood' in specimen:
                result['modality_category'] = 'biospecimen_blood'
            elif 'saliva' in specimen:
                result['modality_category'] = 'biospecimen_saliva'
            elif 'urine' in specimen:
                result['modality_category'] = 'biospecimen_urine'
            elif 'csf' in specimen:
                 result['modality_category'] = 'biospecimen_csf'
            else:
                 result['modality_category'] = 'biospecimen_unknown'
        else:
            result['modality_category'] = 'biospecimen_unspecified'
            
        return result
