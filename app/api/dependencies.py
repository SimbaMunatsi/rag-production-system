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

def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        print("Initializing RAG Pipeline and building BM25 in-memory index...")
        loader = DocumentLoader("data/raw")
        raw_docs = loader.load()
        cleaner = DocumentCleaner()
        corpus_documents = cleaner.clean(raw_docs)
        _rag_pipeline = create_rag_pipeline(corpus_documents=corpus_documents)
        print("Pipeline successfully initialized!")
    return _rag_pipeline

# --- NEW: The Security Lock ---
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