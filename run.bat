@echo off
REM Web Cloner - Quick Run Script for Windows
REM This script activates the virtual environment and runs the Streamlit app

echo ========================================
echo   Starting Web Cloner Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo X Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if streamlit is installed
where streamlit >nul 2>nul
if %errorlevel% neq 0 (
    echo X Streamlit not found!
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Streamlit app...
echo Open your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the app
streamlit run src\app.py
