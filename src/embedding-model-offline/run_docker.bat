@echo off
setlocal enabledelayedexpansion

echo === Bat dau chay Embedding API ===

REM Kiem tra Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Docker khong duoc cai dat
    pause
    exit /b 1
)

REM Kiem tra Docker da chay
docker info >nul 2>&1
if errorlevel 1 (
    echo Loi: Docker khong chay
    pause
    exit /b 1
)

REM Kiem tra thu muc model
if not exist "model" (
    echo Loi: Khong tim thay thu muc model
    echo Vui long chay simple_host.py truoc de tai model
    pause
    exit /b 1
)

REM Build Docker image
echo === Build Docker image ===
docker build -t embedding-offline:latest .
if errorlevel 1 (
    echo Loi: Khong the build Docker image
    pause
    exit /b 1
)

REM Kiem tra container da ton tai
docker ps -a --filter "name=embedding-service" --format "{{.Names}}" | findstr "embedding-service" >nul
if not errorlevel 1 (
    echo Container embedding-service da ton tai. Dang dung va xoa...
    docker stop embedding-service
    docker rm embedding-service
)

REM Kiem tra port 8000
netstat -ano | findstr ":8000" >nul
if not errorlevel 1 (
    echo Canh bao: Port 8000 dang duoc su dung
    echo Vui long dong ung dung dang su dung port nay hoac thay doi port trong script
    pause
    exit /b 1
)

REM Khoi dong container
echo === Khoi dong container ===
docker run -d --name embedding-service -p 8000:8000 embedding-offline:latest
if errorlevel 1 (
    echo Loi: Khong the khoi dong container
    pause
    exit /b 1
)

echo === Hoan tat! ===
echo API da duoc khoi dong tai http://localhost:8000
echo Kiem tra trang thai: curl http://localhost:8000
pause 