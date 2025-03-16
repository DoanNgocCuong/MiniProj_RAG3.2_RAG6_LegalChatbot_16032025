#!/usr/bin/env python3
"""
Test script to diagnose Qdrant connection issues
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Load environment variables
load_dotenv()

# Get configuration from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

def print_separator():
    print("\n" + "="*50 + "\n")

def test_env_variables():
    """Test if environment variables are set correctly"""
    print("Testing environment variables:")
    
    # Check QDRANT_URL
    if not QDRANT_URL:
        print("❌ QDRANT_URL is not set")
    else:
        print(f"✓ QDRANT_URL = {QDRANT_URL}")
        # Check if URL has angle brackets
        if "<" in QDRANT_URL or ">" in QDRANT_URL:
            print("❌ QDRANT_URL contains angle brackets (<>). Please remove them.")
    
    # Check QDRANT_API_KEY
    if not QDRANT_API_KEY:
        print("❌ QDRANT_API_KEY is not set")
    else:
        # Only show first 10 characters for security
        print(f"✓ QDRANT_API_KEY = {QDRANT_API_KEY[:10]}...")

def test_direct_http_request():
    """Test direct HTTP request to Qdrant API"""
    print_separator()
    print("Testing direct HTTP request to Qdrant API:")
    
    if not QDRANT_URL:
        print("❌ Cannot test: QDRANT_URL is not set")
        return
    
    # Clean URL (remove angle brackets if present)
    clean_url = QDRANT_URL.replace("<", "").replace(">", "")
    
    # Construct URL for collections endpoint
    if clean_url.endswith("/"):
        api_url = f"{clean_url}collections"
    else:
        api_url = f"{clean_url}/collections"
    
    headers = {}
    if QDRANT_API_KEY:
        headers["api-key"] = QDRANT_API_KEY
    
    print(f"Making GET request to: {api_url}")
    print(f"Headers: {json.dumps(headers)}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}")  # Show first 500 chars
        
        if response.status_code == 200:
            print("✓ Direct HTTP request successful")
        elif response.status_code == 403:
            print("❌ Forbidden (403): API key may be invalid or expired")
        elif response.status_code == 401:
            print("❌ Unauthorized (401): Authentication required")
        else:
            print(f"❌ Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed with error: {str(e)}")

def test_qdrant_client():
    """Test connection using Qdrant client"""
    print_separator()
    print("Testing connection using Qdrant client:")
    
    if not QDRANT_URL:
        print("❌ Cannot test: QDRANT_URL is not set")
        return
    
    # Clean URL (remove angle brackets if present)
    clean_url = QDRANT_URL.replace("<", "").replace(">", "")
    
    print(f"Connecting to: {clean_url}")
    print(f"Using API key: {QDRANT_API_KEY[:10]}..." if QDRANT_API_KEY else "No API key provided")
    
    try:
        client = QdrantClient(
            url=clean_url,
            api_key=QDRANT_API_KEY,
            timeout=10
        )
        
        # Try to list collections
        print("Attempting to list collections...")
        collections = client.get_collections()
        print(f"✓ Connection successful! Collections: {collections}")
        
        # Try to create a test collection
        print("\nAttempting to create a test collection...")
        test_collection_name = "test_connection_collection"
        try:
            client.create_collection(
                collection_name=test_collection_name,
                vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE),
            )
            print(f"✓ Successfully created collection: {test_collection_name}")
            
            # Clean up - delete the test collection
            print(f"Deleting test collection: {test_collection_name}")
            client.delete_collection(collection_name=test_collection_name)
            print(f"✓ Successfully deleted collection: {test_collection_name}")
        except Exception as e:
            print(f"❌ Failed to create/delete test collection: {str(e)}")
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        
        # Check for common error patterns
        error_str = str(e)
        if "403" in error_str and "forbidden" in error_str.lower():
            print("\nPossible causes:")
            print("1. API key is invalid or expired")
            print("2. API key doesn't have sufficient permissions")
            print("3. Your IP might be restricted")
        elif "timeout" in error_str.lower():
            print("\nPossible causes:")
            print("1. Qdrant server is not reachable")
            print("2. Network connectivity issues")
            print("3. Firewall blocking the connection")

def main():
    """Main function"""
    print("Qdrant Connection Test\n")
    
    test_env_variables()
    test_direct_http_request()
    test_qdrant_client()
    
    print_separator()
    print("Test completed. Check the results above for any issues.")

if __name__ == "__main__":
    main() 