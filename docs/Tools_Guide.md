# Tools Guide: How the Procurement Agent Works

This guide explains the tools our agent uses to answer procurement questions. Tools are specialized functions that retrieve and analyze data - the agent picks the right tools based on your question and combines results into clear recommendations.

---

## How It Works

When you ask "Should I buy cotton now?", the agent:

1. **Understands** - Classifies your question type
2. **Selects tools** - Picks relevant data tools (price, forecast, etc.)
3. **Calls tools** - Gets structured data (numbers, dates, calculations)
4. **Responds** - Combines results into a clear recommendation

Tools handle math and data. The agent handles understanding and explanation.

---

## Tool Categories

We have 6 categories of tools:

1. **Historical Data Tools** - What happened in the past
2. **Forecast Tools** - What might happen in the future
3. **Driver Analysis Tools** - Why prices change
4. **Comparative Tools** - How commodities relate to each other
5. **Strategic Recommendation Tools** - What you should do
6. **Negotiation Support Tools** - How to negotiate with suppliers

---

## 1. Historical Data Tools

### `query_historical_data`

**What it does:** Gets past commodity prices and trends.

**How it works:**
- Reads CSV files with historical price data (monthly records)
- Can get the latest price, a specific date, or a date range
- Calculates trends and percentage changes

**Example:**
```
User: "What's the latest cotton price?"

Agent calls: query_historical_data(dataset_name="cotton_price")

Tool returns: {
  'query_type': 'latest',
  'dataset': 'cotton_price',
  'date': '2025-08-01',
  'value': 171.00
}

Agent responds: "The latest Pima Cotton Price is $171.00 per ton as of August 1, 2025."
```

---

### Helper Functions (used by query_historical_data)

**`get_latest_value`** - Gets the most recent price
- **Data source:** Reads last row from CSV file
- **Query:** `df.iloc[-1]` (pandas)
- Returns date and value

**`get_value_by_date`** - Gets price for a specific date
- **Data source:** Filters CSV by date
- **Query:** `df[df['Period'] == date]` (pandas)
- Returns value or error if date not found

**`get_values_by_range`** - Gets prices for a date range
- **Data source:** Filters CSV by date range
- **Query:** `df[(df['Period'] >= start) & (df['Period'] <= end)]`
- Returns list of date/value pairs

**`calculate_percentage_change`** - Calculates price change between two dates
- **Formula:** `((end_price - start_price) / start_price) × 100`
- **Example:** `(178.72 - 171.00) / 171.00 × 100 = 4.52%`
- Returns percentage and trend direction (increasing/decreasing/stable)

---

## 2. Forecast Tools

### `query_forecast_data`

**What it does:** Gets future price predictions with confidence intervals.

**How it works:**
- Reads JSON files with forecast data (up to 36 months ahead)
- Includes 7 confidence levels (quantiles): 0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9
- 0.5 quantile = median/expected forecast
- 0.1 and 0.9 = 80% confidence interval (range where price will likely fall)

**Example:**
```
User: "What will cotton cost in 3 months?"

Agent calls: query_forecast_data(dataset_name="cotton_price", months_ahead=3)

Tool returns: {
  'query_type': 'months_ahead',
  'dataset': 'cotton_price',
  'months_ahead': 3,
  'date': '2025-11-01',
  'forecast_value': 178.72
}

Agent responds: "The 3-month forecast for Pima Cotton Price is $178.72 per ton 
as of November 1, 2025, with moderate uncertainty (±5%)."
```

---

### Helper Functions

**`get_forecast`** - Gets median forecast for N months ahead
- **Data source:** JSON file with quantile forecasts
- **Query:** `quantile_forecast["0.5"][months_ahead - 1]`
- Returns date and forecast value

**`get_forecast_with_quantiles`** - Gets all confidence levels
- **Data source:** JSON file with all quantiles (0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9)
- **Query:** Extracts all quantile values for given months_ahead
- Used by impact analysis tool

---

## 3. Driver Analysis Tools

### `analyze_market_drivers`

