# Integration Tests

This folder contains integration tests that validate end-to-end agent behavior with real LLM interactions.

## Purpose

These tests are **not** part of the automated unit test suite. They are used for:
- End-to-end validation of agent behavior
- Testing integrations that require external services (Ollama, LangSmith)
- Validating agent reasoning and tool selection with real LLM responses

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

These integration tests require Ollama to be running and validate the full agent workflow with real LLM responses. They complement the automated unit tests in the parent `tests/` directory.
