```bash
# Test with localhost
curl -X POST "http://localhost:30000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Quy tắc giao thông đường bộ là gì?"}
    ],
    "model": "gpt-3.5-turbo"
  }'
```

```bash
# Test with production server
curl --location 'http://103.253.20.13:30000/v1/chat/completions' \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [
      {"role": "user", "content": "Quy tắc giao thông đường bộ là gì?"}
    ],
    "model": "gpt-4o"
  }'
```

```bash
# Test with local RAG backend (port 8000)
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Quy tắc giao thông đường bộ là gì?"}
    ],
    "model": "gpt-3.5-turbo"
  }'
```




