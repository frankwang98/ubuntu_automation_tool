# Cross-Platform Automation Tool

A cross-platform automation toolkit for Windows, Linux (Ubuntu/Debian), and macOS.

[![Python Version](https://img.shields.io/pypi/pyversions/mysetuptool)](https://pypi.org/project/mysetuptool/)
[![License](https://img.shields.io/pypi/l/mysetuptool)](LICENSE)

## Supported Platforms

| Platform | Script | Status |
|----------|--------|--------|
| Ubuntu/Debian | `ubuntu_tool.py` | ✅ |
| macOS | `mac_tool.py` | ✅ |
| Windows | `windows_tool.py` | ✅ |

## Installation

### From PyPI (Recommended)

```bash
pip install mysetuptool
```

### From Source

```bash
git clone https://github.com/frankwang98/mysetuptool.git
cd mysetuptool
pip install -e .
```

## Usage

### Quick Start

```bash
# After installation, run:
mysetuptool

# Or use the entry script directly:
python -m mysetuptool
```

### Platform-Specific Usage

#### Linux (Ubuntu/Debian)

```bash
python -m mysetuptool.ubuntu_tool
# or
chmod +x ubuntu_tool.py && ./ubuntu_tool.py
```

#### macOS

```bash
python -m mysetuptool.mac_tool
# or
chmod +x mac_tool.py && ./mac_tool.py
```

#### Windows (Python)

```bash
python -m mysetuptool.windows_tool
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
mysetuptool/
├── src/
│   └── mysetuptool/
│       ├── __init__.py
│       ├── cli.py
│       ├── ubuntu_tool.py
│       ├── mac_tool.py
│       └── windows_tool.py
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