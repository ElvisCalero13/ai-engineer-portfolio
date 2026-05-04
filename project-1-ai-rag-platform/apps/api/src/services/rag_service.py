import uuid
from pypdf import PdfReader
from qdrant_client.models import PointStruct

from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.services.llm_service import LlmService

class RagService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LlmService()

    def extract_text_from_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        return text.strip()

    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    def ingest_pdf(self, file_path: str, filename: str) -> dict:
        text = self.extract_text_from_pdf(file_path)

        if not text:
            return {
                "filename": filename,
                "status": "failed",
                "message": "No text could be extracted from the PDF.",
                "chunks": 0,
            }

        chunks = self.chunk_text(text)
        points = []

        for index, chunk in enumerate(chunks):
            vector = self.embedding_service.embed_text(chunk)

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "filename": filename,
                        "chunk_index": index,
                        "text": chunk,
                    },
                )
            )

        self.vector_store.upsert_documents(points)

        return {
            "filename": filename,
            "status": "indexed",
            "chunks": len(chunks),
        }
    
    def answer_question(self, question: str) -> dict:
        query_vector = self.embedding_service.embed_text(question)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=5,
        )

        contexts = []
        sources = []

        for result in results:
            payload = result.payload or {}
            text = payload.get("text", "")
            filename = payload.get("filename", "unknown")
            chunk_index = payload.get("chunk_index", "unknown")

            if text:
                contexts.append(text)
                sources.append(f"{filename} - chunk {chunk_index}")

        context = "\n\n---\n\n".join(contexts)

        answer = self.llm_service.generate_answer(
            question=question,
            context=context,
        )

        return {
            "answer": answer,
            "sources": sources,
        }
    
    def retrieve_context(self, question: str, limit: int = 5) -> dict:
        query_vector = self.embedding_service.embed_text(question)

        results = self.vector_store.search(
            query_vector=query_vector,
            limit=limit,
        )

        chunks = []

        for result in results:
            payload = result.payload or {}

            chunks.append({
                "score": result.score,
                "filename": payload.get("filename", "unknown"),
                "chunk_index": payload.get("chunk_index", "unknown"),
                "text": payload.get("text", ""),
            })

        return {
            "question": question,
            "results": chunks,
        }