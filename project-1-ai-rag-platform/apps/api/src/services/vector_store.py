from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue

from src.config import settings


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.qdrant_collection
        self.vector_size = self.get_vector_size()

    def get_vector_size(self):
        if settings.embedding_provider == "openai":
            return 1536
        return 384

    def ensure_collection(self):
        collections = self.client.get_collections().collections
        existing = [collection.name for collection in collections]

        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_documents(self, points: list[PointStruct]):
        self.ensure_collection()
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector: list[float], limit: int = 5):
        self.ensure_collection()

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
    
    def delete_by_filename(self, filename: str):
        self.ensure_collection()

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchValue(value=filename),
                    )
                ]
            ),
        )