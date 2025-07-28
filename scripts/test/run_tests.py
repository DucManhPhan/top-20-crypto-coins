#!/usr/bin/env python3
"""
Script to run unit tests locally
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if result.returncode == 0:
        print(f"[PASS] {description} - PASSED")
        return True
    else:
        print(f"[FAIL] {description} - FAILED")
        return False

def check_coverage_available():
    """Check if pytest-cov is available"""
    try:
        import pytest_cov
        return True
    except ImportError:
        return False

def main():
    """Main function to run tests"""
    print("Starting Unit Tests...")
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    os.chdir(project_root)
    
    tests = [
        ("python -m pytest tests/ -v", "Unit Tests (Verbose)"),
        ("python -m pytest tests/ -v --tb=short", "Unit Tests (Short Traceback)"),
    ]
    
    # Add coverage test only if pytest-cov is available
    if check_coverage_available():
        tests.append(("python -m pytest tests/ --cov=backend --cov-report=term-missing", "Unit Tests with Coverage"))
    else:
        print("\nNote: pytest-cov not installed. Skipping coverage test.")
        print("Install with: pip install pytest-cov")
    
    results = []
    for command, description in tests:
        success = run_command(command, description)
        results.append((description, success))
        if not success and "Coverage" not in description:
            break  # Stop on first failure (but continue if only coverage fails)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for description, success in results:
        status = "[PASS] PASSED" if success else "[FAIL] FAILED"
        print(f"{description:<40} {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print(f"\nAll tests passed!")
        sys.exit(0)
    else:
        print(f"\nSome tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()