from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    name="MLExpert Server",
    host="localhost",
    port=9999,
    sse_path="/sse"
)

@mcp.tool()
def list_tasks(max_results: int) -> list[str]:
    """
    List all tasks in the system.
    """
    return [
        "Eat breakfast",
        "Go to the gym",
        "Read a book"
    ][:max_results]


if __name__ == '__main__':
    mcp.run(transport="sse")