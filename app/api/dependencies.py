from app.rag.service import create_rag_pipeline
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner

_rag_pipeline = None

def get_rag_pipeline():
    global _rag_pipeline

    if _rag_pipeline is None:
        print("Initializing RAG Pipeline and building BM25 in-memory index...")
        
        # 1. Load the raw documents from your data folder
        loader = DocumentLoader("data/raw")
        raw_docs = loader.load()

        # 2. Clean them
        cleaner = DocumentCleaner()
        corpus_documents = cleaner.clean(raw_docs)

        # 3. Initialize the pipeline with the required documents
        _rag_pipeline = create_rag_pipeline(corpus_documents=corpus_documents)
        
        print("Pipeline successfully initialized!")

    return _rag_pipeline