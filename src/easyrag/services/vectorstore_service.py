"""Vectorstore service for managing Qdrant vector database."""
import logging
from typing import Optional, List
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

from easyrag.config import settings

logger = logging.getLogger(__name__)


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
        """Get or create Qdrant client using gRPC."""
        if self._client is None:
            self._client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_grpc_port,
                prefer_grpc=True
            )
            logger.info(f"Initialized Qdrant client using gRPC at {settings.qdrant_host}:{settings.qdrant_grpc_port}")
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
    
    def add_documents_batched(self, documents: List, batch_size: int = None) -> int:
        """
        Add documents to the vectorstore in batches to handle large document sets.
        
        Args:
            documents: List of Document objects to add
            batch_size: Number of documents to process per batch (defaults to config batch_size)
            
        Returns:
            Total number of documents added
        """
        if batch_size is None:
            batch_size = settings.batch_size
        
        total_added = 0
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        logger.info(f"Adding {len(documents)} documents in {total_batches} batches of {batch_size}")
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            try:
                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} documents)")
                self.vectorstore.add_documents(batch)
                total_added += len(batch)
                logger.info(f"Successfully added batch {batch_num}/{total_batches}")
            except Exception as e:
                logger.error(f"Error adding batch {batch_num}/{total_batches}: {str(e)}")
                raise
        
        logger.info(f"Successfully added all {total_added} documents to vectorstore")
        return total_added
    
    def similarity_search_with_score(self, query: str, k: Optional[int] = None):
        """
        Perform similarity search and return results with scores.
        
        Args:
            query: Query string
            k: Number of documents to retrieve
            
        Returns:
            List of tuples (Document, score)
        """
        if k is None:
            k = settings.default_k
        
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
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

