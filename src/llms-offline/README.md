# Triển khai Dịch vụ LLMs Offline

## Giới thiệu

Thư mục này chứa mã nguồn và cấu hình để triển khai một dịch vụ cung cấp khả năng sinh văn bản sử dụng mô hình Llama-3.2-3B-Instruct-Frog FP16, chạy offline trong một container Docker.

Dịch vụ được xây dựng bằng FastAPI và sử dụng thư viện `transformers` cùng PyTorch để load và chạy mô hình trên GPU.

## Yêu cầu

- Docker và Docker Compose đã được cài đặt.
- Trình điều khiển (driver) NVIDIA đã được cài đặt trên hệ thống host (nếu chạy trên GPU).
- Đảm bảo GPU của bạn có đủ VRAM (tối thiểu ~6.5GB VRAM cho model FP16).

## Chuẩn bị Model

Mô hình FP16 và tokenizer cần được đặt trong thư mục `./model` trên hệ thống host. Thư mục này sẽ được mount vào container Docker tại `/app/model`.

Cấu trúc thư mục `model` nên như sau:

```
./model/
├── fp16/        # Chứa model Llama-3.2-3B-Instruct-Frog ở định dạng FP16
└── tokenizer/   # Chứa tokenizer của mô hình
```

Nếu bạn cần chuẩn bị model từ bản gốc, bạn có thể tham khảo script `prepare_model_fp16.py` (tuy nhiên, file README này tập trung vào việc triển khai dịch vụ khi đã có sẵn model FP16).

## Build Docker Image

Điều hướng đến thư mục `src/llms-offline` trong terminal và chạy lệnh sau để build image Docker:

```bash
docker compose build
```

Lệnh này sẽ đọc `Dockerfile` và `requirements.txt` để tạo ra image chứa ứng dụng Python và các dependencies cần thiết.

## Chạy Dịch vụ

Sau khi build image thành công, chạy lệnh sau trong cùng thư mục để khởi động dịch vụ bằng Docker Compose:

```bash
docker compose up -d
```

- Lệnh `-d` để chạy container ở chế độ nền.
- Dịch vụ sẽ chạy trên port 8000 bên trong container và được map ra port 8001 trên hệ thống host (như cấu hình trong `docker-compose.yml`).
- Thư mục `./model` và `./logs` trên host sẽ được mount vào container.

## Kiểm tra API và Tham số Mô hình

Dịch vụ cung cấp một endpoint `/v1/generate` để sinh văn bản với các tham số cấu hình quá trình sinh.

Bạn có thể kiểm tra API bằng `curl`. Tham khảo file `API.md` để biết ví dụ cụ thể:

```bash
curl -X POST http://localhost:8001/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Câu hỏi của bạn",
    "max_tokens":128,
    "temperature":0.7,
    "top_p":0.9,
    "do_sample": true
  }'
```

**Các tham số chính:**

-   `prompt` (string, bắt buộc): Đoạn văn bản đầu vào để mô hình tiếp tục sinh.
-   `max_tokens` (integer, tùy chọn, mặc định 128): Số lượng token tối đa mô hình sẽ sinh thêm sau prompt. Giá trị lớn hơn sẽ cho phản hồi dài hơn nhưng tốn nhiều tài nguyên hơn.
-   `temperature` (float, tùy chọn, mặc định 0.7): Kiểm soát tính ngẫu nhiên của đầu ra. Giá trị cao hơn (ví dụ: 1.0) làm cho văn bản ngẫu nhiên và sáng tạo hơn; giá trị thấp hơn (ví dụ: 0.2) làm cho văn bản tập trung và ít ngẫu nhiên hơn.
-   `top_p` (float, tùy chọn, mặc định 0.9): Kiểm soát việc lấy mẫu từ phân phối xác suất của các token tiếp theo. Mô hình chỉ xem xét các token có xác suất tích lũy đến `top_p`. Giá trị thấp hơn làm cho đầu ra an toàn hơn; giá trị cao hơn cho phép đa dạng hơn.
-   `do_sample` (boolean, tùy chọn, mặc định true): Nếu `true`, sử dụng lấy mẫu ngẫu nhiên với `temperature` và `top_p`. Nếu `false`, sử dụng greedy decoding (luôn chọn token có xác suất cao nhất).

