import pandas as pd
from pathlib import Path
from src.python.core.harmonizer import BaseHarmonizer

class ClinicalAssessmentHarmonizer(BaseHarmonizer):
    """
    Standard Plugin for Clinical Assessment and Survey Data.
    Handles data from external survey tools like REDCap, Qualtrics, or native CRFs.
    Ensures survey scoring logic maps strictly to the Master Registry.
    """
    
    def ingest(self, source_path: Path) -> pd.DataFrame:
        if source_path.suffix == '.csv':
             return pd.read_csv(source_path)
        else:
             self.logger.error(f"Unsupported survey format: {source_path.suffix}")
             return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        mapped_vars = self.registry['original_variable_name'].tolist()
        available_cols = [c for c in df.columns if c in mapped_vars]
        
        # Zero-Trust Filter: Keeps only documented psychometric/survey scores
        result = df[available_cols].copy()
        
        # Standardize Modality Tagging
        if 'phq9_total' in df.columns or 'gad7_total' in df.columns:
             result['modality_category'] = 'clinical_survey_psychometrics'
        else:
             result['modality_category'] = 'clinical_survey_general'
             
        return result
