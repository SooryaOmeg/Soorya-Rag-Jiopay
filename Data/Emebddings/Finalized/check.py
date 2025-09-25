import numpy as np
import json

embeddings = np.load('Structural_Hierarchical_voyage_embeddings_embeddings.npy')

met = np.load('Structural_Hierarchical_voyage_embeddings_metadata.npy', allow_pickle=True)

texts = np.load('Structural_Hierarchical_voyage_embeddings_texts.npy', allow_pickle=True)

print(embeddings.shape)

print(embeddings[0])

print(met.shape)

print(met[0])

print(texts.shape)

print(texts[0])


# # Load original metadata JSON
# with open("Structural_Hierarchical.json", encoding='utf-8') as f:
#     chunks = json.load(f)

# print(len(embeddings), len(texts), len(chunks))  # sanity check

# metadatas = []
# for i, chunk in enumerate(chunks):
#     metadatas.append({
#         "chunk_id": chunk.get("chunk_id", f"chunk_{i}"),
#         "source_url": chunk.get("source_url", "unknown"),
#         "source_title": chunk.get("source_title", "unknown"),
#         "chunk_index": chunk.get("chunk_index", i),
#         "token_count": chunk.get("token_count", None),
#         "char_count": chunk.get("char_count", None),
#         "strategy": chunk.get("strategy", None),
#         "structural_info": chunk.get("structural_info", None),
#     })

# # Save clean version
# np.save("Structural_Hierarchical_voyage_embeddings_metadata.npy", np.array(metadatas, dtype=object))

# fixed_metadata = np.load("Structural_Hierarchical_voyage_embeddings_metadata.npy", allow_pickle=True)

# print(embeddings.shape)        # (380, 1024)
# print(texts.shape)             # (380,)
# print(len(fixed_metadata))     # 380

# print(fixed_metadata[0])       # should now show full fields, not "unknown"
# print(texts[0][:200])          # preview first chunk text



