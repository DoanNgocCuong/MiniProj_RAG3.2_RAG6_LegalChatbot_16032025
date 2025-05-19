# Hướng dẫn chi tiết triển khai mô hình Embedding với ONNX trong Docker cho môi trường hải đảo offline

Dưới đây là hướng dẫn đầy đủ để đóng gói mô hình embedding `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` sử dụng ONNX trong Docker cho môi trường offline hải đảo.

## Bước 1: Chuẩn bị môi trường phát triển

Đầu tiên, tạo cấu trúc thư mục dự án:

```bash
mkdir -p embedding-offline-project/{app,model,scripts,data}
cd embedding-offline-project
```

## Bước 2: Tạo script tải và chuyển đổi mô hình sang ONNX

Tạo file `scripts/prepare_model.py`:

```python
import os
from sentence_transformers import SentenceTransformer
import torch

# Đường dẫn lưu mô hình
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
MODEL_DIR = "./model"
ONNX_DIR = os.path.join(MODEL_DIR, "onnx")

# Tạo thư mục nếu chưa tồn tại
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(ONNX_DIR, exist_ok=True)

print(f"Đang tải mô hình {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME)

# Lưu mô hình tiêu chuẩn trước (để phòng hờ)
standard_model_path = os.path.join(MODEL_DIR, "standard")
print(f"Lưu mô hình tiêu chuẩn vào {standard_model_path}")
model.save(standard_model_path)

# Chuyển đổi và lưu mô hình ONNX
print(f"Chuyển đổi và lưu mô hình ONNX vào {ONNX_DIR}")
model.save_to_onnx(ONNX_DIR)

# Tạo file test để kiểm tra
test_sentences = [
    "Đây là câu thử nghiệm bằng tiếng Việt.",
    "This is a test sentence in English."
]

# Tạo embeddings với mô hình ONNX để kiểm tra
print("Kiểm tra mô hình ONNX...")
onnx_model = SentenceTransformer(ONNX_DIR)
embeddings = onnx_model.encode(test_sentences)

print(f"Kích thước embedding: {embeddings.shape}")
print("Quá trình chuẩn bị mô hình hoàn tất!")
```

## Bước 3: Tạo ứng dụng FastAPI

Tạo file `app/main.py` chứa API:

```python
import os
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("embedding_api.log")
    ]
)

logger = logging.getLogger("embedding-api")

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Embedding API cho môi trường Offline",
    description="API tạo embeddings từ văn bản sử dụng mô hình sentence-transformers",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Định nghĩa models cho API
class EmbeddingRequest(BaseModel):
    texts: List[str]
    batch_size: Optional[int] = 32

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dimensions: int
    model_name: str
    processing_time_ms: float

# Biến toàn cục cho model
model = None

def get_model():
    """Singleton pattern để tải và lưu mô hình trong bộ nhớ"""
    global model
    if model is None:
        model_path = os.environ.get("MODEL_PATH", "/app/model/onnx")
        logger.info(f"Đang tải mô hình từ {model_path}")
        try:
            model = SentenceTransformer(model_path)
            logger.info("Mô hình đã được tải thành công")
        except Exception as e:
            logger.error(f"Lỗi khi tải mô hình: {str(e)}")
            raise RuntimeError(f"Không thể tải mô hình: {str(e)}")
    return model

@app.get("/")
def health_check():
    """Endpoint kiểm tra trạng thái"""
    return {
        "status": "online", 
        "model": "paraphrase-multilingual-mpnet-base-v2 (ONNX)",
        "version": "1.0.0"
    }

@app.post("/embeddings", response_model=EmbeddingResponse)
def create_embeddings(request: EmbeddingRequest, model: SentenceTransformer = Depends(get_model)):
    """Tạo embeddings từ văn bản đầu vào"""
    try:
        start_time = time.time()
        
        # Kiểm tra đầu vào
        if not request.texts:
            raise HTTPException(status_code=400, detail="Danh sách văn bản không được để trống")
        
        if len(request.texts) > 100:
            logger.warning(f"Số lượng văn bản lớn: {len(request.texts)}")
        
        # Tạo embedding
        embeddings = model.encode(request.texts, batch_size=request.batch_size)
        
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # ms
        
        # Ghi log
        logger.info(f"Đã tạo {len(embeddings)} embeddings trong {processing_time:.2f}ms")
        
        # Chuẩn bị phản hồi
        return {
            "embeddings": embeddings.tolist(),
            "dimensions": embeddings.shape[1],
            "model_name": "paraphrase-multilingual-mpnet-base-v2 (ONNX)",
            "processing_time_ms": processing_time
        }
        
    except Exception as e:
        logger.error(f"Lỗi khi tạo embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo embeddings: {str(e)}")

@app.get("/info")
def model_info(model: SentenceTransformer = Depends(get_model)):
    """Trả về thông tin về mô hình"""
    try:
        info = {
            "model_name": "paraphrase-multilingual-mpnet-base-v2",
            "format": "ONNX",
            "embedding_dimension": model.get_sentence_embedding_dimension(),
            "supports_languages": ["Vietnamese", "English", "Chinese", "Japanese", "Korean", "và hầu hết các ngôn ngữ phổ biến"],
            "max_sequence_length": model.get_max_seq_length(),
            "version": "1.0.0"
        }
        return info
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin mô hình: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy thông tin mô hình: {str(e)}")

@app.post("/similarity")
def compute_similarity(texts: List[str], model: SentenceTransformer = Depends(get_model)):
    """Tính toán độ tương đồng giữa các văn bản"""
    if len(texts) < 2:
        raise HTTPException(status_code=400, detail="Cần ít nhất 2 văn bản để tính độ tương đồng")
    
    try:
        embeddings = model.encode(texts)
        
        # Tính toán độ tương đồng cosine giữa tất cả các cặp
        similarity_matrix = np.zeros((len(texts), len(texts)))
        for i in range(len(texts)):
            for j in range(len(texts)):
                e1 = embeddings[i]
                e2 = embeddings[j]
                similarity = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
                similarity_matrix[i, j] = similarity
                
        return {
            "similarity_matrix": similarity_matrix.tolist(),
            "texts": texts
        }
    except Exception as e:
        logger.error(f"Lỗi khi tính độ tương đồng: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tính độ tương đồng: {str(e)}")
```

