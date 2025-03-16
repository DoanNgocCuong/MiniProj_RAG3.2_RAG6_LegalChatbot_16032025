#!/usr/bin/env python3
"""
Vector Database Query Script for Legal RAG System

This script allows querying the Qdrant vector database created by create_vector_database.py.
"""

import os
import argparse
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores import Qdrant

# Load environment variables
load_dotenv()

# Get configuration from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "legal_rag")

def query_vector_database(query_text, collection_name=None, k=3):
    """
    Query the vector database with the given text.
    
    Args:
        query_text (str): The query text
        collection_name (str, optional): Name of the Qdrant collection
        k (int): Number of results to return
    
    Returns:
        list: List of documents matching the query
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME
    
    print(f"Initializing embeddings with model: {EMBEDDINGS_MODEL_NAME}")
    # Generate embeddings using HuggingFaceInferenceAPIEmbeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        model_name=EMBEDDINGS_MODEL_NAME,
        api_key=HUGGINGFACE_API_KEY
    )
    
    print(f"Connecting to Qdrant collection: {collection_name}")
    # Connect to the existing Qdrant collection
    qdrant = Qdrant(
        client_location=QDRANT_URL,
        collection_name=collection_name,
        embeddings=embeddings,
        api_key=QDRANT_API_KEY,
        prefer_grpc=False,
    )
    
    print(f"Querying: '{query_text}'")
    # Search for similar documents
    results = qdrant.similarity_search_with_score(query_text, k=k)
    
    return results

def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description='Query the legal vector database')
    parser.add_argument('query', type=str, help='The query text')
    parser.add_argument('--collection', type=str, help='Name of the Qdrant collection')
    parser.add_argument('--k', type=int, default=3, help='Number of results to return')
    
    args = parser.parse_args()
    
    results = query_vector_database(args.query, args.collection, args.k)
    
    print("\nResults:")
    for i, (doc, score) in enumerate(results):
        print(f"\n--- Result {i+1} (Similarity: {score:.4f}) ---")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    main() 