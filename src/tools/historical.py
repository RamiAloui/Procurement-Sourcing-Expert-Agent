"""Historical data query tools."""

from typing import Dict, List
import numpy as np
from src.data import DataLoader


def get_latest_value(dataset_name: str, data_path: str = "Agents - Code Challenge/Data") -> Dict:
    """Get the most recent historical value for a dataset."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Get last row
    latest = df.iloc[-1]
    
    return {
        'date': latest['Period'],
        'value': float(latest['Value'])
    }


def get_value_by_date(dataset_name: str, date: str, data_path: str = "Agents - Code Challenge/Data") -> Dict:
    """Get historical value for a specific date."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
    # Filter by date
    result = df[df['Period'] == date]
    
    if result.empty:
        raise ValueError(f"No data found for date {date}")
    
    return {
        'date': date,
        'value': float(result.iloc[0]['Value'])
    }


def get_values_by_range(
    dataset_name: str, 
    start_date: str, 
    end_date: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> List[Dict]:
    """Get historical values for a date range."""
    loader = DataLoader(data_path)
    df = loader.load_historical(dataset_name)
    
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
    
    # Get values for dates
    start_row = df[df['Period'] == start_date]
    end_row = df[df['Period'] == end_date]
    
    if start_row.empty or end_row.empty:
        raise ValueError(f"Date not found in data")
    
    start_value = float(start_row.iloc[0]['Value'])
    end_value = float(end_row.iloc[0]['Value'])
    
    # Calculate percentage change
    pct_change = ((end_value - start_value) / start_value) * 100
    pct_change = round(pct_change, 2)
    
    # Determine trend
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
    
    # Find max value
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
    
    # Find min value
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
    
    # Calculate moving average
    df['MA'] = df['Value'].rolling(window=window_size).mean()
    
    # Drop NaN values (first window_size-1 rows)
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
    
    # Create x values (0, 1, 2, ...)
    x = np.arange(len(df))
    y = df['Value'].values
    
    # Calculate linear regression
    slope, intercept = np.polyfit(x, y, 1)
    
    # Determine trend
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
