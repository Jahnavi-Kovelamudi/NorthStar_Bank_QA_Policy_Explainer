from app.services.llm_service import call_gemini_text

def generate_answer(question: str, planner_result: dict, retrieval_result: dict, domain_outputs: list) -> str:
    prompt = f"""
You are the Answer Agent for a banking support assistant.

You must answer using ONLY the provided domain outputs and retrieved evidence.
Do not invent policies.
Do not ask for passwords, OTPs, PINs, or account numbers.
Do not promise refunds, reversals, approvals, or account actions.
If the issue is account-specific or security-sensitive, recommend official support channels.

User question:
{question}

Planner result:
{planner_result}

Matched files:
{retrieval_result["matched_files"]}

Domain outputs:
{domain_outputs}

Write a clear, concise, user-facing answer in plain language.
"""
    return call_gemini_text(prompt)