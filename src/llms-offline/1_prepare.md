Dưới đây là hướng dẫn đã sửa lại, đổi tên thư mục gốc thành `llms-offline`:

---

## 1. Cấu trúc thư mục

```
llms-offline/
├── docker-compose.yml
├── Dockerfile
├── model/                   # thư mục chứa model đã quantize (llama-3b-4bit hoặc 8bit)
└── app/
    ├── service.py          # FastAPI server
    └── inference.py        # loader + generate()
```

---

## 2. `Dockerfile`

```dockerfile
# Dockerfile
FROM nvidia/cuda:11.8-cudnn8-runtime-ubuntu22.04

# Cài đặt Python và các thư viện
RUN apt-get update && apt-get install -y python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./app /app
COPY ./model /app/model

RUN pip3 install --no-cache-dir \
    torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118 \
    transformers accelerate bitsandbytes fastapi uvicorn[standard] vllm

EXPOSE 8000
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. `docker-compose.yml`

```yaml
version: "3.8"

services:
  llm-3b:
    build: .
    image: vietnam-llm-3b:latest
    container_name: llm-3b
    ports:
      - "8000:8000"
    # GPU support với NVIDIA Container Toolkit
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=0
    restart: unless-stopped
```

---

## 4. Cách chạy

1. Clone repo vào máy có GPU + Docker
2. Copy model đã quantize vào `./model` (ví dụ: thư mục chứa `pytorch_model.bin` và config)
3. Chuyển vào thư mục `llms-offline/` và chạy:

   ```bash
   cd llms-offline
   docker compose up -d --build
   ```
4. Test API:

   ```bash
   curl -X POST http://localhost:8000/v1/generate \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Viết đoạn văn tiếng Việt về AI.","max_tokens":50}'
   ```

---

Nếu cần thêm tuỳ chỉnh hay bổ sung, bạn cứ phản hồi nhé!
