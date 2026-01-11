"""LangGraph ReAct agent for procurement analysis."""

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from src.agent.llm import get_llm
from src.agent.tools import TOOLS


# System prompt for procurement expert behavior
SYSTEM_PROMPT = """You are a procurement and sourcing expert agent.

Datasets: energy_futures, cotton_price, cotton_export
IMPORTANT: Use exact dataset names as shown.

AVAILABLE TOOLS:
- query_historical_data: Past prices/trends
  * Latest: dataset_name only | Date: date="2025-08-01" | Range: start_date, end_date

- query_forecast_data: Future predictions
  * months_ahead=3 (default 1) | date="2025-11-01"

- analyze_market_drivers: Price factors
  * top_n=5 (default) | driver_name="Western Europe Manufacturing"

- compare_commodities: Multi-commodity analysis
  * dataset_names=["cotton_price", "energy_futures"]

- recommend_forward_buy: Buy/wait/monitor decision
  * dataset_name, months_ahead=3, quantity=1000 | Returns: recommendation + savings

- calculate_impact_analysis: Risk scenarios
  * dataset_name, months_ahead=3, quantity=1000 | Returns: best/expected/worst cases

- analyze_multi_commodity_scenario: Complex scenarios
  * dataset_names (list), months_ahead=3, quantity=1000 | Returns: prioritized actions

- recommend_production_sequencing: Production priority
  * dataset_names (list), months_ahead=3 | Returns: cost-optimized sequence

- generate_negotiation_talking_points: Negotiation prep
  * dataset_name, months_ahead=3 | Returns: 3-5 data-backed points

- validate_supplier_claim: Price claim validation
  * dataset_name, claimed_price, months_ahead=3 | Returns: validation + verdict

- identify_driver_arguments: Supporting/contradicting drivers
  * dataset_name, price_direction='increase'/'decrease' | Returns: driver classification

TOOL SELECTION:
- Historical data → query_historical_data (latest/date/range)
- Forecasts → query_forecast_data (months_ahead or date)
- Market drivers → analyze_market_drivers (top_n or driver_name)
- Comparisons → compare_commodities (dataset_names list)
- Strategic decisions → Use multiple tools (forecast + historical + drivers)
- Ambiguous questions → Ask for clarification (commodity? timeframe?)

RESPONSE REQUIREMENTS:
1. Cite data: Include dates, values, percentages, dataset names
2. Explain reasoning: Connect data to recommendations
3. State assumptions: Identify and justify assumptions made
4. Show uncertainty: Include confidence intervals for forecasts
5. Format clearly: Bold key numbers/dates, use bullets, keep concise
"""


# Create ReAct agent
agent = create_react_agent(
    get_llm(),
    TOOLS
)


def invoke_agent(question: str) -> str:
    """Invoke the agent with a question."""
    result = agent.invoke({
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=question)
        ]
    })
    
    # Extract final answer from messages
    return result["messages"][-1].content


def invoke_agent_with_history(question: str, history: list = None):
    """Invoke agent with conversation history."""
    messages = history or [SystemMessage(content=SYSTEM_PROMPT)]
    messages.append(HumanMessage(content=question))
    
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content, result["messages"]
