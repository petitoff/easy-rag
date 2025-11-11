"""Main application entry point."""

import sys
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config import settings
from src.routers import documents, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="Easy RAG API",
    description="A simple RAG (Retrieval-Augmented Generation) API using Qdrant and LangChain",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router)
app.include_router(health.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Easy RAG API", "version": "1.0.0", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
