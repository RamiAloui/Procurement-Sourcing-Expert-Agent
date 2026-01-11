"""Cross-dataset comparison tools."""

from typing import List, Dict
import pandas as pd
from src.data import DataLoader


def compare_datasets(
    dataset_names: List[str],
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Compare historical data across multiple datasets."""
    loader = DataLoader(data_path)
    
    # Load all datasets
    dfs = {}
    for name in dataset_names:
        dfs[name] = loader.load_historical(name)
    
    # Find common dates across all datasets
    common_dates = set(dfs[dataset_names[0]]['Period'])
    for name in dataset_names[1:]:
        common_dates = common_dates.intersection(set(dfs[name]['Period']))
    
    # Sort dates for consistent output
    common_dates = sorted(common_dates)
    
    # Build aligned data
    aligned_data = []
    for date in common_dates:
        record = {'date': date}
        for name in dataset_names:
            df = dfs[name]
            value = df[df['Period'] == date]['Value'].iloc[0]
            record[name] = float(value)
        aligned_data.append(record)
    
    # Build result
    result = {
        'datasets': dataset_names,
        'common_date_range': {
            'start': common_dates[0] if common_dates else None,
            'end': common_dates[-1] if common_dates else None
        },
        'aligned_data': aligned_data,
        'total_aligned_records': len(aligned_data)
    }
    
    return result


def calculate_correlation(
    dataset1_name: str,
    dataset2_name: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Calculate correlation between two datasets."""
    # Get aligned data using compare_datasets
    aligned_data = compare_datasets([dataset1_name, dataset2_name], data_path)
    
    # Convert to DataFrame for correlation calculation
    df = pd.DataFrame(aligned_data['aligned_data'])
    
    # Calculate Pearson correlation
    correlation = df[dataset1_name].corr(df[dataset2_name])
    
    # Determine direction
    if correlation > 0.1:
        direction = 'positive'
    elif correlation < -0.1:
        direction = 'negative'
    else:
        direction = 'none'
    
    # Classify strength
    abs_corr = abs(correlation)
    if abs_corr >= 0.7:
        strength = 'strong'
    elif abs_corr >= 0.3:
        strength = 'moderate'
    else:
        strength = 'weak'
    
    # Generate interpretation
    if direction == 'positive':
        interpretation = f"{strength.capitalize()} positive correlation - when {dataset1_name} rises, {dataset2_name} tends to rise"
    elif direction == 'negative':
        interpretation = f"{strength.capitalize()} negative correlation - when {dataset1_name} rises, {dataset2_name} tends to fall"
    else:
        interpretation = f"No meaningful correlation - {dataset1_name} and {dataset2_name} move independently"
    
    return {
        'dataset1': dataset1_name,
        'dataset2': dataset2_name,
        'correlation_coefficient': round(correlation, 2),
        'direction': direction,
        'strength': strength,
        'interpretation': interpretation,
        'data_points_used': len(aligned_data['aligned_data'])
    }


def analyze_timing_relationships(
    dataset1_name: str,
    dataset2_name: str,
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Analyze timing relationships between two datasets using driver lag data."""
    loader = DataLoader(data_path)
    
    # Load driver data for both datasets
    drivers1 = loader.load_drivers(dataset1_name)
    drivers2 = loader.load_drivers(dataset2_name)
    
    # Find common drivers
    common_drivers = list(set(drivers1.keys()).intersection(set(drivers2.keys())))
    
    # Analyze lag for each common driver
    timing_insights = []
    lag_differences = []
    
    for driver in common_drivers:
        lag1 = drivers1[driver].get('lag', 0)
        lag2 = drivers2[driver].get('lag', 0)
        
        # Handle None values
        if lag1 is None:
            lag1 = 0
        if lag2 is None:
            lag2 = 0
        
        lag_diff = lag1 - lag2
        lag_differences.append(abs(lag_diff))
        
        # Generate interpretation
        if lag1 < lag2:
            interpretation = f"{dataset1_name} responds after {lag1} months, {dataset2_name} follows after {lag2} months"
        elif lag2 < lag1:
            interpretation = f"{dataset2_name} responds after {lag2} months, {dataset1_name} follows after {lag1} months"
        else:
            interpretation = f"Both respond after {lag1} months to {driver}"
        
        timing_insights.append({
            'driver': driver,
            'dataset1_lag': lag1,
            'dataset2_lag': lag2,
            'interpretation': interpretation
        })
    
    # Calculate average lag difference
    avg_lag_diff = sum(lag_differences) / len(lag_differences) if lag_differences else 0
    
    # Determine lead commodity
    dataset1_avg_lag = sum(drivers1[d].get('lag', 0) or 0 for d in common_drivers) / len(common_drivers) if common_drivers else 0
    dataset2_avg_lag = sum(drivers2[d].get('lag', 0) or 0 for d in common_drivers) / len(common_drivers) if common_drivers else 0
    
    if dataset1_avg_lag < dataset2_avg_lag - 0.5:
        lead_commodity = dataset1_name
    elif dataset2_avg_lag < dataset1_avg_lag - 0.5:
        lead_commodity = dataset2_name
    else:
        lead_commodity = 'similar'
    
    # Classify predictive value
    if avg_lag_diff >= 3:
        predictive_value = 'high'
    elif avg_lag_diff >= 1:
        predictive_value = 'moderate'
    else:
        predictive_value = 'low'
    
    return {
        'dataset1': dataset1_name,
        'dataset2': dataset2_name,
        'common_drivers': common_drivers,
        'lead_commodity': lead_commodity,
        'average_lag_months': round(avg_lag_diff, 1),
        'timing_insights': timing_insights,
        'predictive_value': predictive_value
    }


def analyze_multi_commodity_strategy(
    dataset_names: List[str],
    data_path: str = "Agents - Code Challenge/Data"
) -> Dict:
    """Perform comprehensive strategic analysis across multiple commodities."""
    from src.tools.historical import get_latest_value
    from src.tools.drivers import get_top_drivers
    
    loader = DataLoader(data_path)
    
    # Individual analysis for each commodity
    individual_analysis = {}
    all_drivers = {}
    
    for dataset in dataset_names:
        # Get latest value
        latest = get_latest_value(dataset, data_path)
        
        # Get top drivers
        drivers = get_top_drivers(dataset, top_n=5, data_path=data_path)
        driver_names = [d['name'] for d in drivers]
        all_drivers[dataset] = set(driver_names)
        
        individual_analysis[dataset] = {
            'latest_value': latest['value'],
            'top_drivers': driver_names
        }
    
    # Cross-commodity insights
    # Find shared drivers
    if len(dataset_names) >= 2:
        shared_drivers = set.intersection(*all_drivers.values())
    else:
        shared_drivers = set()
    
    cross_commodity_insights = {
        'shared_drivers': list(shared_drivers)
    }
    
    # Generate strategic recommendations
    recommendations = []
    
    # Recommendation based on shared drivers
    if shared_drivers:
        recommendations.append(
            f"Monitor {len(shared_drivers)} shared market drivers affecting all commodities: {', '.join(list(shared_drivers)[:3])}"
        )
    
    # Recommendation for each commodity
    for dataset in dataset_names:
        analysis = individual_analysis[dataset]
        recommendations.append(
            f"{dataset}: Current value {analysis['latest_value']:.2f}, influenced by {len(analysis['top_drivers'])} key drivers"
        )
    
    # Add correlation insight if 2 commodities
    if len(dataset_names) == 2:
        try:
            corr = calculate_correlation(dataset_names[0], dataset_names[1], data_path)
            recommendations.append(
                f"Correlation: {corr['strength']} {corr['direction']} relationship between {dataset_names[0]} and {dataset_names[1]}"
            )
        except:
            pass
    
    return {
        'commodities_analyzed': dataset_names,
        'individual_analysis': individual_analysis,
        'cross_commodity_insights': cross_commodity_insights,
        'strategic_recommendations': recommendations
    }
