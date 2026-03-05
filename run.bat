@echo off
REM Windows batch script to run the MIB to Zabbix converter
REM This script checks for Python and runs the main application

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://www.python.org
    pause
    exit /b 1
)

echo Starting MIB to Zabbix Template Converter...
python main.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Failed to run the application
    echo Please make sure Python is properly installed
    pause
    exit /b 1
)
