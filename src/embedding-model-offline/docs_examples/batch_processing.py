"""
Ví dụ xử lý embedding hàng loạt cho tập dữ liệu lớn.
"""
import requests
import json
import numpy as np
import time

# URL API
API_URL = "http://localhost:8000"

def batch_embeddings(texts, batch_size=32):
    """Tạo embedding theo batch để xử lý hiệu quả hơn với dữ liệu lớn"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"Đang xử lý batch {i//batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
        
        response = requests.post(
            f"{API_URL}/embeddings",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"texts": batch, "batch_size": batch_size})
        )
        
        batch_embeddings = response.json()["embeddings"]
        all_embeddings.extend(batch_embeddings)
        
    return all_embeddings

# Tạo một tập dữ liệu giả định
print("Tạo dữ liệu mẫu...")
sample_data = [f"Đây là câu văn mẫu thứ {i+1}" for i in range(100)]

# Đo thời gian xử lý
print("Bắt đầu tạo embedding...")
start_time = time.time()
embeddings = batch_embeddings(sample_data, batch_size=32)
end_time = time.time()

print(f"Đã tạo embedding cho {len(sample_data)} câu trong {end_time - start_time:.2f} giây")
print(f"Kích thước output: {np.array(embeddings).shape}") 