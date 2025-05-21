# So sánh hai cách lưu Vector Database

## 1. Cấu trúc Metadata khi lưu DB

### Version 1 (create_vector_database.py - dùng LangChain)
```python
documents = [
    Document(
        page_content=answer,
        metadata={
            "source": excel_file_path, 
            "question": question  # Lưu câu hỏi trong metadata.question
        }
    )
]
```

### Version 2 (create_vector_database_QdantLocal.py - không dùng LangChain)
```python
payloads = [
    {
        "source": excel_file_path, 
        "question": q,  # Lưu câu hỏi trực tiếp trong payload
        "page_content": a
    }
]
```

## 2. Sự khác biệt chính

1. **Cách tổ chức metadata:**
   - Version 1: Sử dụng LangChain Document, metadata được tổ chức rõ ràng với `metadata.question`
   - Version 2: Lưu trực tiếp vào payload của Qdrant, không có cấu trúc metadata rõ ràng

2. **Cách lưu trữ:**
   - Version 1: Metadata được lưu trong cấu trúc Document của LangChain
   - Version 2: Metadata được lưu trực tiếp trong payload của Qdrant

3. **Cách truy xuất:**
   - Version 1: `metadata.question` luôn tồn tại và có thể truy xuất
   - Version 2: `metadata.question` không tồn tại, thay vào đó là `payload.question`

## 3. Vấn đề hiện tại

### Nguyên nhân lỗi
- Khi tìm kiếm chính xác trong `rag_backend.py`, code đang tìm kiếm trong `metadata.question`
- Nhưng trong Version 2, câu hỏi được lưu trực tiếp trong payload, không có cấu trúc metadata
- Điều này dẫn đến việc không tìm thấy kết quả khi tìm kiếm chính xác

### Log lỗi
```
CHI TIẾT TÌM KIẾM CHÍNH XÁC:
Câu hỏi cần tìm: '...'
Filter được tạo:
Field: metadata.question
Value cần match: ...
✗ Không tìm thấy kết quả trong DB
```

## 4. Cách khắc phục

### Phương án 1: Sửa lại cấu trúc payload trong Version 2
```python
payloads = [
    {
        "metadata": {  # Thêm cấu trúc metadata
            "question": q,
            "source": excel_file_path
        },
        "page_content": a
    }
]
```

### Phương án 2: Sửa lại logic tìm kiếm trong rag_backend.py
```python
scroll_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="question",  # Tìm trực tiếp trong payload.question
            match=models.MatchValue(value=query)
        )
    ]
)
```

## 5. Khuyến nghị

1. **Ngắn hạn:**
   - Sửa lại cấu trúc payload trong `create_vector_database_QdantLocal.py` để thêm cấu trúc metadata
   - Hoặc sửa lại logic tìm kiếm trong `rag_backend.py` để tìm trong `payload.question`

2. **Dài hạn:**
   - Thống nhất cấu trúc metadata giữa các version
   - Thêm validation để đảm bảo cấu trúc metadata nhất quán
   - Cập nhật documentation để ghi rõ cấu trúc metadata cần tuân thủ

## 6. Các bước thực hiện

1. Backup dữ liệu hiện tại trong Qdrant
2. Chọn một trong hai phương án khắc phục
3. Cập nhật code theo phương án đã chọn
4. Tạo lại vector database với cấu trúc mới
5. Test lại chức năng tìm kiếm chính xác
6. Cập nhật documentation 

## 7. Phân tích MECE về vấn đề tìm kiếm chính xác

### A. Phân tích theo MECE (Mutually Exclusive, Collectively Exhaustive)

1. **Input đầu vào**
   - ✓ Câu hỏi từ user được truyền đúng vào hàm search_exact()
   - ✓ Format câu hỏi giống nhau giữa các version
   - ❓ Có thể có vấn đề về encoding hoặc whitespace

2. **Database (Qdrant)**
   - ❌ Version 1: Dữ liệu được lưu với cấu trúc metadata.question
   - ❌ Version 2: Dữ liệu được lưu trực tiếp trong payload.question
   - ❓ Cần kiểm tra dashboard Qdrant để xác nhận dữ liệu

3. **Cơ chế tìm kiếm**
   - Version 1: Tìm trong metadata.question -> trả về kết quả trực tiếp
   - Version 2: Tìm trong metadata.question (không tồn tại) -> không tìm thấy -> chuyển sang LLM

### B. Vấn đề với LLM Processing

1. **Version 1 (Hoạt động đúng)**
```python
# Flow xử lý
1. Tìm kiếm chính xác trong metadata.question
2. Nếu tìm thấy -> trả về kết quả trực tiếp từ DB
3. Không gọi LLM nếu có kết quả chính xác
```

