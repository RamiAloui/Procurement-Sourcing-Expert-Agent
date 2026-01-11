"""Integration test for response generation with data citations."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.agent import invoke_agent

print("=" * 70)
print("Testing Response Generation with Citations")
print("=" * 70)

# Test 1: Historical Query - Check Date and Value Citations
print("\n1. HISTORICAL QUERY - DATE AND VALUE CITATIONS")
print("-" * 70)
try:
    response = invoke_agent("What's the latest cotton price?")
    print(f"Q: What's the latest cotton price?")
    print(f"A: {response}\n")
    
    # Check for citations
    has_value = any(char.isdigit() for char in response)
    has_date = "202" in response  # Year format
    has_bold = "**" in response
    
    print("Citation checks:")
    print(f"  {'✅' if has_value else '❌'} Contains numeric value")
    print(f"  {'✅' if has_date else '❌'} Contains date reference")
    print(f"  {'✅' if has_bold else '❌'} Uses bold formatting")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 2: Forecast Query - Check Confidence Intervals
print("\n2. FORECAST QUERY - CONFIDENCE INTERVALS")
print("-" * 70)
try:
    response = invoke_agent("What will cotton cost in 3 months?")
    print(f"Q: What will cotton cost in 3 months?")
    print(f"A: {response}\n")
    
    # Check for forecast elements
    has_forecast_value = any(char.isdigit() for char in response)
    has_uncertainty = any(word in response.lower() for word in ["uncertainty", "confidence", "interval", "±"])
    
    print("Forecast checks:")
    print(f"  {'✅' if has_forecast_value else '❌'} Contains forecast value")
    print(f"  {'✅' if has_uncertainty else '❌'} Mentions uncertainty/confidence")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 3: Strategic Query - Check Reasoning Explanation
print("\n3. STRATEGIC QUERY - REASONING EXPLANATION")
print("-" * 70)
try:
    response = invoke_agent("Should I buy cotton now or wait?")
    print(f"Q: Should I buy cotton now or wait?")
    print(f"A: {response}\n")
    
    # Check for reasoning elements
    has_reasoning = any(word in response.lower() for word in ["since", "because", "therefore", "shows", "indicates"])
    has_data = any(char.isdigit() for char in response)
    has_recommendation = any(word in response.lower() for word in ["buy", "wait", "recommend", "suggest"])
    
    print("Reasoning checks:")
    print(f"  {'✅' if has_reasoning else '❌'} Contains reasoning words")
    print(f"  {'✅' if has_data else '❌'} Cites data to support reasoning")
    print(f"  {'✅' if has_recommendation else '❌'} Provides recommendation")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 4: Complex Query - Check Assumption Statements
print("\n4. COMPLEX QUERY - ASSUMPTION STATEMENTS")
print("-" * 70)
try:
    response = invoke_agent("What's the best procurement strategy for energy?")
    print(f"Q: What's the best procurement strategy for energy?")
    print(f"A: {response}\n")
    
    # Check for assumptions
    has_assumption = any(word in response.lower() for word in ["assuming", "assumption", "assumes", "if"])
    has_strategy = any(word in response.lower() for word in ["strategy", "approach", "recommend"])
    
    print("Assumption checks:")
    print(f"  {'✅' if has_assumption else '❌'} States assumptions")
    print(f"  {'✅' if has_strategy else '❌'} Provides strategy")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 5: Response Formatting
print("\n5. RESPONSE FORMATTING")
print("-" * 70)
try:
    response = invoke_agent("Compare cotton and energy prices")
    print(f"Q: Compare cotton and energy prices")
    print(f"A: {response}\n")
    
    # Check formatting elements
    has_bold = "**" in response
    has_bullets = any(marker in response for marker in ["- ", "* ", "• "])
    has_numbers = any(char.isdigit() for char in response)
    is_structured = "\n" in response  # Has line breaks
    
    print("Formatting checks:")
    print(f"  {'✅' if has_bold else '❌'} Uses bold for emphasis")
    print(f"  {'✅' if has_bullets else '❌'} Uses bullet points")
    print(f"  {'✅' if has_numbers else '❌'} Cites numeric data")
    print(f"  {'✅' if is_structured else '❌'} Uses structured formatting")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "=" * 70)
print("Citation Testing Complete")
print("=" * 70)
print("\nNext: Check LangSmith traces to verify:")
print("- Tool results match cited data")
print("- Reasoning is traceable")
print("- Citations are accurate")
