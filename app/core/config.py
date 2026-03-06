from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # API Keys
    OPENAI_API_KEY: str
    LANGCHAIN_API_KEY: str | None = None

    # Vector Database
    CHROMA_DB_PATH: str = "./data/embeddings"

    # LangChain Tracing (optional)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "rag-production-system"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",        # prevents crashes if extra env vars exist
        case_sensitive=False
    )


settings = Settings()