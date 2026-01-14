"""Data models for the procurement agent.

Defines dataclasses for historical data, forecasts, and market drivers.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


# exceptions for data loading errors

class DatasetNotFoundError(Exception):
    """Raised when dataset name is invalid."""
    pass


class InvalidDateRangeError(Exception):
    """Raised when date range is invalid."""
    pass


class DataLoadError(Exception):
    """Raised when data file cannot be loaded."""
    pass


# Dataset mapping
DATASET_MAPPING = {
    "energy_futures": "#1181-Dataset_Germany Energy Futures, Settlement Price",
    "cotton_price": "#1597-Dataset_Pima Cotton Price",
    "cotton_export": "#1616-Dataset_Pima Cotton Export Quantity"
}


@dataclass
class HistoricalData:
    """Historical commodity data from CSV files."""
    period: str
    value: float
    
    def __post_init__(self):
        # Check date format
        try:
            datetime.strptime(self.period, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid period format: {self.period}. Expected YYYY-MM-DD"
            )
        
        if not isinstance(self.value, (int, float)):
            raise TypeError(
                f"Invalid value type: {type(self.value)}. Expected numeric"
            )


@dataclass
class ForecastData:
    """Forecast data with quantile predictions."""
    forecast_series: List[str]
    quantile_forecast: Dict[str, List[float]]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        # verifying data
        if not self.forecast_series:
            raise ValueError("forecast_series cannot be empty")
        
        
        for date_str in self.forecast_series:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Invalid date format in forecast_series: {date_str}. "
                    f"Expected YYYY-MM-DD"
                )
        
        
        if "0.5" not in self.quantile_forecast:
            raise ValueError(
                "quantile_forecast must include '0.5' (median) quantile"
            )
        
        # Check lengths match
        series_length = len(self.forecast_series)
        for quantile, values in self.quantile_forecast.items():
            if len(values) != series_length:
                raise ValueError(
                    f"Quantile {quantile} has {len(values)} values, "
                    f"expected {series_length} to match forecast_series"
                )


@dataclass
class DriverData:
    """Market driver analysis data."""
    driver_name: str
    importance_score: float
    importance_max: float
    importance_min: float
    direction: str
    pearson_correlation: Optional[float] = None
    granger_causality: Optional[float] = None
    lag_periods: Optional[int] = None
    normalized_series: Optional[List[float]] = None
    
    def __post_init__(self):
        # Checking if scores are numeric
        for score_name, score_value in [
            ("importance_score", self.importance_score),
            ("importance_max", self.importance_max),
            ("importance_min", self.importance_min)
        ]:
            if not isinstance(score_value, (int, float)):
                raise TypeError(
                    f"Invalid {score_name} type: {type(score_value)}. "
                    f"Expected numeric"
                )
        
        # Score range 
        if not (self.importance_min <= self.importance_score <= self.importance_max):
            raise ValueError(
                f"Importance score {self.importance_score} is outside valid range "
                f"[{self.importance_min}, {self.importance_max}]"
            )
        
        # Direction positive/negative
        if self.direction not in ("positive", "negative"):
            raise ValueError(
                f"Invalid direction: {self.direction}. "
                f"Expected 'positive' or 'negative'"
            )
