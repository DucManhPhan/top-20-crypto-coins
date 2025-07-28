@echo off
echo 🚀 Starting Code Quality Checks...

cd /d "%~dp0..\.."

echo.
echo ================================================
echo Running: Code Formatting (Black)
echo ================================================
python -m black backend/ tests/
if %errorlevel% neq 0 (
    echo ❌ Code Formatting - FAILED
    goto :summary
) else (
    echo ✅ Code Formatting - PASSED
)

echo.
echo ================================================
echo Running: Code Formatting Check
echo ================================================
python -m black --check backend/ tests/
if %errorlevel% neq 0 (
    echo ❌ Code Formatting Check - FAILED
    set "format_check_failed=1"
) else (
    echo ✅ Code Formatting Check - PASSED
)

echo.
echo ================================================
echo Running: Linting Check (Flake8)
echo ================================================
python -m flake8 backend/ tests/ --max-line-length=88 --extend-ignore=E203,W503
if %errorlevel% neq 0 (
    echo ❌ Linting Check - FAILED
    set "lint_failed=1"
) else (
    echo ✅ Linting Check - PASSED
)

echo.
echo ================================================
echo Running: Security Check (Bandit)
echo ================================================
python -m bandit -r backend/
if %errorlevel% neq 0 (
    echo ❌ Security Check - FAILED
    set "security_failed=1"
) else (
    echo ✅ Security Check - PASSED
)

:summary
echo.
echo ============================================================
echo 📊 SUMMARY
echo ============================================================

if defined format_check_failed (
    echo Code Formatting Check          ❌ FAILED
    set "has_failures=1"
) else (
    echo Code Formatting Check          ✅ PASSED
)

if defined lint_failed (
    echo Linting Check                  ❌ FAILED
    set "has_failures=1"
) else (
    echo Linting Check                  ✅ PASSED
)

if defined security_failed (
    echo Security Check                 ❌ FAILED
    set "has_failures=1"
) else (
    echo Security Check                 ✅ PASSED
)

echo.
if defined has_failures (
    echo 💥 Some checks failed. Please fix the issues above.
    exit /b 1
) else (
    echo 🎉 All checks passed! Ready to commit.
    exit /b 0
)