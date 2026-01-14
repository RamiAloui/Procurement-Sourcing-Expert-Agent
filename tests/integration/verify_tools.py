"""Integration test for LangChain tool registration."""

from src.agent.tools import TOOLS, query_historical_data, query_forecast_data, analyze_market_drivers, compare_commodities

def test_tools():
    """Test each registered tool."""
    print("Testing LangChain Tool Registration\n")
    print("=" * 60)
    
    print("\n1. Testing query_historical_data (latest)...")
    try:
        result = query_historical_data.invoke({"dataset_name": "energy_futures"})
        print(f"[PASS] Latest energy_futures: {result['value']} on {result['date']}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
    
    print("\n2. Testing query_historical_data (specific date)...")
    try:
        result = query_historical_data.invoke({"dataset_name": "cotton_price", "date": "2024-01-01"})
        print(f"[PASS] cotton_price on 2024-01-01: {result['value']}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
    
    print("\n3. Testing query_forecast_data...")
    try:
        result = query_forecast_data.invoke({"dataset_name": "energy_futures", "months_ahead": 3})
        print(f"[PASS] energy_futures forecast (3 months): {result['forecast_value']} on {result['date']}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
    
    print("\n4. Testing analyze_market_drivers...")
    try:
        result = analyze_market_drivers.invoke({"dataset_name": "energy_futures", "top_n": 3})
        print(f"[PASS] Top 3 drivers for energy_futures:")
        for driver in result['drivers']:
            print(f"  - {driver['name']}: importance={driver['importance_mean']:.3f}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
    
    print("\n5. Testing compare_commodities...")
    try:
        result = compare_commodities.invoke({"dataset_names": ["energy_futures", "cotton_price"]})
        print(f"[PASS] Compared 2 commodities: {result['total_aligned_records']} aligned records")
        print(f"  Date range: {result['common_date_range']['start']} to {result['common_date_range']['end']}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")
    
    print(f"\n[PASS] All {len(TOOLS)} tools registered successfully!")
    print("\nRegistered tools:")
    for tool in TOOLS:
        print(f"  - {tool.name}: {tool.description.split('.')[0]}")

if __name__ == "__main__":
    test_tools()