**What it does:** Identifies what factors affect commodity prices.

**How it works:**
- Reads JSON files with driver data (economic indicators, correlations)
- Each driver has:
  - **Importance score** (0-100%) - how much it affects prices
  - **Direction** (positive/negative) - whether it pushes prices up or down
  - **Lag** (months) - how long before the effect shows up
  - **Correlation** - statistical relationship strength

**Example:**
```
User: "What factors affect cotton prices?"

Agent calls: analyze_market_drivers(dataset_name="cotton_price", top_n=5)

Tool returns: {
  'query_type': 'top_drivers',
  'dataset': 'cotton_price',
  'top_n': 5,
  'drivers': [
    {
      'name': 'Industry Turnover - Non-Domestic, Energy, Balkans',
      'importance_mean': 100.0,
      'direction': 'positive',
      'lag_months': 0
    },
    {
      'name': 'North America Finished Goods Prices',
      'importance_mean': 67.0,
      'direction': 'positive',
      'lag_months': 1
    },
    ...
  ]
}

Agent responds: "The top drivers affecting cotton prices include:
1. Industry Turnover - Non-Domestic, Energy, Balkans (100% importance)
2. North America Finished Goods Prices (67% importance)
..."
```

---

## 4. Comparative Tools

### `compare_commodities`

**What it does:** Compares multiple commodities to find relationships.

**How it works:**
- Loads historical data for multiple datasets
- Aligns data by date (finds common dates)
- Calculates correlation coefficient (-1 to +1)
  - +1 = perfect positive correlation (move together)
  - -1 = perfect negative correlation (move opposite)
  - 0 = no correlation

**Example:**
```
User: "Compare cotton and energy prices"

Agent calls: compare_commodities(dataset_names=["cotton_price", "energy_futures"])

Tool returns: {
  'query_type': 'multi_commodity_comparison',
  'datasets': ['cotton_price', 'energy_futures'],
  'aligned_data': [...],
  'correlation': -0.23
}

Agent responds: "Cotton and energy show weak negative correlation (-0.23), 
meaning they tend to move in opposite directions, though not strongly."
```

**Correlation Calculation:**
```
Pearson correlation coefficient (via pandas)

Interpretation:
  +0.7 to +1.0 = Strong positive (move together)
  +0.3 to +0.7 = Moderate positive
  -0.3 to +0.3 = Weak/no correlation
  -0.7 to -0.3 = Moderate negative
  -1.0 to -0.7 = Strong negative (move opposite)

Example: -0.23 = Weak negative correlation
```


---

## 5. Strategic Recommendation Tools

These tools help you make procurement decisions by analyzing data and providing actionable recommendations.

### `recommend_forward_buy`

**What it does:** Recommends whether to buy now or wait.

**How it works:**
1. Gets current price (using `get_latest_value`)
2. Gets forecast price (using `get_forecast`)
3. Calculates price change percentage
4. Makes recommendation based on thresholds:
   - **Rising >2%** → Buy now (lock in lower price)
   - **Falling <-2%** → Wait (prices dropping)
   - **Stable ±2%** → Monitor (no urgency)
   - **Uncertain 0.5-2%** → Hedge (buy partial, wait on rest)
5. Calculates savings: (price_change) × quantity

**Example:**
```
User: "Should I buy cotton now or wait?"

Agent calls: recommend_forward_buy(dataset_name="cotton_price", quantity=1000)

Tool returns: {
  'recommendation': 'buy_now',
  'current_price': 171.00,
  'current_date': '2025-08-01',
  'forecast_price': 178.72,
  'forecast_date': '2025-11-01',
  'price_change_pct': 4.52,
  'savings': 7720.00,
  'rationale': 'Price expected to rise 4.5%. Buy now to lock in lower price.'
}

Agent responds: "Recommendation: Buy cotton now

Current price: $171.00 per ton (August 1, 2025)
3-month forecast: $178.72 per ton (November 1, 2025)
Expected increase: +4.5%

Savings if you buy now: $7.72 per ton
For 1000 tons: $7,720 saved

Rationale: Price is rising. Buying now locks in lower price and avoids 4.5% increase."
```

