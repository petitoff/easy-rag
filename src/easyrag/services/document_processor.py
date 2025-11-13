"""Document processing service for loading and chunking documents."""
import logging
from typing import List, Iterator
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

from easyrag.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Service for processing documents (loading and chunking)."""
    
    def __init__(self):
        # Improved separators for better chunking, especially for PDFs
        # Prioritize paragraph breaks, then sentences, then words
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n\n", "\n\n", "\n", ". ", " ", ""]  # Better handling of PDF structure
        )
    
    def load_document(self, file_path: str, original_filename: str = None) -> List[Document]:
        """
        Load a document from file path.
        
        Args:
            file_path: Path to the document file (can be temporary)
            original_filename: Original filename from user upload (used in metadata)
            
        Returns:
            List of Document objects
        """
        import os
        
        # Use original filename if provided, otherwise use file path basename
        if original_filename:
            source_name = original_filename
        else:
            source_name = os.path.basename(file_path)
        
        ext = file_path.lower().split(".")[-1]
        if ext == "pdf":
            loader = PyMuPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = source_name
        
        return docs
    
    def load_document_batched(self, file_path: str, original_filename: str = None, batch_size: int = None) -> Iterator[List[Document]]:
        """
        Load a document in batches to handle large files efficiently.
        
        For PDFs, loads pages in batches. For other files, loads the entire file.
        
        Args:
            file_path: Path to the document file (can be temporary)
            original_filename: Original filename from user upload (used in metadata)
            batch_size: Number of pages/documents to load per batch (defaults to config batch_size)
            
        Yields:
            Batches of Document objects
        """
        import os
        
        if batch_size is None:
            batch_size = settings.batch_size
        
        # Use original filename if provided, otherwise use file path basename
        if original_filename:
            source_name = original_filename
        else:
            source_name = os.path.basename(file_path)
        
        ext = file_path.lower().split(".")[-1]
        
        if ext == "pdf":
            # For PDFs, load page by page to avoid memory issues
            # PyMuPDFLoader preserves structure better for multi-column layouts and diagrams
            loader = PyMuPDFLoader(file_path)
            pages = loader.load()
            
            logger.info(f"Loading PDF with {len(pages)} pages in batches of {batch_size}")
            
            # Process pages in batches
            for i in range(0, len(pages), batch_size):
                batch = pages[i:i + batch_size]
                for idx, doc in enumerate(batch):
                    doc.metadata["source"] = source_name
                    # PyMuPDFLoader typically includes page number in metadata
                    # If not present, infer from position (1-indexed)
                    if "page" not in doc.metadata or doc.metadata["page"] is None:
                        doc.metadata["page"] = i + idx + 1
                    # Ensure page is an integer
                    try:
                        doc.metadata["page"] = int(doc.metadata["page"])
                    except (ValueError, TypeError):
                        doc.metadata["page"] = i + idx + 1
                logger.info(f"Loaded batch {i // batch_size + 1} ({len(batch)} pages)")
                yield batch
        else:
            # For non-PDF files, load normally but still yield in batches
            loader = TextLoader(file_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = source_name
            
            # Yield in batches
            for i in range(0, len(docs), batch_size):
                yield docs[i:i + batch_size]
    
    def chunk_documents(self, docs: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            docs: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        return self.splitter.split_documents(docs)
    
    def chunk_documents_batched(self, docs: List[Document]) -> List[Document]:
        """
        Split documents into chunks (same as chunk_documents, kept for consistency).
        
        Args:
            docs: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        return self.chunk_documents(docs)

