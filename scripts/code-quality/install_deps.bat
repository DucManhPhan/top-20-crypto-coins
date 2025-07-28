@echo off
echo 📦 Installing Code Quality Dependencies...

python -m pip install black flake8 bandit

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    exit /b 1
) else (
    echo ✅ Dependencies installed successfully
    echo.
    echo You can now run: scripts\code-quality\code_quality.bat
)