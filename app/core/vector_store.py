from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


def get_vector_store():

    embeddings = OpenAIEmbeddings()

    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store