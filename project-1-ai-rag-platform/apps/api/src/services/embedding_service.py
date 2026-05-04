from sentence_transformers import SentenceTransformer
from openai import OpenAI

from src.config import settings


class EmbeddingService:
    def __init__(self):
        self.provider = getattr(settings, "embedding_provider", "local")

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")

            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = "text-embedding-3-small"

        else:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, text: str) -> list[float]:
        if self.provider == "openai":
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding

        else:
            embedding = self.model.encode(text)
            return embedding.tolist()