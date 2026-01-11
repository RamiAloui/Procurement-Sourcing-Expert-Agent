# Procurement & Sourcing Expert Agent

Automated procurement and sourcing decision support using LangChain, LangGraph, and LangSmith.

## Overview

This project implements an agent that analyzes commodity data (Energy Futures, Cotton Price, Cotton Export) to provide strategic procurement recommendations, supplier negotiation support, and market analysis.

## Setup

### Prerequisites

- Python 3.11 or higher
- Ollama (for local LLM runtime)

### Virtual Environment Setup

**Windows:**
```bash
# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Activate virtual environment
source venv/bin/activate
```

### Installation

1. Activate the virtual environment (see commands above)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Verify installation:
   ```bash
   pip list
   ```

**Installed Dependencies:**
- **AI Agent Framework:** langchain (1.2.2), langgraph (1.0.5), langsmith (0.3.45), langchain-ollama (1.0.1)
- **Data Processing:** pandas (2.2.3)
- **Chat Interface:** streamlit (1.41.1)
- **Testing:** pytest (8.3.4), pytest-cov (6.0.0)
- **Development Tools:** python-dotenv (1.0.1)

### Updating Dependencies

To update dependencies to newer versions:

1. Update version numbers in `requirements.txt`
2. Activate virtual environment
3. Run: `pip install -r requirements.txt --upgrade`
4. Test imports: `pytest tests/test_dependencies.py -v`
5. Verify no conflicts: `pip check`

**Note:** Always test thoroughly after updating dependencies to ensure compatibility.

### Troubleshooting

**Virtual environment not activating:**
- Verify path: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)

**Module not found after installation:**
- Ensure venv is active (look for `(venv)` prefix in terminal)
- Verify Python path: `python -c "import sys; print(sys.executable)"`

**Ollama connection errors:**
- Check Ollama is running: `ollama list`
- Verify URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

## Configuration

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` and update the following settings:

**LLM Configuration:**
- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_MODEL`: Model to use (recommended: `qwen3:8b` for better reasoning, or `llama3.1:8b`)
- `OLLAMA_TEMPERATURE`: Temperature for responses (default: `0.7`, range: 0.0-1.0)

**LangSmith Configuration (for observability):**
- `LANGCHAIN_TRACING_V2`: Enable tracing (default: `true`)
- `LANGCHAIN_API_KEY`: Your LangSmith API key (get from https://smith.langchain.com/)
- `LANGCHAIN_PROJECT`: Project name in LangSmith dashboard (default: `procurement-agent`)

**Data Configuration:**
- `DATA_PATH`: Path to datasets (default: `Agents - Code Challenge/Data/`)

### 3. Install and Configure Ollama

**Install Ollama:**
1. Download from https://ollama.ai
2. Install and start Ollama service:
   ```bash
   ollama serve
   ```
3. Pull a model (recommended: qwen3:8b for better reasoning):
   ```bash
   ollama pull qwen3:8b
   # Or alternatively:
   ollama pull llama3.1:8b
   ```
4. Verify installation:
   ```bash
   ollama list
   ```

**Model Recommendations:**
- **qwen3:8b** (recommended): Better reasoning capabilities for complex procurement analysis, supports thinking tokens for transparency
- **llama3.1:8b**: Stable alternative, simpler responses

### 4. Set Up LangSmith (Optional - for Observability)

LangSmith provides tracing and debugging for agent operations. This is optional but highly recommended for development.

**Create LangSmith Account:**
1. Sign up at https://smith.langchain.com/ (free tier available)
2. Go to Settings → API Keys
3. Click "Create API Key"
4. Copy the generated API key

**Add API Key to .env:**
```bash
# In your .env file, replace the placeholder:
LANGCHAIN_API_KEY=your_actual_api_key_here
```

**Verify Tracing:**
1. Run any LLM operation (the agent will automatically trace)
2. Visit https://smith.langchain.com/
3. Select your project (`procurement-agent`)
4. View traces showing LLM calls, tool usage, and agent decisions

**Troubleshooting:**
- If traces don't appear, verify `LANGCHAIN_TRACING_V2=true` in `.env`
- Check API key is correct (no extra spaces)
- Ensure you're viewing the correct project in dashboard

### 5. Verify Configuration

```bash
python -c "from src.config import get_config_summary; print(get_config_summary())"
```

This will display your current configuration (with API key masked for security).

## Usage

Run the Streamlit chat interface:
```bash
streamlit run src/ui/app.py
```

Or use the agent programmatically:
```python
from src.agent.agent import invoke_agent

response = invoke_agent("What's the latest cotton price?")
print(response)
```

## Testing

### Run Unit Tests
```bash
pytest tests/ --ignore=tests/integration/
```

**Current Status:** 198 tests passing

### Run Tests with Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term --ignore=tests/integration/
```

Open `htmlcov/index.html` in your browser to view the detailed coverage report.

**Current Coverage:** 79% (851 statements, 181 missed)

**Coverage by Module:**
- `src/data/models.py`: 100%
- `src/config.py`: 100%
- `src/tools/historical.py`: 94%
- `src/tools/drivers.py`: 90%
- `src/data/loader.py`: 89%
- `src/tools/recommendations.py`: 89%
- `src/tools/forecast.py`: 88%
- `src/tools/negotiation.py`: 88%
- `src/tools/comparative.py`: 81%

**Note:** Agent files (`src/agent/`) have 0% coverage as they require LLM integration and are tested via integration tests instead.

### Run Integration Tests
```bash
# Requires Ollama to be running
python tests/integration/verify_agent.py
python tests/integration/verify_citations.py
python tests/integration/verify_classification.py
python tests/integration/verify_conversation_context.py
python tests/integration/verify_impact_analysis.py
python tests/integration/verify_multi_commodity_scenario.py
python tests/integration/verify_production_sequencing.py
python tests/integration/verify_recommendations.py
```

**Integration Tests:** 10 verification scripts for end-to-end agent behavior

## Project Structure

```
Agents - Code Challenge/
├── src/
│   ├── agent/          # LangGraph ReAct agent and system prompts
│   ├── tools/          # Analysis tools for historical, forecast, and driver data
│   ├── data/           # Data loading and caching layer
│   └── ui/             # Streamlit chat interface
├── tests/              # Unit and integration tests
├── Agents - Code Challenge/
│   └── Data/           # Dataset files (3 commodities)
├── venv/               # Virtual environment
├── .gitignore          # Git ignore patterns
└── README.md           # This file