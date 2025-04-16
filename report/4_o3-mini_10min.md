Dưới đây là một báo cáo siêu chi tiết cho Chương 3 của Đồ án Thạc sĩ, tập trung vào xây dựng mô hình tìm kiếm và truy vấn thông tin liên quan đến môn học Luật biển và Quy tắc tránh va quốc tế của Trường Cao đẳng Kỹ thuật Hải quân. Báo cáo này bao gồm các phần sau:

---

# CHƯƠNG 3: XÂY DỰNG MÔ HÌNH TÌM KIẾM VÀ TRUY VẤN THÔNG TIN LIÊN QUAN ĐẾN MÔN HỌC LUẬT BIỂN VÀ QUY TẮC TRÁCH VA QUỐC TẾ CỦA TRƯỜNG CAO ĐẲNG KỸ THUẬT HẢI QUÂN

## 3.1. Giới thiệu tổng quan, phân tích một số thành phần trong mô hình

### 3.1.1. Tổng quan về hệ thống  
Hệ thống được xây dựng nhằm mục đích hỗ trợ truy vấn thông tin liên quan đến môn học Luật biển và các quy tắc tránh va quốc tế. Mô hình sử dụng phương pháp tích hợp giữa tìm kiếm theo vector (vector search) và truy vấn ngữ nghĩa (semantic retrieval) thông qua kỹ thuật Retrieval Augmented Generation (RAG). Các thành phần chính của hệ thống bao gồm:  
- **Cơ sở dữ liệu vector:** Dùng để lưu trữ các embedding được tạo ra từ dữ liệu văn bản (ví dụ như các câu hỏi – đáp án về luật biển)  
- **Quy trình tạo embedding:** Áp dụng các mô hình chuyển đổi ngôn ngữ (như sentence-transformers) để chuyển đổi văn bản thành các vector đại diện  
- **API backend:** Được triển khai bằng FastAPI, xử lý yêu cầu từ phía client, thực hiện truy vấn dựa trên hai phương án: (a) tìm kiếm chính xác (exact match) và (b) tìm kiếm ngữ nghĩa (semantic search) với Qdrant, sau đó gọi OpenAI để tạo phản hồi nếu cần  
- **Giao diện người dùng (frontend):** Xây dựng bằng React với các trang như HomePage, ChatBot, FAQPage và IssuePage. Ngoài ra, việc quản lý người dùng, xác thực và định tuyến (ProtectedRoute) được xử lý qua Context API để đảm bảo bảo mật và trải nghiệm người dùng mượt mà.

### 3.1.2. Phân tích các thành phần chính  
- **Xử lý dữ liệu:**  
  Dữ liệu đầu vào bao gồm file Excel chứa cặp câu hỏi – đáp án và các file văn bản (txt) được chia nhỏ thành các đoạn. Qua đó, dữ liệu được tạo thành các đối tượng Document có cấu trúc gồm nội dung trang (page_content) và thông tin metadata (nguồn, câu hỏi, …).  
- **Mô hình embedding:**  
  Sử dụng mô hình “sentence-transformers/paraphrase-multilingual-mpnet-base-v2” để tạo embedding cho từng tài liệu. Embedding giúp chuyển văn bản sang dạng vector, cho phép tính toán khoảng cách và điểm tương đồng giữa các văn bản.  
- **Vector Database với Qdrant:**  
  Qdrant được chọn làm nền tảng lưu trữ vector nhờ khả năng truy vấn nhanh và linh hoạt. Hệ thống tạo collection lưu trữ các vector tương ứng với nội dung và metadata của từng tài liệu.  
- **Mô hình API và xử lý truy vấn:**  
  API backend có chức năng:
  - **Tìm kiếm chính xác:** Sử dụng filter để xác định các câu hỏi trùng khớp hoàn toàn với truy vấn của người dùng.
  - **Tìm kiếm ngữ nghĩa:** Khi không có kết quả chính xác, hệ thống tính toán embedding cho câu hỏi của người dùng và truy vấn trong Qdrant để tìm các tài liệu có độ tương đồng cao. Nếu điểm số tương đồng vượt qua ngưỡng đặt trước, hệ thống có thể trả về kết quả trực tiếp hoặc kết hợp với LLM (OpenAI) để tạo ra phản hồi tự động.
