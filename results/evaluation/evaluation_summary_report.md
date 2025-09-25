# COMPREHENSIVE CHUNKING EVALUATION REPORT
============================================================
Generated at: 2025-09-25 19:33:18
Total strategies evaluated: 13

## EXECUTIVE SUMMARY
------------------------------
**Best Overall Strategy:** Structural_Balanced
- Overall Score: 0.576

## STRATEGY RANKINGS
------------------------------
1. Structural_Balanced: 0.576
2. Fixed_512_64: 0.573
3. Structural_Hierarchical: 0.572
4. Fixed_1024_128: 0.554
5. Recursive_Small: 0.548
6. Recursive_Large: 0.546
7. Recursive_Balanced: 0.545
8. Structural_Large: 0.539
9. Fixed_256_0: 0.531
10. LLM_smallChunks: 0.521
11. Semantic_Med_Sim: 0.508
12. Semantic_High_Sim: 0.504
13. Semantic_Low_Sim: 0.489

## DETAILED ANALYSIS
------------------------------
### Fixed_256_0

**Basic Statistics:**
- Total Chunks: 642
- Avg Tokens/Chunk: 219.9
- Token Std Dev: 74.4

**Retrieval Performance:**
- Precision@1: 0.750
- Recall@5: 0.979
- MRR: 0.861

**Answer Quality:**
- Answer F1: 0.663
- Coverage Score: 0.750
- Semantic Coherence: 0.048

**Performance:**
- Avg Latency: 59.36 ms
- Queries/Second: 16.8

### Fixed_512_64

**Basic Statistics:**
- Total Chunks: 415
- Avg Tokens/Chunk: 382.8
- Token Std Dev: 193.7

**Retrieval Performance:**
- Precision@1: 0.917
- Recall@5: 1.000
- MRR: 0.958

**Answer Quality:**
- Answer F1: 0.667
- Coverage Score: 0.750
- Semantic Coherence: 0.048

**Performance:**
- Avg Latency: 68.94 ms
- Queries/Second: 14.5

### Fixed_1024_128

**Basic Statistics:**
- Total Chunks: 262
- Avg Tokens/Chunk: 599.0
- Token Std Dev: 449.8

**Retrieval Performance:**
- Precision@1: 0.833
- Recall@5: 1.000
- MRR: 0.917

**Answer Quality:**
- Answer F1: 0.663
- Coverage Score: 0.722
- Semantic Coherence: 0.045

**Performance:**
- Avg Latency: 74.97 ms
- Queries/Second: 13.3

### Semantic_High_Sim

**Basic Statistics:**
- Total Chunks: 1486
- Avg Tokens/Chunk: 93.3
- Token Std Dev: 80.3

**Retrieval Performance:**
- Precision@1: 0.667
- Recall@5: 1.000
- MRR: 0.819

**Answer Quality:**
- Answer F1: 0.595
- Coverage Score: 0.646
- Semantic Coherence: 0.098

**Performance:**
- Avg Latency: 75.37 ms
- Queries/Second: 13.3

### Semantic_Low_Sim

**Basic Statistics:**
- Total Chunks: 1065
- Avg Tokens/Chunk: 130.2
- Token Std Dev: 127.5

**Retrieval Performance:**
- Precision@1: 0.667
- Recall@5: 0.972
- MRR: 0.819

**Answer Quality:**
- Answer F1: 0.574
- Coverage Score: 0.639
- Semantic Coherence: 0.071

**Performance:**
- Avg Latency: 75.57 ms
- Queries/Second: 13.2

### Semantic_Med_Sim

**Basic Statistics:**
- Total Chunks: 1320
- Avg Tokens/Chunk: 105.1
- Token Std Dev: 91.5

**Retrieval Performance:**
- Precision@1: 0.750
- Recall@5: 0.972
- MRR: 0.875

**Answer Quality:**
- Answer F1: 0.570
- Coverage Score: 0.674
- Semantic Coherence: 0.087

**Performance:**
- Avg Latency: 67.79 ms
- Queries/Second: 14.8

