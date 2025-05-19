@llms-offline 

Dưới đây là 2 file code mẫu để bạn triển khai nhanh Llama-3.2-3B-Instruct-Frog ở chế độ FP16 (\~6.5 GB VRAM) với FastAPI. Giả sử bạn đã có model trên thư mục `llms-offline/model`.

---

### 1. `inference.py`

```python
# inference.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# Đường dẫn tới thư mục chứa model đã tải về
MODEL_PATH = "llms-offline/model"

# 1. Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=True)

# 2. Load model FP16, device_map="auto" sẽ tự chọn GPU nếu có
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
).eval()

# 3. Hàm generate
def generate(
    prompt: str,
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    top_p: float = 0.9,
    do_sample: bool = True,
):
    # tokenize và chuyển tensor lên device model
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # cấu hình generation
    gen_config = GenerationConfig(
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        do_sample=do_sample,
        pad_token_id=tokenizer.eos_token_id,
    )

    # sinh văn bản
    out = model.generate(**inputs, generation_config=gen_config)
    return tokenizer.decode(out[0], skip_special_tokens=True)
```

---

### 2. `service.py`

```python
# service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from inference import generate

class Request(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True

class Response(BaseModel):
    text: str

app = FastAPI(title="Llama-3.2-3B-Instruct-Frog API")

@app.post("/v1/generate", response_model=Response)
async def v1_generate(req: Request):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="`prompt` is required.")
    try:
        text = generate(
            prompt=req.prompt,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            do_sample=req.do_sample
        )
        return Response(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 3. Chạy service

* Đảm bảo bạn đang ở thư mục `llms-offline/` (chứa `Dockerfile`, `docker-compose.yml`, `app/`, `model/`).
* Trong `docker-compose.yml` giữ nguyên cấu hình trước đó.
* Build & chạy:

```bash
cd llms-offline
docker compose up -d --build
```

* Test nhanh:

```bash
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Viết một đoạn văn ngắn về tầm quan trọng của AI trong giáo dục.",
    "max_tokens":60,
    "temperature":0.8,
    "top_p":0.95
  }'
```

Vậy là bạn đã có API service chạy Llama-3.2-3B-Instruct-Frog ở chế độ FP16, tận dụng \~6.5 GB VRAM. Nếu cần thêm streaming hoặc tuỳ chỉnh khác, bạn có thể mở rộng trực tiếp trong `service.py`.



====


@llms-offline 