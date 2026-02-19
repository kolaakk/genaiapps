from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # App
    app_env: str = Field(default="local", alias="APP_ENV")
    api_key: str = Field(default="change-me", alias="APP_API_KEY")
    #cors_origins: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
    cors_origins: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
    max_input_chars: int = Field(default=12000, alias="MAX_INPUT_CHARS")

    # Provider selection
    # - "auto" (default): use Azure if AZURE_OPENAI_ENDPOINT is set, else OpenAI if OPENAI_API_KEY is set
    # - "azure": force Azure OpenAI
    # - "openai": force standard OpenAI
    llm_provider: str = Field(default="auto", alias="LLM_PROVIDER")

    # -------- Azure OpenAI --------
    azure_openai_endpoint: str | None = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str | None = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    azure_chat_deployment: str = Field(default="gpt-4o-mini", alias="AZURE_OPENAI_CHAT_DEPLOYMENT")
    azure_embed_deployment: str = Field(default="text-embedding-3-large", alias="AZURE_OPENAI_EMBED_DEPLOYMENT")
    azure_api_version_chat: str = Field(default="2024-08-01-preview", alias="AZURE_OPENAI_API_VERSION_CHAT")
    azure_api_version_embed: str = Field(default="2023-05-15", alias="AZURE_OPENAI_API_VERSION_EMBED")

    # -------- Standard OpenAI --------
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_chat_model: str = Field(default="gpt-4o-mini", alias="OPENAI_CHAT_MODEL")
    openai_embed_model: str = Field(default="text-embedding-3-large", alias="OPENAI_EMBED_MODEL")

    # Optional: for proxies/self-hosted gateways
    openai_base_url: str | None = Field(default=None, alias="OPENAI_BASE_URL")

    class Config:
        case_sensitive = False

    def resolved_provider(self) -> str:
        p = (self.llm_provider or "auto").lower().strip()
        if p in {"azure", "openai"}:
            return p

        # auto
        if self.azure_openai_endpoint and self.azure_openai_api_key:
            return "azure"
        if self.openai_api_key:
            return "openai"
        return "none"


settings = Settings()