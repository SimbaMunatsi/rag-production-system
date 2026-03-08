from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Production RAG API",
    version="1.0"
)

app.include_router(router)