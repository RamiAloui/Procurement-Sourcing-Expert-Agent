# Integration Tests

This folder contains essential integration tests that validate end-to-end agent behavior with real LLM interactions.

## Purpose

These tests complement the unit tests and validate:
- Core agent functionality with real LLM responses
- Tool registration and invocation
- LangSmith tracing integration

## Scripts

### `verify_agent.py`
Tests the LangGraph ReAct agent with sample questions:
- Simple historical queries
- Multi-step comparison queries
- Conversation with context

**Usage:**
```bash
python tests/integration/verify_agent.py
```

### `verify_langsmith.py`
Verifies LangSmith tracing integration is working correctly.

**Usage:**
```bash
python tests/integration/verify_langsmith.py
```

### `verify_tools.py`
Integration test for LangChain tool registration and invocation.

**Usage:**
```bash
python tests/integration/verify_tools.py
```

## Note

These integration tests require Ollama to be running and validate the core agent workflow. They provide practical validation of the main functionality without over-testing edge cases.
