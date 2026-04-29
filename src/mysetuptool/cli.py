#!/usr/bin/env python3
"""Environment setup automation tool CLI"""
import os
import sys
import platform
import subprocess


def get_script_dir():
    """Get the script directory"""
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)  # src/envsetup
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
    """Run Windows Python tool"""
    script_path = os.path.join(script_dir, "windows_tool.py")
    if not os.path.exists(script_path):
        print("Error: windows_tool.py not found")
        sys.exit(1)
    subprocess.run([sys.executable, script_path])


def main():
    script_dir = get_script_dir()
    system = detect_platform()

    print(f"\n{'='*50}")
    print(f"  Environment Setup Tool v1.0.0")
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