"""Unit tests for data models."""

import pytest
from src.data.models import (
    HistoricalData,
    ForecastData,
    DriverData,
    DATASET_MAPPING,
    DatasetNotFoundError,
    InvalidDateRangeError,
    DataLoadError
)


class TestHistoricalData:
    """Tests for HistoricalData model."""
    
    def test_historical_data_creation(self):
        """Test HistoricalData can be created with valid data."""
        data = HistoricalData(period="2024-01-01", value=100.5)
        assert data.period == "2024-01-01"
        assert data.value == 100.5
    
    def test_historical_data_validation_invalid_period(self):
        """Test HistoricalData validates period format."""
        with pytest.raises(ValueError, match="Invalid period format"):
            HistoricalData(period="invalid-date", value=100.5)
    
    def test_historical_data_validation_invalid_value(self):
        """Test HistoricalData validates numeric value."""
        with pytest.raises(TypeError, match="Invalid value type"):
            HistoricalData(period="2024-01-01", value="not-a-number")
    
    def test_historical_data_with_integer_value(self):
        """Test HistoricalData accepts integer values."""
        data = HistoricalData(period="2024-01-01", value=100)
        assert data.value == 100
    
    def test_historical_data_with_negative_value(self):
        """Test HistoricalData accepts negative values."""
        data = HistoricalData(period="2024-01-01", value=-50.5)
        assert data.value == -50.5
    
    def test_historical_data_with_future_date(self):
        """Test HistoricalData accepts future dates."""
        data = HistoricalData(period="2099-12-31", value=1000.0)
        assert data.period == "2099-12-31"


class TestForecastData:
    """Tests for ForecastData model."""
    
    def test_forecast_data_creation(self):
        """Test ForecastData can be created with valid data."""
        data = ForecastData(
            forecast_series=["2024-01-01", "2024-02-01"],
            quantile_forecast={"0.5": [100.0, 105.0]}
        )
        assert len(data.forecast_series) == 2
        assert "0.5" in data.quantile_forecast
    
    def test_forecast_data_validation_empty_series(self):
        """Test ForecastData validates non-empty series."""
        with pytest.raises(ValueError, match="forecast_series cannot be empty"):
            ForecastData(
                forecast_series=[],
                quantile_forecast={"0.5": []}
            )
    
    def test_forecast_data_validation_missing_median(self):
        """Test ForecastData requires 0.5 quantile."""
        with pytest.raises(ValueError, match="must include '0.5'"):
            ForecastData(
                forecast_series=["2024-01-01"],
                quantile_forecast={"0.1": [90.0]}
            )
    
    def test_forecast_data_validation_mismatched_lengths(self):
        """Test ForecastData validates matching list lengths."""
        with pytest.raises(ValueError, match="expected 2 to match forecast_series"):
            ForecastData(
                forecast_series=["2024-01-01", "2024-02-01"],
                quantile_forecast={"0.5": [100.0]}  # Only 1 value, expected 2
            )
    
    def test_forecast_data_with_metadata(self):
        """Test ForecastData accepts optional metadata."""
        data = ForecastData(
            forecast_series=["2024-01-01"],
            quantile_forecast={"0.5": [100.0]},
            metadata={"model": "test", "version": "1.0"}
        )
        assert data.metadata == {"model": "test", "version": "1.0"}
    
    def test_forecast_data_with_multiple_quantiles(self):
        """Test ForecastData with multiple quantile levels."""
        data = ForecastData(
            forecast_series=["2024-01-01", "2024-02-01"],
            quantile_forecast={
                "0.1": [90.0, 95.0],
                "0.5": [100.0, 105.0],
                "0.9": [110.0, 115.0]
            }
        )
        assert len(data.quantile_forecast) == 3
        assert all(len(values) == 2 for values in data.quantile_forecast.values())
    
    def test_forecast_data_validation_invalid_date_format(self):
        """Test ForecastData validates date format in forecast_series."""
        with pytest.raises(ValueError, match="Invalid date format in forecast_series"):
            ForecastData(
                forecast_series=["invalid-date"],
                quantile_forecast={"0.5": [100.0]}
            )


