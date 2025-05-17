#!/usr/bin/env python3
"""
Test script for HuggingFace Embeddings using new InferenceClient
"""

import os
import logging
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("embedding-test")

# Load environment variables
load_dotenv()

def test_embedding_generation():
    """Test embedding generation with the new InferenceClient"""
    try:
        # Initialize the client
        client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HUGGINGFACE_API_KEY")
        )
        logger.info("InferenceClient initialized successfully")

        # Test with Vietnamese text
        test_text = "Xin chào, đây là một câu tiếng Việt để kiểm tra."
        logger.info(f"Testing with text: {test_text}")

        # Generate embedding
        embedding = client.feature_extraction(
            model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            text=test_text
        )
        
        logger.info(f"Successfully generated embedding of length: {len(embedding)}")
        logger.info(f"Embedding type: {type(embedding)}")
        logger.info(f"First 5 values: {embedding[:5]}")
        
        return True
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return False

def test_sentence_similarity():
    """Test sentence similarity using the new client"""
    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HUGGINGFACE_API_KEY")
        )
        
        # Test sentences
        source = "Tôi muốn hỏi về luật giao thông"
        sentences = [
            "Tôi cần tư vấn về luật giao thông",
            "Thời tiết hôm nay thật đẹp",
            "Luật giao thông đường bộ quy định gì?"
        ]
        
        # Get similarity scores
        result = client.sentence_similarity(
            inputs={
                "source_sentence": source,
                "sentences": sentences
            },
            model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )
        
        logger.info("Sentence similarity results:")
        for sentence, score in zip(sentences, result):
            logger.info(f"Similarity with '{sentence}': {score:.4f}")
        
        return True
    except Exception as e:
        logger.error(f"Error in sentence similarity test: {str(e)}")
        return False

def test_batch_embeddings():
    """Test batch embedding generation"""
    try:
        client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HUGGINGFACE_API_KEY")
        )
        
        # Test batch of texts
        texts = [
            "Luật giao thông đường bộ",
            "Quy định về tốc độ xe",
            "Xử phạt vi phạm giao thông"
        ]
        
        # Generate embeddings for all texts
        embeddings = client.feature_extraction(
            model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            text=texts
        )
        
        logger.info(f"Generated {len(embeddings)} embeddings")
        logger.info(f"Each embedding has length: {len(embeddings[0])}")
        
        # Calculate cosine similarity between first and other embeddings
        first_embedding = embeddings[0]
        for i, text in enumerate(texts[1:], 1):
            similarity = np.dot(first_embedding, embeddings[i]) / (
                np.linalg.norm(first_embedding) * np.linalg.norm(embeddings[i])
            )
            logger.info(f"Similarity between '{texts[0]}' and '{text}': {similarity:.4f}")
        
        return True
    except Exception as e:
        logger.error(f"Error in batch embeddings test: {str(e)}")
        return False

def main():
    """Run all tests"""
    logger.info("=== Starting Embedding Tests ===")
    
    # Check API key
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        logger.error("HUGGINGFACE_API_KEY not found in environment variables")
        return
    
    logger.info("API Key found")
    
    # Run tests
    tests = [
        ("Single Embedding Test", test_embedding_generation),
        ("Sentence Similarity Test", test_sentence_similarity),
        ("Batch Embeddings Test", test_batch_embeddings)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n=== Running {test_name} ===")
        success = test_func()
        results.append((test_name, success))
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        logger.info(f"{test_name}: {status}")

if __name__ == "__main__":
    main()
