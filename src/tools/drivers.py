"""Market driver analysis tools."""

from typing import Dict, List
from src.data import DataLoader


def get_top_drivers(
    dataset_name: str,
    top_n: int = 5,
    data_path: str = "Agents - Code Challenge/Data"
) -> List[Dict]:
    """Get top N market drivers sorted by importance score.
    
    Args:
        dataset_name: Name of dataset
        top_n: Number of top drivers to return (default: 5)
        data_path: Path to data directory
    
    Returns list of dicts with driver name and importance metrics.
    """
    loader = DataLoader(data_path)
    drivers_data = loader.load_drivers(dataset_name)
    
    # Extract drivers (skip target entry)
    drivers = []
    for driver_id, driver_info in drivers_data.items():
        # Skip target entry (doesn't have importance scores)
        if 'importance' not in driver_info:
            continue
        
        # Extract importance metrics
        importance = driver_info.get('importance', {}).get('overall', {})
        
        drivers.append({
            'name': driver_info.get('driver_name', 'Unknown'),
            'importance_mean': importance.get('mean', 0.0),
            'importance_max': importance.get('max', 0.0),
            'importance_min': importance.get('min', 0.0)
        })
    
    # Sort by mean importance descending
    drivers.sort(key=lambda x: x['importance_mean'], reverse=True)
    
    # Return top N
    return drivers[:top_n]


def get_driver_details(
    dataset_name: str,
    driver_name: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Get detailed information for a specific driver.
    
    Args:
        dataset_name: Name of dataset
        driver_name: Name of the driver to query
        data_path: Path to data directory
    
    Returns dict with driver details including direction and correlations.
    """
    loader = DataLoader(data_path)
    drivers_data = loader.load_drivers(dataset_name)
    
    # Find driver by name
    driver_info = None
    for driver_id, info in drivers_data.items():
        if info.get('driver_name') == driver_name:
            driver_info = info
            break
    
    if not driver_info:
        raise ValueError(f"Driver not found: {driver_name}")
    
    # Extract direction
    direction_value = driver_info.get('direction', {}).get('overall', {}).get('mean', 0)
    if direction_value is None:
        direction_value = 0
    direction = "positive" if direction_value > 0 else "negative"
    
    # Direction explanation
    if direction == "positive":
        explanation = "When this driver increases, prices tend to increase"
    else:
        explanation = "When this driver increases, prices tend to decrease"
    
    # Extract Pearson correlation
    pearson = driver_info.get('pearson_correlation', {}).get('overall', {})
    
    # Extract Granger causality
    granger = driver_info.get('granger_correlation', {}).get('overall', {})
    
    # Extract lag information
    lag_str = driver_info.get('overall_lag')
    lag_explanation = None
    
    if lag_str:
        # Parse lag string to create user-friendly explanation
        lag_explanation = f"Impact occurs {lag_str} after driver changes"
    else:
        lag_explanation = "Lag information not available"
    
    return {
        'name': driver_name,
        'direction': direction,
        'direction_explanation': explanation,
        'pearson_correlation': {
            'mean': pearson.get('mean', 0.0),
            'max': pearson.get('max', 0.0),
            'min': pearson.get('min', 0.0)
        },
        'granger_causality': {
            'mean': granger.get('mean', 0.0),
            'max': granger.get('max', 0.0),
            'min': granger.get('min', 0.0)
        },
        'lag': lag_str,
        'lag_explanation': lag_explanation
    }


def analyze_drivers_combined(
    dataset_name: str,
    top_n: int = 10,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Analyze multiple drivers together to understand combined effects.
    
    Args:
        dataset_name: Name of dataset
        top_n: Number of top drivers to analyze (default: 10)
        data_path: Path to data directory
    
    Returns dict with drivers categorized by direction and net effect summary.
    """
    # Get top drivers
    top_drivers = get_top_drivers(dataset_name, top_n, data_path)
    
    # Categorize drivers by direction
    positive_drivers = []
    negative_drivers = []
    
    for driver in top_drivers:
        # Get detailed info for direction
        details = get_driver_details(dataset_name, driver['name'], data_path)
        
        driver_info = {
            'name': driver['name'],
            'importance': driver['importance_mean'],
            'direction': details['direction']
        }
        
        if details['direction'] == 'positive':
            positive_drivers.append(driver_info)
        else:
            negative_drivers.append(driver_info)
    
    # Calculate combined importance scores
    positive_total = sum(d['importance'] for d in positive_drivers)
    negative_total = sum(d['importance'] for d in negative_drivers)
    
    # Determine net effect
    if positive_total > negative_total * 1.2:
        net_effect = "increase"
        net_explanation = "Drivers strongly support price increases"
    elif negative_total > positive_total * 1.2:
        net_effect = "decrease"
        net_explanation = "Drivers strongly support price decreases"
    else:
        net_effect = "mixed"
        net_explanation = "Drivers show mixed signals with no clear direction"
    
    return {
        'drivers_supporting_increase': positive_drivers,
        'drivers_supporting_decrease': negative_drivers,
        'total_importance_increase': round(positive_total, 2),
        'total_importance_decrease': round(negative_total, 2),
        'net_effect': net_effect,
        'net_explanation': net_explanation,
        'total_drivers_analyzed': len(top_drivers)
    }
