"""Integration test for LangGraph ReAct agent functionality."""

from src.agent.agent import invoke_agent, invoke_agent_with_history

print("Test 1: Simple historical query")
print("=" * 60)
question1 = "What's the latest cotton price?"
try:
    response1 = invoke_agent(question1)
    print(f"Question: {question1}")
    print(f"Response: {response1}")
    print(" Test 1 passed - Agent responded to simple query")
except Exception as e:
    print(f"Test 1 failed: {e}")

print("\n" + "=" * 60)
print("Test 2: Multi-step comparison query")
print("=" * 60)
question2 = "Compare the latest cotton price with energy futures"
try:
    response2 = invoke_agent(question2)
    print(f"Question: {question2}")
    print(f"Response: {response2}")
    print("Test 2 passed - Agent handled multi-step query")
except Exception as e:
    print(f"Test 2 failed: {e}")

print("\n" + "=" * 60)
print("Test 3: Conversation with history")
print("=" * 60)
try:
    response3, history = invoke_agent_with_history("What's the cotton price forecast?")
    print(f"Question 1: What's the cotton price forecast?")
    print(f"Response 1: {response3}")
    
    response4, history = invoke_agent_with_history("How does that compare to energy?", history)
    print(f"Question 2: How does that compare to energy?")
    print(f"Response 2: {response4}")
    print("Test 3 passed")
except Exception as e:
    print(f"Test 3 failed: {e}")

print("\n" + "=" * 60)
print("All manual tests completed!")
print("=" * 60)
