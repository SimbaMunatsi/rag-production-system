import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings 
from app.api.dependencies import get_rag_pipeline

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT

from fastapi import FastAPI
from app.api.routes import router

# --- NEW: Lifespan event to pre-warm the RAG pipeline ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server booting up: Pre-warming BumbiroAI pipeline...")
    # By calling this here, the BM25 index builds in RAM before the server accepts traffic.
    get_rag_pipeline()
    print("BumbiroAI is fully indexed and ready to receive traffic!")
    
    yield # This tells FastAPI to run the server now
    
    print("Shutting down BumbiroAI...")

# --- Add the lifespan to the FastAPI initialization ---
app = FastAPI(
    title="Production RAG API",
    version="1.0",
    lifespan=lifespan
)

app.include_router(router)