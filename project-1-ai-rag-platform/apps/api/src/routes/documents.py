import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.services.rag_service import RagService

router = APIRouter()

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported for now.",
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    service = RagService()
    result = service.ingest_pdf(file_path=file_path, filename=file.filename)

    return result