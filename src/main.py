from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from pydantic import BaseModel

from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

import os
import tempfile
import uvicorn


# -----------------
# Config
# -----------------
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"
COLLECTION_NAME = "rag_store"

embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL,
    model_kwargs={"trust_remote_code": True}
)

app = FastAPI()
vectorstore = None


# -----------------
# Helpers
# -----------------
def load_document(file_path: str) -> List[Document]:
    ext = file_path.lower().split(".")[-1]
    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = os.path.basename(file_path)
    return docs


def chunk_docs(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(docs)


def ensure_vectorstore():
    global vectorstore
    if vectorstore is None:
        client = QdrantClient(url=QDRANT_URL)

        # Detect embedding size
        vector_size = len(embeddings.embed_query("test"))

        # Create collection if missing
        collections = client.get_collections().collections
        if COLLECTION_NAME not in [c.name for c in collections]:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

        vectorstore = QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
        )
    return vectorstore


# -----------------
# API Endpoints
# -----------------
class QueryRequest(BaseModel):
    query: str


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        docs = load_document(tmp_path)
        chunks = chunk_docs(docs)

        store = ensure_vectorstore()
        store.add_documents(chunks)

        return {"status": "ok", "chunks_indexed": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(tmp_path)


@app.post("/ask")
async def ask(request: QueryRequest):
    try:
        store = ensure_vectorstore()
        
        # Check if collection has any documents
        client = QdrantClient(url=QDRANT_URL)
        collection_info = client.get_collection(COLLECTION_NAME)
        if collection_info.points_count == 0:
            return {
                "query": request.query,
                "results": [],
                "message": "No documents found in the vector store. Please upload documents first."
            }
        
        # Use similarity search instead of MMR for more reliable results
        # MMR can fail if there are fewer documents than fetch_k
        retriever = store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": min(8, collection_info.points_count)}
        )
        results = retriever.invoke(request.query)

        return {
            "query": request.query,
            "results": [
                {"source": doc.metadata.get("source"), "text": doc.page_content}
                for doc in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
