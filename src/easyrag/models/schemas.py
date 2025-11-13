"""Pydantic models for API request/response schemas."""
from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    query: str


class DocumentResult(BaseModel):
    """Model for a single document result."""
    source: Optional[str]
    text: str
    score: Optional[float] = None  # Relevance score (higher is better)
    page: Optional[int] = None  # Page number if available


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    query: str
    results: List[DocumentResult]
    message: Optional[str] = None


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    status: str
    chunks_indexed: int

