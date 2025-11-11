"""Document processing service for loading and chunking documents."""
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader

from src.config import settings


class DocumentProcessor:
    """Service for processing documents (loading and chunking)."""
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a document from file path.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects
        """
        import os
        
        ext = file_path.lower().split(".")[-1]
        if ext == "pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = os.path.basename(file_path)
        
        return docs
    
    def chunk_documents(self, docs: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            docs: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects
        """
        return self.splitter.split_documents(docs)

