# ADK Made Simple - Agent Examples

This project demonstrates simple agents built using the Google Agent Development Kit (ADK). It accompanies the YouTube tutorial series "ADK Made Simple" hosted on the [AIOriented YouTube channel](https://www.youtube.com/@AIOriented).

Full series playlist: [ADK Made Simple Playlist](https://www.youtube.com/playlist?list=PLWUH7ke1DYK98Di2FF8Ux3IX6qG-mZ3A7)

## Lessons

| Lesson | Link | Description |
| ------ | ---- | ----------- |
| 1      | [Lesson 1: Basics of ADK & Reddit Scout Agent](https://www.youtube.com/watch?v=BiP4tKZKTvU) | Basics of ADK, Building a Reddit news agent with PRAW |
| 2      | [Lesson 2: Multi-Agent Systems & TTS](https://www.youtube.com/watch?v=FODBW9az-sw) | Combining ADK with MCP, Multi-Agent Systems, Text-To-Speech with ElevenLabs, LiteLLM |
| 3      | [Lesson 3: Custom UI for Speaker Agent (ADK API Server)](https://www.youtube.com/watch?v=jrFFEPWoB1Q) | Building a Streamlit UI for the Speaker Agent using the ADK API server (no A2A yet) |
| 4      | [Lesson 4: Serving Agents via A2A Protocol](https://www.youtube.com/@AIOriented?sub_confirmation=1) | Introducing the A2A protocol, running agents as standalone A2A services, and building UIs for A2A agents |

## Agents

- **NiFi User Agent**: Creates and manages Apache NiFi data pipelines with A2A integration for specialized tasks (query optimization, security validation, monitoring). Uses a2a-python framework for agent-to-agent communication.

## General Setup

1.  **Create and activate a virtual environment (Recommended):**

    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

2.  **Install general dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Key:**

    - Copy the example environment file:
      ```bash
      cp ../.env.example .env
      ```
    - Edit the `.env` file and add your Google AI API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).
      ```dotenv
      GOOGLE_API_KEY=YOUR_API_KEY_HERE

    - _Note:_ You might need to load this into your environment depending on your OS and shell (`source .env` or similar) if `python-dotenv` doesn't automatically pick it up when running `adk`.

4.  **Agent-Specific Setup:** Navigate to the specific agent's directory within `agents/` and follow the instructions in its `README.md` (or follow the steps below for the default agent).

## Setup & Running Agents

This section describes running agents via the ADK framework (e.g., `adk run` or `adk web`).

1.  **Navigate to Agent Directory:**

    ```bash
    cd agents/
    ```

2.  **Run the Agent:**

    - Make sure your virtual environment (from the root directory) is activated.
    - From the `agents/nifi_user_agent` directory, run the agent using the ADK CLI, specifying the core code package:
      ```bash
      adk run nifi_user_agent
      ```
      _(Check ADK documentation for preferred discovery method)_
    - Asynchronous agents can only be run from the web view, so first `cd` into the `agents` directory and run 
      ```bash
      adk web
      ```
      _(Check ADK documentation for preferred discovery method)_

4.  **Interact:** The agent will start, and you can interact with it in the terminal or web UI.
