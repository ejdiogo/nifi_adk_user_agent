from google.adk.agents import Agent, LlmAgent
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from contextlib import AsyncExitStack
from .prompt import agent_prompt
from google.adk.models.lite_llm import LiteLlm
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def create_mcp_toolset():
    """Create the MCP toolset instance."""
    return MCPToolset(
        connection_params=SseServerParams(url="http://127.0.0.1:8050/sse")
    )


# Create the NiFi agent with MCP toolset
root_agent = Agent(
    name="nifi_pipeline_creator_agent",
    description="A NiFi pipeline creator agent with MCP tool integration",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction=agent_prompt,
    tools=[
        create_mcp_toolset()  # Pass the toolset instance, not the tools
    ],
)