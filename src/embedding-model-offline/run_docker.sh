#!/bin/bash
set -e

echo "=== Bat dau chay Embedding API ==="

# Kiem tra Docker
docker --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Loi: Docker khong duoc cai dat"
    exit 1
fi

# Kiem tra Docker da chay
docker info >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Loi: Docker khong chay"
    exit 1
fi

# Kiem tra file image
if [ ! -f "embedding-offline-image.tar" ]; then
    echo "Loi: Khong tim thay file embedding-offline-image.tar"
    echo "Vui long chay prepare_model.sh truoc"
    exit 1
fi

# Tai Docker image
echo "=== Tai Docker image ==="
docker load -i embedding-offline-image.tar

# Kiem tra container da ton tai
if docker ps -a --format '{{.Names}}' | grep -q "^embedding-service$"; then
    echo "Container embedding-service da ton tai. Dang dung va xoa..."
    docker stop embedding-service
    docker rm embedding-service
fi

# Kiem tra port 8000
if netstat -tuln | grep -q ":8000 "; then
    echo "Canh bao: Port 8000 dang duoc su dung"
    echo "Vui long dong ung dung dang su dung port nay hoac thay doi port trong script"
    exit 1
fi

# Khoi dong container
echo "=== Khoi dong container ==="
docker run -d --name embedding-service -p 8000:8000 embedding-offline:latest

echo "=== Hoan tat! ==="
echo "API da duoc khoi dong tai http://localhost:8000"
echo "Kiem tra trang thai: curl http://localhost:8000" 