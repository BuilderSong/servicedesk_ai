"""Optional MCP SDK v1-style teaching server. Local stdio; fixed scope.
Verify imports against the SDK version you install. Never print to stdout.
"""
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from solutions.core import retrieve
mcp=FastMCP("Course guidance")
docs=json.loads((Path(__file__).parents[1]/"data/documents.json").read_text())

@mcp.tool()
def search_guidance(query: str) -> list[str]:
    """Search synthetic organization A guidance. Returns source IDs."""
    return retrieve(query,docs,org_id="A")

if __name__ == "__main__":
    mcp.run(transport="stdio")
