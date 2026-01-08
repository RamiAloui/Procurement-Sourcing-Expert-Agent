"""
Configuration management for Agents - Code Challenge.

Loads configuration from environment variables with fallback defaults.
Uses python-dotenv to load .env file if present.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# LLM Configuration
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# LangSmith Configuration
LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "procurement-agent")

# Data Configuration
DATA_PATH: Path = Path(os.getenv("DATA_PATH", "Agents - Code Challenge/Data/"))

# Validation
if not DATA_PATH.exists():
    raise ValueError(
        f"DATA_PATH does not exist: {DATA_PATH}\n"
        f"Please ensure the dataset directory is present or update DATA_PATH in .env"
    )


def get_config_summary() -> dict:
    """Return configuration summary (safe for logging - no secrets)."""
    return {
        "OLLAMA_BASE_URL": OLLAMA_BASE_URL,
        "OLLAMA_MODEL": OLLAMA_MODEL,
        "LANGCHAIN_TRACING_V2": LANGCHAIN_TRACING_V2,
        "LANGCHAIN_PROJECT": LANGCHAIN_PROJECT,
        "DATA_PATH": str(DATA_PATH),
        "LANGCHAIN_API_KEY": "***" if LANGCHAIN_API_KEY else "(not set)"
    }
