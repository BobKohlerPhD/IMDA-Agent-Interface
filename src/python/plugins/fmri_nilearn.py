import pandas as pd
from pathlib import Path
import nibabel as nib
import numpy as np
from src.python.core.harmonizer import BaseHarmonizer

class fMRINilearnHarmonizer(BaseHarmonizer):
    """
    State-of-the-art computational plug-in.
    Instead of just parsing metadata, it ingests a 4D fMRI NIfTI,
    processes the BOLD signals across time, and extracts the global amplitude.
    """
    
    def ingest(self, source_path: Path) -> pd.DataFrame:
        if not str(source_path).endswith('.nii') and not str(source_path).endswith('.nii.gz'):
            self.logger.error(f"fMRI Nilearn requires a NIfTI file, got: {source_path}")
            return pd.DataFrame()
            
        self.logger.info(f"Nilearn Engine computing BOLD amplitudes for {source_path.name}...")
        try:
            # 1. Load the 4D fMRI data
            img = nib.load(str(source_path))
            data = img.get_fdata()
            
            # For demonstration: We compute a global mean timeseries (taking mean across spatial dimensions)
            # In a real SOTA implementation, we'd use nilearn.maskers.NiftiMasker with a brain mask
            # data shape is (x, y, z, time)
            if len(data.shape) == 4:
                global_timeseries = np.mean(data, axis=(0, 1, 2))
                
                # We calculate the amplitude (Standard Deviation of the BOLD signal)
                fmri_amplitude = np.std(global_timeseries)
                
                # Output as a single computational feature
                return pd.DataFrame([{
                    "fmri_amplitude": fmri_amplitude,
                    "modality_category": "functional_mri_bold_signal"
                }])
            else:
                self.logger.error("fMRI requires 4-Dimensional NIfTI data.")
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"Nilearn computation failed: {e}")
            return pd.DataFrame()

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
            
        mapped_vars = self.registry['original_variable_name'].tolist()
        available_cols = [c for c in df.columns if c in mapped_vars]
        
        result = df[available_cols].copy()
        # Keep the modality category injected during ingest
        if 'modality_category' in df.columns:
             result['modality_category'] = df['modality_category'].iloc[0]
             
        return result
