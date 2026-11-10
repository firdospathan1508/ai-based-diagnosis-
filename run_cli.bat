@echo off
title Medical Diagnosis Expert System (CLI Mode)
color 0B

echo ======================================================================
echo           Starting Medical Diagnosis Expert System (CLI)
echo ======================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in your system PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo and make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

python cli_diagnosis.py
pause
