Cùng 1 đoạn code: 

```bash

#!/usr/bin/env python3
"""
Script này dùng để test hàm lấy embedding từ huggingface_hub.
"""

import os
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient

# Load biến môi trường từ file .env
load_dotenv()
print("Đang load .env từ:", find_dotenv())

# Lấy các biến môi trường
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Khởi tạo InferenceClient
try:
    client = InferenceClient(provider="hf-inference", api_key=HUGGINGFACE_API_KEY)
except Exception as e:
    print(f"Lỗi khi khởi tạo InferenceClient: {e}")
    print("Vui lòng đảm bảo HUGGINGFACE_API_KEY đã được thiết lập chính xác trong file .env")
    exit()

def get_embedding(text):
    """
    Hàm lấy embedding cho một đoạn văn bản sử dụng Hugging Face Inference API.
    """
    if not text:
        return []
    try:
        # feature_extraction trả về list các float, có thể là np.array hoặc list thuần túy
        embedding = client.feature_extraction(model=EMBEDDINGS_MODEL_NAME, text=text)
        return embedding
    except Exception as e:
        print(f"Lỗi khi lấy embedding cho văn bản '{text[:50]}...': {e}")
        return None

def test_embedding_function():
    """
    Chạy các test case để kiểm tra hàm get_embedding.
    """
    print(f"\n--- Bắt đầu kiểm tra hàm get_embedding với model: {EMBEDDINGS_MODEL_NAME} ---")

    # Test case 1: Văn bản tiếng Việt cơ bản
    text_vi = "Đây là một câu văn bản tiếng Việt để kiểm tra embedding."
    print(f"\nTest case 1: Văn bản tiếng Việt")
    embedding_vi = get_embedding(text_vi)
    if embedding_vi is not None:
        print(f"Văn bản: '{text_vi}'")
        print(f"Kích thước embedding: {len(embedding_vi)}")
        print(f"5 giá trị đầu tiên của embedding: {embedding_vi[:5]}")
    else:
        print("Không thể lấy embedding cho văn bản tiếng Việt.")

    # Test case 2: Văn bản tiếng Anh cơ bản
    text_en = "This is a simple English text to test the embedding function."
    print(f"\nTest case 2: Văn bản tiếng Anh")
    embedding_en = get_embedding(text_en)
    if embedding_en is not None:
        print(f"Văn bản: '{text_en}'")
        print(f"Kích thước embedding: {len(embedding_en)}")
        print(f"5 giá trị đầu tiên của embedding: {embedding_en[:5]}")
    else:
        print("Không thể lấy embedding cho văn bản tiếng Anh.")

    # Test case 3: Văn bản rỗng
    text_empty = ""
    print(f"\nTest case 3: Văn bản rỗng")
    embedding_empty = get_embedding(text_empty)
    if not embedding_empty:
        print("Trả về rỗng cho văn bản rỗng (Đúng).")
    else:
        print(f"Văn bản rỗng trả về embedding có kích thước: {len(embedding_empty)} (Sai)")

    # Test case 4: Văn bản dài hơn
    text_long = "Nghị định 23/2024/NĐ-CP của Chính phủ quy định chi tiết một số điều của Luật Đấu thầu về lựa chọn nhà thầu, có hiệu lực từ ngày 15 tháng 5 năm 2024. Nghị định này bao gồm các quy định về hồ sơ mời thầu, tiêu chuẩn đánh giá hồ sơ dự thầu, và các thủ tục liên quan đến quá trình đấu thầu. Việc ban hành nghị định này nhằm mục đích tăng cường tính minh bạch, hiệu quả và công bằng trong hoạt động đấu thầu, góp phần thúc đẩy sự phát triển kinh tế-xã hội của đất nước."
    print(f"\nTest case 4: Văn bản dài hơn (tiếng Việt)")
    embedding_long = get_embedding(text_long)
    if embedding_long is not None:
        print(f"Văn bản: '{text_long[:100]}...'")
        print(f"Kích thước embedding: {len(embedding_long)}")
        print(f"5 giá trị đầu tiên của embedding: {embedding_long[:5]}")
    else:
        print("Không thể lấy embedding cho văn bản dài hơn.")

    print("\n--- Kết thúc kiểm tra ---")

if __name__ == "__main__":
    # Yêu cầu người dùng nhập API Key nếu chưa có
    if HUGGINGFACE_API_KEY is None:
        print("\nCảnh báo: Biến môi trường HUGGINGFACE_API_KEY chưa được thiết lập.")
        print("Vui lòng thêm dòng sau vào file .env của bạn:")
        print("HUGGINGFACE_API_KEY='hf_YOUR_ACTUAL_HUGGINGFACE_API_KEY'")
        print("Bạn có thể lấy API Key từ https://huggingface.co/settings/tokens")
    else:
        test_embedding_function()

```

