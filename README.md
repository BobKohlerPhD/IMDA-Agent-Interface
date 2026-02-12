# IMDA Agent Interface

This repository contains the Integrated Medical Data Architecture (IMDA) MCP Server. It provides an autonomously engineered context protocol for the orchestration of high-dimensional, multi-modal clinical data.

## Features

- **Registry Orchestration**: Tools to summarize, filter, and validate the master clinical registry.
- **Data Harmonization**: Triggers for R-based statistical gathering and variable processing.
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
