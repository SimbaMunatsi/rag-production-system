import asyncio
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
    db: Session = Depends(get_db)
):
    # 1. Create a secure, isolated session ID for this specific user
    secure_session_id = f"user_{current_user.id}_{request.session_id}"
    
    # 2. Run the pipeline (Handles retrieval, agentic memory, and generation)
    result = await rag.run(
        query=request.query,
        session_id=secure_session_id,
        db=db 
    )

    # 3. Trust the pipeline! 
    # SourceFormatter already ran inside rag.run(), so these are perfectly formatted strings.
    clean_sources = result.get("sources", [])

    return {
        "answer": str(result.get("answer", "")),
        "sources": clean_sources
    }


async def simulated_stream(answer: str):
    """
    Simulates token-by-token streaming without blocking the FastAPI event loop.
    (Note: To implement TRUE generation streaming in the future, the RAGPipeline.run() 
    method itself would need to be refactored to `yield` chunks from the LLM).
    """
    for token in answer.split():
        yield token + " "
        await asyncio.sleep(0.02)  # Yields control back to the async loop for high concurrency


@router.post("/query-stream")
async def query_stream(
    request: QueryRequest, 
    rag=Depends(get_rag_pipeline),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    secure_session_id = f"user_{current_user.id}_{request.session_id}"
    
    # Await the full generation
    result = await rag.run(
        query=request.query,
        session_id=secure_session_id,
        db=db
    )

    # Stream the resulting text back to the Streamlit UI
    return StreamingResponse(
        simulated_stream(str(result["answer"])),
        media_type="text/event-stream"
    )


@router.get("/health")
def health():
    return {"status": "ok", "message": "BumbiroAI API is running."}