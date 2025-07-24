import os
import zipfile
import subprocess
import shutil

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

def clean_unnecessary_files(target_dir):
    """
    Clean unnecessary files from the target directory.

    Args:
        target_dir (str): The directory to clean. Ex: 'lambda_layer/python'
    """

    print(f"[CLEAN_UNNECESSARY_FILES] Cleaning unnecessary files in {target_dir}")
    for root, dirs, files in os.walk(target_dir, topdown=False):
        # Remove cache directories
        for dir_name in dirs[:]:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                print(f"[CLEAN_UNNECESSARY_FILES] Removing directory: {dir_path}")
                shutil.rmtree(dir_path)
                dirs.remove(dir_name)
        
        # Remove cache files
        for file in files:
            if file.endswith(('.pyc', '.pyo', '.pyd')):
                file_path = os.path.join(root, file)
                print(f"[CLEAN_UNNECESSARY_FILES] Removing file: {file_path}")
                os.remove(file_path)
    print(f"[CLEAN_UNNECESSARY_FILES] Cleaning completed.")

def zip_directory(folder_path, zip_path):
    """
    Compress the specified folder into a zip file.

    Args:
        folder_path (str): The path to the folder to compress. Ex: 'lambda_layer/python
        zip_path (str): The path where the zip file will be created. Ex: 'lambda_layer.zip'
    """

    print(f"[ZIP_DIRECTORY] Zipping folder: {folder_path} to {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # arcname = os.path.relpath(file_path, folder_path)
                arcname = os.path.join('python', os.path.relpath(file_path, folder_path))
                zipf.write(file_path, arcname)
    print(f"[ZIP_DIRECTORY] Successfully zipped folder to {zip_path}")

def cleanup_python_folder(target_dir):
    """
    Remove all contents from the python folder after zipping.
    
    Args:
        target_dir (str): The directory to clean. Ex: 'lambda_layer/python'
    """
    print(f"[CLEANUP] Removing all contents from {target_dir}")
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
        os.makedirs(target_dir)
        print(f"[CLEANUP] Successfully cleaned {target_dir}")
    else:
        print(f"[CLEANUP] Directory {target_dir} does not exist")

def publish_layer(layer_name, zip_path, runtime, region):
    """
    Upload layer to AWS Lambda.
    """

    cmd = [
        'aws', 'lambda', 'publish-layer-version',
        '--layer-name', layer_name,
        '--zip-file', f'fileb://{zip_path}',
        '--compatible-runtimes', runtime,
        '--region', region
    ]
    subprocess.run(cmd, check=True)
    print(f"Done uploading Layer {layer_name} to AWS.")

def main():
    requirements_file = 'lambda-layer/requirements.txt'
    python_dir = 'lambda-layer/python'
    output_zip = 'lambda-layer.zip'

    if not os.path.exists(python_dir):
        os.makedirs(python_dir)

    install_requirements(requirements_file, python_dir)    
    clean_unnecessary_files(python_dir)

    print(f"[MAIN] Starting to zip directory: {python_dir}")
    zip_directory(python_dir, output_zip)
    print(f"[MAIN] Zipping completed. Output file: {output_zip}")
    
    # cleanup_python_folder(python_dir)

    # publish_layer('lambda-layer', output_zip, 'python3.9', 'ap-southeast-1')

if __name__ == "__main__":
    main()