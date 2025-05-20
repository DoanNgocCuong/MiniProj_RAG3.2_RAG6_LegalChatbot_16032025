from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()

class QdrantDB:
    def __init__(self):
        self.api_key = os.getenv("QDRANT_API_KEY", "my_super_secret_key")
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.client = self._create_client()

    def _create_client(self):
        """Tạo kết nối đến Qdrant server"""
        return QdrantClient(
            host=self.host,
            port=self.port,
            api_key=self.api_key
        )

    def create_collection(self, collection_name: str, vector_size: int = 1536):
        """Tạo collection mới trong Qdrant"""
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' đã được tạo thành công")
            return True
        except Exception as e:
            print(f"Lỗi khi tạo collection: {str(e)}")
            return False

    def upsert_vectors(self, collection_name: str, vectors, payloads=None, ids=None):
        """Thêm hoặc cập nhật vectors vào collection"""
        try:
            self.client.upsert(
                collection_name=collection_name,
                points=models.Batch(
                    ids=ids or list(range(len(vectors))),
                    vectors=vectors,
                    payloads=payloads or [{}] * len(vectors)
                )
            )
            print(f"Đã upsert {len(vectors)} vectors vào collection '{collection_name}'")
            return True
        except Exception as e:
            print(f"Lỗi khi upsert vectors: {str(e)}")
            return False

    def search_vectors(self, collection_name: str, query_vector, limit: int = 5):
        """Tìm kiếm vectors tương tự"""
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Lỗi khi tìm kiếm vectors: {str(e)}")
            return None

    def delete_collection(self, collection_name: str):
        """Xóa collection"""
        try:
            self.client.delete_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' đã được xóa")
            return True
        except Exception as e:
            print(f"Lỗi khi xóa collection: {str(e)}")
            return False

# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo kết nối
    qdrant_db = QdrantDB()
    
    # Tạo collection mới
    collection_name = "test_collection"
    qdrant_db.create_collection(collection_name)
    
    # Thêm vectors mẫu
    test_vectors = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    test_payloads = [{"text": "sample 1"}, {"text": "sample 2"}]
    qdrant_db.upsert_vectors(collection_name, test_vectors, test_payloads)
    
    # Tìm kiếm vectors
    query_vector = [0.1, 0.2, 0.3]
    results = qdrant_db.search_vectors(collection_name, query_vector)
    print("Kết quả tìm kiếm:", results) 