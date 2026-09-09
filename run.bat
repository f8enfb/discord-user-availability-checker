@echo off
chcp 65001 >nul
cls
echo.
echo ============================================================
echo    Discord Username Checker v2.0 Bot Edition - Launch
echo ============================================================
echo.

REM Check Python
echo [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found! Please install Python 3.8+
    echo [!] Download from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check dependencies
echo [*] Checking dependencies...
python -c "import discord" >nul 2>&1
if errorlevel 1 (
    echo [!] Discord.py not installed!
    echo [*] Installing discord.py and requests...
    pip install discord.py requests
    if errorlevel 1 (
        echo [!] Error installing dependencies!
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] All dependencies installed
)
echo.

REM Launch application
echo [*] Launching Discord Username Checker v2.0...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [!] Error launching application!
    pause
    exit /b 1
)
