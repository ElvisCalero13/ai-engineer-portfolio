from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class RetrieveRequest(BaseModel):
    question: str
    limit: int = 5

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5