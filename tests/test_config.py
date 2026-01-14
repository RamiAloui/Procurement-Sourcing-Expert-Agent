"""Tests for configuration module."""

import os
import pytest
from pathlib import Path


def test_config_module_imports():
    """Test config module import."""
    from src import config
    assert config is not None


def test_ollama_configuration_defaults():
    """Test OLLAMA default values."""
    from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
    
    assert OLLAMA_BASE_URL == "http://localhost:11434"
    assert OLLAMA_MODEL == "qwen3:8b"


def test_langsmith_configuration_defaults():
    """Test LangSmith default values."""
    from src.config import LANGCHAIN_TRACING_V2, LANGCHAIN_API_KEY, LANGCHAIN_PROJECT
    
    assert LANGCHAIN_TRACING_V2 == "true"
    # API key can be empty or set from .env file
    assert isinstance(LANGCHAIN_API_KEY, str)
    assert LANGCHAIN_PROJECT == "procurement-agent"


def test_data_path_configuration():
    """Test DATA_PATH configuration."""
    from src.config import DATA_PATH
    
    assert DATA_PATH is not None
    assert isinstance(DATA_PATH, Path)


def test_data_path_exists():
    """Test DATA_PATH points to existing directory."""
    from src.config import DATA_PATH
    
    # DATA_PATH should exist (the Agents - Code Challenge/Data/ directory)
    assert DATA_PATH.exists(), f"DATA_PATH does not exist: {DATA_PATH}"
    assert DATA_PATH.is_dir(), f"DATA_PATH is not a directory: {DATA_PATH}"


def test_config_summary_function():
    """Test config summary structure."""
    from src.config import get_config_summary
    
    summary = get_config_summary()
    
    assert isinstance(summary, dict)
    assert "OLLAMA_BASE_URL" in summary
    assert "OLLAMA_MODEL" in summary
    assert "LANGCHAIN_TRACING_V2" in summary
    assert "LANGCHAIN_PROJECT" in summary
    assert "DATA_PATH" in summary
    assert "LANGCHAIN_API_KEY" in summary


def test_config_summary_masks_api_key():
    """Test API key masking in summary."""
    from src.config import get_config_summary
    
    summary = get_config_summary()
    
    # API key should be masked or show "(not set)"
    assert summary["LANGCHAIN_API_KEY"] in ["***", "(not set)"]


def test_config_respects_environment_variables(monkeypatch):
    """Test environment variable override."""
    # Set environment variables before importing config
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1")
    monkeypatch.setenv("LANGCHAIN_PROJECT", "test-project")
    
    # Need to reload the module to pick up new env vars
    import importlib
    import sys
    if 'src.config' in sys.modules:
        importlib.reload(sys.modules['src.config'])
    else:
        import src.config
        
    from src.config import OLLAMA_MODEL, LANGCHAIN_PROJECT
    
    assert OLLAMA_MODEL == "llama3.1"
    assert LANGCHAIN_PROJECT == "test-project"


def test_invalid_data_path_raises_error(monkeypatch, tmp_path):
    """Test invalid DATA_PATH error handling."""
    # Set DATA_PATH to non-existent directory
    invalid_path = tmp_path / "nonexistent"
    monkeypatch.setenv("DATA_PATH", str(invalid_path))
    
    # Importing config with invalid DATA_PATH should raise ValueError
    import sys
    if 'src.config' in sys.modules:
        del sys.modules['src.config']
    
    with pytest.raises(ValueError, match="DATA_PATH does not exist"):
        import src.config
