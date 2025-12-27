"""
Microsoft Agent Framework Python sample
Demonstrates how to use the Microsoft Agent Framework with Azure OpenAI to call GPT-5.
Reference: https://github.com/microsoft/agent-framework
Requires: pip install agent-framework python-dotenv
"""

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables from .env file
load_dotenv()


async def main():
    # Create Azure OpenAI chat client
    chat_client = AzureOpenAIChatClient(
        api_key=os.getenv("API_KEY"),
        endpoint=os.getenv("API_ENDPOINT"),
        deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
    )

    # Create a ChatAgent using the Azure OpenAI client
    agent = ChatAgent(
        chat_client=chat_client,
        instructions="You are a helpful assistant.",
    )

    try:
        # Send a message to the agent and get a response
        response = await agent.run("Hello, GPT-5!")

        # Derive a user-friendly text representation from the response
        if isinstance(response, str):
            response_text = response
        elif hasattr(response, "content"):
            response_text = response.content
        elif hasattr(response, "output"):
            response_text = response.output
        elif hasattr(response, "message"):
            # Some response types may expose a single message object
            message = response.message
            response_text = getattr(message, "content", str(message))
        elif hasattr(response, "messages"):
            # If there are multiple messages, use the last one's content if available
            messages = response.messages
            last_message = messages[-1] if messages else None
            if last_message is not None and hasattr(last_message, "content"):
                response_text = last_message.content
            else:
                response_text = str(response)
        else:
            response_text = str(response)

        # Print the response text
        print("Response from Microsoft Agent Framework:")
        print(response_text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
