"""API routes for document management and querying."""
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.models.schemas import QueryRequest, QueryResponse, UploadResponse, DocumentResult
from src.services.document_processor import DocumentProcessor
from src.services.vectorstore_service import VectorStoreService
from src.config import settings

router = APIRouter(prefix="/api/v1", tags=["documents"])

# Initialize services
document_processor = DocumentProcessor()
vectorstore_service = VectorStoreService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document.
    
    Supports PDF and text files.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    try:
        # Load and process document
        docs = document_processor.load_document(tmp_path)
        chunks = document_processor.chunk_documents(docs)
        
        # Add to vectorstore
        vectorstore_service.add_documents(chunks)
        
        return UploadResponse(
            status="ok",
            chunks_indexed=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(tmp_path)


@router.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Query the document store using semantic search.
    
    Returns the most relevant document chunks for the given query.
    """
    try:
        # Check if collection has any documents
        collection_info = vectorstore_service.get_collection_info()
        
        if collection_info.points_count == 0:
            return QueryResponse(
                query=request.query,
                results=[],
                message="No documents found in the vector store. Please upload documents first."
            )
        
        # Get retriever with appropriate k value
        k = min(settings.default_k, collection_info.points_count)
        retriever = vectorstore_service.get_retriever(
            search_type="similarity",
            k=k
        )
        
        # Retrieve relevant documents
        results = retriever.invoke(request.query)
        
        # Format response
        return QueryResponse(
            query=request.query,
            results=[
                DocumentResult(
                    source=doc.metadata.get("source"),
                    text=doc.page_content
                )
                for doc in results
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

