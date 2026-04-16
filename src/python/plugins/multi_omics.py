import pandas as pd
from pathlib import Path
from src.python.core.harmonizer import BaseHarmonizer

class MultiOmicsHarmonizer(BaseHarmonizer):
    """
    Standard Plugin for Multi-Omics datasets (Genomics, Proteomics, Metabolomics).
    Handles tabular data ingestion (VCF-parsed CSV or Mass-Spec reports).
    """
    
    def ingest(self, source_path: Path) -> pd.DataFrame:
        if source_path.suffix == '.csv':
            return pd.read_csv(source_path)
        elif source_path.suffix == '.parquet':
            return pd.read_parquet(source_path)
        else:
            self.logger.error(f"Unsupported Omics format: {source_path.suffix}")
            return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        mapped_vars = self.registry['original_variable_name'].tolist()
        available_cols = [c for c in df.columns if c in mapped_vars]
        
        # Filtering for mapped variables (Zero-Trust)
        result = df[available_cols].copy()
        
        # Logic to infer omics sub-modality
        if 'rsid' in df.columns:
            result['modality_category'] = 'genomics'
        elif 'protein_id' in df.columns:
            result['modality_category'] = 'proteomics'
        elif 'metabolite_name' in df.columns:
            result['modality_category'] = 'metabolomics'
            
        return result
