# VẤN ĐỀ MÔ HÌNH EMBEDDING ĐANG GẶP TRÊN HUGGING FACE

[Previous content remains the same...]

## 5. IMPLEMENTATION MỚI (KHÔNG SỬ DỤNG LANGCHAIN)

### 5.1. Cấu trúc mới

```python
from huggingface_hub import InferenceClient
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Khởi tạo client
client = InferenceClient(
    provider="hf-inference",
    api_key=HUGGINGFACE_API_KEY
)

# Hàm lấy embedding
def get_embedding(text):
    return client.feature_extraction(
        model=EMBEDDINGS_MODEL_NAME,
        text=text
    )
```

### 5.2. Những thay đổi chính

1. **Loại bỏ phụ thuộc vào LangChain**:
   - Không sử dụng `HuggingFaceInferenceAPIEmbeddings`
   - Truy cập trực tiếp Hugging Face API thông qua `InferenceClient`
   - Tương tác trực tiếp với Qdrant thông qua `QdrantClient`

2. **Cải thiện hiệu suất**:
   - Giảm độ trễ do loại bỏ lớp trung gian LangChain
   - Xử lý trực tiếp các vector và metadata
   - Kiểm soát tốt hơn quá trình tạo collection và upsert

3. **Xử lý lỗi tốt hơn**:
   - Kiểm tra và tạo collection tự động
   - Xử lý các trường hợp dữ liệu không đồng nhất
   - Log chi tiết quá trình xử lý

### 5.3. Cấu trúc dữ liệu

1. **Vector Database (Qdrant)**:
   ```python
   {
       "collection_name": "legal_rag",
       "vectors_config": {
           "size": 768,  # Kích thước vector từ model
           "distance": "Cosine"
       }
   }
   ```

2. **Document Structure**:
   ```python
   {
       "id": int,
       "vector": List[float],
       "payload": {
           "source": str,
           "question": str,
           "page_content": str
       }
   }
   ```

### 5.4. Lợi ích của cách triển khai mới

1. **Đơn giản hóa**:
   - Giảm số lượng dependencies
   - Code dễ đọc và bảo trì hơn
   - Ít lớp trừu tượng hơn

2. **Hiệu suất**:
   - Xử lý nhanh hơn do loại bỏ lớp trung gian
   - Kiểm soát tốt hơn việc tạo và quản lý vector
   - Tối ưu hóa việc sử dụng bộ nhớ

3. **Bảo mật**:
   - Kiểm soát tốt hơn việc xác thực API
   - Xử lý an toàn các thông tin nhạy cảm
   - Dễ dàng cập nhật và quản lý API keys

4. **Khả năng mở rộng**:
   - Dễ dàng thêm các tính năng mới
   - Tùy chỉnh quá trình xử lý dữ liệu
   - Tích hợp với các hệ thống khác

### 5.5. Hướng dẫn sử dụng

1. **Cài đặt dependencies**:
   ```bash
   pip install huggingface-hub qdrant-client pandas python-dotenv
   ```

2. **Cấu hình môi trường**:
   ```env
   HUGGINGFACE_API_KEY=your_api_key
   QDRANT_API_KEY=your_qdrant_key
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   EMBEDDINGS_MODEL_NAME=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
   COLLECTION_NAME=legal_rag
   ```

3. **Chạy script**:
   ```bash
   python create_vector_database.py --excel path/to/data.xlsx
   # hoặc
   python create_vector_database.py --text-dir path/to/text/files
   ```
