"""Application configuration settings."""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Qdrant Configuration
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_grpc_port: int = int(os.getenv("QDRANT_GRPC_PORT", "6334"))
    collection_name: str = "rag_store"

    # Embedding Model Configuration
    embed_model: str = "Qwen/Qwen3-Embedding-0.6B"

    # Document Processing Configuration
    chunk_size: int = 800  # Increased for better context preservation
    chunk_overlap: int = 100  # Increased overlap for better continuity
    batch_size: int = 100

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
