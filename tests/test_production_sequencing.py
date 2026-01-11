import pytest
from src.tools.recommendations import recommend_production_sequencing


def test_production_sequencing():
    """Test production sequencing recommendations."""
    datasets = ["cotton_price", "energy_futures", "cotton_export"]
    result = recommend_production_sequencing(datasets, months_ahead=3)
    
    assert len(result['datasets_analyzed']) == 3
    assert len(result['recommended_sequence']) == 3
    assert 'favorable_commodities' in result
    assert 'unfavorable_commodities' in result


def test_favorable_prioritization():
    """Test favorable commodities are prioritized first."""
    datasets = ["cotton_price", "energy_futures"]
    result = recommend_production_sequencing(datasets)
    
    first = result['recommended_sequence'][0]
    last = result['recommended_sequence'][-1]
    
    commodity_map = {c['dataset']: c for c in result['commodity_analysis']}
    assert commodity_map[first['dataset']]['priority'] <= commodity_map[last['dataset']]['priority']


def test_favorability_classification():
    """Test commodities are classified correctly."""
    datasets = ["cotton_price", "energy_futures"]
    result = recommend_production_sequencing(datasets)
    
    for commodity in result['commodity_analysis']:
        if commodity['price_change_pct'] <= 0:
            assert commodity['favorability'] == 'favorable'
        elif commodity['price_change_pct'] <= 2:
            assert commodity['favorability'] == 'moderately_favorable'
        else:
            assert commodity['favorability'] == 'unfavorable'


def test_cost_impact_summary():
    """Test cost impact summary is calculated."""
    datasets = ["cotton_price", "energy_futures"]
    result = recommend_production_sequencing(datasets)
    
    assert 'cost_impact_summary' in result
    assert 'favorable_trend' in result['cost_impact_summary']
    assert 'unfavorable_trend' in result['cost_impact_summary']


def test_sequence_order():
    """Test sequence has correct ordering."""
    datasets = ["cotton_price", "energy_futures", "cotton_export"]
    result = recommend_production_sequencing(datasets)
    
    for i, item in enumerate(result['recommended_sequence'], 1):
        assert item['sequence_order'] == i


def test_insights_generation():
    """Test insights are generated."""
    datasets = ["cotton_price", "energy_futures"]
    result = recommend_production_sequencing(datasets)
    
    assert 'insights' in result
    assert isinstance(result['insights'], list)


def test_single_commodity():
    """Test sequencing works with single commodity."""
    datasets = ["cotton_price"]
    result = recommend_production_sequencing(datasets)
    
    assert len(result['datasets_analyzed']) == 1
    assert len(result['recommended_sequence']) == 1


def test_commodity_analysis_structure():
    """Test commodity analysis has required fields."""
    datasets = ["cotton_price", "energy_futures"]
    result = recommend_production_sequencing(datasets)
    
    required_fields = ['dataset', 'current_price', 'forecast_price', 
                      'price_change_pct', 'favorability', 'priority']
    
    for commodity in result['commodity_analysis']:
        for field in required_fields:
            assert field in commodity
