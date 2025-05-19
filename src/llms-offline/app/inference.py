import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# Đường dẫn tới thư mục chứa model FP16 và tokenizer
MODEL_FP16_PATH = "/app/model/fp16"
TOKENIZER_PATH = "/app/model/tokenizer"

# 1. Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, use_fast=True)

# 2. Load model FP16 và chuyển lên GPU nếu có
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device for inference: {device}")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_FP16_PATH,
    torch_dtype=torch.float16,
).to(device).eval()

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
