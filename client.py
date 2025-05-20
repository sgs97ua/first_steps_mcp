import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from rich.pretty import pprint

async def ollama_client():
    async with sse_client("http://localhost:9999/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
                        
# Example: List available tools
            tools_result = await session.list_tools()
            pprint(tools_result.tools)

# Example: Call a specific tool (replace 'ollama_tool' with the actual tool name)
            tool_result = await session.call_tool("ollama_tool", arguments={"example_arg": "value"})
            pprint(tool_result.content)

if __name__ == "__main__":  
    asyncio.run(ollama_client())