### Structural_Balanced

**Basic Statistics:**
- Total Chunks: 368
- Avg Tokens/Chunk: 235.1
- Token Std Dev: 387.6

**Retrieval Performance:**
- Precision@1: 0.917
- Recall@5: 1.000
- MRR: 0.944

**Answer Quality:**
- Answer F1: 0.684
- Coverage Score: 0.750
- Semantic Coherence: 0.062

**Performance:**
- Avg Latency: 59.83 ms
- Queries/Second: 16.7

### Structural_Hierarchical

**Basic Statistics:**
- Total Chunks: 380
- Avg Tokens/Chunk: 227.7
- Token Std Dev: 341.1

**Retrieval Performance:**
- Precision@1: 0.917
- Recall@5: 1.000
- MRR: 0.944

**Answer Quality:**
- Answer F1: 0.669
- Coverage Score: 0.750
- Semantic Coherence: 0.061

**Performance:**
- Avg Latency: 58.56 ms
- Queries/Second: 17.1

### Structural_Large

**Basic Statistics:**
- Total Chunks: 489
- Avg Tokens/Chunk: 175.8
- Token Std Dev: 740.2

**Retrieval Performance:**
- Precision@1: 0.917
- Recall@5: 0.979
- MRR: 0.958

**Answer Quality:**
- Answer F1: 0.591
- Coverage Score: 0.722
- Semantic Coherence: 0.033

**Performance:**
- Avg Latency: 54.23 ms
- Queries/Second: 18.4

### Recursive_Balanced

**Basic Statistics:**
- Total Chunks: 619
- Avg Tokens/Chunk: 158.3
- Token Std Dev: 200.6

**Retrieval Performance:**
- Precision@1: 0.833
- Recall@5: 1.000
- MRR: 0.917

**Answer Quality:**
- Answer F1: 0.656
- Coverage Score: 0.750
- Semantic Coherence: 0.039

**Performance:**
- Avg Latency: 49.60 ms
- Queries/Second: 20.2

### Recursive_Large

**Basic Statistics:**
- Total Chunks: 600
- Avg Tokens/Chunk: 163.3
- Token Std Dev: 227.7

**Retrieval Performance:**
- Precision@1: 0.833
- Recall@5: 1.000
- MRR: 0.917

**Answer Quality:**
- Answer F1: 0.656
- Coverage Score: 0.750
- Semantic Coherence: 0.039

**Performance:**
- Avg Latency: 52.10 ms
- Queries/Second: 19.2

### Recursive_Small

**Basic Statistics:**
- Total Chunks: 654
- Avg Tokens/Chunk: 150.0
- Token Std Dev: 171.1

**Retrieval Performance:**
- Precision@1: 0.833
- Recall@5: 1.000
- MRR: 0.917

**Answer Quality:**
- Answer F1: 0.663
- Coverage Score: 0.750
- Semantic Coherence: 0.039

**Performance:**
- Avg Latency: 52.87 ms
- Queries/Second: 18.9

### LLM_smallChunks

**Basic Statistics:**
- Total Chunks: 584
- Avg Tokens/Chunk: 107.1
- Token Std Dev: 898.6

**Retrieval Performance:**
- Precision@1: 0.833
- Recall@5: 0.972
- MRR: 0.917

**Answer Quality:**
- Answer F1: 0.604
- Coverage Score: 0.701
- Semantic Coherence: 0.074

**Performance:**
- Avg Latency: 37.91 ms
- Queries/Second: 26.4

## RECOMMENDATIONS
------------------------------
- For general use: Consider 'Structural_Balanced' as it shows the best overall performance
- For high precision retrieval: 'Fixed_512_64' shows the best Precision@1
- For comprehensive answers: 'Fixed_256_0' provides the best topic coverage
- For high throughput: 'LLM_smallChunks' offers the best query processing speed
- Consider your specific use case requirements when choosing a strategy
- Monitor performance metrics regularly and adjust parameters as needed
- Test with domain-specific queries for more accurate evaluation
