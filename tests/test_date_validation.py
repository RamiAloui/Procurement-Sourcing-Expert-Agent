"""Tests for out-of-range date handling in historical and forecast tools."""

import pytest
from src.tools.historical import get_value_by_date, get_values_by_range, calculate_percentage_change
from src.tools.forecast import get_forecast, get_forecast_by_date


def test_get_value_by_date_before_range():
    """Test date before available data range returns error dict."""
    result = get_value_by_date("energy_futures", "1990-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result
    assert 'available_range' in result
    assert 'suggested_date' in result


def test_get_value_by_date_after_range():
    """Test date after available data range returns error dict."""
    result = get_value_by_date("energy_futures", "2030-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result
    assert 'available_range' in result
    assert 'suggested_date' in result


def test_get_values_by_range_start_before_range():
    """Test range starting before available data returns error dict."""
    result = get_values_by_range("energy_futures", "1990-01-01", "2024-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'available_range' in result


def test_get_values_by_range_end_after_range():
    """Test range ending after available data returns error dict."""
    result = get_values_by_range("energy_futures", "2024-01-01", "2030-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'available_range' in result


def test_calculate_percentage_change_dates_out_of_range():
    """Test percentage change with out-of-range dates returns error dict."""
    result = calculate_percentage_change("energy_futures", "1990-01-01", "2030-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result


def test_get_forecast_beyond_horizon():
    """Test forecast beyond available horizon returns error dict."""
    result = get_forecast("energy_futures", months_ahead=100)
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result
    assert 'max_horizon' in result or 'available_range' in result


def test_get_forecast_by_date_beyond_horizon():
    """Test forecast by date beyond horizon returns error dict."""
    result = get_forecast_by_date("energy_futures", "2030-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result
