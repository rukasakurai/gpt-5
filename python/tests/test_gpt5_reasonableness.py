"""
Unit tests to verify GPT-5 runtime output reasonableness.

These tests:
- Run the main code components that utilize GPT-5
- Check the runtime responses or outputs produced by GPT-5
- Assert that the responses are reasonable by using GPT-5 to evaluate the outputs
"""

import os
import pytest
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_openai_client():
    """Create and return an OpenAI client configured for Azure OpenAI."""
    default_headers = {
        "api-key": os.getenv("API_KEY"),
    }
    
    return OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/v1/",
        default_headers=default_headers,
    )


def call_gpt5(client, messages):
    """Make a chat completion request to GPT-5."""
    response = client.chat.completions.create(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        messages=messages
    )
    return response.choices[0].message.content


def evaluate_reasonableness(client, prompt, response):
    """
    Use GPT-5 to evaluate whether a given response is reasonable.
    
    Returns a tuple of (is_reasonable: bool, explanation: str)
    """
    evaluation_prompt = f"""You are an AI response evaluator. Your task is to evaluate whether a given AI response is reasonable and appropriate for the given prompt.

Prompt given to AI: {prompt}

AI's response: {response}

Evaluate the response and answer with ONLY "REASONABLE" or "UNREASONABLE" on the first line, followed by a brief explanation on subsequent lines.

Criteria for a reasonable response:
1. The response is relevant to the prompt
2. The response is coherent and makes sense
3. The response does not contain harmful or inappropriate content
4. The response demonstrates understanding of the prompt"""

    evaluation_messages = [
        {"role": "user", "content": evaluation_prompt}
    ]
    
    evaluation_result = call_gpt5(client, evaluation_messages)
    
    # Parse the result - first line should be REASONABLE or UNREASONABLE
    lines = evaluation_result.strip().split('\n')
    is_reasonable = lines[0].strip().upper() == "REASONABLE"
    explanation = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
    
    return is_reasonable, explanation


class TestGPT5OutputReasonableness:
    """Test class for GPT-5 output reasonableness verification."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Skip tests if environment variables are not configured
        if not all([os.getenv("API_ENDPOINT"), os.getenv("API_KEY"), os.getenv("MODEL_DEPLOYMENT_NAME")]):
            pytest.skip("API credentials not configured. Set API_ENDPOINT, API_KEY, and MODEL_DEPLOYMENT_NAME environment variables.")
        
        self.client = get_openai_client()
    
    def test_greeting_response(self):
        """Test that GPT-5 responds reasonably to a simple greeting."""
        prompt = "Hello, GPT-5!"
        messages = [{"role": "user", "content": prompt}]
        
        response = call_gpt5(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(self.client, prompt, response)
        
        assert is_reasonable, f"GPT-5 response was deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_factual_question_response(self):
        """Test that GPT-5 responds reasonably to a factual question."""
        prompt = "What is the capital of France?"
        messages = [{"role": "user", "content": prompt}]
        
        response = call_gpt5(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(self.client, prompt, response)
        
        assert is_reasonable, f"GPT-5 response was deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_coding_question_response(self):
        """Test that GPT-5 responds reasonably to a coding question."""
        prompt = "Write a simple Python function that adds two numbers."
        messages = [{"role": "user", "content": prompt}]
        
        response = call_gpt5(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(self.client, prompt, response)
        
        assert is_reasonable, f"GPT-5 response was deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_conversation_context(self):
        """Test that GPT-5 maintains context in a multi-turn conversation."""
        messages = [
            {"role": "user", "content": "My name is Alice."},
        ]
        
        # Get first response
        first_response = call_gpt5(self.client, messages)
        
        # Add context and ask a follow-up
        messages.append({"role": "assistant", "content": first_response})
        messages.append({"role": "user", "content": "What is my name?"})
        
        follow_up_response = call_gpt5(self.client, messages)
        
        # Verify we got a non-empty response
        assert follow_up_response is not None
        assert len(follow_up_response) > 0
        
        # Use GPT-5 to evaluate the reasonableness of the conversation
        full_conversation = f"""
Conversation:
User: My name is Alice.
Assistant: {first_response}
User: What is my name?
Assistant: {follow_up_response}
"""
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, 
            "A conversation where user states their name is Alice, then asks what their name is",
            follow_up_response
        )
        
        assert is_reasonable, f"GPT-5 response was deemed unreasonable. Response: {follow_up_response}. Explanation: {explanation}"
