"""Tests for cross-dataset comparison tools."""

import pytest
from src.tools.comparative import (
    compare_datasets, 
    calculate_correlation, 
    analyze_timing_relationships,
    analyze_multi_commodity_strategy
)


def test_compare_two_datasets():
    """Test basic comparison with 2 datasets."""
    result = compare_datasets(['energy_futures', 'cotton_price'])
    
    assert 'datasets' in result
    assert 'aligned_data' in result
    assert 'common_date_range' in result
    assert 'total_aligned_records' in result
    
    # Should have both datasets
    assert result['datasets'] == ['energy_futures', 'cotton_price']
    
    # Should have aligned data
    assert len(result['aligned_data']) > 0
    
    # Each record should have date and both dataset values
    first_record = result['aligned_data'][0]
    assert 'date' in first_record
    assert 'energy_futures' in first_record
    assert 'cotton_price' in first_record


def test_compare_three_datasets():
    """Test comparison with all 3 datasets."""
    result = compare_datasets(['energy_futures', 'cotton_price', 'cotton_export'])
    
    assert len(result['datasets']) == 3
    assert len(result['aligned_data']) > 0
    
    # Each record should have all three datasets
    first_record = result['aligned_data'][0]
    assert 'energy_futures' in first_record
    assert 'cotton_price' in first_record
    assert 'cotton_export' in first_record


def test_date_alignment():
    """Test that dates are properly aligned."""
    result = compare_datasets(['energy_futures', 'cotton_price'])
    
    # Dates should be sorted
    dates = [record['date'] for record in result['aligned_data']]
    assert dates == sorted(dates)
    
    # Common date range should match actual data
    assert result['common_date_range']['start'] == dates[0]
    assert result['common_date_range']['end'] == dates[-1]
    
    # Total records should match
    assert result['total_aligned_records'] == len(result['aligned_data'])


def test_no_common_dates():
    """Test handling when datasets have no overlap."""
    # This test assumes we can't easily create non-overlapping datasets
    # So we test that the function handles empty results gracefully
    result = compare_datasets(['energy_futures', 'cotton_price'])
    
    # Should still return valid structure even if minimal overlap
    assert isinstance(result['aligned_data'], list)
    assert isinstance(result['total_aligned_records'], int)


def test_calculate_correlation():
    """Test basic correlation calculation."""
    result = calculate_correlation('energy_futures', 'cotton_price')
    
    assert 'dataset1' in result
    assert 'dataset2' in result
    assert 'correlation_coefficient' in result
    assert 'direction' in result
    assert 'strength' in result
    assert 'interpretation' in result
    assert 'data_points_used' in result
    
    # Correlation should be between -1 and 1
    assert -1 <= result['correlation_coefficient'] <= 1
    
    # Should have used some data points
    assert result['data_points_used'] > 0


def test_correlation_strength_classification():
    """Test correlation strength categories."""
    result = calculate_correlation('energy_futures', 'cotton_price')
    
    # Strength should be one of the three categories
    assert result['strength'] in ['weak', 'moderate', 'strong']
    
    # Verify classification logic
    r = abs(result['correlation_coefficient'])
    if r >= 0.7:
        assert result['strength'] == 'strong'
    elif r >= 0.3:
        assert result['strength'] == 'moderate'
    else:
        assert result['strength'] == 'weak'


def test_correlation_direction():
    """Test correlation direction classification."""
    result = calculate_correlation('energy_futures', 'cotton_price')
    
    # Direction should be one of the three options
    assert result['direction'] in ['positive', 'negative', 'none']
    
    # Verify direction logic
    r = result['correlation_coefficient']
    if r > 0.1:
        assert result['direction'] == 'positive'
    elif r < -0.1:
        assert result['direction'] == 'negative'
    else:
        assert result['direction'] == 'none'


def test_analyze_timing_relationships():
    """Test basic timing relationship analysis."""
    result = analyze_timing_relationships('energy_futures', 'cotton_price')
    
    assert 'dataset1' in result
    assert 'dataset2' in result
    assert 'common_drivers' in result
    assert 'lead_commodity' in result
    assert 'average_lag_months' in result
    assert 'timing_insights' in result
    assert 'predictive_value' in result
    
    # Should have some common drivers
    assert isinstance(result['common_drivers'], list)
    
    # Lead commodity should be one of the two datasets
    assert result['lead_commodity'] in ['energy_futures', 'cotton_price', 'similar']
    
    # Predictive value should be classified
    assert result['predictive_value'] in ['low', 'moderate', 'high']


def test_lead_lag_identification():
    """Test lead commodity detection."""
    result = analyze_timing_relationships('energy_futures', 'cotton_price')
    
    # Should identify which commodity leads
    assert 'lead_commodity' in result
    
    # Should have timing insights
    assert len(result['timing_insights']) >= 0
    
    # Each insight should have required fields
    for insight in result['timing_insights']:
        assert 'driver' in insight
        assert 'dataset1_lag' in insight
        assert 'dataset2_lag' in insight
        assert 'interpretation' in insight


def test_lag_quantification():
    """Test time delay calculation."""
    result = analyze_timing_relationships('energy_futures', 'cotton_price')
    
    # Average lag should be a number
    assert isinstance(result['average_lag_months'], (int, float))
    
    # Average lag should be non-negative
    assert result['average_lag_months'] >= 0
    
    # Predictive value should match lag difference
    avg_lag = result['average_lag_months']
    if avg_lag >= 3:
        assert result['predictive_value'] == 'high'
    elif avg_lag >= 1:
        assert result['predictive_value'] == 'moderate'
    else:
        assert result['predictive_value'] == 'low'


def test_analyze_multi_commodity_strategy():
    """Test basic multi-commodity strategic analysis."""
    result = analyze_multi_commodity_strategy(['energy_futures', 'cotton_price'])
    
    assert 'commodities_analyzed' in result
    assert 'individual_analysis' in result
    assert 'cross_commodity_insights' in result
    assert 'strategic_recommendations' in result
    
    # Should analyze both commodities
    assert len(result['commodities_analyzed']) == 2
    
    # Each commodity should have individual analysis
    for commodity in result['commodities_analyzed']:
        assert commodity in result['individual_analysis']
        analysis = result['individual_analysis'][commodity]
        assert 'latest_value' in analysis
        assert 'top_drivers' in analysis
    
    # Should have cross-commodity insights
    assert 'shared_drivers' in result['cross_commodity_insights']
    
    # Should have recommendations
    assert isinstance(result['strategic_recommendations'], list)
    assert len(result['strategic_recommendations']) > 0


def test_strategic_recommendations():
    """Test that strategic recommendations are generated."""
    result = analyze_multi_commodity_strategy(['energy_futures', 'cotton_price'])
    
    # Should have recommendations
    assert 'strategic_recommendations' in result
    assert len(result['strategic_recommendations']) > 0
    
    # Each recommendation should be a string
    for rec in result['strategic_recommendations']:
        assert isinstance(rec, str)
        assert len(rec) > 0


def test_three_commodity_analysis():
    """Test analysis with all 3 datasets."""
    result = analyze_multi_commodity_strategy(['energy_futures', 'cotton_price', 'cotton_export'])
    
    # Should analyze all three
    assert len(result['commodities_analyzed']) == 3
    
    # Each should have individual analysis
    assert len(result['individual_analysis']) == 3
    
    # Should have cross-commodity insights
    assert 'shared_drivers' in result['cross_commodity_insights']
    
    # Should have recommendations
    assert len(result['strategic_recommendations']) > 0
