"""API routes for document management and querying."""
import os
import logging
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException

from easyrag.models.schemas import QueryRequest, QueryResponse, UploadResponse, DocumentResult
from easyrag.services.document_processor import DocumentProcessor
from easyrag.services.vectorstore_service import VectorStoreService
from easyrag.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["documents"])

# Initialize services
document_processor = DocumentProcessor()
vectorstore_service = VectorStoreService()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document.
    
    Supports PDF and text files. Large PDFs are processed in batches
    to avoid memory issues.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    total_chunks = 0
    
    try:
        logger.info(f"Starting upload of file: {file.filename}")
        
        # Process document in batches for large files
        # Pass original filename so it's preserved in metadata instead of temp filename
        batch_count = 0
        for doc_batch in document_processor.load_document_batched(tmp_path, original_filename=file.filename):
            batch_count += 1
            logger.info(f"Processing document batch {batch_count}")
            
            # Chunk the batch
            chunks = document_processor.chunk_documents(doc_batch)
            logger.info(f"Created {len(chunks)} chunks from batch {batch_count}")
            
            # Add chunks to vectorstore in batches
            if chunks:
                added = vectorstore_service.add_documents_batched(chunks)
                total_chunks += added
        
        logger.info(f"Successfully indexed {total_chunks} chunks from {file.filename}")
        
        return UploadResponse(
            status="ok",
            chunks_indexed=total_chunks
        )
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
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
        
        # Get appropriate k value
        k = min(settings.default_k, collection_info.points_count)
        
        # Use similarity_search_with_score to get relevance scores
        results_with_scores = vectorstore_service.similarity_search_with_score(
            request.query, 
            k=k
        )
        
        # Format response with scores and metadata
        formatted_results = []
        for doc, score in results_with_scores:
            # Extract page number from metadata if available
            page = doc.metadata.get("page")
            if page is not None:
                try:
                    page = int(page)
                except (ValueError, TypeError):
                    page = None
            
            formatted_results.append(
                DocumentResult(
                    source=doc.metadata.get("source"),
                    text=doc.page_content,
                    score=float(score),  # Convert to float for JSON serialization
                    page=page
                )
            )
        
        # Results are already sorted by score (highest first)
        return QueryResponse(
            query=request.query,
            results=formatted_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

