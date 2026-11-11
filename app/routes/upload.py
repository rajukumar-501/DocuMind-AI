import logging
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ingestion import process_and_store_document
from app.db.metadata import save_metadata

logger = logging.getLogger(__name__)
router = APIRouter()
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDF must be 10 MB or smaller.")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid PDF.")

    # Rewind the in-memory UploadFile for the ingestion service.
    await file.seek(0)
    document_id = str(uuid.uuid4())
    try:
        chunks = await process_and_store_document(file, document_id)
        save_metadata(
            document_id=document_id,
            filename=file.filename,
            chunks=chunks,
        )
        return {
            "status": "success",
            "document_id": document_id,
            "chunk_count": len(chunks),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        logger.exception("Document upload failed")
        raise HTTPException(
            status_code=500,
            detail="Document processing failed. Check the server logs.",
        )
