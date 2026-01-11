"""Integration test for forward-buy recommendations."""

from src.agent.agent import invoke_agent


def test_rising_price_scenario():
    """Test buy recommendation for rising prices (cotton)."""
    print("\n" + "="*80)
    print("TEST 1: Rising Price Scenario (Cotton)")
    print("="*80)
    
    query = "Should I buy cotton now or wait?"
    print(f"\nQuery: {query}")
    print("\nExpected: Buy now recommendation with quantified savings")
    print("Data: Current $171, Forecast $178.72 (+4.5%)\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    # Check for key elements
    checks = {
        "Contains 'buy'": "buy" in response.lower(),
        "Contains price data": "$" in response,
        "Contains savings": "save" in response.lower() or "savings" in response.lower(),
        "Contains rationale": len(response) > 100
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_stable_price_scenario():
    """Test monitor recommendation for stable prices."""
    print("\n" + "="*80)
    print("TEST 2: Stable Price Scenario (Energy Futures)")
    print("="*80)
    
    query = "Should I buy energy futures now?"
    print(f"\nQuery: {query}")
    print("\nExpected: Monitor/hedge recommendation")
    print("Data: Minimal price change (-0.06%)\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains recommendation": any(word in response.lower() for word in ["monitor", "hedge", "wait", "stable"]),
        "Contains price data": "$" in response,
        "Contains rationale": len(response) > 100
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_savings_quantification():
    """Test that savings are quantified correctly."""
    print("\n" + "="*80)
    print("TEST 3: Savings Quantification")
    print("="*80)
    
    query = "How much will I save if I buy 1000 tons of cotton now?"
    print(f"\nQuery: {query}")
    print("\nExpected: Exact dollar amount calculated")
    print("Verify: (forecast - current) × 1000 = savings\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains dollar amount": "$" in response,
        "Contains quantity": "1000" in response or "thousand" in response.lower(),
        "Contains calculation": any(word in response.lower() for word in ["save", "savings", "cost"]),
        "Cites data": "forecast" in response.lower() or "current" in response.lower()
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_data_citations():
    """Test that agent cites data sources correctly."""
    print("\n" + "="*80)
    print("TEST 4: Data Citations")
    print("="*80)
    
    query = "Give me a forward-buy recommendation for cotton with full details"
    print(f"\nQuery: {query}")
    print("\nExpected: Response includes dates, prices, and data sources\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains dates": "2025" in response,
        "Contains prices": "$" in response,
        "Contains dataset name": "cotton" in response.lower(),
        "Contains forecast info": "forecast" in response.lower(),
        "Well formatted": "**" in response or "\n" in response
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MANUAL INTEGRATION TEST: Forward-Buy Recommendations")
    print("="*80)
    print("\nThis test verifies the agent uses recommend_forward_buy tool correctly")
    print("and provides clear, data-backed recommendations.\n")
    
    try:
        test_rising_price_scenario()
        test_stable_price_scenario()
        test_savings_quantification()
        test_data_citations()
        
        print("\n" + "="*80)
        print("TESTS COMPLETE")
        print("="*80)
        print("\nReview the responses above to verify:")
        print("  1. Agent calls recommend_forward_buy tool")
        print("  2. Recommendations are clear and actionable")
        print("  3. Data citations are accurate")
        print("  4. Savings calculations are correct")
        print("\nCheck LangSmith traces for detailed tool usage verification.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
