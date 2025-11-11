.. Easy RAG documentation master file

Welcome to Easy RAG's documentation!
=====================================

Easy RAG is a simple and efficient RAG (Retrieval-Augmented Generation) API built with FastAPI, Qdrant, and LangChain. It enables you to upload documents (PDFs and text files), index them using semantic embeddings, and query them using natural language.

Features
--------

* **Document Upload**: Upload PDF and text files for indexing
* **Batch Processing**: Efficiently handles large documents (3500+ pages) with batch processing
* **Semantic Search**: Query documents using natural language with relevance scoring
* **Page Tracking**: Results include page numbers for easy reference
* **gRPC Communication**: Fast communication with Qdrant using gRPC protocol
* **Docker Support**: Easy deployment with Docker and Docker Compose
* **RESTful API**: Clean REST API with automatic OpenAPI documentation

Key Technologies
---------------

* **FastAPI**: Modern, fast web framework for building APIs
* **Qdrant**: Vector database for storing embeddings
* **LangChain**: Framework for building LLM applications
* **PyMuPDF**: PDF processing with better structure preservation
* **HuggingFace**: Embedding models for semantic search

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
