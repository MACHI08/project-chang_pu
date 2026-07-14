@echo off
setlocal
title CHANGPU SYSTEM

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" goto venv_missing

".venv\Scripts\python.exe" "main.py"
set "APP_EXIT_CODE=%ERRORLEVEL%"

if not "%APP_EXIT_CODE%"=="0" echo [ERROR] The program exited with an error.

echo.
pause
exit /b %APP_EXIT_CODE%

:venv_missing
echo [ERROR] Project virtual environment was not found.
echo Run INSTALL.bat first.
pause
exit /b 1
