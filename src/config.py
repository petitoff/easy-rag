"""Application configuration settings."""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    collection_name: str = "rag_store"

    # Embedding Model Configuration
    embed_model: str = "Qwen/Qwen3-Embedding-0.6B"

    # Document Processing Configuration
    chunk_size: int = 600
    chunk_overlap: int = 80

    # Retrieval Configuration
    default_k: int = 8
    max_k: int = 20

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
