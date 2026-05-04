from fastapi import APIRouter

from src.schemas.chat import ChatRequest, ChatResponse, RetrieveRequest
from src.services.rag_service import RagService

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    service = RagService()
    result = service.answer_question(request.question)

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )


@router.post("/retrieve")
def retrieve(request: RetrieveRequest):
    service = RagService()
    return service.retrieve_context(
        question=request.question,
        limit=request.limit,
    )