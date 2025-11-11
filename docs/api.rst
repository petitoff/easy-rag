API Reference
==============

This section provides detailed documentation for all API endpoints in Easy RAG.

Base URL
--------

All API endpoints are prefixed with ``/api/v1``:

* Development: ``http://localhost:8000/api/v1``
* Production: ``https://your-domain.com/api/v1``

Authentication
--------------

Currently, Easy RAG does not require authentication. For production deployments, consider adding authentication middleware.

Endpoints
---------

Upload Document
~~~~~~~~~~~~~~~

Upload and index a document for semantic search.

**Endpoint:** ``POST /api/v1/upload``

**Content-Type:** ``multipart/form-data``

**Parameters:**

* ``file`` (required): The document file to upload (PDF or text file)

**Request Example:**

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"

**Response:**

.. code-block:: json

   {
     "status": "ok",
     "chunks_indexed": 1250
   }

**Response Fields:**

* ``status`` (string): Status of the upload operation (always "ok" on success)
* ``chunks_indexed`` (integer): Number of document chunks created and indexed

**Status Codes:**

* ``200 OK``: Document uploaded and indexed successfully
* ``500 Internal Server Error``: Error processing the document

**Notes:**

* Large PDFs (3500+ pages) are automatically processed in batches
* Original filename is preserved in document metadata
* Processing progress is logged for monitoring

Query Documents
~~~~~~~~~~~~~~~

Query the indexed documents using semantic search.

**Endpoint:** ``POST /api/v1/ask``

**Content-Type:** ``application/json``

**Request Body:**

.. code-block:: json

   {
     "query": "What is an Amazon EC2 instance?"
   }

**Request Fields:**

* ``query`` (string, required): The natural language query to search for

**Response:**

.. code-block:: json

   {
     "query": "What is an Amazon EC2 instance?",
     "results": [
       {
         "source": "aws-ec2-guide.pdf",
         "text": "An Amazon EC2 instance is a virtual server in the AWS cloud environment...",
         "score": 0.8358426094055176,
         "page": 320
       },
       {
         "source": "aws-ec2-guide.pdf",
         "text": "Amazon EC2 provides a wide range of instance types...",
         "score": 0.8067034482955933,
         "page": 22
       }
     ],
     "message": null
   }

**Response Fields:**

* ``query`` (string): The original query
* ``results`` (array): Array of document results, sorted by relevance
* ``message`` (string, optional): Informational message (e.g., when no documents are found)

**Result Object Fields:**

* ``source`` (string): Original filename of the document
* ``text`` (string): The relevant text chunk from the document
* ``score`` (float): Relevance score (higher = more relevant, typically 0.7-0.9)
* ``page`` (integer, optional): Page number in the source document

**Status Codes:**

* ``200 OK``: Query executed successfully
* ``500 Internal Server Error``: Error executing the query

**Notes:**

* Results are sorted by relevance score (highest first)
* Default number of results is 8 (configurable via ``DEFAULT_K``)
* Scores are cosine similarity scores (higher is better)

Health Check
~~~~~~~~~~~~

Check the health status of the API and Qdrant connection.

**Endpoint:** ``GET /health``

**Request Example:**

.. code-block:: bash

   curl http://localhost:8000/health

**Response:**

.. code-block:: json

   {
     "status": "healthy",
     "qdrant_connected": true,
     "documents_count": 1250
   }

**Response Fields:**

* ``status`` (string): Health status ("healthy" or "unhealthy")
* ``qdrant_connected`` (boolean): Whether Qdrant is accessible
* ``documents_count`` (integer): Total number of indexed document chunks

Root Endpoint
~~~~~~~~~~~~~

Get API information and version.

**Endpoint:** ``GET /``

**Request Example:**

.. code-block:: bash

   curl http://localhost:8000/

**Response:**

.. code-block:: json

   {
     "message": "Easy RAG API",
     "version": "1.0.0",
     "docs": "/docs"
   }

Error Responses
---------------

All endpoints may return error responses in the following format:

.. code-block:: json

   {
     "detail": "Error message describing what went wrong"
   }

Common Error Codes:

* ``400 Bad Request``: Invalid request parameters
* ``404 Not Found``: Endpoint not found
* ``500 Internal Server Error``: Server-side error

Rate Limiting
-------------

Currently, Easy RAG does not implement rate limiting. For production deployments, consider adding rate limiting middleware.

Interactive Documentation
-------------------------

Easy RAG provides interactive API documentation:

* **Swagger UI**: ``http://localhost:8000/docs``
  - Interactive API explorer
  - Try out endpoints directly from the browser
  - View request/response schemas

* **ReDoc**: ``http://localhost:8000/redoc``
  - Alternative documentation interface
  - Clean, readable format

Data Models
-----------

QueryRequest
~~~~~~~~~~~~

.. code-block:: python

   {
     "query": str  # Required: The search query
   }

QueryResponse
~~~~~~~~~~~~~

.. code-block:: python

   {
     "query": str,
     "results": List[DocumentResult],
     "message": Optional[str]
   }

DocumentResult
~~~~~~~~~~~~~~

.. code-block:: python

   {
     "source": Optional[str],      # Original filename
     "text": str,                   # Document text chunk
     "score": Optional[float],      # Relevance score
     "page": Optional[int]          # Page number
   }

UploadResponse
~~~~~~~~~~~~~~

.. code-block:: python

   {
     "status": str,                 # "ok" on success
     "chunks_indexed": int          # Number of chunks created
   }

