#!/usr/bin/env python3
"""
Installation script for Sume application dependencies
Run this to install all required packages for the optimized version
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False
    return True

def main():
    """Install all required dependencies"""
    packages = [
        "google-generativeai",
        "pydub",
        "yt-dlp",
        "openai-whisper",
        "trafilatura",
        "requests",
        "gradio",
        "ffmpeg-python",
        "PyPDF2",
        "python-docx",
        "beautifulsoup4"
    ]
    
    print("🚀 Installing Sume application dependencies...")
    print("=" * 50)
    
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("=" * 50)
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("Please install these manually or check your internet connection.")
    else:
        print("✅ All dependencies installed successfully!")
        print("\n🎉 You can now run the optimized Sume application!")
        print("Run: python app.py")

if __name__ == "__main__":
    main()
