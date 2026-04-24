# NorthStar Bank Multi-Agent Assistant

A multi-agent banking support assistant built with FastAPI, Gemini, and custom orchestration.

## Features
- Input and output guardrails
- LLM-based planner, answer, and critic agents
- Retrieval over internal banking policy documents
- Conditional Accounts, Cards, and Fraud domain agents
- Evidence-backed response traces

## Run locally
1. Create virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Add `.env` with Gemini API key
4. Run:
   uvicorn app.main:app --reload