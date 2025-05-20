#!/usr/bin/env python3
"""
RAG Backend API for Legal Chatbot
Based on Qdrant Pipeline
"""

import os
import asyncio
import uvicorn
import aiohttp
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
    QDRANT_URL = "http://host.docker.internal:6333"
    QDRANT_API_KEY = "my_super_secret_key"
    QDRANT_COLLECTION = os.getenv("COLLECTION_NAME", "legal_rag")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "offline")  # "offline" or "huggingface"
    EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "http://embedding-offline-service:8000")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "local"
    LOCAL_LLM_API_URL = os.getenv("LOCAL_LLM_API_URL", "http://localhost:8001")

    @classmethod
    def log_config(cls):
        """Log current configuration"""
        logger.info("Current configuration:")
        logger.info(f"LLM_PROVIDER: {cls.LLM_PROVIDER}")
        logger.info(f"EMBEDDING_PROVIDER: {cls.EMBEDDING_PROVIDER}")
        logger.info(f"EMBEDDING_API_URL: {cls.EMBEDDING_API_URL}")
        logger.info(f"LOCAL_LLM_API_URL: {cls.LOCAL_LLM_API_URL}")

# Log configuration on startup
Config.log_config()

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

class EmbeddingProvider:
    """Interface for different embedding providers"""
    def __init__(self, provider_type: str = "offline"):
        self.provider_type = provider_type
        self.hf_client = None
        self.offline_url = Config.EMBEDDING_API_URL
        
        if provider_type == "huggingface":
            self.hf_client = InferenceClient(
                provider="hf-inference",
                api_key=Config.HUGGINGFACE_API_KEY
            )
    
    async def get_embeddings(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Get embeddings from the selected provider"""
        if self.provider_type == "huggingface":
            return self._get_hf_embeddings(texts)
        else:
            return await self._get_offline_embeddings(texts, batch_size)
    
    def _get_hf_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings from HuggingFace"""
        try:
            embeddings = self.hf_client.feature_extraction(
                model=Config.EMBEDDINGS_MODEL_NAME,
                text=texts
            )
            return embeddings
        except Exception as e:
            logger.error(f"HuggingFace embedding error: {str(e)}")
            raise
    
    async def _get_offline_embeddings(self, texts: List[str], batch_size: int) -> List[List[float]]:
        """Get embeddings from offline API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.offline_url}/embeddings",
                    json={
                        "texts": texts,
                        "batch_size": batch_size
                    }
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Offline API error: {await response.text()}")
                    result = await response.json()
                    return result["embeddings"]
        except Exception as e:
            logger.error(f"Offline embedding error: {str(e)}")
            raise

class LLMProvider:
    def __init__(self, provider_type: str = "openai"):
        self.provider_type = provider_type
        self.openai_client = None
        self.local_url = Config.LOCAL_LLM_API_URL
        
        if provider_type == "openai":
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    async def get_completion(self, messages: List[Dict[str, str]], 
                           model: str = "gpt-3.5-turbo",
                           temperature: float = 0.7) -> Dict:
        if self.provider_type == "openai":
            return await self._get_openai_completion(messages, model, temperature)
        else:
            return await self._get_llama_completion(messages, temperature)
    
    async def _get_openai_completion(self, messages: List[Dict[str, str]], 
                                   model: str = "gpt-3.5-turbo",
                                   temperature: float = 0.7) -> Dict:
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2048
            )
            return {
                "model": response.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content
                    },
                    "finish_reason": response.choices[0].finish_reason
                }],
                "usage": response.usage.model_dump() if hasattr(response, 'usage') else {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    
    async def _get_llama_completion(self, messages: List[Dict[str, str]], 
                                  temperature: float = 0.7) -> Dict:
        try:
            # Chuyển đổi messages thành prompt
            prompt = self._convert_messages_to_prompt(messages)
            
            # Gọi Llama API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.local_url}/v1/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": 2048,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Llama API error: {await response.text()}")
                    result = await response.json()
                    return self._format_llama_response(result)
        except Exception as e:
            logger.error(f"Llama API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Llama API error: {str(e)}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Chuyển đổi messages thành prompt cho Llama"""
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        prompt += "Assistant: "
        return prompt
    
    def _format_llama_response(self, result: Dict) -> Dict:
        """Format Llama response thành format tương tự OpenAI"""
        return {
            "model": "llama-3.2-3b-instruct-frog",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result["text"]
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

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
embeddings_provider = None
qdrant_client = None
llm_provider = None

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    global embeddings_provider, qdrant_client, llm_provider
    
    try:
        logger.info("Initializing RAG Backend...")
        
        # Initialize embedding provider
        embeddings_provider = EmbeddingProvider(provider_type=Config.EMBEDDING_PROVIDER)
        logger.info(f"Embedding provider initialized: {Config.EMBEDDING_PROVIDER}")

        # Initialize Qdrant
        qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            timeout=10
        )
        logger.info(f"Qdrant client initialized (local): {Config.QDRANT_URL}")

        # Initialize LLM provider
        llm_provider = LLMProvider(provider_type=Config.LLM_PROVIDER)
        logger.info(f"LLM provider initialized: {Config.LLM_PROVIDER}")

        # Verify collection
        collection_info = qdrant_client.get_collection(
            collection_name=Config.QDRANT_COLLECTION
        )
        logger.info(f"Connected to collection: {Config.QDRANT_COLLECTION}")
        logger.info(f"Vector size: {collection_info.config.params.vectors.size}")
        
        # Thêm code debug
        points = qdrant_client.scroll(
            collection_name=Config.QDRANT_COLLECTION,
            limit=1,
            with_payload=True
        )
        if points and len(points[0]) > 0:
            first_point = points[0][0]
            logger.info("Cấu trúc dữ liệu mẫu:")
            logger.info(f"ID: {first_point.id}")
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

async def search_semantic(query: str, top_k: int = 5):
    """Search for semantically similar documents"""
    global embeddings_provider, qdrant_client
    
    try:
        # Get embedding from provider
        query_vector = (await embeddings_provider.get_embeddings([query]))[0]
        
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
        logger.info("-"*30)
        logger.info("CHI TIẾT TÌM KIẾM CHÍNH XÁC:")
        logger.info(f"Câu hỏi cần tìm: '{query}'")
        
        # Create filter for exact match
        scroll_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.question",
                    match=models.MatchValue(value=query)
                )
            ]
        )
        
        logger.info("Filter được tạo:")
        logger.info(f"Field: metadata.question")
        logger.info(f"Value cần match: {query}")
        
        # Search in Qdrant
        logger.info("Đang gọi Qdrant API...")
        scroll_results = qdrant_client.scroll(
            collection_name=Config.QDRANT_COLLECTION,
            scroll_filter=scroll_filter,
            limit=1,
            with_payload=True
        )
        
        # Log chi tiết kết quả
        if scroll_results and len(scroll_results[0]) > 0:
            first_point = scroll_results[0][0]
            logger.info("✓ Tìm thấy kết quả trong DB:")
            logger.info(f"ID: {first_point.id}")
            logger.info(f"Question trong DB: {first_point.payload.get('metadata', {}).get('question', '')}")
            logger.info(f"Content: {first_point.payload.get('page_content', '')[:100]}...")
            return first_point
        else:
            logger.info("✗ Không tìm thấy kết quả trong DB")
            # Thêm log để kiểm tra dữ liệu trong DB
            logger.info("Kiểm tra dữ liệu mẫu trong DB:")
            sample_points = qdrant_client.scroll(
                collection_name=Config.QDRANT_COLLECTION,
                limit=5,  # Lấy 5 điểm dữ liệu mẫu
                with_payload=True
            )
            if sample_points and len(sample_points[0]) > 0:
                logger.info("Dữ liệu mẫu trong DB:")
                for idx, point in enumerate(sample_points[0], 1):
                    logger.info(f"\nMẫu #{idx}:")
                    logger.info(f"Question: {point.payload.get('metadata', {}).get('question', '')}")
                    logger.info(f"Content: {point.payload.get('page_content', '')[:100]}...")
            return None
            
    except Exception as e:
        logger.error(f"❌ Lỗi khi tìm kiếm chính xác: {str(e)}")
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
    global embeddings_provider, qdrant_client, llm_provider
    
    if not embeddings_provider or not qdrant_client or not llm_provider:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        user_message = request.messages[-1].content
        logger.info("="*50)
        logger.info(f"BẮT ĐẦU XỬ LÝ CÂU HỎI: {user_message}")
        logger.info("="*50)
        
        # BƯỚC 1: KIỂM TRA KHỚP CHÍNH XÁC
        logger.info("-"*30)
        logger.info("BƯỚC 1: KIỂM TRA KHỚP CHÍNH XÁC")
        logger.info(f"Đang tìm kiếm câu hỏi giống hệt: '{user_message}'")
        exact_match = search_exact(user_message)
        
        if exact_match:
            logger.info("✓ TÌM THẤY KHỚP CHÍNH XÁC")
            logger.info(f"ID: {exact_match.id}")
            logger.info(f"Score: {exact_match.score if hasattr(exact_match, 'score') else 'N/A'}")
            logger.info(f"Content: {exact_match.payload.get('page_content', '')[:100]}...")
            logger.info(f"Metadata: {exact_match.payload.get('metadata', {})}")
            
            response_content = (
                f"{exact_match.payload.get('page_content', '')}\n\n"
                f"(Nguồn: {exact_match.payload.get('metadata', {}).get('source', 'Không rõ')})"
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
        else:
            logger.info("✗ KHÔNG TÌM THẤY KHỚP CHÍNH XÁC")
        
        # BƯỚC 2: TÌM KIẾM NGỮ NGHĨA
        logger.info("-"*30)
        logger.info("BƯỚC 2: TÌM KIẾM NGỮ NGHĨA")
        logger.info("Đang tìm kiếm các tài liệu liên quan...")
        search_results = await search_semantic(user_message)
        
        if not search_results:
            logger.info("✗ KHÔNG TÌM THẤY KẾT QUẢ NGỮ NGHĨA")
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
        
        logger.info(f"✓ Tìm thấy {len(search_results)} kết quả ngữ nghĩa")
        
        # Phân tích kết quả
        context = []
        for idx, result in enumerate(search_results, 1):
            score = result.score
            payload = result.payload
            content = payload.get("page_content", "")
            metadata = payload.get("metadata", {})
            
            logger.info(f"\nKết quả #{idx}:")
            logger.info(f"Score: {score}")
            logger.info(f"Source: {metadata.get('source', 'Không rõ')}")
            logger.info(f"Content preview: {content[:100]}...")
            
            if score >= 0.85:
                logger.info("✓ Tìm thấy kết quả có độ tin cậy cao")
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
                logger.info("✓ Thêm vào context cho LLM")
        
        # BƯỚC 3: SỬ DỤNG LLM
        if context:
            logger.info("-"*30)
            logger.info("BƯỚC 3: SỬ DỤNG LLM")
            logger.info(f"Số lượng context đã thu thập: {len(context)}")
            logger.info("Đang gọi LLM để tổng hợp câu trả lời...")
            system_content = (
                "Bạn là trợ lý AI giúp trả lời các câu hỏi về luật giao thông. "
                "Hãy sử dụng thông tin sau để trả lời:\n\n" + 
                "\n\n".join(context)
            )
            
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message}
            ]
            
            response = await llm_provider.get_completion(
                messages=messages,
                model=request.model,
                temperature=request.temperature
            )
            
            return ChatResponse(
                model=response["model"],
                choices=response["choices"],
                usage=response["usage"]
            )
        else:
            logger.info("✗ Không đủ context để gọi LLM")
        
        logger.info("="*50)
        logger.info("KẾT THÚC XỬ LÝ CÂU HỎI")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"❌ LỖI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global embeddings_provider, qdrant_client, openai_client
    
    status = {
        "status": "healthy",
        "embeddings": embeddings_provider is not None,
        "qdrant": qdrant_client is not None,
        "openai": openai_client is not None,
        "embedding_provider": Config.EMBEDDING_PROVIDER
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