# Architecture Overview

This document explains how the procurement agent is built and why certain design choices were made.

For detailed tool examples and usage patterns, see [Tools_Guide.md](Tools_Guide.md).

## System Design

The agent follows a simple flow:

1. User asks a question in the Streamlit chat
2. Agent figures out what kind of question it is
3. Agent picks the right tools to get data
4. Tools return structured data (prices, forecasts, etc.)
5. Agent combines the results into a clear answer

Think of it like having a procurement expert who knows exactly where to find information and how to analyze it.

## Components

### 1. Data Layer (`src/data/`)

**What it does:** Loads CSV and JSON files, caches them in memory.

**Key files:**
- `loader.py` - DataLoader class that handles all file I/O
- `models.py` - Data structures (HistoricalData, ForecastData, DriverData)

**Why separate this?**
- Tools don't need to know about file formats
- Caching happens in one place
- Easy to swap data sources later if needed

**How it works:**
```python
loader = DataLoader()
df = loader.load_historical("cotton_price")  # Returns pandas DataFrame
```

First call reads the file, subsequent calls return cached data. If a file is missing, returns `None` instead of crashing.

### 2. Tools Layer (`src/tools/`)

**What it does:** Provides specific analysis functions the agent can call.

**Tool categories:**
- `historical.py` - Past price queries (latest, by date, ranges, trends)
- `forecast.py` - Future predictions (confidence intervals, comparisons)
- `drivers.py` - Market factors (top drivers, correlations, lag analysis)
- `comparative.py` - Cross-commodity analysis (correlations, timing)
- `recommendations.py` - Buy/wait/monitor decisions
- `negotiation.py` - Talking points for supplier negotiations
- Plus 4 more strategic tools

**Why tools instead of direct data access?**
- Agent can't access files directly (LangChain design)
- Tools provide structured, validated data
- Each tool has a clear purpose
- Easier to test (just test the tool function)

**Example tool:**
```python
def get_latest_value(dataset_name: str) -> dict:
    """Get most recent price for a commodity."""
    loader = DataLoader()
    df = loader.load_historical(dataset_name)
    if df is None:
        return {"error": "Dataset not found"}
    
    latest = df.iloc[-1]
    return {
        "dataset": dataset_name,
        "date": latest["Period"],
        "value": latest["Value"]
    }
```

Tools return dicts, not exceptions. This makes the agent more conversational when things go wrong.

### 3. Agent Layer (`src/agent/`)

**What it does:** LangGraph ReAct agent that decides which tools to call.

**Key files:**
- `agent.py` - Main agent setup with system prompt
- `llm.py` - Ollama LLM configuration
- `tools.py` - Tool registration with LangChain

**How it works:**
1. User question comes in
2. Agent reads system prompt (tells it what tools exist)
3. Agent decides which tool(s) to call
4. Agent calls tools, gets results
5. Agent formats a natural language response

**Why LangGraph?**
- Structured workflow (better than raw LLM calls)
- Built-in tool calling
- State management for multi-turn conversations
- Easy to trace and debug

**Trade-off:** More complex than simple prompting, but much more reliable for tool-heavy tasks.

### 4. UI Layer (`src/ui/`)

**What it does:** Streamlit chat interface.

**Why Streamlit?**
- Fast to build
- Built-in chat components
- No frontend framework needed
- Good enough for a demo/prototype

**Trade-off:** Limited customization vs React, but saved weeks of development time.

## Data Flow

```
User Question
    ↓
Streamlit UI
    ↓
LangGraph Agent (decides what to do)
    ↓
Tool Selection (based on question type)
    ↓
DataLoader (loads CSV/JSON files)
    ↓
Tool Processing (calculations, analysis)
    ↓
Structured Result (dict with data)
    ↓
Agent (formats natural language response)
    ↓
Streamlit UI (displays to user)
```

**Example flow for "What's the latest cotton price?":**
1. Agent sees "latest" + "cotton price"
2. Calls `query_historical_data(dataset_name="cotton_price")`
3. Tool calls `DataLoader.load_historical("cotton_price")`
4. Returns `{"dataset": "cotton_price", "date": "2025-08-01", "value": 171.00}`
5. Agent responds: "The latest Pima Cotton Price is $171.00 per ton as of August 1, 2025."

## Design Decisions

### Why Ollama (Local LLM)?

**Decision:** Run LLM locally instead of using OpenAI/Anthropic.

**Reasons:**
- No API costs
- Data stays private (important for procurement data)
- Works offline
- Good enough for structured tool calling

**Trade-off:** Slower responses than cloud LLMs, but acceptable for this use case.

### Why Error Dicts Instead of Exceptions?

**Decision:** Tools return `{"error": "message"}` instead of raising exceptions.

**Reasons:**
- Agent can present errors conversationally
- No crashes on missing data
- Better user experience

**Example:**
```python
# Instead of:
raise DatasetNotFoundError("cotton_price not found")

# We do:
return {"error": "Dataset 'cotton_price' not found. Available: energy_futures, cotton_price, cotton_export"}
```

Agent turns this into: "I couldn't find that dataset. Did you mean cotton_price or energy_futures?"

### Why Caching in DataLoader?

**Decision:** Cache loaded data in memory.

**Reasons:**
- Same data used multiple times per question
- CSV/JSON parsing is slow
- Agent might call multiple tools

**Trade-off:** Uses more memory, but data files are small (~100KB each).

### Why 11 Tools Instead of Fewer?

**Decision:** Create specialized tools for each analysis type.

**Reasons:**
- Clear tool names help agent pick correctly
- Each tool has focused purpose
- Easier to test individual functions
- Better than one giant "analyze everything" tool

**Trade-off:** More code to maintain, but much clearer for the agent.

### Why Not Test the Agent Code?

**Decision:** Focus tests on tools and data layer, skip agent testing.

**Reasons:**
- Agent code is thin (just LangGraph setup)
- Testing LLMs is hard (non-deterministic)
- Integration tests verify end-to-end behavior
- 72% coverage is good enough for a challenge

**Trade-off:** Lower overall coverage, but tests cover the important logic.

## Trade-offs Made

### Local LLM vs Cloud
**Chose:** Local (Ollama)  
**Gained:** Privacy, no costs, offline capability  
**Lost:** Speed, latest models

### Streamlit vs React
**Chose:** Streamlit  
**Gained:** Fast development, no frontend expertise needed  
**Lost:** UI customization, mobile support

### Tool Granularity
**Chose:** 11 specialized tools  
**Gained:** Clear purposes, better agent decisions  
**Lost:** More code, more maintenance

### Test Coverage Focus
**Chose:** Test tools heavily, skip agent  
**Gained:** Fast test suite, reliable core logic  
**Lost:** Full coverage metrics

### Error Handling Approach
**Chose:** Return error dicts, not exceptions  
**Gained:** Conversational errors, no crashes  
**Lost:** Traditional error handling patterns

## Why This Architecture Works

**For this challenge:**
- Tools provide clean data access
- Agent handles natural language understanding
- Separation of concerns makes testing easier
- Local LLM keeps costs zero
- Simple enough to build in a week

**For production:**
- Would need: Cloud LLM for speed, proper error logging, rate limiting, authentication
- Would keep: Tool-based architecture, data caching, error dict pattern

## Key Takeaways

1. **Tools are the core** - They do the real work, agent just orchestrates
2. **Keep it simple** - Streamlit + Ollama + LangGraph is good enough
3. **Error handling matters** - Return dicts, don't crash
4. **Cache everything** - Data files are read many times
5. **Test what matters** - Tools and data layer, not LLM behavior

This architecture prioritizes getting a working demo quickly while keeping the code maintainable and testable.
