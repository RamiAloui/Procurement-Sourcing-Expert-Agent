"""Tests for missing data handling in DataLoader and tools."""

import pytest
from src.data.loader import DataLoader
from src.tools.historical import get_value_by_date, get_latest_value
from src.tools.forecast import get_forecast


def test_load_historical_missing_file():
    """Test DataLoader returns None for missing historical file."""
    loader = DataLoader("Agents - Code Challenge/Data")
    result = loader.load_historical("nonexistent_dataset")
    
    assert result is None


def test_load_forecast_missing_file():
    """Test DataLoader returns None for missing forecast file."""
    loader = DataLoader("Agents - Code Challenge/Data")
    result = loader.load_forecast("nonexistent_dataset")
    
    assert result is None


def test_get_value_by_date_missing_dataset():
    """Test tool returns error dict when dataset doesn't exist."""
    result = get_value_by_date("nonexistent_dataset", "2024-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'not found' in result.get('message', '').lower()
    assert 'available_datasets' in result


def test_get_latest_value_missing_dataset():
    """Test tool returns error dict when dataset doesn't exist."""
    result = get_latest_value("nonexistent_dataset")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'not found' in result.get('message', '').lower()


def test_get_forecast_missing_dataset():
    """Test forecast tool returns error dict when dataset doesn't exist."""
    result = get_forecast("nonexistent_dataset", months_ahead=1)
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'not found' in result.get('message', '').lower()