2. **Version 2 (Có vấn đề)**
```python
# Flow xử lý hiện tại
1. Tìm kiếm trong metadata.question (không tồn tại)
2. Không tìm thấy kết quả -> chuyển sang semantic search
3. Semantic search tìm thấy kết quả -> vẫn gọi LLM
```

### C. Các bước kiểm tra và khắc phục

1. **Kiểm tra Database**
   ```bash
   # 1. Kiểm tra dashboard Qdrant
   - Truy cập http://localhost:6333/dashboard
   - Xác nhận collection legal_rag tồn tại
   - Kiểm tra cấu trúc payload của các điểm dữ liệu
   
   # 2. Kiểm tra format dữ liệu
   - So sánh payload giữa version 1 và 2
   - Xác nhận vị trí lưu trữ câu hỏi
   ```

2. **Kiểm tra cơ chế tìm kiếm**
   ```python
   # Version 1 (create_vector_database.py)
   - Sử dụng LangChain Document
   - Metadata được tổ chức rõ ràng
   - Tìm kiếm chính xác hoạt động tốt
   
   # Version 2 (create_vector_database_QdantLocal.py)
   - Không dùng LangChain
   - Metadata bị flatten trong payload
   - Tìm kiếm chính xác không hoạt động
   ```

3. **Kiểm tra flow xử lý**
   ```python
   # Thêm logging chi tiết
   logger.info("=== FLOW XỬ LÝ ===")
   logger.info("1. Tìm kiếm chính xác")
   logger.info(f"   - Query: {query}")
   logger.info(f"   - Field tìm kiếm: metadata.question")
   logger.info(f"   - Kết quả: {'Tìm thấy' if result else 'Không tìm thấy'}")
   
   if not result:
       logger.info("2. Chuyển sang semantic search")
       logger.info("3. Gọi LLM nếu cần")
   ```

### D. Kết luận và Hướng giải quyết

1. **Nguyên nhân chính**
   - Cấu trúc metadata khác nhau giữa hai version
   - Version 2 không có cấu trúc metadata.question
   - Flow xử lý không đồng nhất giữa các version

2. **Giải pháp đề xuất**
   - Phương án 1: Sửa lại cấu trúc payload trong Version 2
   - Phương án 2: Sửa lại logic tìm kiếm trong rag_backend.py
   - Thêm validation và logging chi tiết

3. **Các bước thực hiện**
   1. Backup dữ liệu hiện tại
   2. Chọn phương án sửa đổi
   3. Cập nhật code
   4. Tạo lại vector database
   5. Test kỹ flow xử lý
   6. Cập nhật documentation

4. **Kiểm tra sau khi sửa**
   - Xác nhận cấu trúc metadata đúng
   - Kiểm tra tìm kiếm chính xác hoạt động
   - Xác nhận không gọi LLM khi có kết quả chính xác
   - Log đầy đủ flow xử lý để debug 



---

Tôi sẽ cập nhật file `create_vector_database_QdantLocal.py` để lưu data với cấu trúc metadata giống hệt version dùng LangChain:



Tôi đã cập nhật file `create_vector_database_QdantLocal.py` với những thay đổi chính sau:

1. **Cấu trúc metadata giống LangChain**:
   ```python
   payloads = [
       {
           "metadata": {  # Cấu trúc metadata giống LangChain
               "source": excel_file_path,
               "question": question
           },
           "page_content": answer  # Tương đương với page_content trong LangChain Document
       }
   ]
   ```

2. **Thêm logging để kiểm tra**:
   ```python
   # Log cấu trúc payload mẫu
   if payloads:
       print("\nCấu trúc payload mẫu:")
       print(f"Metadata: {payloads[0].get('metadata', {})}")
       print(f"Page content: {payloads[0].get('page_content', '')[:100]}...")
   ```

3. **Cập nhật cấu trúc cho cả text files**:
   ```python
   documents.append({
       "metadata": {
           "source": file_path,
           "_id": os.path.basename(file_path)
       },
       "page_content": paragraph
   })
   ```

4. **Thêm docstrings và comments** để giải thích rõ cấu trúc

Bây giờ cấu trúc metadata sẽ giống hệt version dùng LangChain, đảm bảo:
1. Câu hỏi được lưu trong `metadata.question`
2. Nội dung được lưu trong `page_content`
3. Source được lưu trong `metadata.source`

Các bước tiếp theo:
1. Backup dữ liệu hiện tại trong Qdrant
2. Chạy lại script để tạo lại vector database với cấu trúc mới
3. Kiểm tra dashboard Qdrant để xác nhận cấu trúc metadata
4. Test lại chức năng tìm kiếm chính xác

Bạn muốn tôi giúp thực hiện bước nào trước?
