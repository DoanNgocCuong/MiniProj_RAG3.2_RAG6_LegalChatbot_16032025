# Base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Sao chép requirements trước để tận dụng Docker cache
COPY app/requirements.txt /app/requirements.txt

# Cài đặt các gói Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Sao chép mô hình và mã nguồn
COPY model/ /app/model/
COPY app/ /app/

# Thiết lập biến môi trường
ENV MODEL_PATH=/app/model
ENV MODEL_NAME=paraphrase-multilingual-mpnet-base-v2

# Mở cổng
EXPOSE 8000

# Tạo thư mục cho logs và quyền ghi
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Thêm user không phải root cho bảo mật tốt hơn
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Khởi động ứng dụng
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 