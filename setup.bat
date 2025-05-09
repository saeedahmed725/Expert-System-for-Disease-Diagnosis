@echo off
echo ===================================================
echo Expert System for Disease Diagnosis - Setup Script
echo ===================================================
echo.
echo This script will help you set up the required dependencies
echo for the Expert System for Disease Diagnosis project.
echo.
echo Steps:
echo 1. Install Python dependencies
echo 2. Run the Streamlit application
echo.
echo ===================================================
echo.

REM Install Python dependencies
echo Installing required Python packages...
pip install -r requirements.txt
echo.

REM Run the Streamlit app
echo Starting the Expert System application...
echo.
echo If the application doesn't open automatically, copy and paste this URL in your browser:
echo http://localhost:8501
echo.
echo Press Ctrl+C in this console to stop the application when done.
echo.
streamlit run app.py

pause
