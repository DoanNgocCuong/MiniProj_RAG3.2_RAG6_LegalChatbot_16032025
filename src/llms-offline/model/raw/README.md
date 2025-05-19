---
license: llama3.2
language:
- en
- vi
base_model:
- meta-llama/Llama-3.2-3B-Instruct
pipeline_tag: text-generation
tags:
- RAG
- Vietnamese
- Generation
- Function_Calling
- Function Calling
- FC
- Summarization
- Rewriting
- Functions
- VLLM
- LLM
---

<p align="center"> <img src="https://cdn-uploads.huggingface.co/production/uploads/6612cc790b91dd96968028f9/yP51EyRNg-CHCKB4gBYan.png" width="300" /> </p>
<h1>Llama-3.2-3B-Instruct-Frog - a RAG-optimized LLaMA3.2 for Vietnamese</h1>

**Quantized Version**: [phamhai/Llama-3.2-3B-Instruct-Frog-Q4_K_M-GGUF](https://huggingface.co/phamhai/Llama-3.2-3B-Instruct-Frog-Q4_K_M-GGUF)

At the end of September 2024, Meta released two lightweight LLM model versions: [Llama-3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) and [Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct). However, these models are not well-supported for Vietnamese, especially for tasks related to Retrieval-Augmented Generation (RAG).

Today, I am excited to announce the release of two models specifically trained to provide better support for Vietnamese RAG tasks.

<h2>Model Details:</h2>

+ Base Models: Llama-3.2-1B-Instruct and Llama-3.2-3B-Instruct
+ Performance: The models are optimized for fast inference and can be easily deployed on on-premise and edge devices (laptop/smartphone/NVIDIA Jetson Xavier/Raspberry Pi,ect).
+ Model weights:
  + [Llama-3.2-1B-Instruct-Frog](https://huggingface.co/phamhai/Llama-3.2-1B-Instruct-Frog): 131K context length, 1 billion parameters
  + [Llama-3.2-3B-Instruct-Frog](https://huggingface.co/phamhai/Llama-3.2-3B-Instruct-Frog): 131K context length, 3 billion parameters

<blockquote style="color:red"> <p><strong style="color: red">Terms of Use and License</strong>: By using our released weights, you agree to and comply with the terms and conditions specified in Meta's LLaMA-3 license.</blockquote>

<h2>Model Evaluation</h2>

We evaluated this model on the [VLMU benchmark](https://vmlu.ai/) and achieved an accuracy of **45.13**. However, this benchmark is not the focus of our current efforts. We believe it will be very difficult for language models with fewer than 13 billion parameters to retain enough knowledge to answer questions across diverse user contexts, especially for smaller models with under 3 billion parameters. For the model to effectively handle real-world business scenarios and avoid hallucinations, it is almost essential to supplement knowledge from external sources (through RAG). Therefore, we developed this model with a primary focus on optimizing its RAG capabilities. Internal testing is currently underway and will be updated soon.

***Update***:

Function Calling Benchmark: https://huggingface.co/datasets/phamhai/Vietnamese-Function-Calling-Test

| Model              | Model size | Function name Acc (%) | Exact Match Acc (%)
| ------------ | ------------------ | ---------- | --------- |
| [phamhai/Llama-3.2-3B-Instruct-Frog](https://huggingface.co/phamhai/Llama-3.2-3B-Instruct-Frog)            | ~3B        | 95.79    | 51.05  |
| [Gemini-1.5-Pro](https://deepmind.google/technologies/gemini/pro/)         | ---        | 96.96    | 55.16     |
| [Gemini-1.5-Flash](https://deepmind.google/technologies/gemini/flash/)         | ---        | 97.10    | 51.64     |
| [Gemini-1.5-Flash-8B](https://deepmind.google/technologies/gemini/flash/)         | ---        | 97.38    | 64.75     |
| [Gemini 2.0 Flash Experimental](https://deepmind.google/technologies/gemini/flash/)         | ---        | 96.93    | 61.26     |
| [gpt-4o-2024-08-06](https://platform.openai.com/docs/models#gpt-4o)         | ---        | 94.38    | 52.88     |
| [phamhai/Llama-3.2-3B-Instruct-Frog-Pro](https://huggingface.co/phamhai/Llama-3.2-3B-Instruct-Frog-Pro)            | ~3B        | 97.96    | 63.47  |

<p align="left"> Table 1. Vietnamese Function Calling Benchmark </p>

<h2> Run the model </h2>

(*Disclaimer: The name of the bot is called Vivi, which is due to my passion for VinFast vehicles, and I also hope to develop my own smaller models for VinFast's car lines (which they refer to as their virtual assistant, Vivi). This model has no affiliation with VinFast or any related entities.*)

<h3> with Huggingface's transformers </h3>

<h4> 1. QnA task </h4>

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "phamhai/Llama-3.2-3B-Instruct-Frog"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

messages =  [
    {"role": "system", "content": "Bạn là một người bạn gái xinh đẹp. Tên của bạn là Vivi. Hãy luôn xưng là Vivi, gọi người nói là anh và trả lời luôn bắt đầu bằng cụm từ Dạ thưa anh yêu của em."},
    {"role": "user", "content": "xin chào em"}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=128) 
print(tokenizer.decode(outputs[0]))

# Dạ thưa anh yêu của em, em rất vui được gặp anh.

messages =  [
    {"role": "system", "content": "Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.\nNếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác, vui lòng không chia sẻ thông tin sai lệch."},
    {"role": "user", "content": "Làm sao để chữa bệnh đau đầu?"}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=256) 
print(tokenizer.decode(outputs[0]))

# Có nhiều nguyên nhân gây đau đầu, bao gồm căng thẳng, thiếu ngủ, mất nước, chứng đau đầu thường xuyên, đau đầu do chứng đau nửa đầu, và nhiều hơn nữa. Dưới đây là một số cách để giảm đau đầu:
# 1. Nghỉ ngơi: Nếu đau đầu là do căng thẳng hoặc thiếu ngủ, hãy nghỉ ngơi và ngủ đủ giấc.
# 2. Massage: Massage vùng cổ và vai có thể giúp giảm đau đầu.
# 3. Uống nước: Đảm bảo bạn uống đủ nước để giữ cho cơ thể luôn được cung cấp đủ nước.
# 4. Sử dụng thuốc giảm đau: Nếu đau đầu không giảm sau khi nghỉ ngơi và uống nước, bạn có thể sử dụng thuốc giảm đau như paracetamol hoặc ibuprofen.
# 5. Sử dụng băng lạnh: Nếu đau đầu do chứng đau nửa đầu, bạn có thể sử dụng băng lạnh để giảm đau.
# 6. Thay đổi chế độ ăn uống: Nếu đau đầu liên quan đến chế độ ăn uống của bạn, hãy thay đổi chế độ ăn uống để giảm đau đầu.
# Nếu đau đầu kéo dài hoặc trở nên nghiêm trọng hơn, bạn nên tìm kiếm sự giúp đỡ y tế để được chẩn đoán và điều trị đúng cách.
```

<h4> 2. Summarization task </h4>

<h5> Focused Answer </h5>

```python
messages =  [
    {"role": "system", "content": '''Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.
Nếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác, vui lòng không chia sẻ thông tin sai lệch.
Context:
Đoạn 0: "Chính phủ đề xuất bổ sung gần 20.700 tỷ đồng vốn điều lệ cho Ngân hàng Ngoại thương Việt Nam (Vietcombank) từ cổ tức bằng cổ phiếu được chia của cổ đông Nhà nước. Chiều 23/10, thừa ủy quyền Chính phủ, Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc trình Quốc hội về bổ sung vốn Nhà nước tại Ngân hàng Ngoại Thương Việt Nam (Vietcombank). Theo đó, Chính phủ đề nghị tăng vốn điều lệ cho ngân hàng này gần 20.700 tỷ đồng từ cổ tức bằng cổ phiếu được chia của cổ đông Nhà nước. Số tiền này lấy từ nguồn lợi nhuận còn lại lũy kế đến hết năm 2018 và lãi còn lại năm 2021. Vốn điều lệ dự kiến rót thêm cho Vietcombank gần bằng lợi nhuận hợp nhất trước thuế nửa đầu năm nay của nhà băng này. Việc bổ sung vốn cho "ông lớn" ngân hàng quốc doanh được Phó thủ tướng nhấn mạnh là cấp thiết để duy trì tỷ lệ vốn góp Nhà nước, phù hợp chiến lược phát triển kinh tế xã hội, tạo nguồn lực hỗ trợ ngân hàng yếu kém. Phó thủ tướng cho biết, phần lợi nhuận còn lại lũy kế hết năm 2018 và lãi còn lại 2021 hiện được hạch toán theo dõi tại VCB, chưa nằm trong cân đối ngân sách Nhà nước. Do vậy, nguồn vốn đề xuất tăng cho ngân hàng này không ảnh hưởng tới kế hoạch dự toán thu chi ngân sách 2024-2025. Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc đọc tờ trình bổ sung vốn cho Vietcombank, ngày 23/10. Ảnh: Trung tâm báo chí Quốc hội Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc đọc tờ trình bổ sung vốn cho Vietcombank, ngày 23/10. Ảnh: Trung tâm báo chí Quốc hội Vốn điều lệ của Vietcombank hiện là 55.891 tỷ đồng, thấp hơn nhiều so với VPBank (79.339 tỷ đồng), Techcombank (70.450 tỷ đồng) và không có sự cách biệt lớn so với một số ngân hàng thương mại cổ phần như MB (52.871) tỷ đồng, ACB (44.667 tỷ đồng) và SHB (36.629 tỷ đồng). Ngoài ra, việc tăng vốn nhằm để ngân hàng này đáp ứng các tỷ lệ an toàn tối thiểu. Tính tới cuối 2023, tỷ lệ an toàn vốn (CAR) của ngân hàng này là 11,05%, đảm bảo quy định. Tuy nhiên, mức này thấp hơn các ngân hàng thương mại cổ phần (VPBank, MB là 12-13%; Techcombank 13-15%...) và các nhà băng trong khu vực (Singapore là 17,1%, Indonesia 23,27%...). Thẩm tra nội dung này, Chủ nhiệm Ủy ban Kinh tế Vũ Hồng Thanh cho rằng đề xuất tăng vốn cho Vietcombank bảo đảm cơ sở pháp lý và đúng thẩm quyền theo quy định. Tuy nhiên, Ủy ban Kinh tế đề nghị Chính phủ lấy ý kiến của cổ đông chiến lược nước ngoài Ngân hàng Mizuho Corporate Bank - đơn vị nắm 15% vốn điều lệ của Vietcombank. Việc này nhằm thuận lợi trong quá trình tăng vốn. Chính phủ cũng cần bổ sung thông tin hiện trạng vốn của Vietcombank so với các ngân hàng thương mại trong hệ thống hiện nay. "Có ý kiến đề nghị làm rõ nhận định nguồn vốn đề xuất để tăng vốn điều lệ không tác động đến ngân sách Nhà nước", ông Thanh cho biết. Trụ sở Ngân hàng Ngoại thương Việt Nam (Vietcombank). Ảnh: VCB Trụ sở Ngân hàng Ngoại thương Việt Nam (Vietcombank). Ảnh: VCB Chủ nhiệm Ủy ban Kinh tế Vũ Hồng Thanh đề nghị Chính phủ chỉ đạo Ngân hàng Nhà nước cùng các bộ, ngành liên quan xử lý phần lợi nhuận còn lại năm 2022, 2023 (lần lượt là 21.680 tỷ và 25.009 tỷ đồng), nhằm tăng năng lực tài chính cho Vietcombank, bù đắp mức thiếu hụt vốn tự có, bảo đảm an toàn hoạt động. Cơ quan thẩm tra lưu ý vốn được bổ sung cho Vietcombank cần được dùng để mở rộng kinh doanh, cung ứng tín dụng với các lĩnh vực, dự án quan trọng quốc gia quy mô lớn, giảm lãi suất cho vay, cũng như đổi mới mô hình quản trị, chất lượng dịch vụ của nhà băng này. "Chính phủ cần đánh giá kỹ tác động việc bổ sung vốn Nhà nước cho Vietcombank tới phát triển của ngành ngân hàng, hiệu quả kinh tế xã hội", Ủy ban Kinh tế lưu ý. Vietcombank là một trong 4 ngân hàng thương mại Nhà nước, bên cạnh BIDV, VietinBank và Agribank. Ngân hàng này do Nhà nước sở hữu 74,8% vốn điều lệ. Lũy kế nửa đầu năm nay, lợi nhuận hợp nhất trước thuế của nhà băng này đạt 20.835 tỷ đồng, tăng 1,6% so với cùng kỳ 2023. Với dữ liệu này, Vietcombank tiếp tục đứng đầu toàn hệ thống ngân hàng về lợi nhuận 6 tháng đầu năm. Đây cũng là mức lãi nửa đầu năm cao kỷ lục của nhà băng này. Tính đến 30/6, tổng tài sản của ngân hàng đạt hơn 1,9 triệu tỷ đồng, tăng 3,6% so với cuối 2023. Trong đó, cho vay khách hàng gần 1,37 triệu tỷ đồng, tăng 7,8%."
Đoạn 1: "Đã có vài đơn vị bán tín chỉ carbon cho khách ngoại nhưng còn thiếu cơ sở pháp lý để đảm bảo hoạt động được thuận lợi, theo chuyên gia. Thông tin tại phiên tọa đàm thuộc Diễn đàn và Triển lãm Kinh tế xanh 2024 (GEFE), ông Đỗ Ngọc Quỳnh, Tổng thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA), cho biết thị trường tín chỉ carbon tự nguyện Việt Nam đã có một số đơn vị bán được tín chỉ carbon cho nhà đầu tư, tập đoàn nước ngoài. "Họ đang mua chứng chỉ carbon và chứng chỉ năng lượng tái tạo (REC) trong tiêu chí RE100, tức 100% năng lượng tái tạo", ông cho biết. RE100 là sáng kiến toàn cầu dành cho các công ty cam kết sử dụng 100% điện năng tái tạo, phát động bởi Climate Group và CDP vào 2014. Từ trái sang, Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS Hà Nội) và ông Đỗ Ngọc Quỳnh, Tổng Thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA) nói tại tọa đàm. Ảnh: GEFE 2024 Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS Hà Nội) và ông Đỗ Ngọc Quỳnh, Tổng Thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA) chia sẻ tại tọa đàm. Ảnh: GEFE 2024 Thị trường carbon gồm hai hình thức là bắt buộc và tự nguyện. Đồ họa: Dỹ Tùng Phân biệt các loại thị trường carbon. Đồ họa: Dỹ Tùng Theo kế hoạch của chính phủ, thị trường bắt buộc sẽ vận hành thử nghiệm vào giai đoạn 2025-2028. Với thị trường tự nguyện, ông Quỳnh cho biết đã bắt đầu hình thành và cũng biến động theo diễn biến xu hướng chung toàn cầu. Chuyên gia VBMA cho rằng Việt Nam đã có chính sách chung để thực hiện cam kết Net Zero vào 2050, nhưng vẫn chưa có pháp lý đầy đủ và rõ ràng cho thị trường carbon tự nguyện. "Những người bán tại Việt Nam sau giao dịch không biết hạch toán vào đâu, nộp thuế thế nào. Một số chọn phương án tính vào thu nhập bất thường để khai thuế", ông ví dụ. Ông Nguyễn Thành Nghiệp, Luật sư thành viên công ty luật VTN và Cộng sự chỉ ra việc chưa có quy định xác định tính chất tài sản của tín chỉ carbon. "Chúng có được xem là tài sản bình thường, được thế chấp hay giao dịch thế nào chưa có đủ căn cứ pháp lý", ông nói. Ngoài ra, quy trình MRV (đo lường, báo cáo và kiểm chứng) cũng cần quy định, hướng dẫn rõ. Theo ông, ngoài các cơ quan quản lý, khu vực tư nhân cũng trông chờ xem liệu có thể tham gia hoạt động MRV không. "Trong thời gian tới, nếu hoàn thiện pháp lý, thị trường sẽ có nhiều tiềm năng phát triển hơn", ông Đỗ Ngọc Quỳnh dự báo. Ngoài tín chỉ carbon, với tiềm năng điện tái tạo thứ tư thế giới theo McKenzie, ông cho rằng có thể khai thác việc vừa bán tín chỉ carbon vừa bán được REC. Theo VBMA, quy mô thị trường carbon bắt buộc toàn cầu đạt 104 tỷ USD năm ngoái, tăng 100% so với năm 2020. Trong khi, thị trường tự nguyện đã thu hẹp còn 800 triệu USD, giảm hai phần ba so với 2021 do một số vụ bê bối liên quan đến "giặt xanh" (green washing) làm ảnh hưởng đến uy tín, niềm tin. Theo dõi biến động của thị trường thế giới giúp các bên tham gia trong thị trường carbon tự nguyện còn sơ khai của Việt Nam rút kinh nghiệm và tìm ra hướng đi. Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS) văn phòng Hà Nội, dự báo người mua sẽ cần tìm kiếm các bên bán tín chỉ có hệ thống quản trị tốt và rõ ràng. Ông cho rằng người mua đang thiên về chuộng mua tín chỉ lĩnh vực giảm phát thải sản xuất vì dễ chứng minh. Một loại được quan tâm khác là "carbon xanh dương" (blue carbon) - tín chỉ tạo ra từ các dự án hấp thụ carbon của rừng ngập mặn, đầm lầy bãi triều và cỏ biển. Ông chỉ ra Việt Nam triển vọng với 200.000 ha rừng ngập mặn, có thể làm các dự án carbon tương tự như ở Honduras. Bà Thu Nguyễn, Quản lý chính sách tại Apanada Management Consultancy, Đại diện Viện Tài nguyên Thế giới (WRI) khuyến nghị các dự án tín chỉ carbon nâng cao giá trị bằng cách quan tâm đến tính bình đẳng và bao trùm. Theo đó, mục tiêu không chỉ là giảm phát thải mà còn là cải thiện đời sống người dân và phát triển bình đẳng hơn "Dự án cần bảo đảm có tham vấn của cộng đồng, đặc biệt là phụ nữ và các nhóm yếu thế, để tạo ra lợi ích cho cả cộng đồng lẫn nhà đầu tư", bà nói."
Đoạn 2: "Giá nhẫn trơn liên tục điều chỉnh, tăng gần một triệu đồng trong ngày và có nơi lên sát 89 triệu đồng một lượng. 15h ngày 23/10, giá mua bán nhẫn trơn được các thương hiệu kinh doanh điều chỉnh theo diễn biến đi lên của thế giới. Chiều nay, mỗi ounce vàng quốc tế tiếp tục thiết lập kỷ lục mới 2.755 USD. Giá nhẫn trơn tại Công ty Vàng bạc đá quý Sài Gòn (SJC) cũng tăng nửa triệu đồng so với đầu sáng và gần 1 triệu đồng so với cuối ngày hôm qua, lên 86,9 - 88,2 triệu đồng. Công ty Vàng bạc đá quý Phú Nhuận (PNJ) và Mi Hồng niêm yết giá nhẫn trơn quanh vùng 87,4 - 88,4 triệu đồng. Còn tại Tập đoàn Vàng bạc đá quý DOJI, giá mua bán nhẫn trơn cùng thời điểm thậm chí lên 88 - 88,9 triệu đồng một lượng. Trước đó đầu ngày, Công ty Vàng bạc đá quý Sài Gòn (SJC) đã tăng 300.000 đồng một lượng so với cuối ngày hôm qua, niêm yết giá nhẫn trơn tại 86,3 - 87,6 triệu đồng. Biểu giá mua bán nhẫn trơn tại Tập đoàn Vàng bạc đá quý DOJI lúc 9h sáng là 87 - 88 triệu đồng, tăng 200.000 đồng so với cuối ngày hôm qua. Nhẫn trơn giữ nhịp tăng liên tục trong 10 ngày qua. So với giữa tháng, mỗi lượng nhẫn trơn đã tăng hơn 5 triệu đồng. Còn so với đầu năm, nhẫn trơn tăng gần 25 triệu một lượng, tương đương hiệu suất 39%. Trong khi giá vàng miếng SJC đứng yên ở vùng 87 - 89 triệu một lượng, do Ngân hàng Nhà nước chưa thay đổi giá bán can thiệp. Thời điểm này là mùa cưới cuối năm và nhu cầu mua vàng nhẫn làm quà cưới tăng, song người dân không dễ để mua được mặt hàng này tại các thương hiệu lớn. Các thương hiệu lớn như DOJI, PNJ, Bảo Tín Minh Châu thường xuyên trong tình trạng cháy hàng. Khách lẻ chỉ may mắn mua được số lượng ít nếu cửa hàng vừa có khách bán ra. Còn tại SJC, các chi nhánh giới hạn lượng mua tối đa 5 phân đến 1 chỉ mỗi người. Trên thị trường quốc tế, mỗi ounce vàng trong 5 ngày qua tăng mạnh hơn 100 USD. Kim loại quý có thời điểm lên mức kỷ lục gần 2.750 USD, trước khi lùi về vùng 2.738 USD vào sáng nay. Quy đổi theo tỷ giá bán Vietcombank, giá vàng trong nước chênh lệch 3,5-5 triệu đồng một lượng so với thế giới. Theo dự báo của các nhà băng hàng đầu thế giới, giá vàng thế giới có thể lên 3.000 USD một ounce vào năm sau. Các chuyên gia khuyến nghị nhà đầu tư phân bổ tỷ trọng nhỏ danh mục vào kênh trú ẩn này, đặc biệt trong bối cảnh kim loại quý đã tăng mạnh thời gian qua."
Đoạn 3: "Nhu cầu trú ẩn khi căng thẳng địa chính trị leo thang kéo giá vàng lên mức đỉnh mới, tại 2.748 USD một ounce. Chốt phiên giao dịch 22/10, giá vàng thế giới giao ngay tăng gần 30 USD lên 2.748 USD một ounce. Đây là mức cao kỷ lục mới của kim loại quý. "Căng thẳng địa chính trị vẫn là nguyên nhân chủ yếu. Hai tuần nữa sẽ diễn ra bầu cử Tổng thống Mỹ và cuộc đua vẫn rất sát sao. Bất ổn chính trị đang kéo nhu cầu trú ẩn lên cao", Peter A. Grant - Phó giám đốc Zaner Metals nhận định trên Reuters. Giá vàng thế giới đảo chiều tăng mạnh trong phiên 22/10. Đồ thị: Kitco Giá vàng thế giới đảo chiều tăng mạnh trong phiên 22/10. Đồ thị: Kitco Cuộc thăm dò mới nhất của Reuters/Ipsos cho thấy tỷ lệ ủng hộ Phó tổng thống Kamala Harris hiện là 46%, nhỉnh hơn so với 43% của cựu Tổng thống Donald Trump. "Sự sát sao này đang tạo nên tình trạng thiếu chắc chắn. Môi trường này có lợi cho vàng", các nhà phân tích tại ngân hàng BNP Paribas nhận định. Grant dự báo nếu căng thẳng tại Trung Đông tiếp tục tăng nhiệt, giá có thể lên 3.000 USD cuối năm nay. Từ đầu năm, giá đã tăng 33% và liên tiếp lập đỉnh mới. Một yếu tố khác đang hỗ trợ kim loại quý là làn sóng giảm lãi suất của các ngân hàng trung ương lớn trên toàn cầu. Mỹ, châu Âu, Trung Quốc cùng hàng loạt nền kinh tế khác đã giảm lãi suất năm nay để hỗ trợ nền kinh tế. Trong khi đó, tại Wall Street, các chỉ số chính gần như đứng yên. Nhà đầu tư hiện theo dõi lợi suất trái phiếu chính phủ Mỹ và chờ đánh giá thêm báo cáo tài chính của các doanh nghiệp. Ngoài vàng, các kim loại quý khác cũng tăng giá. Bạc lập đỉnh 12 năm, khi tăng 3,2% lên gần 35 USD một ounce. Han Tan - chiến lược gia thị trường tại Exinity Group dự báo bạc vượt mốc 35 USD trước khi cuộc bầu cử diễn ra. Bạch kim đắt thêm 2,8% lên 1.031 USD một ounce. Palladium tăng 2,9% lên 1.081 USD."
'''},
    {"role": "user", "content": '''giá nhẫn trơn hôm nay là bao nhiêu?'''}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=128) 
print(tokenizer.decode(outputs[0]))

# Giá nhẫn trơn hôm nay là 86,9 - 88,2 triệu đồng.

```

<h5> Answer with bot persona</h5>

```python
messages =  [
    {"role": "system", "content": '''Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.
Nếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác, vui lòng không chia sẻ thông tin sai lệch.
Context:
Đoạn 0: "Chính phủ đề xuất bổ sung gần 20.700 tỷ đồng vốn điều lệ cho Ngân hàng Ngoại thương Việt Nam (Vietcombank) từ cổ tức bằng cổ phiếu được chia của cổ đông Nhà nước. Chiều 23/10, thừa ủy quyền Chính phủ, Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc trình Quốc hội về bổ sung vốn Nhà nước tại Ngân hàng Ngoại Thương Việt Nam (Vietcombank). Theo đó, Chính phủ đề nghị tăng vốn điều lệ cho ngân hàng này gần 20.700 tỷ đồng từ cổ tức bằng cổ phiếu được chia của cổ đông Nhà nước. Số tiền này lấy từ nguồn lợi nhuận còn lại lũy kế đến hết năm 2018 và lãi còn lại năm 2021. Vốn điều lệ dự kiến rót thêm cho Vietcombank gần bằng lợi nhuận hợp nhất trước thuế nửa đầu năm nay của nhà băng này. Việc bổ sung vốn cho "ông lớn" ngân hàng quốc doanh được Phó thủ tướng nhấn mạnh là cấp thiết để duy trì tỷ lệ vốn góp Nhà nước, phù hợp chiến lược phát triển kinh tế xã hội, tạo nguồn lực hỗ trợ ngân hàng yếu kém. Phó thủ tướng cho biết, phần lợi nhuận còn lại lũy kế hết năm 2018 và lãi còn lại 2021 hiện được hạch toán theo dõi tại VCB, chưa nằm trong cân đối ngân sách Nhà nước. Do vậy, nguồn vốn đề xuất tăng cho ngân hàng này không ảnh hưởng tới kế hoạch dự toán thu chi ngân sách 2024-2025. Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc đọc tờ trình bổ sung vốn cho Vietcombank, ngày 23/10. Ảnh: Trung tâm báo chí Quốc hội Phó thủ tướng, Bộ trưởng Tài chính Hồ Đức Phớc đọc tờ trình bổ sung vốn cho Vietcombank, ngày 23/10. Ảnh: Trung tâm báo chí Quốc hội Vốn điều lệ của Vietcombank hiện là 55.891 tỷ đồng, thấp hơn nhiều so với VPBank (79.339 tỷ đồng), Techcombank (70.450 tỷ đồng) và không có sự cách biệt lớn so với một số ngân hàng thương mại cổ phần như MB (52.871) tỷ đồng, ACB (44.667 tỷ đồng) và SHB (36.629 tỷ đồng). Ngoài ra, việc tăng vốn nhằm để ngân hàng này đáp ứng các tỷ lệ an toàn tối thiểu. Tính tới cuối 2023, tỷ lệ an toàn vốn (CAR) của ngân hàng này là 11,05%, đảm bảo quy định. Tuy nhiên, mức này thấp hơn các ngân hàng thương mại cổ phần (VPBank, MB là 12-13%; Techcombank 13-15%...) và các nhà băng trong khu vực (Singapore là 17,1%, Indonesia 23,27%...). Thẩm tra nội dung này, Chủ nhiệm Ủy ban Kinh tế Vũ Hồng Thanh cho rằng đề xuất tăng vốn cho Vietcombank bảo đảm cơ sở pháp lý và đúng thẩm quyền theo quy định. Tuy nhiên, Ủy ban Kinh tế đề nghị Chính phủ lấy ý kiến của cổ đông chiến lược nước ngoài Ngân hàng Mizuho Corporate Bank - đơn vị nắm 15% vốn điều lệ của Vietcombank. Việc này nhằm thuận lợi trong quá trình tăng vốn. Chính phủ cũng cần bổ sung thông tin hiện trạng vốn của Vietcombank so với các ngân hàng thương mại trong hệ thống hiện nay. "Có ý kiến đề nghị làm rõ nhận định nguồn vốn đề xuất để tăng vốn điều lệ không tác động đến ngân sách Nhà nước", ông Thanh cho biết. Trụ sở Ngân hàng Ngoại thương Việt Nam (Vietcombank). Ảnh: VCB Trụ sở Ngân hàng Ngoại thương Việt Nam (Vietcombank). Ảnh: VCB Chủ nhiệm Ủy ban Kinh tế Vũ Hồng Thanh đề nghị Chính phủ chỉ đạo Ngân hàng Nhà nước cùng các bộ, ngành liên quan xử lý phần lợi nhuận còn lại năm 2022, 2023 (lần lượt là 21.680 tỷ và 25.009 tỷ đồng), nhằm tăng năng lực tài chính cho Vietcombank, bù đắp mức thiếu hụt vốn tự có, bảo đảm an toàn hoạt động. Cơ quan thẩm tra lưu ý vốn được bổ sung cho Vietcombank cần được dùng để mở rộng kinh doanh, cung ứng tín dụng với các lĩnh vực, dự án quan trọng quốc gia quy mô lớn, giảm lãi suất cho vay, cũng như đổi mới mô hình quản trị, chất lượng dịch vụ của nhà băng này. "Chính phủ cần đánh giá kỹ tác động việc bổ sung vốn Nhà nước cho Vietcombank tới phát triển của ngành ngân hàng, hiệu quả kinh tế xã hội", Ủy ban Kinh tế lưu ý. Vietcombank là một trong 4 ngân hàng thương mại Nhà nước, bên cạnh BIDV, VietinBank và Agribank. Ngân hàng này do Nhà nước sở hữu 74,8% vốn điều lệ. Lũy kế nửa đầu năm nay, lợi nhuận hợp nhất trước thuế của nhà băng này đạt 20.835 tỷ đồng, tăng 1,6% so với cùng kỳ 2023. Với dữ liệu này, Vietcombank tiếp tục đứng đầu toàn hệ thống ngân hàng về lợi nhuận 6 tháng đầu năm. Đây cũng là mức lãi nửa đầu năm cao kỷ lục của nhà băng này. Tính đến 30/6, tổng tài sản của ngân hàng đạt hơn 1,9 triệu tỷ đồng, tăng 3,6% so với cuối 2023. Trong đó, cho vay khách hàng gần 1,37 triệu tỷ đồng, tăng 7,8%."
Đoạn 1: "Đã có vài đơn vị bán tín chỉ carbon cho khách ngoại nhưng còn thiếu cơ sở pháp lý để đảm bảo hoạt động được thuận lợi, theo chuyên gia. Thông tin tại phiên tọa đàm thuộc Diễn đàn và Triển lãm Kinh tế xanh 2024 (GEFE), ông Đỗ Ngọc Quỳnh, Tổng thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA), cho biết thị trường tín chỉ carbon tự nguyện Việt Nam đã có một số đơn vị bán được tín chỉ carbon cho nhà đầu tư, tập đoàn nước ngoài. "Họ đang mua chứng chỉ carbon và chứng chỉ năng lượng tái tạo (REC) trong tiêu chí RE100, tức 100% năng lượng tái tạo", ông cho biết. RE100 là sáng kiến toàn cầu dành cho các công ty cam kết sử dụng 100% điện năng tái tạo, phát động bởi Climate Group và CDP vào 2014. Từ trái sang, Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS Hà Nội) và ông Đỗ Ngọc Quỳnh, Tổng Thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA) nói tại tọa đàm. Ảnh: GEFE 2024 Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS Hà Nội) và ông Đỗ Ngọc Quỳnh, Tổng Thư ký Hiệp hội Thị trường Trái phiếu Việt Nam (VBMA) chia sẻ tại tọa đàm. Ảnh: GEFE 2024 Thị trường carbon gồm hai hình thức là bắt buộc và tự nguyện. Đồ họa: Dỹ Tùng Phân biệt các loại thị trường carbon. Đồ họa: Dỹ Tùng Theo kế hoạch của chính phủ, thị trường bắt buộc sẽ vận hành thử nghiệm vào giai đoạn 2025-2028. Với thị trường tự nguyện, ông Quỳnh cho biết đã bắt đầu hình thành và cũng biến động theo diễn biến xu hướng chung toàn cầu. Chuyên gia VBMA cho rằng Việt Nam đã có chính sách chung để thực hiện cam kết Net Zero vào 2050, nhưng vẫn chưa có pháp lý đầy đủ và rõ ràng cho thị trường carbon tự nguyện. "Những người bán tại Việt Nam sau giao dịch không biết hạch toán vào đâu, nộp thuế thế nào. Một số chọn phương án tính vào thu nhập bất thường để khai thuế", ông ví dụ. Ông Nguyễn Thành Nghiệp, Luật sư thành viên công ty luật VTN và Cộng sự chỉ ra việc chưa có quy định xác định tính chất tài sản của tín chỉ carbon. "Chúng có được xem là tài sản bình thường, được thế chấp hay giao dịch thế nào chưa có đủ căn cứ pháp lý", ông nói. Ngoài ra, quy trình MRV (đo lường, báo cáo và kiểm chứng) cũng cần quy định, hướng dẫn rõ. Theo ông, ngoài các cơ quan quản lý, khu vực tư nhân cũng trông chờ xem liệu có thể tham gia hoạt động MRV không. "Trong thời gian tới, nếu hoàn thiện pháp lý, thị trường sẽ có nhiều tiềm năng phát triển hơn", ông Đỗ Ngọc Quỳnh dự báo. Ngoài tín chỉ carbon, với tiềm năng điện tái tạo thứ tư thế giới theo McKenzie, ông cho rằng có thể khai thác việc vừa bán tín chỉ carbon vừa bán được REC. Theo VBMA, quy mô thị trường carbon bắt buộc toàn cầu đạt 104 tỷ USD năm ngoái, tăng 100% so với năm 2020. Trong khi, thị trường tự nguyện đã thu hẹp còn 800 triệu USD, giảm hai phần ba so với 2021 do một số vụ bê bối liên quan đến "giặt xanh" (green washing) làm ảnh hưởng đến uy tín, niềm tin. Theo dõi biến động của thị trường thế giới giúp các bên tham gia trong thị trường carbon tự nguyện còn sơ khai của Việt Nam rút kinh nghiệm và tìm ra hướng đi. Marco Gaspari, Điều phối viên Ngành Môi trường tại Cơ quan Hợp tác Phát triển Italy (AICS) văn phòng Hà Nội, dự báo người mua sẽ cần tìm kiếm các bên bán tín chỉ có hệ thống quản trị tốt và rõ ràng. Ông cho rằng người mua đang thiên về chuộng mua tín chỉ lĩnh vực giảm phát thải sản xuất vì dễ chứng minh. Một loại được quan tâm khác là "carbon xanh dương" (blue carbon) - tín chỉ tạo ra từ các dự án hấp thụ carbon của rừng ngập mặn, đầm lầy bãi triều và cỏ biển. Ông chỉ ra Việt Nam triển vọng với 200.000 ha rừng ngập mặn, có thể làm các dự án carbon tương tự như ở Honduras. Bà Thu Nguyễn, Quản lý chính sách tại Apanada Management Consultancy, Đại diện Viện Tài nguyên Thế giới (WRI) khuyến nghị các dự án tín chỉ carbon nâng cao giá trị bằng cách quan tâm đến tính bình đẳng và bao trùm. Theo đó, mục tiêu không chỉ là giảm phát thải mà còn là cải thiện đời sống người dân và phát triển bình đẳng hơn "Dự án cần bảo đảm có tham vấn của cộng đồng, đặc biệt là phụ nữ và các nhóm yếu thế, để tạo ra lợi ích cho cả cộng đồng lẫn nhà đầu tư", bà nói."
Đoạn 2: "Giá nhẫn trơn liên tục điều chỉnh, tăng gần một triệu đồng trong ngày và có nơi lên sát 89 triệu đồng một lượng. 15h ngày 23/10, giá mua bán nhẫn trơn được các thương hiệu kinh doanh điều chỉnh theo diễn biến đi lên của thế giới. Chiều nay, mỗi ounce vàng quốc tế tiếp tục thiết lập kỷ lục mới 2.755 USD. Giá nhẫn trơn tại Công ty Vàng bạc đá quý Sài Gòn (SJC) cũng tăng nửa triệu đồng so với đầu sáng và gần 1 triệu đồng so với cuối ngày hôm qua, lên 86,9 - 88,2 triệu đồng. Công ty Vàng bạc đá quý Phú Nhuận (PNJ) và Mi Hồng niêm yết giá nhẫn trơn quanh vùng 87,4 - 88,4 triệu đồng. Còn tại Tập đoàn Vàng bạc đá quý DOJI, giá mua bán nhẫn trơn cùng thời điểm thậm chí lên 88 - 88,9 triệu đồng một lượng. Trước đó đầu ngày, Công ty Vàng bạc đá quý Sài Gòn (SJC) đã tăng 300.000 đồng một lượng so với cuối ngày hôm qua, niêm yết giá nhẫn trơn tại 86,3 - 87,6 triệu đồng. Biểu giá mua bán nhẫn trơn tại Tập đoàn Vàng bạc đá quý DOJI lúc 9h sáng là 87 - 88 triệu đồng, tăng 200.000 đồng so với cuối ngày hôm qua. Nhẫn trơn giữ nhịp tăng liên tục trong 10 ngày qua. So với giữa tháng, mỗi lượng nhẫn trơn đã tăng hơn 5 triệu đồng. Còn so với đầu năm, nhẫn trơn tăng gần 25 triệu một lượng, tương đương hiệu suất 39%. Trong khi giá vàng miếng SJC đứng yên ở vùng 87 - 89 triệu một lượng, do Ngân hàng Nhà nước chưa thay đổi giá bán can thiệp. Thời điểm này là mùa cưới cuối năm và nhu cầu mua vàng nhẫn làm quà cưới tăng, song người dân không dễ để mua được mặt hàng này tại các thương hiệu lớn. Các thương hiệu lớn như DOJI, PNJ, Bảo Tín Minh Châu thường xuyên trong tình trạng cháy hàng. Khách lẻ chỉ may mắn mua được số lượng ít nếu cửa hàng vừa có khách bán ra. Còn tại SJC, các chi nhánh giới hạn lượng mua tối đa 5 phân đến 1 chỉ mỗi người. Trên thị trường quốc tế, mỗi ounce vàng trong 5 ngày qua tăng mạnh hơn 100 USD. Kim loại quý có thời điểm lên mức kỷ lục gần 2.750 USD, trước khi lùi về vùng 2.738 USD vào sáng nay. Quy đổi theo tỷ giá bán Vietcombank, giá vàng trong nước chênh lệch 3,5-5 triệu đồng một lượng so với thế giới. Theo dự báo của các nhà băng hàng đầu thế giới, giá vàng thế giới có thể lên 3.000 USD một ounce vào năm sau. Các chuyên gia khuyến nghị nhà đầu tư phân bổ tỷ trọng nhỏ danh mục vào kênh trú ẩn này, đặc biệt trong bối cảnh kim loại quý đã tăng mạnh thời gian qua."
Đoạn 3: "Nhu cầu trú ẩn khi căng thẳng địa chính trị leo thang kéo giá vàng lên mức đỉnh mới, tại 2.748 USD một ounce. Chốt phiên giao dịch 22/10, giá vàng thế giới giao ngay tăng gần 30 USD lên 2.748 USD một ounce. Đây là mức cao kỷ lục mới của kim loại quý. "Căng thẳng địa chính trị vẫn là nguyên nhân chủ yếu. Hai tuần nữa sẽ diễn ra bầu cử Tổng thống Mỹ và cuộc đua vẫn rất sát sao. Bất ổn chính trị đang kéo nhu cầu trú ẩn lên cao", Peter A. Grant - Phó giám đốc Zaner Metals nhận định trên Reuters. Giá vàng thế giới đảo chiều tăng mạnh trong phiên 22/10. Đồ thị: Kitco Giá vàng thế giới đảo chiều tăng mạnh trong phiên 22/10. Đồ thị: Kitco Cuộc thăm dò mới nhất của Reuters/Ipsos cho thấy tỷ lệ ủng hộ Phó tổng thống Kamala Harris hiện là 46%, nhỉnh hơn so với 43% của cựu Tổng thống Donald Trump. "Sự sát sao này đang tạo nên tình trạng thiếu chắc chắn. Môi trường này có lợi cho vàng", các nhà phân tích tại ngân hàng BNP Paribas nhận định. Grant dự báo nếu căng thẳng tại Trung Đông tiếp tục tăng nhiệt, giá có thể lên 3.000 USD cuối năm nay. Từ đầu năm, giá đã tăng 33% và liên tiếp lập đỉnh mới. Một yếu tố khác đang hỗ trợ kim loại quý là làn sóng giảm lãi suất của các ngân hàng trung ương lớn trên toàn cầu. Mỹ, châu Âu, Trung Quốc cùng hàng loạt nền kinh tế khác đã giảm lãi suất năm nay để hỗ trợ nền kinh tế. Trong khi đó, tại Wall Street, các chỉ số chính gần như đứng yên. Nhà đầu tư hiện theo dõi lợi suất trái phiếu chính phủ Mỹ và chờ đánh giá thêm báo cáo tài chính của các doanh nghiệp. Ngoài vàng, các kim loại quý khác cũng tăng giá. Bạc lập đỉnh 12 năm, khi tăng 3,2% lên gần 35 USD một ounce. Han Tan - chiến lược gia thị trường tại Exinity Group dự báo bạc vượt mốc 35 USD trước khi cuộc bầu cử diễn ra. Bạch kim đắt thêm 2,8% lên 1.031 USD một ounce. Palladium tăng 2,9% lên 1.081 USD."
'''},
    {"role": "user", "content": '''Hãy trả lời câu hỏi sau dựa vào đoạn ngữ cảnh được cung cấp. Câu trả lời phải có thưa gửi rõ ràng, xưng là em và kính thưa quý khách.\nCâu hỏi: giá nhẫn trơn hôm nay là bao nhiêu?'''}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=512) 
print(tokenizer.decode(outputs[0]))

# Em xin thông báo rằng giá nhẫn trơn hôm nay dao động từ 86,9 đến 88,2 triệu đồng một ounce, tùy thuộc vào từng thương hiệu.

```

***You can customize the prompt before the answer to get a response that suits your needs.***
***You can also add information about this bot's persona in the system prompt.***

<h4> 3. Function Calling task </h4>

***In this task, we are following the Function Calling template from Glaive AI: [glaiveai/glaive-function-calling-v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2).***

```python

messages =  [
    {"role": "system", "content": '''Bạn là một trợ lý hữu ích với khả năng truy cập vào các hàm sau. Hãy sử dụng chúng nếu cần -
{
    "name": "weather_forecast",
    "description": "Cung cấp cập nhật và dự báo thời tiết cho các địa điểm cụ thể, bao gồm nhiệt độ, độ ẩm và tình trạng thời tiết. Ví dụ: thời tiết hôm nay, dự báo thời tiết ở Hà Nội, nhiệt độ tại Đà Nẵng, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
},
{
    "name": "news_update",
    "description": "Cung cấp các bài báo và cập nhật tin tức mới nhất trên nhiều lĩnh vực như chính trị, công nghệ, thể thao và giải trí. Ví dụ: tin tức hôm nay, cập nhật thể thao, tin công nghệ mới nhất, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
},
{
    "name": "recipe_search",
    "description": "Tìm kiếm và gợi ý công thức nấu ăn dựa trên nguyên liệu hoặc sở thích dinh dưỡng. Ví dụ: công thức món ăn với gà, món chay, ăn kiêng, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
},
{
    "name": "movie_recommendation",
    "description": "Cung cấp gợi ý phim dựa trên thể loại, tâm trạng hoặc tiêu đề cụ thể. Ví dụ: phim hài hay, phim hành động mới, gợi ý phim cho tối nay, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
},
{
    "name": "fitness_advice",
    "description": "Cung cấp mẹo và bài tập cho sức khỏe và thể dục dựa trên mục tiêu của người dùng. Ví dụ: bài tập giảm cân, lịch tập gym cho người mới, lời khuyên về dinh dưỡng, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
},
{
    "name": "travel_planner",
    "description": "Hỗ trợ lập kế hoạch du lịch, bao gồm gợi ý lịch trình, mẹo đặt vé và thông tin về điểm đến. Ví dụ: lên kế hoạch du lịch Đà Nẵng, địa điểm tham quan ở Nha Trang, mẹo du lịch Nhật Bản, v.v.",
    "parameters": {
        "properties": {
            "__arg1": {
                "description": "__arg1",
                "type": "string"
            }
        },
        "required": [
            "__arg1"
        ],
        "type": "object"
    }
}'''},
    {"role": "user", "content": "hôm nay có tin tức gì về ô nhiễm không khí"}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=128) 
print(tokenizer.decode(outputs[0]))

# <functioncall> {"name": "news_update", "arguments": {"__arg1": "ô nhiễm không khí"}}

```

<h4> 4. Question Rewriting task </h4>

```python

messages =  [
    {"role": "system", "content": '''Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể, đồng thời giữ an toàn.\nNếu một câu hỏi không có ý nghĩa hoặc không hợp lý về mặt thông tin, hãy giải thích tại sao thay vì trả lời một điều gì đó không chính xác, vui lòng không chia sẻ thông tin sai lệch.
Context:
USER: Concert "Anh trai vượt ngàn chông gai" diễn ra ở đâu?
ASSISTANT: Đêm concert Anh trai vượt ngàn chông gai diễn ra vào tối 19-10, tại công viên bờ sông Sài Gòn, TP.HCM với sự tham dự của khoảng 20.000 khán giả.
USER: Buổi biểu diễn có bao nhiêu nghệ sĩ?
ASSISTANT: Danh sách nghệ sĩ gồm 17 nghệ sĩ: Kay Trần, Jun Phạm, Cường Seven, Tự Long, (S)TRONG Trọng Hiếu, S.T Sơn Thạch, BB Trần, Bùi Công Nam, Rhymastic, Soobin Hoàng Sơn, Binz, Quốc Thiên, Thanh Duy, Bằng Kiều, Tiến Luật, Đinh Tiến Đạt và Đỗ Hoàng Hiệp.
USER: Chương trình phát sóng khi nào và ở đâu?
ASSISTANT: chương trình phát sóng từ ngày 29 tháng 6 năm 2024 lúc 20:00 thứ 7 hàng tuần trên VTV3 và công chiếu lúc 20:30 cùng ngày trên kênh YouTube YeaH1 Show của nhà sản xuất chương trình.'''},
    {"role": "user", "content": '''Dựa vào đoạn hội thoại được cung cấp, viết lại câu nói của người dùng sao cho đầu đủ ý nhất có thể mà không bị sai lệch thông tin.
Câu nói: Concert này có tổ chức ở Hà Nội không?
    '''}]
tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")

outputs = model.generate(tokenized_chat, max_new_tokens=512) 
print(tokenizer.decode(outputs[0]))

# Buổi hòa nhạc Anh trai vượt ngàn chông gai có diễn ra ở Hà Nội không?

```

***Modify the parameters "temperature", "top_k", "top_p" to suit your usecase.***

Corresponding Author:
+ phamhuuhai1402@gmail.com