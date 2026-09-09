@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Discord Username Checker v2.0 Bot Edition - Запуск       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [*] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python не найден! Пожалуйста установите Python 3.8+
    echo [!] Скачайте с https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [✓] Python найден
echo.

REM Проверка зависимостей
echo [*] Проверка зависимостей...
python -c "import discord" >nul 2>&1
if errorlevel 1 (
    echo [!] Discord.py не установлен!
    echo [*] Установка discord.py...
    pip install discord.py requests
    if errorlevel 1 (
        echo [!] Ошибка при установке зависимостей!
        pause
        exit /b 1
    )
    echo [✓] Зависимости установлены
) else (
    echo [✓] Все зависимости установлены
)
echo.

REM Запуск приложения
echo [*] Запуск Discord Username Checker v2.0...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [!] Ошибка при запуске приложения!
    pause
    exit /b 1
)
