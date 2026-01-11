"""Integration test for impact analysis and risk scenarios."""

from src.agent.agent import invoke_agent


def test_rising_price_impact():
    """Test impact analysis for rising prices (cotton)."""
    print("\n" + "="*80)
    print("TEST 1: Rising Price Impact Analysis (Cotton)")
    print("="*80)
    
    query = "Give me a detailed impact analysis for cotton procurement"
    print(f"\nQuery: {query}")
    print("\nExpected: Best/expected/worst case scenarios with quantified impacts")
    print("Data: Current $171, rising to ~$178.72\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains 'best'": "best" in response.lower(),
        "Contains 'worst'": "worst" in response.lower(),
        "Contains 'expected'": "expected" in response.lower(),
        "Contains dollar amounts": "$" in response,
        "Contains scenarios": "scenario" in response.lower() or "case" in response.lower(),
        "Well formatted": len(response) > 200
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_risk_quantification():
    """Test that risk is properly quantified."""
    print("\n" + "="*80)
    print("TEST 2: Risk Quantification")
    print("="*80)
    
    query = "What are the risks if I buy 2000 tons of cotton? Show me all scenarios."
    print(f"\nQuery: {query}")
    print("\nExpected: Quantified best/expected/worst scenarios for 2000 tons\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains quantity": "2000" in response or "2,000" in response,
        "Multiple scenarios": response.lower().count("case") >= 2 or response.lower().count("scenario") >= 2,
        "Contains calculations": "$" in response and any(word in response.lower() for word in ["save", "cost", "impact"]),
        "Contains confidence": any(word in response.lower() for word in ["confidence", "range", "interval"])
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_management_justification():
    """Test output suitable for management reporting."""
    print("\n" + "="*80)
    print("TEST 3: Management Justification")
    print("="*80)
    
    query = "I need to justify a cotton purchase to management. Give me a complete impact analysis."
    print(f"\nQuery: {query}")
    print("\nExpected: Professional analysis with all scenarios and data citations\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Professional tone": len(response) > 300,
        "Contains dates": "2025" in response,
        "Contains prices": "$" in response,
        "Multiple scenarios": "best" in response.lower() and "worst" in response.lower(),
        "Risk assessment": any(word in response.lower() for word in ["risk", "confidence", "range"])
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_scenario_ordering():
    """Test that scenarios are properly ordered and explained."""
    print("\n" + "="*80)
    print("TEST 4: Scenario Ordering and Clarity")
    print("="*80)
    
    query = "Show me the best case, expected case, and worst case for energy futures procurement"
    print(f"\nQuery: {query}")
    print("\nExpected: Clear explanation of each scenario with proper ordering\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Best case mentioned": "best" in response.lower(),
        "Expected case mentioned": "expected" in response.lower(),
        "Worst case mentioned": "worst" in response.lower(),
        "Contains energy": "energy" in response.lower(),
        "Clear structure": "\n" in response or "**" in response
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MANUAL INTEGRATION TEST: Impact Analysis")
    print("="*80)
    print("\nThis test verifies the agent uses calculate_impact_analysis tool correctly")
    print("and provides comprehensive risk scenarios for management decisions.\n")
    
    try:
        test_rising_price_impact()
        test_risk_quantification()
        test_management_justification()
        test_scenario_ordering()
        
        print("\n" + "="*80)
        print("TESTS COMPLETE")
        print("="*80)
        print("\nReview the responses above to verify:")
        print("  1. Agent calls calculate_impact_analysis tool")
        print("  2. All three scenarios (best/expected/worst) are presented")
        print("  3. Calculations are accurate to 2 decimal places")
        print("  4. Risk assessment is clear and actionable")
        print("  5. Output is suitable for management reporting")
        print("\nCheck LangSmith traces for detailed tool usage verification.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
