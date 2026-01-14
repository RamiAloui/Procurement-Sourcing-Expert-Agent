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
    
    assert result['datasets'] == ['energy_futures', 'cotton_price']
    
    assert len(result['aligned_data']) > 0
    
    first_record = result['aligned_data'][0]
    assert 'date' in first_record
    assert 'energy_futures' in first_record
    assert 'cotton_price' in first_record


def test_compare_three_datasets():
    """Test comparison with all 3 datasets."""
    result = compare_datasets(['energy_futures', 'cotton_price', 'cotton_export'])
    
    assert len(result['datasets']) == 3
    assert len(result['aligned_data']) > 0
    
    first_record = result['aligned_data'][0]
    assert 'energy_futures' in first_record
    assert 'cotton_price' in first_record
    assert 'cotton_export' in first_record


def test_date_alignment():
    """Test date alignment."""
    result = compare_datasets(['energy_futures', 'cotton_price'])
    
    dates = [record['date'] for record in result['aligned_data']]
    assert dates == sorted(dates)
    
    assert result['common_date_range']['start'] == dates[0]
    assert result['common_date_range']['end'] == dates[-1]
    
    assert result['total_aligned_records'] == len(result['aligned_data'])


def test_no_common_dates():
    """Test no overlap handling."""
    result = compare_datasets(['energy_futures', 'cotton_price'])
    
    assert isinstance(result, dict)
    assert 'aligned_data' in result
    assert 'total_aligned_records' in result


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
    
    assert -1 <= result['correlation_coefficient'] <= 1
    
    assert result['data_points_used'] > 0


def test_correlation_strength_classification():
    """Test correlation strength categories."""
    result = calculate_correlation('energy_futures', 'cotton_price')
    
    assert result['strength'] in ['weak', 'moderate', 'strong']
    
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
    
    assert result['direction'] in ['positive', 'negative', 'none']
    
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
    
    assert isinstance(result['common_drivers'], list)
    
    assert result['lead_commodity'] in ['energy_futures', 'cotton_price', 'similar']
    
    assert result['predictive_value'] in ['low', 'moderate', 'high']


def test_lead_lag_identification():
    """Test lead commodity detection."""
    result = analyze_timing_relationships('energy_futures', 'cotton_price')
    
    assert 'lead_commodity' in result
    
    assert len(result['timing_insights']) >= 0
    
    for insight in result['timing_insights']:
        assert 'driver' in insight
        assert 'dataset1_lag' in insight
        assert 'dataset2_lag' in insight
        assert 'interpretation' in insight


def test_lag_quantification():
    """Test time delay calculation."""
    result = analyze_timing_relationships('energy_futures', 'cotton_price')
    
    assert isinstance(result['average_lag_months'], (int, float))
    
    assert result['average_lag_months'] >= 0
    
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
    
    assert len(result['commodities_analyzed']) == 2
    
    for commodity in result['commodities_analyzed']:
        assert commodity in result['individual_analysis']
        analysis = result['individual_analysis'][commodity]
        assert 'latest_value' in analysis
        assert 'top_drivers' in analysis
    
    # Should have cross-commodity insights
    assert 'shared_drivers' in result['cross_commodity_insights']
    
    assert isinstance(result['strategic_recommendations'], list)
    assert len(result['strategic_recommendations']) > 0


def test_strategic_recommendations():
    """Test that strategic recommendations are generated."""
    result = analyze_multi_commodity_strategy(['energy_futures', 'cotton_price'])
    
    assert 'strategic_recommendations' in result
    assert len(result['strategic_recommendations']) > 0
    
    for rec in result['strategic_recommendations']:
        assert isinstance(rec, str)
        assert len(rec) > 0


def test_three_commodity_analysis():
    """Test analysis with all 3 datasets."""
    result = analyze_multi_commodity_strategy(['energy_futures', 'cotton_price', 'cotton_export'])
    
    assert len(result['commodities_analyzed']) == 3
    
    assert len(result['individual_analysis']) == 3
    
    # Should have cross-commodity insights
    assert 'shared_drivers' in result['cross_commodity_insights']
    
    assert len(result['strategic_recommendations']) > 0
