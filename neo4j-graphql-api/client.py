# Create server parameters for stdio connection
from mcp import ClientSession
from mcp.client.sse import sse_client
# Ensure the required modules are installed and accessible
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
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
            resources = await load_mcp_resources(session)

            neo4j_entity_representation = None
            api_schema = None 
            # GET GRAPQL NEO4J RESOURCES
            for resource in resources:
                if resource.name == "neo4j-graphql":
                    neo4j_entity_representation = resource.data
                
                elif resource.name == "api_schema":
                    api_schema = resource.data
                    



            # Create and run the agent
            agent = create_react_agent(ChatOllama(model="qwen3:4b",num_ctx=8192), tools)
        
            agent_response = await agent.ainvoke({"messages": f"""A partir del siguiente esquema de una API Neo4j GraphQL Library quiero que generes una consulta en GraphQL para obtener el código de un municipio. 
                                                  El esquema es el siguiente:
                                                  <SCHEMA>{resources[0].data}</SCHEMA> 

                                                  Ejemplo:
                                                  <QUERY> Nombre de municipios en la base de datos </QUERY>
                                                    <RESULT>
                                                  {{
                                                    municipios{{
                                                        nombre
                                                    }}
                                                  }}
                                                    </RESULT>
                                                  Consulta Usuario:
                                                  <QUERY>Número de secciones censales en el municipio con código '122'?</QUERY>"""})
            pprint(agent_response)

# Run the main function
asyncio.run(main())
