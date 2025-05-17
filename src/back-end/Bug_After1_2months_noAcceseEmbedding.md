# VẤN ĐỀ MÔ HÌNH EMBEDDING ĐANG GẶP TRÊN HUGGING FACE

Sau khi tìm hiểu các thông tin từ nhiều nguồn, tôi có thể xác định được nguyên nhân và giải pháp cho vấn đề các mô hình embedding đột ngột không hoạt động trong dự án của bạn.

## 1. VẤN ĐỀ

Dựa trên log lỗi, hệ thống của bạn đang gặp vấn đề với mã lỗi 401 (Unauthorized) khi cố gắng truy cập các mô hình embedding từ Hugging Face. Tất cả các mô hình embedding tiếng Việt được thử nghiệm đều trả về lỗi 401, mặc dù kết nối đến API Hugging Face thành công thông qua lệnh `whoami`.

## 2. NGUYÊN NHÂN

Sau khi nghiên cứu, tôi phát hiện có một số thay đổi quan trọng trong hệ thống API của Hugging Face trong những tháng gần đây:

### 2.1. Thay đổi cơ chế API của Hugging Face

Hugging Face đã chuyển từ mô hình "Serverless Inference API" cũ sang hệ thống mới là "Inference Providers" vào đầu năm 2025. Như được đề cập trong [tài liệu chính thức](https://huggingface.co/docs/inference-providers/en/index), đây là một cách tiếp cận hoàn toàn mới, làm thay đổi cách thức truy cập và xác thực các mô hình.

### 2.2. Thay đổi chính sách hạn ngạch và giới hạn sử dụng

Có nhiều người dùng báo cáo rằng Hugging Face đã thay đổi giới hạn API từ 1000 lệnh gọi miễn phí mỗi ngày xuống còn $0.10 tín dụng miễn phí mỗi tháng, ảnh hưởng đến nhiều người dùng, đặc biệt là trong các tình huống sử dụng không thương mại.

### 2.3. Lỗi kỹ thuật trên hệ thống

Như được thấy trong [bài thảo luận này](https://discuss.huggingface.co/t/inference-api-stopped-working/150492), bắt đầu từ giữa tháng 4/2025, nhiều người dùng báo cáo rằng API suy luận (Inference API) đột nhiên ngừng hoạt động đối với nhiều mô hình khác nhau, trả về lỗi 401 hoặc thông báo "Model xxx is not supported HF inference api".

### 2.4. Thay đổi cách xác thực token

Cách thức xác thực token đã thay đổi, yêu cầu thêm quyền "inference.serverless.write" cho các token mới, và có thể các token cũ không còn khả năng tương thích.

### 2.5. Giới hạn mô hình được hỗ trợ

Hugging Face đã giới hạn đáng kể số lượng mô hình được hỗ trợ thông qua API suy luận miễn phí. Thay vì hỗ trợ hàng chục nghìn mô hình như trước đây, giờ đây chỉ còn một số mô hình được chọn lọc.

## 3. GIẢI PHÁP

Dựa trên phân tích trên, dưới đây là các giải pháp tôi đề xuất:

### 3.1. Tạo token API mới với quyền cụ thể

```bash
# Truy cập vào trang https://huggingface.co/settings/tokens/new
# Tạo token mới với các quyền sau:
# - inference.serverless.write
```

Đảm bảo chọn token loại "fine-grained" thay vì token đơn giản, và chọn phạm vi "Make calls to Inference Providers" như được đề cập trong tài liệu mới.

### 3.2. Cập nhật cách truyền mới 

```bash
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key="hf_xxxxxxxxxxxxxxxxxxxxxxxx",
)

result = client.sentence_similarity(
    inputs={
    "source_sentence": "That is a happy person",
    "sentences": [
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day"
    ]
},
    model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
)
```

## 4. IMPLEMENTATION FIX

### 4.1. Trước khi fix

Ban đầu, code sử dụng `HuggingFaceInferenceAPIEmbeddings` từ `langchain_community.embeddings`:

```python
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=Config.HUGGINGFACE_API_KEY,
    model_name=Config.EMBEDDINGS_MODEL_NAME
)

# Sử dụng
query_vector = embeddings.embed_query(query)
```

### 4.2. Sau khi fix

Đã chuyển sang sử dụng `InferenceClient` trực tiếp từ `huggingface_hub`:

```python
from huggingface_hub import InferenceClient

embeddings_client = InferenceClient(
    provider="hf-inference",
    api_key=Config.HUGGINGFACE_API_KEY
)

# Sử dụng
query_vector = embeddings_client.feature_extraction(
    model=Config.EMBEDDINGS_MODEL_NAME,
    text=query  # Lưu ý: sử dụng 'text' thay vì 'inputs'
)
```

### 4.3. Những thay đổi chính

1. Thay đổi import:
   - Từ: `from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings`
   - Thành: `from huggingface_hub import InferenceClient`

2. Thay đổi cách khởi tạo client:
   - Thêm tham số `provider="hf-inference"`
   - Đổi tên biến từ `embeddings` thành `embeddings_client`

3. Thay đổi cách gọi API:
   - Từ: `embeddings.embed_query(query)`
   - Thành: `embeddings_client.feature_extraction(model=..., text=query)`

4. Thay đổi tên tham số:
   - Sử dụng `text` thay vì `inputs` trong phương thức `feature_extraction()`

### 4.4. Lợi ích của cách triển khai mới

1. Truy cập trực tiếp API của Hugging Face, giảm độ trễ
2. Kiểm soát tốt hơn các tham số và xử lý lỗi
3. Tương thích với hệ thống Inference Providers mới
4. Dễ dàng mở rộng và tùy chỉnh theo nhu cầu