# Financial Research Agent

## Overview

1. Executive Summary
Financial Research Agent is a Python-based multi-agent pipeline that produces structured, data-driven financial research reports. The system is designed to minimize cost and risk by separating utility work from reasoning and adding an explicit verification stage. It is built using the Google ADK framework and OpenRouter's free models.

2. Problem Statement
Retail investors face high latency and "hallucination" risks when using standard LLMs for financial data. Existing AI solutions are either too expensive (high API costs) or unreliable. Solution: A hierarchical workflow that offloads "Utility Tasks" to a local model and "Reasoning Tasks" to the cloud, ensuring data-backed accuracy through a mandatory verification layer.

3. Target Audience
Retail Investors: Seeking professional-grade market synthesis.
Financial Analysts: Requiring a "first draft" of market resilience reports.

## Architecture

- `fin_research_agent/agent.py` defines the `root_agent` pipeline using `google.adk.agents.SequentialAgent`.
- `fin_research_agent/subagents/planner.py` creates a planning agent that produces a structured research plan using a local or low-cost model.
- `fin_research_agent/subagents/writer.py` creates a writer agent that synthesizes the final report using a cloud Gemini model and on-demand market data tools.
- `fin_research_agent/subagents/verifier.py` creates a verifier agent that validates numeric outputs and flags any data mismatches.
- `fin_research_agent/skills/market_data.py` provides tool functions for fetching stock statistics and sector performance using `yfinance` and `pandas`.
- `fin_research_agent/helper.py` loads environment configuration and model settings with `python-dotenv`.
- `fin_research_agent/observability.py` initializes OpenTelemetry tracing with an OTLP exporter.

## Components

### Planner Agent
- Uses `google.adk.agents.LlmAgent` and `LiteLlm`.
- Produces a `ResearchPlan` containing 3 tickers and research rationale.
- Optimized for local or low-cost inference.

### Writer Agent
- Uses `google.adk.models.google_llm.Gemini`.
- Accepts the planning output and fetches data through two tools:
  - `get_stock_stats(symbol)`
  - `get_sector_performance(tickers)`
- Generates a financial report with executive summary, analysis, and conclusion.

### Verifier Agent
- Uses `google.adk.agents.LlmAgent` and `LiteLlm`.
- Checks drafted report values against the raw data context.
- Outputs either `CRITICAL ERROR: DATA MISMATCH` or `VERIFIED: ACCURATE`.

## Installation

1. Clone the repository.
2. Create a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy and configure environment variables:

```bash
cp env_template.txt .env
```

5. Fill `.env` with API keys and model settings.

## Configuration

The project uses environment variables defined in `.env`.
Important supported variables include:

- `GOOGLE_API_KEY`
- `OPENROUTER_API_KEY`
- `WANDB_API_KEY`
- `LOCAL_API_BASE`
- `ROOT_MODEL_NAME`
- `ROOT_MODEL_PROVIDER`
- `PLANNER_MODEL_NAME`
- `PLANNER_MODEL_PROVIDER`
- `WRITER_MODEL_NAME`
- `WRITER_MODEL_PROVIDER`
- `VERIFIER_MODEL_NAME`
- `VERIFIER_MODEL_PROVIDER`

## Usage

Import and execute the pipeline from Python:

```python
from fin_research_agent import root_agent

# Example: run the root agent in an async environment
import asyncio

async def main():
    result = await root_agent.run({})
    print(result)

asyncio.run(main())
```

> Note: The repository is not packaged for notebook execution. The `notebook/` directory is intended for experiments only and is not part of the installable package.

## Dependency Summary

The project depends on:

- `google-adk`
- `google-genai`
- `python-dotenv`
- `opentelemetry-api`
- `opentelemetry-sdk`
- `opentelemetry-exporter-otlp-proto-http`
- `yfinance`
- `pandas`
- `pydantic`

## Project Structure

- `fin_research_agent/`
  - `agent.py`
  - `helper.py`
  - `observability.py`
  - `requirements.txt`
  - `env_template.txt`
  - `skills/market_data.py`
  - `subagents/planner.py`
  - `subagents/writer.py`
  - `subagents/verifier.py`

## Notes

- The system is designed for hybrid orchestration: local models for utility and cloud models for synthesis.
- The verification stage is mandatory to reduce hallucination risk.
- Observability is integrated through OpenTelemetry and a configurable OTLP exporter.
