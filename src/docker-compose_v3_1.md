
Docker compose cho con llms-service (3B-FP16) mà mỗi lần nó ngốn của em 8min để đợi load models anh ạ. 

(Em đang ghép model local này vào luồng RAG cũ), muốn docker compose 1 phát ăn luôn mà có vẻ nếu thế thì mỗi lần build RAG lại phải build cả llms-services lại đợi 8min (vì image của llms-service nó ko có model, model được mount nên mất time load vào GPU). 


```bash
Loading checkpoint shards: 0%| | 0/2 [00:00<?, ?it/s]


Loading checkpoint shards: 50%|█████ | 1/2 [03:46<03:46, 226.60s/it]


Loading checkpoint shards: 100%|██████████| 2/2 [04:51<00:00, 131.35s/it]


Loading checkpoint shards: 100%|██████████| 2/2 [04:51<00:00, 145.64s/it]


2025-05-19 19:55:48 | [After model load] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.98GB (allocated) / 6.59GB (reserved) | RAM: 1.68GB/7.63GB (26.7%)


INFO: Started server process [1]


INFO: Waiting for application startup.


INFO: Application startup complete.


INFO: Uvicorn running on http://0.0.0.0:8000⁠ (Press CTRL+C to quit)
```


# Cấu trúc và Cấu hình Docker Compose v3

## 1. Tổng quan các Service

### 1.1 Backend Service
- **Tên service**: `backend`
- **Image**: `chatbot-rag-backend:latest`
- **Container**: `chatbot-rag-backend`
- **Port**: 30000:30000
- **Volumes**: 
  - `./back-end/.env:/app/.env`
- **Dependencies**: 
  - `embedding-service`
  - `llms-service`
- **Network**: `legal-chatbot-network`

### 1.2 Frontend Service
- **Tên service**: `frontend`
- **Image**: `chatbot-rag-frontend:latest`
- **Container**: `chatbot-rag-frontend`
- **Port**: 30001:30001
- **Volumes**:
  - `./front-end/nginx.conf:/etc/nginx/conf.d/default.conf:ro`
- **Dependencies**: 
  - `backend`
- **Network**: `legal-chatbot-network`

### 1.3 Embedding Service
- **Tên service**: `embedding-service`
- **Image**: `chatbot-embedding-model-offline:latest`
- **Container**: `chatbot-embedding-model-offline`
- **Port**: 8000:8000
- **Volumes**:
  - `./embedding-model-offline/model:/app/model`
  - `./embedding-model-offline/app:/app`
  - `./embedding-model-offline/logs:/app/logs`
- **Environment**:
  - `MODEL_PATH=/app/model`
  - `MODEL_NAME=paraphrase-multilingual-mpnet-base-v2`
- **Resources**:
  - Memory limit: 4GB
  - Memory reservation: 2GB
- **Network**: `legal-chatbot-network`

### 1.4 LLM Service
- **Tên service**: `llms-service`
- **Image**: `chatbot-llms-offline:latest`
- **Container**: `chatbot-llms-offline`
- **Port**: 8001:8000
- **Volumes**:
  - `./llms-offline/model:/app/model`
  - `./llms-offline/logs:/app/logs`
- **Environment**:
  - `PYTHONUNBUFFERED=1`
  - `TORCH_CUDA_ARCH_LIST="8.6"`
- **Resources**:
  - Memory limit: 12GB
  - GPU: NVIDIA (1 device)
- **Network**: `legal-chatbot-network`

## 2. Cấu hình .env cần thiết

### 2.1 Backend (.env)
```env
# Qdrant Configuration
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-api-key>
COLLECTION_NAME=legal_rag

# Embedding Configuration
EMBEDDING_PROVIDER=offline
EMBEDDING_API_URL=http://embedding-service:8000  # Sử dụng tên service trong Docker network

# LLM Configuration
LLM_PROVIDER=local
LOCAL_LLM_API_URL=http://llms-service:8000  # Sử dụng tên service trong Docker network

# OpenAI Configuration (optional)
OPENAI_API_KEY=<your-openai-api-key>

# HuggingFace Configuration (optional)
HUGGINGFACE_API_KEY=<your-huggingface-api-key>
EMBEDDINGS_MODEL_NAME=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

## 3. Luồng xử lý

1. **Frontend -> Backend**:
   - Frontend gửi request đến Backend qua port 30000
   - Backend xử lý request và tương tác với các service khác

2. **Backend -> Embedding Service**:
   - Backend gửi text đến Embedding Service qua port 8000
   - Embedding Service chuyển đổi text thành vector
   - Kết quả được trả về Backend

3. **Backend -> LLM Service**:
   - Backend gửi prompt đến LLM Service qua port 8000
   - LLM Service xử lý và tạo câu trả lời
   - Kết quả được trả về Backend

## 4. Lưu ý quan trọng

1. **URL trong Docker Network**:
   - Sử dụng tên service thay vì localhost
   - Ví dụ: `http://embedding-service:8000` thay vì `http://localhost:8000`
   - Các service giao tiếp với nhau qua tên service trong Docker network

2. **Resource Management**:
   - Embedding Service: 4GB RAM
   - LLM Service: 12GB RAM + GPU
   - Đảm bảo máy chủ có đủ tài nguyên

3. **Health Checks**:
   - Tất cả service đều có health check
   - Interval: 30s
   - Timeout: 10s
   - Retries: 3

4. **Logging**:
   - Tất cả service đều sử dụng json-file driver
   - Max size: 10MB
   - Max files: 3

## 5. Các bước triển khai

1. **Chuẩn bị**:
   ```bash
   # Tạo các thư mục cần thiết
   mkdir -p embedding-model-offline/{model,app,logs}
   mkdir -p llms-offline/{model,logs}
   ```

2. **Cấu hình**:
   - Copy file .env.example thành .env
   - Cập nhật các biến môi trường cần thiết
   - Đảm bảo URL trong .env sử dụng đúng tên service

3. **Khởi động**:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

4. **Kiểm tra**:
   ```bash
   # Kiểm tra trạng thái các container
   docker-compose ps
   
   # Xem logs của tất cả service
   docker-compose logs -f
   
   # Xem logs của service cụ thể
   docker-compose logs -f backend
   docker-compose logs -f embedding-service
   docker-compose logs -f llms-service
   ```

## 6. Xử lý sự cố

1. **Kiểm tra kết nối**:
   ```bash
   # Kiểm tra network
   docker network inspect legal-chatbot-network
   
   # Kiểm tra logs của service
   docker-compose logs -f <service-name>
   ```

2. **Các lỗi thường gặp**:
   - Lỗi kết nối: Kiểm tra tên service trong .env
   - Lỗi memory: Kiểm tra resource limits
   - Lỗi GPU: Kiểm tra cấu hình NVIDIA

3. **Khởi động lại service**:
   ```bash
   docker-compose restart <service-name>
   ```