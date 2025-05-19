# Báo cáo tích hợp Embedding Offline

## 1. Phân tích sự thay đổi

### 1.1. Thay đổi trong cấu hình (Config)
```python
# Phiên bản Online (v1)
class Config:
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = os.getenv("COLLECTION_NAME", "legal_rag")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Phiên bản Offline (v2)
class Config:
    # Thêm các cấu hình mới
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "offline")  # "offline" or "huggingface"
    EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "http://localhost:8000")
```

### 1.2. Thay đổi trong xử lý Embedding
```python
# Phiên bản Online (v1)
embeddings_client = InferenceClient(
    provider="hf-inference",
    api_key=Config.HUGGINGFACE_API_KEY
)

# Phiên bản Offline (v2)
class EmbeddingProvider:
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
        if self.provider_type == "huggingface":
            return self._get_hf_embeddings(texts)
        else:
            return await self._get_offline_embeddings(texts, batch_size)
```

### 1.3. Thay đổi trong Health Check
```python
# Phiên bản Online (v1)
status = {
    "status": "healthy",
    "embeddings": embeddings_client is not None,
    "qdrant": qdrant_client is not None,
    "openai": openai_client is not None
}

# Phiên bản Offline (v2)
status = {
    "status": "healthy",
    "embeddings": embeddings_provider is not None,
    "qdrant": qdrant_client is not None,
    "openai": openai_client is not None,
    "embedding_provider": Config.EMBEDDING_PROVIDER
}
```

## 2. Các thay đổi chính

1. **Cấu trúc Embedding Provider**:
   - Chuyển từ sử dụng trực tiếp HuggingFace sang mô hình Provider Pattern
   - Hỗ trợ nhiều loại provider (offline/huggingface)
   - Thêm xử lý bất đồng bộ (async) cho offline provider

2. **Cấu hình**:
   - Thêm biến môi trường EMBEDDING_PROVIDER
   - Thêm biến môi trường EMBEDDING_API_URL
   - Mặc định sử dụng offline provider

3. **Xử lý Embedding**:
   - Thêm batch processing cho offline embedding
   - Tách biệt logic xử lý cho từng loại provider
   - Cải thiện error handling

## 3. Quá trình triển khai

### 3.1. Bước 1: Tạo Embedding API Service
```yaml
# embedding-model-offline/docker-compose.yml
version: '3.8'
services:
  embedding-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: embedding-api
    ports:
      - "8000:8000"
    volumes:
      - ./model:/app/model
      - ./app:/app
      - ./logs:/app/logs
    environment:
      - MODEL_PATH=/app/model
      - MODEL_NAME=paraphrase-multilingual-mpnet-base-v2
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

### 3.2. Bước 2: Cập nhật Docker Compose chung
```yaml
# docker-compose.yml
services:
  embedding-api:
    build:
      context: ./embedding-model-offline
      dockerfile: Dockerfile
    networks:
      - legal-chatbot-network
    # ... các cấu hình khác

  backend:
    environment:
      - EMBEDDING_PROVIDER=offline
      - EMBEDDING_API_URL=http://embedding-api:8000
    depends_on:
      - embedding-api
    networks:
      - legal-chatbot-network
```

## 7. Tài liệu tham khảo

1. [Sentence Transformers Documentation](https://www.sbert.net/)
2. [FastAPI Documentation](https://fastapi.tiangolo.com/)
3. [Docker Documentation](https://docs.docker.com/)
