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
- Through API Management, not directly to Azure OpenAI Service: [Details](azure-api-management.md)

As of 2025 October 28, [the "Azure OpenAI reasoning models" page on learn.microsoft.com](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning#api--feature-support), has only "v1" under "API Version" for the GPT-5 series, while for the o-series reasoning models it lists both "v1" and "2025-04-01-preview." This seems to imply that the YYYY-MM-DD APIs are not officially supported. While as of 2025 October 28, it seems possible to call GPT-5 on Azure through the YYYY-MM-DD APIs (i.e., not v1), and I have not been able to find any official documentation that excplictly says that YYYY-MM-DD APIs cannnot be used, it would be safe to default to "v1".

As of 2025 October 28, when [looking at the code of openai-python/src/openai/lib/azure.py](openai-python.src.openai.lib.azure.py.md), it seems like the `AzureOpenAI` nor the `AsyncAzureOpenAI` clients call the "v1" API. While as of 2025 October 28, the [README of OpenAI Python API library](https://github.com/openai/openai-python?tab=readme-ov-file#microsoft-azure-openai) uses `AzureOpenAI`, the use of the `OpenAI` client seems required for using the "v1" API.

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

While the page (Authenticate and authorize access to Azure OpenAI APIs using Azure API Management)[https://learn.microsoft.com/en-us/azure/api-management/api-management-authenticate-authorize-azure-openai] exists, it currently only covers the APIM -> Azure OpenAI Service part rather than the client -> APIM part.

