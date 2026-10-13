# Hybrid RAG Engine

A Python-based hybrid retrieval pipeline combining semantic search, keyword matching, rank fusion, and cross-encoder reranking, with role-based document filtering and PII masking.

## Architecture

- **Dense Retrieval:** Sentence Transformers generates embeddings for semantic similarity search.
- **Sparse Retrieval:** BM25 retrieves documents based on keyword relevance.
- **Rank Fusion:** Reciprocal Rank Fusion (RRF) combines dense and sparse rankings.
- **Reranking:** A Cross-Encoder reranks the fused candidates for improved relevance.
- **Security:** PII masking helps prevent sensitive information from being passed downstream. Role-based filtering restricts document retrieval according to user permissions.

## Retrieval Pipeline

    User Query
         |
         v
    PII Masking
         |
         +----------------------+
         |                      |
         v                      v
    Dense Vector Search     BM25 Search
         |                      |
         +----------+-----------+
                    |
                    v
                RRF Fusion
                    |
                    v
             Cross-Encoder
                Reranking
                    |
                    v
          Ranked Search Results

Role-based document filtering is applied during dense retrieval and to sparse results before fusion.

## Project Structure

    app/
    ├── core/
    │   ├── embedder.py
    │   └── reranker.py
    ├── data/
    │   └── documents.py
    ├── search/
    │   ├── vector_search.py
    │   ├── bm25_search.py
    │   └── rrf_fusion.py
    └── security/
        └── pii_masker.py

    main.py

## Run

Install the required dependencies, then execute:

    python main.py

The current implementation uses sample documents and runs a demonstration pipeline from `main.py`.
