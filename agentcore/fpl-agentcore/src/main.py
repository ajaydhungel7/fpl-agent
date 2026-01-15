"""
FPL Assistant wrapped for AWS Bedrock AgentCore using the official SDK.

This uses the bedrock-agentcore-sdk-python to properly integrate
with AgentCore's memory, runtime, and gateway services.
"""

import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import AgentCore SDK
try:
    from bedrock_agentcore import BedrockAgentCoreApp
except ImportError:
    print("Installing bedrock-agentcore SDK...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'bedrock-agentcore-sdk-python'])
    from bedrock_agentcore import BedrockAgentCoreApp

# Import your Strands agent
from agent import create_fpl_agent

# Create the AgentCore app wrapper
app = BedrockAgentCoreApp()

# Initialize your Strands agent
fpl_agent = create_fpl_agent()


@app.entrypoint()
def handler(request):
    """
    AgentCore entrypoint for processing requests.

    AgentCore automatically handles:
    - Memory management (conversation history)
    - Session isolation
    - Authentication
    - Observability/tracing

    Args:
        request: AgentCore request object with:
            - request.message: User's input text
            - request.session_id: Session identifier
            - request.memory: Access to AgentCore Memory service
            - request.user: User identity info

    Returns:
        Response text from the agent
    """

    # Get user input
    user_message = request.message

    print(f"Session: {request.session_id}")
    print(f"User message: {user_message}")

    # AgentCore Memory: Get conversation history (short-term memory)
    # This is automatically maintained by AgentCore across the session
    try:
        conversation_history = request.memory.get_messages(limit=10)
        print(f"Conversation history: {len(conversation_history)} messages")
    except Exception as e:
        print(f"Memory access: {e}")
        conversation_history = []

    # AgentCore Memory: Retrieve any long-term context (e.g., user's FPL team ID)
    try:
        user_team_id = request.memory.get("fpl_team_id")
        if user_team_id:
            print(f"User's FPL Team ID from memory: {user_team_id}")
            # You could set this as an env var for the agent if needed
            os.environ['FPL_TEAM_ID'] = user_team_id
    except Exception as e:
        print(f"Long-term memory access: {e}")

    # Invoke your Strands agent
    # The agent processes the request with its own internal logic
    response = fpl_agent(user_message)

    # AgentCore Memory: Store important info for future sessions (long-term memory)
    # Example: If user mentions their team ID, save it
    if "team" in user_message.lower() and any(char.isdigit() for char in user_message):
        # Extract potential team ID (simplified - you'd want better parsing)
        team_id_match = re.search(r'\b\d{6,8}\b', user_message)
        if team_id_match:
            team_id = team_id_match.group()
            try:
                request.memory.save("fpl_team_id", team_id)
                print(f"Saved team ID to long-term memory: {team_id}")
            except Exception as e:
                print(f"Failed to save to memory: {e}")

    # Note: Conversation history (short-term memory) is automatically saved by AgentCore
    # You don't need to manually save the current message/response

    return response


if __name__ == "__main__":
    # For local testing
    print("FPL Assistant AgentCore App")
    print("=" * 50)

    class MockRequest:
        def __init__(self, message):
            self.message = message
            self.session_id = "local-test"
            self.memory = None
            self.user = None

    # Test locally
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break

            request = MockRequest(user_input)
            response = handler(request)
            print(f"\nAssistant: {response}")

        except KeyboardInterrupt:
            break

    print("\nGoodbye!")
