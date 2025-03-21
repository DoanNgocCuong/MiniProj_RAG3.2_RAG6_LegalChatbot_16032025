
# Phân tích Cơ chế Chuyển đổi Port giữa Development và Production

## 1. THẮC MẮC/VẤN ĐỀ
Tại sao ứng dụng có thể hoạt động mượt mà ở cả hai môi trường mà không cần sửa code:

**Production:**
- Backend: 103.253.20.13:30000
- Frontend: 103.253.20.13:30001
- Sử dụng Docker Compose và Nginx

**Development:**
- Cả Frontend và Backend: localhost:30002
- Chạy bằng lệnh: `npm run dev -- --port 30002`

## 2. NGUYÊN NHÂN/CÁCH XỬ LÝ GỐC RỄ

### 2.1. Môi trường Development
**Vite Dev Server đóng vai trò Proxy Server:**
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://103.253.20.13:30000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```
- Khi frontend gọi `/api/*`, Vite tự động proxy request đến backend
- Không cần cấu hình CORS phức tạp
- Dev server xử lý mọi request trên cùng một port

### 2.2. Môi trường Production
**Nginx đóng vai trò Reverse Proxy:**
```nginx
# nginx.conf
server {
    listen 30001;
    
    # Serve frontend static files
    location / {
        root /usr/share/nginx/html;
    }
    
    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://chatbot-rag-backend:30000/;
    }
}
```
- Nginx phục vụ frontend static files
- Tự động chuyển tiếp các request `/api/*` đến backend container
- Xử lý CORS và các vấn đề bảo mật

### 2.3. Cơ chế Hoạt động
1. **Frontend Code:**
   - Luôn sử dụng đường dẫn tương đối `/api/*`
   - Không cần biết backend thực sự ở đâu

2. **Request Flow:**
   - Development: Browser → Vite Dev Server → Backend
   - Production: Browser → Nginx → Backend

## 3. BÀI HỌC

### 3.1. Thiết kế Kiến trúc
- Sử dụng đường dẫn tương đối trong code
- Tách biệt logic ứng dụng khỏi cấu hình môi trường
- Để proxy server (Vite/Nginx) xử lý routing và CORS

### 3.2. DevOps Best Practices
- Development environment đơn giản hóa để phát triển
- Production environment tối ưu cho hiệu suất và bảo mật
- Sử dụng công cụ phù hợp cho từng môi trường (Vite Dev Server vs Nginx)

### 3.3. Maintainability
- Code không phụ thuộc vào môi trường
- Dễ dàng chuyển đổi giữa các môi trường
- Cấu hình tập trung trong các file riêng biệt (vite.config.js, nginx.conf)

