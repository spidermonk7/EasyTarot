from typing import Any, Dict
import asyncio
import logging
from mcp.server.fastmcp import FastMCP
from MCPs.myTarot.run_draw_cards import draw


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server for the Tarot drawing functionality
mcp = FastMCP("Tarot_Drawer")

@mcp.tool()
def draw_Tarot() -> Dict[str, Any]:
    logging.info(f"Performing advanced search with parameters: {locals()}")
    """
    Draw three Tarot cards for divination.
    Args:
        No arguments required.

    Returns:
        Dict[str, Any]: A dictionary containing the drawn cards and their orientations.
    """
    try:
        results =  draw()
    
        return results
    except Exception as e:
        return [{"error": f"An error occurred while performing Drawing Tarot: {str(e)}"}]



if __name__ == "__main__":
    mcp.run()
