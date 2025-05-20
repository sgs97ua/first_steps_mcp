# Create server parameters for stdio connection
from mcp import ClientSession
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.client.stdio import stdio_client
# Ensure the required modules are installed and accessible
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from rich.pretty import pprint

from langchain_ollama import ChatOllama


client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["./server_math.py"],
            "transport": "stdio",
        },
        "weather": {
            # make sure you start your weather server on port 8000
            "url": "http://localhost:9999/mcp",
            "transport": "sse",
        }
    }
)


async def main():

    tools = await client.get_tools()
    agent = create_react_agent(ChatOllama(model="llama3.1:8b"), tools)
    agent_response = await agent.ainvoke({"messages": "what's (3 + 5)?"})
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    pprint(agent_response)
    pprint(weather_response)
# Run the main function
asyncio.run(main())
