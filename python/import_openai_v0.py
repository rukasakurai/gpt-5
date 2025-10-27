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

# When using Azure API Management as the endpoint with "Subscription required", it is necessary to set the subscription key in the header
default_headers = {
    "api-key": os.getenv("API_KEY"), # Whether to use "api-key" or "Ocp-Apim-Subscription-Key" or something else depends on the settings in Azure API Management
}

def main():
    # Initialize OpenAI client configured for Azure OpenAI
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/deployments/{os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}",
        default_query={"api-version": "2024-02-01"},
        default_headers=default_headers, # When using Azure API Management as the endpoint with "Subscription required", it is necessary to set the subscription key in the header
    )
    
    try:
        # Make a chat completion request
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {
                    "role": "user",
                    "content": "Hello, GPT-5!"
                }
            ]
        )
        
        # Print the response
        print("Response from Azure OpenAI (using standard OpenAI client):")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