class TestDriverData:
    """Tests for DriverData model."""
    
    def test_driver_data_creation(self):
        """Test DriverData can be created with valid data."""
        data = DriverData(
            driver_name="Export Demand",
            importance_score=35.2,
            importance_max=45.0,
            importance_min=25.0,
            direction="positive"
        )
        assert data.driver_name == "Export Demand"
        assert data.importance_score == 35.2
        assert data.direction == "positive"
    
    def test_driver_data_validation_direction(self):
        """Test DriverData validates direction values."""
        with pytest.raises(ValueError, match="Invalid direction"):
            DriverData(
                driver_name="Test Driver",
                importance_score=30.0,
                importance_max=40.0,
                importance_min=20.0,
                direction="invalid"
            )
    
    def test_driver_data_validation_importance_score_type(self):
        """Test DriverData validates importance score is numeric."""
        with pytest.raises(TypeError, match="Invalid importance_score type"):
            DriverData(
                driver_name="Test Driver",
                importance_score="not-a-number",
                importance_max=40.0,
                importance_min=20.0,
                direction="positive"
            )
    
    def test_driver_data_with_optional_fields(self):
        """Test DriverData with all optional fields."""
        data = DriverData(
            driver_name="Export Demand",
            importance_score=35.2,
            importance_max=45.0,
            importance_min=25.0,
            direction="positive",
            pearson_correlation=0.85,
            granger_causality=0.01,
            lag_periods=2,
            normalized_series=[0.1, 0.2, 0.3]
        )
        assert data.pearson_correlation == 0.85
        assert data.granger_causality == 0.01
        assert data.lag_periods == 2
        assert len(data.normalized_series) == 3
    
    def test_driver_data_negative_direction(self):
        """Test DriverData with negative direction."""
        data = DriverData(
            driver_name="Inventory Levels",
            importance_score=22.1,
            importance_max=30.0,
            importance_min=15.0,
            direction="negative"
        )
        assert data.direction == "negative"
    
    def test_driver_data_validation_score_below_min(self):
        """Test DriverData validates score is not below minimum."""
        with pytest.raises(ValueError, match="outside valid range"):
            DriverData(
                driver_name="Test Driver",
                importance_score=10.0,
                importance_max=50.0,
                importance_min=20.0,
                direction="positive"
            )
    
    def test_driver_data_validation_score_above_max(self):
        """Test DriverData validates score is not above maximum."""
        with pytest.raises(ValueError, match="outside valid range"):
            DriverData(
                driver_name="Test Driver",
                importance_score=60.0,
                importance_max=50.0,
                importance_min=20.0,
                direction="positive"
            )


class TestDatasetMapping:
    """Tests for DATASET_MAPPING constant."""
    
    def test_dataset_mapping_exists(self):
        """Test DATASET_MAPPING constant exists."""
        assert DATASET_MAPPING is not None
    
    def test_dataset_mapping_has_all_datasets(self):
        """Test DATASET_MAPPING includes all 3 datasets."""
        assert "energy_futures" in DATASET_MAPPING
        assert "cotton_price" in DATASET_MAPPING
        assert "cotton_export" in DATASET_MAPPING
    
    def test_dataset_mapping_paths_correct(self):
        """Test DATASET_MAPPING paths match actual folder names."""
        assert "#1181" in DATASET_MAPPING["energy_futures"]
        assert "#1597" in DATASET_MAPPING["cotton_price"]
        assert "#1616" in DATASET_MAPPING["cotton_export"]
    
    def test_dataset_mapping_energy_futures_full_path(self):
        """Test energy_futures mapping is complete."""
        expected = "#1181-Dataset_Germany Energy Futures, Settlement Price"
        assert DATASET_MAPPING["energy_futures"] == expected
    
    def test_dataset_mapping_cotton_price_full_path(self):
        """Test cotton_price mapping is complete."""
        expected = "#1597-Dataset_Pima Cotton Price"
        assert DATASET_MAPPING["cotton_price"] == expected
    
    def test_dataset_mapping_cotton_export_full_path(self):
        """Test cotton_export mapping is complete."""
        expected = "#1616-Dataset_Pima Cotton Export Quantity"
        assert DATASET_MAPPING["cotton_export"] == expected


class TestCustomExceptions:
    """Tests for custom exception classes."""
    
    def test_custom_exceptions_exist(self):
        """Test custom exceptions are defined."""
        # Should import without error
        assert DatasetNotFoundError is not None
        assert InvalidDateRangeError is not None
        assert DataLoadError is not None
    
    def test_dataset_not_found_error_inheritance(self):
        """Test DatasetNotFoundError inherits from Exception."""
        assert issubclass(DatasetNotFoundError, Exception)
    
    def test_invalid_date_range_error_inheritance(self):
        """Test InvalidDateRangeError inherits from Exception."""
        assert issubclass(InvalidDateRangeError, Exception)
    
    def test_data_load_error_inheritance(self):
        """Test DataLoadError inherits from Exception."""
        assert issubclass(DataLoadError, Exception)
    
    def test_dataset_not_found_error_can_be_raised(self):
        """Test DatasetNotFoundError can be raised with message."""
        with pytest.raises(DatasetNotFoundError, match="test message"):
            raise DatasetNotFoundError("test message")
    
    def test_invalid_date_range_error_can_be_raised(self):
        """Test InvalidDateRangeError can be raised with message."""
        with pytest.raises(InvalidDateRangeError, match="test message"):
            raise InvalidDateRangeError("test message")
    
    def test_data_load_error_can_be_raised(self):
        """Test DataLoadError can be raised with message."""
        with pytest.raises(DataLoadError, match="test message"):
            raise DataLoadError("test message")
