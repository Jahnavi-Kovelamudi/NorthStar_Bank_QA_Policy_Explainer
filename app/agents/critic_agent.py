from app.services.llm_service import call_gemini_json

def critique_answer(question: str, answer: str, planner_result: dict) -> dict:
    prompt = f"""
You are the Critic Agent for a banking support assistant.

Review the answer and check:
1. completeness
2. professional tone
3. policy-safe scope
4. whether escalation is suggested when needed
5. whether the answer avoids overpromising

Return ONLY valid JSON in this format:
{{
  "approved": true,
  "completeness": "short comment",
  "tone": "short comment",
  "policy_alignment": "short comment",
  "suggested_fix": "short comment or empty string"
}}

User question:
{question}

Planner result:
{planner_result}

Answer:
{answer}
"""
    return call_gemini_json(prompt)