**Calculation Formula:**
```
Price change % = (forecast - current) / current × 100
Savings = (forecast - current) × quantity

Example:
(178.72 - 171.00) / 171.00 × 100 = 4.52%
(178.72 - 171.00) × 1000 = $7,720.00
```

**Decision Logic:**
```python
if price_change_pct > 2%: recommendation = "buy_now"
elif price_change_pct < -2%: recommendation = "wait"
else: recommendation = "monitor"
```

---

### `calculate_impact_analysis`

**What it does:** Provides best-case, expected, and worst-case scenarios for risk assessment.

**How it works:**
1. Gets current price
2. Gets forecast with all quantiles (0.1, 0.5, 0.9)
3. Determines price direction (rising or falling)
4. Assigns scenarios:
   - **Rising prices:** 0.1 = best (lowest), 0.5 = expected, 0.9 = worst (highest)
   - **Falling prices:** 0.9 = best (highest), 0.5 = expected, 0.1 = worst (lowest)
5. Calculates savings/costs for each scenario

**Calculation:**
```
For rising prices:
  Best case = 0.1 quantile (lowest forecast)
  Expected = 0.5 quantile (median)
  Worst case = 0.9 quantile (highest forecast)

Impact = (forecast_price - current_price) × quantity

Example (1000 tons):
  Best: (175.20 - 171.00) × 1000 = $4,200
  Expected: (178.72 - 171.00) × 1000 = $7,720
  Worst: (182.50 - 171.00) × 1000 = $11,500
```

**Example usage:**
```
User: "What are the risks if I buy cotton now?"

Agent calls: calculate_impact_analysis(dataset_name="cotton_price", quantity=1000)

Tool returns: {
  'current_price': 171.00,
  'price_direction': 'rising',
  'best_case': {
    'forecast_price': 175.20,
    'total_impact': 4200.00
  },
  'expected': {
    'forecast_price': 178.72,
    'total_impact': 7720.00
  },
  'worst_case': {
    'forecast_price': 182.50,
    'total_impact': 11500.00
  }
}

Agent responds: "Impact Analysis for Cotton (1000 tons):

Best Case: Price rises to $175.20 → Cost increase: $4,200
Expected: Price rises to $178.72 → Cost increase: $7,720
Worst Case: Price rises to $182.50 → Cost increase: $11,500

Recommendation: Buy now to avoid these cost increases."
```


---

### `analyze_multi_commodity_scenario`

**What it does:** Analyzes complex scenarios involving multiple commodities.

**How it works:**
1. Calls `recommend_forward_buy` for each commodity
2. Calls `compare_commodities` to get correlations
3. Calculates urgency score for each commodity:
   - Buy_now = 3 points (high urgency)
   - Wait = 2 points (medium urgency)
   - Monitor/Hedge = 1 point (low urgency)
   - +1 point if price change >5%
4. Sorts by urgency (highest first)
5. Generates combined insights

**Urgency Scoring:**
```python
Base score:
  buy_now = 3, wait = 2, monitor/hedge = 1
Bonus: +1 if |price_change_pct| > 5%

Example:
  Cotton: buy_now (4.52%) → Score = 3
  Energy: buy_now (6.2%) → Score = 4 (bonus)
  Priority: Energy > Cotton
```

**Example usage:**
```
User: "If cotton rises and energy falls, what should I do?"

Agent calls: analyze_multi_commodity_scenario(
  dataset_names=["cotton_price", "energy_futures"]
)

Tool returns: {
  'prioritized_actions': [
    {
      'dataset': 'cotton_price',
      'recommendation': 'buy_now',
      'urgency_score': 4,
      'savings': 7720.00
    },
    {
      'dataset': 'energy_futures',
      'recommendation': 'wait',
      'urgency_score': 2,
      'savings': 500.00
    }
  ],
  'insights': [
    'Mixed signals: 1 commodity rising, 1 falling. Consider staggered procurement.'
  ],
  'total_potential_savings': 8220.00
}

Agent responds: "Multi-Commodity Strategy:

Priority 1: Buy cotton now (rising 4.5%) → Save $7,720
Priority 2: Wait on energy (falling 0.06%) → Save $500

Total potential savings: $8,220

Insight: Mixed market signals suggest staggered procurement approach."
```


