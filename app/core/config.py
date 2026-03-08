import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Model provider
    OPENAI_API_KEY: str

    # LangSmith
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_TRACING: str="true"
    LANGSMITH_PROJECT: str = "rag-production-system"
    LANGSMITH_ENDPOINT: str = "https://eu.api.smith.langchain.com"
    # Add this to your environment variables
    os.environ["LANGCHAIN_TRACING_COMPRESSION"] = "false"
    #LANGSMITH_WORKSPACE_ID: str | None = None

    # Vector DB
    CHROMA_DB_PATH: str = "./data/embeddings"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
        case_sensitive=False
    )


settings = Settings()