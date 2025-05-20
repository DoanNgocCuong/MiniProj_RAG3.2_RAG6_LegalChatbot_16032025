# Kế hoạch tích hợp LLM Offline vào RAG Backend

## 1. Cấu trúc và Mục tiêu

### 1.1 Mục tiêu
- Host riêng model LLM offline (Llama-3.2-3B-Instruct-Frog) trên port 8001
- Tích hợp API của model LLM offline vào hệ thống RAG
- Cho phép chuyển đổi linh hoạt giữa OpenAI và LLM offline
- Đảm bảo tính nhất quán trong API response format

### 1.2 Cấu trúc tích hợp
```
RAG Backend (port 30000)
├── EmbeddingProvider (đã có)
└── LLMProvider (mới)
    ├── OpenAI Provider
    └── Local LLM Provider (gọi API localhost:8001)
```

## 2. Các bước triển khai

### 2.1 Cấu hình LLM Service
1. Host riêng model LLM offline:
```bash
# Chạy model LLM offline trên port 8001
python -m llms_offline.main --port 8001
```

2. Kiểm tra API endpoint:
```bash
curl http://localhost:8001/health
```

### 2.2 Cập nhật cấu hình RAG Backend
```python
# Thêm vào Config class
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" hoặc "local"
LOCAL_LLM_API_URL = os.getenv("LOCAL_LLM_API_URL", "http://localhost:8001")
```

### 2.3 Tạo LLMProvider Interface
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

### 2.4 Triển khai các phương thức
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

### 2.5 Cập nhật RAG Backend
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
1. Kiểm tra LLM Service độc lập:
   - Health check endpoint
   - Generate endpoint
   - Response format

2. Kiểm tra tích hợp với RAG:
   - Chuyển đổi giữa providers
   - Format response nhất quán
   - Xử lý lỗi và retry
   - Performance monitoring

### 3.2 Monitoring
- Thêm logging cho LLM calls
- Theo dõi response time
- Error tracking

## 4. Triển khai

### 4.1 Các bước triển khai
1. Chạy LLM Service:
```bash
# Terminal 1: Chạy LLM Service
python -m llms_offline.main --port 8001
```

2. Chạy RAG Backend:
```bash
# Terminal 2: Chạy RAG Backend
python -m rag_backend.main
```

3. Test tích hợp:
```bash
# Test API
curl -X POST http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Xin chào"}]}'
```

### 4.2 Cấu hình môi trường
```env
# LLM Configuration
LLM_PROVIDER=local  # hoặc "openai"
LOCAL_LLM_API_URL=http://localhost:8001
```

## 5. Tài liệu tham khảo
- [LLM Offline API Documentation](src/llms-offline/API.md)
- [RAG Backend Code](src/back-end/rag_backend.py)

## 6. Lưu ý quan trọng

### 6.1 Về LLM Service
- Chạy độc lập trên port 8001
- Có thể chạy trên máy khác trong mạng LAN
- Cần đảm bảo port 8001 không bị block bởi firewall

### 6.2 Về RAG Backend
- Gọi API LLM Service qua localhost:8001
- Có thể cấu hình URL khác qua biến môi trường
- Xử lý timeout và retry khi gọi API

### 6.3 Về Performance
- LLM Service cần GPU để chạy hiệu quả
- RAG Backend có thể chạy trên CPU
- Cần monitor memory usage của cả hai service
