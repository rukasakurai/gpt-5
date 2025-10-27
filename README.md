# gpt-5

> **Note:** This repository is work in progress, and may contain inaccurate/outdated information

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

### Combination 1
- **Client class choice (same Python package)**: `from openai import OpenAI`
- **API endpoint style**: `/v1`
- **Service type**: Azure OpenAI Service (NOT Azure AI Foundry)
- **Authentication method**: API key
- **Operation surface**: Chat Completions
- **Model**: GPT-5
- Through API Management, not directly to Azure OpenAI Service

Compared to directly calling Azure OpenAI Serivce, when calling through Azure API Management with `from openai import OpenAI` (instead of with  `from openai import AzureOpenAI`), the following changes needs to be applied
```diff
+ default_headers = {
+    "api-key": os.getenv("API_KEY"),
+}

    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=f"{os.getenv('API_ENDPOINT')}/openai/v1/",
+        default_headers=default_headers,
    )
```

