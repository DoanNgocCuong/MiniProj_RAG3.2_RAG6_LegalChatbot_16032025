import os
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("embedding_api.log")
    ]
)

logger = logging.getLogger("embedding-api")

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Embedding API cho môi trường Offline",
    description="API tạo embeddings từ văn bản sử dụng mô hình sentence-transformers",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa models cho API
class EmbeddingRequest(BaseModel):
    texts: List[str]
    batch_size: Optional[int] = 32

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dimensions: int
    model_name: str
    processing_time_ms: float

# Biến toàn cục cho model
model = None

def get_model():
    """Singleton pattern để tải và lưu mô hình trong bộ nhớ"""
    global model
    if model is None:
        model_path = os.environ.get("MODEL_PATH", "/app/model")
        model_name = os.environ.get("MODEL_NAME", "paraphrase-multilingual-mpnet-base-v2")
        logger.info(f"Đang tải mô hình {model_name} từ {model_path}")
        try:
            model = SentenceTransformer(model_name, cache_folder=model_path)
            logger.info("Mô hình đã được tải thành công")
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình: {str(e)}")
            raise RuntimeError(f"Không thể tải mô hình: {str(e)}")
    return model

@app.get("/")
def health_check():
    """Endpoint kiểm tra trạng thái"""
    return {
        "status": "online", 
        "model": "paraphrase-multilingual-mpnet-base-v2",
        "version": "1.0.0"
    }

@app.post("/embeddings", response_model=EmbeddingResponse)
def create_embeddings(request: EmbeddingRequest, model: SentenceTransformer = Depends(get_model)):
    """Tạo embeddings từ văn bản đầu vào"""
    try:
        start_time = time.time()
        
        # Kiểm tra đầu vào
        if not request.texts:
            raise HTTPException(status_code=400, detail="Danh sách văn bản không được để trống")
        
        if len(request.texts) > 100:
            logger.warning(f"Số lượng văn bản lớn: {len(request.texts)}")
        
        # Tạo embedding
        embeddings = model.encode(request.texts, batch_size=request.batch_size)
        
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # ms
        
        # Ghi log
        logger.info(f"Đã tạo {len(embeddings)} embeddings trong {processing_time:.2f}ms")
        
        # Chuẩn bị phản hồi
        return {
            "embeddings": embeddings.tolist(),
            "dimensions": embeddings.shape[1],
            "model_name": "paraphrase-multilingual-mpnet-base-v2",
            "processing_time_ms": processing_time
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi tạo embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo embeddings: {str(e)}")

@app.get("/info")
def model_info(model: SentenceTransformer = Depends(get_model)):
    """Trả về thông tin về mô hình"""
    try:
        info = {
            "model_name": "paraphrase-multilingual-mpnet-base-v2",
            "embedding_dimension": model.get_sentence_embedding_dimension(),
            "supports_languages": ["Vietnamese", "English", "Chinese", "Japanese", "Korean", "và hầu hết các ngôn ngữ phổ biến"],
            "max_sequence_length": model.get_max_seq_length(),
            "version": "1.0.0"
        }
        return info
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin mô hình: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy thông tin mô hình: {str(e)}")

@app.post("/similarity")
def compute_similarity(texts: List[str], model: SentenceTransformer = Depends(get_model)):
    """Tính toán độ tương đồng giữa các văn bản"""
    if len(texts) < 2:
        raise HTTPException(status_code=400, detail="Cần ít nhất 2 văn bản để tính độ tương đồng")
    
    try:
        embeddings = model.encode(texts)
        
        # Tính toán độ tương đồng cosine giữa tất cả các cặp
        similarity_matrix = np.zeros((len(texts), len(texts)))
        for i in range(len(texts)):
            for j in range(len(texts)):
                e1 = embeddings[i]
                e2 = embeddings[j]
                similarity = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
                similarity_matrix[i, j] = similarity
                
        return {
            "similarity_matrix": similarity_matrix.tolist(),
            "texts": texts
        }
    except Exception as e:
        logger.error(f"Lỗi khi tính độ tương đồng: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tính độ tương đồng: {str(e)}") 