# Hướng dẫn triển khai Qdrant Vector Database

## Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt Qdrant bằng Docker](#cài-đặt-qdrant-bằng-docker)
3. [So sánh Qdrant Local vs Cloud](#so-sánh-qdrant-local-vs-cloud)
4. [Thao tác CRUD cơ bản](#thao-tác-crud-cơ-bản)
5. [Backup và Restore](#backup-và-restore)
6. [Monitoring và Logging](#monitoring-và-logging)
7. [Troubleshooting](#troubleshooting)

## Giới thiệu

Qdrant là một vector database mã nguồn mở, được thiết kế đặc biệt cho các ứng dụng AI/ML. Nó hỗ trợ:
- Lưu trữ và tìm kiếm vector hiệu quả
- Hỗ trợ nhiều metric distance (Cosine, Euclidean, Dot)
- REST API và gRPC interface
- Web UI để quản lý
- Hỗ trợ cả triển khai local và cloud

## Cài đặt Qdrant bằng Docker

### 1. Yêu cầu hệ thống
- Docker Engine 20.10+
- Docker Compose v2.0+
- ít nhất 2GB RAM
- 10GB ổ cứng trống

### 2. Tạo thư mục lưu dữ liệu
```bash
mkdir -p ~/qdrant_local/qdrant_data
cd ~/qdrant_local
```

### 3. Tạo file docker-compose.yml
```yaml
version: "3.9"
services:
  qdrant:
    image: qdrant/qdrant:v1.14.0
    container_name: qdrant_legal_chatbot
    restart: unless-stopped
    ports:
      - "6333:6333"  # REST API & Web UI
      - "6334:6334"  # gRPC
    volumes:
      - ./qdrant_data:/qdrant/storage
    environment:
      QDRANT__SERVICE__API_KEY: "my_super_secret_key"
    networks:
      - qdrant_network

networks:
  qdrant_network:
    name: qdrant_network
    driver: bridge
```

### 4. Khởi động Qdrant
```bash
# Pull image mới nhất
docker compose pull

# Khởi động container
docker compose up -d

# Kiểm tra trạng thái
docker ps | grep qdrant
```

### 5. Kiểm tra kết nối
```bash
# Health check
curl -H "api-key: my_super_secret_key" http://localhost:6333/healthz
# → "ok"

# Truy cập Web UI
# Mở trình duyệt: http://localhost:6333
# Đăng nhập với API key: my_super_secret_key
```

## So sánh Qdrant Local vs Cloud

### Qdrant Cloud
1. **Thông tin kết nối:**
   ```python
   QDRANT_URL = "https://xxxx.cloud.qdrant.io"
   QDRANT_API_KEY = "your_cloud_api_key"
   ```

2. **Ưu điểm:**
   - Không cần quản lý server
   - Tự động backup
   - Monitoring sẵn có
   - Dễ dàng scale
   - UI quản lý trực quan

3. **Nhược điểm:**
   - Có phí sử dụng
   - Phụ thuộc internet
   - Giới hạn tài nguyên

### Qdrant Local (Docker)
1. **Thông tin kết nối:**
   ```python
   QDRANT_HOST = "localhost"
   QDRANT_PORT = 6333
   QDRANT_API_KEY = "my_super_secret_key"
   ```

2. **Ưu điểm:**
   - Miễn phí
   - Hoạt động offline
   - Toàn quyền kiểm soát
   - Không giới hạn tài nguyên
   - Dữ liệu lưu trữ locally

3. **Nhược điểm:**
   - Tự quản lý server
   - Tự backup dữ liệu
   - Tự cấu hình monitoring

## Thao tác CRUD cơ bản

### 1. Kết nối Python Client
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Local
client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="my_super_secret_key"
)

# Cloud
client = QdrantClient(
    url="https://xxxx.cloud.qdrant.io",
    api_key="your_cloud_api_key"
)
```

### 2. Tạo Collection
```python
client.create_collection(
    collection_name="my_collection",
    vectors_config=models.VectorParams(
        size=1536,  # Kích thước vector
        distance=models.Distance.COSINE  # Metric distance
    )
)
```

### 3. Thêm/Upsert Vectors
```python
client.upsert(
    collection_name="my_collection",
    points=models.Batch(
        ids=[1, 2, 3],
        vectors=[[0.1, 0.2, ...], [0.3, 0.4, ...], [0.5, 0.6, ...]],
        payloads=[
            {"text": "doc1", "metadata": {...}},
            {"text": "doc2", "metadata": {...}},
            {"text": "doc3", "metadata": {...}}
        ]
    )
)
```

### 4. Tìm kiếm Vectors
```python
results = client.search(
    collection_name="my_collection",
    query_vector=[0.1, 0.2, ...],
    limit=5,
    score_threshold=0.7
)
```

### 5. Xóa Collection
```python
client.delete_collection("my_collection")
```

## Backup và Restore

### Local Backup
```bash
# Backup
docker exec qdrant_legal_chatbot tar -czf - /qdrant/storage > qdrant_backup.tar.gz

# Restore
docker cp qdrant_backup.tar.gz qdrant_legal_chatbot:/tmp/
docker exec qdrant_legal_chatbot tar -xzf /tmp/qdrant_backup.tar.gz -C /qdrant/
```

### Cloud Backup
- Sử dụng tính năng backup có sẵn trong Web UI
- Hoặc dùng API:
  ```python
  # Export
  collection_info = client.get_collection("my_collection")
  
  # Import
  client.upload_collection("my_collection", "backup_file.json")
  ```

## Monitoring và Logging

### Local Monitoring
```bash
# Xem logs
docker compose logs -f

# Xem metrics
curl -H "api-key: my_super_secret_key" http://localhost:6333/metrics

# Xem thông tin collection
curl -H "api-key: my_super_secret_key" http://localhost:6333/collections/my_collection
```

### Cloud Monitoring
- Sử dụng dashboard có sẵn
- Metrics được tự động thu thập
- Cảnh báo có thể cấu hình

## Troubleshooting

### 1. Container không khởi động
```bash
# Kiểm tra logs
docker compose logs

# Kiểm tra port conflict
netstat -tulpn | grep 6333
```

### 2. Kết nối bị timeout
- Kiểm tra firewall
- Kiểm tra API key
- Kiểm tra network Docker

### 3. Performance issues
- Tăng RAM cho container
- Kiểm tra disk I/O
- Tối ưu vector size và index

### 4. Backup/Restore fails
- Kiểm tra disk space
- Kiểm tra permissions
- Verify backup file integrity

## Lệnh Docker hữu ích

```bash
# Khởi động lại container
docker compose restart

# Dừng container
docker compose down

# Xem resource usage
docker stats qdrant_legal_chatbot

# Vào container
docker exec -it qdrant_legal_chatbot bash

# Xóa dữ liệu (cẩn thận!)
docker compose down -v
```

## Best Practices

1. **Security:**
   - Luôn sử dụng API key
   - Thay đổi API key định kỳ
   - Giới hạn network access

2. **Performance:**
   - Chọn metric distance phù hợp
   - Tối ưu vector size
   - Sử dụng batch operations

3. **Maintenance:**
   - Backup định kỳ
   - Monitor resource usage
   - Update version thường xuyên

4. **Development:**
   - Sử dụng environment variables
   - Implement error handling
   - Test với dữ liệu mẫu

📦 **Xong!** Bạn đã triển khai Qdrant Local bằng Docker, sẵn sàng dùng cho search/vector store.
