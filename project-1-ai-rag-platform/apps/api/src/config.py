from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI RAG Platform API"
    environment: str = "dev"
    embedding_provider: str = "local"

    openai_api_key: str | None = None

    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection: str = "business_documents"

    class Config:
        env_file = ".env"


settings = Settings()