---

### `recommend_production_sequencing`

**What it does:** Recommends which production activities to prioritize based on commodity costs.

**How it works:**
1. Gets forecasts for all commodities
2. Classifies each as:
   - **Favorable** (falling prices) → High priority
   - **Moderately favorable** (stable) → Medium priority
   - **Unfavorable** (rising prices) → Low priority (delay if possible)
3. Sorts by priority
4. Calculates cost impact

**Favorability Classification:**
```python
if price_change_pct <= 0: favorability = "favorable"
elif price_change_pct <= 2: favorability = "moderately_favorable"
else: favorability = "unfavorable"

Priority: favorable (1) > moderately_favorable (2) > unfavorable (3)
```

**Example usage:**
```
User: "Which production should I prioritize?"

Agent calls: recommend_production_sequencing(
  dataset_names=["cotton_price", "energy_futures", "cotton_export"]
)

Tool returns: {
  'recommended_sequence': [
    {
      'sequence_order': 1,
      'dataset': 'energy_futures',
      'recommendation': 'Prioritize production using energy_futures (prices falling 0.06%)',
      'favorability': 'moderately_favorable'
    },
    {
      'sequence_order': 2,
      'dataset': 'cotton_export',
      'recommendation': 'Schedule production using cotton_export normally (prices stable)',
      'favorability': 'moderately_favorable'
    },
    {
      'sequence_order': 3,
      'dataset': 'cotton_price',
      'recommendation': 'Delay production using cotton_price if possible (prices rising 4.5%)',
      'favorability': 'unfavorable'
    }
  ]
}

Agent responds: "Production Sequencing Recommendation:

1. Prioritize: Energy-intensive production (stable costs)
2. Normal schedule: Cotton export production (stable)
3. Delay if possible: Cotton price production (rising costs +4.5%)

Cost impact: Prioritizing favorable commodities saves ~2% on production costs."
```


---

## 6. Negotiation Support Tools

These tools help you prepare for and conduct supplier negotiations with data-backed arguments.

### `generate_negotiation_talking_points`

**What it does:** Creates 3-5 data-backed talking points for negotiations.

