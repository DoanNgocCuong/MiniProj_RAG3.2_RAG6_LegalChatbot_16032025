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