## Bước 4: Tạo file cấu hình ứng dụng

Tạo file `app/requirements.txt`:

```
sentence-transformers==2.2.2
fastapi==0.97.0
uvicorn==0.22.0
pydantic==1.10.8
numpy>=1.24.0
torch>=2.0.1
onnxruntime>=1.14.0
onnx>=1.14.0
transformers>=4.30.2
```

## Bước 5: Tạo file Docker

Tạo `Dockerfile`:

```dockerfile
# Base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép requirements trước để tận dụng Docker cache
COPY app/requirements.txt /app/requirements.txt

# Cài đặt các gói Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Sao chép mô hình và mã nguồn
COPY model/ /app/model/
COPY app/ /app/

# Thiết lập biến môi trường
ENV MODEL_PATH=/app/model/onnx

# Mở cổng
EXPOSE 8000

# Tạo thư mục cho logs và quyền ghi
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Thêm user không phải root cho bảo mật tốt hơn
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Khởi động ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Bước 6: Tạo script đóng gói

Tạo file `package.sh`:

```bash
#!/bin/bash
set -e

echo "=== Bắt đầu đóng gói mô hình embedding cho môi trường offline ==="

# Cài đặt thư viện cần thiết
pip install -r app/requirements.txt

# Tải và chuyển đổi mô hình
echo "=== Tải và chuyển đổi mô hình sang định dạng ONNX ==="
python scripts/prepare_model.py

# Kiểm tra mô hình ONNX
echo "=== Kiểm tra mô hình ONNX ==="
if [ -f "model/onnx/model.onnx" ]; then
    echo "Mô hình ONNX đã được tạo thành công!"
else
    echo "Lỗi: Không thể tạo mô hình ONNX!"
    exit 1
fi

# Đóng gói Docker
echo "=== Xây dựng Docker image ==="
docker build -t embedding-offline:latest .

# Lưu Docker image
echo "=== Lưu Docker image thành file ==="
docker save -o embedding-offline-image.tar embedding-offline:latest

# Tạo các script hỗ trợ cho việc triển khai
echo "=== Tạo script hỗ trợ ==="
cat > install_offline.sh << 'EOL'
#!/bin/bash
echo "=== Cài đặt Embedding API Offline ==="
echo "Tải Docker image vào hệ thống..."
docker load -i embedding-offline-image.tar
echo "Đã tải Docker image thành công!"

echo "Khởi động container..."
docker run -d --name embedding-service -p 8000:8000 embedding-offline:latest
echo "Container đã được khởi động tại địa chỉ http://localhost:8000"
echo "Kiểm tra trạng thái API bằng lệnh: curl http://localhost:8000"

