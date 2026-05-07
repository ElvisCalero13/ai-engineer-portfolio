from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "AI RAG Platform API"
    environment: str = "dev"

    embedding_provider: str = "local"
    llm_provider: str = "local"

    openai_api_key: str | None = None

    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection: str = "business_documents"


settings = Settings()