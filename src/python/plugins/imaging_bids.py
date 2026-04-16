import json
import pandas as pd
from pathlib import Path
from src.python.core.harmonizer import BaseHarmonizer

class BIDSHarmonizer(BaseHarmonizer):
    """
    Plugin for BIDS (Brain Imaging Data Structure) metadata harmonization.
    Handles T1w, fMRI, and DWI sidecar metadata.
    """
    
    def ingest(self, source_path: Path) -> pd.DataFrame:
        if not source_path.suffix == '.json':
            self.logger.error("BIDS metadata expected in .json format.")
            return pd.DataFrame()
            
        with open(source_path, 'r') as f:
            data = json.load(f)
        
        # Flatten dictionary for mapping
        return pd.DataFrame([data])

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        mapped_vars = self.registry['original_variable_name'].tolist()
        available_cols = [c for c in df.columns if c in mapped_vars]
        
        # Add basic project metadata
        result = df[available_cols].copy()
        
        # Try to infer modality from the scan description or filename
        # This is part of the 'multimodal' requirement
        if 'SeriesDescription' in df.columns:
            desc = str(df['SeriesDescription'].iloc[0]).lower()
            if 't1' in desc:
                result['modality_category'] = 'structural_mri'
            elif 'bold' in desc or 'fmri' in desc:
                result['modality_category'] = 'functional_mri'
            elif 'dwi' in desc or 'diff' in desc:
                result['modality_category'] = 'diffusion_mri'
            elif 'mrs' in desc or 'spec' in desc:
                result['modality_category'] = 'magnetic_resonance_spectroscopy'
            else:
                result['modality_category'] = 'unknown_mri'
        
        return result
