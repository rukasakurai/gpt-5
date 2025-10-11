"""
Azure OpenAI Python sample using the openai library
Requires: pip install openai python-dotenv
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01"
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
        print("Response from Azure OpenAI:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
