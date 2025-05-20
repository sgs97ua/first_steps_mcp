# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# Ensure the required modules are installed and accessible
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from rich.pretty import pprint

from langchain_ollama import ChatOllama


server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["./server_langchain.py"],
)
async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(ChatOllama(model="llama3.1:8b"), tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5)?"})
            pprint(agent_response)

# Run the main function
asyncio.run(main())