- **Giao diện người dùng:**  
  Frontend được xây dựng theo triết lý component-based:
  - **NavBar.jsx:** Điều hướng giữa các trang chính với chức năng chuyển đổi theme.
  - **ProtectedRoute.jsx:** Bảo đảm các trang cần đăng nhập mới có thể truy cập được.
  - **ChatBot.jsx:** Giao diện trò chuyện với người dùng, hiển thị lịch sử hội thoại và xử lý việc gửi yêu cầu/nhận phản hồi.
  - **FAQPage.jsx, HomePage.jsx và IssuePage.jsx:** Cung cấp thông tin, trợ giúp và thu thập phản hồi của người dùng.

---

## 3.2. Xây dựng các thành phần của mô hình

### 3.2.1. Thiết kế kiến trúc tổng thể  
Mô hình được chia thành ba tầng chính:
- **Tầng Dữ liệu (Data Layer):**  
  Bao gồm việc thu thập, tiền xử lý và lưu trữ dữ liệu văn bản. Các công cụ như Pandas được sử dụng để đọc file Excel; dữ liệu sau đó được chuyển đổi thành các đối tượng Document có cấu trúc thống nhất.
- **Tầng Xử lý (Processing Layer):**  
  Các bước tính toán embedding, xây dựng và lưu trữ vector trong Qdrant. Tầng này cũng bao gồm việc xác thực thông qua file .env, cấu hình API client (OpenAI, Qdrant, và HuggingFace).  
- **Tầng Ứng dụng (Application Layer):**  
  API backend được triển khai bằng FastAPI, xử lý các yêu cầu truy vấn, lựa chọn phương án tìm kiếm (chính xác hay ngữ nghĩa) và phản hồi cho người dùng. Đồng thời, giao diện người dùng (React) tương tác với API backend thông qua các endpoint đã được thiết kế.

### 3.2.2. Chi tiết xây dựng từng thành phần

#### a. Tiền xử lý và tạo embedding  
- **Đọc dữ liệu:**  
  Sử dụng Python và Pandas để đọc dữ liệu từ file Excel (các cột “Câu hỏi” và “Đáp án”) và tách nội dung của các file text thành các đoạn dựa trên ký tự xuống dòng đôi.
- **Tạo Document objects:**  
  Mỗi tài liệu được biến đổi thành đối tượng có cấu trúc JSON với trường `page_content` và `metadata`. Đây là bước quan trọng giúp sau này dễ dàng truy xuất thông tin khi truy vấn.
- **Embedding generation:**  
  Sử dụng thư viện `langchain_community.embeddings` với mô hình HuggingFace để chuyển đổi văn bản thành các vector có kích thước cố định. Vector được tạo sẽ được lưu vào Qdrant qua phương thức `from_documents`.

#### b. Xây dựng vector database với Qdrant  
- **Cấu hình kết nối:**  
  Sử dụng các biến môi trường (như QDRANT_URL, QDRANT_API_KEY và COLLECTION_NAME) để thiết lập kết nối đến Qdrant.  
- **Thao tác dữ liệu:**  
  Thực hiện các thao tác như kiểm tra sự tồn tại của collection, thêm vector document và thực hiện truy vấn thông qua API của Qdrant.  
- **Test kết nối:**  
  Một file test (test_qdrant_connection.py) được xây dựng để xác nhận rằng kết nối và thao tác với Qdrant được thực hiện thành công.

#### c. Xây dựng API backend bằng FastAPI  
- **Khởi tạo dịch vụ:**  
  Ứng dụng FastAPI được khởi tạo với các endpoint:  
  - `/v1/chat/completions`: Xử lý các yêu cầu chat. Trước tiên, thực hiện tìm kiếm chính xác. Nếu không có kết quả, sử dụng semantic search rồi gọi OpenAI để sinh phản hồi.  
  - `/health`: Endpoint kiểm tra tình trạng hoạt động của các thành phần (embeddings, Qdrant, OpenAI).
