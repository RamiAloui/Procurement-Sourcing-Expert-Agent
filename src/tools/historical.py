"""Historical data query tools."""

from typing import Dict, List
import numpy as np
from src.data import DataLoader


def get_latest_value(dataset_name: str, data_path: str = "Agents - Code Challenge/Data") -> Dict:
    """Get the most recent historical value for a dataset."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Check if dataset was found
    if df is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the latest energy_futures price?",
                "Show me cotton_price trends",
                "Compare energy_futures and cotton_price"
            ]
        }
    
    # Last row
    latest = df.iloc[-1]
    
    return {
        'date': latest['Period'],
        'value': float(latest['Value'])
    }


def get_value_by_date(dataset_name: str, date: str, data_path: str = "Agents - Code Challenge/Data") -> Dict:
    """Get historical value for a specific date."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Check if dataset was found
    if df is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the latest energy_futures price?",
                "Show me cotton_price trends",
                "Compare energy_futures and cotton_price"
            ]
        }
    
    # Available date range
    min_date = df['Period'].min()
    max_date = df['Period'].max()
    
    # Check if date is out of range
    if date < min_date:
        return {
            'success': False,
            'error': 'date_out_of_range',
            'message': f"The date {date} is before available data range ({min_date} to {max_date}). Would you like data from {min_date} instead?",
            'available_range': {'start': min_date, 'end': max_date},
            'suggested_date': min_date,
            'alternatives': [
                f"What's the {dataset_name} price on {min_date}?",
                f"Show me the latest {dataset_name} price",
                f"What's the {dataset_name} trend from {min_date} to {max_date}?"
            ]
        }
    
    if date > max_date:
        return {
            'success': False,
            'error': 'date_out_of_range',
            'message': f"The date {date} is after available data range ({min_date} to {max_date}). Would you like data from {max_date} instead?",
            'available_range': {'start': min_date, 'end': max_date},
            'suggested_date': max_date,
            'alternatives': [
                f"What's the {dataset_name} price on {max_date}?",
                f"Show me the latest {dataset_name} price",
                f"What's the {dataset_name} forecast for the next 3 months?"
            ]
        }
    
    # Filter by date
    result = df[df['Period'] == date]
    
    if result.empty:
        # Date is in range but not in data
        return {
            'success': False,
            'error': 'date_not_found',
            'message': f"No data found for date {date}. Data is available from {min_date} to {max_date}.",
            'available_range': {'start': min_date, 'end': max_date}
        }
    
    return {
        'date': date,
        'value': float(result.iloc[0]['Value'])
    }


