import os
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize the IMDA MCP Server
mcp = FastMCP("IMDA-Orchestrator")

@mcp.tool()
async def check_registry_integrity() -> str:
    """
    Executes the IMDA integrity suite to ensure zero schema drift 
    in the master clinical registry.
    """
    try:
        script_path = "src/python/data_dictionary/registry_integrity_check.py"
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        if result.returncode == 0:
            return f"INTEGRITY PASSED: {result.stdout}"
        else:
            return f"INTEGRITY FAILED: {result.stderr}"
    except Exception as e:
        return f"ERROR: Could not execute integrity check: {str(e)}"

@mcp.tool()
async def generate_synthetic_cohort(size: int = 100) -> str:
    """
    Generates a statistically representative synthetic dataset 
    preserving the covariance structure of the clinical metadata.
    """
    try:
        script_path = "src/python/analysis/score-analysis_orchestrator.py"
        result = subprocess.run(["python3", script_path, "--size", str(size)], capture_output=True, text=True)
        return f"COHORT GENERATED: {result.stdout}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def gather_r_variables() -> str:
    """
    Triggers the high-performance R-based statistical gathering module 
    to process raw clinical variables into harmonized RDS/Parquet formats.
    """
    try:
        script_path = "src/r/variables/score-variables_gather.r"
        result = subprocess.run(["Rscript", script_path], capture_output=True, text=True)
        return f"R PROCESSING COMPLETE: {result.stdout}"
    except Exception as e:
        return f"ERROR: R execution failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
