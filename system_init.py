import os
import sys
import subprocess
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.resolve()))

from src.python.core.engine import IMDAEngine
from src.python.plugins.imaging_bids import BIDSHarmonizer
from src.python.plugins.converter_nibabel import NibabelConverter
from src.python.plugins.multi_omics import MultiOmicsHarmonizer
from src.python.plugins.clinical_assessments import ClinicalAssessmentHarmonizer
from src.python.plugins.biospecimens import BiospecimenHarmonizer
from src.python.plugins.wearables import WearableHarmonizer
from src.python.plugins.clinical_nlp import ClinicalNLPHarmonizer
from src.python.plugins.fmri_nilearn import fMRINilearnHarmonizer

def main():
    print("=== IMDA Architecture: Federated Multi-Modal Data Engine ===")
    root = Path(__file__).parent.resolve()
    engine = IMDAEngine(root)
    
    # Register Plugins & Converters
    engine.register_plugin("bids", BIDSHarmonizer)
    engine.register_plugin("omics", MultiOmicsHarmonizer)
    engine.register_plugin("assessments", ClinicalAssessmentHarmonizer)
    engine.register_plugin("biospecimens", BiospecimenHarmonizer)
    engine.register_plugin("wearables", WearableHarmonizer)
    engine.register_plugin("nlp", ClinicalNLPHarmonizer)
    engine.register_plugin("fmri_signal", fMRINilearnHarmonizer)
    engine.register_converter(".nii", NibabelConverter())

    # Create samples if missing
    if not (root / "data" / "bronze" / "genomics" / "sub-001_variants.csv").exists():
        try:
            subprocess.run(["python3", "create_omics_samples.py"], check=True)
        except Exception as e:
            print(f"Sample generation failed: {e}")

    print("\n>>> Processing Multi-Modal Federated Data via Parallel Batching...")
    tasks = [
        ("bids", "imaging/sub-001_ses-01_task-rest_bold.json"),
        ("omics", "genomics/sub-001_variants.csv"),
        ("omics", "proteomics/sub-001_mass_spec_report.csv"),
        ("omics", "metabolomics/sub-001_metabolite_panel.csv"),
        ("assessments", "assessments/sub-001_mh_survey.csv"),
        ("biospecimens", "biospecimens/sub-001_blood_draw.csv"),
        ("biospecimens", "biospecimens/sub-001_saliva_swab.csv"),
        ("wearables", "wearables/sub-001_ses-01_actigraphy.json"),
        ("nlp", "ehr_notes/sub-001_ses-01_clinical_note.csv"),
        ("fmri_signal", "imaging/sub-001_ses-01_task-rest_bold.nii.gz")
    ]
    engine.batch_process(tasks)

    print("\n>>> Synchronizing Silver Tiers...")
    silver_files = list((root / "data" / "silver").glob("harmonized_sub-001*.csv"))
    for f in silver_files:
        print(f" - Found Silver Asset: {f.name}")
        
    print("\n>>> Generating SOTA Gold Tier (Multi-Modal Cross-Join & Provenance Hashing)...")
    gold_df = engine.generate_gold_tier()
    if gold_df is not None:
        print("\nGold Tier Columns:")
        print(list(gold_df.columns))
        print(f"\nFinal Cohort Matrix Shape: {gold_df.shape}")

if __name__ == "__main__":
    main()