**How it works:**
1. Gets current price, forecast, and top drivers
2. Generates talking points:
   - Point 1: Current market price (fact)
   - Point 2: Forecast trend (supporting or contradicting supplier's claim)
   - Points 3-5: Top market drivers (evidence for your position)
3. Classifies each point as supporting or contradicting price increases

**Example usage:**
```
User: "Give me talking points for negotiating cotton prices"

Agent calls: generate_negotiation_talking_points(dataset_name="cotton_price")

Tool returns: {
  'talking_points': [
    {
      'point': 'Current market price is $171.00 as of 2025-08-01',
      'type': 'fact',
      'citation': 'Historical data: cotton_price'
    },
    {
      'point': 'Forecast shows 4.5% increase to $178.72 by 2025-11-01',
      'type': 'supporting_increase',
      'citation': 'Forecast data: cotton_price'
    },
    {
      'point': 'Industry Turnover - Balkans (100% importance) shows positive correlation',
      'type': 'supporting_increase',
      'citation': 'Driver analysis: cotton_price'
    }
  ]
}

Agent responds: "Negotiation Talking Points for Cotton:

1. Current market price: $171.00 (Aug 2025)
2. Forecast: 4.5% increase to $178.72 by Nov 2025
3. Key driver: Industry Turnover - Balkans (100% importance, positive)"
```

---

### `validate_supplier_claim`

**What it does:** Compares supplier price claims against forecast data.

**How it works:**
1. Gets forecast with confidence intervals (0.1, 0.5, 0.9 quantiles)
2. Compares supplier's claimed price vs forecast median
3. Calculates difference (absolute and percentage)
4. Classifies claim:
   - **Above forecast range** (>0.9 quantile) → Challenge
   - **Above forecast** (>median +2%) → Negotiate down
   - **Aligned** (within ±2% of median) → Reasonable
   - **Below forecast** (<median -2%) → Good deal
   - **Below range** (<0.1 quantile) → Excellent deal

**Example usage:**
```
User: "My supplier claims cotton will cost $190 in 3 months. Is this reasonable?"

Agent calls: validate_supplier_claim(
  dataset_name="cotton_price",
  claimed_price=190.00,
  months_ahead=3
)

Tool returns: {
  'claimed_price': 190.00,
  'forecast_median': 178.72,
  'forecast_range': {'low': 170.50, 'high': 187.20},
  'difference_abs': 11.28,
  'difference_pct': 6.31,
  'classification': 'above_forecast_range',
  'verdict': 'Challenge this claim - significantly above forecast'
}

Agent responds: "Supplier's claim ($190) is 6.3% above forecast ($178.72) and exceeds 
the forecast range ($170.50-$187.20). Verdict: Challenge this claim."
```


---

### `identify_driver_arguments`

**What it does:** Identifies which market drivers support or contradict price movements.

**How it works:**
1. Gets all drivers for the commodity
2. Classifies based on direction and price movement:
   - **Supporting increase:** Positive drivers (if arguing for higher prices)
   - **Contradicting increase:** Negative drivers (if arguing against higher prices)
3. Ranks by importance score
4. Returns top 5 of each type

**Example usage:**
```
User: "What drivers support or contradict a cotton price increase?"

Agent calls: identify_driver_arguments(
  dataset_name="cotton_price",
  price_direction="increase"
)

Tool returns: {
  'supporting_drivers': [
    {'name': 'Industry Turnover - Balkans', 'importance_mean': 100.0, 'direction': 'positive'},
    {'name': 'North America Finished Goods', 'importance_mean': 67.0, 'direction': 'positive'}
  ],
  'contradicting_drivers': [
    {'name': 'Energy Costs', 'importance_mean': 45.0, 'direction': 'negative'}
  ],
  'balance': {
    'supporting_count': 3,
    'contradicting_count': 2,
    'net_sentiment': 'bullish'
  }
}

Agent responds: "Supporting: Industry Turnover - Balkans (100%), North America Finished Goods (67%). 
Contradicting: Energy Costs (45%). Balance: 3 supporting vs 2 contradicting = Bullish."
```

---

## How Tools Work Together

When you ask "Should I buy cotton now?", the agent calls `recommend_forward_buy` which internally uses `get_latest_value` and `get_forecast`, calculates the price change, applies decision logic, and returns exact savings. The agent then explains the recommendation with data citations.

---

## Tool Accuracy

- **Precision:** All calculations to 2 decimal places
- **Consistency:** Same inputs always produce same outputs
- **Traceability:** Every number cites its source (historical/forecast/driver data)

---

## Summary

The agent combines natural language understanding with precise calculations. You ask questions in plain English, the agent selects the right tools to gather data and run calculations, then explains results with exact numbers and clear recommendations.

---

## Architecture: Prompt vs Tool

| **Component** | **Approach** | **Why** |
|---------------|-------------|---------|
| **Question Classification** | Prompt | LLM understands natural language intent |
| **Tool Selection** | Prompt | Agent decides which tools to call |
| **Data Retrieval** | Tool | Direct file access (CSV/JSON) |
| **Calculations** | Tool | Exact arithmetic, no LLM errors |
| **Decision Logic** | Tool | Deterministic thresholds (if price > 2% → buy) |
| **Citation Formatting** | Prompt | Presentation style (bold, dates, values) |
| **Reasoning & Explanation** | Prompt | Natural language contextualizing |
| **Response Synthesis** | Prompt | Combines tool results into helpful answer |

**Summary:** Tools = Accurate data & calculations. Prompt = Understanding & explanation.
