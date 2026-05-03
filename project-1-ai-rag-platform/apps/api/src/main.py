from fastapi import FastAPI

from src.routes.health import router as health_router
from src.routes.chat import router as chat_router
from src.routes.documents import router as documents_router
from src.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(documents_router, prefix="/documents", tags=["documents"])


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "environment": settings.environment,
        "status": "running",
    }