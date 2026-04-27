# Cross-Platform Automation Tool

A cross-platform automation toolkit for Windows, Linux (Ubuntu/Debian), and macOS.

[![Python Version](https://img.shields.io/pypi/pyversions/cross-tool)](https://pypi.org/project/cross-tool/)
[![License](https://img.shields.io/pypi/l/cross-tool)](LICENSE)

## Supported Platforms

| Platform | Script | Status |
|----------|--------|--------|
| Ubuntu/Debian | `ubuntu_tool.py` | ✅ |
| macOS | `mac_tool.py` | ✅ |
| Windows | `windows_tool.ps1` | ✅ |

## Installation

### From PyPI (Recommended)

```bash
pip install cross-tool
```

### From Source

```bash
git clone https://github.com/frankwang98/cross-automation-tool.git
cd cross-automation-tool
pip install -e .
```

## Usage

### Quick Start

```bash
# After installation, run:
cross-tool

# Or use the entry script directly:
python tool.py
```

### Platform-Specific Usage

#### Linux (Ubuntu/Debian)

```bash
python ubuntu_tool.py
# or
chmod +x ubuntu_tool.py && ./ubuntu_tool.py
```

#### macOS

```bash
python mac_tool.py
# or
chmod +x mac_tool.py && ./mac_tool.py
```

#### Windows (PowerShell)

```powershell
# Run as Administrator
.\windows_tool.ps1

# Or allow script execution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\windows_tool.ps1
```

## Features

### Ubuntu Tool
- System Information Query
- System Update
- System Cleanup
- Install Basic Tools
- Docker Management
- Test Scripts
- App Market
- Network Tools
- Mini Games

### macOS Tool
- System Information Query
- System Maintenance
- Install Dev Tools
- Homebrew Management
- Docker Management
- Disk Utilities
- Network Tools
- Privacy & Security
- Mini Games

### Windows Tool
- System Information Query
- System Update (Windows Update)
- System Cleanup
- Install Software (via winget)
- Docker Management
- Network Tools
- Mini Games

## Development

### Project Structure

```
cross-automation-tool/
├── src/
│   └── cross_tool/
│       ├── __init__.py
│       ├── cli.py
│       ├── ubuntu_tool.py
│       └── mac_tool.py
├── scripts/
│   └── windows_tool.ps1
├── pyproject.toml
├── README.md
└── LICENSE
```

### Build and Publish

```bash
# Build the package
python -m build

# Publish to PyPI
python -m publish
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Frank Wang