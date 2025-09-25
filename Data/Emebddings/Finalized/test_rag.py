import os
from pinecone import Pinecone
import voyageai
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize clients
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
voyage = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY")) 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini = genai.GenerativeModel("gemini-2.0-flash-exp")

# Connect to your index
index = pc.Index("rag-structural-hierarchical")  # or "rag" if you used existing

def test_rag(query):
    print(f"Query: {query}")
    
    # 1. Embed query with Voyage
    query_embedding = voyage.embed([query], model="voyage-3.5", input_type="query").embeddings[0]
    
    # 2. Search Pinecone
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    
    # 3. Build context
    context = ""
    for i, match in enumerate(results['matches']):
        context += f"[{i+1}] Score: {match['score']:.3f}\n"
        context += f"Text: {match['metadata']['text']}\n\n"
    
    # 4. Generate answer with Gemini
    prompt = f"Answer based on context:\n\n{context}\n\nQuestion: {query}\nAnswer:"
    response = gemini.generate_content(prompt, generation_config={'temperature': 0.1})
    
    print(f"Answer: {response.text}")
    print(f"Sources: {len(results['matches'])} chunks")
    print("-" * 50)

if __name__ == "__main__":
    # Test queries
    queries = [
        "What are payment methods?",
        "Business registration requirements", 
        "Account settlement process"
    ]
    
    for q in queries:
        test_rag(q)