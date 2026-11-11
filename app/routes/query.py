import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.retrieval import retrieve_chunks
from app.services.generator import generate_answer

logger = logging.getLogger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=64)
    question: str = Field(min_length=2, max_length=2000)


@router.post("/")
async def query_document(request: QueryRequest):
    try:
        relevant_chunks = retrieve_chunks(request.document_id, request.question)
        if not relevant_chunks:
            return {"answer": "No relevant information found in the document."}

        answer = generate_answer(request.question, relevant_chunks)
        return {"answer": answer}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Document index was not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.warning("Answer generation configuration issue: %s", exc)
        raise HTTPException(status_code=503, detail="The answer service is not configured.") from exc
    except Exception:
        logger.exception("Document query failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to answer this question. Check the server logs.",
        )
