"""
Unit tests to verify GPT-5 runtime output reasonableness.

These tests:
- Run the main code components that utilize GPT-5 from the python/ directory
- Check the runtime responses or outputs produced by GPT-5
- Assert that the responses are reasonable by using GPT-5 to evaluate the outputs
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Add parent directory to path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the actual modules from the python/ directory
import import_azureopenai
import import_openai_v0
import import_openai_v1

# Load environment variables from .env file
load_dotenv()


def evaluate_reasonableness(client, chat_fn, prompt, response):
    """
    Use GPT-5 to evaluate whether a given response is reasonable.
    
    Args:
        client: OpenAI/AzureOpenAI client instance.
        chat_fn: Function to call for chat completion (module's chat_completion function).
        prompt: The original prompt given to the AI.
        response: The AI's response to evaluate.
    
    Returns:
        A tuple of (is_reasonable: bool, explanation: str)
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
    
    evaluation_result = chat_fn(client, evaluation_messages)
    
    # Parse the result - first line should be REASONABLE or UNREASONABLE
    lines = evaluation_result.strip().split('\n')
    is_reasonable = lines[0].strip().upper() == "REASONABLE"
    explanation = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
    
    return is_reasonable, explanation


class TestImportAzureOpenAI:
    """Test the import_azureopenai module."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Skip tests if environment variables are not configured
        if not all([os.getenv("API_ENDPOINT"), os.getenv("API_KEY"), os.getenv("MODEL_DEPLOYMENT_NAME")]):
            pytest.skip("API credentials not configured. Set API_ENDPOINT, API_KEY, and MODEL_DEPLOYMENT_NAME environment variables.")
        
        self.client = import_azureopenai.get_azure_openai_client()
    
    def test_get_azure_openai_client(self):
        """Test that get_azure_openai_client returns a valid client."""
        client = import_azureopenai.get_azure_openai_client()
        assert client is not None
    
    def test_chat_completion_greeting(self):
        """Test chat_completion with a greeting prompt."""
        prompt = "Hello, GPT-5!"
        messages = [{"role": "user", "content": prompt}]
        
        response = import_azureopenai.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, import_azureopenai.chat_completion, prompt, response
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_chat_completion_factual_question(self):
        """Test chat_completion with a factual question."""
        prompt = "What is the capital of France?"
        messages = [{"role": "user", "content": prompt}]
        
        response = import_azureopenai.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, import_azureopenai.chat_completion, prompt, response
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {response}. Explanation: {explanation}"


class TestImportOpenAIV0:
    """Test the import_openai_v0 module."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Skip tests if environment variables are not configured
        if not all([os.getenv("API_ENDPOINT"), os.getenv("API_KEY"), os.getenv("MODEL_DEPLOYMENT_NAME")]):
            pytest.skip("API credentials not configured. Set API_ENDPOINT, API_KEY, and MODEL_DEPLOYMENT_NAME environment variables.")
        
        self.client = import_openai_v0.get_openai_client_v0()
    
    def test_get_openai_client_v0(self):
        """Test that get_openai_client_v0 returns a valid client."""
        client = import_openai_v0.get_openai_client_v0()
        assert client is not None
    
    def test_chat_completion_greeting(self):
        """Test chat_completion with a greeting prompt."""
        prompt = "Hello, GPT-5!"
        messages = [{"role": "user", "content": prompt}]
        
        response = import_openai_v0.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, import_openai_v0.chat_completion, prompt, response
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_chat_completion_coding_question(self):
        """Test chat_completion with a coding question."""
        prompt = "Write a simple Python function that adds two numbers."
        messages = [{"role": "user", "content": prompt}]
        
        response = import_openai_v0.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, import_openai_v0.chat_completion, prompt, response
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {response}. Explanation: {explanation}"


class TestImportOpenAIV1:
    """Test the import_openai_v1 module."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Skip tests if environment variables are not configured
        if not all([os.getenv("API_ENDPOINT"), os.getenv("API_KEY"), os.getenv("MODEL_DEPLOYMENT_NAME")]):
            pytest.skip("API credentials not configured. Set API_ENDPOINT, API_KEY, and MODEL_DEPLOYMENT_NAME environment variables.")
        
        self.client = import_openai_v1.get_openai_client_v1()
    
    def test_get_openai_client_v1(self):
        """Test that get_openai_client_v1 returns a valid client."""
        client = import_openai_v1.get_openai_client_v1()
        assert client is not None
    
    def test_chat_completion_greeting(self):
        """Test chat_completion with a greeting prompt."""
        prompt = "Hello, GPT-5!"
        messages = [{"role": "user", "content": prompt}]
        
        response = import_openai_v1.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert response is not None
        assert len(response) > 0
        
        # Use GPT-5 to evaluate the reasonableness
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, import_openai_v1.chat_completion, prompt, response
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {response}. Explanation: {explanation}"
    
    def test_chat_completion_conversation_context(self):
        """Test that GPT-5 maintains context in a multi-turn conversation."""
        messages = [
            {"role": "user", "content": "My name is Alice."},
        ]
        
        # Get first response
        first_response = import_openai_v1.chat_completion(self.client, messages)
        
        # Add context and ask a follow-up
        messages.append({"role": "assistant", "content": first_response})
        messages.append({"role": "user", "content": "What is my name?"})
        
        follow_up_response = import_openai_v1.chat_completion(self.client, messages)
        
        # Verify we got a non-empty response
        assert follow_up_response is not None
        assert len(follow_up_response) > 0
        
        # Use GPT-5 to evaluate the reasonableness of the conversation
        full_conversation = f"User: My name is Alice. Assistant: {first_response} User: What is my name? Assistant: {follow_up_response}"
        is_reasonable, explanation = evaluate_reasonableness(
            self.client, 
            import_openai_v1.chat_completion,
            "A conversation where user states their name is Alice, then asks what their name is",
            full_conversation
        )
        
        assert is_reasonable, f"Response deemed unreasonable. Response: {follow_up_response}. Explanation: {explanation}"
