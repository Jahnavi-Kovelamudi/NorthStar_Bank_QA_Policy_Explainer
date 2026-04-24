from typing import List, Dict, Any
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class PlannerResult(BaseModel):
    user_intent: str
    domains: List[str]
    needs_escalation: bool
    reasoning: str

class QueryResponse(BaseModel):
    question: str
    planner: Dict[str, Any]
    matched_files: List[str]
    domain_outputs: List[Dict[str, Any]]
    final_answer: str
    output_safe: bool
    critic_feedback: Dict[str, Any]
    trace: List[str]