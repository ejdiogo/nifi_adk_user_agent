"""
Main entry point for the NiFi A2A Agent Server using a2a-python framework.
Run with: python -m agents.nifi_user_agent
"""

import logging
import uvicorn
from dotenv import load_dotenv

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from .agent_executor import create_nifi_agent_executor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
agent_url = "http://localhost:9999/"


def main():
    try:
        # Create agent card with capabilities
        agent_card = get_agent_card()
        
        # Set up request handler with in-memory task store
        request_handler = DefaultRequestHandler(
            agent_executor=create_nifi_agent_executor(),
            task_store=InMemoryTaskStore(),
        )

        # Create and configure the A2A server
        server = A2AStarletteApplication(
            agent_card=agent_card,
            http_handler=request_handler
        )

        # Start the server
        logger.info("Starting NiFi A2A Agent Server on %s", agent_url)
        uvicorn.run(
            server.build(),
            host=agent_url.split(':')[1].strip('/'),
            port=agent_url.split(':')[-1],
            log_level='info'
        )

    except Exception as e:
        logger.error(f"Failed to start NiFi A2A Agent Server: {e}")
        raise 

def get_agent_card():
    """
    Field Name	Type	        Required	Description
    name	    string	        Yes     	Human-readable name of the agent.
    description	string	        Yes	        Human-readable description. CommonMark MAY be used.
    url	string	Yes	            Base        URL for the agent's A2A service. Must be absolute. HTTPS for production.
    provider	AgentProvider	No	        Information about the agent's provider.
    version	    string	        Yes	        Agent or A2A implementation version string.
    documentationUrl    string	No	        URL to human-readable documentation for the agent.
    capabilities	AgentCapabilities	Yes	Specifies optional A2A protocol features supported (e.g., streaming, push notifications).
    securitySchemes	{ [scheme: string]: SecurityScheme }	No	Security scheme details used for authenticating with this agent. undefined implies no A2A-advertised auth (not recommended for production).
    security	{ [scheme: string]: string[]; }[]	No	Security requirements for contacting the agent.
    defaultInputModes	string[]	Yes	Input MIME types accepted by the agent.
    defaultOutputModes	string[]	Yes	Output MIME types produced by the agent.
    skills	AgentSkill[]	Yes	Array of skills. Must have at least one if the agent performs actions.
    supportsAuthenticatedExtendedCard	boolean	No	Indicates support for retrieving a more detailed Agent Card via an authenticated endpoint.
    """
    return AgentCard(
            name='NiFi Expert Agent',
            description='Creates and manages Apache NiFi data pipelines with A2A integration',
            url=agent_url,
            version='1.0.0',
            defaultInputModes=['text'],
            defaultOutputModes=['text'],
            capabilities=get_agent_capabilities(),
            skills=[*get_agent_skills()],
        )

def get_agent_capabilities():
    # Define agent capabilities. This will be a list of capabilities for the agent to present to other agents.
    # 5.5.2. AgentCapabilities Object
    """
    streaming - boolean - default: false    Indicates support for SSE streaming methods (message/stream, tasks/resubscribe).
    pushNotifications - boolean	- default: false	Indicates support for push notification methods (tasks/pushNotificationConfig/*).
    stateTransitionHistory -boolean - default: false	Placeholder for future feature: exposing detailed task status change history.
    """
    return AgentCapabilities(
        streaming=True,
        pushNotifications=False,
        stateTransitionHistory=False
    )

def get_agent_skills():
    # Define agent skills. This will be a list of skills for the agent to present to other agents.
    # TODO: Add more skills
    PIPELINE_CREATION_SKILL = AgentSkill(
        id='create_pipeline',
        name='Create NiFi Pipeline',
        description='Creates data pipelines in Apache NiFi with various sources and destinations',
        tags=['nifi', 'pipeline', 'data-integration', 'etl'],
        examples=[
            'Create a pipeline that reads from a CSV file and writes to PostgreSQL',
            'Build a Kafka to Elasticsearch pipeline with JSON transformation',
            'Set up a secure SFTP to S3 pipeline with encryption'
        ],
    )
    PIPELINE_OPTIMIZATION_SKILL = AgentSkill(
        id='optimize_pipeline',
        name='Optimize NiFi Pipeline',
        description='Optimizes existing NiFi pipelines for performance and reliability',
        tags=['optimization', 'performance', 'tuning'],
        examples=[
            'Optimize the Kafka consumer settings for better throughput',
            'Tune the PostgreSQL processor batch size',
            'Configure back pressure settings for the pipeline'
        ],
    )
    return [PIPELINE_CREATION_SKILL, 
            PIPELINE_OPTIMIZATION_SKILL]


if __name__ == '__main__':
    main()