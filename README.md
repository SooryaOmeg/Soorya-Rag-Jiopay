# LLM Production Evaluation: RAG, Embeddings & Retrieval

This repository contains code, experiments, and evaluation results for a **production-ready LLM retrieval and generation system**. The project focuses on **document chunking, embedding evaluation, and RAG (Retrieval-Augmented Generation) pipelines** with multiple embedding models.

---

## 🚀 Project Overview

The project aims to:

1. Evaluate **different document chunking strategies**:
   - Structural Balanced
   - Structural Hierarchical
2. Compare multiple **embedding models** for similarity search:
   - Qwen3 0.6B
   - Google Gemma-300M
   - Voyage-3.5
3. Perform **RAG-based retrieval and generation** with:
   - Top-k retrieval
   - Optional rerankers
   - Guardrails for answer quality
4. Measure and report:
   - Recall, Precision, MRR
   - Latency and index sizes
   - Answer quality (semantic similarity, faithfulness, relevance)

---

---

## ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/SooryaOmeg/Soorya-Rag-Jiopay

python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt

Webite link: https://jioflow-insight.vercel.app


```
