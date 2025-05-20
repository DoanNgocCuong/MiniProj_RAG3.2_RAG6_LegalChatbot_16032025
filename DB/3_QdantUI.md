Bạn đang truy cập `http://localhost:6333` và chỉ thấy JSON như sau:

```json
{"title":"qdrant - vector search engine","version":"1.14.0","commit":"..."}
```

**Đây là hoàn toàn bình thường!**  
Qdrant **không có giao diện Web UI mặc định** ở cổng 6333, mà chỉ trả về thông tin phiên bản qua endpoint gốc (`/`). Giao diện Web UI của Qdrant chỉ xuất hiện khi bạn truy cập đúng endpoint và có API key hợp lệ.

---

## Cách truy cập Web UI Qdrant

1. **Truy cập đúng endpoint:**  
   - Địa chỉ Web UI:  
     ```
     http://localhost:6333/dashboard
     ```
   - Hoặc:  
     ```
     http://localhost:6333/static
     ```
   - Nếu vẫn không thấy giao diện, Qdrant bản mới đã **loại bỏ Web UI tích hợp**. Bạn chỉ có thể thao tác qua API hoặc dùng Qdrant Cloud (có Web UI).

2. **Nếu muốn giao diện quản lý:**  
   - **Qdrant Cloud**: Đăng ký tài khoản tại [https://cloud.qdrant.io](https://cloud.qdrant.io) để có Web UI quản lý.
   - **Local**: Hiện tại Qdrant bản mới chỉ hỗ trợ API, không còn Web UI local như trước.

---

## Kết luận

- Việc bạn thấy JSON như trên là **đúng chuẩn** khi Qdrant chạy local.
- Bạn vẫn có thể thao tác CRUD, import/export, search... qua API hoặc Python client.
- Nếu cần Web UI, hãy dùng Qdrant Cloud.

---

### Tham khảo tài liệu chính thức:
- [Qdrant API Docs](https://qdrant.tech/documentation/)
- [Qdrant Cloud](https://cloud.qdrant.io)

Bạn có muốn hướng dẫn thao tác với Qdrant qua Python hoặc Postman không? Hoặc cần giải pháp thay thế cho Web UI local?
