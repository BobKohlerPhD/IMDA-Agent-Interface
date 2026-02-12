# IMDA Agent Interface

This repository contains the Integrated Medical Data Architecture (IMDA) MCP Server. It provides an autonomously engineered context protocol for the orchestration of high-dimensional, multi-modal clinical data.

## The Master Clinical Registry

The `clinical_registry_master.csv` file is the central "Source of Truth" for your clinical project. It serves as a data dictionary that defines the schema and metadata for all clinical variables.

### What it contains:
- **`original_variable_name`**: The raw name from the source data.
- **`generalized_variable_name`**: The standardized name used within IMDA.
- **`datatype`**: The variable type (e.g., numeric, categorical).
- **`levels`**: Valid values for categorical data.

### How to provide it:
- **Existing Projects**: Set the `IMDA_PROJECT_ROOT` environment variable to the directory containing your existing `clinical_registry_master.csv`.
- **New Projects**: The agent provides tools to process raw clinical metadata into this standardized format (see `update_master_registry`).

---

## Features

- **Registry Orchestration**: Tools to summarize, filter, and validate the master clinical registry.
- **Data Harmonization**: Triggers for R-based statistical gathering and variable processing.
- **Enhanced Visualizations**: A unified plotting engine (`clinical-plots_unified.r`) that generates multi-panel visualizations for variables:
    - **Categorical Data**: Frequency bar charts and sex-stratified distributions.
    - **Continuous Data**: Density/Histogram views and sex-stratified Violin/Boxplots.
- **Synthetic Data**: Tools for generating statistically representative synthetic cohorts and test datasets.
- **Integrity Checks**: Automated suite to ensure zero schema drift.

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
