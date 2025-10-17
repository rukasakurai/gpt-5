# gpt-5

> **Note:** This repository is work in progress.

Samples of ways to call gpt-5 on Azure

## Variations

The following are key types of variations when using GPT-5, whether calling through Azure API Management or directly via Azure OpenAI Service / Azure AI Foundry:

- **Client class choice (same Python package)** (`from openai import AzureOpenAI` vs. `from openai import OpenAI`)
- **API endpoint style** (e.g., legacy endpoints vs. standardized `/v1` endpoints)
- **API version** (e.g., specific version dates, lifecycle changes)
- **Service type** (e.g., Azure OpenAI Service vs. Azure AI Foundry)
- **Authentication method** (e.g., API key vs. Azure AD token)
- **Operation surface** (e.g., Chat Completions, Responses API, Embeddings)
- **Other** (e.g., deployment vs. model naming, streaming, advanced features)
