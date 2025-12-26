"""
Azure OpenAI Python sample using the openai library
Requires: pip install openai python-dotenv
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_azure_openai_client(endpoint=None, api_key=None, api_version="2024-02-01"):
    """
    Create and return an AzureOpenAI client.
    
    Args:
        endpoint: Azure OpenAI endpoint URL. Defaults to API_ENDPOINT env var.
        api_key: API key for authentication. Defaults to API_KEY env var.
        api_version: API version to use. Defaults to "2024-02-01".
    
    Returns:
        AzureOpenAI client instance.
    """
    return AzureOpenAI(
        azure_endpoint=endpoint or os.getenv('API_ENDPOINT'),
        api_key=api_key or os.getenv("API_KEY"),
        api_version=api_version,
    )


def chat_completion(client, messages, model=None):
    """
    Make a chat completion request using the provided client.
    
    Args:
        client: AzureOpenAI client instance.
        messages: List of message dictionaries with 'role' and 'content'.
        model: Model deployment name. Defaults to MODEL_DEPLOYMENT_NAME env var.
    
    Returns:
        The response content string from the model.
    """
    response = client.chat.completions.create(
        model=model or os.getenv("MODEL_DEPLOYMENT_NAME"),
        messages=messages
    )
    return response.choices[0].message.content


def main():
    # Initialize Azure OpenAI client
    client = get_azure_openai_client()
    
    try:
        # Make a chat completion request
        response_content = chat_completion(
            client,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, GPT-5!"
                }
            ]
        )
        
        # Print the response
        print("Response from Azure OpenAI:")
        print(response_content)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
