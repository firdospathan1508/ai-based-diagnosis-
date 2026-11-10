@echo off
title Sanjeevani Medical Diagnosis Web App
color 0B

echo ======================================================================
echo           Starting Sanjeevani Medical Diagnosis Web App
echo           Knowledge Representation and Reasoning (Unit III)
echo ======================================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [NOTE] Python is not found in PATH.
    echo Opening static web prototype directly in your default web browser...
    start index.html
    pause
    exit /b
)

echo Starting local Python web server and opening browser...
python web_server.py

if %errorlevel% neq 0 (
    echo Opening static HTML directly...
    start index.html
    pause
)
