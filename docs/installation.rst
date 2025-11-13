Installation
============

This guide will help you install and set up Easy RAG on your system.

Requirements
------------

* Python 3.11 or higher
* Qdrant vector database (can be run via Docker)
* 4GB+ RAM recommended for large documents
* Docker and Docker Compose (for containerized deployment)

System Dependencies
-------------------

For PDF processing, you may need system libraries:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y build-essential

   # macOS (using Homebrew)
   brew install build-essential

Installation Methods
--------------------

Method 1: Docker Compose (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to run Easy RAG is using Docker Compose, which sets up both the RAG API and Qdrant:

.. code-block:: bash

   # Clone the repository
   git clone <repository-url>
   cd easy-rag

   # Optionally create a .env file to customize configuration
   # (see Configuration section below for all available options)
   cp .env.example .env  # if .env.example exists
   # Edit .env as needed

   # Build and start services
   docker compose up --build

   # Run in background
   docker compose up -d --build

The API will be available at ``http://localhost:8000`` and Qdrant at ``http://localhost:6333``.

**Note:** Docker Compose will automatically load environment variables from a ``.env`` file in the project root. You can also set environment variables directly in the ``docker-compose.yml`` file under the ``environment`` section for the ``rag`` service.

Method 2: Local Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For local development:

1. **Clone the repository:**

   .. code-block:: bash

      git clone <repository-url>
      cd easy-rag

2. **Create a virtual environment:**

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install dependencies:**

   .. code-block:: bash

      pip install -r requirements.txt

4. **Start Qdrant (using Docker):**

   .. code-block:: bash

      docker compose up -d qdrant

5. **Configure environment variables (optional):**

   Create a ``.env`` file in the project root. You can copy from ``.env.example`` if available, or create one with the following variables:

   .. code-block:: bash

      # Qdrant Configuration
      QDRANT_HOST=localhost
      QDRANT_GRPC_PORT=6334
      COLLECTION_NAME=rag_store

      # Embedding Model
      EMBED_MODEL=Qwen/Qwen3-Embedding-0.6B

      # Document Processing
      CHUNK_SIZE=800
      CHUNK_OVERLAP=100
      BATCH_SIZE=100

      # Retrieval Configuration
      DEFAULT_K=8
      MAX_K=20

      # Server Configuration
      HOST=0.0.0.0
      PORT=8000

6. **Run the application:**

   .. code-block:: bash

      python -m src.main

   Or using uvicorn directly:

   .. code-block:: bash

      uvicorn src.main:app --host 0.0.0.0 --port 8000

Configuration
-------------

All configuration options can be set via environment variables or a ``.env`` file. The application uses `pydantic-settings` which automatically loads variables from a ``.env`` file in the project root.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~~

You can configure Easy RAG using environment variables or a ``.env`` file. All settings are optional and have sensible defaults:

**Qdrant Configuration:**
* ``QDRANT_HOST``: Qdrant server host (default: ``localhost``)
* ``QDRANT_GRPC_PORT``: Qdrant gRPC port (default: ``6334``)
* ``COLLECTION_NAME``: Name of the Qdrant collection to use (default: ``rag_store``)

**Embedding Model Configuration:**
* ``EMBED_MODEL``: HuggingFace embedding model identifier (default: ``Qwen/Qwen3-Embedding-0.6B``)

**Document Processing Configuration:**
* ``CHUNK_SIZE``: Document chunk size in characters (default: ``800``)
  * Larger values preserve more context but may slow processing
  * Recommended range: 500-1000
* ``CHUNK_OVERLAP``: Overlap between chunks in characters (default: ``100``)
  * Helps preserve context across chunk boundaries
  * Recommended: 10-20% of CHUNK_SIZE
* ``BATCH_SIZE``: Batch size for processing documents (default: ``100``)
  * Reduce if you encounter memory issues
  * Recommended range: 50-200

**Retrieval Configuration:**
* ``DEFAULT_K``: Default number of results to return (default: ``8``)
* ``MAX_K``: Maximum number of results that can be requested (default: ``20``)

**Server Configuration:**
* ``HOST``: API server host (default: ``0.0.0.0``)
* ``PORT``: API server port (default: ``8000``)

Creating a .env File
~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file in the project root directory. Variable names are case-insensitive, so you can use uppercase, lowercase, or mixed case:

.. code-block:: bash

   # Example .env file
   QDRANT_HOST=localhost
   QDRANT_GRPC_PORT=6334
   COLLECTION_NAME=rag_store
   EMBED_MODEL=Qwen/Qwen3-Embedding-0.6B
   CHUNK_SIZE=800
   CHUNK_OVERLAP=100
   BATCH_SIZE=100
   DEFAULT_K=8
   MAX_K=20
   HOST=0.0.0.0
   PORT=8000

For Docker Compose deployments, you can also set these variables in the ``docker-compose.yml`` file under the ``environment`` section, or use a ``.env`` file that Docker Compose will automatically load.

Verification
------------

After installation, verify everything is working:

1. **Check API health:**

   .. code-block:: bash

      curl http://localhost:8000/health

2. **Access API documentation:**

   Open ``http://localhost:8000/docs`` in your browser to see the interactive API documentation.

3. **Check Qdrant:**

   Open ``http://localhost:6333/dashboard`` to access Qdrant dashboard.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

* **Port already in use**: Change the port in ``.env`` or docker-compose.yml (note: filename is still docker-compose.yml)
* **Qdrant connection error**: Ensure Qdrant is running and accessible
* **Memory errors with large PDFs**: The batch processing should handle this, but you can reduce ``BATCH_SIZE`` if needed
* **Import errors**: Make sure all dependencies are installed: ``pip install -r requirements.txt``

