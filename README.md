# Integrated Medical Data Architecture (IMDA)

The Integrated Medical Data Architecture (IMDA) is a multi-modal clinical data processing pipeline that helps address constraints inherent in large cohort research and data collection. 

## Data Types and General Information

IMDA is an object oriented pipeline (`IMDAEngine`) with the following architecture:

*   **Bronze Tier (Raw Ingestion)**: NIfTI, DICOM, fastq-derived CSVs, REDCap exports, raw wearable JSONs
*   **Silver Tier (Harmonization)**: Zero-trust schema mapping executed via isolated plugins. Domain-specific metrics are mathematically validated against the `clinical_registry_master`, uniformity across sites.
*   **Gold Tier (Structure)**: Data is dynamically aligned along Subject (`participant_id`) and Time (`visit_session`)

---

## Supported Modalities & Pipelines

The architecture handles data processing through high-efficiency batching, allowing simultaneous evaluation of data structures.

*   **Neuroimaging (fMRI & sMRI)**: Directly ingests 4D NIfTI constructs. Utilizing `nibabel` and `nilearn`, the engine autonomously extracts BOLD (Blood-Oxygen-Level-Dependent) time-series metadata and computes functional amplitude variances natively.
*   **Multi-Omics (Genomic / Proteomic)**: Standardizes Variant Call Formats (e.g., resolving `rsid` and zygosity) and maps proteomic abundances (UniProt) securely into the cohort timeline.
*   **Clinical NLP**: Translates subjective, unstructured physician free-text into computable numerical features, extracting ontological identifiers (e.g., SNOMED-CT).
*   **Digital Biomarkers**: Deconstructs high-frequency time-series arrays representing wearable actigraphy (e.g., Continuous Heart Rate) to extract clinically significant scalar representations such as sleep efficiency.
*   **Biological Specimens & Psychometrics**: Standardizes Laboratory Information Systems (LIMS) assays and clinical survey instruments into standardized statistical bounds.

---

## Privacy

*still a work in progress* 

Clinical environments operate under compliance constraints (HIPAA, GDPR, EU AI Act).

During the generation of the Gold Tier data object, IMDA uses W3C-PROV Compliant Routines to append unique SHA-256 hashes to every row-wise entries. This enforces granular tracking, ensuring every tensor utilized directly connects to a raw data asset. Any variable undetected within the schema registry is automatically removed, helping prevent unapproved PHI from getting into the pipeline
---

## MCP Protocol

### Connecting to an LLM
To expose IMDA to an LLM (i.e., claude, gemini), you can run the server via `fastmcp`:

1.  **Start MCP Server**:
    ```bash
    fastmcp run imda_server.py
    ```
    *(Alternatively, run it dynamically within your agent's config using `python3 imda_server.py` via standard input/output).*

2.  **LLM Interaction**:
    Once attached, LLM will automatically index IMDA's tools such as:
    *   `process_imaging_metadata`: Point the agent to raw `.nii.gz` files to extract 4D BOLD signals natively.
    *   `check_registry_integrity`: Let the agent verify the gold tier schema without writing code.
    *   `generate_synthetic_cohort`: Have the agent mimic the privacy-redacted patient data perfectly for testing.

Allows LLM to act as a fully functioning pipeline for updating registries and pipelining raw input data via standard prompting.

---

## To run

```bash
python3 system_init.py
```

