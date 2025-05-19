import requests
import json
import argparse

def get_embedding(texts, url="http://localhost:8000"):
    """Lấy embedding từ API local"""
    try:
        response = requests.post(
            f"{url}/embeddings",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"texts": texts})
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

def compute_similarity(texts, url="http://localhost:8000"):
    """Tính độ tương đồng giữa các văn bản"""
    try:
        response = requests.post(
            f"{url}/similarity",
            headers={"Content-Type": "application/json"},
            data=json.dumps(texts)
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

def get_model_info(url="http://localhost:8000"):
    """Lấy thông tin về mô hình"""
    try:
        response = requests.get(f"{url}/info")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client kết nối đến Embedding API")
    parser.add_argument("--action", choices=["embed", "similarity", "info"], default="embed", 
                        help="Hành động: embed (tạo embedding), similarity (tính độ tương đồng), info (thông tin mô hình)")
    parser.add_argument("--texts", nargs="+", help="Các văn bản đầu vào")
    parser.add_argument("--url", default="http://localhost:8000", help="URL của API")
    
    args = parser.parse_args()
    
    if args.action == "embed" and args.texts:
        result = get_embedding(args.texts, args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "similarity" and args.texts:
        result = compute_similarity(args.texts, args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.action == "info":
        result = get_model_info(args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Thiếu tham số. Hãy chạy với --help để xem hướng dẫn.") 