- **Xử lý truy vấn:**  
  Các hàm `search_exact` và `search_semantic` được triển khai để thực hiện các loại truy vấn khác nhau. Ngoài ra, quy trình xử lý và truyền dữ liệu giữa các thành phần được log bằng logger để dễ dàng theo dõi và gỡ lỗi.
- **Tích hợp LLM:**  
  Nếu không có kết quả từ truy vấn nội bộ, OpenAI API (hoặc các LLM khác) được gọi với ngữ cảnh được tổng hợp từ các tài liệu liên quan.

#### d. Xây dựng giao diện người dùng với React  
- **Routing và cấu trúc trang:**  
  Sử dụng React Router, các trang chính (HomePage, ChatBot, FAQPage, IssuePage, Login) được định tuyến hợp lý.  
- **Định hướng bảo mật:**  
  ProtectedRoute.jsx kiểm tra trạng thái đăng nhập của người dùng thông qua Context API và cho phép truy cập hoặc điều hướng đến trang đăng nhập nếu chưa đăng nhập.
- **Giao diện chat và lịch sử:**  
  ChatBot.jsx cung cấp giao diện chat tương tác với API backend, xử lý việc gửi yêu cầu, hiển thị phản hồi từ hệ thống và quản lý lịch sử chat. Các thành phần khác như NavBar.jsx cung cấp tính năng chuyển đổi theme, điều hướng giữa các trang và hiển thị thông tin người dùng (bao gồm cả avatar và email).
- **Tính năng feedback và báo lỗi:**  
  IssuePage.jsx cung cấp một giao diện để người dùng gửi góp ý hoặc báo lỗi, với chức năng hiển thị modal xác nhận (sử dụng EmailJS có thể được kích hoạt để gửi email thông báo).

---

## 3.3. Đánh giá kết quả thực hiện thông qua thực nghiệm

### 3.3.1. Phương pháp đánh giá  
- **Chất lượng truy xuất thông tin:**  
  Thực hiện các truy vấn cụ thể và so sánh kết quả trả về giữa tìm kiếm chính xác và tìm kiếm ngữ nghĩa. Qua đó đánh giá độ chính xác và tính liên quan của các tài liệu được truy xuất.  
- **Thời gian phản hồi:**  
  Ghi nhận thời gian phản hồi của hệ thống với các truy vấn đơn giản và truy vấn cần suy luận phức tạp. Ví dụ, một số truy vấn đơn giản trả về kết quả trong khoảng 500ms, trong khi các truy vấn phức tạp có thể mất từ 8 đến 12 giây.
- **Phản hồi người dùng:**  
  Sử dụng feedback từ người dùng thông qua giao diện IssuePage và khảo sát nội bộ để đánh giá mức độ hài lòng với câu trả lời cũng như trải nghiệm tương tác của hệ thống.

### 3.3.2. Kết quả và phân tích  
- **Trích xuất kết quả tìm kiếm:**  
  Qua các thực nghiệm, các kết quả trả về từ tìm kiếm chính xác cho thấy sự khớp hoàn toàn với câu hỏi ban đầu, trong khi tìm kiếm ngữ nghĩa cung cấp các tài liệu có độ liên quan cao trong trường hợp không có kết quả chính xác.  
- **Hiệu năng xử lý:**  
  Đánh giá chỉ số thời gian phản hồi cho thấy hệ thống có hiệu năng xử lý tốt đối với các truy vấn đơn giản, nhưng cũng cần tối ưu thêm ở phần truy vấn ngữ nghĩa và gọi API LLM để giảm thời gian chờ của người dùng.
- **Những bất cập và góp ý cải tiến:**  
  Một số truy vấn có thể không trả về tài liệu liên quan do dữ liệu đầu vào có tính chất đa dạng. Việc tinh chỉnh ngưỡng điểm tương đồng và cải tiến quy trình tiền xử lý dữ liệu có thể giúp nâng cao chất lượng phản hồi.

