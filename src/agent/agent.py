"""LangGraph ReAct agent for procurement analysis."""

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from src.agent.llm import get_llm
from src.agent.tools import TOOLS


# System prompt for agent behavior
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

AMBIGUITY HANDLING:
If question lacks commodity/timeframe/metric, ask for clarification BEFORE calling tools.

Examples:
- "What's the price?" → Ask which commodity (energy_futures, cotton_price, cotton_export)
- "Should I buy cotton?" → Ask timeframe (current, next month, specific date)
- "Tell me about cotton" → Ask what info (prices, forecasts, drivers, recommendations)
- "Is it going up?" → Ask which commodity and timeframe

Rules: NEVER guess. ALWAYS ask with 2-3 options. Only call tools when you have all info.

ERROR HANDLING:
When tools return errors (success=False), present them conversationally:
- Explain the issue in simple terms
- Present alternative queries from the "alternatives" field as options
- Keep tone helpful, not technical
Example: "I don't have data for that date yet. My data goes up to Oct 2025. Here are some things I can help with: [list alternatives]"

RESPONSE REQUIREMENTS:
1. Cite data: Include dates, values, percentages, dataset names
2. Explain reasoning: Connect data to recommendations
3. State assumptions: Identify and justify assumptions made
4. Show uncertainty: Include confidence intervals for forecasts
5. Format clearly: Bold key numbers/dates, use bullets, keep concise

FORMATTING RULES:
- Use ONLY standard markdown: **bold**, *italic*, bullet lists, numbered lists
- NEVER use LaTeX math syntax (no $, $$, \*, or math formulas)
- Write calculations in plain text: "171.00/ton" not "$171.00/ton$"
- Use plain asterisks for multiplication: "5 * 10" not "5 ∗ 10"
- Keep all text readable without special rendering
"""


# ReAct agent
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


def stream_agent(question: str, history: list = None):
    """Stream agent response with both state updates and LLM tokens.
    
    Args:
        question: User's question
        history: Optional list of previous messages for context
    
    Yields tuples of (chunk_type, content):
    - ('status', 'message') for agent state updates (tool calls, etc.)
    - ('token', 'text') for LLM token streaming
    """
    # Message list with history to maintain context
    messages = history or []
    messages.append(SystemMessage(content=SYSTEM_PROMPT))
    messages.append(HumanMessage(content=question))
    
    for mode, chunk in agent.stream(
        {"messages": messages},
        stream_mode=["updates", "messages"]  # Both agent state AND tokens
    ):
        # Handle based on stream mode
        if mode == "messages":
            # Messages mode: (token, metadata)
            token, metadata = chunk
            node = metadata.get('langgraph_node')
            
            if node == 'agent':
                # Stream LLM tokens
                if hasattr(token, 'content') and token.content:
                    yield ('token', token.content)
        
        elif mode == "updates":
            for node_name, node_data in chunk.items():
                if node_name == 'tools':
                    # Tool execution
                    messages = node_data.get('messages', [])
                    if messages:
                        tool_msg = messages[-1]
                        if hasattr(tool_msg, 'name'):
                            yield ('status', f"Using tool: {tool_msg.name}")
                
                elif node_name == 'agent':
                    # Agent planning or thinking
                    messages = node_data.get('messages', [])
                    if messages:
                        last_msg = messages[-1]
                        # To check if agent is calling tools
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            tool_names = [tc['name'] for tc in last_msg.tool_calls]
                            yield ('status', f"Calling tools: {', '.join(tool_names)}")


def invoke_agent_with_history(question: str, history: list = None):
    """Invoke agent with conversation history."""
    messages = history or [SystemMessage(content=SYSTEM_PROMPT)]
    messages.append(HumanMessage(content=question))
    
    result = agent.invoke({"messages": messages})
    return result["messages"][-1].content, result["messages"]
