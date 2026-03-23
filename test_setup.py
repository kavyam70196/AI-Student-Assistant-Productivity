"""
Test script to verify the AI Student Assistant setup
Run this after installation to check if everything is configured correctly
"""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version: {}.{}.{} (OK)".format(version.major, version.minor, version.micro))
        return True
    else:
        print("❌ Python version: {}.{}.{} (Need 3.8+)".format(version.major, version.minor, version.micro))
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'openai', 'PyPDF2', 'dotenv', 'werkzeug']
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package.lower())
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists and has API key"""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY' in content and 'your_openai_api_key_here' not in content:
                print("✅ OpenAI API key is configured")
                return True
            else:
                print("⚠️  OpenAI API key not set in .env file")
                return False
    else:
        print("❌ .env file not found")
        return False

def check_folders():
    """Check if required folders exist"""
    folders = ['static', 'static/css', 'static/js', 'templates', 'uploads']
    all_exist = True
    
    for folder in folders:
        if os.path.exists(folder):
            print(f"✅ {folder}/ folder exists")
        else:
            print(f"❌ {folder}/ folder missing")
            all_exist = False
    
    return all_exist

def check_files():
    """Check if required files exist"""
    files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/script.js'
    ]
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("AI Student Productivity Assistant - Setup Verification")
    print("=" * 60)
    print()
    
    print("📋 Checking Python Version...")
    python_ok = check_python_version()
    print()
    
    print("📦 Checking Dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("🔑 Checking Environment Configuration...")
    env_ok = check_env_file()
    print()
    
    print("📁 Checking Folder Structure...")
    folders_ok = check_folders()
    print()
    
    print("📄 Checking Required Files...")
    files_ok = check_files()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and env_ok and folders_ok and files_ok:
        print("✅ ALL CHECKS PASSED! You're ready to run the application.")
        print("\nRun the application with: python app.py")
    else:
        print("⚠️  SOME CHECKS FAILED. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Create .env file: copy .env.example .env")
        print("- Add your OpenAI API key to .env file")
    print("=" * 60)

if __name__ == "__main__":
    main()
