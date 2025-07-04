#!/usr/bin/env python3
"""
Portable setup for Hand Gesture Recognition app
Creates a portable package that can be shared with others
"""
import os
import shutil
import subprocess
import sys
import zipfile

def create_portable_package():
    """Create a portable package with all necessary files"""
    
    # Create portable directory
    portable_dir = "HandGestureRecognition_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    os.makedirs(portable_dir)
    
    # Copy main files
    files_to_copy = [
        "app.py",
        "utils",
        "model",
        "README.md"
    ]
    
    for item in files_to_copy:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, os.path.join(portable_dir, item))
            else:
                shutil.copy2(item, portable_dir)
    
    # Create requirements.txt
    with open(os.path.join(portable_dir, "requirements.txt"), "w") as f:
        f.write("opencv-python==4.9.0.80\n")
        f.write("mediapipe==0.10.11\n")
        f.write("tensorflow==2.13.0\n")
        f.write("numpy\n")
        f.write("matplotlib\n")
    
    # Create setup script
    setup_script = """@echo off
echo Installing Python dependencies...
pip install -r requirements.txt
echo Setup complete! 
echo.
echo To run the app:
echo python app.py
echo.
pause
"""
    
    with open(os.path.join(portable_dir, "setup.bat"), "w") as f:
        f.write(setup_script)
    
    # Create run script
    run_script = """@echo off
echo Starting Hand Gesture Recognition...
python app.py %*
pause
"""
    
    with open(os.path.join(portable_dir, "run.bat"), "w") as f:
        f.write(run_script)
    
    # Create README
    readme_content = """# Hand Gesture Recognition - Portable Version

## Setup Instructions:
1. Make sure Python 3.7+ is installed on your system
2. Double-click 'setup.bat' to install dependencies
3. Double-click 'run.bat' to start the application

## Manual Setup:
If the batch files don't work, run these commands in a terminal:
```
pip install -r requirements.txt
python app.py
```

## Usage:
- Press ESC to exit
- Use keys 0-9 to record gestures in logging mode
- Press 'n' for normal mode
- Press 'k' for keypoint logging mode
- Press 'h' for history logging mode
"""
    
    with open(os.path.join(portable_dir, "PORTABLE_README.txt"), "w") as f:
        f.write(readme_content)
    
    print(f"Portable package created in: {portable_dir}")
    print("You can now zip this folder and share it with others!")
    
    # Create zip file
    zip_filename = "HandGestureRecognition_Portable.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, portable_dir)
                zipf.write(file_path, arcname)
    
    print(f"Zip file created: {zip_filename}")
    print("This zip file can be shared with others!")

if __name__ == "__main__":
    create_portable_package()