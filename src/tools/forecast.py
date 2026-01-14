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
    
    # Check if dataset was found
    if forecast_data is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the energy_futures forecast for next month?",
                "Show me cotton_price forecast",
                "Compare current and forecast prices for energy_futures"
            ]
        }
    
    max_horizon = len(forecast_data.forecast_series)
    
    # Validataion of forecast horizon
    if months_ahead < 1 or months_ahead > max_horizon:
        return {
            'success': False,
            'error': 'forecast_out_of_range',
            'message': f"Forecast for {months_ahead} months ahead is not available. Maximum forecast horizon is {max_horizon} months.",
            'max_horizon': max_horizon,
            'available_range': {'min_months': 1, 'max_months': max_horizon},
            'alternatives': [
                f"What's the {dataset_name} forecast for {max_horizon} months ahead?",
                f"Show me the {dataset_name} forecast for next month",
                f"What's the {dataset_name} trend over the next 3 months?"
            ]
        }
    
    # Note : Forecasts are 0-indexed, so months_ahead=1 is index 0
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
    
    # Check if dataset was found
    if forecast_data is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the energy_futures forecast for next month?",
                "Show me cotton_price forecast",
                "Compare current and forecast prices for energy_futures"
            ]
        }
    
    max_horizon = len(forecast_data.forecast_series)
    
    if months_ahead < 1 or months_ahead > max_horizon:
        return {
            'success': False,
            'error': 'forecast_out_of_range',
            'message': f"Forecast for {months_ahead} months ahead is not available. Maximum forecast horizon is {max_horizon} months.",
            'max_horizon': max_horizon
        }
    
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
    
    # Check if dataset was found
    if forecast_data is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the energy_futures forecast for next month?",
                "Show me cotton_price forecast",
                "Compare current and forecast prices for energy_futures"
            ]
        }
    
    # Available forecast date range
    min_forecast_date = forecast_data.forecast_series[0]
    max_forecast_date = forecast_data.forecast_series[-1]
    
    # Checking if date is out of forecast range
    if date < min_forecast_date or date > max_forecast_date:
        return {
            'success': False,
            'error': 'date_out_of_forecast_range',
            'message': f"No forecast available for {date}. Forecasts are available from {min_forecast_date} to {max_forecast_date}.",
            'available_range': {'start': min_forecast_date, 'end': max_forecast_date}
        }
    
    # Matching date in forecast series
    try:
        index = forecast_data.forecast_series.index(date)
        value = forecast_data.quantile_forecast["0.5"][index]
        
        return {
            'date': date,
            'forecast_value': float(value)
        }
    except ValueError:
        return {
            'success': False,
            'error': 'date_not_in_forecast',
            'message': f"No forecast found for date {date}. Available range: {min_forecast_date} to {max_forecast_date}.",
            'available_range': {'start': min_forecast_date, 'end': max_forecast_date}
        }


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
    if forecast_data is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the energy_futures forecast for next month?",
                "Show me cotton_price forecast",
                "Compare current and forecast prices for energy_futures"
            ]
        }
    
    quantile_key = str(quantile)
    
    if quantile_key not in forecast_data.quantile_forecast:
        available_quantiles = list(forecast_data.quantile_forecast.keys())
        return {
            'success': False,
            'error': 'quantile_not_available',
            'message': f"Quantile {quantile} not available. Available quantiles: {', '.join(available_quantiles)}",
            'available_quantiles': available_quantiles
        }
    
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
    # Map confidence levels to quantile pairs
    quantile_map = {
        80: (0.15, 0.85),  # 80% confidence interval
        90: (0.05, 0.95)   # 90% confidence interval
    }
    
    if confidence_level not in quantile_map:
        return {
            'success': False,
            'error': 'invalid_confidence_level',
            'message': f"Confidence level {confidence_level}% not supported. Available levels: 80%, 90%",
            'available_levels': [80, 90]
        }
    
    lower_q, upper_q = quantile_map[confidence_level]
    
    # Lower bound, upper bound, and median
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
    # Latest historical value
    current = get_latest_value(dataset_name, data_path)
    
    # Next forecast (1 month ahead)
    forecast = get_forecast(dataset_name, months_ahead=1, data_path=data_path)
    
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
    
    # Check if dataset was found
    if forecast_data is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the energy_futures forecast for next month?",
                "Show me cotton_price forecast",
                "Compare current and forecast prices for energy_futures"
            ]
        }
    
    max_horizon = len(forecast_data.forecast_series)
    
    # Validate months_ahead
    if months_ahead < 2 or months_ahead > max_horizon:
        return {
            'success': False,
            'error': 'forecast_out_of_range',
            'message': f"Forecast trend analysis requires at least 2 months. Maximum available: {max_horizon} months.",
            'max_horizon': max_horizon
        }
    
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
    
    # Overall trend
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
