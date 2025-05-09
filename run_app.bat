@echo off
echo Checking dependencies for Medical Expert System...

REM Check if streamlit is installed
pip show streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo Starting the Expert System for Disease Diagnosis...
streamlit run app.py
pause
