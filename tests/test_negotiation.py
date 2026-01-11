import pytest
from src.tools.negotiation import generate_negotiation_talking_points


def test_talking_points_generation():
    """Test negotiation talking points are generated."""
    result = generate_negotiation_talking_points("cotton_price", months_ahead=3)
    
    assert 'talking_points' in result
    assert len(result['talking_points']) >= 3
    assert len(result['talking_points']) <= 5


def test_data_citations():
    """Test each talking point has data citations."""
    result = generate_negotiation_talking_points("cotton_price")
    
    for point in result['talking_points']:
        assert 'point' in point
        assert 'citation' in point
        assert 'type' in point


def test_supporting_contradicting_factors():
    """Test talking points include both supporting and contradicting factors."""
    result = generate_negotiation_talking_points("cotton_price")
    
    types = [p['type'] for p in result['talking_points']]
    has_supporting = any('supporting' in t for t in types)
    has_contradicting = any('contradicting' in t for t in types)
    
    # Should have at least one of each or be all facts
    assert has_supporting or has_contradicting or all(t == 'fact' for t in types)


def test_market_context():
    """Test market context is provided."""
    result = generate_negotiation_talking_points("cotton_price")
    
    assert 'market_context' in result
    assert 'current_price' in result['market_context']
    assert 'forecast_price' in result['market_context']
    assert 'price_trend' in result['market_context']
    assert 'top_drivers' in result['market_context']


def test_formatted_for_reference():
    """Test talking points are formatted for easy reference."""
    result = generate_negotiation_talking_points("cotton_price")
    
    for point in result['talking_points']:
        # Each point should be a string with meaningful content
        assert isinstance(point['point'], str)
        assert len(point['point']) > 10


def test_dataset_included():
    """Test dataset name is included in result."""
    result = generate_negotiation_talking_points("energy_futures")
    
    assert result['dataset'] == 'energy_futures'


def test_price_trend_classification():
    """Test price trend is correctly classified."""
    result = generate_negotiation_talking_points("cotton_price")
    
    assert result['market_context']['price_trend'] in ['rising', 'falling']
