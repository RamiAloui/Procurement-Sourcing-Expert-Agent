"""
Test suite to verify all required dependencies are installed and importable.
"""
import pytest
from pathlib import Path


def test_langchain_imports():
    """Test that LangChain core packages can be imported and functional."""
    import langchain
    import langchain_core
    from langchain_core.messages import HumanMessage
    
    # Verify imports successful
    assert langchain is not None
    assert langchain_core is not None
    
    # Verify basic functionality
    msg = HumanMessage(content="test")
    assert msg.content == "test"
    assert msg.type == "human"


def test_langgraph_imports():
    """Test that LangGraph packages can be imported and functional."""
    from langgraph.graph import StateGraph
    from langgraph.prebuilt import create_react_agent
    from typing import TypedDict
    
    # Verify imports successful
    assert StateGraph is not None
    assert create_react_agent is not None
    
    # Verify basic functionality - can create a state graph
    class TestState(TypedDict):
        value: int
    
    graph = StateGraph(TestState)
    assert graph is not None


def test_langsmith_import():
    """Test that LangSmith can be imported and has required functionality."""
    import langsmith
    from langsmith import Client
    
    assert langsmith is not None
    assert Client is not None


def test_langchain_ollama_import():
    """Test that LangChain Ollama integration can be imported."""
    from langchain_ollama import ChatOllama
    
    assert ChatOllama is not None
    # Verify it's a callable class
    assert callable(ChatOllama)


def test_pandas_import():
    """Test that pandas can be imported and functional."""
    import pandas as pd
    import numpy as np
    
    # Verify import successful
    assert pd is not None
    
    # Verify basic functionality
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert len(df) == 3
    assert list(df.columns) == ['a', 'b']


def test_streamlit_import():
    """Test that Streamlit can be imported with chat components."""
    import streamlit as st
    
    # Verify import successful
    assert st is not None
    
    # Verify chat components exist
    assert hasattr(st, 'chat_message')
    assert hasattr(st, 'chat_input')


def test_pytest_import():
    """Test that pytest is available and functional."""
    import pytest
    
    assert pytest is not None
    assert hasattr(pytest, 'mark')
    assert hasattr(pytest, 'fixture')


def test_python_dotenv_import():
    """Test that python-dotenv can be imported and functional."""
    from dotenv import load_dotenv, find_dotenv
    
    assert load_dotenv is not None
    assert find_dotenv is not None
    assert callable(load_dotenv)


def test_dependency_versions():
    """Test that installed versions match requirements.txt."""
    import langchain
    import langsmith
    import pandas
    import streamlit
    import pytest as pt
    
    # Read requirements.txt to get expected versions
    requirements_path = Path(__file__).parent.parent / 'requirements.txt'
    assert requirements_path.exists(), "requirements.txt not found"
    
    expected_versions = {}
    with open(requirements_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '==' in line:
                package, version = line.split('==')
                expected_versions[package.strip()] = version.strip()
    
    # Verify versions match
    assert langchain.__version__ == expected_versions['langchain']
    assert langsmith.__version__ == expected_versions['langsmith']
    assert pandas.__version__ == expected_versions['pandas']
    assert streamlit.__version__ == expected_versions['streamlit']
    assert pt.__version__ == expected_versions['pytest']