def get_values_by_range(
    dataset_name: str, 
    start_date: str, 
    end_date: str,
    data_path: str = "Agents - Code Challenge/Data"
):
    """Get historical values for a date range."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Check if dataset was found
    if df is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the latest energy_futures price?",
                "Show me cotton_price trends",
                "Compare energy_futures and cotton_price"
            ]
        }
    
    # Get available date range
    min_date = df['Period'].min()
    max_date = df['Period'].max()
    
    # Check if requested range is out
    if start_date < min_date or end_date > max_date:
        return {
            'success': False,
            'error': 'date_range_out_of_bounds',
            'message': f"Requested range ({start_date} to {end_date}) is outside available data ({min_date} to {max_date}).",
            'available_range': {'start': min_date, 'end': max_date},
            'suggested_range': {'start': max(start_date, min_date), 'end': min(end_date, max_date)}
        }
    
    # Filter by date range
    mask = (df['Period'] >= start_date) & (df['Period'] <= end_date)
    result = df[mask]
    
    if result.empty:
        return []
    
    # Convert to list of dicts
    return [
        {'date': row['Period'], 'value': float(row['Value'])}
        for _, row in result.iterrows()
    ]


def calculate_percentage_change(
    dataset_name: str,
    start_date: str,
    end_date: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Calculate percentage change between two dates."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Check if dataset was found
    if df is None:
        return {
            'success': False,
            'error': 'dataset_not_found',
            'message': f"Dataset '{dataset_name}' not found. Available datasets: energy_futures, cotton_price, cotton_export",
            'available_datasets': ['energy_futures', 'cotton_price', 'cotton_export'],
            'alternatives': [
                "What's the latest energy_futures price?",
                "Show me cotton_price trends",
                "Compare energy_futures and cotton_price"
            ]
        }
    
    # Available date range
    min_date = df['Period'].min()
    max_date = df['Period'].max()
    
    # Check if dates are out of range
    if start_date < min_date or end_date > max_date:
        return {
            'success': False,
            'error': 'date_out_of_range',
            'message': f"One or both dates are outside available range ({min_date} to {max_date}).",
            'available_range': {'start': min_date, 'end': max_date}
        }
    
    # Values for dates
    start_row = df[df['Period'] == start_date]
    end_row = df[df['Period'] == end_date]
    
    if start_row.empty or end_row.empty:
        return {
            'success': False,
            'error': 'date_not_found',
            'message': f"One or both dates not found in data. Available range: {min_date} to {max_date}.",
            'available_range': {'start': min_date, 'end': max_date}
        }
    
    start_value = float(start_row.iloc[0]['Value'])
    end_value = float(end_row.iloc[0]['Value'])
    
    # Calculation of percentage change
    pct_change = ((end_value - start_value) / start_value) * 100
    pct_change = round(pct_change, 2)
    
    # Determination of trend
    if pct_change > 0:
        trend = "increasing"
    elif pct_change < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'start_value': start_value,
        'end_value': end_value,
        'percentage_change': pct_change,
        'trend_direction': trend
    }


def get_trend_direction(
    dataset_name: str,
    start_date: str,
    end_date: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> str:
    """Get trend direction between two dates."""
    result = calculate_percentage_change(dataset_name, start_date, end_date, data_path)
    return result['trend_direction']


def find_peak(
    dataset_name: str,
    start_date: str = None,
    end_date: str = None,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Find highest value (peak) in historical data."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Filter by date range if provided
    if start_date and end_date:
        mask = (df['Period'] >= start_date) & (df['Period'] <= end_date)
        df = df[mask]
    
    # Max value
    max_idx = df['Value'].idxmax()
    peak_row = df.loc[max_idx]
    
    return {
        'date': peak_row['Period'],
        'value': float(peak_row['Value']),
        'type': 'peak'
    }


def find_valley(
    dataset_name: str,
    start_date: str = None,
    end_date: str = None,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Find lowest value (valley) in historical data."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Filter by date range if provided
    if start_date and end_date:
        mask = (df['Period'] >= start_date) & (df['Period'] <= end_date)
        df = df[mask]
    
    # Min value
    min_idx = df['Value'].idxmin()
    valley_row = df.loc[min_idx]
    
    return {
        'date': valley_row['Period'],
        'value': float(valley_row['Value']),
        'type': 'valley'
    }


def find_peak_and_valley(
    dataset_name: str,
    start_date: str = None,
    end_date: str = None,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Find both peak and valley in historical data."""
    peak = find_peak(dataset_name, start_date, end_date, data_path)
    valley = find_valley(dataset_name, start_date, end_date, data_path)
    
    return {
        'peak': peak,
        'valley': valley
    }


def calculate_moving_average(
    dataset_name: str,
    window_size: int = 7,
    start_date: str = None,
    end_date: str = None,
    data_path: str = "Agents - Code Challenge/Data"
) -> List[Dict]:
    """Calculate moving average for historical data."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Filter by date range if provided
    if start_date and end_date:
        mask = (df['Period'] >= start_date) & (df['Period'] <= end_date)
        df = df[mask].copy()
    
    # Calculation of moving average
    df['MA'] = df['Value'].rolling(window=window_size).mean()
    
    # Drop NaN values
    df = df.dropna()
    
    # Convert to list of dicts
    return [
        {'date': row['Period'], 'moving_average': round(float(row['MA']), 2)}
        for _, row in df.iterrows()
    ]


def calculate_trend_line(
    dataset_name: str,
    start_date: str = None,
    end_date: str = None,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Calculate trend line using linear regression."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Filter by date range if provided
    if start_date and end_date:
        mask = (df['Period'] >= start_date) & (df['Period'] <= end_date)
        df = df[mask].copy()
    
    # Create x values
    x = np.arange(len(df))
    y = df['Value'].values
    
    # Linear regression
    slope, intercept = np.polyfit(x, y, 1)
    
    #  Trend
    if slope > 0:
        trend = "increasing"
    elif slope < 0:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        'slope': round(float(slope), 4),
        'intercept': round(float(intercept), 2),
        'trend_direction': trend
    }
