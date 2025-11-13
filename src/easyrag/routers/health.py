"""Health check and status endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel

from easyrag.services.vectorstore_service import VectorStoreService
from easyrag.config import settings

router = APIRouter(tags=["health"])

vectorstore_service = VectorStoreService()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    qdrant_connected: bool
    collection_name: str
    documents_count: int


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health status of the application and Qdrant connection."""
    try:
        collection_info = vectorstore_service.get_collection_info()
        return HealthResponse(
            status="healthy",
            qdrant_connected=True,
            collection_name=settings.collection_name,
            documents_count=collection_info.points_count
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            qdrant_connected=False,
            collection_name=settings.collection_name,
            documents_count=0
        )

