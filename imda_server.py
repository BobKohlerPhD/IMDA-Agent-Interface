import asyncio
import logging
import json
import os
from pathlib import Path
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

# Import the new Skeletal Architecture
from src.python.core.engine import IMDAEngine
from src.python.plugins.imaging_bids import BIDSHarmonizer

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/imda_audit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("IMDA-Orchestrator")

# Initialize the IMDA MCP Server
mcp = FastMCP("IMDA-Orchestrator")

# Initialize the Engine
PROJECT_ROOT = Path(os.environ.get("IMDA_PROJECT_ROOT", Path(__file__).parent.resolve()))
engine = IMDAEngine(PROJECT_ROOT)
engine.register_plugin("bids", BIDSHarmonizer)

@mcp.tool()
async def process_imaging_metadata(filename: str) -> str:
    """
    Processes neuroimaging metadata from the Bronze tier using the BIDS plugin.
    Example filename: 'sub-001/ses-01/func/sub-001_ses-01_task-rest_bold.json'
    """
    try:
        # Note: In a real system, this would be an async call
        result_df = engine.process_modality("bids", filename)
        if result_df is not None and not result_df.empty:
            return f"Successfully processed {filename}. Modalitiy inferred: {result_df['modality_category'].iloc[0]}"
        else:
            return f"Failed to process {filename} or no mapped variables found."
    except Exception as e:
        logger.exception(f"Error processing {filename}: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
async def list_data_tiers() -> str:
    """
    Lists the current contents of Bronze, Silver, and Gold tiers.
    """
    summary = []
    for tier in ["bronze", "silver", "gold"]:
        tier_path = PROJECT_ROOT / "data" / tier
        files = list(tier_path.glob("**/*"))
        summary.append(f"### {tier.upper()} TIER")
        summary.append(f"Total Files: {len(files)}")
        for f in files[:5]: # Show first 5
            summary.append(f" - {f.relative_to(tier_path)}")
        if len(files) > 5:
            summary.append(" - ...")
        summary.append("")
    return "\n".join(summary)

@mcp.resource("clinical-registry://master")
def get_registry_master() -> str:
    """Returns the master clinical registry."""
    return engine.registry_path.read_text()

if __name__ == "__main__":
    mcp.run()
