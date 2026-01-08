# Example Questions & Expected Behaviors

This document provides example questions that the agent should be able to answer, along with guidance on what constitutes a good answer.

---

## Question Categories

### 1. Strategic Decision Making

#### Example 1:
**Question:** "If cotton tightens + energy rises, what's the best action: forward-buy, change mix, renegotiate terms, adjust production sequencing?"

**Expected Behavior:**
- Agent should identify relevant datasets (cotton price, energy futures)
- Analyze current trends and forecasts for both commodities
- Consider the relationship between cotton and energy (if any drivers indicate this)
- Provide a reasoned recommendation based on data
- State assumptions clearly (e.g., "Assuming you're a manufacturer using both cotton and energy...")

**Good Answer Elements:**
- References specific forecast values
- Mentions historical trends
- Considers multiple options
- Provides rationale for the recommendation
- States any assumptions made

---

#### Example 2:
**Question:** "Should I forward-buy cotton now or wait?"

**Expected Behavior:**
- Check current cotton price vs. forecast
- Analyze historical price patterns
- Consider volatility (from quantile forecasts)
- Provide data-driven recommendation

---

### 2. Supplier Negotiations

#### Example 3:
**Question:** "Provide a rationale for cotton price negotiation with the supplier using market drivers and forecasts."

**Expected Behavior:**
- Extract key drivers from `drivers.json` for cotton price
- Identify most important drivers (by importance score)
- Analyze forecast trends
- Provide negotiation talking points based on data
- Reference specific values and dates

**Good Answer Elements:**
- Lists top 3-5 drivers affecting cotton price
- Explains direction of impact (positive/negative)
- References forecast values with confidence intervals
- Provides specific negotiation arguments

---

#### Example 4:
**Question:** "What are the main factors driving cotton price increases?"

**Expected Behavior:**
- Parse `drivers.json` for cotton dataset
- Sort drivers by importance
- Explain each driver's impact
- Reference correlation metrics if relevant

---

### 3. Forecast Analysis

#### Example 5:
**Question:** "What is the forecasted price trend for cotton over the next 6 months?"

**Expected Behavior:**
- Extract forecast data from `forecast.json`
- Present forecast values chronologically
- Mention confidence intervals (quantiles)
- Compare with recent historical values
- Identify trend direction (increasing/decreasing/stable)

**Good Answer Elements:**
- Lists forecast values for each month
- Mentions uncertainty ranges (e.g., "between X and Y with 80% confidence")
- Compares forecast to last known value
- Identifies overall trend

---

#### Example 6:
**Question:** "What is the confidence interval for energy futures prices in Q1 2026?"

**Expected Behavior:**
- Extract relevant forecast dates
- Use quantile forecasts to calculate confidence intervals
- Present in a clear format (e.g., "90% confidence interval: X to Y")

---

### 4. Historical Analysis

#### Example 7:
**Question:** "How have cotton prices changed historically, and what are the main drivers?"

**Expected Behavior:**
- Load historical data from CSV
- Identify key trends (peaks, valleys, overall direction)
- Extract driver information
- Correlate historical events with price movements
- Reference specific dates and values

**Good Answer Elements:**
- Mentions key historical periods (e.g., "Peak in 2022")
- Provides specific values and dates
- Links historical patterns to drivers
- Identifies long-term trends

---

#### Example 8:
**Question:** "What was the highest cotton price in the dataset, and when did it occur?"

**Expected Behavior:**
- Query historical data
- Find maximum value
- Return exact date and value
- Optionally provide context (e.g., "This was during a period when...")

---

### 5. Comparative Analysis

#### Example 9:
**Question:** "What is the relationship between cotton export quantity and cotton price?"

**Expected Behavior:**
- Access both cotton price and export quantity datasets
- Analyze correlation (if data allows)
- Identify patterns (e.g., "When exports increase, prices...")
- Reference specific time periods

---

#### Example 10:
**Question:** "Compare the forecast accuracy assumptions for cotton vs. energy futures."

**Expected Behavior:**
- Extract quantile forecasts for both datasets
- Compare confidence intervals
- Discuss volatility differences
- Reference forecast methodology if available in drivers

---

## Answer Quality Checklist

When evaluating answers, consider:

- [ ] **Data Accuracy:** Are all numbers and dates correct?
- [ ] **Data Citations:** Are specific values referenced?
- [ ] **Assumptions Stated:** Are assumptions clearly mentioned?
- [ ] **Relevance:** Does the answer address the question?
- [ ] **Completeness:** Are all aspects of the question covered?
- [ ] **Clarity:** Is the answer easy to understand?
- [ ] **Reasoning:** Is the logic sound and data-driven?

---

## Edge Cases to Consider

1. **Ambiguous Questions:**
   - "What about cotton?" → Agent should ask for clarification or infer context

2. **Missing Data:**
   - Questions about dates outside the dataset → Agent should state data limitations

3. **Complex Multi-Dataset Questions:**
   - Questions requiring analysis across all three datasets → Agent should handle gracefully

4. **Mathematical Operations:**
   - Percentage changes, averages, trends → Calculations must be accurate

5. **Uncertainty Handling:**
   - When forecasts have wide confidence intervals → Agent should communicate uncertainty

---

## Testing Scenarios

Consider creating test cases for:

1. **Simple Queries:** "What is the current cotton price?"
2. **Complex Queries:** Multi-dataset analysis questions
3. **Edge Cases:** Out-of-range dates, missing data
4. **Error Handling:** Invalid questions, malformed queries
5. **Performance:** Response time for various query types

---

## Notes for Implementation

- The agent should be able to handle natural language variations of these questions
- Consider implementing a question classification system to route to appropriate tools
- Use LangGraph to create decision flows for different question types
- Implement proper error handling and graceful degradation
- Consider caching frequently accessed data for performance

