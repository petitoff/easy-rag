# Project Architecture

This document describes the refactored architecture of the Easy RAG application.

## Directory Structure

```
src/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── models/                # Pydantic models/schemas
│   ├── __init__.py
│   └── schemas.py        # API request/response models
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── document_processor.py    # Document loading and chunking
│   └── vectorstore_service.py   # Qdrant vectorstore management
└── routers/               # API route handlers
    ├── __init__.py
    ├── documents.py       # Document upload and query endpoints
    └── health.py         # Health check endpoints
```

## Architecture Overview

### 1. **Configuration Layer** (`config.py`)
- Centralized configuration using Pydantic Settings
- Environment variable support
- Type-safe configuration access

### 2. **Models Layer** (`models/`)
- Pydantic models for API request/response validation
- Clear separation of data structures
- Type safety and automatic validation

### 3. **Services Layer** (`services/`)
- **DocumentProcessor**: Handles document loading and chunking
- **VectorStoreService**: Manages Qdrant connection and vector operations
- Business logic separated from API routes
- Reusable and testable components

### 4. **Routers Layer** (`routers/`)
- **documents.py**: Document upload (`/api/v1/upload`) and query (`/api/v1/ask`)
- **health.py**: Health check endpoint (`/health`)
- API endpoints organized by domain
- Clean separation of concerns

### 5. **Application Entry Point** (`main.py`)
- FastAPI app initialization
- Router registration
- Middleware configuration (CORS)
- Application metadata

## Benefits of This Architecture

1. **Separation of Concerns**: Each module has a single responsibility
2. **Testability**: Services can be easily unit tested
3. **Maintainability**: Changes are isolated to specific modules
4. **Scalability**: Easy to add new features without affecting existing code
5. **Type Safety**: Pydantic models provide runtime validation
6. **Configuration Management**: Centralized, environment-aware settings

## API Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `POST /api/v1/upload` - Upload and index documents
- `POST /api/v1/ask` - Query documents

## Running the Application

```bash
# From project root
python -m src.main

# Or with uvicorn directly
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Environment Variables

- `QDRANT_HOST` - Qdrant server host (default: localhost)
- `QDRANT_GRPC_PORT` - Qdrant gRPC port (default: 6334)
- Other settings can be configured via `.env` file or environment variables

Note: The application uses gRPC for Qdrant communication, which provides better performance than HTTP.

