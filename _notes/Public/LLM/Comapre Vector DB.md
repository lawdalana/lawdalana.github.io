---
title : Comapre Vector DB
notetype : feed
date : 29-05-2024
---

# Source
- [Which Vector Database Should You Use? Choosing the Best One for Your Needs](https://medium.com/the-ai-forum/which-vector-database-should-you-use-choosing-the-best-one-for-your-needs-5108ec7ba133)
- [vector-databases-compared](https://zackproser.com/blog/vector-databases-compared)


# Comparing Table

## Deployment Options

Vector Database|Local Deployment|Cloud Deployment|On-Premises Deployment
:---:|:---:|:---:|:---:
Pinecone|❌|✅ (Managed)|❌
Milvus|✅|✅ (Self-hosted)|✅
Chroma|✅|✅ (Self-hosted)|✅
Weaviate|✅|✅ (Self-hosted)|✅
Faiss|✅|❌|✅
Elasticsearch|✅|✅ (Self-hosted)|✅
Qdrant|✅|✅ (Self-hosted)|✅

## Scalability

Vector Database|Horizontal Scaling|Vertical Scaling|Distributed Architecture
:---:|:---:|:---:|:---:
Pinecone|✅|✅|✅
Milvus|✅|✅|✅
Chroma|✅|✅|✅
Weaviate|✅|✅|✅
Faiss|❌|✅|❌
Elasticsearch|✅|✅|✅
Qdrant|✅|✅|✅


## Data Management

Vector Database|Data Import|Data Update/Deletion|Data Backup/Restore
:---:|:---:|:---:|:---:
Pinecone|✅|✅|✅
Milvus|✅|✅|✅
Chroma|✅|✅|✅
Weaviate|✅|✅|✅
Faiss|✅|✅|❌
Elasticsearch|✅|✅|✅
Qdrant|✅|✅|✅


## Vector Similarity Search

Vector Database|Distance Metrics|ANN Algorithms|Filtering|Post-Processing
:---:|:---:|:---:|:---:|:---:
Pinecone|Cosine, Euclidean, Dot Product|Proprietary (Pinecone Graph Algorithm)|✅|✅
Milvus|Euclidean, Cosine, IP, L2, Hamming, Jaccard, Tanimoto|HNSW, IVF_FLAT, IVF_SQ8, IVF_PQ, RNSG, ANNOY|✅|✅
Chroma|Cosine, Euclidean, Dot Product|HNSW|✅|✅
Weaviate|Cosine|HNSW|✅|✅
Faiss|L2, Cosine, IP, L1, Linf|IVF, HNSW, IMI, PQ|❌|❌
Elasticsearch|Cosine, Dot Product, L1, L2|HNSW|✅|✅
Qdrant|Cosine, Dot Product, L2|HNSW|✅|✅


## Integration and API

Vector Database|Language SDKs|REST API|GraphQL API|GRPC API
:---:|:---:|:---:|:---:|:---:
Pinecone|Python, Node.js, Go, Rust|✅|❌|✅
Milvus|Python, Java, Go, C++, Node.js, RESTful|✅|❌|✅
Chroma|Python|✅|❌|❌
Weaviate|Python, Java, Go, JavaScript, .NET|✅|✅|✅
Faiss|C++, Python|❌|❌|✅
Elasticsearch|Java, Python, Go, Ruby, PHP, Rust, Perl|✅|❌|❌
Qdrant|Python, Rust|✅|❌|✅


## Security

Vector Database|Authentication|Data Encryption|Access Control
:---:|:---:|:---:|:---:
Pinecone|✅|✅|✅
Milvus|✅|✅|✅
Chroma|❌|❌|❌
Weaviate|✅|✅|✅
Faiss|❌|❌|❌
Elasticsearch|✅|✅|✅
Qdrant|✅|✅|✅


## Community and Ecosystem

Vector Database|Open-Source|Community Support|Integration with Frameworks
:---:|:---:|:---:|:---:
Pinecone|❌|✅|✅
Milvus|✅|✅|✅
Chroma|✅|✅|✅
Weaviate|✅|✅|✅
Faiss|✅|✅|✅
Elasticsearch|✅|✅|✅
Qdrant|✅|✅|✅

## Pricing

Vector Database|Free Tier|Pay-as-you-go|Enterprise Plans
:---:|:---:|:---:|:---:
Pinecone|✅|✅|✅
Milvus|✅|❌|❌
Chroma|✅|❌|❌
Weaviate|✅|❌|✅
Faiss|✅|❌|❌
Elasticsearch|✅|✅|✅
Qdrant|✅|❌|❌

## Additional Features

Vector Database|Metadata Support|Batch Processing|Monitoring and Logging
:---:|:---:|:---:|:---:
Pinecone|✅|✅|✅
Milvus|✅|✅|✅
Chroma|✅|✅|❌
Weaviate|✅|✅|✅
Faiss|❌|✅|❌
Elasticsearch|✅|✅|✅
Qdrant|✅|✅|✅