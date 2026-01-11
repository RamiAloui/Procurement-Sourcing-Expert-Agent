import pytest
from src.tools.recommendations import calculate_impact_analysis


def test_impact_analysis_structure():
    """Test impact analysis returns all required fields."""
    result = calculate_impact_analysis("cotton_price", months_ahead=3)
    
    assert 'best_case' in result
    assert 'expected' in result
    assert 'worst_case' in result
    assert 'confidence_range' in result
    assert 'price_direction' in result
    assert result['quantity'] == 1000


def test_best_expected_worst_order():
    """Test scenarios are ordered correctly based on price direction."""
    result = calculate_impact_analysis("cotton_price", months_ahead=3)
    
    if result['price_direction'] == 'rising':
        assert result['best_case']['forecast_price'] <= result['expected']['forecast_price']
        assert result['expected']['forecast_price'] <= result['worst_case']['forecast_price']
    else:
        assert result['best_case']['forecast_price'] >= result['expected']['forecast_price']
        assert result['expected']['forecast_price'] >= result['worst_case']['forecast_price']


def test_calculation_accuracy():
    """Test calculations are accurate to 2 decimal places."""
    result = calculate_impact_analysis("cotton_price", quantity=500)
    
    assert result['current_price'] == round(result['current_price'], 2)
    assert result['best_case']['forecast_price'] == round(result['best_case']['forecast_price'], 2)
    assert result['expected']['total_impact'] == round(result['expected']['total_impact'], 2)
    assert result['worst_case']['price_change_pct'] == round(result['worst_case']['price_change_pct'], 2)


def test_total_impact_calculation():
    """Test total impact = price_change × quantity."""
    result = calculate_impact_analysis("cotton_price", quantity=500)
    
    expected_impact = result['expected']['price_change_abs'] * 500
    assert abs(result['expected']['total_impact'] - expected_impact) < 1.0


def test_percentage_calculation():
    """Test percentage change calculation."""
    result = calculate_impact_analysis("cotton_price")
    
    current = result['current_price']
    expected_pct = ((result['expected']['forecast_price'] - current) / current) * 100
    assert abs(result['expected']['price_change_pct'] - expected_pct) < 0.1


def test_confidence_range():
    """Test confidence range includes min, median, max."""
    result = calculate_impact_analysis("cotton_price")
    
    assert 'min' in result['confidence_range']
    assert 'median' in result['confidence_range']
    assert 'max' in result['confidence_range']
    assert result['confidence_range']['min'] <= result['confidence_range']['median']
    assert result['confidence_range']['median'] <= result['confidence_range']['max']


def test_custom_quantity():
    """Test custom quantity affects total impact."""
    result_1000 = calculate_impact_analysis("cotton_price", quantity=1000)
    result_2000 = calculate_impact_analysis("cotton_price", quantity=2000)
    
    assert result_2000['expected']['total_impact'] == result_1000['expected']['total_impact'] * 2


def test_scenario_fields():
    """Test each scenario has all required fields."""
    result = calculate_impact_analysis("cotton_price")
    
    required_fields = ['scenario', 'forecast_price', 'price_change_abs', 
                      'price_change_pct', 'total_impact', 'impact_per_unit']
    
    for scenario in ['best_case', 'expected', 'worst_case']:
        for field in required_fields:
            assert field in result[scenario]
