# build_ludo.py
# ====================================================
# Auto-build State Lounge Ludo portable EXE
# ====================================================

import os
import subprocess
import sys
import shutil

print("=== State Lounge Ludo Build Script (Python) ===")

# Ensure Python packages are installed
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError:
        print(f"Error installing {package}. Exiting.")
        sys.exit(1)

# Check Pygame
try:
    import pygame
    print("Pygame is installed.")
except ImportError:
    print("Pygame not found. Installing...")
    install_package("pygame")

# Check PyInstaller
try:
    import PyInstaller
    print("PyInstaller is installed.")
except ImportError:
    print("PyInstaller not found. Installing...")
    install_package("pyinstaller")

# Check required files
required_files = ["ludo.py", "dice.wav", "music.mp3"]
missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print(f"Error: Missing required files: {', '.join(missing)}")
    sys.exit(1)

print("All required files are present.")

# Prepare --add-data arguments
add_data_args = []
add_data_args.append(f"dice.wav{os.pathsep}.")
add_data_args.append(f"music.mp3{os.pathsep}.")

if os.path.exists("assets"):
    add_data_args.append(f"assets{os.pathsep}assets")

# Check for custom icon
icon_arg = []
if os.path.exists("statelounge.ico"):
    icon_arg = ["--icon", "statelounge.ico"]

# Build command
cmd = [sys.executable, "-m", "PyInstaller",
       "--onefile",
       "--noconsole"] + icon_arg

for data in add_data_args:
    cmd += ["--add-data", data]

cmd += ["ludo.py"]

print("\nRunning PyInstaller...")
print("Command:", " ".join(cmd))

# Run PyInstaller
result = subprocess.run(cmd)
if result.returncode != 0:
    print("Build failed.")
    sys.exit(1)

print("\n=== Build Complete ===")
dist_path = os.path.join(os.getcwd(), "dist", "ludo.exe")
if os.path.exists(dist_path):
    print(f"Your portable game is ready: {dist_path}")
else:
    print("ludo.exe not found in dist folder. Something went wrong.")
