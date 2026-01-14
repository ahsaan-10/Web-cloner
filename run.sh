#!/bin/bash

# Web Cloner - Quick Run Script
# This script activates the virtual environment and runs the Streamlit app

echo "========================================"
echo "  Starting Web Cloner Application"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Starting Streamlit app..."
echo "📱 Open your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the app
streamlit run src/app.py
