import hashlib
from datetime import datetime

class MetadataEnricher:
    def enrich(self, chunks):
        enriched_chunks = []
        for i, chunk in enumerate(chunks):
            source = chunk.metadata.get("source", "unknown")
            
            # Generate a deterministic ID for deduplication
            hash_input = f"{source}_{chunk.page_content}".encode('utf-8')
            chunk_id = hashlib.sha256(hash_input).hexdigest()
            
            # Enrich metadata with project context and structural tracking
            chunk.metadata.update({
                "chunk_id": chunk_id,
                "chunk_index": i,
                "ingested_at": datetime.utcnow().isoformat(),
                "project": "BumbiroAI",
                "document_type": "Constitution_or_Legal"
            })
            enriched_chunks.append(chunk)
            
        return enriched_chunks