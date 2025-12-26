"""
Azure OpenAI Python sample using the standard OpenAI client
This shows how to use the standard OpenAI client to call Azure OpenAI endpoints
Requires: pip install openai python-dotenv
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_openai_client_v0(endpoint=None, api_key=None, model_deployment_name=None):
    """
    Create and return an OpenAI client configured for Azure OpenAI (v0 style endpoint).
    
    Args:
        endpoint: Azure OpenAI/APIM endpoint URL. Defaults to API_ENDPOINT env var.
        api_key: API key for authentication. Defaults to API_KEY env var.
        model_deployment_name: Model deployment name. Defaults to MODEL_DEPLOYMENT_NAME env var.
    
    Returns:
        OpenAI client instance.
    """
    endpoint = endpoint or os.getenv('API_ENDPOINT')
    api_key = api_key or os.getenv("API_KEY")
    deployment_name = model_deployment_name or os.getenv('MODEL_DEPLOYMENT_NAME')
    
    # When using Azure API Management as the endpoint with "Subscription required", 
    # it is necessary to set the subscription key in the header
    default_headers = {
        "api-key": api_key,  # Whether to use "api-key" or "Ocp-Apim-Subscription-Key" or something else depends on the settings in Azure API Management
    }
    
    return OpenAI(
        api_key=api_key,
        base_url=f"{endpoint}/openai/deployments/{deployment_name}",
        default_query={"api-version": "2024-02-01"},
        default_headers=default_headers,
    )


def chat_completion(client, messages, model=None):
    """
    Make a chat completion request using the provided client.
    
    Args:
        client: OpenAI client instance.
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
    # Initialize OpenAI client configured for Azure OpenAI
    client = get_openai_client_v0()
    
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
        print("Response from Azure OpenAI (using standard OpenAI client):")
        print(response_content)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
