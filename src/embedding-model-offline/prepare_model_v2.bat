@echo off
setlocal enabledelayedexpansion

echo === Bat dau chuan bi mo hinh embedding ===

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Python khong duoc cai dat
    pause
    exit /b 1
)

REM Kiem tra pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo Loi: pip khong duoc cai dat
    pause
    exit /b 1
)

REM Kiem tra git
git --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Git khong duoc cai dat
    echo Vui long cai dat Git tu https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Kiem tra moi truong ao
if not exist ".venv" (
    echo Loi: Khong tim thay moi truong ao .venv
    echo Vui long chay create_venv.bat truoc de tao moi truong ao
    pause
    exit /b 1
)

REM Kich hoat moi truong ao
echo === Kich hoat moi truong ao Python ===
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Loi: Khong the kich hoat moi truong ao
    echo Vui long chay create_venv.bat de tao lai moi truong ao
    pause
    exit /b 1
)

REM Cai dat thu vien
echo === Cai dat thu vien ===
python -m pip install --upgrade pip
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
python -m pip install -r app/requirements.txt --no-cache-dir

REM Tao thu muc
echo === Tao thu muc ===
if not exist "model" mkdir model
if not exist "model\cache" mkdir model\cache

REM Tai va chuyen doi mo hinh
echo === Tai va chuyen doi mo hinh ===
python scripts/prepare_model.py
if errorlevel 1 (
    echo Loi: Khong the tai hoac chuyen doi mo hinh
    pause
    exit /b 1
)

REM Kiem tra mo hinh
echo === Kiem tra mo hinh ===
if not exist "model\standard" (
    echo Loi: Khong the tao mo hinh tieu chuan!
    pause
    exit /b 1
)
echo Mo hinh tieu chuan da duoc tao thanh cong!

REM Dong goi Docker
echo === Xay dung Docker image ===
docker build -t embedding-offline:latest .
if errorlevel 1 (
    echo Loi: Khong the xay dung Docker image
    pause
    exit /b 1
)

REM Luu Docker image
echo === Luu Docker image thanh file ===
docker save -o embedding-offline-image.tar embedding-offline:latest
if errorlevel 1 (
    echo Loi: Khong the luu Docker image
    pause
    exit /b 1
)

REM Huy kich hoat moi truong ao
call deactivate

echo === Hoan tat! ===
echo Mo hinh da duoc dong goi trong file embedding-offline-image.tar
pause 