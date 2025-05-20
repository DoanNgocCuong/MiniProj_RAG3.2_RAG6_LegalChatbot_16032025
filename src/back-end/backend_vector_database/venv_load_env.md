# ... existing code ...
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
# ... existing code ...

def upsert_to_qdrant(vectors, payloads, collection_name, ids=None):
    # Luôn kết nối Qdrant local
    qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)
    print(f"==> ĐANG KẾT NỐI QDRANT LOCAL: {QDRANT_HOST}:{QDRANT_PORT}")
    if ids is None:
        ids = list(range(1, len(vectors)+1))
    qdrant.upsert(
        collection_name=collection_name,
        points=models.Batch(
            ids=ids,
            vectors=vectors,
            payloads=payloads
        )
    )
    print(f"Đã upsert {len(vectors)} vectors vào collection '{collection_name}'")
# ... existing code ...