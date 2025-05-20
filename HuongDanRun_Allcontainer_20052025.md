# Hướng Dẫn Chạy Tất Cả Container (20/05/2025)

## Yêu Cầu Hệ Thống
- Docker Desktop đã được cài đặt và đang chạy
- Git đã được cài đặt
- PowerShell hoặc Command Prompt

## Các Bước Thực Hiện

### Cách 1: Chạy Trên Windows (PowerShell)
1. Mở PowerShell với quyền Administrator
2. Di chuyển đến thư mục gốc của dự án:
```powershell
cd "D:\1.LUẬN VĂN THẠC SĨ\MiniProj_RAG3.2_RAG6_LegalChatbot_16032025"
```
3. Chạy script trực tiếp:
```linux
chmod +x run.sh
./run.sh
```
Hoặc:
```window
bash run.sh
```


### 4. Kiểm Tra Trạng Thái Các Container
Để kiểm tra xem các container đã chạy thành công chưa, sử dụng lệnh:
```powershell
docker ps
```

## Giải Thích Các Container

Script sẽ khởi động 3 nhóm container theo thứ tự:

1. **Container Chính (src)**
   - Vị trí: `./src`
   - Chứa các service chính của ứng dụng
   - Lệnh: `docker compose up --build -d`

2. **Container LLMs Offline (src/llms-offline)**
   - Vị trí: `./src/llms-offline`
   - Chứa các model ngôn ngữ chạy offline
   - Lệnh: `docker compose up --build -d`

3. **Container Database (DB)**
   - Vị trí: `./DB`
   - Chứa các service cơ sở dữ liệu
   - Lệnh: `docker compose up --build -d`

## Xử Lý Sự Cố

### Nếu Script Không Chạy Được
1. Kiểm tra Docker Desktop đã chạy chưa
2. Kiểm tra quyền thực thi của file run.sh
3. Kiểm tra đường dẫn hiện tại có đúng không

### Nếu Container Không Khởi Động
1. Kiểm tra logs của container:
```powershell
docker logs <container_id>
```
2. Kiểm tra trạng thái container:
```powershell
docker ps -a
```

### Dừng Tất Cả Container
```powershell
docker compose down
```

## Lưu Ý
- Đảm bảo tất cả các port cần thiết không bị conflict
- Kiểm tra tài nguyên hệ thống (RAM, CPU) đủ để chạy các container
- Backup dữ liệu quan trọng trước khi chạy script

## Lưu Ý Đặc Biệt Cho Windows
1. **Quyền Administrator**
   - Luôn chạy PowerShell hoặc Command Prompt với quyền Administrator
   - Đảm bảo Docker Desktop đang chạy với quyền Administrator

2. **Đường Dẫn**
   - Trong PowerShell/CMD: Sử dụng dấu `\` hoặc `/`
   - Trong Git Bash: Sử dụng dấu `/`
   - Nếu đường dẫn có dấu cách, luôn đặt trong dấu ngoặc kép `"`

3. **WSL2 (Windows Subsystem for Linux)**
   - Nếu gặp vấn đề với Docker, hãy đảm bảo WSL2 đã được cài đặt và cập nhật
   - Kiểm tra WSL2 version: `wsl --version`
   - Cập nhật WSL2: `wsl --update`

4. **Tắt Antivirus Tạm Thời**
   - Một số phần mềm antivirus có thể chặn Docker
   - Tạm thời tắt antivirus nếu gặp vấn đề về quyền truy cập

5. **Kiểm Tra Docker Service**
   - Mở Services (services.msc)
   - Tìm "Docker Desktop Service"
   - Đảm bảo service đang chạy và được set là "Automatic"
