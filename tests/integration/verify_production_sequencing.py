"""Integration test for production sequencing recommendations."""

from src.agent.agent import invoke_agent


def test_production_sequencing():
    """Test production sequencing recommendations."""
    print("\n" + "="*80)
    print("TEST 1: Production Sequencing Recommendations")
    print("="*80)
    
    query = "Which production should I prioritize based on commodity forecasts?"
    print(f"\nQuery: {query}")
    print("\nExpected: Prioritized production sequence with rationale\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains prioritization": any(word in response.lower() for word in ["prioritize", "first", "sequence"]),
        "Contains commodities": any(word in response.lower() for word in ["cotton", "energy"]),
        "Contains rationale": len(response) > 200,
        "Well formatted": "\n" in response or "**" in response
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_favorable_identification():
    """Test identification of favorable commodities."""
    print("\n" + "="*80)
    print("TEST 2: Favorable Commodity Identification")
    print("="*80)
    
    query = "Which commodities have favorable price trends for production?"
    print(f"\nQuery: {query}")
    print("\nExpected: Clear identification of favorable vs unfavorable commodities\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Mentions favorable": "favorable" in response.lower() or "stable" in response.lower(),
        "Contains price trends": any(word in response.lower() for word in ["rising", "falling", "stable"]),
        "Multiple commodities": response.lower().count("cotton") + response.lower().count("energy") >= 2,
        "Data-backed": "$" in response or "%" in response
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_cost_impact():
    """Test cost impact explanation."""
    print("\n" + "="*80)
    print("TEST 3: Cost Impact Explanation")
    print("="*80)
    
    query = "What's the cost impact of sequencing production for cotton and energy?"
    print(f"\nQuery: {query}")
    print("\nExpected: Clear explanation of cost impact from sequencing\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Mentions cost": any(word in response.lower() for word in ["cost", "save", "savings", "impact"]),
        "Both commodities": "cotton" in response.lower() and "energy" in response.lower(),
        "Quantified": any(char.isdigit() for char in response),
        "Strategic guidance": len(response) > 250
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_timing_recommendations():
    """Test timing recommendations for production."""
    print("\n" + "="*80)
    print("TEST 4: Timing Recommendations")
    print("="*80)
    
    query = "When should I schedule production for cotton, energy, and cotton export?"
    print(f"\nQuery: {query}")
    print("\nExpected: Timing guidance for each commodity\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "All three mentioned": all(word in response.lower() for word in ["cotton", "energy"]),
        "Timing guidance": any(word in response.lower() for word in ["now", "first", "delay", "schedule"]),
        "Clear sequence": any(word in response.lower() for word in ["prioritize", "sequence", "order"]),
        "Rationale provided": len(response) > 300
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


def test_data_support():
    """Test that recommendations include data support."""
    print("\n" + "="*80)
    print("TEST 5: Data Support in Recommendations")
    print("="*80)
    
    query = "Give me production sequencing recommendations with full data support"
    print(f"\nQuery: {query}")
    print("\nExpected: Recommendations backed by specific price data\n")
    
    response = invoke_agent(query)
    print(f"Agent Response:\n{response}\n")
    
    checks = {
        "Contains prices": "$" in response,
        "Contains percentages": "%" in response,
        "Contains dates": "2025" in response,
        "Contains trends": any(word in response.lower() for word in ["rising", "falling", "stable"]),
        "Professional format": "**" in response or len(response) > 250
    }
    
    print("Verification:")
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("MANUAL INTEGRATION TEST: Production Sequencing Recommendations")
    print("="*80)
    print("\nThis test verifies the agent uses recommend_production_sequencing tool correctly")
    print("and provides clear production sequencing strategies.\n")
    
    try:
        test_production_sequencing()
        test_favorable_identification()
        test_cost_impact()
        test_timing_recommendations()
        test_data_support()
        
        print("\n" + "="*80)
        print("TESTS COMPLETE")
        print("="*80)
        print("\nReview the responses above to verify:")
        print("  1. Agent calls recommend_production_sequencing tool")
        print("  2. Favorable commodities are prioritized first")
        print("  3. Cost impact is clearly explained")
        print("  4. Recommendations include data support")
        print("  5. Sequencing is actionable and clear")
        print("\nCheck LangSmith traces for detailed tool usage verification.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
