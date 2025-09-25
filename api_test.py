import requests
import json

# Test your API response format
def debug_api_response():
    api_url = "https://jioflow-insight.onrender.com"
    test_query = "How can I disable SMS notification from dashboard?"
    
    try:
        response = requests.post(
            f"{api_url}/api/chat",
            json={"message": test_query},
            timeout=30
        )
        
        result = response.json()
        
        print("=== FULL API RESPONSE ===")
        print(json.dumps(result, indent=2))
        
        print("\n=== RESPONSE STRUCTURE ===")
        print(f"Response keys: {list(result.keys())}")
        
        if 'citations' in result:
            print(f"Citations count: {len(result['citations'])}")
            if result['citations']:
                print("First citation keys:", list(result['citations'][0].keys()))
        
        if 'response' in result:
            print(f"Response length: {len(result['response'])}")
            print(f"Response preview: {result['response'][:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_api_response()