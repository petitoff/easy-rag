"""Vectorstore service for managing Qdrant vector database."""
from typing import Optional
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from src.config import settings


class VectorStoreService:
    """Service for managing the Qdrant vectorstore."""
    
    def __init__(self):
        self._vectorstore: Optional[QdrantVectorStore] = None
        self._client: Optional[QdrantClient] = None
        self._embeddings = HuggingFaceEmbeddings(
            model_name=settings.embed_model,
            model_kwargs={"trust_remote_code": True}
        )
    
    @property
    def client(self) -> QdrantClient:
        """Get or create Qdrant client."""
        if self._client is None:
            self._client = QdrantClient(url=settings.qdrant_url)
        return self._client
    
    @property
    def vectorstore(self) -> QdrantVectorStore:
        """Get or create vectorstore instance."""
        if self._vectorstore is None:
            self._ensure_collection_exists()
            self._vectorstore = QdrantVectorStore(
                client=self.client,
                collection_name=settings.collection_name,
                embedding=self._embeddings,
            )
        return self._vectorstore
    
    def _ensure_collection_exists(self) -> None:
        """Ensure the Qdrant collection exists, create if missing."""
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if settings.collection_name not in collection_names:
            # Detect embedding size
            vector_size = len(self._embeddings.embed_query("test"))
            
            # Create collection
            self.client.create_collection(
                collection_name=settings.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
    
    def get_collection_info(self):
        """Get information about the collection."""
        return self.client.get_collection(settings.collection_name)
    
    def add_documents(self, documents: list) -> None:
        """Add documents to the vectorstore."""
        self.vectorstore.add_documents(documents)
    
    def get_retriever(self, search_type: str = "similarity", k: Optional[int] = None):
        """
        Get a retriever from the vectorstore.
        
        Args:
            search_type: Type of search ("similarity" or "mmr")
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        if k is None:
            k = settings.default_k
        
        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )

