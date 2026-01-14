"""Unified data loader for all dataset types."""

import json
import re
from pathlib import Path
from typing import Dict, List
import logging

import pandas as pd

from src.data.models import DATASET_MAPPING, DatasetNotFoundError, DataLoadError, ForecastData, DriverData


logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and caches historical, forecast, and driver data."""
    
    def __init__(self, data_path: str):
        """Initialize with path to data directory."""
        self.data_path = Path(data_path)
        self._cache: Dict = {}
        self._drivers_cache: Dict = {}
    
    def load_historical(self, dataset_name: str) -> pd.DataFrame:
        """Load historical data for a dataset.
        
        Returns DataFrame with Period and Value columns.
        """
        # Check cache first
        cache_key = f"{dataset_name}_historical"
        if cache_key in self._cache:
            logger.info(f"Loading {dataset_name} historical data from cache")
            return self._cache[cache_key]
        
        # Validate dataset name
        if dataset_name not in DATASET_MAPPING:
            logger.warning(f"Dataset '{dataset_name}' not found in mapping")
            return None
        
        # Build file path
        dataset_folder = DATASET_MAPPING[dataset_name]
        csv_path = self.data_path / dataset_folder / "historical_data.csv"
        
        # Check file exists
        if not csv_path.exists():
            logger.warning(f"Historical data file not found: {csv_path}")
            return None
        
        # Load CSV
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise DataLoadError(f"Failed to read CSV file {csv_path}: {e}")
        
        # Validate columns
        required_columns = ["Period", "Value"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise DataLoadError(
                f"CSV file {csv_path} missing required columns: {missing_columns}"
            )
        
        # Cache and return
        self._cache[cache_key] = df
        logger.info(f"Loaded {dataset_name} historical data: {len(df)} records")
        return df
    
    def load_forecast(self, dataset_name: str):
        """Load forecast data for a dataset.
        
        Returns ForecastData with forecast_series and quantile_forecast.
        """
        # Check cache first
        cache_key = f"{dataset_name}_forecast"
        if cache_key in self._cache:
            logger.info(f"Loading {dataset_name} forecast data from cache")
            return self._cache[cache_key]
        
        # Validate dataset name
        if dataset_name not in DATASET_MAPPING:
            logger.warning(f"Dataset '{dataset_name}' not found in mapping")
            return None
        
        # Build file path
        dataset_folder = DATASET_MAPPING[dataset_name]
        json_path = self.data_path / dataset_folder / "forecast.json"
        
        # Check file exists
        if not json_path.exists():
            logger.warning(f"Forecast data file not found: {json_path}")
            return None
        
        # Load JSON
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Failed to parse JSON file {json_path}: {e}")
        except Exception as e:
            raise DataLoadError(f"Failed to read JSON file {json_path}: {e}")
        
        # Validate structure
        if "forecast_series" not in data:
            raise DataLoadError(
                f"JSON file {json_path} missing required field: forecast_series"
            )
        
        # Transform forecast_series dict into lists for ForecastData
        forecast_series_dict = data["forecast_series"]
        dates = sorted(forecast_series_dict.keys())
        
        # Extract quantile forecasts for each date
        quantile_forecast = {}
        for date in dates:
            date_data = forecast_series_dict[date]
            if "quantile_forecast" not in date_data:
                continue
            for quantile, value in date_data["quantile_forecast"].items():
                if quantile not in quantile_forecast:
                    quantile_forecast[quantile] = []
                quantile_forecast[quantile].append(value)
        
        # Validate 0.5 quantile exists
        if "0.5" not in quantile_forecast:
            raise DataLoadError(
                f"JSON file {json_path} missing required '0.5' quantile (point forecast)"
            )
        
        # Create ForecastData instance
        try:
            forecast_data = ForecastData(
                forecast_series=dates,
                quantile_forecast=quantile_forecast,
                metadata={
                    "forecast_start": data.get("forecast_start"),
                    "forecast_end": data.get("forecast_end"),
                    "forecast_horizon": data.get("forecast_horizon")
                }
            )
        except (ValueError, TypeError) as e:
            raise DataLoadError(f"Invalid forecast data structure: {e}")
        
        # Cache and return
        self._cache[cache_key] = forecast_data
        logger.info(f"Loaded {dataset_name} forecast data: {len(forecast_data.forecast_series)} periods")
        return forecast_data
    
    def load_drivers(self, dataset_name: str) -> Dict:
        """Load market driver data from JSON file."""
        if dataset_name in self._drivers_cache:
            return self._drivers_cache[dataset_name]
        
        folder_name = DATASET_MAPPING.get(dataset_name)
        if not folder_name:
            raise DatasetNotFoundError(f"Unknown dataset: {dataset_name}")
        
        file_path = self.data_path / folder_name / "drivers.json"
        
        if not file_path.exists():
            raise DataLoadError(f"Driver file not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Failed to parse JSON file {file_path}: {e}")
        except Exception as e:
            raise DataLoadError(f"Failed to read JSON file {file_path}: {e}")
        
        self._drivers_cache[dataset_name] = data
        return data
    
    def load_drivers_parsed(self, dataset_name: str) -> List[DriverData]:
        """Load market driver data for a dataset.
        
        Returns list of DriverData sorted by importance (descending).
        """
        # Use raw load_drivers method
        data = self.load_drivers(dataset_name)
        
        # Check cache first
        cache_key = f"{dataset_name}_drivers_parsed"
        if cache_key in self._cache:
            logger.info(f"Loading {dataset_name} driver data from cache")
            return self._cache[cache_key]
        
        # Parse drivers (skip target_ entries)
        drivers = []
        for driver_id, driver_info in data.items():
            if driver_id.startswith('target_'):
                continue
            
            # Extract required fields with defaults
            driver_name = driver_info.get('driver_name', 'Unknown')
            
            # Importance scores
            importance = driver_info.get('importance', {}).get('overall', {})
            importance_score = importance.get('mean', 0.0)
            importance_max = importance.get('max', 0.0)
            importance_min = importance.get('min', 0.0)
            
            # Direction
            direction_val = driver_info.get('direction', {}).get('overall', {}).get('mean', 1)
            if direction_val is None:
                direction_val = 1
            direction = 'positive' if direction_val >= 0 else 'negative'
            
            # Correlations (optional)
            pearson = driver_info.get('pearson_correlation', {}).get('overall', {}).get('mean')
            granger = driver_info.get('granger_correlation', {}).get('overall', {}).get('mean')
            
            # Lag (optional)
            lag_str = driver_info.get('overall_lag', '')
            lag_periods = None
            if lag_str and 'month' in lag_str:
                # Parse "6 to 12 month(s)" -> extract first number
                match = re.search(r'(\d+)', lag_str)
                if match:
                    lag_periods = int(match.group(1))
            
            # Normalized series (optional)
            normalized_series = driver_info.get('normalized_series')
            if normalized_series:
                normalized_series = list(normalized_series.values())
            
            # Create DriverData instance
            try:
                driver_data = DriverData(
                    driver_name=driver_name,
                    importance_score=importance_score,
                    importance_max=importance_max,
                    importance_min=importance_min,
                    direction=direction,
                    pearson_correlation=pearson,
                    granger_causality=granger,
                    lag_periods=lag_periods,
                    normalized_series=normalized_series
                )
                drivers.append(driver_data)
            except (ValueError, TypeError) as e:
                # Skip invalid drivers, log warning
                logger.warning(f"Skipping invalid driver {driver_id}: {e}")
                continue
        
        # Sort by importance descending
        drivers.sort(key=lambda d: d.importance_score, reverse=True)
        
        # Cache and return
        self._cache[cache_key] = drivers
        logger.info(f"Loaded {dataset_name} driver data: {len(drivers)} drivers")
        return drivers
