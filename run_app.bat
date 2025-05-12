@echo off
echo Checking dependencies for Medical Expert System...

REM Check if streamlit and pyswip are installed
pip show streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

pip show pyswip >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing pyswip for Prolog integration...
    pip install pyswip
)

REM Check for SWI-Prolog installation
echo Checking for SWI-Prolog installation...
where swipl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: SWI-Prolog was not found in your PATH.
    echo The application requires SWI-Prolog to be installed.
    echo.
    echo Please install SWI-Prolog from https://www.swi-prolog.org/download/stable
    echo Important: During installation, select the option to add SWI-Prolog to your PATH.
    echo.
    echo After installation, you may need to restart your computer.
    echo.
    echo Would you like to continue without SWI-Prolog? The application will run,
    echo but diagnosis functionality will be limited.
    echo.
    choice /C YN /M "Continue anyway [Y/N]?"
    if ERRORLEVEL 2 (
        echo Exiting...
        exit /b 1
    )
) else (
    echo SWI-Prolog found. Continuing...
)

echo Setting up environment for SWI-Prolog...

rem Attempt to find SWI-Prolog installation directory
for %%I in (
    "C:\Program Files\swipl"
    "C:\Program Files (x86)\swipl"
    "C:\swipl"
) do (
    if exist "%%~I\bin\swipl.exe" (
        echo Found SWI-Prolog at: %%~I
        set SWIPL_HOME=%%~I
        goto :found
    )
)

echo SWI-Prolog not found in common locations.
echo Please enter the full path to your SWI-Prolog installation directory:
set /p SWIPL_HOME=

:found
echo Setting SWIPL_HOME to: %SWIPL_HOME%
set PATH=%SWIPL_HOME%\bin;%PATH%

echo Starting the Expert System for Disease Diagnosis...
echo.
echo This application requires SWI-Prolog. If you encounter any errors, please check:
echo 1. SWI-Prolog is installed correctly
echo 2. The pyswip library is installed
echo 3. The expert_system.pl file is in the same directory as app.py
echo.

REM Check if the .new file exists and replace the original if it does
if exist "%~dp0app.py.new" (
    echo Updating application file...
    move /Y "%~dp0app.py.new" "%~dp0app.py"
)

streamlit run app.py

echo.
echo If the application doesn't start automatically, please open a web browser and go to:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application when done.

pause
exit /b 0