Hoặc truy cập http://localhost:8001/docs để xem tài liệu API tự động tạo bởi FastAPI (Swagger UI) với mô tả chi tiết về các tham số.

## Theo dõi Tài nguyên và Phân tích Logs

Dịch vụ tích hợp module `monitoring.py` để ghi log việc sử dụng RAM hệ thống và VRAM GPU tại các thời điểm quan trọng (trước/sau khi load model, trước/sau khi generate). Điều này giúp bạn theo dõi sát sao tài nguyên mà container đang sử dụng.

Logs được lưu trong thư mục `./logs` trên host. Bạn có thể xem logs trực tiếp bằng lệnh Docker:

```bash
docker compose logs -f
```

Lệnh `-f` giúp bạn xem log theo thời gian thực khi chúng xuất hiện.

**Cách đọc log monitoring:**

Các dòng log từ module monitoring sẽ có định dạng:

`YYYY-MM-DD HH:MM:SS | [OPERATION] GPU: Tên_GPU - VRAM: Allocated_GBGB (allocated) / Reserved_GBGB (reserved) | RAM: Used_GBGB/Total_GBGB (Percent%)`

-   `YYYY-MM-DD HH:MM:SS`: Thời gian log được ghi.
-   `[OPERATION]`: Hoạt động đang diễn ra (ví dụ: `[Before model load]`, `[After model load]`, `[Before generation]`, `[After generation]`).
-   `GPU: Tên_GPU`: Tên card đồ họa đang được sử dụng (ví dụ: `NVIDIA GeForce RTX 4060 Laptop GPU`).
-   `VRAM: Allocated_GBGB (allocated)`: Lượng VRAM thực tế đang được các tensor chiếm dụng.
-   `VRAM: Reserved_GBGB (reserved)`: Lượng VRAM mà PyTorch đã cấp phát từ driver GPU.
-   `RAM: Used_GBGB/Total_GBGB (Percent%)`: Lượng RAM (bộ nhớ hệ thống) mà **container Docker** đang sử dụng trên tổng lượng RAM mà container thấy được.

Việc theo dõi các chỉ số này giúp bạn hiểu rõ khi nào mô hình chiếm dụng nhiều bộ nhớ nhất (thường là sau khi load) và lượng tài nguyên cần thiết cho mỗi lượt sinh văn bản. Nếu bạn gặp lỗi Out of Memory (OOM), các log này sẽ là manh mối quan trọng để xác định liệu vấn đề nằm ở RAM hệ thống hay VRAM GPU.

Để theo dõi chi tiết hơn việc sử dụng tài nguyên của container (CPU, RAM, Network, Block I/O), bạn có thể sử dụng lệnh `docker stats`:

```bash
docker stats llms-offline-llm-service-1
```

Lệnh này cung cấp thông tin cập nhật theo thời gian thực về tài nguyên mà container đang tiêu thụ.

## Dừng Dịch vụ

Để dừng dịch vụ và xóa container, chạy lệnh sau trong thư mục `src/llms-offline`:

```bash
docker compose down
```

Lệnh này sẽ dừng và xóa container `llms-offline-llm-service-1`. 



