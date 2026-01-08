# Data Structure Reference Guide

This document provides detailed information about the data structure and formats used in the challenge.

---

## Directory Structure

```
Data/
├── #1181-Dataset_Germany Energy Futures, Settlement Price/
│   ├── historical_data.csv
│   ├── forecast.json
│   └── drivers.json
├── #1597-Dataset_Pima Cotton Price/
│   ├── historical_data.csv
│   ├── forecast.json
│   └── drivers.json
└── #1616-Dataset_Pima Cotton Export Quantity/
    ├── historical_data.csv
    ├── forecast.json
    └── drivers.json
```

---

## File Formats

### 1. `historical_data.csv`

**Format:** CSV with header row

**Columns:**
- `Period`: Date in `YYYY-MM-DD` format (always the first of the month)
- `Value`: Numeric value (float or integer)

**Example:**
```csv
Period,Value
2017-04-01,29.365000000000002
2017-05-01,29.569090909090907
2017-06-01,30.645909090909093
```

**Notes:**
- Dates are monthly (first day of each month)
- Values may be prices, quantities, or indices depending on the dataset
- Some datasets may have longer historical ranges than others

---

### 2. `forecast.json`

**Format:** JSON object

**Structure:**
```json
{
    "forecast_start": "YYYY-MM-DD",
    "forecast_end": "YYYY-MM-DD",
    "forecast_horizon": <number>,
    "last_valid_data_index": "YYYY-MM-DD",
    "forecast_series": {
        "YYYY-MM-DD": {
            "forecast": <float>,
            "quantile_forecast": {
                "0.1": <float>,
                "0.15": <float>,
                "0.25": <float>,
                "0.5": <float>,
                "0.75": <float>,
                "0.85": <float>,
                "0.9": <float>
            }
        },
        ...
    }
}
```

**Fields:**
- `forecast_start`: First forecast date
- `forecast_end`: Last forecast date
- `forecast_horizon`: Number of months forecasted
- `last_valid_data_index`: Last date with actual historical data
- `forecast_series`: Object with dates as keys
  - `forecast`: Point forecast (median, typically 0.5 quantile)
  - `quantile_forecast`: Confidence intervals
    - `0.1`, `0.9`: 80% confidence interval
    - `0.15`, `0.85`: 70% confidence interval
    - `0.25`, `0.75`: 50% confidence interval (interquartile range)
    - `0.5`: Median forecast

**Example:**
```json
{
    "forecast_start": "2025-09-01",
    "forecast_end": "2026-02-01",
    "forecast_horizon": 6,
    "last_valid_data_index": "2025-08-01",
    "forecast_series": {
        "2025-09-01": {
            "forecast": 173.476,
            "quantile_forecast": {
                "0.1": 165.831,
                "0.5": 173.476,
                "0.9": 179.519
            }
        }
    }
}
```

**Usage Tips:**
- Use `forecast` for point estimates
- Use quantiles to express uncertainty (e.g., "80% confidence interval")
- Compare forecasts with `last_valid_data_index` to understand trend

---

### 3. `drivers.json`

**Format:** JSON object (complex nested structure)

**Top-Level Structure:**
```json
{
    "target_<ID>": {
        "driver_name": "<name>",
        "normalized_series": { ... },
        ...
    },
    "<driver_id>": {
        "driver_name": "<name>",
        "importance": { ... },
        "direction": { ... },
        "overall_lag": "<description>",
        "normalized_series": { ... },
        "granger_correlation": { ... },
        "pearson_correlation": { ... },
        ...
    },
    ...
}
```

**Key Fields:**

#### `target_<ID>` (Self-reference)
- `driver_name`: Name of the target variable
- `normalized_series`: Normalized historical values (0-1 scale)

#### Driver Objects (`<driver_id>`)
- `driver_name`: Name/description of the driver
- `importance`: Impact score
  - `overall`: `{max, min, mean}`
  - `horizon_X`: Importance at specific forecast horizons
- `direction`: Correlation direction
  - `overall.mean`: `1` (positive) or `-1` (negative)
  - `horizon_X.<lag>`: Direction at specific horizons
- `overall_lag`: Lag description (e.g., "6 to 12 month(s)")
- `normalized_series`: Time series data (0-1 normalized)
- `granger_correlation`: Granger causality test results
  - `lag_X`: Correlation at specific lag
  - `overall`: `{max, min, mean}`
- `pearson_correlation`: Pearson correlation coefficients
  - `lag_X`: Correlation at specific lag
  - `overall`: `{max, min, mean}`

**Example Driver:**
```json
{
    "0a4908606abc593864806813b3a973e5": {
        "driver_name": "Turnover in industry, turnover, MIG - energy, Mediterranean",
        "importance": {
            "overall": {
                "max": 39.723416,
                "min": 5.088695,
                "mean": 23.752833
            },
            "horizon_1": {
                "12.0": 37.310208
            }
        },
        "direction": {
            "overall": {
                "mean": 1
            }
        },
        "overall_lag": "6 to 12 month(s)",
        "normalized_series": {
            "2017-04-01": 0.03075430511763279,
            ...
        },
        "granger_correlation": {
            "lag_12": 0.999997,
            "overall": {
                "max": 0.999999,
                "min": 0,
                "mean": 0.402283
            }
        },
        "pearson_correlation": {
            "lag_12": 0.062001,
            "overall": {
                "max": 0.240407,
                "min": 0.04943,
                "mean": 0.128768
            }
        }
    }
}
```

**Usage Tips:**
- Sort drivers by `importance.overall.mean` to find most impactful drivers
- Use `direction.overall.mean` to understand if driver increases (+) or decreases (-) the target
- `overall_lag` tells you how far ahead/behind the driver is (e.g., "6 months ahead")
- Higher `granger_correlation` indicates stronger predictive relationship
- `normalized_series` can be used to plot driver trends alongside target trends

---

## Dataset-Specific Information

### Dataset #1181: Germany Energy Futures, Settlement Price
- **Type:** Price/Index
- **Unit:** Likely EUR/MWh or similar energy unit
- **Historical Range:** 2017-04-01 to 2025-10-01 (approximately)
- **Key Characteristics:** Shows significant volatility, especially in 2021-2022

### Dataset #1597: Pima Cotton Price
- **Type:** Price
- **Unit:** Likely USD per unit (e.g., cents/pound)
- **Historical Range:** 2014-01-01 to 2025-08-01 (approximately)
- **Key Characteristics:** Shows price cycles, significant increase in 2021-2022

### Dataset #1616: Pima Cotton Export Quantity
- **Type:** Quantity
- **Unit:** Likely metric tons or similar quantity unit
- **Historical Range:** 1990-01-01 to 2025-08-01 (approximately)
- **Key Characteristics:** Longer historical range, shows seasonal patterns

---

## Data Access Patterns

### Common Queries

1. **Get latest historical value:**
   - Read CSV, find last row, extract `Value`

2. **Get forecast for specific month:**
   - Parse `forecast.json`, access `forecast_series["YYYY-MM-DD"]`

3. **Get top N drivers:**
   - Parse `drivers.json`, sort by `importance.overall.mean`, take top N

4. **Compare historical vs forecast:**
   - Get last value from CSV
   - Get first forecast from JSON
   - Calculate change/trend

5. **Get driver time series:**
   - Access `normalized_series` in driver object
   - Note: Values are normalized (0-1), may need to denormalize for comparison

---

## Implementation Suggestions

### Python Libraries
- `pandas`: For CSV reading and data manipulation
- `json`: For parsing JSON files
- `pathlib`: For file path handling

### Example Code Snippets

```python
import pandas as pd
import json
from pathlib import Path

# Load historical data
def load_historical_data(dataset_path):
    csv_path = Path(dataset_path) / "historical_data.csv"
    df = pd.read_csv(csv_path, parse_dates=['Period'])
    return df

# Load forecast
def load_forecast(dataset_path):
    json_path = Path(dataset_path) / "forecast.json"
    with open(json_path) as f:
        return json.load(f)

# Load drivers
def load_drivers(dataset_path):
    json_path = Path(dataset_path) / "drivers.json"
    with open(json_path) as f:
        return json.load(f)

# Get top drivers
def get_top_drivers(drivers_data, n=5):
    drivers = []
    for driver_id, driver_info in drivers_data.items():
        if driver_id.startswith('target_'):
            continue
        importance = driver_info.get('importance', {}).get('overall', {}).get('mean', 0)
        drivers.append({
            'id': driver_id,
            'name': driver_info.get('driver_name', 'Unknown'),
            'importance': importance
        })
    return sorted(drivers, key=lambda x: x['importance'], reverse=True)[:n]
```

---

## Notes

- All dates are in `YYYY-MM-DD` format with day always being `01` (first of month)
- Some driver series may have `null` values for certain dates
- Normalized series values range from 0 to 1
- Importance scores are relative within each dataset
- Correlation values can be positive or negative
- Lag values indicate how many months ahead/behind the driver is relative to the target

---

## Troubleshooting

**Issue:** Cannot find a specific date in forecast
- **Solution:** Check `forecast_start` and `forecast_end` - forecasts may not cover all requested dates

**Issue:** Driver importance seems inconsistent
- **Solution:** Importance is relative to other drivers in the same dataset, compare within dataset only

**Issue:** Normalized series values don't match historical values
- **Solution:** Normalized series uses min-max normalization (0-1 scale), not actual values

**Issue:** Missing data in historical CSV
- **Solution:** Some months may be missing - handle gracefully, check date ranges

