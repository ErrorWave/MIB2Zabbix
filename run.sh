#!/bin/bash
# Linux/macOS shell script to run the MIB to Zabbix converter

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.6+ for your system:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  macOS: brew install python3"
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not installed"
    echo "Please install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  macOS: brew install python-tk@3.x (where x is your Python version)"
    exit 1
fi

echo "Starting MIB to Zabbix Template Converter..."
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Failed to run the application"
    exit 1
fi
