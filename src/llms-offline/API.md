```bash
curl -X POST http://localhost:8001/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Viết một đoạn văn ngắn về tầm quan trọng của AI trong giáo dục.",
    "max_tokens":60,
    "temperature":0.8,
    "top_p":0.95
  }'
```