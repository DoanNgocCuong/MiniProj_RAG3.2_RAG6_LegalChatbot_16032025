Từ logs tôi thấy cấu hình đã đúng:

```
2025-05-20 07:45:27,884 - rag-backend - INFO - Current configuration:
2025-05-20 07:45:27,884 - rag-backend - INFO - LLM_PROVIDER: openai
2025-05-20 07:45:27,884 - rag-backend - INFO - EMBEDDING_PROVIDER: offline
2025-05-20 07:45:27,884 - rag-backend - INFO - EMBEDDING_API_URL: http://embedding-offline-service:8000
2025-05-20 07:45:27,884 - rag-backend - INFO - LOCAL_LLM_API_URL: http://localhost:8001
```

Và LLM provider cũng đã được khởi tạo đúng:
```
2025-05-20 07:45:28,830 - rag-backend - INFO - LLM provider initialized: openai
```

Bây giờ bạn có thể test API với:

```bash
curl -X POST http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Xin chào"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }'
```

Lưu ý:
1. Port là 30000 (không phải 8000)
2. Model mặc định là "gpt-3.5-turbo"
3. Đảm bảo OPENAI_API_KEY trong file .env đã được set đúng

Bạn có muốn tôi hướng dẫn cách test chi tiết hơn không?


----

# Thêm log để kiểm soát các config tránh xung đột. 
Và có vẻ nnhuw muuoosn thay đổi .env thì phải docker compose down thì phải ? 