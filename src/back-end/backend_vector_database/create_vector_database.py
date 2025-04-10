#!/usr/bin/env python3
"""
Vector Database Creation Script for Legal RAG System

This script creates a vector database from legal data stored in an Excel file.
It extracts answers and questions, creates embeddings, and stores them in Qdrant.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Get configuration from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "legal_rag")

def create_vector_database(excel_file_path, collection_name=None):
    """
    Create a vector database from an Excel file containing legal Q&A data.
    
    Args:
        excel_file_path (str): Path to the Excel file
        collection_name (str, optional): Name for the Qdrant collection
    
    Returns:
        Qdrant: The created vector database
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME
    
    print(f"Loading data from {excel_file_path}...")
    # Load Excel data
    data = pd.read_excel(excel_file_path)
    
    # Extract and preprocess the "Câu hỏi" and "Đáp án" columns
    questions = data["Câu hỏi"].dropna().tolist()
    answers = data["Đáp án"].dropna().tolist()
    
    # Ensure questions and answers have the same length
    if len(questions) != len(answers):
        print(f"Warning: Mismatch between number of questions ({len(questions)}) and answers ({len(answers)})")
        # Find the minimum length to avoid index errors
        min_length = min(len(questions), len(answers))
        questions = questions[:min_length]
        answers = answers[:min_length]
    
    print(f"Creating {len(answers)} document objects with metadata...")
    # Add metadata to each chunk and create Document objects
    documents = [
        Document(
            page_content=answer,
            # metadata: tùy chọn? source: link excel
            metadata={"source": excel_file_path, "question": question}
        )
        for question, answer in zip(questions, answers)
    ]
    
    print(f"Initializing embeddings with model: {EMBEDDINGS_MODEL_NAME}")
    # Generate embeddings using HuggingFaceInferenceAPIEmbeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        model_name=EMBEDDINGS_MODEL_NAME,
        api_key=HUGGINGFACE_API_KEY
    )
    
    print(f"Creating vector database in Qdrant collection: {collection_name}")
    # Create a vector database in Qdrant
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=collection_name,
        api_key=QDRANT_API_KEY,
        prefer_grpc=False,
    )
    
    print(f"Successfully added {len(documents)} documents to Qdrant")
    return qdrant

def create_vector_database_from_text_files(text_dir, collection_name=None):
    """
    Create a vector database from text files in a directory.
    
    Args:
        text_dir (str): Directory containing text files
        collection_name (str, optional): Name for the Qdrant collection
    
    Returns:
        Qdrant: The created vector database
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME + "_text"
    
    print(f"Loading text files from {text_dir}...")
    documents = []
    
    # Walk through the directory and process each text file
    for root, _, files in os.walk(text_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split content into chunks (simple approach - by paragraphs)
                    paragraphs = [p for p in content.split('\n\n') if p.strip()]
                    
                    # Create Document objects for each paragraph
                    for paragraph in paragraphs:
                        if len(paragraph.strip()) > 50:  # Only include substantial paragraphs
                            documents.append(
                                Document(
                                    page_content=paragraph,
                                    metadata={"source": file_path, "_id": os.path.basename(file_path)}
                                )
                            )
                    
                    print(f"Processed {file_path}: {len(paragraphs)} paragraphs")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    if not documents:
        print("No documents found to process!")
        return None
    
    print(f"Creating vector database with {len(documents)} documents...")
    
    # Generate embeddings using HuggingFaceInferenceAPIEmbeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        model_name=EMBEDDINGS_MODEL_NAME,
        api_key=HUGGINGFACE_API_KEY
    )
    
    # Create a vector database in Qdrant
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=collection_name,
        api_key=QDRANT_API_KEY,
        prefer_grpc=False,
    )
    
    print(f"Successfully added {len(documents)} documents to Qdrant collection: {collection_name}")
    return qdrant

def main():
    """Main function to run the script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Create a vector database from legal data')
    parser.add_argument('--excel', type=str, help='Path to Excel file with Q&A data')
    parser.add_argument('--text-dir', type=str, help='Directory containing text files to process')
    parser.add_argument('--collection', type=str, help='Name for the Qdrant collection')
    
    args = parser.parse_args()
    
    if args.excel:
        create_vector_database(args.excel, args.collection)
    elif args.text_dir:
        create_vector_database_from_text_files(args.text_dir, args.collection)
    else:
        print("Please provide either --excel or --text-dir argument")
        parser.print_help()

if __name__ == "__main__":
    main() 