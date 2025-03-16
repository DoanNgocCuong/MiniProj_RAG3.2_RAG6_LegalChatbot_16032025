

```markdown:src/backend_vector_database/Readme_Format_vectorDB.md
# Vector Database Format Documentation

## Input Format

### Excel File Structure
Input là file Excel (.xlsx) có cấu trúc gồm 2 cột chính:
- **Câu hỏi**: Chứa các câu hỏi liên quan đến luật pháp
- **Đáp án**: Chứa các câu trả lời tương ứng với câu hỏi

Ví dụ:
| Câu hỏi | Đáp án |
|---------|--------|
| Trình bày khái niệm, chế độ pháp lý vùng nội thủy... | Luật này quy định về quy tắc giao thông đường bộ... |
| Quy tắc giao thông đường bộ là gì? | Quy tắc giao thông đường bộ bao gồm các quy định về... |

### Text Files
Ngoài ra, hệ thống cũng hỗ trợ xử lý các file văn bản (.txt) chứa nội dung luật pháp. Các file này sẽ được chia thành các đoạn văn (paragraphs) dựa trên dấu xuống dòng kép (`\n\n`).

## Output Format

### Document Structure
Mỗi document trong vector database có cấu trúc:

```json
{
  "page_content": "Nội dung câu trả lời hoặc đoạn văn bản",
  "metadata": {
    "source": "Đường dẫn đến file nguồn (Excel hoặc text)",
    "question": "Câu hỏi tương ứng (chỉ có khi nguồn là Excel)"
  }
}
```

### Ví dụ Output
```
Document 1 content: Luật này quy định về quy tắc giao thông đường bộ...
Document 1 metadata: {'source': 'LegalRAG.xlsx', 'question': 'Trình bày khái niệm, chế độ pháp lý vùng nội thủy...'}
```

## Truy vấn Vector Database

Khi truy vấn vector database, cần lưu ý cấu trúc dữ liệu để truy xuất đúng thông tin:

1. **Truy xuất nội dung**: `document.page_content` hoặc `payload.get('page_content', '')`
2. **Truy xuất metadata**: 
   - Câu hỏi: `document.metadata.get('question', '')` hoặc `payload.get('metadata', {}).get('question', '')`
   - Nguồn: `document.metadata.get('source', '')` hoặc `payload.get('metadata', {}).get('source', '')`

## Lưu ý khi sử dụng Qdrant API

Khi tạo filter để tìm kiếm trong Qdrant, cần sử dụng đúng cấu trúc:

```python
scroll_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="metadata.question",  # Đường dẫn đến trường question trong metadata
            match=models.MatchValue(value=user_message)
        )
    ]
)
```

Hoặc khi truy xuất dữ liệu từ kết quả:

```python
question = match.payload.get('metadata', {}).get('question', '')
content = match.payload.get('page_content', '')
```
```


========
## When successfully

git commit -m "Load Excel Data => Qdant embedding - page_content+metadata:(source, question)

- Viết thêm 1 file test_qdant_connection.py (Cursor)
- Loading data from backend_vector_database/dataset/LegalRAG.xlsx...
Creating 85 document objects with metadata...
Initializing embeddings with model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Creating vector database in Qdrant collection: legal_rag
Successfully added 85 documents to Qdrant"


## View Dataset: 

- Link: https://e5180f0c-01ea-46a0-95c9-208559c12cef.europe-west3-0.gcp.cloud.qdrant.io:6333/dashboard#/collections