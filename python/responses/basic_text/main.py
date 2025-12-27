"""
Azure OpenAI Responses API Python sample - Basic Text
Demonstrates a minimal text input/output request using the Responses API.
Requires: pip install openai python-dotenv
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# When using Azure API Management as the endpoint with "Subscription required",
# it is necessary to set the subscription key in the header
default_headers = {
    "api-key": os.getenv("API_KEY"),
}


def main():
    # Initialize OpenAI client configured for Azure OpenAI Responses API
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/v1/",
        default_headers=default_headers,
    )

    try:
        # Make a Responses API request
        response = client.responses.create(
            model=os.getenv("MODEL_DEPLOYMENT_NAME"),
            input="Hello, GPT-5! Please respond with a brief greeting.",
        )

        # Print the response
        print("Response from Azure OpenAI Responses API:")
        print(response.output_text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
