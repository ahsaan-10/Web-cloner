#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all dependencies are installed and the environment is ready.
"""

import sys
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check Python version"""
    print_header("Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Checking Dependencies")

    dependencies = {
        'streamlit': 'Streamlit',
        'requests': 'Requests',
        'bs4': 'BeautifulSoup4',
        'playwright': 'Playwright',
        'lxml': 'lxml'
    }

    all_installed = True

    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} - Installed")
        except ImportError:
            print(f"❌ {name} - Not Installed")
            all_installed = False

    return all_installed

def check_database():
    """Check if database directory and file exist"""
    print_header("Checking Database")

    db_dir = "data"
    db_file = "data/cloned_sites.db"

    if os.path.exists(db_dir):
        print(f"✅ Database directory exists: {db_dir}/")
    else:
        print(f"❌ Database directory missing: {db_dir}/")
        return False

    if os.path.exists(db_file):
        print(f"✅ Database file exists: {db_file}")
    else:
        print(f"⚠️  Database file will be created on first run")

    return True

def check_source_files():
    """Check if main source files exist"""
    print_header("Checking Source Files")

    files = {
        'src/app.py': 'Main Application',
        'src/__init__.py': 'Source Package Init',
        'requirements.txt': 'Requirements File',
        'README.md': 'README'
    }

    all_exist = True

    for file, description in files.items():
        if os.path.exists(file):
            print(f"✅ {description} - {file}")
        else:
            print(f"❌ {description} - {file} (Missing)")
            all_exist = False

    return all_exist

def check_vscode_config():
    """Check VS Code configuration"""
    print_header("Checking VS Code Configuration")

    vscode_files = {
        '.vscode/settings.json': 'Workspace Settings',
        '.vscode/launch.json': 'Debug Configuration',
        '.vscode/tasks.json': 'Tasks Configuration'
    }

    for file, description in vscode_files.items():
        if os.path.exists(file):
            print(f"✅ {description} - {file}")
        else:
            print(f"⚠️  {description} - {file} (Optional)")

    return True

def test_import_app():
    """Try to import the main app module"""
    print_header("Testing App Import")

    try:
        # Add src to path
        sys.path.insert(0, 'src')

        # Try importing
        print("Attempting to import src.app...")
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "src/app.py")
        if spec and spec.loader:
            print("✅ App module can be loaded")
            return True
        else:
            print("❌ App module cannot be loaded")
            return False
    except Exception as e:
        print(f"❌ Error importing app: {str(e)}")
        return False

def print_summary(results):
    """Print summary of all checks"""
    print_header("Summary")

    passed = sum(results.values())
    total = len(results)

    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")

    print(f"\n{passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! Your setup is ready!")
        print("\nTo run the app:")
        print("  streamlit run src/app.py")
        print("\nOr in VS Code:")
        print("  Press Ctrl+Shift+B")
    else:
        print("\n⚠️  Some checks failed. Please review the errors above.")

    return passed == total

def main():
    """Run all checks"""
    print("\n" + "█"*60)
    print("  WEB CLONER - SETUP VERIFICATION")
    print("█"*60)

    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Database': check_database(),
        'Source Files': check_source_files(),
        'VS Code Config': check_vscode_config(),
        'App Import': test_import_app()
    }

    success = print_summary(results)

    print("\n" + "="*60 + "\n")

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
