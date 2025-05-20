from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather", host="localhost", port=9999, sse_path="/mcp")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return "It's always sunny in New York"

if __name__ == "__main__":
    mcp.run(transport="sse")