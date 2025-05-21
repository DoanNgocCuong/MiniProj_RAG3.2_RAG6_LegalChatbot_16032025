#!/usr/bin/env python3
"""
Vector Database Creation Script for Legal RAG System (No LangChain)

Script này tạo vector database từ dữ liệu pháp luật (Excel/text), lấy embedding bằng huggingface_hub và lưu trực tiếp vào Qdrant.
Cấu trúc metadata được giữ giống hệt version dùng LangChain để đảm bảo tính nhất quán.
"""

import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np

# Load biến môi trường
load_dotenv()
print("Đang load .env từ:", find_dotenv())

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "my_super_secret_key")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "legal_rag")

# Hàm lấy embedding
client = InferenceClient(provider="hf-inference", api_key=HUGGINGFACE_API_KEY)
def get_embedding(text):
    return client.feature_extraction(model=EMBEDDINGS_MODEL_NAME, text=text)

def upsert_to_qdrant(vectors, payloads, collection_name, ids=None):
    """
    Upsert vectors vào Qdrant với cấu trúc metadata giống LangChain
    """
    qdrant = QdrantClient(url="http://localhost:6333", api_key="my_super_secret_key")
    
    # Kiểm tra và tạo collection nếu chưa có
    try:
        qdrant.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' đã tồn tại.")
    except Exception:
        print(f"Collection '{collection_name}' chưa tồn tại. Đang tạo mới...")
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=len(vectors[0]),
                distance=models.Distance.COSINE
            )
        )
        print(f"Đã tạo collection '{collection_name}'.")

    if ids is None:
        ids = list(range(1, len(vectors)+1))
    
    # Log cấu trúc payload mẫu để kiểm tra
    if payloads:
        print("\nCấu trúc payload mẫu:")
        print(f"Metadata: {payloads[0].get('metadata', {})}")
        print(f"Page content: {payloads[0].get('page_content', '')[:100]}...")
    
    qdrant.upsert(
        collection_name=collection_name,
        points=models.Batch(
            ids=ids,
            vectors=vectors,
            payloads=payloads
        )
    )
    print(f"Đã upsert {len(vectors)} vectors vào collection '{collection_name}'")

def create_vector_database_from_excel(excel_file_path, collection_name=None):
    """
    Tạo vector database từ file Excel với cấu trúc metadata giống LangChain
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME
    
    print(f"Loading data from {excel_file_path}...")
    data = pd.read_excel(excel_file_path)
    
    # Extract và preprocess data
    questions = data["Câu hỏi"].dropna().tolist()
    answers = data["Đáp án"].dropna().tolist()
    
    if len(questions) != len(answers):
        print(f"Warning: Mismatch between number of questions ({len(questions)}) and answers ({len(answers)})")
        min_length = min(len(questions), len(answers))
        questions = questions[:min_length]
        answers = answers[:min_length]
    
    print(f"Creating {len(answers)} document objects with metadata...")
    
    # Tạo payload với cấu trúc giống LangChain Document
    payloads = [
        # {"source": excel_file_path, "question": q, "page_content": a}
        # for q, a in zip(questions, answers)
        {
            "metadata": {  # Cấu trúc metadata giống LangChain
                "source": excel_file_path,
                "question": question
            },
            "page_content": answer  # Tương đương với page_content trong LangChain Document
        }
        for question, answer in zip(questions, answers)
    ]
    
    print(f"Lấy embedding cho {len(answers)} đáp án...")
    vectors = [get_embedding(a) for a in answers]
    
    print(f"Upsert vào Qdrant collection: {collection_name}")
    upsert_to_qdrant(vectors, payloads, collection_name)
    print(f"Successfully added {len(answers)} documents to Qdrant")

def create_vector_database_from_text_files(text_dir, collection_name=None):
    """
    Tạo vector database từ text files với cấu trúc metadata giống LangChain
    """
    if collection_name is None:
        collection_name = COLLECTION_NAME + "_text"
    
    print(f"Loading text files from {text_dir}...")
    documents = []
    
    for root, _, files in os.walk(text_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split content into paragraphs
                    paragraphs = [p for p in content.split('\n\n') if p.strip()]
                    
                    # Tạo payload với cấu trúc giống LangChain Document
                    for paragraph in paragraphs:
                        if len(paragraph.strip()) > 50:
                            documents.append({
                                "metadata": {  # Cấu trúc metadata giống LangChain
                                    "source": file_path,
                                    "_id": os.path.basename(file_path)
                                },
                                "page_content": paragraph  # Tương đương với page_content trong LangChain Document
                            })
                    
                    print(f"Processed {file_path}: {len(paragraphs)} paragraphs")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    if not documents:
        print("No documents found to process!")
        return
    
    print(f"Lấy embedding cho {len(documents)} đoạn văn...")
    vectors = [get_embedding(doc["page_content"]) for doc in documents]
    
    print(f"Upsert vào Qdrant collection: {collection_name}")
    upsert_to_qdrant(vectors, documents, collection_name)
    print(f"Successfully added {len(documents)} documents to Qdrant collection: {collection_name}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create a vector database from legal data (no LangChain)')
    parser.add_argument('--excel', type=str, help='Path to Excel file with Q&A data')
    parser.add_argument('--text-dir', type=str, help='Directory containing text files to process')
    parser.add_argument('--collection', type=str, help='Name for the Qdrant collection')
    args = parser.parse_args()
    
    if args.excel:
        create_vector_database_from_excel(args.excel, args.collection)
    elif args.text_dir:
        create_vector_database_from_text_files(args.text_dir, args.collection)
    else:
        print("Please provide either --excel or --text-dir argument")
        parser.print_help()

if __name__ == "__main__":
    main() 