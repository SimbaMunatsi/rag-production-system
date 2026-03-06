from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner
from app.ingestion.chunker import DocumentChunker
from app.ingestion.vector_store_manager import VectorStoreManager
from app.ingestion.pipeline import IngestionPipeline


loader = DocumentLoader("data/raw")

cleaner = DocumentCleaner()

chunker = DocumentChunker()

vector_store = VectorStoreManager()


pipeline = IngestionPipeline(
    loader,
    cleaner,
    chunker,
    vector_store
)


num_chunks = pipeline.run()

print(f"Ingested {num_chunks} chunks")