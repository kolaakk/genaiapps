from typing import Tuple
from openai import AzureOpenAI, OpenAI
from .settings import settings


class LLMClients:
    """
    Unified client wrapper:
    - provider: 'azure' or 'openai'
    - chat_id: deployment name (azure) or model name (openai)
    - embed_id: deployment name (azure) or model name (openai)
    """
    def __init__(self, provider: str, chat_client, embed_client, chat_id: str, embed_id: str):
        self.provider = provider
        self.chat_client = chat_client
        self.embed_client = embed_client
        self.chat_id = chat_id
        self.embed_id = embed_id


def get_llm_clients() -> LLMClients:
    provider = settings.resolved_provider()
    if provider == "none":
        raise RuntimeError(
            "No LLM provider configured. Set AZURE_OPENAI_ENDPOINT+AZURE_OPENAI_API_KEY "
            "or OPENAI_API_KEY (or set LLM_PROVIDER explicitly)."
        )

    if provider == "azure":
        if not settings.azure_openai_endpoint or not settings.azure_openai_api_key:
            raise RuntimeError("Azure provider selected but AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY missing.")

        chat_client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_api_version_chat,
        )
        embed_client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            azure_endpoint=settings.azure_openai_endpoint,
            api_version=settings.azure_api_version_embed,
        )
        return LLMClients(
            provider="azure",
            chat_client=chat_client,
            embed_client=embed_client,
            chat_id=settings.azure_chat_deployment,
            embed_id=settings.azure_embed_deployment,
        )

    # provider == "openai"
    if not settings.openai_api_key:
        raise RuntimeError("OpenAI provider selected but OPENAI_API_KEY missing.")

    kwargs = {"api_key": settings.openai_api_key}
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url

    client = OpenAI(**kwargs)
    # same client can do both chat + embeddings
    return LLMClients(
        provider="openai",
        chat_client=client,
        embed_client=client,
        chat_id=settings.openai_chat_model,
        embed_id=settings.openai_embed_model,
    )