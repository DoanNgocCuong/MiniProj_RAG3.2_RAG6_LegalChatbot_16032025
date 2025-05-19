# Base image
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói phụ thuộc
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Sao chép requirements trước để tận dụng Docker cache
COPY app/requirements.txt /app/requirements.txt

# Cập nhật pip và cài đặt các gói Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 && \
    pip install --no-cache-dir -r requirements.txt

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