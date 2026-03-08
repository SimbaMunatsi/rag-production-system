from app.rag.service import create_rag_pipeline

_rag_pipeline = None


def get_rag_pipeline():
    global _rag_pipeline

    if _rag_pipeline is None:
        _rag_pipeline = create_rag_pipeline()

    return _rag_pipeline