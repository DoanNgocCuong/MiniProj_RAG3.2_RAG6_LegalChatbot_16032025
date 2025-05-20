# 1. Update cách dùng embedding : from huggingface_hub import InferenceClient và 2 Update thay DB Qdant cloud thành DB local 

Ran tool


File đã được cập nhật theo đúng tài liệu hướng dẫn mới:

1. **Embedding:**  
   - Đã thay thế hoàn toàn `HuggingFaceInferenceAPIEmbeddings` bằng `InferenceClient` từ `huggingface_hub`.
   - Tạo hàm `get_embedding_function` để lấy vector embedding cho từng đoạn văn/bản ghi, trả về numpy array phù hợp cho Qdrant.

2. **Qdrant:**  
   - Vẫn giữ logic ưu tiên DB local (host/port) nếu không có QDRANT_URL, đúng như yêu cầu.

3. **Các phần còn lại** (xử lý dữ liệu, tạo document, push vào Qdrant...) **giữ nguyên**.

---

**Bạn chỉ cần đảm bảo:**
- Đã cài đặt thư viện huggingface_hub (`pip install huggingface_hub`)
- Token Hugging Face phải có quyền inference mới (theo tài liệu)
- Qdrant local đã chạy

Nếu cần hướng dẫn test lại hoặc giải thích chi tiết về hàm embedding mới, hãy cho tôi biết!

---
# 2. oke sao ko dùng embedding trực tiếp của from huggingface_hub import InferenceClient luôn nhỉ, qua langchain làm gì 



Mình đã cập nhật lại file `create_vector_database_QdantLocal.py` như sau:

- **Không còn dùng LangChain** (không import hay sử dụng Document, vectorstore, hay embedding của LangChain nữa).
- **Chỉ dùng trực tiếp**:
  - `huggingface_hub.InferenceClient` để lấy embedding.
  - `qdrant-client` để upsert vector vào Qdrant.
- **Đọc dữ liệu** từ Excel hoặc text, sinh embedding, và upsert trực tiếp vào Qdrant với metadata.
- **Giữ nguyên logic** đọc file, metadata, biến môi trường, và các tham số dòng lệnh.

---

### Cách sử dụng:
```bash
python back-end/backend_vector_database/create_vector_database_QdantLocal.py --excel back-end/backend_vector_database/dataset/LegalRAG.xlsx
```
hoặc
```bash
python back-end/backend_vector_database/create_vector_database_QdantLocal.py --text-dir back-end/backend_vector_database/dataset/texts/
```

---

### Ưu điểm:
- Đơn giản, dễ kiểm soát, không phụ thuộc LangChain.
- Chủ động hoàn toàn về embedding và lưu vector.

Bạn muốn tôi bổ sung gì thêm (ví dụ: kiểm tra collection, log chi tiết, hoặc hướng dẫn test lại)?

---



Bạn chỉ cần truyền tham số `url="http://localhost:6333"` khi khởi tạo `QdrantClient` để đảm bảo luôn kết nối qua HTTP (không bị lỗi SSL như trước).

**Cụ thể:**
```python
qdrant = QdrantClient(url="http://localhost:6333", api_key="my_super_secret_key")
```
- Không dùng `host`/`port` nữa.
- Không dùng `https://` (chỉ dùng `http://`).

**Kết quả:**  
- Sẽ không còn lỗi `[SSL: WRONG_VERSION_NUMBER]`.
- Kết nối luôn đúng tới Qdrant local qua HTTP.

Bạn chỉ cần chạy lại script, mọi thứ sẽ hoạt động ổn định!  
Nếu muốn truyền API key động, chỉ cần thay `"my_super_secret_key"` bằng biến hoặc giá trị bạn mong muốn.

---

# 3. Lỗi: Collection `legal_rag` chưa tồn tại trong Qdrant

## Nguyên nhân

- Qdrant **không tự động tạo collection** khi bạn upsert dữ liệu nếu collection đó chưa tồn tại.
- Bạn cần **tạo collection trước** khi upsert vector vào.

## Cách khắc phục

### 1. Thêm hàm tạo collection vào script

Bạn chỉ cần gọi hàm tạo collection trước khi upsert, ví dụ:

```python
def ensure_collection_exists(collection_name, vector_size=768, distance="Cosine"):
    from qdrant_client.http import models
    qdrant = QdrantClient(url="http://localhost:6333", api_key="my_super_secret_key")
    try:
        qdrant.get_collection(collection_name)
        print(f"Collection '{collection_name}' đã tồn tại.")
    except Exception:
        print(f"Tạo collection mới: {collection_name}")
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,  # Đặt đúng kích thước vector của model bạn dùng
                distance=getattr(models.Distance, distance.upper())
            )
        )
```

- Gọi hàm này trước khi upsert:
  ```python
  ensure_collection_exists(collection_name, vector_size=768)  # hoặc 384, 1024, 1536 tùy model
  ```

### 2. Xác định đúng vector size

- Nếu bạn dùng model `"sentence-transformers/paraphrase-multilingual-mpnet-base-v2"` thì vector size là **768**.
- Nếu dùng model khác, kiểm tra lại kích thước vector.

---

## Tóm lại

- **Lỗi này là do collection chưa tồn tại.**
- Bạn cần tạo collection trước khi upsert.
- Sau khi tạo, upsert sẽ thành công.

Bạn muốn tôi cập nhật code mẫu cho bạn không?
