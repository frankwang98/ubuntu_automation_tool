#!/usr/bin/env python3
"""Cross-platform automation tool CLI"""
import os
import sys
import platform
import subprocess


def get_package_root():
    """Get the package root directory (works in development and installed package)"""
    # Check if running as installed package
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle
        return sys._MEIPASS

    # Running in development (editable install)
    # Navigate from src/cross_tool/cli.py to project root
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)  # src/cross_tool
    package_root = os.path.dirname(src_dir)  # src/
    project_root = os.path.dirname(package_root)  # project root (where pyproject.toml is)

    # Check if pyproject.toml exists
    if os.path.exists(os.path.join(project_root, "pyproject.toml")):
        return src_dir  # Return src/cross_tool where the scripts are

    # Fallback: scripts are in the same directory as cli.py
    return src_dir


def detect_platform():
    """Detect the current operating system"""
    return platform.system().lower()


def run_ubuntu_tool(script_dir):
    """Run Ubuntu/Debian tool"""
    script_path = os.path.join(script_dir, "ubuntu_tool.py")
    if not os.path.exists(script_path):
        print("Error: ubuntu_tool.py not found")
        sys.exit(1)
    subprocess.run([sys.executable, script_path])


def run_mac_tool(script_dir):
    """Run macOS tool"""
    script_path = os.path.join(script_dir, "mac_tool.py")
    if not os.path.exists(script_path):
        print("Error: mac_tool.py not found")
        sys.exit(1)
    subprocess.run([sys.executable, script_path])


def run_windows_tool(script_dir):
    """Run Windows PowerShell tool"""
    script_path = os.path.join(script_dir, "windows_tool.ps1")
    if not os.path.exists(script_path):
        print("Error: windows_tool.ps1 not found")
        sys.exit(1)
    subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path])


def main():
    script_dir = get_package_root()
    system = detect_platform()

    print(f"\n{'='*50}")
    print(f"  Cross-Platform Automation Tool v1.0.0")
    print(f"  Detected OS: {platform.system()}")
    print(f"{'='*50}\n")

    if system == "linux":
        if "microsoft" in platform.uname().release.lower():
            print("Detected WSL (Windows Subsystem for Linux)")

        if os.path.exists("/etc/debian_version"):
            run_ubuntu_tool(script_dir)
        else:
            print("Warning: Currently only supports Debian/Ubuntu based Linux distributions")
            run_ubuntu_tool(script_dir)

    elif system == "darwin":
        run_mac_tool(script_dir)

    elif system == "windows":
        run_windows_tool(script_dir)

    else:
        print(f"Unsupported operating system: {platform.system()}")
        sys.exit(1)


if __name__ == "__main__":
    main()