```
2025-05-20 01:09:32.264 | 2025-05-19 18:09:32 | [Before model load] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 0.0GB (allocated) / 0.0GB (reserved) | RAM: 1.89GB/7.63GB (28.5%)
2025-05-20 01:09:33.831 | 2025-05-19 18:09:33 | We will use 90% of the memory on device 0 for storing the model, and 10% for the buffer to avoid OOM. You can set `max_memory` in to a higher value to use more memory (at your own risk).
2025-05-20 01:14:17.323 | 
2025-05-20 01:14:17.351 | 2025-05-19 18:14:17 | [After model load] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.98GB (allocated) / 6.59GB (reserved) | RAM: 1.95GB/7.63GB (30.3%)
2025-05-20 01:14:17.359 | INFO:     Started server process [1]
2025-05-20 01:14:17.359 | INFO:     Waiting for application startup.
2025-05-20 01:14:17.360 | INFO:     Application startup complete.
2025-05-20 01:14:17.360 | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2025-05-20 01:21:47.599 | INFO:     172.18.0.1:43368 - "GET /docs HTTP/1.1" 200 OK
2025-05-20 01:21:47.742 | INFO:     172.18.0.1:43368 - "GET /openapi.json HTTP/1.1" 200 OK
2025-05-20 01:21:56.255 | 2025-05-19 18:21:56 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.98GB (allocated) / 6.59GB (reserved) | RAM: 1.96GB/7.63GB (30.4%)
2025-05-20 01:21:56.264 | /app/app/inference.py:50: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
2025-05-20 01:21:56.264 |   with torch.cuda.amp.autocast():
2025-05-20 01:21:56.264 | `generation_config` default values have been modified to match model-specific defaults: {'bos_token_id': 128000, 'eos_token_id': [128001, 128008, 128009]}. If this is not desired, please set these values explicitly.
2025-05-20 01:22:00.770 | 2025-05-19 18:22:00 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.81GB/7.63GB (41.7%)
2025-05-20 01:22:00.773 | 2025-05-19 18:22:00 | GPU memory cache cleared
2025-05-20 01:22:00.774 | INFO:     172.18.0.1:43352 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:28:35.391 | 2025-05-19 18:28:35 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:28:39.925 | 2025-05-19 18:28:39 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:39.927 | 2025-05-19 18:28:39 | GPU memory cache cleared
2025-05-20 01:28:39.928 | INFO:     172.18.0.1:52484 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:28:47.381 | 2025-05-19 18:28:47 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:51.954 | 2025-05-19 18:28:51 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:51.956 | 2025-05-19 18:28:51 | GPU memory cache cleared
2025-05-20 01:28:51.956 | INFO:     172.18.0.1:43490 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:01.423 | 2025-05-19 18:29:01 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:29:06.224 | 2025-05-19 18:29:06 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:06.226 | 2025-05-19 18:29:06 | GPU memory cache cleared
2025-05-20 01:29:06.227 | INFO:     172.18.0.1:39902 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:22.833 | 2025-05-19 18:29:22 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:27.559 | 2025-05-19 18:29:27 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:29:27.562 | 2025-05-19 18:29:27 | GPU memory cache cleared
2025-05-20 01:29:27.562 | INFO:     172.18.0.1:42740 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:43.758 | 2025-05-19 18:29:43 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:46.869 | 2025-05-19 18:29:46 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.6GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:46.872 | 2025-05-19 18:29:46 | GPU memory cache cleared
2025-05-20 01:29:46.872 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:47.849 | 2025-05-19 18:29:47 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:52.174 | 2025-05-19 18:29:52 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:52.176 | 2025-05-19 18:29:52 | GPU memory cache cleared
2025-05-20 01:29:52.177 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:54.945 | 2025-05-19 18:29:54 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:59.694 | 2025-05-19 18:29:59 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:59.696 | 2025-05-19 18:29:59 | GPU memory cache cleared
2025-05-20 01:29:59.697 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:13.971 | 2025-05-19 18:32:13 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:32:18.678 | 2025-05-19 18:32:18 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:32:18.681 | 2025-05-19 18:32:18 | GPU memory cache cleared
2025-05-20 01:32:18.681 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:19.910 | 2025-05-19 18:32:19 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:32:24.279 | 2025-05-19 18:32:24 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:24.283 | 2025-05-19 18:32:24 | GPU memory cache cleared
2025-05-20 01:32:24.283 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:26.612 | 2025-05-19 18:32:26 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:31.120 | 2025-05-19 18:32:31 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:31.122 | 2025-05-19 18:32:31 | GPU memory cache cleared
2025-05-20 01:32:31.123 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:43:00.801 | Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]
2025-05-20 01:43:00.801 | Loading checkpoint shards:  50%|█████     | 1/2 [03:36<03:36, 216.49s/it]
2025-05-20 01:43:00.801 | Loading checkpoint shards: 100%|██████████| 2/2 [04:43<00:00, 128.54s/it]
2025-05-20 01:43:00.801 | Loading checkpoint shards: 100%|██████████| 2/2 [04:43<00:00, 141.73s/it]
```