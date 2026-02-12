# IMDA Agent Interface

This repository contains the Integrated Medical Data Architecture (IMDA) MCP Server. It provides an autonomously engineered context protocol for the orchestration of high-dimensional, multi-modal clinical data.

## The Master Clinical Registry

The `clinical_registry_master.csv` file is the central "Source of Truth" for your clinical project. It serves as a comprehensive data dictionary that defines the schema, validation rules, and harmonization logic for all clinical variables in the architecture.

### Key Metadata Specification:
- **`original_variable_name`**: The exact variable name as it exists in raw data sources (e.g., electronic health records, imaging headers).
- **`generalized_variable_name`**: A standardized, human-readable name used for cross-study orchestration (e.g., `subject_age_years`).
- **`datatype`**: Defines how the system processes the value:
    - `nominal` / `ordinal`: Categorical data used for frequency analysis and grouped bar charts.
    - `ratio` / `interval`: Continuous numerical data used for density plots and violin distributions.
- **`levels`**: A JSON-formatted mapping (e.g., `["1 = Male", "2 = Female"]`) that allows the system to automatically apply labels to raw encoded values during visualization.

### Usage Workflows:
- **Project Bootstrapping**: Point the `IMDA_PROJECT_ROOT` environment variable to the directory containing this file. The MCP server will automatically index these variables as resources.
- **Schema Enforcement**: The built-in integrity tools use this file to validate raw data imports, ensuring that no "schema drift" occurs over the lifecycle of the project.
- **Automated Reporting**: The plotting engine reads this metadata to determine which statistical visualizations are most appropriate for a given variable.

---

## Features

- **Registry Orchestration**: Tools to summarize, filter, and validate the master clinical registry.
- **Data Harmonization**: Automated engines to process raw clinical variables into harmonized formats.
- **Enhanced Visualizations**: A unified plotting engine that generates multi-panel visualizations (e.g., distribution views, sex-stratified analysis) based on registry metadata.
- **Synthetic Data**: Tools for generating statistically representative synthetic cohorts and test datasets.
- **Integrity Checks**: Automated suite to ensure zero schema drift across the data architecture.

## Setup

1. Install dependencies:
   ```bash
   pip install .
   ```

2. Run the server:
   ```bash
   python imda_server.py
   ```

## Configuration

Set the `IMDA_PROJECT_ROOT` environment variable to point to your clinical data project directory (containing `clinical_registry_master.csv`).