---

## 3.4. Các vấn đề cần chú ý trong việc ứng dụng thực tế

### 3.4.1. Quản lý và tối ưu hóa dữ liệu  
- **Độ chính xác của dữ liệu:**  
  Đảm bảo rằng dữ liệu đầu vào (các cặp câu hỏi – đáp án, file văn bản) được tiền xử lý sạch sẽ, chuẩn hóa ngôn ngữ, và không có lỗi chính tả để mô hình embedding có thể hoạt động hiệu quả.
- **Cập nhật và bảo trì cơ sở dữ liệu vector:**  
  Các vector document cần được cập nhật định kỳ để phản ánh những thay đổi và bổ sung thông tin mới liên quan đến môn học.

### 3.4.2. Hiệu năng và tối ưu hóa hệ thống  
- **Tối ưu hóa thời gian phản hồi:**  
  Tối ưu hóa việc tính toán embedding và truy vấn Qdrant bằng cách điều chỉnh cấu hình API và áp dụng caching đối với các truy vấn thường gặp.  
- **Tối ưu hóa các cuộc gọi tới LLM:**  
  Giảm thiểu số lần gọi API từ OpenAI thông qua việc xác định rõ ràng ngưỡng trả về kết quả từ vector search trước khi gọi mô hình sinh câu trả lời.

### 3.4.3. Vấn đề bảo mật và xác thực  
- **Quản lý thông tin người dùng:**  
  Sử dụng các giao thức bảo mật khi xử lý thông tin đăng nhập, yêu cầu bảo vệ các khóa API và thông tin nhạy cảm khác.  
- **Đảm bảo an toàn khi truy vấn dữ liệu:**  
  Xây dựng các biện pháp kiểm soát truy cập tới API backend, nhất là với các endpoints quan trọng như `/v1/chat/completions`.

### 3.4.4. Giao diện người dùng và trải nghiệm  
- **Tối ưu giao diện người dùng:**  
  Giao diện cần tương thích đa thiết bị, dễ sử dụng và phản hồi nhanh. Việc chuyển đổi theme và điều hướng trực quan góp phần nâng cao trải nghiệm người dùng.
- **Phản hồi người dùng:**  
  Hệ thống cần có cơ chế thu thập góp ý, báo lỗi nhanh chóng thông qua IssuePage, đảm bảo người dùng có thể liên hệ hỗ trợ và gửi phản hồi trực tiếp.

---

## Kết luận  
Chương 3 đã trình bày chi tiết quy trình xây dựng mô hình tìm kiếm và truy vấn thông tin liên quan đến môn học Luật biển và quy tắc tránh va quốc tế. Từ quá trình tiền xử lý dữ liệu, tạo embedding, xây dựng vector database trên Qdrant, tích hợp API backend với FastAPI đến xây dựng giao diện người dùng hiện đại bằng React, hệ thống đã cho thấy tiềm năng trong việc cung cấp thông tin chính xác và hỗ trợ ra quyết định cho người dùng.  
Tuy nhiên, để ứng dụng thực tế, cần chú ý tối ưu hóa hiệu năng, cải thiện chất lượng dữ liệu và đảm bảo vấn đề bảo mật. Qua các thí nghiệm và phản hồi ban đầu, mô hình sẽ được tiếp tục cải tiến để phục vụ hiệu quả hơn cho nhu cầu tra cứu thông tin và tư vấn pháp lý của sinh viên cũng như người dùng ngoài trường.

---

Báo cáo trên đây cung cấp cái nhìn tổng quát và sâu sắc về toàn bộ quy trình xây dựng mô hình, các thành phần kỹ thuật chính cũng như những vấn đề cần quan tâm trong giai đoạn ứng dụng thực tế. Nếu cần thông tin bổ sung hoặc làm rõ thêm bất kỳ nội dung nào, bạn hãy cho biết nhé!