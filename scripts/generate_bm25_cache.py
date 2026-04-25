import os
import pickle

from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner

CACHE_FILE_PATH = "data/bm25_cache.pkl"

def main():
    print("========================================")
    print("Initiating Build-Time BM25 Caching...")
    print("========================================")
    
    # 1. Load the raw documents
    print("Loading raw files...")
    loader = DocumentLoader("data/raw")
    raw_docs = loader.load()
    
    # 2. Clean and chunk the documents
    print("Cleaning and chunking documents...")
    cleaner = DocumentCleaner()
    corpus_documents = cleaner.clean(raw_docs)
    
    # 3. Save the processed chunks to a pickle file
    print("Serializing documents to disk...")
    os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)
    
    with open(CACHE_FILE_PATH, "wb") as f:
        pickle.dump(corpus_documents, f)
        
    print(f"✅ Successfully baked BM25 index to {CACHE_FILE_PATH}!")

if __name__ == "__main__":
    main()