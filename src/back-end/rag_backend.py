#!/usr/bin/env python3
"""
RAG Backend API for Legal Chatbot
Based on Qdrant Pipeline
"""

import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient, models
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

logger = logging.getLogger("rag-backend")

# Load environment variables
load_dotenv()

# Configuration
class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("COLLECTION_NAME", "legal_rag")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{os.urandom(12).hex()}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(asyncio.get_event_loop().time()))
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, Any] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

# Create FastAPI app
app = FastAPI(
    title="Legal RAG API",
    description="API for Legal RAG Chatbot",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
embeddings_client = None
qdrant_client = None
openai_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    global embeddings_client, qdrant_client, openai_client
    
    try:
        logger.info("Initializing RAG Backend...")
        
        # Initialize embeddings client
        embeddings_client = InferenceClient(
            provider="hf-inference",
            api_key=Config.HUGGINGFACE_API_KEY
        )
        logger.info("Embeddings client initialized")

        # Initialize Qdrant
        qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=10
        )
        logger.info("Qdrant client initialized")

        # Verify collection
        collection_info = qdrant_client.get_collection(
            collection_name=Config.QDRANT_COLLECTION
        )
        logger.info(f"Connected to collection: {Config.QDRANT_COLLECTION}")
        logger.info(f"Vector size: {collection_info.config.params.vectors.size}")

        # Initialize OpenAI
        openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        logger.info("OpenAI client initialized")

        # Check sample point
        points = qdrant_client.scroll(
            collection_name=Config.QDRANT_COLLECTION,
            limit=1,
            with_payload=True
        )
        if points and len(points[0]) > 0:
            first_point = points[0][0]
            logger.info("Sample point structure:")
            logger.info(f"Point ID: {first_point.id}")
            logger.info(f"Payload: {first_point.payload}")
            
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global qdrant_client
    if qdrant_client:
        qdrant_client.close()

def search_semantic(query: str, top_k: int = 5):
    """Search for semantically similar documents"""
    global embeddings_client, qdrant_client
    
    try:
        # Create embedding for query using the new client
        query_vector = embeddings_client.feature_extraction(
            model=Config.EMBEDDINGS_MODEL_NAME,
            text=query
        )
        
        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name=Config.QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
            score_threshold=0.5
        )
        
        return search_results
    except Exception as e:
        logger.error(f"Semantic search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

def search_exact(query: str):
    """Search for exact match in questions"""
    global qdrant_client
    
    try:
        # Create filter for exact match
        scroll_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.question",
                    match=models.MatchValue(value=query)
                )
            ]
        )
        
        # Search in Qdrant
        scroll_results = qdrant_client.scroll(
            collection_name=Config.QDRANT_COLLECTION,
            scroll_filter=scroll_filter,
            limit=1,
            with_payload=True
        )
        
        if scroll_results and len(scroll_results[0]) > 0:
            return scroll_results[0][0]
        return None
    except Exception as e:
        logger.error(f"Exact search error: {str(e)}")
        # Don't raise exception, just return None
        return None

async def get_openai_response(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", temperature: float = 0.7):
    """Get response from OpenAI"""
    global openai_client
    
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2048
        )
        return response
    except Exception as e:
        logger.error(f"OpenAI error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    """Chat completions endpoint compatible with OpenAI format"""
    global embeddings_client, qdrant_client, openai_client
    
    if not embeddings_client or not qdrant_client or not openai_client:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        # Get the user's message
        user_message = request.messages[-1].content
        logger.info(f"Processing query: {user_message}")
        
        # Step 1: Try exact match
        logger.info("Trying exact match...")
        exact_match = search_exact(user_message)
        if exact_match:
            logger.info("Found exact match")
            content = exact_match.payload.get('page_content', '')
            metadata = exact_match.payload.get('metadata', {})
            
            response_content = (
                f"{content}\n\n"
                f"(Nguồn: {metadata.get('source', 'Không rõ')})"
            )
            
            return ChatResponse(
                model=request.model,
                choices=[{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_content
                    },
                    "finish_reason": "stop"
                }]
            )
        
        # Step 2: Semantic search
        logger.info("Performing semantic search...")
        search_results = search_semantic(user_message)
        
        if not search_results:
            logger.info("No relevant documents found")
            return ChatResponse(
                model=request.model,
                choices=[{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Xin lỗi, tôi không tìm thấy thông tin liên quan đến câu hỏi của bạn."
                    },
                    "finish_reason": "stop"
                }]
            )
        
        # Extract context from search results
        context = []
        for result in search_results:
            score = result.score
            payload = result.payload
            content = payload.get("page_content", "")
            metadata = payload.get("metadata", {})
            
            # For high confidence results, return directly
            if score >= 0.85:
                logger.info(f"High confidence match found (score: {score})")
                response_content = (
                    f"{content}\n\n"
                    f"(Nguồn: {metadata.get('source', 'Không rõ')})"
                )
                
                return ChatResponse(
                    model=request.model,
                    choices=[{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_content
                        },
                        "finish_reason": "stop"
                    }]
                )
            
            if score > 0.5:
                context.append(content)
        
        # Step 3: Use OpenAI with context
        logger.info("Using OpenAI with context...")
        system_content = (
            "Bạn là trợ lý AI giúp trả lời các câu hỏi về luật giao thông. "
            "Hãy sử dụng thông tin sau để trả lời:\n\n" + 
            "\n\n".join(context)
        )
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ]
        
        openai_response = await get_openai_response(
            messages=messages,
            model=request.model,
            temperature=request.temperature
        )
        
        return ChatResponse(
            model=openai_response.model,
            choices=[{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": openai_response.choices[0].message.content
                },
                "finish_reason": openai_response.choices[0].finish_reason
            }],
            usage=openai_response.usage.model_dump() if hasattr(openai_response, 'usage') else {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global embeddings_client, qdrant_client, openai_client
    
    status = {
        "status": "healthy",
        "embeddings": embeddings_client is not None,
        "qdrant": qdrant_client is not None,
        "openai": openai_client is not None
    }
    
    if all(status.values()):
        return status
    else:
        return JSONResponse(
            status_code=503,
            content=status
        )

if __name__ == "__main__":
    uvicorn.run("rag_backend:app", host="0.0.0.0", port=8000, reload=True) 