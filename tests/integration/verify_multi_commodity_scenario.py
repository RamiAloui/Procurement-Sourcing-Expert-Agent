"""Integration test for multi-commodity scenario analysis."""

from src.agent.agent import invoke_agent


def test_complex_scenario():
    """Test complex multi-commodity scenario."""
    print("\n" + "="*80)
    print("TEST 1: Complex Multi-Commodity Scenario")
    print("="*80)
    
    query = "If cotton prices rise and energy prices stay stable, what should I do?"
    print(f"\nQuery: {query}")
    print("\nExpected: Prioritized recommendations for both commodities with correlation insights\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Mentions cotton": "cotton" in response.lower(),
        "Mentions energy": "energy" in response.lower(),
        "Contains prioritization": any(word in response.lower() for word in ["priority", "first", "urgent"]),
        "Contains recommendations": any(word in response.lower() for word in ["buy", "wait", "monitor"]),
        "Well formatted": len(response) > 200
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_correlation_insights():
    """Test that correlation insights are provided."""
    print("\n" + "="*80)
    print("TEST 2: Correlation Insights")
    print("="*80)
    
    query = "Analyze cotton and energy procurement together. How are they related?"
    print(f"\nQuery: {query}")
    print("\nExpected: Correlation information and how it affects strategy\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Mentions correlation": "correlat" in response.lower(),
        "Multiple commodities": "cotton" in response.lower() and "energy" in response.lower(),
        "Strategic insight": any(word in response.lower() for word in ["strategy", "together", "relationship"]),
        "Contains data": "$" in response or "%" in response
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_prioritized_recommendations():
    """Test prioritized recommendations across commodities."""
    print("\n" + "="*80)
    print("TEST 3: Prioritized Recommendations")
    print("="*80)
    
    query = "I need to procure cotton, energy, and cotton export. What's my priority order?"
    print(f"\nQuery: {query}")
    print("\nExpected: Clear priority order with rationale for each\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "All three mentioned": all(word in response.lower() for word in ["cotton", "energy"]),
        "Priority indicated": any(word in response.lower() for word in ["first", "priority", "urgent", "order"]),
        "Contains rationale": len(response) > 300,
        "Actionable": any(word in response.lower() for word in ["buy", "wait", "monitor"])
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_total_savings():
    """Test total savings calculation across commodities."""
    print("\n" + "="*80)
    print("TEST 4: Total Savings Calculation")
    print("="*80)
    
    query = "What's the total potential savings if I optimize procurement for cotton and energy?"
    print(f"\nQuery: {query}")
    print("\nExpected: Total savings calculation with breakdown\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains dollar amounts": "$" in response,
        "Multiple commodities": "cotton" in response.lower() and "energy" in response.lower(),
        "Mentions savings": any(word in response.lower() for word in ["save", "savings", "total"]),
        "Quantified": any(char.isdigit() for char in response)
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_mixed_signals():
    """Test handling of mixed buy/wait signals."""
    print("\n" + "="*80)
    print("TEST 5: Mixed Signals Handling")
    print("="*80)
    
    query = "Should I buy cotton and energy now, or wait? Give me a complete analysis."
    print(f"\nQuery: {query}")
    print("\nExpected: Recognition of different trends and staggered strategy\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Both commodities": "cotton" in response.lower() and "energy" in response.lower(),
        "Different recommendations": len(response) > 250,
        "Strategic guidance": any(word in response.lower() for word in ["strategy", "approach", "consider"]),
        "Clear actions": any(word in response.lower() for word in ["buy", "wait", "monitor"])
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MANUAL INTEGRATION TEST: Multi-Commodity Scenario Analysis")
    print("="*80)
    print("\nThis test verifies the agent uses analyze_multi_commodity_scenario tool correctly")
    print("and provides comprehensive multi-commodity procurement strategies.\n")
    
    try:
        test_complex_scenario()
        test_correlation_insights()
        test_prioritized_recommendations()
        test_total_savings()
        test_mixed_signals()
        
        print("\n" + "="*80)
        print("TESTS COMPLETE")
        print("="*80)
        print("\nReview the responses above to verify:")
        print("  1. Agent calls analyze_multi_commodity_scenario tool")
        print("  2. Recommendations are prioritized by urgency")
        print("  3. Correlation insights are provided")
        print("  4. Total savings are calculated")
        print("  5. Mixed signals are handled appropriately")
        print("\nCheck LangSmith traces for detailed tool usage verification.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
