Usage
=====

This guide will help you get started with Easy RAG and show you how to use its features.

Quick Start
-----------

1. **Start the services:**

   .. code-block:: bash

      docker compose up -d

2. **Upload a document:**

   .. code-block:: bash

      curl -X POST "http://localhost:8000/api/v1/upload" \
           -H "accept: application/json" \
           -H "Content-Type: multipart/form-data" \
           -F "file=@your-document.pdf"

3. **Query the documents:**

   .. code-block:: bash

      curl -X POST "http://localhost:8000/api/v1/ask" \
           -H "accept: application/json" \
           -H "Content-Type: application/json" \
           -d '{"query": "What is an Amazon EC2 instance?"}'

Uploading Documents
-------------------

Supported Formats
~~~~~~~~~~~~~~~~~

* PDF files (recommended: uses PyMuPDF for better structure preservation)
* Text files (.txt)

Large Document Support
~~~~~~~~~~~~~~~~~~~~~~

Easy RAG can handle large documents efficiently:

* **Batch Processing**: Documents are processed in batches to avoid memory issues
* **3500+ Pages**: Successfully tested with PDFs containing 3500+ pages
* **Automatic Chunking**: Documents are automatically split into optimal chunks
* **Progress Logging**: Monitor processing progress through logs

Example: Upload a PDF
~~~~~~~~~~~~~~~~~~~~~

Using curl:

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/upload" \
        -F "file=@aws-ec2-guide.pdf"

Response:

.. code-block:: json

   {
     "status": "ok",
     "chunks_indexed": 1250
   }

Using Python:

.. code-block:: python

   import requests

   url = "http://localhost:8000/api/v1/upload"
   files = {"file": open("aws-ec2-guide.pdf", "rb")}
   response = requests.post(url, files=files)
   print(response.json())

Using JavaScript/Node.js:

.. code-block:: javascript

   const FormData = require('form-data');
   const fs = require('fs');
   const axios = require('axios');

   const form = new FormData();
   form.append('file', fs.createReadStream('aws-ec2-guide.pdf'));

   axios.post('http://localhost:8000/api/v1/upload', form, {
     headers: form.getHeaders()
   })
   .then(response => console.log(response.data))
   .catch(error => console.error(error));

Querying Documents
------------------

Basic Query
~~~~~~~~~~~

Query your documents using natural language:

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/ask" \
        -H "Content-Type: application/json" \
        -d '{"query": "What is an Amazon EC2 instance?"}'

Response:

.. code-block:: json

   {
     "query": "What is an Amazon EC2 instance?",
     "results": [
       {
         "source": "aws-ec2-guide.pdf",
         "text": "An Amazon EC2 instance is a virtual server...",
         "score": 0.8358426094055176,
         "page": 320
       },
       ...
     ]
   }

Understanding Results
~~~~~~~~~~~~~~~~~~~~~

Each result includes:

* **source**: Original filename of the document
* **text**: The relevant text chunk
* **score**: Relevance score (higher = more relevant, typically 0.7-0.9 for good matches)
* **page**: Page number in the source document (if available)

Results are sorted by relevance score (highest first).

Python Example
~~~~~~~~~~~~~~

.. code-block:: python

   import requests

   url = "http://localhost:8000/api/v1/ask"
   payload = {"query": "What are the different EC2 instance types?"}
   response = requests.post(url, json=payload)
   
   results = response.json()["results"]
   for result in results:
       print(f"Score: {result['score']:.3f}")
       print(f"Page: {result.get('page', 'N/A')}")
       print(f"Text: {result['text'][:200]}...")
       print("-" * 50)

JavaScript Example
~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   const axios = require('axios');

   axios.post('http://localhost:8000/api/v1/ask', {
     query: 'What are the different EC2 instance types?'
   })
   .then(response => {
     response.data.results.forEach(result => {
       console.log(`Score: ${result.score.toFixed(3)}`);
       console.log(`Page: ${result.page || 'N/A'}`);
       console.log(`Text: ${result.text.substring(0, 200)}...`);
       console.log('-'.repeat(50));
     });
   });

Best Practices
--------------

Query Optimization
~~~~~~~~~~~~~~~~~~

* **Be specific**: More specific queries yield better results
* **Use keywords**: Include relevant technical terms
* **Ask complete questions**: Full questions work better than single words

Document Preparation
~~~~~~~~~~~~~~~~~~~

* **Use structured PDFs**: Well-formatted PDFs produce better results
* **Avoid scanned PDFs**: Text-based PDFs work better than scanned images
* **Multiple documents**: Upload multiple related documents for comprehensive search

Performance Tips
~~~~~~~~~~~~~~~

* **Batch size**: Adjust ``BATCH_SIZE`` for your system's memory
* **Chunk size**: Larger chunks (800-1000) preserve more context
* **Result limit**: Use appropriate ``default_k`` based on your needs

API Documentation
------------------

Interactive API documentation is available at:

* **Swagger UI**: ``http://localhost:8000/docs``
* **ReDoc**: ``http://localhost:8000/redoc``

Health Check
------------

Check if the API is running:

.. code-block:: bash

   curl http://localhost:8000/health

Response:

.. code-block:: json

   {
     "status": "healthy",
     "qdrant_connected": true,
     "documents_count": 1250
   }

