# Hướng dẫn kết nối Qdrant và Backend qua Docker Network

## 1. Nếu cả Qdrant và Backend đều chạy bằng Docker Compose (cùng network)
- **KHÔNG dùng `localhost` để các container truy cập lẫn nhau.**
- Hãy dùng **tên service** trong docker-compose, ví dụ:
  ```yaml
  QDRANT_URL: http://qdrant:6333
  ```
  (trong đó `qdrant` là tên service của Qdrant)
- Docker sẽ tự động tạo network bridge, các service truy cập nhau qua tên service.

### Ví dụ cấu hình docker-compose:
```yaml
docker-compose.yml:

services:
  qdrant:
    image: qdrant/qdrant:v1.14.0
    container_name: qdrant
    ports:
      - "6333:6333"
    networks:
      - ragnet

  chatbot-backend:
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
- **Lưu ý:**
  - Cả hai service phải cùng khai báo chung một network (ví dụ: `ragnet`).
  - Backend truy cập Qdrant qua `http://qdrant:6333` (không phải localhost).

### Nếu bạn có nhiều file docker-compose khác nhau (multi-compose)
- Hãy tạo network external để các service ở các compose file khác nhau cùng truy cập được.
- Ví dụ:
  ```yaml
  # Tạo network external trước:
  docker network create ragnet

  # docker-compose-qdrant.yml
  services:
    qdrant:
      image: qdrant/qdrant:v1.14.0
      networks:
        - ragnet
  networks:
    ragnet:
      external: true

  # docker-compose-backend.yml
  services:
    chatbot-backend:
      build: .
      environment:
        QDRANT_URL: http://qdrant:6333
      networks:
        - ragnet
  networks:
    ragnet:
      external: true
  ```
- Khi đó, backend vẫn truy cập Qdrant qua `http://qdrant:6333`.

## 2. Nếu Qdrant chạy trên máy host, Backend chạy trong Docker
- Dùng địa chỉ đặc biệt:
  ```
  QDRANT_URL: http://host.docker.internal:6333
  ```
- `host.docker.internal` cho phép container truy cập về máy host (chỉ hỗ trợ trên Windows/Mac).

## 3. Nếu cả hai chạy local (không Docker)
- Dùng `localhost:6333` như bình thường.

---

**Tóm lại:**
- **Không dùng `localhost` trong container để truy cập container khác.**
- Dùng tên service hoặc `host.docker.internal` tùy mô hình triển khai.
