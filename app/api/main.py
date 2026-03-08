import os

from dotenv import load_dotenv
load_dotenv()

from app.core.config import settings 


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Production RAG API",
    version="1.0"
)

app.include_router(router)