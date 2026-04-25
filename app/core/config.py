import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Set LangChain environment variables before initializing settings
os.environ["LANGCHAIN_TRACING_COMPRESSION"] = "false"

class Settings(BaseSettings):
    # Model provider
    OPENAI_API_KEY: str

    # LangSmith Observability
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_TRACING: str = "true"
    LANGSMITH_PROJECT: str = "rag-production-system"
    LANGSMITH_ENDPOINT: str = "https://eu.api.smith.langchain.com"

    # Relational Database & Vector Store (PostgreSQL + pgvector)
    DATABASE_URL: str
    PGVECTOR_DATABASE_URL: str

    # Security & Authentication
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        case_sensitive=False
    )

settings = Settings()