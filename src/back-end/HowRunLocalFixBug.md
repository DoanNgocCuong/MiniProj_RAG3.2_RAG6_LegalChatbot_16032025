```bash
uvicorn rag_backend:app --host 0.0.0.0 --port 30002 --reload --log-level debug
```
```bash
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

logger = logging.getLogger("rag-backend")
```

1. Test câu hỏi có sẵn: 
```bash
curl --location 'http://localhost:30002/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
       "messages": [
         {"role": "user", "content": "Trình bày những quy định cấm trong vùng đặc quyền kinh tế, thềm lục địa và quyền truy đuổi tàu thuyền nước ngoài theo luật biển Việt Nam?"}
       ],
       "model": "gpt-4o"
     }'
```

Tầm: 500ms 


2. Test câu hỏi cần suy luận, tầm 8-12s: 
```
curl --location 'http://localhost:30002/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
       "messages": [
         {"role": "user", "content": "Quy tắc giao thông đường bộ là gì?"}
       ],
       "model": "gpt-4o"
     }'
```

Output: 
```
{
    "id": "chatcmpl-90e44fc938acb1150d92bd06",
    "object": "chat.completion",
    "created": 20764607,
    "model": "gpt-4o-2024-08-06",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Quy tắc giao thông đường bộ là tập hợp các quy định và hướng dẫn nhằm điều chỉnh hành vi của người tham gia giao thông trên đường bộ. Những quy tắc này được thiết lập để đảm bảo an toàn và trật tự giao thông, giảm thiểu tai nạn và tối ưu hóa lưu thông trên đường.\n\nQuy tắc giao thông đường bộ thường bao gồm các quy định về:\n\n1. Các biển báo và tín hiệu giao thông: Hướng dẫn người tham gia giao thông về các biển báo hiệu, đèn tín hiệu và các chỉ dẫn trên đường.\n\n2. Quyền ưu tiên: Quy định về quyền ưu tiên của các phương tiện giao thông tại các giao lộ, ngã ba, ngã tư và các tình huống khác trên đường.\n\n3. Tốc độ và khoảng cách: Hướng dẫn về tốc độ tối đa cho phép và khoảng cách an toàn giữa các phương tiện.\n\n4. Làn đường và hướng đi: Quy định về việc di chuyển trong các làn đường và hướng đi đúng theo quy định của từng loại đường.\n\n5. Đỗ xe: Các quy định về vị trí và cách thức đỗ xe hợp pháp.\n\n6. Hành vi của người điều khiển phương tiện: Quy định về việc sử dụng điện thoại, uống rượu bia khi lái xe và các hành vi khác ảnh hưởng đến an toàn giao thông.\n\n7. Quy định dành cho người đi bộ và người đi xe đạp: Hướng dẫn về cách thức di chuyển an toàn cho người đi bộ và người đi xe đạp.\n\nQuy tắc giao thông đường bộ được quy định bởi các cơ quan chức năng của từng quốc gia hoặc vùng lãnh thổ và thường được điều chỉnh theo thời gian để phù hợp với tình hình giao thông thực tế."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "completion_tokens": 370,
        "prompt_tokens": 2791,
        "total_tokens": 3161,
        "completion_tokens_details": {
            "accepted_prediction_tokens": 0,
            "audio_tokens": 0,
            "reasoning_tokens": 0,
            "rejected_prediction_tokens": 0
        },
        "prompt_tokens_details": {
            "audio_tokens": 0,
            "cached_tokens": 2688
        }
    }
}
```