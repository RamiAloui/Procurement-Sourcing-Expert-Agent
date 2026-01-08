# Procurement & Sourcing Expert Agent

AI-powered agent for procurement and sourcing decisions using LangChain, LangGraph, and LangSmith.

## Overview

This project implements an intelligent agent that analyzes commodity data (Energy Futures, Cotton Price, Cotton Export) to provide strategic procurement recommendations, supplier negotiation support, and market analysis.

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

1. **Install Ollama** (local LLM - no API key required):
   ```bash
   # Download from https://ollama.ai
   ollama pull llama3.1
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   ```
   Default settings work immediately - no changes needed.

3. **(Optional)** Enable LangSmith tracing for debugging:
   - Get free API key: https://smith.langchain.com/
   - Add to `.env`: `LANGSMITH_API_KEY=your-key` and set `LANGSMITH_TRACING=true`

## Usage

(To be completed after implementation)

## Testing

(To be completed in Epic 12)

## Project Structure

```
Agents - Code Challenge/
├── src/
│   ├── agent/          # LangGraph state machine and prompts (to be implemented)
│   ├── tools/          # Analysis tools (to be implemented)
│   ├── data/           # Data loading and caching (to be implemented)
│   └── ui/             # Streamlit chat interface (to be implemented)
├── tests/              # Unit and integration tests
├── Agents - Code Challenge/
│   └── Data/           # Dataset files (3 commodities - already provided)
├── venv/               # Virtual environment
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

**Current Status:** Dependencies configured and installed (Story 1.2 complete)

## License

(To be determined)
