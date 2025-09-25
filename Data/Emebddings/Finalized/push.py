import os
import numpy as np
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm
from dotenv import load_dotenv
import time

# sooryasiva17@gmail.com <- pinecone repo

# Load environment variables
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "rag-structural-hierarchical"  # Descriptive name for your embeddings

def load_embeddings_data():
    """Load your pre-computed embeddings and associated data"""
    print("Loading embeddings data...")
    
    embeddings = np.load('Structural_Hierarchical_voyage_embeddings_embeddings.npy')
    metadata = np.load('Structural_Hierarchical_voyage_embeddings_metadata.npy', allow_pickle=True)
    texts = np.load('Structural_Hierarchical_voyage_embeddings_texts.npy', allow_pickle=True)
    
    print(f"Loaded {embeddings.shape[0]} embeddings with dimension {embeddings.shape[1]}")
    print(f"Sample metadata: {metadata[0]}")
    print(f"Sample text length: {len(texts[0])} characters")
    
    return embeddings, metadata, texts

def initialize_pinecone():
    """Initialize Pinecone client and create index if needed"""
    print("Initializing Pinecone...")
    
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check existing indexes
    existing_indexes = pc.list_indexes().names()
    print(f"Existing indexes: {existing_indexes}")
    
    # Create index if it doesn't exist
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating new index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1024,  # Voyage embeddings are 1024-dimensional
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        time.sleep(10)
        print("Index created successfully")
    else:
        print(f"Using existing index: {PINECONE_INDEX_NAME}")
    
    # Connect to the index
    index = pc.Index(PINECONE_INDEX_NAME)
    return index

def prepare_vectors_for_upload(embeddings, metadata, texts):
    """Prepare vectors in the format Pinecone expects"""
    print("Preparing vectors for upload...")
    
    vectors = []
    for i in tqdm(range(len(embeddings)), desc="Preparing vectors"):
        # Create a unique ID for each vector
        vector_id = f"chunk_{i}_{metadata[i]['chunk_id'].replace('/', '_').replace('#', '_')}"
        
        # Prepare metadata (Pinecone has some restrictions on metadata)
        vector_metadata = {
            'chunk_id': metadata[i]['chunk_id'],
            'source_url': metadata[i]['source_url'],
            'source_title': metadata[i]['source_title'],
            'chunk_index': int(metadata[i]['chunk_index']),
            'token_count': int(metadata[i]['token_count']),
            'char_count': int(metadata[i]['char_count']),
            'strategy': metadata[i]['strategy'],
            'text': texts[i][:1000],  # Truncate text for metadata (Pinecone has size limits)
            'full_text_length': len(texts[i])
        }
        
        # Add structural info if available
        if 'structural_info' in metadata[i]:
            struct_info = metadata[i]['structural_info']
            vector_metadata.update({
                'structure_type': struct_info.get('structure_type', ''),
                'level': int(struct_info.get('level', 0)),
                'heading': struct_info.get('heading', '')[:200],  # Truncate long headings
                'topic': struct_info.get('topic', '')
            })
        
        vectors.append({
            'id': vector_id,
            'values': embeddings[i].tolist(),  # Convert numpy array to list
            'metadata': vector_metadata
        })
    
    print(f"Prepared {len(vectors)} vectors for upload")
    return vectors

def upload_vectors_to_pinecone(index, vectors, batch_size=100):
    """Upload vectors to Pinecone in batches"""
    print(f"Uploading {len(vectors)} vectors to Pinecone...")
    
    # Upload in batches to avoid memory issues and API limits
    for i in tqdm(range(0, len(vectors), batch_size), desc="Uploading batches"):
        batch = vectors[i:i + batch_size]
        
        try:
            # Upsert the batch
            index.upsert(vectors=batch)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error uploading batch {i//batch_size + 1}: {e}")
            # Continue with next batch
            continue
    
    print("Upload completed!")

def verify_upload(index, expected_count):
    """Verify that vectors were uploaded correctly"""
    print("Verifying upload...")
    
    # Wait a moment for indexing to complete
    time.sleep(5)
    
    # Check index stats
    stats = index.describe_index_stats()
    actual_count = stats['total_vector_count']
    
    print(f"Expected vectors: {expected_count}")
    print(f"Actual vectors in index: {actual_count}")
    
    if actual_count == expected_count:
        print("✅ Upload verification successful!")
    else:
        print(f"⚠️ Upload verification failed. Missing {expected_count - actual_count} vectors")
    
    # Show index stats
    print(f"Index stats: {stats}")

def test_similarity_search(index, sample_text="payment methods"):
    """Test similarity search with a sample query"""
    print(f"\nTesting similarity search with query: '{sample_text}'")
    
    try:
        # For testing, we'll search by text content in metadata
        # In production, you'd embed the query using Voyage API
        results = index.query(
            vector=[0.0] * 1024,  # Dummy vector for testing
            filter={"text": {"$regex": ".*payment.*"}},  # Search in text metadata
            top_k=3,
            include_metadata=True
        )
        
        print("Sample search results:")
        for i, result in enumerate(results['matches']):
            print(f"{i+1}. ID: {result['id']}")
            print(f"   Score: {result['score']:.4f}")
            print(f"   Source: {result['metadata']['source_title']}")
            print(f"   Text preview: {result['metadata']['text'][:100]}...")
            print()
            
    except Exception as e:
        print(f"Test search failed: {e}")

def main():
    """Main function to upload embeddings to Pinecone"""
    try:
        # Step 1: Load data
        embeddings, metadata, texts = load_embeddings_data()
        
        # Step 2: Initialize Pinecone
        index = initialize_pinecone()
        
        # Step 3: Prepare vectors
        vectors = prepare_vectors_for_upload(embeddings, metadata, texts)
        
        # Step 4: Upload to Pinecone
        upload_vectors_to_pinecone(index, vectors)
        
        # Step 5: Verify upload
        verify_upload(index, len(vectors))
        
        # Step 6: Test search (optional)
        # test_similarity_search(index)
        
        print("\n🎉 Successfully uploaded Structural Hierarchical Voyage embeddings to Pinecone!")
        print(f"Index name: {PINECONE_INDEX_NAME}")
        print(f"Total vectors: {len(vectors)}")
        print(f"Vector dimension: 1024")
        
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        import traceback
        traceback.print_exc()

# For debugging - check what will be uploaded
def preview_upload_data():
    """Preview what will be uploaded without actually uploading"""
    embeddings, metadata, texts = load_embeddings_data()
    vectors = prepare_vectors_for_upload(embeddings, metadata, texts)
    
    print("\nPreview of first vector:")
    print(f"ID: {vectors[0]['id']}")
    print(f"Embedding shape: {len(vectors[0]['values'])}")
    print("Metadata:")
    for key, value in vectors[0]['metadata'].items():
        print(f"  {key}: {value}")
    
    print(f"\nTotal vectors prepared: {len(vectors)}")
    print("Metadata keys across all vectors:")
    all_keys = set()
    for v in vectors[:10]:  # Check first 10
        all_keys.update(v['metadata'].keys())
    print(sorted(all_keys))

if __name__ == "__main__":
    print("Structural Hierarchical + Voyage Embeddings → Pinecone Upload")
    print("=" * 60)
    
    # Uncomment to preview data before uploading
    preview_upload_data()
    
    # Upload the embeddings
    # main()