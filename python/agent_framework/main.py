"""
Microsoft Agent Framework Python sample using Semantic Kernel
Demonstrates how to use the Microsoft Agent Framework with Azure OpenAI to call GPT-5.
Requires: pip install semantic-kernel python-dotenv
"""

import asyncio
import os

from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables from .env file
load_dotenv()


async def main():
    # Create Azure OpenAI chat completion service
    service = AzureChatCompletion(
        deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
        endpoint=os.getenv("API_ENDPOINT"),
        api_key=os.getenv("API_KEY"),
    )

    # Create a ChatCompletionAgent using the Azure OpenAI service
    agent = ChatCompletionAgent(
        service=service,
        name="GPT5-Assistant",
        instructions="You are a helpful assistant.",
    )

    try:
        # Send a message to the agent and get a response
        response = await agent.get_response(messages="Hello, GPT-5!")

        # Print the response
        print("Response from Microsoft Agent Framework (Semantic Kernel):")
        print(response.content)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
