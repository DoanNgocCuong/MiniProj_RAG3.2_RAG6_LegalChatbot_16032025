## Tóm tắt

Hiện tượng sử dụng **RAM CPU rất cao (\~12–15 GB)** trong khi **VRAM chỉ chiếm \~1–2 GB** cho thấy model 3 tỉ tham số đang được load chủ yếu lên CPU chứ không phải GPU, rồi chỉ một phần nhỏ (hoặc chỉ context CUDA) được đẩy lên card. Theo mặc định, `from_pretrained(..., device_map="auto")` sẽ “chia” weights giữa GPU/CPU/ổ cứng tuỳ tình trạng bộ nhớ ([Hugging Face][1]), và PyTorch còn khởi tạo context CUDA chiếm thêm \~1–2 GB VRAM trước khi inference ([BOINC AI][2]). Do đó bạn thấy RAM hệ thống vọt lên và container phải chờ tới khi “phân phối” xong mới khởi động FastAPI.

---

## 1. Chẩn đoán nguyên nhân

### 1.1. Mô hình chưa nằm đầy trên GPU

* **`device_map="auto"`** tự động gán layers vào GPU tới khi hết chỗ, rồi phần còn lại nằm trên CPU; nếu CPU RAM không đủ hoặc thiếu spa ce còn lại, HF sẽ dùng memory-mapping ra ổ cứng ([Hugging Face][1]).
* Quá trình load weights ban đầu diễn ra toàn bộ trên CPU trước khi dispatch, dẫn đến spike RAM hệ thống (gần bằng kích thước model FP16 \~6.5 GB cùng overhead) ([GitHub][3]).
* GPU VRAM thấp (\~1–2 GB) chỉ phản ánh **CUDA runtime context** và một số buffer nhỏ, không phải toàn bộ weights ([BOINC AI][2]).

### 1.2. Tác động của offloading & CPU offload

* HF Accelerate có cơ chế **offload**: nếu GPU không đủ, weights phụ sẽ nằm trên CPU (hoặc disk) và chỉ được tải tạm lên GPU khi inference tới đúng layer đó ([Hugging Face][4]).
* Điều này giúp chạy model lớn trên GPU nhỏ, nhưng đổi lại **tốc độ load** và **RAM hệ thống** tăng cao, đồng thời GPU VRAM vẫn thấp vì chỉ “nạp” từng phần khi inference.

---

## 2. Giải pháp tối ưu hoá

### 2.1. Load trực tiếp lên GPU, giảm CPU RAM

Thêm tham số `low_cpu_mem_usage=True` vào `from_pretrained` để **khởi tạo weights ngay trên GPU** (bỏ qua việc load toàn bộ vào CPU) ([Stack Overflow][5], [GitHub][3]):

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
```

### 2.2. Cố định toàn bộ model lên GPU

Nếu bạn chắc có đủ VRAM cho FP16 (\~6.5 GB + overhead):

```python
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map={"": "cuda:0"}   # ép toàn bộ weights lên GPU:0
)
```

Hoặc load rồi gọi:

```python
model = model.to("cuda")
```

để chuyển trọn vẹn lên card ([Stack Overflow][6]).

### 2.3. Dùng Accelerate dispatch nâng cao

Với Accelerate bạn có thể **streaming weights** và tự động offload thông minh hơn:

```python
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
from transformers import AutoConfig, AutoModelForCausalLM

config = AutoConfig.from_pretrained(MODEL_PATH)
with init_empty_weights():
    model = AutoModelForCausalLM(config)
model = load_checkpoint_and_dispatch(
    model,
    checkpoint=MODEL_PATH,
    device_map="auto",
    dtype=torch.float16,
    offload_folder="offload"
)
```

Cách này tận dụng meta-device để khởi tạo nhanh và chỉ tải tensors cần thiết lên GPU ([Hugging Face][7], [Hugging Face][8]).

---

## 3. Giám sát & kiểm thử

1. **Xác thực phân bổ**

   ```python
   from accelerate import infer_auto_device_map
   print(infer_auto_device_map(model, max_memory={"cuda:0":"8GiB","cpu":"16GiB"}))
   ```

   hoặc check `model.device_map` sau khi load.

2. **Theo dõi VRAM tại runtime**

   * Dùng `torch.cuda.memory_allocated()` và `torch.cuda.memory_reserved()` trong code.
   * Dùng `nvidia-smi -l 1` để monitor.

3. **Theo dõi RAM hệ thống**

   * Trong container: `docker stats` hoặc `htop`.
   * Trên host: Task Manager (Windows) / `free -h` (Linux).

---

## 4. Kết luận

* **Nguyên nhân**: model FP16 ban đầu được load trên CPU, `device_map="auto"` offload weights → RAM vọt lên, VRAM vẫn thấp.
* **Khắc phục**:

  1. thêm `low_cpu_mem_usage=True` để stream trực tiếp lên GPU ([Stack Overflow][5])
  2. hoặc ép toàn bộ model lên GPU qua `device_map={"":"cuda:0"}` ([Stack Overflow][6])
  3. hoặc dùng Accelerate dispatch cho big model inference ([Hugging Face][7], [Hugging Face][8])

Áp dụng xong, bạn sẽ thấy **RAM hệ thống hạ xuống** và **VRAM** nhảy lên gần **6–7 GB** như kỳ vọng, đồng thời container khởi động nhanh hơn mà không phải chờ hết spike RAM.

[1]: https://huggingface.co/docs/accelerate/concept_guides/big_model_inference?utm_source=chatgpt.com "Loading big models into memory - Hugging Face"
[2]: https://boinc-ai.gitbook.io/accelerate/concepts-and-fundamentals/loading-big-models-into-memory?utm_source=chatgpt.com "Loading big models into memory | Accelerate - GitBook"
[3]: https://github.com/huggingface/transformers/issues/21913?utm_source=chatgpt.com "[performance] from_pretrained is still much slower than torch.load and ..."
[4]: https://huggingface.co/docs/diffusers/main/en/optimization/memory?utm_source=chatgpt.com "Reduce memory usage - Hugging Face"
[5]: https://stackoverflow.com/questions/75725818/loading-hugging-face-model-is-taking-too-much-memory?utm_source=chatgpt.com "Loading Hugging face model is taking too much memory"
[6]: https://stackoverflow.com/questions/77713051/why-does-my-device-map-auto-in-transformers-pipline-uses-cpu-only-even-though?utm_source=chatgpt.com "Why does my device_map=\"auto\" in transformers.pipline uses CPU only ..."
[7]: https://huggingface.co/docs/accelerate/package_reference/big_modeling?utm_source=chatgpt.com "Working with large models - Hugging Face"
[8]: https://huggingface.co/docs/accelerate/usage_guides/big_modeling?utm_source=chatgpt.com "Big Model Inference - Hugging Face"
