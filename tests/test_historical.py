"""Unit tests for historical query tools."""

import pytest
from src.tools.historical import (
    get_latest_value, 
    get_value_by_date, 
    get_values_by_range,
    calculate_percentage_change,
    get_trend_direction,
    find_peak,
    find_valley,
    find_peak_and_valley,
    calculate_moving_average,
    calculate_trend_line
)


def test_get_latest_value():
    """Test getting latest historical value."""
    result = get_latest_value("energy_futures")
    
    assert 'date' in result
    assert 'value' in result
    assert isinstance(result['value'], float)


def test_get_value_by_date_valid():
    """Test getting value for valid date."""
    result = get_value_by_date("energy_futures", "2024-08-01")
    
    assert result['date'] == "2024-08-01"
    assert isinstance(result['value'], float)


def test_get_value_by_date_invalid():
    """Test error for invalid date."""
    result = get_value_by_date("energy_futures", "2099-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result


def test_get_values_by_range_valid():
    """Test getting values for valid date range."""
    result = get_values_by_range("energy_futures", "2024-08-01", "2024-08-31")
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all('date' in item and 'value' in item for item in result)


def test_get_values_by_range_empty():
    """Test empty result for out-of-range dates."""
    result = get_values_by_range("energy_futures", "2099-01-01", "2099-12-31")
    
    assert isinstance(result, dict)
    assert result.get('success') is False


def test_calculate_percentage_change():
    """Test percentage change calculation."""
    result = calculate_percentage_change("energy_futures", "2024-01-01", "2024-02-01")
    
    assert 'percentage_change' in result
    assert 'trend_direction' in result
    assert 'start_value' in result
    assert 'end_value' in result
    assert isinstance(result['percentage_change'], float)
    assert result['trend_direction'] in ['increasing', 'decreasing', 'stable']


def test_trend_direction_accuracy():
    """Test trend direction calculation accuracy."""
    result = calculate_percentage_change("energy_futures", "2024-01-01", "2024-08-01")
    
    # Verify calculation is accurate to 2 decimals
    expected = round(((result['end_value'] - result['start_value']) / result['start_value']) * 100, 2)
    assert result['percentage_change'] == expected


def test_get_trend_direction():
    """Test get_trend_direction helper."""
    trend = get_trend_direction("energy_futures", "2024-01-01", "2024-02-01")
    
    assert trend in ['increasing', 'decreasing', 'stable']


def test_find_peak():
    """Test finding peak value."""
    result = find_peak("energy_futures")
    
    assert 'date' in result
    assert 'value' in result
    assert result['type'] == 'peak'
    assert isinstance(result['value'], float)


def test_find_valley():
    """Test finding valley value."""
    result = find_valley("energy_futures")
    
    assert 'date' in result
    assert 'value' in result
    assert result['type'] == 'valley'
    assert isinstance(result['value'], float)


def test_find_peak_and_valley():
    """Test finding both peak and valley."""
    result = find_peak_and_valley("energy_futures")
    
    assert 'peak' in result
    assert 'valley' in result
    assert result['peak']['value'] > result['valley']['value']


def test_find_peak_with_date_range():
    """Test finding peak within date range."""
    result = find_peak("energy_futures", "2024-01-01", "2024-06-30")
    
    assert result['date'] >= "2024-01-01"
    assert result['date'] <= "2024-06-30"


def test_calculate_moving_average():
    """Test moving average calculation."""
    result = calculate_moving_average("energy_futures", window_size=7)
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all('date' in item and 'moving_average' in item for item in result)


def test_calculate_moving_average_with_range():
    """Test moving average with date range."""
    result = calculate_moving_average(
        "energy_futures", 
        window_size=3,
        start_date="2024-08-01",
        end_date="2024-10-31"
    )
    
    assert isinstance(result, list)


def test_calculate_trend_line():
    """Test trend line calculation."""
    result = calculate_trend_line("energy_futures")
    
    assert 'slope' in result
    assert 'intercept' in result
    assert 'trend_direction' in result
    assert result['trend_direction'] in ['increasing', 'decreasing', 'stable']


def test_calculate_trend_line_with_range():
    """Test trend line with date range."""
    result = calculate_trend_line(
        "energy_futures",
        start_date="2024-08-01",
        end_date="2024-10-31"
    )
    
    assert isinstance(result['slope'], float)
    assert isinstance(result['intercept'], float)
