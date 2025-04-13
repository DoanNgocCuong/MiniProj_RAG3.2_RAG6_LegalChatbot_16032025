# MiniProj_RAG3_RAG6_LegalChatbot_

LỜI ĐẦU: GỬI LỜI CẢM ƠN CHÂN THÀNH ĐÊN CHÍNH CHỦ CỦA UI: https://github.com/phatjkk/nttu-chatbot - anh Phát ikkk

Support Project Graduation for 1 friend.  RAG on Legal Docs in vietnamese - xài LLMs 4omini - Deploy Server - Chạy with no Memory and Add Memory in the Future. --- - Phân vân là : lưu tài liệu nội bộ của nó trên qdant hay milvus (deploy database trên server luôn)  - Cân nhắc để có thể tích hợp mem0 và supabase vào làm memory  Cho cả chatbot và RAG 

# Changelog

## [v1.1] - 2025-03-16 - Từ 17h đến 23h30 = 6h30

### Added
- Integrated OpenWebUI and RAG3NTTU_RAG into a unified system
- Added dark mode support with automatic theme detection
- Created new project variant #1

### Technical
- Git tag: v1.1-16032025
- Command to push tag: `git push origin v1.1-16032025`

![HomePage](note/ver1_HomePage.png)
![UIChat](note/ver1_UIChatPage.png)

Link Demo: https://youtu.be/ZOTE_l9lsNI 

---
## Update: 1.2 - 11/04/2025
- Enhanced authentication flow with Supabase
- Dark mode optimized login/register UI
- Comprehensive logging system
- Environment variables management
  
![Login](note/LOGIN_2.png)


```mermaid
flowchart TD
    A["Dữ liệu đầu vào: File Excel và file văn bản"]
    B["Tiền xử lý dữ liệu: Đọc, tách và chuẩn hóa văn bản"]
    C["Tạo đối tượng Tài liệu (Nội dung & Metadata)"]
    D["Tính toán Embedding (Sentence-Transformers)"]
    E["Lưu trữ Embedding vào Qdrant"]
    F["API Backend (FastAPI)"]
    G["Loại truy vấn?"]
    H["Tìm kiếm chính xác (lọc theo câu hỏi)"]
    I["Tìm kiếm ngữ nghĩa (truy vấn vector trong Qdrant)"]
    J["Độ tin cậy cao?"]
    K["Phản hồi trực tiếp"]
    L["Gộp ngữ cảnh và gọi LLM (OpenAI)"]
    M["Định dạng phản hồi (bao gồm nguồn, metadata)"]
    N["Gửi phản hồi đến Client"]
    O["Giao diện Người dùng (React)"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G -- "Tìm kiếm chính xác" --> H
    G -- "Không tìm thấy chính xác" --> I
    H --> M
    I --> J
    J -- "Có" --> K
    J -- "Không" --> L
    K --> M
    L --> M
    M --> N
    N --> O
```