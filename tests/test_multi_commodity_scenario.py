import pytest
from src.tools.recommendations import analyze_multi_commodity_scenario


def test_multi_commodity_analysis():
    """Test multi-commodity scenario analysis."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets, months_ahead=3)
    
    assert len(result['datasets_analyzed']) == 2
    assert 'individual_recommendations' in result
    assert 'prioritized_actions' in result
    assert len(result['prioritized_actions']) == 2


def test_prioritization_order():
    """Test recommendations are prioritized by urgency."""
    datasets = ["cotton_price", "energy_futures", "cotton_export"]
    result = analyze_multi_commodity_scenario(datasets)
    
    urgencies = [p['urgency_score'] for p in result['prioritized_actions']]
    assert urgencies == sorted(urgencies, reverse=True)


def test_correlation_insights():
    """Test correlation insights are included when applicable."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets)
    
    assert 'correlation_data' in result
    assert 'insights' in result


def test_total_savings_calculation():
    """Test total potential savings is sum of individual savings."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets, quantity=500)
    
    expected_total = sum(
        rec['savings'] 
        for rec in result['individual_recommendations'].values()
    )
    assert result['total_potential_savings'] == expected_total


def test_single_commodity():
    """Test analysis works with single commodity."""
    datasets = ["cotton_price"]
    result = analyze_multi_commodity_scenario(datasets)
    
    assert len(result['datasets_analyzed']) == 1
    assert len(result['prioritized_actions']) == 1


def test_urgency_scoring():
    """Test urgency scoring logic."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets)
    
    for action in result['prioritized_actions']:
        assert 'urgency_score' in action
        assert action['urgency_score'] >= 1


def test_individual_recommendations_structure():
    """Test individual recommendations have correct structure."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets)
    
    for dataset in datasets:
        assert dataset in result['individual_recommendations']
        rec = result['individual_recommendations'][dataset]
        assert 'recommendation' in rec
        assert 'savings' in rec
        assert 'price_change_pct' in rec


def test_prioritized_actions_structure():
    """Test prioritized actions have required fields."""
    datasets = ["cotton_price", "energy_futures"]
    result = analyze_multi_commodity_scenario(datasets)
    
    required_fields = ['dataset', 'recommendation', 'urgency_score', 
                      'price_change_pct', 'savings', 'rationale']
    
    for action in result['prioritized_actions']:
        for field in required_fields:
            assert field in action
