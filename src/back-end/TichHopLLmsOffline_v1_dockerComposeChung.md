# Kế hoạch tích hợp LLM Offline vào RAG Backend

## 1. Cấu trúc và Mục tiêu

### 1.1 Mục tiêu
- Tích hợp dịch vụ LLM offline (Llama-3.2-3B-Instruct-Frog) vào hệ thống RAG
- Cho phép chuyển đổi linh hoạt giữa OpenAI và LLM offline
- Đảm bảo tính nhất quán trong API response format

### 1.2 Cấu trúc tích hợp
```
RAG Backend
├── EmbeddingProvider (đã có)
└── LLMProvider (mới)
    ├── OpenAI Provider
    └── Local LLM Provider
```

## 2. Các bước triển khai

### 2.1 Cập nhật cấu hình
```python
# Thêm vào Config class
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" hoặc "local"
LOCAL_LLM_API_URL = os.getenv("LOCAL_LLM_API_URL", "http://localhost:8001")
```

### 2.2 Tạo LLMProvider Interface
```python
class LLMProvider:
    def __init__(self, provider_type: str = "openai"):
        self.provider_type = provider_type
        self.openai_client = None
        self.local_url = Config.LOCAL_LLM_API_URL

    async def get_completion(self, messages: List[Dict[str, str]], 
                           model: str = "gpt-3.5-turbo",
                           temperature: float = 0.7) -> Dict:
        if self.provider_type == "openai":
            return await self._get_openai_completion(messages, model, temperature)
        else:
            return await self._get_local_completion(messages, temperature)
```

### 2.3 Triển khai các phương thức
1. `_get_openai_completion`: Sử dụng OpenAI API (đã có)
2. `_get_local_completion`: Gọi API local LLM với format:
```python
async def _get_local_completion(self, messages: List[Dict[str, str]], 
                              temperature: float = 0.7) -> Dict:
    # Chuyển đổi messages thành prompt
    prompt = self._convert_messages_to_prompt(messages)
    
    # Gọi API local
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{self.local_url}/v1/generate",
            json={
                "prompt": prompt,
                "max_tokens": 2048,
                "temperature": temperature,
                "top_p": 0.95,
                "do_sample": True
            }
        ) as response:
            result = await response.json()
            return self._format_local_response(result)
```

### 2.4 Cập nhật RAG Backend
1. Thêm LLMProvider vào startup:
```python
@app.on_event("startup")
async def startup_event():
    global llm_provider
    llm_provider = LLMProvider(provider_type=Config.LLM_PROVIDER)
```

2. Cập nhật endpoint chat:
```python
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    # ... existing code ...
    
    # Thay thế OpenAI call bằng LLMProvider
    response = await llm_provider.get_completion(
        messages=messages,
        model=request.model,
        temperature=request.temperature
    )
```

## 3. Kiểm thử

### 3.1 Test Cases
1. Chuyển đổi giữa providers
2. Format response nhất quán
3. Xử lý lỗi và retry
4. Performance monitoring

### 3.2 Monitoring
- Thêm logging cho LLM calls
- Theo dõi response time
- Error tracking

## 4. Triển khai

### 4.1 Các bước triển khai
1. Cập nhật code theo kế hoạch
2. Test locally với cả hai providers
3. Cập nhật documentation
4. Deploy và monitor

### 4.2 Cấu hình môi trường
```env
LLM_PROVIDER=local  # hoặc "openai"
LOCAL_LLM_API_URL=http://localhost:8001
```

## 5. Tài liệu tham khảo
- [LLM Offline API Documentation](src/llms-offline/API.md)
- [RAG Backend Code](src/back-end/rag_backend.py)

## 6. Cập nhật các file

### 6.1 Cập nhật rag_backend.py
1. Thêm biến môi trường mới vào class Config:
```python
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" hoặc "local"
LOCAL_LLM_API_URL = os.getenv("LOCAL_LLM_API_URL", "http://localhost:8001")
```

2. Thêm LLMProvider class và cập nhật startup_event:
```python
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
            return await self._get_local_completion(messages, temperature)

    async def _get_local_completion(self, messages: List[Dict[str, str]], 
                                  temperature: float = 0.7) -> Dict:
        prompt = self._convert_messages_to_prompt(messages)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.local_url}/v1/generate",
                json={
                    "prompt": prompt,
                    "max_tokens": 2048,
                    "temperature": temperature,
                    "top_p": 0.95,
                    "do_sample": True
                }
            ) as response:
                result = await response.json()
                return self._format_local_response(result)
```

3. Cập nhật hàm chat_completions để sử dụng LLMProvider:
```python
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    # ... existing code ...
    
    # Thay thế OpenAI call bằng LLMProvider
    response = await llm_provider.get_completion(
        messages=messages,
        model=request.model,
        temperature=request.temperature
    )
```

### 6.2 Cập nhật docker-compose.yml
Thêm service LLM offline vào docker-compose.yml:
```yaml
services:
  # ... existing services ...
  
  llm-service:
    build:
      context: ./llms-offline
      dockerfile: Dockerfile
    container_name: llm-service
    ports:
      - "8001:8000"
    volumes:
      - ./llms-offline/model:/app/model
      - ./llms-offline/logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 12G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - PYTHONUNBUFFERED=1
      - TORCH_CUDA_ARCH_LIST="8.6"
    networks:
      - legal-chatbot-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 6.3 Cập nhật .env và .env.example
Thêm các biến môi trường mới vào cả hai file:

```env
# LLM Configuration
LLM_PROVIDER=local  # hoặc "openai"
LOCAL_LLM_API_URL=http://llm-service:8000  # URL trong Docker network
```

Lưu ý: URL của LLM service trong Docker network sẽ là `http://llm-service:8000` thay vì `http://localhost:8001` vì các container giao tiếp với nhau thông qua Docker network.


---
Tôi sẽ giúp bạn cập nhật các file theo yêu cầu. Hãy thực hiện từng bước một.

1. Đầu tiên, tôi sẽ cập nhật file `TichHopLLmsOffline.md` để thêm các bước cập nhật cụ thể:



Bây giờ tôi sẽ cập nhật file `docker-compose.yml` để thêm service LLM offline:



Bây giờ tôi sẽ cập nhật file `rag_backend.py` để thêm LLMProvider:



Tôi đã hoàn thành việc cập nhật các file theo yêu cầu của bạn. Tóm tắt các thay đổi:

1. Đã cập nhật `TichHopLLmsOffline.md` với hướng dẫn chi tiết về cách cập nhật các file.

2. Đã cập nhật `docker-compose.yml` để thêm service LLM offline với các cấu hình cần thiết:
   - Port mapping: 8001:8000
   - Volume mounts cho model và logs
   - GPU support
   - Health check
   - Logging configuration

3. Đã cập nhật `rag_backend.py` với:
   - Thêm biến môi trường mới vào Config class
   - Thêm LLMProvider class để xử lý cả OpenAI và local LLM
   - Cập nhật startup_event để khởi tạo LLMProvider
   - Cập nhật chat_completions endpoint để sử dụng LLMProvider
   - Cập nhật health check endpoint

Bạn cần thêm các biến môi trường sau vào file `.env` và `.env.example`:

```env
# LLM Configuration
LLM_PROVIDER=local  # hoặc "openai"
LOCAL_LLM_API_URL=http://llm-service:8000  # URL trong Docker network
```

Lưu ý: URL của LLM service trong Docker network sẽ là `http://llm-service:8000` thay vì `http://localhost:8001` vì các container giao tiếp với nhau thông qua Docker network.

Bạn có cần tôi giải thích thêm về bất kỳ phần nào không?
