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
        local_dir=target_dir,
        token=os.getenv("HF_TOKEN")  # Thêm token nếu model private
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
        low_cpu_mem_usage=True,  # tiết kiệm RAM khi load
        device_map="auto"  # tự động chọn device phù hợp
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
    # Model Llama-3.2-3B-Instruct-Frog từ Hugging Face
    HF_REPO   = "phamhai/Llama-3.2-3B-Instruct-Frog"
    RAW_DIR   = "raw"   # nơi download nguyên gốc
    FP16_DIR  = "fp16"  # nơi sẽ lưu model FP16
    TOK_DIR   = "tokenizer"

    # Download model raw
    download_repo(HF_REPO, RAW_DIR)

    # Save tokenizer
    save_tokenizer(RAW_DIR, TOK_DIR)

    # Convert & save FP16
    convert_fp16_and_save(RAW_DIR, FP16_DIR)

if __name__ == "__main__":
    main() 