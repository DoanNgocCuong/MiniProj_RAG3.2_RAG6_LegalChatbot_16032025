Model: Llama-3.2-3B-Instruct-Frog

* **FP16**: \~6.5 GB VRAM ([Llama Ai Model][5])

---
Dưới đây là script mẫu `prepare_model_fp16.py` để:

1. Tự động tải model về từ Hugging Face
2. Chuyển weights sang FP16 (16-bit)
3. Lưu lại vào thư mục `llms-offline/model/fp16` để bạn mount vào Docker Compose

```python
# prepare_model_fp16.py

import os
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def download_repo(repo_id: str, target_dir: str):
    """
    Tải toàn bộ repo model về target_dir thông qua huggingface_hub
    """
    print(f"[1/3] Downloading {repo_id} into {target_dir} …")
    snapshot_download(
        repo_id=repo_id,
        cache_dir=target_dir,
        resume_download=True,
        local_dir=target_dir
    )
    print("    Download complete.\n")

def convert_fp16_and_save(src_dir: str, dst_dir: str):
    """
    Load model full-precision, convert sang FP16 và save
    """
    print(f"[2/3] Loading model from {src_dir} in FP16 …")
    model = AutoModelForCausalLM.from_pretrained(
        src_dir,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True  # tiết kiệm RAM khi load
    )
    os.makedirs(dst_dir, exist_ok=True)
    print(f"[3/3] Saving FP16 model to {dst_dir} …")
    # đưa model về CPU trước khi save để tránh lỗi
    model.to("cpu")
    model.save_pretrained(dst_dir)
    print("    FP16 model saved.\n")

def save_tokenizer(src_dir: str, dst_dir: str):
    """
    Copy tokenizer (vẫn full-precision)
    """
    print("Saving tokenizer …")
    tokenizer = AutoTokenizer.from_pretrained(src_dir, use_fast=True)
    os.makedirs(dst_dir, exist_ok=True)
    tokenizer.save_pretrained(dst_dir)
    print("    Tokenizer saved.\n")

def main():
    # 1. Thay bằng repo của bạn
    HF_REPO   = "YourOrg/Llama-3.2-3B-Instruct-Frog"
    RAW_DIR   = "llms-offline/model/raw"   # nơi download nguyên gốc
    FP16_DIR  = "llms-offline/model/fp16"  # nơi sẽ lưu model FP16
    TOK_DIR   = "llms-offline/model/tokenizer"

    # Download model raw
    download_repo(HF_REPO, RAW_DIR)

    # Save tokenizer
    save_tokenizer(RAW_DIR, TOK_DIR)

    # Convert & save FP16
    convert_fp16_and_save(RAW_DIR, FP16_DIR)

if __name__ == "__main__":
    main()
```

---

### Cách dùng

1. Cài thư viện:

   ```bash
   pip install torch transformers huggingface_hub
   ```
2. Chạy script:

   ```bash
   cd llms-offline
   python prepare_model_fp16.py
   ```
3. Kết quả:

   * `llms-offline/model/raw/` chứa repo gốc
   * `llms-offline/model/tokenizer/` chứa tokenizer
   * `llms-offline/model/fp16/` chứa weights đã chuyển sang FP16

Sau đó bạn chỉ cần chỉnh `docker-compose.yml` mount thư mục `model/fp16` và `model/tokenizer` vào container là xong.
