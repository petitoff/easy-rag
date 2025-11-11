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

   # Build and start services
   docker-compose up --build

   # Run in background
   docker-compose up -d --build

The API will be available at ``http://localhost:8000`` and Qdrant at ``http://localhost:6333``.

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

      docker-compose up -d qdrant

5. **Configure environment variables (optional):**

   Create a ``.env`` file:

   .. code-block:: bash

      QDRANT_HOST=localhost
      QDRANT_GRPC_PORT=6334
      PORT=8000
      HOST=0.0.0.0

6. **Run the application:**

   .. code-block:: bash

      python -m src.main

   Or using uvicorn directly:

   .. code-block:: bash

      uvicorn src.main:app --host 0.0.0.0 --port 8000

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~~

You can configure Easy RAG using environment variables or a ``.env`` file:

* ``QDRANT_HOST``: Qdrant server host (default: ``localhost``)
* ``QDRANT_GRPC_PORT``: Qdrant gRPC port (default: ``6334``)
* ``HOST``: API server host (default: ``0.0.0.0``)
* ``PORT``: API server port (default: ``8000``)
* ``EMBED_MODEL``: HuggingFace embedding model (default: ``Qwen/Qwen3-Embedding-0.6B``)
* ``CHUNK_SIZE``: Document chunk size in characters (default: ``800``)
* ``CHUNK_OVERLAP``: Overlap between chunks (default: ``100``)
* ``BATCH_SIZE``: Batch size for processing (default: ``100``)
* ``DEFAULT_K``: Default number of results to return (default: ``8``)

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

* **Port already in use**: Change the port in ``.env`` or docker-compose.yml
* **Qdrant connection error**: Ensure Qdrant is running and accessible
* **Memory errors with large PDFs**: The batch processing should handle this, but you can reduce ``BATCH_SIZE`` if needed
* **Import errors**: Make sure all dependencies are installed: ``pip install -r requirements.txt``

