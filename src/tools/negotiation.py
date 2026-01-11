"""Negotiation support tools."""

from typing import Dict
from src.tools.historical import get_latest_value
from src.tools.forecast import get_forecast, get_forecast_with_quantiles
from src.tools.drivers import get_top_drivers, get_driver_details


def generate_negotiation_talking_points(
    dataset_name: str,
    months_ahead: int = 3,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Generate negotiation talking points with data citations."""
    current = get_latest_value(dataset_name, data_path)
    forecast = get_forecast(dataset_name, months_ahead, data_path)
    drivers = get_top_drivers(dataset_name, top_n=5, data_path=data_path)
    
    price_change = forecast['forecast_value'] - current['value']
    pct_change = (price_change / current['value']) * 100
    
    talking_points = []
    
    # Point 1: Current market price
    talking_points.append({
        'point': f"Current market price is ${current['value']:.2f} as of {current['date']}",
        'type': 'fact',
        'citation': f"Historical data: {dataset_name}"
    })
    
    # Point 2: Forecast trend
    if pct_change > 0:
        talking_points.append({
            'point': f"Forecast shows {pct_change:.1f}% increase to ${forecast['forecast_value']:.2f} by {forecast['date']}",
            'type': 'supporting_increase',
            'citation': f"Forecast data: {dataset_name}"
        })
    else:
        talking_points.append({
            'point': f"Forecast shows {abs(pct_change):.1f}% decrease to ${forecast['forecast_value']:.2f} by {forecast['date']}",
            'type': 'contradicting_increase',
            'citation': f"Forecast data: {dataset_name}"
        })
    
    # Point 3-5: Top drivers with direction details
    for driver in drivers[:3]:
        try:
            driver_detail = get_driver_details(dataset_name, driver['name'], data_path)
            direction = driver_detail.get('direction', 'neutral')
            driver_type = 'supporting_increase' if direction == 'positive' else 'contradicting_increase'
            talking_points.append({
                'point': f"{driver['name']} ({driver['importance_mean']:.1f}% importance) shows {direction} correlation",
                'type': driver_type,
                'citation': f"Driver analysis: {dataset_name}"
            })
        except (ValueError, KeyError):
            # If driver details not available, skip this driver
            continue
    
    return {
        'dataset': dataset_name,
        'talking_points': talking_points,
        'market_context': {
            'current_price': current['value'],
            'forecast_price': forecast['forecast_value'],
            'price_trend': 'rising' if pct_change > 0 else 'falling',
            'top_drivers': [d['name'] for d in drivers[:3]]
        }
    }


def validate_supplier_claim(
    dataset_name: str,
    claimed_price: float,
    months_ahead: int = 3,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Validate supplier price claim against forecast data."""
    current = get_latest_value(dataset_name, data_path)
    forecast_data = get_forecast_with_quantiles(dataset_name, months_ahead, data_path)
    
    # Get median (always 0.5)
    forecast_median = forecast_data['quantile_0.5']
    
    # Get low/high quantiles - different datasets have different quantiles available
    # Try 0.1/0.9 first, fall back to 0.05/0.95 or 0.15/0.85
    forecast_low = (forecast_data.get('quantile_0.1') or 
                   forecast_data.get('quantile_0.05') or 
                   forecast_data.get('quantile_0.15'))
    forecast_high = (forecast_data.get('quantile_0.9') or 
                    forecast_data.get('quantile_0.95') or 
                    forecast_data.get('quantile_0.85'))
    
    diff_abs = claimed_price - forecast_median
    diff_pct = (diff_abs / forecast_median) * 100
    
    if claimed_price > forecast_high:
        classification = 'above_forecast_range'
        verdict = 'Challenge this claim - significantly above forecast'
    elif claimed_price < forecast_low:
        classification = 'below_forecast_range'
        verdict = 'Excellent deal - below forecast range'
    elif claimed_price > forecast_median + (forecast_median * 0.02):
        classification = 'above_forecast'
        verdict = 'Negotiate down - above expected forecast'
    elif claimed_price < forecast_median - (forecast_median * 0.02):
        classification = 'below_forecast'
        verdict = 'Good deal - below expected forecast'
    else:
        classification = 'aligned_with_forecast'
        verdict = 'Reasonable - aligned with forecast'
    
    return {
        'dataset': dataset_name,
        'claimed_price': claimed_price,
        'forecast_median': round(forecast_median, 2),
        'forecast_range': {
            'low': round(forecast_low, 2),
            'high': round(forecast_high, 2)
        },
        'difference_abs': round(diff_abs, 2),
        'difference_pct': round(diff_pct, 2),
        'classification': classification,
        'verdict': verdict,
        'current_price': current['value'],
        'forecast_date': forecast_data['date']
    }


def identify_driver_arguments(
    dataset_name: str,
    price_direction: str = 'increase',
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Identify drivers supporting or contradicting price movements."""
    drivers = get_top_drivers(dataset_name, top_n=10, data_path=data_path)
    
    supporting = []
    contradicting = []
    
    for driver in drivers:
        # Get driver details to determine direction
        try:
            driver_detail = get_driver_details(dataset_name, driver['name'], data_path)
            is_positive = driver_detail.get('direction', 'neutral') == 'positive'
            
            if price_direction == 'increase':
                if is_positive:
                    supporting.append(driver)
                else:
                    contradicting.append(driver)
            else:  # decrease
                if is_positive:
                    contradicting.append(driver)
                else:
                    supporting.append(driver)
        except (ValueError, KeyError):
            # Skip drivers without direction info
            continue
    
    return {
        'dataset': dataset_name,
        'price_direction': price_direction,
        'supporting_drivers': supporting[:5],
        'contradicting_drivers': contradicting[:5],
        'balance': {
            'supporting_count': len(supporting),
            'contradicting_count': len(contradicting),
            'net_sentiment': 'bullish' if len(supporting) > len(contradicting) else 'bearish'
        }
    }
