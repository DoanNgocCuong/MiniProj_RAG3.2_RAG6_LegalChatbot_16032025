# Embedding API Documentation

## Tổng quan
API này cung cấp các endpoint để tạo embeddings từ văn bản sử dụng mô hình sentence-transformers. API được thiết kế để chạy trong môi trường offline.

## Endpoints

### 1. Health Check
```
GET /
```
Kiểm tra trạng thái hoạt động của API.

### 2. Tạo Embeddings
```
POST /embeddings
```
Tạo embeddings từ danh sách văn bản đầu vào.

#### Request Body
```json
{
  "texts": [
    "văn bản 1",
    "văn bản 2",
    ...
  ],
  "batch_size": 32
}
```

#### Response
```json
{
  "embeddings": [
    [0.1, 0.2, ...], // embedding của văn bản 1
    [0.3, 0.4, ...]  // embedding của văn bản 2
  ],
  "dimensions": 768,
  "model_name": "paraphrase-multilingual-mpnet-base-v2",
  "processing_time_ms": 31.89
}
```

### 3. Thông tin Model
```
GET /info
```
Lấy thông tin về model đang sử dụng.

### 4. Tính toán độ tương đồng
```
POST /similarity
```
Tính toán ma trận độ tương đồng giữa các văn bản.

#### Request Body
```json
[
  "văn bản 1",
  "văn bản 2",
  ...
]
```

#### Response
```json
{
  "similarity_matrix": [
    [1.0, 0.38],
    [0.38, 1.0]
  ],
  "texts": [
    "văn bản 1",
    "văn bản 2"
  ]
}
```

## Thông số kỹ thuật

- Model: paraphrase-multilingual-mpnet-base-v2
- Kích thước embedding: 768 chiều
- Ngôn ngữ hỗ trợ: Đa ngôn ngữ (bao gồm tiếng Việt)
- Batch size mặc định: 32

## Lưu ý

- API yêu cầu request body phải ở định dạng JSON
- Độ tương đồng được tính toán dựa trên cosine similarity
- Thời gian xử lý được tính bằng milliseconds 