# NiFi Agent with A2A Integration

This is a refactored version of the NiFi ADK agent that integrates with the **a2a-python** framework for agent-to-agent communication.

## Overview

The NiFi agent is now capable of:
- Creating and managing Apache NiFi pipelines through MCP tools
- Communicating with other specialized agents via A2A protocol
- Delegating tasks like query optimization, security validation, and monitoring setup
- Running as a standalone A2A server

## Architecture

```
┌─────────────────┐    A2A Protocol    ┌─────────────────┐
│   NiFi Agent    │◄──────────────────►│  Query Expert   │
│   (Port 8001)   │                    │   (Port 8002)   │
└─────────────────┘                    └─────────────────┘
         │                                       
         │ A2A Protocol                          
         ▼                                       
┌─────────────────┐                    ┌─────────────────┐
│ Security Agent  │                    │ Monitoring Agent│
│  (Port 8003)    │                    │  (Port 8004)    │
└─────────────────┘                    └─────────────────┘
         ▲                                       ▲
         │ MCP Protocol                          │
         ▼                                       ▼
┌─────────────────┐                    ┌─────────────────┐
│  NiFi MCP       │                    │  Other Services │
│  (Port 8050)    │                    │                 │
└─────────────────┘                    └─────────────────┘
```

## Features

### Core Capabilities
- **Pipeline Creation**: Build complex NiFi data pipelines
- **MCP Integration**: Uses MCP tools to interact with NiFi instances
- **A2A Communication**: Delegates specialized tasks to other agents
- **Security Validation**: Automatically validates pipeline security
- **Query Optimization**: Optimizes SQL queries through expert agents
- **Monitoring Setup**: Configures monitoring for created pipelines

### A2A Integration Features
- **Query Expert Agent**: Optimizes SQL queries and data queries
- **Security Agent**: Validates pipeline configurations for security issues
- **Monitoring Agent**: Sets up monitoring and alerting for pipelines

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Install a2a-python**:
   ```bash
   pip install a2a-python
   ```

## Running the Agent

### As A2A Server

Run the NiFi agent as a standalone A2A server:

```bash
python -m agents.nifi_user_agent
```

The agent will start on `http://localhost:8001`

### Prerequisites

1. **NiFi MCP Server**: Ensure your NiFi MCP server is running on `http://localhost:8050/sse`
2. **Other A2A Agents** (Optional): Start other specialized agents if you want full A2A functionality

## Usage

### Direct A2A Communication

You can interact with the agent using the A2A client:

```python
from a2a.client import A2AClient

# Create client
nifi_client = A2AClient("http://localhost:8001")

# Send request
response = await nifi_client.send_message(
    "Create a pipeline from Kafka to S3",
    context={
        "kafka_topic": "user-events",
        "s3_bucket": "data-lake"
    }
)
```

### Test the Agent

Run the comprehensive test suite:

```bash
python test_nifi_a2a_client.py
```

This will test various pipeline creation scenarios including:
- Basic file-to-file pipelines
- Database to cloud storage pipelines
- Real-time Kafka to Elasticsearch pipelines
- Secure pipelines with encryption

## A2A Integration Examples

### Query Optimization

When you provide SQL queries, the agent automatically delegates to a query expert:

```
User: "Create a pipeline with this query: SELECT * FROM large_table WHERE date = '2024-01-01'"
Agent: "Let me optimize this query with the query expert agent..."
Result: Optimized query with proper indexing suggestions
```

### Security Validation

For sensitive data pipelines, the agent validates security:

```
User: "Create a pipeline for processing customer PII data"
Agent: "I'll validate the security configuration with the security agent..."
Result: Pipeline with proper encryption, access controls, and audit logging
```

### Monitoring Setup

Automatically sets up monitoring for created pipelines:

```
User: "Create a production pipeline from database to data warehouse"
Agent: "Setting up monitoring through the monitoring agent..."
Result: Pipeline with comprehensive monitoring, alerting, and metrics
```

## Configuration

### Agent URLs

Configure other agent URLs in `a2a_client_wrapper.py`:

```python
self.agent_urls = {
    "query_expert": "http://localhost:8002",
    "security_agent": "http://localhost:8003", 
    "monitoring_agent": "http://localhost:8004",
}
```

### Environment Variables

Required environment variables in `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key  # for LiteLLM
NIFI_MCP_URL=http://localhost:8050/sse
```

## Development

### Adding New A2A Integrations

1. **Add agent URL** in `a2a_client_wrapper.py`
2. **Create specialized method** for the integration
3. **Update agent prompt** to mention the new capability

Example:

```python
async def validate_data_quality(self, data_schema: Dict[str, Any]) -> Dict[str, Any]:
    """Send data schema to data quality agent for validation."""
    response = await self.send_message(
        "data_quality_agent",
        "Please validate this data schema",
        {"schema": data_schema, "task_type": "quality_validation"}
    )
    return response.get("validation_result", {})
```

### Creating Custom Tools

Add custom A2A-based tools in `agent.py`:

```python
async def custom_a2a_tool(param: str) -> str:
    """Custom tool that uses A2A communication."""
    result = await nifi_a2a_client.send_message(
        "specialized_agent",
        f"Process this: {param}",
        {"task_type": "custom_processing"}
    )
    return result.get("processed_result", param)
```

## Troubleshooting

### Common Issues

1. **A2A Connection Failed**: Ensure target agents are running and accessible
2. **MCP Server Not Found**: Check that NiFi MCP server is running on the correct port
3. **Authentication Errors**: Verify API keys in `.env` file

### Logging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Individual Components

Test A2A client wrapper:

```python
from agents.nifi_user_agent.a2a_client_wrapper import nifi_a2a_client

# Test query optimization
result = await nifi_a2a_client.optimize_query("SELECT * FROM users")
```

## API Reference

### A2A Endpoints

- **POST /message/send**: Send message to agent
- **GET /.well-known/agent**: Get agent metadata
- **POST /task/status**: Get task status

### Message Format

```json
{
  "message": "Create a pipeline from source to destination",
  "context": {
    "source": {"type": "database", "host": "localhost"},
    "destination": {"type": "s3", "bucket": "data-lake"},
    "task_type": "pipeline_creation"
  }
}
```

## Contributing

1. Follow the existing A2A integration patterns
2. Add comprehensive tests for new features
3. Update documentation for new A2A integrations
4. Ensure compatibility with the a2a-python framework

## License

This project follows the same license as the parent ADK project. 