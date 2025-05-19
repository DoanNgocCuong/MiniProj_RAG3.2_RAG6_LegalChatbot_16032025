"""
Ví dụ sử dụng Embedding API trong môi trường Python.
"""
import requests
import json
import numpy as np

# URL API
API_URL = "http://localhost:8000"

def get_embedding(texts):
    """Lấy embedding từ API"""
    response = requests.post(
        f"{API_URL}/embeddings",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"texts": texts})
    )
    return response.json()["embeddings"]

def cosine_similarity(v1, v2):
    """Tính độ tương đồng cosine giữa hai vector"""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Ví dụ 1: Tạo embedding cho vài câu
print("Ví dụ 1: Tạo embedding")
sentences = [
    "Hôm nay trời đẹp quá.",
    "Thời tiết hôm nay rất tốt.",
    "Tôi không thích thời tiết hôm nay."
]
embeddings = get_embedding(sentences)

# Ví dụ 2: So sánh độ tương đồng
print("\nVí dụ 2: So sánh độ tương đồng")
similarity_01 = cosine_similarity(embeddings[0], embeddings[1])
similarity_02 = cosine_similarity(embeddings[0], embeddings[2])

print(f"Độ tương đồng giữa câu 1 và câu 2: {similarity_01:.4f}")
print(f"Độ tương đồng giữa câu 1 và câu 3: {similarity_02:.4f}")

# Ví dụ 3: Gọi API tính toán độ tương đồng
print("\nVí dụ 3: API tính độ tương đồng")
response = requests.post(
    f"{API_URL}/similarity",
    headers={"Content-Type": "application/json"},
    data=json.dumps(sentences)
)
similarity_matrix = response.json()["similarity_matrix"]

print("Ma trận độ tương đồng:")
for i, row in enumerate(similarity_matrix):
    for j, value in enumerate(row):
        print(f"[{i+1},{j+1}]: {value:.4f}", end="\t")
    print() 