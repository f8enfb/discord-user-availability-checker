@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   Discord Username Checker - Установка v1.0        ║
echo ╚════════════════════════════════════════════════════╝
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

REM Обновление pip
echo [*] Обновление pip...
python -m pip install --upgrade pip >nul 2>&1
echo [✓] pip обновлён
echo.

REM Установка зависимостей
echo [*] Установка зависимостей (requests)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [!] Ошибка при установке зависимостей!
    pause
    exit /b 1
)
echo [✓] Зависимости установлены
echo.

REM Установка PyInstaller для создания EXE
echo [*] Установка PyInstaller (для создания .exe)...
pip install pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [!] Ошибка при установке PyInstaller!
    pause
    exit /b 1
)
echo [✓] PyInstaller установлен
echo.

REM Создание EXE файла
echo [*] Создание EXE файла...
pyinstaller --onefile --windowed --name "Discord Username Checker" main.py >nul 2>&1
if errorlevel 1 (
    echo [!] Ошибка при создании EXE файла!
    pause
    exit /b 1
)
echo [✓] EXE файл создан
echo.

REM Успешная установка
echo ╔════════════════════════════════════════════════════╗
echo ║          ✓ Установка завершена успешно!           ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo [✓] Зависимости установлены
echo [✓] PyInstaller установлен
echo [✓] EXE файл создан в папке: dist\
echo.
echo Вы можете запустить приложение:
echo   1. Через Python: python main.py
echo   2. Через EXE: dist\Discord Username Checker.exe
echo.
pause
