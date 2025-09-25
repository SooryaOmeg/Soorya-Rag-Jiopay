# UNIFIED CHUNKING EVALUATION REPORT
============================================================
Generated: 2025-09-25 19:33:49
Strategies Evaluated: 13
Test Queries: 15

## EXECUTIVE SUMMARY
------------------------------
**🏆 Best Overall Strategy:** LLM_smallChunks
- Final Score: 0.742
- RAG Quality: 0.680
- Retrieval Performance: 0.925

## EVALUATION METHODOLOGY
------------------------------
This evaluation combines two complementary approaches:

### Weighting Scheme:
- **RAG Quality (40%)**: Domain-specific content quality metrics
  - Semantic coherence, context completeness, information density, topic coverage
- **Retrieval Performance (35%)**: Actual retrieval effectiveness
  - Precision@1, Precision@K, Recall@K, Mean Reciprocal Rank
- **Size Optimization (15%)**: Chunk size appropriateness
  - Optimal size distribution for embeddings (150-600 tokens)
- **Performance (10%)**: Processing efficiency
  - Query latency and throughput

## STRATEGY RANKINGS
------------------------------
1. **LLM_smallChunks**: 0.742
2. **Structural_Hierarchical**: 0.725
3. **Structural_Balanced**: 0.724
4. **Structural_Large**: 0.710
5. **Recursive_Small**: 0.709
6. **Recursive_Large**: 0.706
7. **Recursive_Balanced**: 0.706
8. **Fixed_256_0**: 0.704
9. **Fixed_512_64**: 0.695
10. **Semantic_Med_Sim**: 0.692
11. **Fixed_1024_128**: 0.686
12. **Semantic_Low_Sim**: 0.681
13. **Semantic_High_Sim**: 0.680

## DETAILED ANALYSIS
------------------------------
### LLM_smallChunks
**Core Metrics:**
- Final Score: 0.742
- RAG Quality: 0.680
- Retrieval Performance: 0.925
- Size Optimization: 0.815

**Chunk Statistics:**
- Total Chunks: 584
- Avg Tokens: 107.1
- Token Std Dev: 898.6

**Domain-Specific Metrics:**
- Semantic Coherence: 0.477
- Context Completeness: 0.702
- Information Density: 0.542
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.867
- Recall@5: 0.967
- MRR: 0.933

**Performance:**
- Avg Latency: 36.83 ms
- Queries/Second: 27.1

### Structural_Hierarchical
**Core Metrics:**
- Final Score: 0.725
- RAG Quality: 0.670
- Retrieval Performance: 0.906
- Size Optimization: 0.766

**Chunk Statistics:**
- Total Chunks: 380
- Avg Tokens: 227.7
- Token Std Dev: 341.1

**Domain-Specific Metrics:**
- Semantic Coherence: 0.348
- Context Completeness: 0.726
- Information Density: 0.606
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.867
- Recall@5: 0.967
- MRR: 0.922

**Performance:**
- Avg Latency: 68.97 ms
- Queries/Second: 14.5

### Structural_Balanced
**Core Metrics:**
- Final Score: 0.724
- RAG Quality: 0.671
- Retrieval Performance: 0.902
- Size Optimization: 0.758

**Chunk Statistics:**
- Total Chunks: 368
- Avg Tokens: 235.1
- Token Std Dev: 387.6

**Domain-Specific Metrics:**
- Semantic Coherence: 0.356
- Context Completeness: 0.720
- Information Density: 0.608
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.867
- Recall@5: 0.967
- MRR: 0.922

**Performance:**
- Avg Latency: 63.68 ms
- Queries/Second: 15.7

### Structural_Large
**Core Metrics:**
- Final Score: 0.710
- RAG Quality: 0.658
- Retrieval Performance: 0.889
- Size Optimization: 0.723

**Chunk Statistics:**
- Total Chunks: 489
- Avg Tokens: 175.8
- Token Std Dev: 740.2

**Domain-Specific Metrics:**
- Semantic Coherence: 0.413
- Context Completeness: 0.624
- Information Density: 0.595
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.867
- Recall@5: 0.944
- MRR: 0.933

**Performance:**
- Avg Latency: 63.46 ms
- Queries/Second: 15.8

### Recursive_Small
**Core Metrics:**
- Final Score: 0.709
- RAG Quality: 0.668
- Retrieval Performance: 0.856
- Size Optimization: 0.814

**Chunk Statistics:**
- Total Chunks: 654
- Avg Tokens: 150.0
- Token Std Dev: 171.1

**Domain-Specific Metrics:**
- Semantic Coherence: 0.348
- Context Completeness: 0.710
- Information Density: 0.614
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.800
- Recall@5: 0.939
- MRR: 0.900

**Performance:**
- Avg Latency: 55.67 ms
- Queries/Second: 18.0

### Recursive_Large
**Core Metrics:**
- Final Score: 0.706
- RAG Quality: 0.668
- Retrieval Performance: 0.856
- Size Optimization: 0.784

**Chunk Statistics:**
- Total Chunks: 600
- Avg Tokens: 163.3
- Token Std Dev: 227.7

