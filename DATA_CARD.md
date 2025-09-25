---
### **DATA CARD.md**

# DATA CARD: LLM Production Evaluation

This data card describes the datasets, embeddings, and metadata used in the **LLM retrieval and RAG evaluation pipeline**.
---

## 1. Data Sources

| Source Name                              | Type              | Count / Size    | Description                                                                          |
| ---------------------------------------- | ----------------- | --------------- | ------------------------------------------------------------------------------------ |
| Website Content (`website.txt`)          | Text              | 1 file (~50 KB) | Sample website content used for retrieval evaluation                                 |
| Embeddings (`Data/Embeddings/Finalized`) | Embedding vectors | 748 chunks      | Generated from chunked documents using three embedding models (Qwen3, Gemma, Voyage) |
| Evaluation Queries (`queries.json`)      | JSON              | 20 queries      | Queries used to evaluate retrieval + generation pipelines                            |

---

## 2. Embedding Models

| Model Name        | Embedding Dimension | Chunks                              | Notes                                      |
| ----------------- | ------------------- | ----------------------------------- | ------------------------------------------ |
| Qwen3-0.6B        | 1024                | 368 (Balanced) / 380 (Hierarchical) | HuggingFace tokenizer + model              |
| Google Gemma-300M | 768                 | 368 / 380                           | Pooler or mean of last hidden state        |
| Voyage-3.5        | 1024                | 368 / 380                           | Remote API embedding; retry logic included |

---

## 3. Chunking Strategies

- **Structural Balanced:** Balanced division of text into chunks based on structure.
- **Structural Hierarchical:** Hierarchical chunking respecting the document structure.

---

## 4. Evaluation Metadata

| Metric                | Description                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| Recall@k              | Fraction of expected relevant documents retrieved in top-k              |
| Precision@k           | Fraction of top-k retrieved documents that are relevant                 |
| MRR                   | Mean Reciprocal Rank of the first relevant document                     |
| Latency (ms)          | Time to compute embedding or generate response                          |
| Index Size (MB)       | Memory footprint of embedding index                                     |
| Success Rate (%)      | Fraction of queries with at least one relevant document retrieved       |
| Answer Quality Scores | Semantic Similarity, Faithfulness, Completeness, Relevance, Exact Match |

---

## 5. Notes & Considerations

- Queries and embeddings are internally generated and/or derived from sample website content.
- Sensitive environment variables and local files are excluded (`.env`, `venv/`, etc.).
- This dataset is primarily for **internal evaluation** and not for external distribution.
