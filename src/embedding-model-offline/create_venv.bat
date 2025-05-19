@echo off
echo === Tao moi truong ao Python ===

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Python khong duoc cai dat
    pause
    exit /b 1
)

REM Xoa moi truong ao cu neu ton tai
if exist ".venv" (
    echo Xoa moi truong ao cu...
    rmdir /s /q .venv
)

REM Tao moi truong ao moi
echo Tao moi truong ao moi...
python -m venv .venv

REM Kich hoat moi truong ao
echo Kich hoat moi truong ao...
call .venv\Scripts\activate.bat

REM Cai dat pip moi nhat
echo Cai dat pip moi nhat...
python -m pip install --upgrade pip

echo === Hoan tat tao moi truong ao! ===
echo Ban co the chay prepare_model_v2.bat de tiep tuc
pause 