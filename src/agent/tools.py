"""LangChain tool registration for procurement analysis."""

from langchain.tools import tool
from typing import List, Dict
from src.tools import historical, forecast, drivers, comparative, recommendations


@tool
def query_historical_data(
    dataset_name: str,
    date: str = None,
    start_date: str = None,
    end_date: str = None
) -> dict:
    """Get historical commodity prices - latest value, specific date, or date range."""
    data_path = "Agents - Code Challenge/Data"
    
    # Range query
    if start_date and end_date:
        values = historical.get_values_by_range(dataset_name, start_date, end_date, data_path)
        return {
            'query_type': 'range',
            'dataset': dataset_name,
            'start_date': start_date,
            'end_date': end_date,
            'values': values,
            'count': len(values)
        }
    
    # Handle "latest" keyword - treat as latest value query
    if date and date.lower() in ["latest", "current", "now"]:
        date = None
    
    # Specific date query
    if date:
        result = historical.get_value_by_date(dataset_name, date, data_path)
        return {
            'query_type': 'specific_date',
            'dataset': dataset_name,
            **result
        }
    
    # Latest value query
    result = historical.get_latest_value(dataset_name, data_path)
    return {
        'query_type': 'latest',
        'dataset': dataset_name,
        **result
    }


@tool
def query_forecast_data(
    dataset_name: str,
    months_ahead: int = 1,
    date: str = None
) -> dict:
    """Get future price forecasts for commodities."""
    data_path = "Agents - Code Challenge/Data"
    
    # Handle keywords - treat as default months_ahead query
    if date and date.lower() in ["latest", "next", "soon"]:
        date = None
    
    # Specific date forecast
    if date:
        result = forecast.get_forecast_by_date(dataset_name, date, data_path)
        return {
            'query_type': 'specific_date',
            'dataset': dataset_name,
            **result
        }
    
    # N months ahead forecast
    result = forecast.get_forecast(dataset_name, months_ahead, data_path)
    return {
        'query_type': 'months_ahead',
        'dataset': dataset_name,
        'months_ahead': months_ahead,
        **result
    }


@tool
def analyze_market_drivers(
    dataset_name: str,
    top_n: int = 5,
    driver_name: str = None
) -> dict:
    """Analyze what factors and market drivers affect commodity prices."""
    data_path = "Agents - Code Challenge/Data"
    
    # Specific driver details
    if driver_name:
        result = drivers.get_driver_details(dataset_name, driver_name, data_path)
        return {
            'query_type': 'driver_details',
            'dataset': dataset_name,
            **result
        }
    
    # Top N drivers
    top_drivers = drivers.get_top_drivers(dataset_name, top_n, data_path)
    return {
        'query_type': 'top_drivers',
        'dataset': dataset_name,
        'top_n': top_n,
        'drivers': top_drivers
    }


@tool
def compare_commodities(
    dataset_names: List[str]
) -> dict:
    """Compare multiple commodities to find correlations and relationships."""
    data_path = "Agents - Code Challenge/Data"
    
    # Get aligned data across all datasets
    result = comparative.compare_datasets(dataset_names, data_path)
    
    return {
        'query_type': 'multi_commodity_comparison',
        **result
    }


@tool
def recommend_forward_buy(
    dataset_name: str,
    months_ahead: int = 3,
    quantity: int = 1000
) -> dict:
    """Get buy/wait/monitor recommendation for forward-buy decisions.
    
    Analyzes current price vs forecast and recommends whether to buy now or wait.
    Includes quantified savings/costs and rationale.
    """
    data_path = "Agents - Code Challenge/Data"
    return recommendations.recommend_forward_buy(
        dataset_name, months_ahead, quantity, data_path
    )


@tool
def calculate_impact_analysis(
    dataset_name: str,
    months_ahead: int = 3,
    quantity: int = 1000
) -> dict:
    """Calculate quantified impact analysis with best/expected/worst case scenarios.
    
    Provides risk assessment using forecast confidence intervals to help justify
    procurement decisions to management.
    """
    data_path = "Agents - Code Challenge/Data"
    return recommendations.calculate_impact_analysis(
        dataset_name, months_ahead, quantity, data_path
    )


@tool
def analyze_multi_commodity_scenario(
    dataset_names: List[str],
    months_ahead: int = 3,
    quantity: int = 1000
) -> dict:
    """Analyze complex scenarios involving multiple commodities.
    
    Provides holistic procurement strategy by analyzing all commodities together,
    considering correlations and prioritizing recommendations.
    """
    data_path = "Agents - Code Challenge/Data"
    return recommendations.analyze_multi_commodity_scenario(
        dataset_names, months_ahead, quantity, data_path
    )


@tool
def recommend_production_sequencing(
    dataset_names: List[str],
    months_ahead: int = 3
) -> dict:
    """Recommend production sequencing based on commodity forecasts.
    
    Identifies which commodities have favorable forecasts and recommends
    prioritizing production activities using those commodities first.
    """
    data_path = "Agents - Code Challenge/Data"
    return recommendations.recommend_production_sequencing(
        dataset_names, months_ahead, data_path
    )


@tool
def generate_negotiation_talking_points(
    dataset_name: str,
    months_ahead: int = 3
) -> dict:
    """Generate negotiation talking points with data citations.
    
    Provides 3-5 data-backed talking points for supplier negotiations,
    including current prices, forecasts, and market drivers.
    """
    data_path = "Agents - Code Challenge/Data"
    from src.tools import negotiation
    return negotiation.generate_negotiation_talking_points(
        dataset_name, months_ahead, data_path
    )


@tool
def validate_supplier_claim(
    dataset_name: str,
    claimed_price: float,
    months_ahead: int = 3
) -> dict:
    """Validate supplier price claim against forecast data.
    
    Compares supplier's claimed price against forecast with confidence intervals
    to identify if claim is above, below, or aligned with market expectations.
    """
    data_path = "Agents - Code Challenge/Data"
    from src.tools import negotiation
    return negotiation.validate_supplier_claim(
        dataset_name, claimed_price, months_ahead, data_path
    )


@tool
def identify_driver_arguments(
    dataset_name: str,
    price_direction: str = 'increase'
) -> dict:
    """Identify drivers supporting or contradicting price movements.
    
    Analyzes market drivers to identify which support or contradict expected
    price movements, helping build balanced negotiation arguments.
    """
    data_path = "Agents - Code Challenge/Data"
    from src.tools import negotiation
    return negotiation.identify_driver_arguments(
        dataset_name, price_direction, data_path
    )


# Export all tools for agent use
TOOLS = [
    query_historical_data,
    query_forecast_data,
    analyze_market_drivers,
    compare_commodities,
    recommend_forward_buy,
    calculate_impact_analysis,
    analyze_multi_commodity_scenario,
    recommend_production_sequencing,
    generate_negotiation_talking_points,
    validate_supplier_claim,
    identify_driver_arguments
]
