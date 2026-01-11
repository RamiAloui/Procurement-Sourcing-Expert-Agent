import pytest
from src.tools.negotiation import identify_driver_arguments


def test_driver_arguments_structure():
    """Test driver arguments returns required fields."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    assert 'dataset' in result
    assert 'price_direction' in result
    assert 'supporting_drivers' in result
    assert 'contradicting_drivers' in result
    assert 'balance' in result


def test_supporting_drivers_for_increase():
    """Test supporting drivers are identified for price increases."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    assert isinstance(result['supporting_drivers'], list)
    assert len(result['supporting_drivers']) <= 5


def test_contradicting_drivers_for_increase():
    """Test contradicting drivers are identified for price increases."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    assert isinstance(result['contradicting_drivers'], list)
    assert len(result['contradicting_drivers']) <= 5


def test_supporting_drivers_for_decrease():
    """Test supporting drivers are identified for price decreases."""
    result = identify_driver_arguments("cotton_price", price_direction='decrease')
    
    assert isinstance(result['supporting_drivers'], list)


def test_driver_ranking():
    """Test drivers are ranked by importance."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    for driver in result['supporting_drivers']:
        assert 'importance_mean' in driver
        assert 'name' in driver


def test_balance_calculation():
    """Test balance between supporting and contradicting drivers."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    assert 'balance' in result
    assert 'supporting_count' in result['balance']
    assert 'contradicting_count' in result['balance']
    assert 'net_sentiment' in result['balance']


def test_net_sentiment():
    """Test net sentiment is calculated correctly."""
    result = identify_driver_arguments("cotton_price", price_direction='increase')
    
    sentiment = result['balance']['net_sentiment']
    assert sentiment in ['bullish', 'bearish']


def test_price_direction_parameter():
    """Test price_direction parameter is respected."""
    result_increase = identify_driver_arguments("cotton_price", price_direction='increase')
    result_decrease = identify_driver_arguments("cotton_price", price_direction='decrease')
    
    assert result_increase['price_direction'] == 'increase'
    assert result_decrease['price_direction'] == 'decrease'
