"""Test project structure and environment setup."""
import os
import sys
from pathlib import Path


def test_python_version():
    """Verify Python version is 3.11 or higher."""
    assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"


def test_src_directory_exists():
    """Verify src directory exists."""
    assert Path("src").is_dir(), "src/ directory must exist"


def test_src_init_exists():
    """Verify src/__init__.py exists."""
    assert Path("src/__init__.py").is_file(), "src/__init__.py must exist"


def test_agent_package_exists():
    """Verify src/agent package exists with __init__.py."""
    assert Path("src/agent").is_dir(), "src/agent/ directory must exist"
    assert Path("src/agent/__init__.py").is_file(), "src/agent/__init__.py must exist"


def test_tools_package_exists():
    """Verify src/tools package exists with __init__.py."""
    assert Path("src/tools").is_dir(), "src/tools/ directory must exist"
    assert Path("src/tools/__init__.py").is_file(), "src/tools/__init__.py must exist"


def test_data_package_exists():
    """Verify src/data package exists with __init__.py."""
    assert Path("src/data").is_dir(), "src/data/ directory must exist"
    assert Path("src/data/__init__.py").is_file(), "src/data/__init__.py must exist"


def test_ui_package_exists():
    """Verify src/ui package exists with __init__.py."""
    assert Path("src/ui").is_dir(), "src/ui/ directory must exist"
    assert Path("src/ui/__init__.py").is_file(), "src/ui/__init__.py must exist"


def test_tests_directory_exists():
    """Verify tests directory exists."""
    assert Path("tests").is_dir(), "tests/ directory must exist"
    assert Path("tests/__init__.py").is_file(), "tests/__init__.py must exist"


def test_virtual_environment_exists():
    """Verify virtual environment directory exists."""
    assert Path("venv").is_dir(), "venv/ directory must exist"


def test_virtual_environment_python_exists():
    """Verify virtual environment has Python executable."""
    if sys.platform == "win32":
        venv_python = Path("venv/Scripts/python.exe")
    else:
        venv_python = Path("venv/bin/python")
    
    assert venv_python.is_file(), f"Virtual environment Python executable must exist at {venv_python}"


def test_readme_exists():
    """Verify README.md exists."""
    assert Path("README.md").is_file(), "README.md must exist"


def test_gitignore_exists():
    """Verify .gitignore exists."""
    assert Path(".gitignore").is_file(), ".gitignore must exist"


def test_gitignore_excludes_venv():
    """Verify .gitignore excludes virtual environment."""
    gitignore_content = Path(".gitignore").read_text()
    assert "venv/" in gitignore_content, ".gitignore must exclude venv/"


def test_gitignore_excludes_env_file():
    """Verify .gitignore excludes .env file."""
    gitignore_content = Path(".gitignore").read_text()
    assert ".env" in gitignore_content, ".gitignore must exclude .env"


def test_gitignore_excludes_pycache():
    """Verify .gitignore excludes __pycache__."""
    gitignore_content = Path(".gitignore").read_text()
    assert "__pycache__/" in gitignore_content, ".gitignore must exclude __pycache__/"
