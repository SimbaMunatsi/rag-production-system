from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_rag_pipeline
from app.api.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest, rag=Depends(get_rag_pipeline)):
    result = rag.run(
        query=request.query,
        session_id=request.session_id
    )

    raw_sources = result.get("sources", [])
    normalized_sources = []

    for source in raw_sources:
        if isinstance(source, str):
            normalized_sources.append(source)
        elif hasattr(source, "page_content"):
            normalized_sources.append(source.page_content)
        elif isinstance(source, dict):
            if "content" in source:
                normalized_sources.append(str(source["content"]))
            else:
                normalized_sources.append(str(source))
        else:
            normalized_sources.append(str(source))

    return {
        "answer": str(result.get("answer", "")),
        "sources": normalized_sources
    }


def stream_answer(answer: str):
    for token in answer.split():
        yield token + " "


@router.post("/query-stream")
def query_stream(request: QueryRequest, rag=Depends(get_rag_pipeline)):
    result = rag.run(
        query=request.query,
        session_id=request.session_id
    )

    return StreamingResponse(
        stream_answer(str(result["answer"])),
        media_type="text/plain"
    )


@router.get("/health")
def health():
    return {"status": "ok"}