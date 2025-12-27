"""
Azure OpenAI Responses API Python sample - Tool/Function Calling
Demonstrates how to use tool/function calling with the Responses API.
Requires: pip install openai python-dotenv
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# When using Azure API Management as the endpoint with "Subscription required",
# it is necessary to set the subscription key in the header
default_headers = {
    "api-key": os.getenv("API_KEY"),
}

# Define a tool/function for the model to call
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name (e.g., London, Paris, Tokyo)"
                }
            },
            "required": ["city"]
        }
    }
]


def get_weather(city):
    """Simulated weather function - in production, call a real weather API."""
    weather_data = {
        "London": {"temperature": "12°C", "condition": "Cloudy"},
        "Paris": {"temperature": "15°C", "condition": "Sunny"},
        "Tokyo": {"temperature": "18°C", "condition": "Clear"},
        "New York": {"temperature": "10°C", "condition": "Rainy"},
    }
    data = weather_data.get(city, {"temperature": "Unknown", "condition": "Unknown"})
    return json.dumps({"city": city, **data})


def main():
    # Initialize OpenAI client configured for Azure OpenAI Responses API
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/v1/",
        default_headers=default_headers,
    )

    try:
        # Make a Responses API request with tools
        response = client.responses.create(
            model=os.getenv("MODEL_DEPLOYMENT_NAME"),
            tools=tools,
            input="What's the weather like in London?",
        )

        # Process tool calls if any
        input_items = []
        for item in response.output:
            if item.type == "function_call":
                # Execute the function
                try:
                    args = json.loads(item.arguments)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Invalid JSON in tool arguments for '{item.name}': {item.arguments}"
                    ) from e
                if not isinstance(args, dict) or "city" not in args:
                    print(f"Skipping function call {item.name}: missing required 'city' argument in {args}")
                    continue
                city = args["city"]
                result = get_weather(city)
                print(f"Function called: {item.name}({args})")
                print(f"Function result: {result}")

                # Add function result to conversation
                input_items.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result
                })

        # If there were tool calls, get the final response
        if input_items:
            final_response = client.responses.create(
                model=os.getenv("MODEL_DEPLOYMENT_NAME"),
                input=input_items,
                previous_response_id=response.id,
            )
            print("\nFinal response from Azure OpenAI Responses API:")
            print(final_response.output_text)
        else:
            print("\nResponse from Azure OpenAI Responses API:")
            print(response.output_text)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