---

Ở chỗ RAG3 chạy được, mà qua đây ko chạy được -> test mất tầm 1h ở nhà, nào là AI code extract embedding từ những code đã chạy được ,.... + nào là tìm search ở trên các trang web và AI search để xem liệu có thay đổi gì mà mình ko check ko?? + 1h ở chỗ dạy :3 ....

Sau cùng có 2 yếu tố ảnh  ơươnởng êếncêcệc code chạy: 
1. Là code 
2. Môi trường 


```bash
.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject> python src\system\baselineRAG\_010203_OfflineIndexing_dataIngestion_Chunking_Embedding\embedding.py
Đang load .env từ: D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\baselineRAG\_010203_OfflineIndexing_dataIngestion_Chunking_Embedding\.env

--- Bắt đầu kiểm tra hàm get_embedding với model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2 ---

Test case 1: Văn bản tiếng Việt
Lỗi khi lấy embedding cho văn bản 'Đây là một câu văn bản tiếng Việt để kiểm tra embe...': 404 Client Error: Not Found for url: https://router.huggingface.co/hf-inference/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (Request ID: Root=1-6831ce75-3862e8cd75e16b5c703e07f2;6f8cea75-69d6-4db0-a4f5-c90e879309e2)
Không thể lấy embedding cho văn bản tiếng Việt.

Test case 2: Văn bản tiếng Anh
Lỗi khi lấy embedding cho văn bản 'This is a simple English text to test the embeddin...': 404 Client Error: Not Found for url: https://router.huggingface.co/hf-inference/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (Request ID: Root=1-6831ce76-3aebd6c8417dc95024c089a1;fed3faf4-5d4f-4218-98f9-db605d7f6f7b)
Không thể lấy embedding cho văn bản tiếng Anh.

Test case 3: Văn bản rỗng
Trả về rỗng cho văn bản rỗng (Đúng).

Test case 4: Văn bản dài hơn (tiếng Việt)
Lỗi khi lấy embedding cho văn bản 'Nghị định 23/2024/NĐ-CP của Chính phủ quy định chi...': 404 Client Error: Not Found for url: https://router.huggingface.co/hf-inference/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (Request ID: Root=1-6831ce77-6a6d73481924bc9561ea19ca;c83faebf-8f01-434e-af0d-60284c40b7dc)
Không thể lấy embedding cho văn bản dài hơn.

--- Kết thúc kiểm tra ---
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject> 
```


```bash
(.venv) PS D:\GIT\MiniProj_RAG3.2_RAG6_LegalChatbot_16032025\src\back-end> python .\backend_vector_database\test_embedding.py
Đang load .env từ: D:\GIT\MiniProj_RAG3.2_RAG6_LegalChatbot_16032025\src\back-end\.env

--- Bắt đầu kiểm tra hàm get_embedding với model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2 ---

Test case 1: Văn bản tiếng Việt
Văn bản: 'Đây là một câu văn bản tiếng Việt để kiểm tra embedding.'
Kích thước embedding: 768
5 giá trị đầu tiên của embedding: [ 0.1385759  -0.29555336 -0.01034726  0.04029174 -0.00863896]     

Test case 2: Văn bản tiếng Anh
Văn bản: 'This is a simple English text to test the embedding function.'
Kích thước embedding: 768
5 giá trị đầu tiên của embedding: [-0.03884416 -0.46244752 -0.00993104  0.08450592 -0.0193656 ]     

Test case 3: Văn bản rỗng
Trả về rỗng cho văn bản rỗng (Đúng).

Test case 4: Văn bản dài hơn (tiếng Việt)
Văn bản: 'Nghị định 23/2024/NĐ-CP của Chính phủ quy định chi tiết một số điều của Luật Đấu thầu về lựa chọn nh...'
Kích thước embedding: 768
5 giá trị đầu tiên của embedding: [-0.02905461  0.1478979  -0.00844338 -0.0625884  -0.00353251]     

--- Kết thúc kiểm tra ---
(.venv) PS D:\GIT\MiniProj_RAG3.2_RAG6_LegalChatbot_16032025\src\back-end>
```


---

### Sau xoá .venv đi, cài lại là fix được. Khá là ???



