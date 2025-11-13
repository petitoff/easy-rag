# Easy RAG

[![Documentation](https://readthedocs.org/projects/easy-rag/badge/?version=latest)](https://easy-rag.readthedocs.io/en/latest/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A simple and efficient RAG (Retrieval-Augmented Generation) API built with FastAPI, Qdrant, and LangChain. Upload documents, index them using semantic embeddings, and query them using natural language.

📚 **Full Documentation**: [https://easy-rag.readthedocs.io/en/latest/](https://easy-rag.readthedocs.io/en/latest/)

## Features

- 📄 **Document Upload**: Upload PDF and text files for indexing
- ⚡ **Batch Processing**: Efficiently handles large documents (3500+ pages) with batch processing
- 🔍 **Semantic Search**: Query documents using natural language with relevance scoring
- 📑 **Page Tracking**: Results include page numbers for easy reference
- 🚀 **gRPC Communication**: Fast communication with Qdrant using gRPC protocol
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📖 **RESTful API**: Clean REST API with automatic OpenAPI documentation

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd easy-rag

# Optionally create a .env file to customize configuration
cp .env.example .env  # if available

# Build and start services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

The API will be available at `http://localhost:8000` and Qdrant at `http://localhost:6333`.

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd easy-rag

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Qdrant (using Docker)
docker-compose up -d qdrant

# Create .env file (optional)
cp .env.example .env

# Run the application
uvicorn src.easyrag.main:app --host 0.0.0.0 --port 8000
```

## Configuration

All configuration options can be set via environment variables or a `.env` file. See `.env.example` for all available options:

- **Qdrant**: `QDRANT_HOST`, `QDRANT_GRPC_PORT`, `COLLECTION_NAME`
- **Embedding Model**: `EMBED_MODEL`
- **Document Processing**: `CHUNK_SIZE`, `CHUNK_OVERLAP`, `BATCH_SIZE`
- **Retrieval**: `DEFAULT_K`, `MAX_K`
- **Server**: `HOST`, `PORT`

For detailed configuration documentation, see the [Installation Guide](https://easy-rag.readthedocs.io/en/latest/installation.html#configuration).

## Usage Examples

### Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
     -F "file=@your-document.pdf"
```

### Query Documents

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is an Amazon EC2 instance?"}'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Qdrant**: Vector database for storing embeddings
- **LangChain**: Framework for building LLM applications
- **PyMuPDF**: PDF processing with better structure preservation
- **HuggingFace**: Embedding models for semantic search

## Documentation

📚 **Full documentation is available at**: [https://easy-rag.readthedocs.io/en/latest/](https://easy-rag.readthedocs.io/en/latest/)

The documentation includes:
- [Installation Guide](https://easy-rag.readthedocs.io/en/latest/installation.html) - Detailed setup instructions
- [Usage Guide](https://easy-rag.readthedocs.io/en/latest/usage.html) - Examples and best practices
- [API Reference](https://easy-rag.readthedocs.io/en/latest/api.html) - Complete API documentation

## Requirements

- Python 3.11 or higher
- Qdrant vector database (can be run via Docker)
- 4GB+ RAM recommended for large documents
- Docker and Docker Compose (for containerized deployment)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Easy RAG** - A simple RAG API using Qdrant and LangChain