echo "=== Cài đặt hoàn tất! ==="
EOL

chmod +x install_offline.sh

# Tạo file hướng dẫn sử dụng
echo "=== Tạo tài liệu hướng dẫn ==="
cat > README.md << 'EOL'
# Embedding API Offline cho môi trường hải đảo

## Giới thiệu
Đây là API tạo embedding sử dụng mô hình sentence-transformers/paraphrase-multilingual-mpnet-base-v2 được tối ưu hóa với ONNX cho môi trường offline.

## Cài đặt
1. Chạy script cài đặt: `./install_offline.sh`

## Sử dụng API
### Tạo embedding
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Đây là một ví dụ văn bản tiếng Việt.", "This is an example text in English."]}'
```

### Tính độ tương đồng giữa các văn bản
```bash
curl -X POST "http://localhost:8000/similarity" \
     -H "Content-Type: application/json" \
     -d '["Câu thứ nhất.", "Câu thứ hai.", "Câu thứ ba."]'
```

### Lấy thông tin mô hình
```bash
curl "http://localhost:8000/info"
```

## Tích hợp với Python
```python
import requests
import json

def get_embedding(texts):
    response = requests.post(
        "http://localhost:8000/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["embeddings"]

# Sử dụng
embeddings = get_embedding(["Câu ví dụ"])
print(embeddings)
```
EOL

# Tạo file Python client đơn giản
cat > embedding_client.py << 'EOL'
import requests
import json
import argparse

def get_embedding(texts, url="http://localhost:8000"):
    """Lấy embedding từ API local"""
    try:
        response = requests.post(
            f"{url}/embeddings",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"texts": texts})
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

def compute_similarity(texts, url="http://localhost:8000"):
    """Tính độ tương đồng giữa các văn bản"""
    try:
        response = requests.post(
            f"{url}/similarity",
            headers={"Content-Type": "application/json"},
            data=json.dumps(texts)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

def get_model_info(url="http://localhost:8000"):
    """Lấy thông tin về mô hình"""
    try:
        response = requests.get(f"{url}/info")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client kết nối đến Embedding API")
    parser.add_argument("--action", choices=["embed", "similarity", "info"], default="embed", 
                        help="Hành động: embed (tạo embedding), similarity (tính độ tương đồng), info (thông tin mô hình)")
    parser.add_argument("--texts", nargs="+", help="Các văn bản đầu vào")
    parser.add_argument("--url", default="http://localhost:8000", help="URL của API")
    
    args = parser.parse_args()
    
    if args.action == "embed" and args.texts:
        result = get_embedding(args.texts, args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "similarity" and args.texts:
        result = compute_similarity(args.texts, args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "info":
        result = get_model_info(args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Thiếu tham số. Hãy chạy với --help để xem hướng dẫn.")
EOL

# Tạo thư mục tài liệu với các ví dụ
mkdir -p docs_examples
cat > docs_examples/example.py << 'EOL'
"""
Ví dụ sử dụng Embedding API trong môi trường Python.
"""
import requests
import json
import numpy as np

# URL API
API_URL = "http://localhost:8000"

def get_embedding(texts):
    """Lấy embedding từ API"""
    response = requests.post(
        f"{API_URL}/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["embeddings"]

def cosine_similarity(v1, v2):
    """Tính độ tương đồng cosine giữa hai vector"""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Ví dụ 1: Tạo embedding cho vài câu
print("Ví dụ 1: Tạo embedding")
sentences = [
    "Hôm nay trời đẹp quá.",
    "Thời tiết hôm nay rất tốt.",
    "Tôi không thích thời tiết hôm nay."
]
embeddings = get_embedding(sentences)

# Ví dụ 2: So sánh độ tương đồng
print("\nVí dụ 2: So sánh độ tương đồng")
similarity_01 = cosine_similarity(embeddings[0], embeddings[1])
similarity_02 = cosine_similarity(embeddings[0], embeddings[2])

print(f"Độ tương đồng giữa câu 1 và câu 2: {similarity_01:.4f}")
print(f"Độ tương đồng giữa câu 1 và câu 3: {similarity_02:.4f}")

# Ví dụ 3: Gọi API tính toán độ tương đồng
print("\nVí dụ 3: API tính độ tương đồng")
response = requests.post(
    f"{API_URL}/similarity",
    headers={"Content-Type": "application/json"},
    data=json.dumps(sentences)
)
similarity_matrix = response.json()["similarity_matrix"]

print("Ma trận độ tương đồng:")
for i, row in enumerate(similarity_matrix):
    for j, value in enumerate(row):
        print(f"[{i+1},{j+1}]: {value:.4f}", end="\t")
    print()
EOL

cat > docs_examples/batch_processing.py << 'EOL'
"""
Ví dụ xử lý embedding hàng loạt cho tập dữ liệu lớn.
"""
import requests
import json
import numpy as np
import time

# URL API
API_URL = "http://localhost:8000"

def batch_embeddings(texts, batch_size=32):
    """Tạo embedding theo batch để xử lý hiệu quả hơn với dữ liệu lớn"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"Đang xử lý batch {i//batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
        
        response = requests.post(
            f"{API_URL}/embeddings",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"texts": batch, "batch_size": batch_size})
        )
        
        batch_embeddings = response.json()["embeddings"]
        all_embeddings.extend(batch_embeddings)
        
    return all_embeddings

# Tạo một tập dữ liệu giả định
print("Tạo dữ liệu mẫu...")
sample_data = [f"Đây là câu văn mẫu thứ {i+1}" for i in range(100)]

# Đo thời gian xử lý
print("Bắt đầu tạo embedding...")
start_time = time.time()
embeddings = batch_embeddings(sample_data, batch_size=32)
end_time = time.time()

print(f"Đã tạo embedding cho {len(sample_data)} câu trong {end_time - start_time:.2f} giây")
print(f"Kích thước output: {np.array(embeddings).shape}")
EOL

# Đóng gói tất cả thành một file
echo "=== Đóng gói tất cả tài nguyên ==="
tar -czf embedding-offline-package.tar.gz \
    embedding-offline-image.tar \
    install_offline.sh \
    README.md \
    embedding_client.py \
    docs_examples

echo "=== Đóng gói hoàn tất! ==="
echo "Tài nguyên đã được đóng gói trong file embedding-offline-package.tar.gz"
echo "Để triển khai tại hải đảo, hãy chuyển file này và thực hiện theo hướng dẫn trong README.md"
```

Thêm quyền thực thi cho script:

```bash
chmod +x package.sh
```

## Bước 7: Chạy script đóng gói và kiểm tra

```bash
./package.sh
```

Script này sẽ:
1. Tải mô hình embedding
2. Chuyển đổi mô hình sang định dạng ONNX
3. Đóng gói mô hình trong Docker image
4. Tạo các script và tài liệu hướng dẫn triển khai
5. Đóng gói tất cả vào một file duy nhất `embedding-offline-package.tar.gz`

## Bước 8: Triển khai tại môi trường hải đảo

1. Chuyển file `embedding-offline-package.tar.gz` đến máy tính tại hải đảo
2. Giải nén:
   ```bash
   tar -xzf embedding-offline-package.tar.gz
   ```
3. Chạy script cài đặt:
   ```bash
   ./install_offline.sh
   ```
4. Kiểm tra API:
   ```bash
   curl http://localhost:8000
   ```

## Bước 9: Sử dụng API

Sau khi cài đặt, bạn có thể sử dụng API bằng cách:

### Với cURL:
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Đây là một ví dụ văn bản tiếng Việt.", "This is an example text in English."]}'
```

### Với Python client:
```bash
python embedding_client.py --action embed --texts "Câu ví dụ thứ nhất" "Câu ví dụ thứ hai"
```

### Thông qua ứng dụng Python:
```python
import requests
import json

def get_embedding(texts):
    response = requests.post(
        "http://localhost:8000/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["embeddings"]

# Sử dụng
embeddings = get_embedding(["Câu ví dụ tiếng Việt", "Example sentence in English"])
print(embeddings)
```

## Lợi ích của giải pháp này

1. **Hoàn toàn offline**: Không cần kết nối internet để hoạt động
2. **Tối ưu hiệu năng**: Sử dụng ONNX runtime tăng tốc xử lý embedding
3. **Dễ dàng triển khai**: Đóng gói Docker giúp triển khai dễ dàng
4. **Đầy đủ tài liệu**: Kèm theo tài liệu hướng dẫn và ví dụ mã nguồn
5. **Tính linh hoạt**: API hỗ trợ nhiều chức năng như tạo embedding và tính độ tương đồng

Với giải pháp này, bạn có thể triển khai mô hình embedding đa ngôn ngữ mạnh mẽ trong môi trường hải đảo offline một cách hiệu quả và ổn định.