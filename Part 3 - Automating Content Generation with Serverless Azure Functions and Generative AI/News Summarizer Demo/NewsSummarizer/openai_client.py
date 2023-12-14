import os
from openai import AzureOpenAI

# Setting the OPENAI details
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-09-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)