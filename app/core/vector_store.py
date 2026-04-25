from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


def get_vector_store(embeddings=None):
    # If embeddings are passed from the ingestion pipeline, use them.
    # Otherwise, initialize the default embeddings (useful for your retrieval/chat scripts).
    if embeddings is None:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", # Matching the model from embedder.py
            api_key=settings.OPENAI_API_KEY
        )

    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store