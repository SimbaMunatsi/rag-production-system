import os
import pickle
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from app.rag.service import create_rag_pipeline
from app.ingestion.document_loader import DocumentLoader
from app.ingestion.document_cleaner import DocumentCleaner
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User

_rag_pipeline = None
# Define a path to save the cached BM25 index
CACHE_FILE_PATH = "data/bm25_cache.pkl"

def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        print("Initializing RAG Pipeline...")
        
        # --- THE FIX: Check for a cached index on the hard drive ---
        if os.path.exists(CACHE_FILE_PATH):
            print("Loading BM25 index from disk cache (Lightning Fast)...")
            with open(CACHE_FILE_PATH, "rb") as f:
                corpus_documents = pickle.load(f)
        else:
            print("No cache found. Building BM25 index from raw files (Slow)...")
            loader = DocumentLoader("data/raw")
            raw_docs = loader.load()
            cleaner = DocumentCleaner()
            corpus_documents = cleaner.clean(raw_docs)
            
            # Save the cleaned, processed documents to disk for next time
            os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)
            with open(CACHE_FILE_PATH, "wb") as f:
                pickle.dump(corpus_documents, f)
            print("Saved BM25 index to disk cache for future reboots.")

        _rag_pipeline = create_rag_pipeline(corpus_documents=corpus_documents)
        print("Pipeline successfully initialized!")
        
    return _rag_pipeline

# --- Security Lock ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
        
    return user