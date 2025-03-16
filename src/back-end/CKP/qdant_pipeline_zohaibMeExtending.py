
"""
title: Qdrant RAG Pipeline
author: your_name
date: 2024-01-10
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from Qdrant vector database
requirements: qdrant-client, langchain, langchain-community, python-dotenv
"""

from typing import List, Union, Generator, Iterator, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from qdrant_client import QdrantClient
import requests
import json
from openai import OpenAI
import asyncio
from qdrant_client import QdrantClient, models

load_dotenv()

class Pipeline:
    class Valves(BaseModel):
        """Configuration for Qdrant Pipeline"""
        QDRANT_API_URL: str = os.getenv("QDRANT_API_URL", "<key trực tiếp>")
        QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "<key trực tiếp>")
        QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "<key trực tiếp>")
        HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "<key trực tiếp>")
        EMBEDDINGS_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    def __init__(self):
        self.name = "Qdrant RAG Pipeline"
        self.embeddings = None
        self.qdrant_client = None
        self.valves = self.Valves()

    async def on_startup(self):
        """Initialize connections on startup"""
        try:
            print(f"Starting {self.name}...")
            
            # Initialize embeddings
            self.embeddings = HuggingFaceInferenceAPIEmbeddings(
                api_key=self.valves.HUGGINGFACE_API_KEY,
                model_name=self.valves.EMBEDDINGS_MODEL_NAME
            )
            print("Embeddings model initialized")

            # Initialize Qdrant
            self.qdrant_client = QdrantClient(
                url=self.valves.QDRANT_API_URL,
                api_key=self.valves.QDRANT_API_KEY,
                timeout=10
            )
            print("Qdrant client initialized")

            # Initialize OpenAI
            print("Initializing OpenAI client with key:", self.valves.OPENAI_API_KEY[:10] + "...")
            self.openai_client = OpenAI(api_key=self.valves.OPENAI_API_KEY)
            print("OpenAI client initialized")

            # Verify collection
            collection_info = self.qdrant_client.get_collection(
                collection_name=self.valves.QDRANT_COLLECTION
            )
            print(f"Connected to collection: {self.valves.QDRANT_COLLECTION}")
            print(f"Vector size: {collection_info.config.params.vectors.size}")

            # Kiểm tra sample point
            points = self.qdrant_client.scroll(
                collection_name=self.valves.QDRANT_COLLECTION,
                limit=1
            )
            if points and len(points[0]) > 0:  # points[0] là tuple (records, next_page_offset)
                first_point = points[0][0]  # Lấy record đầu tiên
                print("Sample point payload:", first_point.payload)
                print("Sample point vector:", len(first_point.vector))

        except Exception as e:
            print(f"Startup error: {str(e)}")
            raise

    async def on_shutdown(self):
        """Cleanup on shutdown"""
        if self.qdrant_client:
            self.qdrant_client.close()

    def search_vectors(self, query_vector: List[float], top_k: int = 5) -> dict:
        """Search Qdrant collection"""
        try:
            # Encode payload as UTF-8
            payload = {
                "vector": query_vector,
                "limit": top_k,
                "with_payload": True,
                "score_threshold": 0.5
            }
            
            url = f"{self.valves.QDRANT_API_URL}/collections/{self.valves.QDRANT_COLLECTION}/points/search"
            headers = {
                "Authorization": f"Bearer {self.valves.QDRANT_API_KEY}",
                "Content-Type": "application/json; charset=utf-8",
            }
            
            # Encode JSON với ensure_ascii=False
            json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            
            response = requests.post(
                url, 
                data=json_data,
                headers=headers
            )
            response.raise_for_status()
            
            return {"result": response.json().get("result", [])}
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            return {"error": str(e)}

    async def get_completion(self, messages: List[dict]) -> str:
        """Get completion from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {str(e)}")
            return f"Error getting completion: {str(e)}"

    def pipe(self, user_message: str, model_id: str, messages: List[dict], body: dict) -> Union[str, Generator, Iterator]:
        """Process user message and return relevant context"""
        try:
            print(f"\n=== Starting pipeline execution ===")
            print(f"Input message: {user_message}")
            
            # Debug: In ra cấu trúc collection
            print("\n--- Debug: Checking collection structure ---")
            points = self.qdrant_client.scroll(
                collection_name=self.valves.QDRANT_COLLECTION,
                limit=2,
                with_payload=True,
                with_vectors=False
            )
            print("Sample points from collection:")
            for point in points[0]:
                print(f"Point ID: {point.id}")
                print(f"Payload: {point.payload}")
                print("---")

            # Bước 1: Thử tìm kiếm câu hỏi trùng khớp bằng scroll method
            try:
                print("\n--- Step 1: Text search with scroll method ---")
                scroll_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="metadata.question",
                            match=models.MatchValue(value=user_message)
                        )
                    ]
                )
                print(f"Filter condition: {scroll_filter}")
                
                scroll_results = self.qdrant_client.scroll(
                    collection_name=self.valves.QDRANT_COLLECTION,
                    scroll_filter=scroll_filter,
                    limit=1,
                    with_payload=True
                )
                print(f"Scroll results: {scroll_results}")
                
                if scroll_results and len(scroll_results[0]) > 0:
                    match = scroll_results[0][0]
                    print(f"Found exact match: {match.payload.get('metadata.question', '')}")
                    return match.payload.get('page_content', '')

            except Exception as e:
                print(f"\nError in scroll search:")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")

            # Bước 2: Nếu không tìm được kết quả, thử semantic search
            print("\n--- Step 2: Semantic search ---")
            print("Creating embedding for semantic search...")
            query_vector = self.embeddings.embed_query(user_message)
            print(f"Embedding created with size: {len(query_vector)}")
            
            results = self.search_vectors(query_vector)
            print("Semantic search completed")
            
            if "error" in results:
                return f"Search error: {results['error']}"

            matches = results.get("result", [])
            if matches:
                for match in matches:
                    score = float(match.get("score", 0))
                    payload = match.get("payload", {})
                    metadata = payload.get('metadata', {})
                    
                    # Trả về kết quả nếu độ tương đồng cao
                    if score >= 0.8 and "page_content" in payload:
                        return (
                            f"Câu trả lời từ tài liệu: {payload['page_content']} "
                            f"(Nguồn: {metadata.get('source', 'Không rõ')}, "
                            f"Câu hỏi gốc: {metadata.get('question', 'Không rõ')})"
                        )

            # Bước 3: Xử lý với OpenAI nếu không tìm được kết quả phù hợp
            if not matches:
                return "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn"

            context = []
            for match in matches:
                score = float(match.get("score", 0))
                content = match.get("payload", {}).get("page_content", "No content")
                if score > 0.5:
                    context.append(content)

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Bạn là trợ lý AI giúp trả lời các câu hỏi về luật giao thông. "
                        "Hãy sử dụng thông tin sau để trả lời:\n\n" + 
                        "\n\n".join(context)
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            response = asyncio.run(self.get_completion(messages))
            return response

        except Exception as e:
            print(f"Pipeline error: {str(e)}")
            return f"Error: {str(e)}"

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """Pre-process incoming messages"""
        try:
            if "messages" in body:
                last_message = body["messages"][-1]["content"]
                print(f"Processing: {last_message}")
                
                query_vector = self.embeddings.embed_query(last_message)
                results = self.search_vectors(query_vector)
                
                if "error" not in results:
                    matches = results.get("result", [])
                    if matches:
                        context = []
                        for idx, match in enumerate(matches, 1):
                            score = float(match.get("score", 0))
                            content = match.get("payload", {}).get("page_content", "No content")
                            if score > 0.5:
                                context.append(f"{content}")
                        
                        # Tạo system message với context
                        system_message = {
                            "role": "system",
                            "content": (
                                "Bạn là trợ lý AI giúp trả lời các câu hỏi về luật giao thông. "
                                "Hãy sử dụng thông tin sau để trả lời:\n\n" + 
                                "\n\n".join(context)
                            )
                        }
                        
                        # Thêm system message vào đầu conversations
                        body["messages"].insert(0, system_message)
                        
            return body
        except Exception as e:
            print(f"Inlet error: {str(e)}")
            return body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """Post-process outgoing messages"""
        return body
