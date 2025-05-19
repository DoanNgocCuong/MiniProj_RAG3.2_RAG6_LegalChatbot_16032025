# Embedding API Offline cho môi trường hải đảo

## Giới thiệu
Đây là API tạo embedding sử dụng mô hình sentence-transformers/paraphrase-multilingual-mpnet-base-v2 được tối ưu hóa với ONNX cho môi trường offline.

## Cài đặt
1. Chạy script cài đặt: `./install_offline.sh`

## Sử dụng API
### Tạo embedding
```bash
curl -X POST "http://localhost:8000/embeddings" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Đây là một ví dụ văn bản tiếng Việt.", "This is an example text in English."]}'
```

### Tính độ tương đồng giữa các văn bản
```bash
curl -X POST "http://localhost:8000/similarity" \
     -H "Content-Type: application/json" \
     -d '["Câu thứ nhất.", "Câu thứ hai.", "Câu thứ ba."]'
```

### Lấy thông tin mô hình
```bash
curl "http://localhost:8000/info"
```

## Tích hợp với Python
```python
import requests
import json

def get_embedding(texts):
    response = requests.post(
        "http://localhost:8000/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["embeddings"]

# Sử dụng
embeddings = get_embedding(["Câu ví dụ"])
print(embeddings)
``` 