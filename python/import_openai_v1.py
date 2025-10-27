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

# TODO (Double chekc): Verify if "api-key" header is needed
default_headers = {
    "api-key": os.getenv("API_KEY"),
#    "Ocp-Apim-Subscription-Key": os.getenv("AZURE_OPENAI_API_KEY"), # Results in `Error: Error code: 401 - {'statusCode': 401, 'message': 'Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API.'}` with this
}

def main():
    # Initialize OpenAI client configured for Azure OpenAI
    client = OpenAI(
        api_key=os.getenv("API_KEY"), # When the endpoint is Azure API Management, the value does not matter, but it is required to set it.
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/v1/",
        default_headers=default_headers, # TODO (Double chekc): Verify if needed
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
