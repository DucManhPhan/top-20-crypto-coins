import os
import subprocess

def install_requirements(requirements_file, target_dir):
    """
    Install Python packages from a requirements file into a target directory.

    Args:
        requirements_file (str): The path to the requirements file. Ex: 'requirements.txt'
        target_dir (str): The directory where the packages will be installed. Ex: 'lambda_layer/python'
    """

    print(f"[INSTALL_REQUIREMENTS] Installing packages from {requirements_file} to {target_dir}")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    subprocess.check_call([
        'python', '-m', 'pip', 'install', '-r', requirements_file, '--target', target_dir
    ])
    print(f"[INSTALL_REQUIREMENTS] Successfully installed packages to {target_dir}")

if __name__ == "__main__":
    requirements_file = 'lambda-layer/requirements.txt'
    target_dir = 'lambda-layer/python'

    install_requirements(requirements_file, target_dir)