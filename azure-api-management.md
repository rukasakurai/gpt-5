# Azure API Management with GPT-5
## Setting up Azure API Management
### Provisioning
Provisioning of the Azure API Management resource can be done various ways: Azure Portal GUI, Bicep, etc.
While for repeatability purposes IaC (e.g., Bicep) is preferrable, this repository as of now does not contain Bicep, and testing was done with an Azure API Management that was provisioned through the Azure Portal GUI.

### APIs
Setting up the the APIs can also be done various ways: Azure Portal GUI, Bicep, etc.
While for repeatability purposes IaC (e.g., Bicep) is preferrable, this repository as of now does not contain Bicep, and testing was done with an Azure API Management that was provisioned through the Azure Portal GUI.

#### Setting up APIs through the Azure Portal GUI
As of the "+Add API" button in the "APIs" menu of Azure API Management service shows the following options
- "HTTP: Manually define an HTTP API"
- "Language Model API: Create an API for an OpenAI API compatible model"
- "Azure OpenAI Service: Connect API Management service to Azure OpenAI - Please use 'Azure AI Foundry' import for a more updated experience"
- "Azure AI Foundry: Connect API Management services to Azure AI Foundry"

Testing with the repository was performed using an API that was created with the "Language Model API" option.