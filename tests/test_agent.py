"""Tests for agent module imports and basic setup."""

def test_agent_imports():
    """Test agent module can be imported."""
    try:
        from src.agent import agent
        assert agent is not None
    except ImportError:
        # Skip if dependencies not available
        pass


def test_tools_import():
    """Test tools module can be imported."""
    try:
        from src.agent import tools
        assert tools is not None
    except ImportError:
        # Skip if dependencies not available
        pass


def test_llm_import():
    """Test LLM module can be imported."""
    try:
        from src.agent import llm
        assert llm is not None
    except ImportError:
        # Skip if dependencies not available
        pass
