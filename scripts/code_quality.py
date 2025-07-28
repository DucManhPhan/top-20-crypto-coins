#!/usr/bin/env python3
"""
Script to run code quality checks locally
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

def main():
    """Main function to run all code quality checks"""
    print("Starting Code Quality Checks...")
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    checks = [
        ("python -m black backend/ tests/", "Code Formatting (Black)"),
        ("python -m black --check backend/ tests/", "Code Formatting Check"),
        ("python -m flake8 backend/ tests/ --max-line-length=88 --extend-ignore=E203,W503", "Linting Check (Flake8)"),
        ("python -m bandit -r backend/", "Security Check (Bandit)"),
    ]
    
    results = []
    for command, description in checks:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for description, success in results:
        status = "[PASS] PASSED" if success else "[FAIL] FAILED"
        print(f"{description:<30} {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print(f"\nAll checks passed! Ready to commit.")
        sys.exit(0)
    else:
        print(f"\nSome checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()