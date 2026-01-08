"""Data models for procurement datasets.

This module defines data structures for historical data, forecasts, and market
drivers used in the procurement agent system.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


__all__ = [
    'HistoricalData',
    'ForecastData',
    'DriverData',
    'DATASET_MAPPING',
    'DatasetNotFoundError',
    'InvalidDateRangeError',
    'DataLoadError'
]


# Custom Exceptions
class DatasetNotFoundError(Exception):
    """Raised when dataset name is invalid."""
    pass


class InvalidDateRangeError(Exception):
    """Raised when date range is invalid or out of bounds."""
    pass


class DataLoadError(Exception):
    """Raised when data file cannot be loaded."""
    pass


# Dataset Mapping
DATASET_MAPPING = {
    "energy_futures": "#1181-Dataset_Germany Energy Futures, Settlement Price",
    "cotton_price": "#1597-Dataset_Pima Cotton Price",
    "cotton_export": "#1616-Dataset_Pima Cotton Export Quantity"
}
"""Mapping of friendly dataset names to actual folder names.

This mapping allows the system to use simple names like 'cotton_price' instead
of the full folder names with IDs.
"""


@dataclass
class HistoricalData:
    """Historical commodity price data from CSV files.
    
    Attributes:
        period: Date in YYYY-MM-DD format
        value: Commodity price/quantity value
    """
    period: str
    value: float
    
    def __post_init__(self):
        """Validate data structure on initialization."""
        # Validate period format (YYYY-MM-DD)
        try:
            datetime.strptime(self.period, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                f"Invalid period format: {self.period}. Expected YYYY-MM-DD"
            )
        
        # Validate value is numeric
        if not isinstance(self.value, (int, float)):
            raise TypeError(
                f"Invalid value type: {type(self.value)}. Expected numeric"
            )


@dataclass
class ForecastData:
    """Forecast data with quantile predictions from JSON files.
    
    Attributes:
        forecast_series: List of forecast dates
        quantile_forecast: Dict mapping quantiles to value lists
        metadata: Optional metadata from forecast file
    """
    forecast_series: List[str]
    quantile_forecast: Dict[str, List[float]]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate data structure on initialization."""
        # Validate forecast_series is not empty
        if not self.forecast_series:
            raise ValueError("forecast_series cannot be empty")
        
        # Validate forecast_series dates are in correct format
        for date_str in self.forecast_series:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Invalid date format in forecast_series: {date_str}. "
                    f"Expected YYYY-MM-DD"
                )
        
        # Validate quantile_forecast has required quantiles (0.5 minimum)
        if "0.5" not in self.quantile_forecast:
            raise ValueError(
                "quantile_forecast must include '0.5' (median) quantile"
            )
        
        # Validate lists have matching lengths
        series_length = len(self.forecast_series)
        for quantile, values in self.quantile_forecast.items():
            if len(values) != series_length:
                raise ValueError(
                    f"Quantile {quantile} has {len(values)} values, "
                    f"expected {series_length} to match forecast_series"
                )


@dataclass
class DriverData:
    """Market driver analysis data from JSON files.
    
    Attributes:
        driver_name: Name of the market driver
        importance_score: Overall importance score (mean)
        importance_max: Maximum importance score
        importance_min: Minimum importance score
        direction: Correlation direction (positive/negative)
        pearson_correlation: Pearson correlation coefficient
        granger_causality: Granger causality p-value
        lag_periods: Lag information (timing relationship)
        normalized_series: Normalized time series data
    """
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
        """Validate data structure on initialization."""
        # Validate importance scores are numeric
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
        
        # Validate importance score range is logical
        if not (self.importance_min <= self.importance_score <= self.importance_max):
            raise ValueError(
                f"Importance score {self.importance_score} is outside valid range "
                f"[{self.importance_min}, {self.importance_max}]"
            )
        
        # Validate direction is 'positive' or 'negative'
        if self.direction not in ("positive", "negative"):
            raise ValueError(
                f"Invalid direction: {self.direction}. "
                f"Expected 'positive' or 'negative'"
            )
