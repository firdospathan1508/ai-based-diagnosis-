@echo off
title Medical Diagnosis Expert System
color 0A

echo ======================================================================
echo           Starting Medical Diagnosis Expert System
echo           Knowledge Representation and Reasoning (Unit III)
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

echo Launching Desktop GUI Application...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Application exited with code %errorlevel%.
    pause
)
