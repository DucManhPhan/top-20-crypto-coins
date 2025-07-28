@echo off
echo Installing Test Dependencies...

cd /d "%~dp0..\.."
python -m pip install -r tests/requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install test dependencies
    exit /b 1
) else (
    echo Test dependencies installed successfully
    echo.
    echo You can now run: scripts\test\run_tests.bat
)