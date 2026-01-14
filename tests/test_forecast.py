"""Unit tests for forecast query tools."""

import pytest
from src.tools.forecast import (
    get_forecast, 
    get_forecast_by_date, 
    get_all_forecasts,
    get_quantile_forecast,
    get_confidence_interval,
    compare_current_to_forecast,
    analyze_forecast_trend
)


def test_get_forecast():
    """Test getting forecast N months ahead."""
    result = get_forecast("energy_futures", months_ahead=1)
    
    assert 'date' in result
    assert 'forecast_value' in result
    assert isinstance(result['forecast_value'], float)


def test_get_forecast_multiple_months():
    """Test different month forecasts."""
    result_1 = get_forecast("energy_futures", months_ahead=1)
    result_3 = get_forecast("energy_futures", months_ahead=3)
    
    assert result_1['date'] != result_3['date']


def test_get_forecast_by_date_valid():
    """Test forecast for valid date."""
    # First get a valid forecast date
    all_forecasts = get_all_forecasts("energy_futures")
    valid_date = all_forecasts[0]['date']
    
    result = get_forecast_by_date("energy_futures", valid_date)
    
    assert result['date'] == valid_date
    assert isinstance(result['forecast_value'], float)


def test_get_forecast_by_date_invalid():
    """Test error for invalid date."""
    result = get_forecast_by_date("energy_futures", "2099-01-01")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'message' in result


def test_get_all_forecasts():
    """Test getting all forecasts."""
    result = get_all_forecasts("energy_futures")
    
    assert isinstance(result, list)
    assert len(result) > 0
    assert all('date' in item and 'forecast_value' in item for item in result)


def test_get_quantile_forecast():
    """Test getting forecast for specific quantile."""
    all_forecasts = get_all_forecasts("energy_futures")
    valid_date = all_forecasts[0]['date']
    
    result = get_quantile_forecast("energy_futures", valid_date, 0.5)
    
    assert result['date'] == valid_date
    assert result['quantile'] == 0.5
    assert isinstance(result['forecast_value'], float)


def test_get_confidence_interval_80():
    """Test 80% confidence interval."""
    all_forecasts = get_all_forecasts("energy_futures")
    valid_date = all_forecasts[0]['date']
    
    result = get_confidence_interval("energy_futures", valid_date, confidence_level=80)
    
    assert result['confidence_level'] == 80
    assert result['lower_bound'] < result['median'] < result['upper_bound']


def test_get_confidence_interval_90():
    """Test 90% confidence interval."""
    all_forecasts = get_all_forecasts("energy_futures")
    valid_date = all_forecasts[0]['date']
    
    result = get_confidence_interval("energy_futures", valid_date, confidence_level=90)
    
    assert result['confidence_level'] == 90
    assert result['lower_bound'] < result['upper_bound']


def test_get_confidence_interval_invalid_level():
    """Test error for invalid confidence level."""
    all_forecasts = get_all_forecasts("energy_futures")
    valid_date = all_forecasts[0]['date']
    
    result = get_confidence_interval("energy_futures", valid_date, confidence_level=95)
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'available_levels' in result


def test_compare_current_to_forecast():
    """Test comparing current price to forecast."""
    result = compare_current_to_forecast("energy_futures")
    
    assert 'current_date' in result
    assert 'current_value' in result
    assert 'forecast_date' in result
    assert 'forecast_value' in result
    assert 'difference' in result
    assert 'percentage_change' in result
    assert 'trend_direction' in result
    assert result['trend_direction'] in ['increasing', 'decreasing', 'stable']


def test_compare_percentage_change_accuracy():
    """Test percentage change calculation accuracy."""
    result = compare_current_to_forecast("energy_futures")
    
    # Verify calculation
    expected = round(
        ((result['forecast_value'] - result['current_value']) / result['current_value']) * 100,
        2
    )
    assert result['percentage_change'] == expected


def test_compare_trend_direction():
    """Test trend direction logic."""
    result = compare_current_to_forecast("energy_futures")
    
    if result['percentage_change'] > 0:
        assert result['trend_direction'] == "increasing"
    elif result['percentage_change'] < 0:
        assert result['trend_direction'] == "decreasing"
    else:
        assert result['trend_direction'] == "stable"


def test_analyze_forecast_trend():
    """Test forecast trend analysis."""
    result = analyze_forecast_trend("energy_futures", months_ahead=3)
    
    assert 'start_date' in result
    assert 'end_date' in result
    assert 'average_monthly_change' in result
    assert 'trend_direction' in result
    assert 'monthly_changes' in result
    assert result['trend_direction'] in ['increasing', 'decreasing', 'stable']
    assert result['months_analyzed'] == 3


def test_analyze_forecast_trend_different_months():
    """Test trend analysis with different month counts."""
    result_3 = analyze_forecast_trend("energy_futures", months_ahead=3)
    result_6 = analyze_forecast_trend("energy_futures", months_ahead=6)
    
    assert result_3['months_analyzed'] == 3
    assert result_6['months_analyzed'] == 6
    assert len(result_3['monthly_changes']) == 2  # 3 months = 2 changes
    assert len(result_6['monthly_changes']) == 5  # 6 months = 5 changes


def test_analyze_forecast_average_calculation():
    """Test average change calculation accuracy."""
    result = analyze_forecast_trend("energy_futures", months_ahead=3)
    
    # Verify average calculation
    expected_avg = round(sum(result['monthly_changes']) / len(result['monthly_changes']), 2)
    assert result['average_monthly_change'] == expected_avg
