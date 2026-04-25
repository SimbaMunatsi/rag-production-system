from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

from app.core.config import settings

def get_vector_store(embeddings=None):
    if embeddings is None:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )

    # Revert back to the stable, synchronous connection string
    connection_string = settings.PGVECTOR_DATABASE_URL

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="bumbiro_constitution",
        connection=connection_string,
        use_jsonb=True, 
    )

    return vector_store