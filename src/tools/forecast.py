"""Forecast data query tools."""

from typing import Dict, List
from src.data import DataLoader
from src.tools.historical import get_latest_value


def get_forecast(
    dataset_name: str, 
    months_ahead: int = 1,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get forecast for N months ahead."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    # Get forecast series (0.5 quantile = median/point forecast)
    if months_ahead < 1 or months_ahead > len(forecast_data.forecast_series):
        raise ValueError(
            f"months_ahead must be between 1 and {len(forecast_data.forecast_series)}"
        )
    
    # Forecasts are 0-indexed, so months_ahead=1 is index 0
    date = forecast_data.forecast_series[months_ahead - 1]
    value = forecast_data.quantile_forecast["0.5"][months_ahead - 1]
    
    return {
        'date': date,
        'forecast_value': float(value)
    }


def get_forecast_with_quantiles(
    dataset_name: str,
    months_ahead: int = 1,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get forecast with all quantile levels for risk assessment."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    if months_ahead < 1 or months_ahead > len(forecast_data.forecast_series):
        raise ValueError(
            f"months_ahead must be between 1 and {len(forecast_data.forecast_series)}"
        )
    
    date = forecast_data.forecast_series[months_ahead - 1]
    
    result = {'date': date}
    for quantile, values in forecast_data.quantile_forecast.items():
        result[f'quantile_{quantile}'] = float(values[months_ahead - 1])
    
    return result


def get_forecast_by_date(
    dataset_name: str,
    date: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get forecast for a specific date."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    # Find matching date in forecast series
    try:
        index = forecast_data.forecast_series.index(date)
        value = forecast_data.quantile_forecast["0.5"][index]
        
        return {
            'date': date,
            'forecast_value': float(value)
        }
    except ValueError:
        raise ValueError(f"No forecast found for date {date}")


def get_all_forecasts(
    dataset_name: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> List[Dict]:
    """Get all available forecasts for a dataset."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    # Convert to list of dicts
    return [
        {
            'date': forecast_data.forecast_series[i],
            'forecast_value': float(forecast_data.quantile_forecast["0.5"][i])
        }
        for i in range(len(forecast_data.forecast_series))
    ]


def get_quantile_forecast(
    dataset_name: str,
    date: str,
    quantile: float,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get forecast for a specific quantile."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    # Convert quantile to string key
    quantile_key = str(quantile)
    
    if quantile_key not in forecast_data.quantile_forecast:
        raise ValueError(f"Quantile {quantile} not available")
    
    # Find date index
    try:
        index = forecast_data.forecast_series.index(date)
        value = forecast_data.quantile_forecast[quantile_key][index]
        
        return {
            'date': date,
            'quantile': quantile,
            'forecast_value': float(value)
        }
    except ValueError:
        raise ValueError(f"No forecast found for date {date}")


def get_confidence_interval(
    dataset_name: str,
    date: str,
    confidence_level: int = 80,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get confidence interval for a forecast."""
    # Map confidence levels to quantile pairs (using available quantiles)
    quantile_map = {
        80: (0.15, 0.85),  # 80% confidence interval
        90: (0.05, 0.95)   # 90% confidence interval
    }
    
    if confidence_level not in quantile_map:
        raise ValueError(f"Confidence level must be 80 or 90, got {confidence_level}")
    
    lower_q, upper_q = quantile_map[confidence_level]
    
    # Get lower bound, upper bound, and median
    lower = get_quantile_forecast(dataset_name, date, lower_q, data_path)
    upper = get_quantile_forecast(dataset_name, date, upper_q, data_path)
    median = get_quantile_forecast(dataset_name, date, 0.5, data_path)
    
    return {
        'date': date,
        'confidence_level': confidence_level,
        'lower_bound': lower['forecast_value'],
        'upper_bound': upper['forecast_value'],
        'median': median['forecast_value']
    }


def compare_current_to_forecast(
    dataset_name: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Compare current price with next forecast."""
    # Get latest historical value
    current = get_latest_value(dataset_name, data_path)
    
    # Get next forecast (1 month ahead)
    forecast = get_forecast(dataset_name, months_ahead=1, data_path=data_path)
    
    # Calculate difference and percentage change
    current_value = current['value']
    forecast_value = forecast['forecast_value']
    
    difference = forecast_value - current_value
    pct_change = ((forecast_value - current_value) / current_value) * 100
    pct_change = round(pct_change, 2)
    
    # Determine trend
    if pct_change > 0:
        trend = "increasing"
    elif pct_change < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        'current_date': current['date'],
        'current_value': current_value,
        'forecast_date': forecast['date'],
        'forecast_value': forecast_value,
        'difference': round(difference, 2),
        'percentage_change': pct_change,
        'trend_direction': trend
    }


def analyze_forecast_trend(
    dataset_name: str,
    months_ahead: int = 3,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Analyze forecast trend over multiple months."""
    loader = DataLoader(data_path)
    forecast_data = loader.load_forecast(dataset_name)
    
    # Validate months_ahead
    if months_ahead < 2 or months_ahead > len(forecast_data.forecast_series):
        raise ValueError(
            f"months_ahead must be between 2 and {len(forecast_data.forecast_series)}"
        )
    
    # Get forecast values for the period (0.5 quantile = point forecast)
    forecast_values = forecast_data.quantile_forecast["0.5"][:months_ahead]
    forecast_dates = forecast_data.forecast_series[:months_ahead]
    
    # Calculate percentage changes between consecutive months
    pct_changes = []
    for i in range(1, len(forecast_values)):
        prev_value = float(forecast_values[i-1])
        curr_value = float(forecast_values[i])
        pct_change = ((curr_value - prev_value) / prev_value) * 100
        pct_changes.append(round(pct_change, 2))
    
    # Calculate average change
    avg_change = round(sum(pct_changes) / len(pct_changes), 2)
    
    # Determine overall trend
    if avg_change > 0:
        trend = "increasing"
    elif avg_change < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        'start_date': forecast_dates[0],
        'end_date': forecast_dates[-1],
        'start_value': float(forecast_values[0]),
        'end_value': float(forecast_values[-1]),
        'months_analyzed': months_ahead,
        'average_monthly_change': avg_change,
        'trend_direction': trend,
        'monthly_changes': pct_changes
    }
