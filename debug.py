import json
import time
import requests
import numpy as np
from sentence_transformers import SentenceTransformer, util

class DebugRAGEvaluator:
    def __init__(self, api_url):
        self.api_url = api_url
        self.embedder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    
    def debug_single_query(self, query):
        """Debug a single query to see what's happening."""
        print(f"🔍 Debugging query: {query}")
        print("-" * 50)
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={"message": query},
                timeout=30
            )
            latency = (time.time() - start_time) * 1000
            
            print(f"✅ Status Code: {response.status_code}")
            print(f"⏱️  Latency: {latency:.0f}ms")
            
            if response.status_code == 200:
                resp_json = response.json()
                print(f"📝 Response Keys: {list(resp_json.keys())}")
                
                generated = resp_json.get("response", "")
                citations = resp_json.get("citations", [])
                
                print(f"📄 Generated Answer Length: {len(generated)} chars")
                print(f"📚 Citations Count: {len(citations)}")
                
                if generated:
                    print(f"📖 First 200 chars: {generated[:200]}...")
                else:
                    print("❌ EMPTY RESPONSE - This is the problem!")
                    
                return resp_json, latency
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"📄 Response: {response.text[:300]}")
                return None, latency
                
        except requests.exceptions.Timeout:
            print("⏰ REQUEST TIMEOUT - API taking too long")
            return None, 0
        except Exception as e:
            print(f"💥 ERROR: {e}")
            return None, 0
    
    def test_rate_limits(self, test_queries):
        """Test multiple queries quickly to detect rate limiting."""
        print("🚀 Testing for rate limits...")
        print("=" * 60)
        
        results = []
        for i, query in enumerate(test_queries):
            print(f"\n[{i+1}/{len(test_queries)}] Testing: {query[:50]}...")
            
            resp, latency = self.debug_single_query(query)
            
            if resp:
                generated = resp.get("response", "")
                status = "✅ SUCCESS" if generated else "❌ EMPTY RESPONSE"
            else:
                status = "💥 FAILED"
                generated = ""
            
            results.append({
                "query": query,
                "status": status,
                "response_length": len(generated),
                "latency": latency
            })
            
            print(f"Result: {status}")
            
            # Add small delay to be nice to the API
            time.sleep(1)
        
        return results
    
    def analyze_results(self, results):
        """Analyze the test results."""
        print("\n" + "=" * 60)
        print("📊 ANALYSIS")
        print("=" * 60)
        
        total = len(results)
        successful = len([r for r in results if r["response_length"] > 0])
        empty_responses = len([r for r in results if r["response_length"] == 0])
        failed = total - successful - empty_responses
        
        print(f"Total Queries: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Empty Responses: {empty_responses} ({empty_responses/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        
        if empty_responses > successful:
            print("\n🚨 DIAGNOSIS: RATE LIMITING DETECTED!")
            print("Your RAG system is likely hitting VoyageAI/Gemini rate limits")
            print("Solutions:")
            print("  1. Add delays between requests (20+ seconds)")
            print("  2. Reduce batch size")
            print("  3. Upgrade API limits")
            print("  4. Use local embedding model")
        
        avg_latency = np.mean([r["latency"] for r in results if r["latency"] > 0])
        print(f"\nAverage Latency: {avg_latency:.0f}ms")
        
        return {
            "success_rate": successful/total,
            "empty_response_rate": empty_responses/total,
            "avg_latency": avg_latency
        }

# Quick test script
if __name__ == "__main__":
    # Test queries - mix of simple and complex
    test_queries = [
        "What is JioPay?",
        "How can I disable SMS notifications?", 
        "Where is your registered address?",
        "What are the payment gateway products?",
        "How do I download JioPay?"
    ]
    
    evaluator = DebugRAGEvaluator("https://jioflow-insight.onrender.com")
    
    print("🔧 DEBUGGING RAG SYSTEM FOR RATE LIMITS")
    print("=" * 60)
    
    # Test the queries
    results = evaluator.test_rate_limits(test_queries)
    
    # Analyze what happened
    analysis = evaluator.analyze_results(results)
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if analysis["empty_response_rate"] > 0.5:
        print("1. 🐌 Add time.sleep(20) between each evaluation query")
        print("2. 🔄 Run evaluation in smaller batches (5 queries at a time)")
        print("3. 📊 Consider evaluating only on a subset (10 queries) first")
        print("4. 🏠 Switch to local embeddings (sentence-transformers)")
    else:
        print("✅ Rate limiting doesn't seem to be the main issue")
        print("🔍 Check your API response format and error handling")