```mermaid
flowchart TD
    A["Input Data: Excel and Text Files"]
    B["Preprocess Data: Read, Split, Normalize"]
    C["Create Document Objects (Content & Metadata)"]
    D["Compute Embeddings (Sentence-Transformers)"]
    E["Store Embeddings in Qdrant"]
    F["API Backend (FastAPI)"]
    G["Query Type?"]
    H["Exact Match Search (Filter by Question)"]
    I["Semantic Search (Vector Query in Qdrant)"]
    J["High Confidence?"]
    K["Direct Response"]
    L["Aggregate Context and Call LLM (OpenAI)"]
    M["Format Response (Include Source Info)"]
    N["Send Response to Client"]
    O["Frontend (React)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G -- "Exact Match" --> H
    G -- "No Exact Match" --> I
    H --> M
    I --> J
    J -- "Yes" --> K
    J -- "No" --> L
    K --> M
    L --> M
    M --> N
    N --> O
```

---

# Update
Dưới đây là sơ đồ pipeline bằng Mermaid (đã chuyển hoàn toàn sang tiếng Việt) với điều kiện so sánh độ trùng khớp:

- Nếu tỷ lệ trùng khớp từ tìm kiếm chính xác ≥ 80% thì trả về ngay câu trả lời chuẩn (đã được chuẩn bị sẵn) kèm theo thông tin nguồn và metadata.
- Nếu tỷ lệ trùng khớp < 80% thì chuyển sang sử dụng tìm kiếm ngữ nghĩa: chọn Top K kết quả, gộp ngữ cảnh và gọi LLM (OpenAI) để sinh ra phản hồi, sau đó định dạng và gửi về phía client.

Dưới đây là mã sơ đồ:

```mermaid
flowchart TD
    A["Dữ liệu đầu vào: File Excel và file văn bản"]
    B["Tiền xử lý dữ liệu: Đọc, tách và chuẩn hóa văn bản"]
    C["Tạo đối tượng Tài liệu (Nội dung & Metadata)"]
    D["Tính toán Embedding (Sentence-Transformers)"]
    E["Lưu trữ Embedding vào Qdrant"]
    F["API Backend (FastAPI)"]
    G["Xác định loại truy vấn"]
    H["Tìm kiếm chính xác (lọc theo câu hỏi)"]
    I["Độ trùng khớp ≥ 80%?"]
    J["Trả về phản hồi trực tiếp (Câu trả lời chuẩn)"]
    K["Tìm kiếm ngữ nghĩa (truy vấn vector trong Qdrant)"]
    L["Chọn Top K kết quả"]
    M["Gộp ngữ cảnh và gọi LLM (OpenAI)"]
    N["Định dạng phản hồi: Câu trả lời, nguồn & metadata"]
    O["Gửi phản hồi đến Client"]
    P["Giao diện Người dùng (React)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G -- "Truy vấn chính xác" --> H
    H --> I
    I -- "Có (≥ 80%)" --> J
    I -- "Không (< 80%)" --> K
    K --> L
    L --> M
    J --> N
    M --> N
    N --> O
    O --> P
```

### Giải thích sơ đồ:
1. **Dữ liệu đầu vào:**  
   - Hệ thống nhận dữ liệu từ file Excel chứa cặp câu hỏi – đáp án và các file văn bản khác.

2. **Tiền xử lý dữ liệu:**  
   - Đọc dữ liệu, tách các đoạn văn bản theo tiêu chí định sẵn và chuẩn hóa dữ liệu.

3. **Tạo đối tượng Tài liệu:**  
   - Mỗi đoạn văn bản được chuyển thành một đối tượng tài liệu với các trường: nội dung (page_content) và metadata (nguồn, câu hỏi, …).

4. **Tính toán Embedding:**  
   - Sử dụng mô hình chuyển đổi ngôn ngữ (sentence-transformers) để chuyển nội dung thành vector embedding thể hiện ý nghĩa ngữ cảnh.

5. **Lưu trữ Embedding vào Qdrant:**  
   - Các vector embedding được lưu trữ trong Qdrant để phục vụ truy vấn sau này.

6. **API Backend (FastAPI):**  
   - Hệ thống backend nhận yêu cầu từ phía người dùng và xác định loại truy vấn.

7. **Xác định loại truy vấn:**  
   - Hệ thống thực hiện tìm kiếm chính xác dựa trên bộ lọc theo câu hỏi.

8. **So sánh độ trùng khớp:**  
   - Nếu tỷ lệ trùng khớp từ tìm kiếm chính xác đạt ≥ 80% thì hệ thống sẽ trả về ngay câu trả lời chuẩn đã được chuẩn bị sẵn (kèm theo thông tin nguồn và metadata).

9. **Tìm kiếm ngữ nghĩa:**  
   - Nếu không đạt tỷ lệ trùng khớp ≥ 80%, hệ thống sẽ thực hiện tìm kiếm ngữ nghĩa bằng cách tạo embedding cho câu hỏi và so sánh với các vector trong Qdrant, sau đó chọn ra Top K kết quả.

10. **Gộp ngữ cảnh và gọi LLM:**  
    - Các kết quả Top K được gộp thành một context chung và được gửi kèm với câu truy vấn tới LLM (ví dụ: OpenAI) để sinh ra câu trả lời tự động.

11. **Định dạng phản hồi:**  
    - Câu trả lời cuối cùng được định dạng lại bao gồm cả thông tin nguồn và metadata nếu cần.

12. **Gửi phản hồi đến Client:**  
    - Phản hồi được gửi về cho client để hiển thị qua giao diện người dùng (React).

Sơ đồ này giúp minh họa toàn bộ quy trình xử lý trong hệ thống từ lúc nhận dữ liệu cho đến khi trả về câu trả lời hoàn chỉnh cho người dùng.

---

# Sửa tay 

```mermaid
flowchart TD
    A["Dữ liệu đầu vào
    (Excel Q&A & Văn bản Luật biển)"]
    B["Tiền xử lý & Tính Embedding
    (Chunking, tạo nội dung (content), Metadata(Nguồn, câu hỏi))"]
    C["Tính toán Embedding của nội dung và Lưu trữ vào Qdrant 
    (Lưu trữ: Vector Embedding, Content & Metadata)"]
    D["API Backend (FastAPI)
    (Nhận yêu cầu truy vấn từ User và Phản hồi)"]
    E["Kiểm tra truy vấn
    (So sánh câu hỏi của User với câu hỏi trong Metadata. Kiểm tra độ trùng ≥ 80%)"]
    F["Nếu trùng ≥ 80%
    => Phản hồi chuẩn nội dung có sẵn"]
    G["Nếu không đạt (< 80%)
    => Truy vấn ngữ nghĩa, chọn Top K nội dung gần với câu hỏi của user nhất, để tạo thành Ngữ cảnh (Context) 
    => Gộp câu truy vấn của user với Context, sau đó gọi LLM (OpenAI)"]
    H["Định dạng phản hồi (Câu trả lời, nguồn tài liệu, Metadata)"]
    I["Gửi phản hồi đến Client
    (Hiển thị trên giao diện React)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E -- "Trùng ≥ 80%" --> F
    E -- "< 80%" --> G
    F --> H
    G --> H
    H --> I

```