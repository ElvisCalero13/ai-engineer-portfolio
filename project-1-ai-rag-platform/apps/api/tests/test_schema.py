from src.schemas.chat import ChatRequest, RetrieveRequest


def test_chat_request_default_top_k():
    request = ChatRequest(question="What is RAG?")

    assert request.question == "What is RAG?"
    assert request.top_k == 5


def test_retrieve_request_default_limit():
    request = RetrieveRequest(question="What is RAG?")

    assert request.question == "What is RAG?"
    assert request.limit == 5