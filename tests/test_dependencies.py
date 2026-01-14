"""Test required dependencies are installed."""
import pytest
from pathlib import Path


def test_langchain_imports():
    """Test LangChain imports."""
    import langchain
    import langchain_core
    from langchain_core.messages import HumanMessage
    
    assert langchain is not None
    assert langchain_core is not None
    
    msg = HumanMessage(content="test")
    assert msg.content == "test"
    assert msg.type == "human"


def test_langgraph_imports():
    """Test LangGraph imports."""
    from langgraph.graph import StateGraph
    from langgraph.prebuilt import create_react_agent
    from typing import TypedDict
    
    assert StateGraph is not None
    assert create_react_agent is not None
    
    class TestState(TypedDict):
        value: int
    
    graph = StateGraph(TestState)
    assert graph is not None


def test_langsmith_import():
    """Test LangSmith import."""
    import langsmith
    from langsmith import Client
    
    assert langsmith is not None
    assert Client is not None


def test_langchain_ollama_import():
    """Test LangChain Ollama import."""
    from langchain_ollama import ChatOllama
    
    assert ChatOllama is not None
    assert callable(ChatOllama)


def test_pandas_import():
    """Test pandas import."""
    import pandas as pd
    import numpy as np
    
    assert pd is not None
    
    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    assert len(df) == 3
    assert list(df.columns) == ['a', 'b']


def test_streamlit_import():
    """Test Streamlit import."""
    import streamlit as st
    
    assert st is not None
    
    assert hasattr(st, 'chat_message')
    assert hasattr(st, 'chat_input')


def test_pytest_import():
    """Test pytest import."""
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
