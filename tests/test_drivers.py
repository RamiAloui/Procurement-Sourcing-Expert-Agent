"""Tests for market driver analysis tools."""

import pytest
from src.tools.drivers import get_top_drivers, get_driver_details, analyze_drivers_combined


def test_get_top_drivers_default():
    """Test getting top 5 drivers by default."""
    result = get_top_drivers("energy_futures")
    
    assert len(result) <= 5
    assert all('name' in d for d in result)
    assert all('importance_mean' in d for d in result)
    
    # Check sorted by importance descending
    for i in range(len(result) - 1):
        assert result[i]['importance_mean'] >= result[i + 1]['importance_mean']


def test_get_top_drivers_custom_n():
    """Test getting custom number of top drivers."""
    result = get_top_drivers("energy_futures", top_n=3)
    
    assert len(result) <= 3


def test_get_top_drivers_includes_metrics():
    """Test that drivers include all importance metrics."""
    result = get_top_drivers("energy_futures", top_n=1)
    
    assert len(result) > 0
    driver = result[0]
    
    assert 'importance_mean' in driver
    assert 'importance_max' in driver
    assert 'importance_min' in driver
    assert isinstance(driver['importance_mean'], (int, float))


def test_get_top_drivers_invalid_dataset():
    """Test error handling for invalid dataset."""
    with pytest.raises(Exception):
        get_top_drivers("invalid_dataset")


def test_get_driver_details():
    """Test getting detailed driver information."""
    # Get a valid driver name first
    top_drivers = get_top_drivers("energy_futures", top_n=1)
    driver_name = top_drivers[0]['name']
    
    result = get_driver_details("energy_futures", driver_name)
    
    assert result['name'] == driver_name
    assert result['direction'] in ['positive', 'negative']
    assert 'direction_explanation' in result
    assert 'pearson_correlation' in result
    assert 'granger_causality' in result


def test_get_driver_details_direction():
    """Test direction extraction and interpretation."""
    top_drivers = get_top_drivers("energy_futures", top_n=1)
    driver_name = top_drivers[0]['name']
    
    result = get_driver_details("energy_futures", driver_name)
    
    # Check direction is valid
    assert result['direction'] in ['positive', 'negative']
    
    # Check explanation exists
    assert len(result['direction_explanation']) > 0
    
    if result['direction'] == 'positive':
        assert 'increase' in result['direction_explanation'].lower()


def test_get_driver_details_correlations():
    """Test correlation metrics extraction."""
    top_drivers = get_top_drivers("energy_futures", top_n=1)
    driver_name = top_drivers[0]['name']
    
    result = get_driver_details("energy_futures", driver_name)
    
    # Check Pearson correlation structure
    assert 'mean' in result['pearson_correlation']
    assert 'max' in result['pearson_correlation']
    assert 'min' in result['pearson_correlation']
    
    # Check Granger causality structure
    assert 'mean' in result['granger_causality']
    assert isinstance(result['granger_causality']['mean'], (int, float))


def test_get_driver_details_not_found():
    """Test error handling for driver not found."""
    result = get_driver_details("energy_futures", "Nonexistent Driver")
    
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'available_drivers' in result
    assert isinstance(result, dict)
    assert result.get('success') is False
    assert 'available_drivers' in result


def test_get_driver_details_with_lag():
    """Test lag information extraction."""
    # Find a driver with lag information
    top_drivers = get_top_drivers("energy_futures", top_n=5)
    
    # Get details for first driver
    driver_name = top_drivers[0]['name']
    result = get_driver_details("energy_futures", driver_name)
    
    # Check lag fields exist
    assert 'lag' in result
    assert 'lag_explanation' in result


def test_get_driver_details_lag_explanation():
    """Test lag explanation is user-friendly."""
    top_drivers = get_top_drivers("energy_futures", top_n=5)
    driver_name = top_drivers[0]['name']
    
    result = get_driver_details("energy_futures", driver_name)
    
    # Check explanation exists
    assert result['lag_explanation'] is not None
    assert len(result['lag_explanation']) > 0
    
    # If lag exists, explanation should mention it
    if result['lag']:
        assert 'month' in result['lag_explanation'].lower()


def test_get_driver_details_missing_lag():
    """Test handling of missing lag information."""
    # The target entry doesn't have lag info
    # We'll test with a driver that might not have it
    top_drivers = get_top_drivers("energy_futures", top_n=10)
    
    # At least one should work
    result = get_driver_details("energy_futures", top_drivers[0]['name'])
    
    # Should handle gracefully
    assert 'lag_explanation' in result
    
    # If no lag, explanation should indicate unavailable
    if not result['lag']:
        assert 'not available' in result['lag_explanation'].lower()


def test_analyze_drivers_combined():
    """Test combined driver analysis."""
    result = analyze_drivers_combined("energy_futures", top_n=5)
    
    assert 'drivers_supporting_increase' in result
    assert 'drivers_supporting_decrease' in result
    assert 'net_effect' in result
    assert 'total_drivers_analyzed' in result
    
    # Should analyze requested number of drivers
    total = len(result['drivers_supporting_increase']) + len(result['drivers_supporting_decrease'])
    assert total <= 5


def test_analyze_drivers_combined_categorization():
    """Test drivers are categorized by direction."""
    result = analyze_drivers_combined("energy_futures", top_n=10)
    
    # Check positive drivers
    for driver in result['drivers_supporting_increase']:
        assert driver['direction'] == 'positive'
        assert 'name' in driver
        assert 'importance' in driver
    
    # Check negative drivers
    for driver in result['drivers_supporting_decrease']:
        assert driver['direction'] == 'negative'


def test_analyze_drivers_combined_importance():
    """Test combined importance calculation."""
    result = analyze_drivers_combined("energy_futures", top_n=5)
    
    # Check importance totals exist
    assert 'total_importance_increase' in result
    assert 'total_importance_decrease' in result
    
    # Totals should be non-negative
    assert result['total_importance_increase'] >= 0
    assert result['total_importance_decrease'] >= 0


def test_analyze_drivers_combined_net_effect():
    """Test net effect determination."""
    result = analyze_drivers_combined("energy_futures", top_n=10)
    
    # Net effect should be one of three values
    assert result['net_effect'] in ['increase', 'decrease', 'mixed']
    
    # Should have explanation
    assert len(result['net_explanation']) > 0
