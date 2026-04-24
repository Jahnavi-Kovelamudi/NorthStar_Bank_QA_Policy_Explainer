# NorthStar Bank QA Policy Explainer

NorthStar Bank QA Policy Explainer is a banking-support multi-agent assistant built for the **Wipro Junior FDE assignment**. It answers banking-related policy and support questions with safety guardrails, targeted retrieval, domain routing, and a simple explainable demo UI.

## Problem statement

The goal of this project is to build a realistic and defensible multi-agent system for banking support. The assistant handles banking-related questions safely, avoids processing sensitive credentials, rejects out-of-scope queries, and provides clear user-facing guidance without pretending to perform real account actions.

## Final architecture

- **Backend:** FastAPI
- **Orchestration:** Custom Python orchestration, not LangChain
- **LLM:** Gemini for Planner Agent, Answer Agent, and Critic Agent
- **Deterministic logic:** Guardrails, Retrieval, and domain routing

## Agent flow

1. Input Guardrails
2. Planner Agent
3. Retrieval Agent
4. Domain Agents (Accounts / Cards / Fraud)
5. Answer Agent
6. Output Guardrails
7. Critic Agent

## Endpoints

- `GET /health` – health check
- `POST /assist` – full internal workflow response for explainability
- `POST /ask` – final user-facing answer only

## Guardrails

The system uses both input and output guardrails.

### Input guardrails
- Block empty input
- Block sensitive credentials like OTPs, PINs, passwords, SSNs, and security answers
- Block unclear banking queries
- Block out-of-scope non-banking queries

### Output guardrails
- Block unsafe statements such as asking users to share passwords or OTPs
- Block overpromising statements such as guaranteed refunds or guaranteed fee reversals

### Example guardrail cases

- **Sensitive input:** `My OTP is 482911. Can you verify my account?` → blocked
- **Unclear input:** `help` → blocked as unclear
- **Out of scope:** `Write a poem about mountains` → blocked
- **Unsafe output pattern:** `Your refund is guaranteed` → blocked or replaced with a safe fallback

## Retrieval approach

The Retrieval Agent ranks candidate files and snippets using keyword overlap and domain-specific bonus words, then selects only the top relevant files and paragraphs instead of sending too many unrelated documents downstream.

## UI

The project includes a simple Streamlit UI with two modes:

- **Presentation mode** → calls `/ask` and shows only the final answer
- **Explainability mode** → calls `/assist` and shows planner output, matched files, domain outputs, critic feedback, and execution trace

## Local setup

### Backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload


### UI

From inside the `ui/` folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```



## Repository structure

```text
app/
  agents/
  services/
  main.py
  models.py
  config.py
ui/
  app.py
  Dockerfile
  requirements.txt
README.md
requirements.txt
```

## Screenshots
![Backend test](assets\API_Result_1.jpg)



## Assignment alignment

This project demonstrates:
- realistic multi-agent architecture,
- deterministic safety guardrails,
- targeted retrieval and domain routing,
- explainability support through `/assist`,
- live deployable backend and UI suitable for demo submission.