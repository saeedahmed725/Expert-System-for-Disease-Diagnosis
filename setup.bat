@echo off
echo ===================================================
echo Expert System for Disease Diagnosis - Setup Script
echo ===================================================
echo.
echo This script will help you set up the required dependencies
echo for the Expert System for Disease Diagnosis project.
echo.
echo Steps:
echo 1. Check for SWI-Prolog installation
echo 2. Install Python dependencies
echo 3. Run the Streamlit application
echo.
echo ===================================================
echo.

REM Check for SWI-Prolog installation
echo Checking for SWI-Prolog installation...
where swipl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: SWI-Prolog was not found in your PATH.
    echo Please install SWI-Prolog from https://www.swi-prolog.org/download/stable
    echo After installation, ensure that swipl.exe is in your system PATH.
    echo.
    echo Press any key to continue with Python setup anyway...
    pause >nul
) else (
    echo SWI-Prolog found. Continuing with setup...
)
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
