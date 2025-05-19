import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from .monitoring import log_resource_usage, clear_gpu_memory

# Đường dẫn tới thư mục chứa model FP16 và tokenizer
MODEL_FP16_PATH = "/app/model/fp16"
TOKENIZER_PATH = "/app/model/tokenizer"

# 1. Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, use_fast=True)

# 2. Load model FP16 và chuyển lên GPU nếu có
device = "cuda" if torch.cuda.is_available() else "cpu"
log_resource_usage("Before model load")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_FP16_PATH,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
    device_map="auto"
).eval()

log_resource_usage("After model load")

# 3. Hàm generate
def generate(
    prompt: str,
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    top_p: float = 0.9,
    do_sample: bool = True,
):
    log_resource_usage("Before generation")
    
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

    # sinh văn bản với inference mode và mixed precision
    with torch.inference_mode():
        with torch.cuda.amp.autocast():
            out = model.generate(**inputs, generation_config=gen_config)
            result = tokenizer.decode(out[0], skip_special_tokens=True)
    
    log_resource_usage("After generation")
    clear_gpu_memory()  # Xóa cache sau mỗi lần generate
    
    return result
