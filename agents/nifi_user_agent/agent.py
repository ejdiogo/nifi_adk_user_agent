from google.adk.agents import Agent, LlmAgent
from dotenv import load_dotenv
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from contextlib import AsyncExitStack
from .prompt import agent_prompt
from google.adk.models.lite_llm import LiteLlm
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class NiFiAgent:
    """NiFi Agent implementation."""
    
    def __init__(self):
        """Initialize the NiFi agent."""
        self.agent = self.create_agent()
        
    async def create_agent():
        """Create the NiFi agent with MCP tools and A2A client integration."""
        common_exit_stack = AsyncExitStack()
        
        # Get tools from MCP Server
        remote_tools, _ = await MCPToolset.from_server(
            connection_params=SseServerParams(url="http://127.0.0.1:8050/sse"),
            async_exit_stack=common_exit_stack
        )
        
        # Create the enhanced prompt that includes A2A capabilities
        # enhanced_prompt = agent_prompt + """

        #     <A2A Integration Guidelines>
        #     When processing requests, you can delegate specialized tasks to other agents:

        #     1. Query Optimization: For SQL queries or complex data queries, use the query_expert agent
        #     2. Monitoring Setup: For setting up monitoring, use the monitoring_agent

        #     To use A2A agents, mention in your response when you're delegating tasks to other agents.
        #     The system will automatically handle the A2A communication.

        #     Examples:
        #     - "Let me optimize this query with the query expert agent..."
        #     - "I'll validate the security configuration with the security agent..."
        #     - "Setting up monitoring through the monitoring agent..."
        #     </A2A Integration Guidelines>"""
        
        agent = Agent(
            name="nifi_pipeline_creator_agent",
            description="A NiFi pipeline creator agent with A2A integration for specialized tasks",
            model=LiteLlm(model="openai/gpt-4o-mini"),
            instruction=agent_prompt,
            tools=[
                *remote_tools    
            ],
        )
        
        
        return agent, common_exit_stack


root_agent = NiFiAgent.create_agent()