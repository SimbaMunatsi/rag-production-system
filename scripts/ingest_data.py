from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner
from app.ingestion.chunker import DocumentChunker
from app.ingestion.metadata_enricher import MetadataEnricher
from app.ingestion.embedder import EmbeddingService
from app.ingestion.vector_store_manager import VectorStoreManager
from app.ingestion.pipeline import IngestionPipeline

def main():
    # 1. Initialize data processing components
    loader = DocumentLoader("data/raw")
    cleaner = DocumentCleaner()
    chunker = DocumentChunker()
    enricher = MetadataEnricher()
    
    # 2. Explicitly initialize embeddings
    embedder = EmbeddingService()
    embeddings = embedder.get_embeddings()
    
    # 3. Pass embeddings to the vector store
    vector_store = VectorStoreManager(embeddings=embeddings)
    
    # 4. Assemble and run the deterministic pipeline
    pipeline = IngestionPipeline(
        loader=loader,
        cleaner=cleaner,
        chunker=chunker,
        enricher=enricher,
        vector_store=vector_store
    )
    
    num_chunks = pipeline.run()
    print(f"Successfully ingested and deduplicated {num_chunks} chunks for BumbiroAI.")

if __name__ == "__main__":
    main()