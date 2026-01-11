"""Tools package - Analysis tools for historical, forecast, drivers, and comparative data."""

from src.tools.historical import (
    get_latest_value,
    get_value_by_date,
    get_values_by_range,
    calculate_percentage_change,
    get_trend_direction,
    find_peak,
    find_valley,
    find_peak_and_valley,
    calculate_moving_average,
    calculate_trend_line
)

from src.tools.forecast import (
    get_forecast,
    get_forecast_by_date,
    get_all_forecasts,
    get_quantile_forecast,
    get_confidence_interval,
    compare_current_to_forecast,
    analyze_forecast_trend
)

from src.tools.drivers import (
    get_top_drivers,
    get_driver_details,
    analyze_drivers_combined
)

from src.tools.comparative import (
    compare_datasets,
    calculate_correlation,
    analyze_timing_relationships,
    analyze_multi_commodity_strategy
)
