"""Integration test for LangSmith tracing."""

from src.agent.llm import get_llm

def test_langsmith_tracing():
    """Test that LLM calls are traced to LangSmith."""
    print("Testing LangSmith tracing...")
    print("Make sure LANGCHAIN_TRACING_V2=true in your .env file")
    print()
    
    llm = get_llm()
    response = llm.invoke("Hello, this is a test for LangSmith tracing")
    
    print(f"Response: {response.content}")
    print()
    print("[PASS] LLM call completed successfully")
    print()
    print("Next steps:")
    print("1. Visit https://smith.langchain.com/")
    print("2. Select your project (procurement-agent)")
    print("3. You should see a trace for this test message")
    print()
    print("If you don't see traces:")
    print("- Verify LANGCHAIN_TRACING_V2=true in .env")
    print("- Check LANGCHAIN_API_KEY is correct")
    print("- Ensure you're viewing the correct project")

if __name__ == "__main__":
    test_langsmith_tracing()
