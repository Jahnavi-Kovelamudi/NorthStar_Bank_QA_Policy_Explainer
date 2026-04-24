from fastapi import FastAPI
from app.models import QueryRequest
from app.services.orchestrator import run_workflow
import google.generativeai as genai
from app.config import GEMINI_API_KEY

app = FastAPI(title="NorthStar Bank QA Policy Explainer")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.get("/")
def root():
    return {"message": "NorthStar Bank QA Policy Explainer API is running."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def list_models():
    models = []
    for m in genai.list_models():
        models.append({
            "name": m.name,
            "supported_generation_methods": getattr(m, "supported_generation_methods", [])
        })
    return {"models": models}

@app.post("/assist")
def assist(request: QueryRequest):
    return run_workflow(request.question)

@app.post("/ask")
def ask(request: QueryRequest):
    result = run_workflow(request.question)
    return {
        "answer": result["final_answer"]
    }