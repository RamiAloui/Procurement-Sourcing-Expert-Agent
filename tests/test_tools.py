"""Tests for tool registration and basic functionality."""

from src.agent.tools import TOOLS


def test_tools_registered():
    """Test that tools are registered."""
    assert len(TOOLS) > 0
    
    tool_names = [tool.name for tool in TOOLS]
    assert "query_historical_data" in tool_names
    assert "query_forecast_data" in tool_names
    assert "analyze_market_drivers" in tool_names


def test_tools_have_descriptions():
    """Test that tools have descriptions."""
    for tool in TOOLS:
        assert hasattr(tool, 'description')
        assert len(tool.description) > 10
