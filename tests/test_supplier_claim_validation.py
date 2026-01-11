import pytest
from src.tools.negotiation import validate_supplier_claim


def test_claim_validation_structure():
    """Test supplier claim validation returns required fields."""
    result = validate_supplier_claim("cotton_price", claimed_price=180.0, months_ahead=3)
    
    assert 'claimed_price' in result
    assert 'forecast_median' in result
    assert 'forecast_range' in result
    assert 'difference_abs' in result
    assert 'difference_pct' in result
    assert 'classification' in result
    assert 'verdict' in result


def test_claim_above_forecast():
    """Test claim significantly above forecast is flagged."""
    result = validate_supplier_claim("cotton_price", claimed_price=200.0, months_ahead=3)
    
    # Should be classified as above forecast
    assert 'above' in result['classification']


def test_claim_below_forecast():
    """Test claim below forecast is identified."""
    result = validate_supplier_claim("cotton_price", claimed_price=160.0, months_ahead=3)
    
    # Should be classified as below or aligned
    assert result['classification'] in ['below_forecast', 'below_forecast_range', 'aligned_with_forecast']


def test_claim_aligned_with_forecast():
    """Test claim aligned with forecast."""
    result = validate_supplier_claim("cotton_price", claimed_price=178.0, months_ahead=3)
    
    # Should be reasonably close to forecast
    assert abs(result['difference_pct']) < 10


def test_difference_calculations():
    """Test difference calculations are accurate."""
    result = validate_supplier_claim("cotton_price", claimed_price=180.0, months_ahead=3)
    
    expected_diff = 180.0 - result['forecast_median']
    assert abs(result['difference_abs'] - expected_diff) < 0.01
    
    expected_pct = (expected_diff / result['forecast_median']) * 100
    assert abs(result['difference_pct'] - expected_pct) < 0.1


def test_confidence_intervals():
    """Test confidence intervals are included."""
    result = validate_supplier_claim("cotton_price", claimed_price=180.0)
    
    assert 'forecast_range' in result
    assert 'low' in result['forecast_range']
    assert 'high' in result['forecast_range']
    assert result['forecast_range']['low'] < result['forecast_range']['high']


def test_verdict_provided():
    """Test verdict is provided for negotiation guidance."""
    result = validate_supplier_claim("cotton_price", claimed_price=180.0)
    
    assert 'verdict' in result
    assert isinstance(result['verdict'], str)
    assert len(result['verdict']) > 10


def test_dataset_included():
    """Test dataset name is included in result."""
    result = validate_supplier_claim("energy_futures", claimed_price=90.0)
    
    assert result['dataset'] == 'energy_futures'