**Domain-Specific Metrics:**
- Semantic Coherence: 0.350
- Context Completeness: 0.694
- Information Density: 0.628
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.800
- Recall@5: 0.939
- MRR: 0.900

**Performance:**
- Avg Latency: 63.57 ms
- Queries/Second: 15.7

### Recursive_Balanced
**Core Metrics:**
- Final Score: 0.706
- RAG Quality: 0.666
- Retrieval Performance: 0.856
- Size Optimization: 0.787

**Chunk Statistics:**
- Total Chunks: 619
- Avg Tokens: 158.3
- Token Std Dev: 200.6

**Domain-Specific Metrics:**
- Semantic Coherence: 0.348
- Context Completeness: 0.700
- Information Density: 0.619
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.800
- Recall@5: 0.939
- MRR: 0.900

**Performance:**
- Avg Latency: 62.47 ms
- Queries/Second: 16.0

### Fixed_256_0
**Core Metrics:**
- Final Score: 0.704
- RAG Quality: 0.641
- Retrieval Performance: 0.843
- Size Optimization: 0.970

**Chunk Statistics:**
- Total Chunks: 642
- Avg Tokens: 219.9
- Token Std Dev: 74.4

**Domain-Specific Metrics:**
- Semantic Coherence: 0.252
- Context Completeness: 0.859
- Information Density: 0.454
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.733
- Recall@5: 0.944
- MRR: 0.856

**Performance:**
- Avg Latency: 54.49 ms
- Queries/Second: 18.4

### Fixed_512_64
**Core Metrics:**
- Final Score: 0.695
- RAG Quality: 0.634
- Retrieval Performance: 0.860
- Size Optimization: 0.826

**Chunk Statistics:**
- Total Chunks: 415
- Avg Tokens: 382.8
- Token Std Dev: 193.7

**Domain-Specific Metrics:**
- Semantic Coherence: 0.242
- Context Completeness: 0.847
- Information Density: 0.446
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.800
- Recall@5: 0.928
- MRR: 0.872

**Performance:**
- Avg Latency: 75.09 ms
- Queries/Second: 13.3

### Semantic_Med_Sim
**Core Metrics:**
- Final Score: 0.692
- RAG Quality: 0.647
- Retrieval Performance: 0.828
- Size Optimization: 0.875

**Chunk Statistics:**
- Total Chunks: 1320
- Avg Tokens: 105.1
- Token Std Dev: 91.5

**Domain-Specific Metrics:**
- Semantic Coherence: 0.448
- Context Completeness: 0.722
- Information Density: 0.418
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.733
- Recall@5: 0.922
- MRR: 0.856

**Performance:**
- Avg Latency: 66.98 ms
- Queries/Second: 14.9

### Fixed_1024_128
**Core Metrics:**
- Final Score: 0.686
- RAG Quality: 0.636
- Retrieval Performance: 0.854
- Size Optimization: 0.722

**Chunk Statistics:**
- Total Chunks: 262
- Avg Tokens: 599.0
- Token Std Dev: 449.8

**Domain-Specific Metrics:**
- Semantic Coherence: 0.277
- Context Completeness: 0.827
- Information Density: 0.441
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.800
- Recall@5: 0.906
- MRR: 0.883

**Performance:**
- Avg Latency: 63.13 ms
- Queries/Second: 15.8

### Semantic_Low_Sim
**Core Metrics:**
- Final Score: 0.681
- RAG Quality: 0.644
- Retrieval Performance: 0.801
- Size Optimization: 0.880

**Chunk Statistics:**
- Total Chunks: 1065
- Avg Tokens: 130.2
- Token Std Dev: 127.5

**Domain-Specific Metrics:**
- Semantic Coherence: 0.429
- Context Completeness: 0.735
- Information Density: 0.412
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.667
- Recall@5: 0.939
- MRR: 0.811

**Performance:**
- Avg Latency: 68.95 ms
- Queries/Second: 14.5

### Semantic_High_Sim
**Core Metrics:**
- Final Score: 0.680
- RAG Quality: 0.647
- Retrieval Performance: 0.799
- Size Optimization: 0.866

**Chunk Statistics:**
- Total Chunks: 1486
- Avg Tokens: 93.3
- Token Std Dev: 80.3

**Domain-Specific Metrics:**
- Semantic Coherence: 0.459
- Context Completeness: 0.707
- Information Density: 0.420
- Topic Coverage: 1.000

**Retrieval Metrics:**
- Precision@1: 0.667
- Recall@5: 0.944
- MRR: 0.811

**Performance:**
- Avg Latency: 71.83 ms
- Queries/Second: 13.9

## RECOMMENDATIONS
------------------------------
### Primary Recommendation: LLM_smallChunks
Use **LLM_smallChunks** as your primary chunking strategy for the JioPay RAG chatbot.

**Key Strengths:**
- High precision retrieval
- Comprehensive topic coverage

### Implementation Guidelines:
- Monitor retrieval performance in production
- Consider A/B testing with top 2-3 strategies
- Regularly evaluate with domain-specific queries
- Adjust chunk sizes based on embedding model performance
