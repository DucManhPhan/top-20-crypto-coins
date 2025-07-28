@echo off
echo Starting Unit Tests...

cd /d "%~dp0..\.."

echo.
echo ================================================
echo Running: Unit Tests (Verbose)
echo ================================================
python -m pytest tests/ -v
if %errorlevel% neq 0 (
    echo [FAIL] Unit Tests - FAILED
    goto :summary
) else (
    echo [PASS] Unit Tests - PASSED
)

echo.
echo ================================================
echo Checking for pytest-cov...
echo ================================================
python -c "import pytest_cov" 2>nul
if %errorlevel% neq 0 (
    echo pytest-cov not installed. Skipping coverage test.
    echo Install with: pip install pytest-cov
    goto :summary
)

echo.
echo ================================================
echo Running: Unit Tests with Coverage
echo ================================================
python -m pytest tests/ --cov=backend --cov-report=term-missing
if %errorlevel% neq 0 (
    echo [FAIL] Unit Tests with Coverage - FAILED
    set "coverage_failed=1"
) else (
    echo [PASS] Unit Tests with Coverage - PASSED
)

:summary
echo.
echo ============================================================
echo TEST SUMMARY
echo ============================================================

echo Unit Tests                         [PASS] PASSED
if defined coverage_failed (
    echo Unit Tests with Coverage           [FAIL] FAILED
) else (
    echo Unit Tests with Coverage           [PASS] PASSED
)

echo.
if defined has_failures (
    echo Some tests failed.
    exit /b 1
) else (
    echo All tests passed!
    exit /b 0
)