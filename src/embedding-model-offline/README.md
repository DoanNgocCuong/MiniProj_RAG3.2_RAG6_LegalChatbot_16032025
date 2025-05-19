# Embedding API Offline cho môi trường hải đảo

## Giới thiệu
Đây là API tạo embedding sử dụng mô hình sentence-transformers/paraphrase-multilingual-mpnet-base-v2 cho môi trường offline. API hỗ trợ đa ngôn ngữ, đặc biệt là tiếng Việt và tiếng Anh.

## Yêu cầu hệ thống
- Python 3.9+
- Docker
- 4GB RAM trở lên
- 2GB ổ cứng trống

## Cài đặt và Chạy

### Bước 1: Tải model
```bash
python scripts/simple_host.py
```
Script này sẽ tải model về thư mục `model/`.

### Bước 2: Chạy API với Docker
```bash
run_docker.bat
```
Script sẽ:
- Build Docker image
- Tạo và chạy container
- API sẽ chạy tại http://localhost:8000

## Sử dụng API

### Kiểm tra trạng thái
```bash
curl http://localhost:8000
```

### Tạo embedding
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -d '{
           "texts": [
             "Đây là một ví dụ văn bản tiếng Việt.",
             "This is an example text in English."
           ],
           "batch_size": 2
         }'
```

### Tính độ tương đồng giữa các văn bản
```bash
curl -X POST "http://localhost:8000/similarity" \
     -H "Content-Type: application/json" \
     -d '{
           "texts": [
             "Câu thứ nhất.",
             "Câu thứ hai.",
             "Câu thứ ba."
           ]
         }'
```

### Lấy thông tin mô hình
```bash
curl "http://localhost:8000/info"
```

## Tích hợp với Python
```python
import requests
import json

def get_embedding(texts, batch_size=32):
    response = requests.post(
        "http://localhost:8000/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "texts": texts,
            "batch_size": batch_size
        })
    )
    return response.json()["embeddings"]

def get_similarity(texts):
    response = requests.post(
        "http://localhost:8000/similarity",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["similarity_matrix"]

# Ví dụ sử dụng
texts = ["Xin chào", "Hello", "Hola"]
embeddings = get_embedding(texts)
similarity = get_similarity(texts)
```

## API Documentation
Truy cập http://localhost:8000/docs để xem tài liệu API đầy đủ với Swagger UI.

## Xử lý sự cố

### Container không khởi động
```bash
# Kiểm tra logs
docker logs embedding-service

# Kiểm tra trạng thái container
docker ps -a
```

### Lỗi kết nối
- Đảm bảo port 8000 không bị sử dụng
- Kiểm tra firewall có chặn port 8000 không

### Lỗi model
- Kiểm tra thư mục `model/` đã có model chưa
- Chạy lại `simple_host.py` để tải model

## Giới hạn
- Batch size mặc định: 32
- Số lượng văn bản tối đa mỗi request: 100
- Kích thước văn bản tối đa: 512 tokens 