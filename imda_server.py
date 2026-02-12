import os
import subprocess
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize the IMDA MCP Server
mcp = FastMCP("IMDA-Orchestrator")

# In this repository, scripts are located relative to the server root
PROJECT_ROOT = Path(__file__).parent.resolve()

@mcp.resource("clinical-registry://master")
def get_registry_master() -> str:
    """
    Returns the contents of the master clinical registry CSV.
    """
    registry_path = PROJECT_ROOT / "clinical_registry_master.csv"
    try:
        return registry_path.read_text()
    except Exception as e:
        return f"Error reading registry: {str(e)}"

@mcp.tool()
async def check_registry_integrity() -> str:
    """
    Executes the integrity suite to ensure zero schema drift in the master registry.
    """
    try:
        script_path = PROJECT_ROOT / "src/python/data_dictionary/registry_integrity_check.py"
        result = subprocess.run(["python3", str(script_path)], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return f"INTEGRITY PASSED:\n{result.stdout}"
        else:
            return f"INTEGRITY FAILED:\n{result.stderr}\nSTDOUT:\n{result.stdout}"
    except Exception as e:
        return f"ERROR: Could not execute integrity check: {str(e)}"

@mcp.tool()
async def generate_synthetic_cohort(size: int = 100) -> str:
    """
    Generates a statistically representative synthetic dataset based on registry metadata.
    """
    try:
        script_path = PROJECT_ROOT / "src/python/analysis/score-analysis_orchestrator.py"
        result = subprocess.run(["python3", str(script_path), "--size", str(size)], 
                                capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return f"COHORT GENERATED:\n{result.stdout}"
        else:
            return f"ERROR GENERATING COHORT:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def gather_variables() -> str:
    """
    Triggers the statistical gathering module to process raw variables into harmonized formats.
    """
    try:
        script_path = PROJECT_ROOT / "src/r/variables/score-variables_gather.r"
        result = subprocess.run(["Rscript", str(script_path)], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return f"PROCESSING COMPLETE:\n{result.stdout}"
        else:
            return f"PROCESSING FAILED:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: execution failed: {str(e)}"

@mcp.tool()
async def list_registry_variables(
    keyword: Optional[str] = None, 
    search_col: Optional[str] = None, 
    output_col: Optional[str] = None
) -> str:
    """
    Filters and lists variables from the master clinical registry.
    """
    try:
        script_path = PROJECT_ROOT / "src/python/variables/score-variables_list.py"
        cmd = ["python3", str(script_path)]
        if search_col:
            cmd.extend(["--search_col", search_col])
        if output_col:
            cmd.extend(["--output_col", output_col])
        if keyword:
            cmd.extend(["--keyword", keyword])
            
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"ERROR LISTING VARIABLES:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def summarize_registry() -> str:
    """
    Provides a summary of the master registry, including dimensions and data quality metrics.
    """
    try:
        script_path = PROJECT_ROOT / "src/python/data_dictionary/check_datadictionary_summary.py"
        result = subprocess.run(["python3", str(script_path)], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"ERROR SUMMARIZING REGISTRY:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def update_master_registry() -> str:
    """
    Processes raw metadata sources to regenerate the master clinical registry.
    """
    try:
        script_path = PROJECT_ROOT / "src/python/data_dictionary/score-variables_process_dictionary.py"
        result = subprocess.run(["python3", str(script_path)], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return f"REGISTRY UPDATED:\n{result.stdout}"
        else:
            return f"UPDATE FAILED:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

@mcp.tool()
async def generate_test_data() -> str:
    """
    Generates a mock dataset based on the current registry schema for testing purposes.
    """
    try:
        script_path = PROJECT_ROOT / "src/r/variables/generate_test_data.r"
        result = subprocess.run(["Rscript", str(script_path)], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return f"TEST DATA GENERATED:\n{result.stdout}\n{result.stderr}"
        else:
            return f"EXECUTION FAILED:\n{result.stderr}"
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    mcp.run()
