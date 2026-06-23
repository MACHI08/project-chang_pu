@echo off
chcp 65001 >nul
title Python Project Setup

echo.
echo ==========================================
echo        Python Project Environment Setup
echo ==========================================
echo.

echo [1/5] Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python 명령어를 찾을 수 없습니다.
    echo Python 3.12 설치 및 PATH 설정을 확인하세요.
    pause
    exit /b 1
)

echo.
echo [2/5] Creating virtual environment...

if exist ".venv\Scripts\python.exe" (
    echo .venv already exists. Skipping creation.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo [ERROR] 가상환경 생성 실패.
        pause
        exit /b 1
    )
)

echo.
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate

if errorlevel 1 (
    echo.
    echo [ERROR] 가상환경 활성화 실패.
    pause
    exit /b 1
)

echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [5/5] Installing requirements...

if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping package installation.
)

echo.
echo ==========================================
echo              Setup Complete
echo ==========================================
echo.
echo Virtual environment is now active.
echo.
echo Run your project with:
echo     python main.py
echo.
echo Or if your file is grab.py:
echo     python grab.py
echo.
cmd /k