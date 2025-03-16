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

{
    "id": "chatcmpl-bd3d4c3c2ca5b11947d8756f",
    "object": "chat.completion",
    "created": 20764663,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Quy định cấm trong vùng đặc quyền kinh tế và thềm lục địa Việt Nam\n - Khi thực hiện quyền tự do hàng hải, tự do hàng không trong vùng đặc quyền kinh tế và thềm lục địa Việt Nam, tổ chức, cá nhân không được tiến hành các hoạt động sau đây:\n + Đe dọa chủ quyền, quốc phòng, an ninh của Việt Nam;\n + Khai thác trái phép tài nguyên sinh vật, đánh bắt hải sản trái phép;\n \n + Khai thác trái phép dòng chảy, năng lượng gió và tài nguyên phi sinh vật khác;\n + Xây dựng, lắp đặt, sử dụng trái phép các thiết bị, công trình nhân tạo;\n + Khoan, đào trái phép;\n + Tiến hành nghiên cứu khoa học trái phép;\n + Gây ô nhiễm môi trường biển;\n + Cướp biển, cướp có vũ trang;\n + Các hoạt động bất hợp pháp khác theo quy định của pháp luật Việt Nam và pháp luật quốc tế.\n Quyền truy đuổi tàu thuyền nước ngoài\n - Lực lượng tuần tra, kiểm soát trên biển có quyền truy đuổi tàu thuyền nước ngoài vi phạm các quy định của pháp luật Việt Nam nếu các tàu thuyền này đang ở trong nội thủy, lãnh hải và vùng tiếp giáp lãnh hải Việt Nam.\n - Quyền truy đuổi được tiến hành sau khi lực lượng tuần tra, kiểm soát trên biển đã phát tín hiệu yêu cầu tàu thuyền vi phạm hay có dấu hiệu vi phạm pháp luật dưng lại để tiến hành kiểm tra nhưng tàu thuyền đó không chấp hành. Việc truy đuổi có thể được tiếp tục ở ngoài ranh giới của lãnh hải hay vùng tiếp giáp lãnh hải Viêt Nam nếu được tiến hành liên tục, không ngắt quãng.\n - Quyền truy đuổi cũng được áp dụng đối với hành vi vi phạm quyền chủ quyền, quyền tài phán quốc gia của Việt Nam, vi phạm trong phạm vi vành đai an toàn và trên các đảo nhân tạo, thiết bị, công trình trên biển trong vùng đặc quyền kinh tế và thềm lục địa Việt Nam.\n - Việc truy đuổi của các lực lượng tuần tra, kiểm soát Việt Nam chấm dứt khi tàu thuyền bị truy đuổi đi vào lãnh hải của quốc gia khác.\n\n(Nguồn: backend_vector_database/dataset/LegalRAG.xlsx)"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }
}


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