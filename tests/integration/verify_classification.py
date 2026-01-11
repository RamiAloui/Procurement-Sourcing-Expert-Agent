"""Integration test for question classification and routing."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.agent import invoke_agent

print("=" * 70)
print("Testing Question Classification and Routing")
print("=" * 70)

# Test 1: Historical Analysis
print("\n1. HISTORICAL ANALYSIS")
print("-" * 70)
try:
    response = invoke_agent("What's the latest cotton price?")
    print(f"Q: What's the latest cotton price?")
    print(f"A: {response[:200]}...")
    print("✅ Historical query handled")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 2: Forecast Analysis
print("\n2. FORECAST ANALYSIS")
print("-" * 70)
try:
    response = invoke_agent("What will cotton cost next month?")
    print(f"Q: What will cotton cost next month?")
    print(f"A: {response[:200]}...")
    print("✅ Forecast query handled")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 3: Market Drivers
print("\n3. MARKET DRIVERS")
print("-" * 70)
try:
    response = invoke_agent("What affects energy prices?")
    print(f"Q: What affects energy prices?")
    print(f"A: {response[:200]}...")
    print("✅ Drivers query handled")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 4: Comparative Analysis
print("\n4. COMPARATIVE ANALYSIS")
print("-" * 70)
try:
    response = invoke_agent("Compare cotton and energy")
    print(f"Q: Compare cotton and energy")
    print(f"A: {response[:200]}...")
    print("✅ Comparative query handled")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 5: Strategic/Complex (Multi-tool)
print("\n5. STRATEGIC/COMPLEX (Multi-tool)")
print("-" * 70)
try:
    response = invoke_agent("Should I buy cotton now or wait?")
    print(f"Q: Should I buy cotton now or wait?")
    print(f"A: {response[:200]}...")
    print("✅ Strategic query handled")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 6: Ambiguous Question
print("\n6. AMBIGUOUS QUESTION HANDLING")
print("-" * 70)
try:
    response = invoke_agent("Show me prices")
    print(f"Q: Show me prices")
    print(f"A: {response[:200]}...")
    if "which" in response.lower() or "clarify" in response.lower():
        print("✅ Agent asked for clarification")
    else:
        print("⚠️ Agent may not have asked for clarification")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "=" * 70)
print("Classification Testing Complete")
print("=" * 70)
print("\nNext: Check LangSmith traces to verify:")
print("- Classification reasoning is visible")
print("- Correct tools selected for each intent type")
print("- Multi-tool invocation for strategic questions")
