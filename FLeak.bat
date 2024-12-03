@echo off
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Pythonがインストールされていません。
    pause
    exit /b
)

python bot.py
pause
