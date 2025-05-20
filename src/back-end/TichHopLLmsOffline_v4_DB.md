Đang khác network đó, bạn dùng cái internal docker đi.

---
Chính xác! Nếu backend và Qdrant **chạy trong các container Docker khác nhau**, bạn **không thể dùng `localhost`** để các container truy cập lẫn nhau.  
Thay vào đó, bạn nên dùng **tên service** trong Docker Compose network, hoặc dùng `host.docker.internal` nếu backend chạy trong Docker và Qdrant chạy trên máy host (Windows/Mac).

---

## 1. Nếu cả backend và Qdrant đều chạy bằng Docker Compose

**Ví dụ docker-compose.yml:**
```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.14.0
    ports:
      - "6333:6333"
    networks:
      - ragnet

  chatbot-rag-backend:
    build: .
    environment:
      QDRANT_URL: http://qdrant:6333
      QDRANT_API_KEY: my_super_secret_key
    depends_on:
      - qdrant
    networks:
      - ragnet

networks:
  ragnet:
    driver: bridge
```

**Trong code backend:**
```python
QDRANT_URL = "http://qdrant:6333"
```
- `qdrant` là **tên service** của Qdrant trong docker-compose.

---

## 2. Nếu Qdrant chạy trên máy host, backend chạy trong Docker

**Trong code backend:**
```python
QDRANT_URL = "http://host.docker.internal:6333"
```
- `host.docker.internal` là địa chỉ đặc biệt để container truy cập về máy host (chỉ hỗ trợ trên Windows/Mac).

---

## 3. Nếu cả hai chạy local (không Docker) thì dùng `localhost`.

---

## Tóm lại

- **Không dùng `localhost` trong container để truy cập service ở container khác!**
- Dùng `http://qdrant:6333` (nếu cùng docker-compose network)  
- Hoặc `http://host.docker.internal:6333` (nếu Qdrant chạy trên máy host, backend trong Docker)

---

Bạn muốn tôi cập nhật lại code backend để dùng `host.docker.internal` hoặc tên service không? Nếu có, hãy xác nhận mô hình bạn đang dùng (cả hai đều Docker, hay chỉ backend Docker, hay cả hai local)!

---