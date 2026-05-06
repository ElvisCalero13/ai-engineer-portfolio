# Traditional RAG Design

## Overview

This project implements a traditional Retrieval-Augmented Generation (RAG) architecture for answering questions over uploaded PDF documents.

The system follows a simple and production-oriented RAG flow:

```text
PDF Upload
→ Text Extraction
→ Chunking
→ Embedding Generation
→ Vector Storage
→ Semantic Retrieval
→ LLM Answer Generation