# Code Challenge: Procurement & Sourcing Expert Agent

## Position
**Agent/LLM Developer (Junior)**

---

## Overview

You are tasked with developing an intelligent agent that acts as a **Procurement and Sourcing Expert**. The agent should be able to access and analyze procurement-related datasets and provide expert advice through a conversational chat interface.

The agent will help users make informed decisions about procurement strategies, supplier negotiations, forward-buying, production adjustments, and other sourcing-related questions based on historical data, forecasts, and market drivers.

---

## Dataset Structure

The challenge includes **3 datasets** located in the `Data/` folder:

1. **#1181-Dataset_Germany Energy Futures, Settlement Price**
2. **#1597-Dataset_Pima Cotton Price**
3. **#1616-Dataset_Pima Cotton Export Quantity**

Each dataset folder contains three files:

### 1. `historical_data.csv`
- Contains monthly historical values
- Format: `Period` (YYYY-MM-DD), `Value` (numeric)
- Provides historical context for trend analysis

### 2. `forecast.json`
- Contains forecasted values for future months
- Includes point forecasts and quantile forecasts (0.1, 0.15, 0.25, 0.5, 0.75, 0.85, 0.9)
- Provides forward-looking insights for decision-making

### 3. `drivers.json`
- Contains identified market drivers that influence the forecast
- Includes driver metadata:
  - Driver names and descriptions
  - Importance scores (overall and by forecast horizon)
  - Direction indicators (positive/negative correlation)
  - Lag information (how many months ahead/behind)
  - Correlation metrics (Pearson, Granger)
  - Normalized time series data for each driver

---

## Example Questions

The agent should be able to answer questions such as:

1. **Strategic Decision Making:**
   - "If cotton tightens + energy rises, what's the best action: forward-buy, change mix, renegotiate terms, adjust production sequencing?"
   - "What procurement strategy should I adopt given the current market conditions?"

2. **Data-Driven Negotiations:**
   - "Provide a rationale for cotton price negotiation with the supplier using market drivers and forecasts."
   - "What are the key drivers affecting cotton prices, and how can I use this in negotiations?"

3. **Forecast Analysis:**
   - "What is the forecasted price trend for cotton over the next 6 months?"
   - "What is the confidence interval for energy futures prices?"

4. **Market Analysis:**
   - "How have cotton prices changed historically, and what are the main drivers?"
   - "What is the relationship between cotton export quantity and cotton price?"

---

## Answer Quality Guidelines

When answering questions, the agent must:

1. **Use Only Available Data:** Base answers strictly on the provided datasets. Do not invent or assume data that isn't present.

2. **Clearly State Assumptions:** If any assumptions are made (e.g., about market conditions, business context), explicitly state them.

3. **Accurate Math Calculations:** Perform calculations correctly when analyzing trends, percentages, or comparing values.

4. **Data Citations (Optional but Recommended):** Reference specific data points, dates, or values when making claims. For example:
   - "Based on the forecast for September 2025 (173.48), cotton prices are expected to..."
   - "Historical data shows a peak in August 2022 (535.94) followed by..."

---

## Technical Requirements

### Required Technologies

1. **LangChain** - For building the agent framework and tooling
2. **LangGraph** - For creating the agent's decision flow and state management
3. **LangSmith** - For observability, tracing, and debugging
4. **Test Coverage** - Comprehensive unit and integration tests
5. **Chat Interface** - Any interface (CLI, web, Streamlit, Gradio, etc.) for user interaction

### LLM Provider

- You may use **any LLM provider** (OpenAI, Anthropic, Google, local models via Ollama, etc.)
- **No API keys required** in the submission - use environment variables or config files with placeholders

---

## Plus Points (Optional Enhancements)

1. **Scenario Testing:** Implement automated test coverage with predefined questions and expected answer patterns
2. **LLM as a Judge:** Use an LLM to evaluate answer quality, relevance, and accuracy

---

## Deliverables

Please provide:

1. **Full Codebase:**
   - Well-structured, documented code
   - Clear separation of concerns (data loading, agent logic, tools, interface)
   - README with setup instructions

2. **Configuration Files:**
   - Environment variable templates (`.env.example`)
   - Configuration files for LLM provider settings
   - Dependencies file (`requirements.txt`, `pyproject.toml`, or `Pipfile`)

3. **Documentation:**
   - Architecture overview
   - How to run the application
   - How to configure LLM providers
   - Explanation of key design decisions

4. **Test Suite:**
   - Unit tests for core functionality
   - Integration tests for the agent workflow
   - Test coverage report (if possible)

5. **Optional:**
   - Video demonstration or screenshots of the working chat interface
   - Performance considerations and optimizations

---

## Evaluation Criteria

Your submission will be evaluated on:

1. **Functionality:** Does the agent correctly access and analyze the data?
2. **Answer Quality:** Are answers accurate, well-reasoned, and data-driven?
3. **Code Quality:** Is the code clean, maintainable, and well-documented?
4. **Architecture:** Is the agent properly structured using LangChain/LangGraph patterns?
5. **Testing:** Is there adequate test coverage?
6. **User Experience:** Is the chat interface intuitive and responsive?
7. **Observability:** Is LangSmith properly integrated for tracing and debugging?

---

## Getting Started

1. Explore the datasets in the `Data/` folder
2. Set up your development environment
3. Design your agent architecture (consider tools for data access, analysis, and reasoning)
4. Implement the core agent using LangChain and LangGraph
5. Integrate LangSmith for observability
6. Build a chat interface
7. Write comprehensive tests
8. Document your solution

---

## Tips

- Start by understanding the data structure thoroughly
- Design tools that allow the agent to query historical data, forecasts, and drivers
- Consider creating specialized tools for different types of analysis (trend analysis, driver analysis, forecast comparison)
- Use LangGraph to create a clear decision flow (e.g., understand question → retrieve relevant data → analyze → generate answer)
- Test with various question types to ensure robustness
- Consider edge cases (missing data, ambiguous questions, etc.)

---

## Questions?

If you have any questions about the challenge, please reach out. Good luck!

---

## Submission

Please submit your solution as a Git repository (GitHub, GitLab, etc.) or as a compressed archive containing all code, documentation, and configuration files.

**Deadline:** 1 week

