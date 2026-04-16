# Integrated Medical Data Architecture (IMDA)

The Integrated Medical Data Architecture (IMDA) is a multi-modal clinical data orchestration framework designed to address multimodal data constraints inherent in large cohonort data collection. By fusing high-dimensional arrays from disparate biomedical domains—including Neuroimaging (fMRI/sMRI BIDS), Multi-Omics (Genomics, Proteomics, Metabolomics), Digital Biomarkers (Wearables), and Electronic Health Records (Clinical NLP & EHR)—IMDA yields mathematically aligned, temporally accurate, and cryptographically secure multi-modal tensors for immediate machine learning interoperability.



## Data Types and General Information

IMDA is an extensible Object-Oriented Engine (`IMDAEngine`) with a data-tier architecture described below: 

**Bronze Tier (Raw Ingestion)**: NIfTI, DICOM, fastq-derived CSVs, REDCap exports, raw wearable JSONs
**Silver Tier (Harmonization)**: Zero-trust schema mapping executed via isolated plugins. Domain-specific metrics are mathematically validated against the `clinical_registry_master`, uniformity across sites.
**Gold Tier (Structure)**: Data is dynamically aligned along Subject (`participant_id`) and Time (`visit_session`)

---

## Supported Modalities & Pipelines

The architecture handles complex native processing through high-efficiency asynchronous batching, allowing simultaneous evaluation of non-isomorphic data structures.

*   **Neuroimaging (fMRI & sMRI)**: Directly ingests 4D NIfTI constructs. Utilizing `nibabel` and `nilearn`, the engine autonomously extracts BOLD (Blood-Oxygen-Level-Dependent) time-series metadata and computes functional amplitude variances natively.
*   **Multi-Omics (Genomic / Proteomic)**: Standardizes Variant Call Formats (e.g., resolving `rsid` and zygosity) and maps proteomic abundances (UniProt) securely into the cohort timeline.
*   **Clinical NLP**: Translates subjective, unstructured physician free-text into computable numerical features, extracting ontological identifiers (e.g., SNOMED-CT).
*   **Digital Biomarkers**: Deconstructs high-frequency time-series arrays representing wearable actigraphy (e.g., Continuous Heart Rate) to extract clinically significant scalar representations such as sleep efficiency.
*   **Biological Specimens & Psychometrics**: Standardizes Laboratory Information Systems (LIMS) assays and clinical survey instruments into standardized statistical bounds.

---

## Privacy

Clinical environments operate under strict compliance constraints (HIPAA, GDPR, EU AI Act).

During the generation of the Gold Tier data object, IMDA uses W3C-PROV Compliant Routines to append unique SHA-256 hashes to every row-wise entries. This enforces granular tracking, ensuring every tensor utilized directly connects to a raw data asset. 

Any variable undetected within the schema registry is automatically removed, helping guarantee unapproved Protected Health Information (PHI) never gets into the pipeline.

---

## 4. MCP Protocol

IMDA is a Python library and AI-native interface. Under the `imda_server.py` implementation, the architecture acts as an autonomous node utilizing the **Model Context Protocol (MCP). Allows for lanuage models to explore data, issue pipeline ingestions, plot, and model data autonomously without manual user intervention.

---

## To run

```bash
python3 system_init.py
```

