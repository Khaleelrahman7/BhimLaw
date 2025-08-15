#!/usr/bin/env python3
"""
Simple test script to check if BhimLaw API is working
"""

import requests
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:5001/health", timeout=10)
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("Health endpoint response:", response.json())
            return True
        else:
            print("Health endpoint failed:", response.text)
            return False
    except Exception as e:
        print(f"Health endpoint error: {e}")
        return False

def test_specialized_analyze():
    """Test the specialized analyze endpoint"""
    try:
        url = "http://localhost:5001/api/specialized/analyze"
        data = {
            "query": "I've inherited a property, but the mutation record hasn't been updated in my name. How do I proceed?",
            "case_type": "property_violations",
            "session_id": "test_session_123",
            "force_new_session": True
        }
        
        print(f"Testing URL: {url}")
        print(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("API Response:")
            print(json.dumps(response_data, indent=2))
            return True
        else:
            print("API Error Response:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"API test error: {e}")
        return False

def main():
    print("🧪 Testing BhimLaw API...")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    health_ok = test_health_endpoint()
    
    if health_ok:
        print("\n2. Testing Specialized Analyze Endpoint...")
        api_ok = test_specialized_analyze()
        
        if api_ok:
            print("\n✅ All tests passed! BhimLaw API is working correctly.")
        else:
            print("\n❌ API test failed!")
    else:
        print("\n❌ Health check failed! Server might not be running.")

if __name__ == "__main__":
    main()
