"""Unit tests for DataLoader."""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch

from src.data.loader import DataLoader
from src.data.models import DatasetNotFoundError, DataLoadError, ForecastData, DriverData


class TestDataLoader:
    """Test DataLoader class."""

    def test_load_historical_success(self, data_loader):
        """Test historical data loading."""
        df = data_loader.load_historical("energy_futures")
        
        assert isinstance(df, pd.DataFrame)
        assert "Period" in df.columns
        assert "Value" in df.columns
        assert len(df) > 0

    def test_load_historical_all_datasets(self, data_loader):
        """Test loading all datasets."""
        for dataset_name in ["energy_futures", "cotton_price", "cotton_export"]:
            df = data_loader.load_historical(dataset_name)
            assert len(df) > 0
            assert "Period" in df.columns
            assert "Value" in df.columns

    def test_load_historical_caching(self, data_loader):
        """Test caching behavior."""
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame({
                "Period": ["2024-01-01"],
                "Value": [100.0]
            })
            
            df1 = data_loader.load_historical("energy_futures")
            assert mock_read_csv.call_count == 1
            
            df2 = data_loader.load_historical("energy_futures")
            assert mock_read_csv.call_count == 1
            
            assert df1 is df2

    def test_load_historical_invalid_dataset(self, data_loader):
        """Test error handling for invalid dataset name."""
        result = data_loader.load_historical("invalid_dataset")
        assert result is None

    def test_load_historical_missing_file(self, tmp_path):
        """Test error handling for missing CSV file."""
        empty_loader = DataLoader(tmp_path)
        
        result = empty_loader.load_historical("energy_futures")
        assert result is None

    def test_load_historical_invalid_csv_structure(self, tmp_path):
        """Test CSV with missing columns."""
        bad_csv_dir = tmp_path / "#1181-Dataset_Germany Energy Futures, Settlement Price"
        bad_csv_dir.mkdir(parents=True)
        csv_file = bad_csv_dir / "historical_data.csv"
        csv_file.write_text("Date,Price\n2024-01-01,100.0\n")
        
        loader = DataLoader(tmp_path)
        
        with pytest.raises(DataLoadError) as exc_info:
            loader.load_historical("energy_futures")
        
        assert "missing required columns" in str(exc_info.value).lower()

    def test_load_historical_dataframe_structure(self, data_loader):
        """Test that loaded DataFrame has correct structure."""
        df = data_loader.load_historical("energy_futures")
        
        # Check columns exist
        assert "Period" in df.columns
        assert "Value" in df.columns
        
        # Check data types
        assert len(df) > 0
        assert isinstance(df["Period"].iloc[0], str)
        assert isinstance(df["Value"].iloc[0], (int, float))
    
    def test_load_forecast_success(self, data_loader):
        """Test successful forecast data loading."""
        forecast = data_loader.load_forecast("energy_futures")
        
        assert isinstance(forecast, ForecastData)
        assert len(forecast.forecast_series) > 0
        assert "0.5" in forecast.quantile_forecast
        assert len(forecast.quantile_forecast) > 0
    
    def test_load_forecast_all_datasets(self, data_loader):
        """Test loading forecasts for all 3 datasets."""
        for dataset_name in ["energy_futures", "cotton_price", "cotton_export"]:
            forecast = data_loader.load_forecast(dataset_name)
            assert len(forecast.forecast_series) > 0
            assert "0.5" in forecast.quantile_forecast
    
    def test_load_forecast_caching(self, data_loader):
        """Test forecast caching behavior."""
        # First call
        forecast1 = data_loader.load_forecast("energy_futures")
        
        # Second call - should use cache
        forecast2 = data_loader.load_forecast("energy_futures")
        
        # Verify same object returned
        assert forecast1 is forecast2
    
    def test_load_forecast_invalid_dataset(self, data_loader):
        """Test error for invalid dataset name."""
        result = data_loader.load_forecast("invalid_dataset")
        assert result is None
    
    def test_load_forecast_missing_file(self, tmp_path):
        """Test error for missing JSON file."""
        empty_loader = DataLoader(tmp_path)
        
        result = empty_loader.load_forecast("energy_futures")
        assert result is None
    
    def test_load_forecast_malformed_json(self, tmp_path):
        """Test error for malformed JSON."""
        # Create invalid JSON file
        dataset_dir = tmp_path / "#1181-Dataset_Germany Energy Futures, Settlement Price"
        dataset_dir.mkdir(parents=True)
        json_file = dataset_dir / "forecast.json"
        json_file.write_text("{invalid json")
        
        loader = DataLoader(tmp_path)
        
        with pytest.raises(DataLoadError) as exc_info:
            loader.load_forecast("energy_futures")
        
        assert "parse" in str(exc_info.value).lower()
    
    def test_load_drivers_success(self, data_loader):
        """Test successful driver data loading."""
        drivers = data_loader.load_drivers_parsed("energy_futures")
        
        assert isinstance(drivers, list)
        assert len(drivers) > 0
        assert all(isinstance(d, DriverData) for d in drivers)
        
        # Check first driver has required fields
        first = drivers[0]
        assert first.driver_name
        assert first.importance_score >= 0
        assert first.direction in ('positive', 'negative')
    
    def test_load_drivers_sorted_by_importance(self, data_loader):
        """Test drivers are sorted by importance descending."""
        drivers = data_loader.load_drivers_parsed("energy_futures")
        
        # Check descending order
        for i in range(len(drivers) - 1):
            assert drivers[i].importance_score >= drivers[i+1].importance_score
    
    def test_load_drivers_caching(self, data_loader):
        """Test driver caching behavior."""
        # First call
        drivers1 = data_loader.load_drivers_parsed("energy_futures")
        
        # Second call
        drivers2 = data_loader.load_drivers_parsed("energy_futures")
        
        # Verify same object returned
        assert drivers1 is drivers2
    
    def test_load_drivers_invalid_dataset(self, data_loader):
        """Test error for invalid dataset name."""
        with pytest.raises(DatasetNotFoundError) as exc_info:
            data_loader.load_drivers("invalid_dataset")
        
        assert "invalid_dataset" in str(exc_info.value)
    
    def test_load_drivers_missing_file(self, tmp_path):
        """Test error for missing JSON file."""
        empty_loader = DataLoader(tmp_path)
        
        with pytest.raises(DataLoadError) as exc_info:
            empty_loader.load_drivers("energy_futures")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_load_drivers_malformed_json(self, tmp_path):
        """Test error for malformed JSON."""
        # Create invalid JSON file
        dataset_dir = tmp_path / "#1181-Dataset_Germany Energy Futures, Settlement Price"
        dataset_dir.mkdir(parents=True)
        json_file = dataset_dir / "drivers.json"
        json_file.write_text("{invalid json")
        
        loader = DataLoader(tmp_path)
        
        with pytest.raises(Exception) as exc_info:
            loader.load_drivers("energy_futures")
        
        assert "json" in str(exc_info.value).lower() or "parse" in str(exc_info.value).lower()
