"""Integration test for conversation context management."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.agent import invoke_agent_with_history

print("=" * 70)
print("Testing Conversation Context Management")
print("=" * 70)

# Test 1: Basic Follow-up Question
print("\n1. BASIC FOLLOW-UP QUESTION")
print("-" * 70)
try:
    response1, history = invoke_agent_with_history("What's the latest energy price?")
    print(f"Q1: What's the latest energy price?")
    print(f"A1: {response1[:150]}...")
    
    response2, history = invoke_agent_with_history("What about cotton?", history)
    print(f"\nQ2: What about cotton?")
    print(f"A2: {response2[:150]}...")
    
    if "cotton" in response2.lower() and "price" in response2.lower():
        print("✅ Agent understood context switch to cotton price")
    else:
        print("⚠️ Agent may not have understood context")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 2: Pronoun Resolution
print("\n2. PRONOUN RESOLUTION")
print("-" * 70)
try:
    response1, history = invoke_agent_with_history("What's the cotton forecast?")
    print(f"Q1: What's the cotton forecast?")
    print(f"A1: {response1[:150]}...")
    
    response2, history = invoke_agent_with_history("What drives it?", history)
    print(f"\nQ2: What drives it?")
    print(f"A2: {response2[:150]}...")
    
    if "cotton" in response2.lower() or "driver" in response2.lower():
        print("✅ Agent resolved 'it' to cotton")
    else:
        print("⚠️ Agent may not have resolved pronoun correctly")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 3: Multi-Turn Conversation (5+ turns)
print("\n3. MULTI-TURN CONVERSATION (5 turns)")
print("-" * 70)
try:
    response1, history = invoke_agent_with_history("Compare cotton and energy")
    print(f"Turn 1: Compare cotton and energy")
    print(f"Response: {response1[:100]}...")
    
    response2, history = invoke_agent_with_history("Which is more volatile?", history)
    print(f"\nTurn 2: Which is more volatile?")
    print(f"Response: {response2[:100]}...")
    
    response3, history = invoke_agent_with_history("What are the drivers for the volatile one?", history)
    print(f"\nTurn 3: What are the drivers for the volatile one?")
    print(f"Response: {response3[:100]}...")
    
    response4, history = invoke_agent_with_history("Should I buy it now?", history)
    print(f"\nTurn 4: Should I buy it now?")
    print(f"Response: {response4[:100]}...")
    
    response5, history = invoke_agent_with_history("What's the forecast?", history)
    print(f"\nTurn 5: What's the forecast?")
    print(f"Response: {response5[:100]}...")
    
    print(f"\n✅ Multi-turn conversation completed ({len(history)} messages in history)")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 4: Context Switch
print("\n4. CONTEXT SWITCH")
print("-" * 70)
try:
    response1, history = invoke_agent_with_history("What's the energy forecast?")
    print(f"Q1: What's the energy forecast?")
    print(f"A1: {response1[:150]}...")
    
    response2, history = invoke_agent_with_history("Actually, tell me about cotton instead", history)
    print(f"\nQ2: Actually, tell me about cotton instead")
    print(f"A2: {response2[:150]}...")
    
    if "cotton" in response2.lower():
        print("✅ Agent handled context switch gracefully")
    else:
        print("⚠️ Agent may not have switched context")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test 5: State Management Efficiency
print("\n5. STATE MANAGEMENT EFFICIENCY")
print("-" * 70)
try:
    response, history = invoke_agent_with_history("What's the cotton price?")
    initial_size = len(history)
    
    for i in range(5):
        response, history = invoke_agent_with_history(f"What about turn {i+2}?", history)
    
    final_size = len(history)
    growth = final_size - initial_size
    
    print(f"Initial history size: {initial_size} messages")
    print(f"After 5 more turns: {final_size} messages")
    print(f"Growth: {growth} messages (expected: ~10 for 5 turns)")
    
    if growth <= 12:  # 2 messages per turn (user + assistant) = 10, allow some buffer
        print("✅ History grows linearly (efficient)")
    else:
        print("⚠️ History may be growing faster than expected")
except Exception as e:
    print(f"❌ Failed: {e}")

print("\n" + "=" * 70)
print("Conversation Context Testing Complete")
print("=" * 70)
print("\nNext: Check LangSmith traces to verify:")
print("- Full conversation history is visible")
print("- Agent references previous messages")
print("- Context is used in reasoning steps")
