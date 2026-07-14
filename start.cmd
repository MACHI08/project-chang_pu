@echo off
chcp 65001 >nul
title CHANGPU SYSTEM

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] 프로젝트 가상환경을 찾을 수 없습니다.
    echo 먼저 INSTALL.bat을 실행하세요.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py

if errorlevel 1 (
    echo.
    echo [ERROR] 프로그램 실행 중 오류가 발생했습니다.
)

pause
