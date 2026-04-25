from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_rag_pipeline, get_current_user
from app.api.schemas import QueryRequest, QueryResponse
from app.models.user import User
from app.core.database import get_db

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_rag(
    request: QueryRequest, 
    rag=Depends(get_rag_pipeline),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db) # <-- Get the active DB session
):
    secure_session_id = f"user_{current_user.id}_{request.session_id}"
    
    # Pass the DB session into the pipeline
    result = await rag.run(
        query=request.query,
        session_id=secure_session_id,
        db=db 
    )

    raw_sources = result.get("sources", [])
    normalized_sources = [
        source.page_content if hasattr(source, "page_content") 
        else str(source.get("content", source)) if isinstance(source, dict) 
        else str(source) 
        for source in raw_sources
    ]

    return {
        "answer": str(result.get("answer", "")),
        "sources": normalized_sources
    }

def stream_answer(answer: str):
    for token in answer.split():
        yield token + " "

@router.post("/query-stream")
async def query_stream(
    request: QueryRequest, 
    rag=Depends(get_rag_pipeline),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db) # <-- Get the active DB session
):
    secure_session_id = f"user_{current_user.id}_{request.session_id}"
    
    # Pass the DB session into the pipeline
    result = await rag.run(
        query=request.query,
        session_id=secure_session_id,
        db=db
    )

    return StreamingResponse(
        stream_answer(str(result["answer"])),
        media_type="text/plain"
    )

@router.get("/health")
def health():
    return {"status": "ok"}