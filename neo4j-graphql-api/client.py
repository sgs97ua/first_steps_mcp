# Create server parameters for stdio connection
from mcp import ClientSession
from mcp.client.sse import sse_client
# Ensure the required modules are installed and accessible
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from rich.pretty import pprint

from langchain_ollama import ChatOllama



async def main():
    async with sse_client('http://localhost:9999/sse') as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)
            
            # Create and run the agent
            agent = create_react_agent(ChatOllama(model="llama3.1:8b"), tools)
            agent_response = await agent.ainvoke({"messages": "Build me a GraphQL query to fetch the code of San Vicente del Raspeig"})
            pprint(agent_response)

# Run the main function
asyncio.run(main())
