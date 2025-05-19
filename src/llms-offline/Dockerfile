FROM python:3.10-slim

WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ ./app/
COPY model/ ./model/

# Expose port
EXPOSE 8000

# Chạy service
CMD ["uvicorn", "app.service:app", "--host", "0.0.0.0", "--port", "8000"]
