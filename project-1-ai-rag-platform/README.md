# Project 1 — Traditional AI RAG Platform

End-to-end traditional RAG platform for answering questions over uploaded PDF documents.

## Tech Stack

- FastAPI
- Qdrant
- OpenAI / local embeddings
- Docker Compose
- Python
- GitHub Actions

## Architecture

```text
PDF Upload
→ Text Extraction
→ Chunking
→ Embeddings
→ Qdrant Vector Store
→ Semantic Retrieval
→ LLM Answer