# Embedding API Offline cho môi trường hải đảo

## Giới thiệu
Đây là API tạo embedding sử dụng mô hình sentence-transformers/paraphrase-multilingual-mpnet-base-v2 cho môi trường offline. API hỗ trợ đa ngôn ngữ, đặc biệt là tiếng Việt và tiếng Anh.

## Yêu cầu hệ thống
- Python 3.10+
- Docker
- 4GB RAM trở lên (được cấu hình trong docker-compose.yml)
- 2GB ổ cứng trống
- CUDA (tùy chọn, nếu muốn sử dụng GPU)

## Cài đặt và Chạy

### Bước 1: Tạo môi trường ảo
```bash
# Windows
create_venv.bat

# Linux/Mac
./create_venv.sh
```

### Bước 2: Tải model
```bash
# Windows
prepare_model_v2.bat

# Linux/Mac
python scripts/simple_host.py
```
Script này sẽ tải model về thư mục `model/`.

### Bước 3: Chạy API với Docker
```bash
# Windows
run_docker.bat

# Linux/Mac
./run_docker.sh
```
Script sẽ:
- Build Docker image với Python 3.10-slim
- Tạo và chạy container với các cấu hình:
  - Port: 8000
  - Memory limit: 4GB
  - Memory reservation: 2GB
  - Health check mỗi 30s
- API sẽ chạy tại http://localhost:8000

## Sử dụng API

### Kiểm tra trạng thái
```bash
curl http://localhost:8000
```
Response:
```json
{
    "status": "online",
    "model": "paraphrase-multilingual-mpnet-base-v2",
    "version": "1.0.0"
}
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
           "batch_size": 32
         }'
```

### Tính độ tương đồng giữa các văn bản
```bash
curl -X POST "http://localhost:8000/similarity" \
     -H "Content-Type: application/json" \
     -d '[
           "Câu thứ nhất.",
           "Câu thứ hai.",
           "Câu thứ ba."
         ]'
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
        data=json.dumps(texts)
    )
    return response.json()["similarity_matrix"]

# Ví dụ sử dụng
texts = ["Xin chào", "Hello", "Hola"]
embeddings = get_embedding(texts)
similarity = get_similarity(texts)
```

## Cấu trúc thư mục
```
embedding-model-offline/
├── app/
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── model/               # Thư mục chứa model đã tải
├── scripts/
│   └── simple_host.py   # Script tải model
├── logs/               # Thư mục chứa logs
├── Dockerfile         # Cấu hình Docker image
├── docker-compose.yml # Cấu hình Docker services
└── README.md
```

## Xử lý sự cố

### Container không khởi động
```bash
# Kiểm tra logs
docker logs embedding-api

# Kiểm tra trạng thái container
docker ps -a
```

### Lỗi kết nối
- Đảm bảo port 8000 không bị sử dụng
- Kiểm tra firewall có chặn port 8000 không
- Kiểm tra logs trong thư mục `logs/`

### Lỗi model
- Kiểm tra thư mục `model/` đã có model chưa
- Chạy lại script tải model
- Kiểm tra biến môi trường MODEL_PATH và MODEL_NAME

## Giới hạn và Lưu ý
- Batch size mặc định: 32
- Số lượng văn bản tối đa mỗi request: 100
- Kích thước văn bản tối đa: 512 tokens
- API sử dụng FastAPI và Uvicorn
- Logs được lưu trong thư mục `logs/`
- Container tự động restart trừ khi bị dừng thủ công
- Health check được thực hiện mỗi 30 giây

## Dependencies chính
- FastAPI 0.97.0
- Uvicorn 0.22.0
- Sentence-Transformers 4.1.0
- PyTorch 2.1.0
- NumPy 1.24.3
- Transformers 4.51.3

## Thông tin về Model

### Model hiện tại
- Tên model: paraphrase-multilingual-mpnet-base-v2
- Phiên bản: 1.0.0
- Chế độ chạy: CPU only
- Kích thước embedding: 768 chiều
- Ngôn ngữ hỗ trợ: Đa ngôn ngữ (bao gồm tiếng Việt)
- Định dạng: PyTorch native (chưa được tối ưu hóa với Triton)

### Giới hạn hiện tại
- Chưa hỗ trợ GPU acceleration
- Chưa được tối ưu hóa với NVIDIA Triton Inference Server
- Chưa có caching mechanism cho embeddings
- Batch size mặc định là 32, có thể điều chỉnh qua API

## Next Steps

### 1. Tối ưu hóa Model
- [ ] Chuyển đổi model sang định dạng ONNX
- [ ] Tích hợp với NVIDIA Triton Inference Server
- [ ] Thêm caching layer cho embeddings
- [ ] Tối ưu hóa batch processing

### 2. Cải thiện Performance
- [ ] Thêm GPU support
- [ ] Implement async processing
- [ ] Thêm request queuing
- [ ] Tối ưu hóa memory usage

### 3. Monitoring & Logging
- [ ] Thêm Prometheus metrics
- [ ] Tích hợp với ELK stack
- [ ] Thêm performance monitoring
- [ ] Cải thiện error tracking

### 4. Security
- [ ] Thêm authentication
- [ ] Implement rate limiting
- [ ] Thêm request validation
- [ ] Cải thiện error handling

### 5. Documentation
- [ ] Thêm API versioning
- [ ] Cập nhật OpenAPI documentation
- [ ] Thêm performance benchmarks
- [ ] Tạo deployment guide

### 6. Testing
- [ ] Thêm unit tests
- [ ] Thêm integration tests
- [ ] Thêm load testing
- [ ] Thêm performance testing 